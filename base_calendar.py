import os
import pickle
from pathlib import Path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


class GoogleCalendar(object):
    """
    Base class to use Google Calendar API.
    """

    def __init__(self, *args, **kwargs):
        self._init_service(*args, **kwargs)

    def _init_service(self, token_path: str=None, creds_path: str=None):
        """
        Authenticate and initialize Google Calendar API service

        Parameters
        ----------
        token_path : str, default 'token.pickle'
            Path of the token.pickle file.
            The file token.pickle stores the user's access and refresh tokens,
            and is created automatically when the authorization flow completes for the first time.
        creds_path : str, default 'credentials.json'
            Path to credentials file.
            Checkout https://developers.google.com/calendar/quickstart/python to learn
            about generating and downloading credentials
        """

        creds = None
        token_path = Path(token_path or 'token.pickle')
        creds_path = Path(creds_path or 'credentials.json')

        if os.path.exists(token_path):
            with token_path.open('rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with token_path.open('wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def fetch_calendar_list(self, **kwargs) -> dict:
        """
        Get the list of available calendars and their ID.

        Parameters
        ----------
        kwargs :
            Arguments to be passed to calendarList().list method

        Returns
        -------
        Dictionary with calendar name as key and calendar ID as value

        """

        func = self.service.calendarList().list
        parser = self._calendar_list_item_parser
        calendar_list = []
        self.fetch_query_results(func, parser, calendar_list, **kwargs)
        return dict(calendar_list)

    @staticmethod
    def _calendar_list_item_parser(item: dict) -> tuple:
        """
        Parse calendar name and id from the item json object
        """

        return item.get('summaryOverride', item.get('summary', 'Other')), item['id']

    def fetch_query_results(self, func, parser, items: list, **kwargs):
        """
        Fetch, parse and combine paginated results of the query into a list.

        Parameters
        ----------
        func :
            Query function
        parser :
            Function to parse an item from the query result
        items : list
            Parsed items are appended to this list
        kwargs :
            Arguments to be passed to the query function
        """

        resp = func(**kwargs).execute()
        for item in resp['items']:
            items.append(parser(item))
        if 'nextPageToken' in resp:
            self.fetch_query_results(func, parser, items, pageToken=resp['nextPageToken'])

    def fetch_events(self, calendarId: str, parser, singleEvents: bool=True, orderBy: str='startTime',
                     **kwargs) -> list:
        """
        Fetch calendar events

        Parameters
        ----------
        calendarId : str
            ID obtained from the calendarList.list method for the required calendar
        parser :
            Function to parse an item from the query result
        singleEvents : bool, default True
            To be passed to service.events().list method
        orderBy : str, default 'startTime'
            To be passed to service.events().list method
        kwargs :
            Additional arguments to be passed to service.events().list method

        Returns
        -------
        List of parsed events
        """

        func = self.service.events().list
        events = []
        self.fetch_query_results(func, parser, events, calendarId=calendarId, singleEvents=singleEvents,
                                 orderBy=orderBy, **kwargs)
        return events


if __name__ == '__main__':
    """
    Print the list of available calendars
    """

    calendar = GoogleCalendar()
    available_calendars = calendar.fetch_calendar_list()
    print('Available calendars:')
    for k in available_calendars:
        print(k)

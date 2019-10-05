import pandas as pd
import argparse

from base_calendar import GoogleCalendar


class GoogleSportsCalendar(GoogleCalendar):

    def fetch_sports_events(self, calendar_name: str, **kwargs):
        """
        Get holidays data from Google Calendar.

        Parameters
        ----------
        region : str
            Region for which holiday calendar is required
        kwargs :
            Arguments to be passed to the events API.
        """

        calendar_list = self.fetch_calendar_list()
        if calendar_name not in calendar_list:
            error_msg = f'Calendar with name {calendar_name} not available.'
            error_msg +='\nPlease ensure that calendar name is correct and you have subscribed to the calendar'
            raise ValueError(error_msg)
        holidays = self.fetch_events(calendar_list[calendar_name], self._sports_event_parser, **kwargs)
        return pd.DataFrame(holidays, columns=['name', 'start_datetime', 'end_datetime'])

    @staticmethod
    def _sports_event_parser(item):
        """
        Parse holiday name, start date and end date from the holiday json object
        """
        return item['summary'], item.get('start',{}).get('dateTime'), item.get('end',{}).get('dateTime')


def main(calendar_name, token_path: str=None, creds_path: str=None, output_path: str=None, **kwargs):
    calendar = GoogleSportsCalendar(token_path, creds_path)
    events = calendar.fetch_sports_events(calendar_name, **kwargs)
    output_path = output_path or f'{calendar_name} Events.csv'
    print(f'Saving sports event data to {output_path} file')
    events.to_csv(output_path, index=False)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('calendar_name', help='Name of the required sports event calendar')
    argparser.add_argument('--orderBy', choices=['startTIme', 'updated'], help='Order of the events returned in the result. Default: startTime')
    argparser.add_argument('--timeMin', help="Lower bound (exclusive) for an event's end time to filter by. Must be an RFC3339 timestamp with mandatory time zone offset. Default: None")
    argparser.add_argument('--timeMax', help="Upper bound (exclusive) for an event's start time to filter by. Must be an RFC3339 timestamp with mandatory time zone offset. Default: None")
    argparser.add_argument('--creds_path', help='Path of the credentials file. Default is ./credentials.json')
    argparser.add_argument('--token_path', help='Path of the token file. Default is ./token.pickle')
    argparser.add_argument('--output_path', help='Path to store the output. Default is ./holidays_<region_name>.csv')

    args = argparser.parse_args()
    main(**vars(args))
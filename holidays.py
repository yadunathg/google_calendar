import pandas as pd
import argparse

from base_calendar import GoogleCalendar


class GoogleHolidaysCalendar(GoogleCalendar):

    def fetch_holidays(self, region: str, **kwargs):
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
        if f'Holidays in {region}' not in calendar_list:
            error_msg = f'Holiday calendar not available for region {region}.'
            error_msg +='\nPlease ensure that the region name is valid and you have subscribed to its holiday calendar'
            raise ValueError(error_msg)
        holidays = self.fetch_events(calendar_list[f'Holidays in {region}'], self._holiday_parser, **kwargs)
        return pd.DataFrame(holidays, columns=['name', 'start_date', 'end_date'])

    @staticmethod
    def _holiday_parser(item):
        """
        Parse holiday name, start date and end date from the holiday json object
        """

        return item['summary'], item.get('start',{}).get('date'), item.get('end',{}).get('date')


def main(region, token_path: str=None, creds_path: str=None, output_path: str=None, **kwargs):
    calendar = GoogleHolidaysCalendar(token_path, creds_path)
    holidays = calendar.fetch_holidays(region, **kwargs)
    output_path = output_path or f'Holidays in {region}.csv'
    print(f'Saving holidays data to {output_path} file')
    holidays.to_csv(output_path, index=False)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('region', help='Region for which holiday calendar is required')
    argparser.add_argument('--orderBy', choices=['startTIme', 'updated'], help='Order of the events returned in the result. Default: startTime')
    argparser.add_argument('--timeMin', help="Lower bound (exclusive) for an event's end time to filter by. Must be an RFC3339 timestamp with mandatory time zone offset. Default: None")
    argparser.add_argument('--timeMax', help="Upper bound (exclusive) for an event's start time to filter by. Must be an RFC3339 timestamp with mandatory time zone offset. Default: None")
    argparser.add_argument('--creds_path', help='Path of the credentials file. Default is ./credentials.json')
    argparser.add_argument('--token_path', help='Path of the token file. Default is ./token.pickle')
    argparser.add_argument('--output_path', help='Path to store the output. Default is "./Holidays In <region>.csv"')

    args = argparser.parse_args()
    main(**vars(args))
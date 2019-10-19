# Introduction

This repository contains scripts to download information about regional holidays or sports event data from Google Calendar API in a csv format.

# Requirements

Python 3.7 or later with following packages:

- pandas
- pathlib
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib

Run the following command to install the library using pip:

```python
pip3 install -U pandas pathlib google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

# Setup

Please checkout [Python Quickstart Guide](https://developers.google.com/calendar/quickstart/python) to enable Calendar API for your Google account, generate and download credentials. You will also need to subscribe to the calendar of interest to make it available for downloading. Go to <https://calendar.google.com/calendar/r/settings/browsecalendars> and select the checkbox against the calendar of interest to subscribe.

# Usage

To download Indian holidays for last, current and next year, use below command:

```python
python holidays.py India
```



Holidays for other region can be downloaded by entering respective region name as argument in the command line. To find the list of accepted region names, checkout *Regional holidays* section at <https://calendar.google.com/calendar/r/settings/browsecalendars>

To download data for sports event, run the script `sports.py` with calendar name as the command line argument:

```python
python sports.py "India ICC Cricket"
```



Calendar names for the subscribed calendars can be found under *Other calendars* section in the left pane of [Google Calendar](https://calendar.google.com/) page 

Please refer to the [Calendar API Documentation](https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/index.html) for more details.

# Extension

You can add/change the fields stored for each event by modifying the parser method. For example, to change the fields stored for regional holidays, modify the method `_holiday_parser` in `holidays.py` script. You will also need to update the column names of the dataframe in `fetch_holidays` method.

# Contact

Issues should be raised directly in the repository. For additional questions or comments please email me at yadunathkgp@gmail.com


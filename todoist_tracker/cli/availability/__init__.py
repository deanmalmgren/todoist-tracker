import httplib2
import os
import datetime
import collections

import arrow
from oauth2client.file import Storage
from apiclient import discovery

from ..base import TimeBaseCommand
from ... import tasks

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'todoist-tracker'


def iterdates(start_date, n_days):
    for n in range(0, n_days+1):
        yield start_date + datetime.timedelta(days=n)


class Command(TimeBaseCommand):
    help_text = (
        "Check availability over the coming days"
    )

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def add_command_line_options(self):
        super(Command, self).add_command_line_options()
        self.option_parser.add_argument(
            '--n-days',
            metavar='N',
            type=int,
            default=14,
            help='look N days into the future',
        )

    def execute(self, **kwargs):
        super(Command, self).execute(**kwargs)
        n_days = kwargs['n_days']

        # https://developers.google.com/google-apps/calendar/quickstart/python
        # instantiate the calendar api service
        credential_dir = os.path.join(os.path.expanduser('~'), '.credentials')
        credential_path = os.path.join(credential_dir, 'todoist-tracker.json')
        store = Storage(credential_path)
        credentials = store.get()
        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        # get all events over the next two weeks
        now = datetime.datetime.utcnow()
        future = now + datetime.timedelta(days=n_days)
        eventsResult = service.events().list(
            calendarId='primary',
            timeMin=now.isoformat() + 'Z',
            timeMax=future.isoformat() + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = eventsResult.get('items', [])

        # count the amount of meeting time per day
        #
        # NOTE: this does not work very well with double booked meetings
        daily_events = collections.Counter()
        for event in events:
            # import ipdb; ipdb.set_trace()
            start = arrow.get(event['start'].get('dateTime'))
            end = arrow.get(event['end'].get('dateTime'))
            duration = end - start
            daily_events[start.date()] += duration.seconds / 3600.0

        # count the number of tasks that are due on each day
        daily_tasks = collections.Counter()
        future_tasks = tasks.get_future(self.todoist_api, n_days)
        today = datetime.date.today()
        for task in future_tasks:
            duedate = max([tasks.get_duedate(task), today])
            daily_tasks[duedate] += self.get_hours_estimate(task)

        print "{:12s} {:>8s} {:>8s} {:>8s}".format(
            "DATE",
            "EVENTS",
            "TASKS",
            "TOTAL",
        )
        for date in iterdates(datetime.date.today(), n_days):
            print "{:12s} {:8.2f} {:8.2f} {:8.2f}".format(
                str(date),
                daily_events[date],
                daily_tasks[date],
                daily_events[date] + daily_tasks[date],
            )

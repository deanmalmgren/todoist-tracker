import os
import shutil
import glob
import datetime

import arrow

TODOIST_FORMAT = 'ddd DD MMM YYYY HH:mm:ss ZZ'


def sync(todoist_api):
    """sync the todoist api locally---ONCE per instantiation"""
    if hasattr(todoist_api, '_is_synced') and todoist_api._is_synced:
        return
    dir_contents = glob.glob(os.path.join(todoist_api.cache, '*'))
    if dir_contents:
        for f in dir_contents:
            os.remove(f)
    todoist_api.items.sync()
    todoist_api._is_synced = True


def iter_task_duedates(todoist_api):
    sync(todoist_api)
    for item in todoist_api.items.all():
        if item['due_date_utc']:
            yield item, get_duedate(item)


def get_duedate(task):
    due_datetime = arrow.get(task['due_date_utc'], [TODOIST_FORMAT])
    local_due_datetime = due_datetime.to('local')
    return local_due_datetime.date()


def get_overdue(todoist_api):
    """get overdue items from authenticated todoist_api instance"""
    overdue_items = []
    today = arrow.utcnow().to('local').date()
    for item, due_date in iter_task_duedates(todoist_api):
        if due_date <= today:
            overdue_items.append(item)
    return overdue_items


def get_future(todoist_api, n_days):
    """get future items from authenticated todoist_api instance"""
    future_items = []
    today = arrow.utcnow().to('local').date()
    future = today + datetime.timedelta(days=n_days)
    for item, due_date in iter_task_duedates(todoist_api):
        if due_date <= future:
            future_items.append(item)
    return future_items

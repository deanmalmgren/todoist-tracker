import arrow
import os
import shutil
import glob

TODOIST_FORMAT = 'ddd DD MMM YYYY HH:mm:ss ZZ'


def sync(todoist_api):
    """sync the todoist api locally---ONCE per instantiation"""
    if hasattr(todoist_api, '_is_synced') and todoist_api._is_synced:
        return
    dir_contents = glob.glob(os.path.join(todoist_api.cache, '*'))
    if dir_contents:
        for f in dir_contents:
            shutil.rmtree(f)
    todoist_api.items.sync()
    todoist_api._is_synced = True


def get_overdue(todoist_api):
    """get overdue items from authenticated todoist_api instance"""
    sync(todoist_api)
    overdue_items = []
    today = arrow.utcnow().to('local').date()
    for item in todoist_api.items.all():
        if item['due_date_utc']:
            due_datetime = arrow.get(item['due_date_utc'], [TODOIST_FORMAT])
            local_due_datetime = due_datetime.to('local')
            local_due_date = local_due_datetime.date()
            if local_due_date <= today:
                overdue_items.append(item)
    return overdue_items


def get_future(todoist_api, n_days):
    """get future items from authenticated todoist_api instance"""
    sync(todoist_api)
    future_items = []
    today = arrow.utcnow().to('local').date()
    for item in todoist_api.items.all():
        if item['due_date_utc']:
            due_datetime = arrow.get(item['due_date_utc'], [TODOIST_FORMAT])
            local_due_datetime = due_datetime.to('local')
            local_due_date = local_due_datetime.date()
            if local_due_date <= today:
                overdue_items.append(item)
    return overdue_items

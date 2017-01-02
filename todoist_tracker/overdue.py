import arrow

TODOIST_FORMAT = 'ddd DD MMM YYYY HH:mm:ss ZZ'


def get_overdue_items(todoist_api):
    """get overdue items from authenticated todoist_api instance"""
    overdue_items = []
    today = arrow.utcnow().to('local').date()
    todoist_api.items.sync()
    for item in todoist_api.items.all():
        if item['due_date_utc']:
            due_datetime = arrow.get(item['due_date_utc'], [TODOIST_FORMAT])
            local_due_datetime = due_datetime.to('local')
            local_due_date = local_due_datetime.date()
            if local_due_date <= today:
                overdue_items.append(item)
    return overdue_items

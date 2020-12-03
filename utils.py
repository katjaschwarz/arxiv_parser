from datetime import datetime
import re


def get_date(entry):
    y, m, d = entry.published.split('T')[0].split('-')
    return datetime(int(y), int(m), int(d), 0, 0, 0, 0)


def entries_on(sorted_entries, date):
    date = date.replace(minute=0, hour=0, second=0, microsecond=0)
    first, last = None, None
    for i, entry in enumerate(sorted_entries):
        entry_date = get_date(entry)
        if entry_date == date and first is None:
            first = i
        elif entry_date < date:
            last = i
            break

    return sorted_entries[first:last]


def contains(string, keywords, flaglist=None):
    if isinstance(keywords, str):
        keywords = (keywords,)

    if flaglist is None:
        flaglist = [()] * len(keywords)

    positives = filter(lambda args: bool(re.search(args[0], string, *args[1])), zip(keywords, flaglist))

    return list(map(lambda x: x[0], positives))


def clean_whitespaces(string):
    return ' '.join(string.split())


def write_in_color(string, color):
    return '<span style="color:%s"> %s </span>' % (color, string)

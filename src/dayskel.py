#!/usr/bin/env python
import os
import sys
from appscript import its, app
from datetime import datetime, timedelta

EMAIL = os.environ['ICAL_EMAIL']


def get_events(email):
    the_cal = None
    for c in app('iCal').calendars():
        if c.name() == email:
            the_cal = c
            break
    if not the_cal:
        return
    now = datetime.now()
    start = datetime(now.year, now.month, now.day)
    end = start + timedelta(1)
    return the_cal.events[(its.start_date >= start).AND(its.start_date < end)]()


def mktemplate(events):
    now = datetime.now()
    parts = ['Day Notes for %s' % now.strftime('%b %d %Y')]
    for evt in sorted(events, key=lambda evt: evt.start_date()):
        start = evt.start_date()
        end = evt.end_date()
        parts.append('[%02d:%02d—%02d:%02d] %s' % (start.hour, start.minute, end.hour, end.minute, evt.summary()))
    return '\n'.join(parts)


if __name__ == '__main__':
    events = get_events(EMAIL)
    print(mktemplate(events))

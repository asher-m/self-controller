# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:18:25 2020

@author: asher
"""

import ctypes
import datetime as dt
import subprocess
import time

# ctypes promtps:
MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000

# ctypes icons:
ICON_EXLAIM = 0x30
ICON_INFO = 0x40
ICON_STOP = 0x10

# ctypes default buttons:
DEF_BUT1 = 0x000  # default to button 1
DEF_BUT2 = 0x100  # default to button 2, etc...
DEF_BUT3 = 0x200
DEF_BUT4 = 0x300

# ctypes responses:
ID_OK = 0
ID_CANCEL = 2
ID_ABORT = 3
ID_YES = 6
ID_NO = 7

badtimes = (  # badtimes[0] <= bad <= badtimes[-1]
    dt.time(0, 30),
    dt.time(4, 30)
)

shutdown = 'shutdown -s -t 60'
shutdown_abort = 'shutdown -a'


def main():
    # Wait until it's a bad time:
    now = dt.datetime.now()
    if not badtimes[0] <= now.time() <= badtimes[-1]:
        if now.time() < badtimes[0]:
            # Sleep until later today (case after midnight before bedtime):
            time.sleep(
                (
                    dt.datetime.combine(dt.date.today(), badtimes[0]) -
                    dt.datetime.combine(dt.date.today(), now.time())
                ).total_seconds()
            )  # I hate this formatting...
        else:  # now.time() > badtimes[-1]:
            badtime_tomorrow = dt.datetime.combine(
                now + dt.timedelta(days=1),
                badtimes[0]
            )
            # Sleep until tomorrow's bedtime (ie., after midnight):
            time.sleep((badtime_tomorrow - now).total_seconds())

    while True:
        # Then start shutdown clock:
        subprocess.run(shutdown.split())

        # Ask if the user wants a delay:
        response = ctypes.windll.user32.MessageBoxW(
            None,
            "Shutdown scheduled...\nSnooze for 10 minutes?",
            "Self Controller Improved",
            MB_YESNO | ICON_INFO | DEF_BUT2
        )
        if response == ID_YES:
            subprocess.run(shutdown_abort.split())
            time.sleep(5)
        else:
            break


if __name__ == '__main__':
    main()
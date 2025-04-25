# Overview

There are three scripts in this directory:

- `extract_authentication_headers.py`
- `reserve.py`
- `schedule_booking.py`

`extract_authentication_headers.py` is a Python script that uses Playwright to log into your Lifetime account (using the username/password supplied in the .env file) and save your authentication headers to a local file. You need these headers in order to make requests to Lifetime's API. This script needs to be run sometime before you attempt to reserve a court. Otherwise, you'll fail Lifetime's authentication. It doesn't have to _immediately_ before, but it should be reasonably close.

`reserve.py` is a Python script that makes requests to Lifetime's API to book a reservation. To run it manually, you need to pass in the following arguments:

- --date: a YYYY-MM-DD date string like "2025-05-01". (You don't literally need ""s.)
- --time: an HH:MM 24-hour time string like "11:00"

By default, it tries to book court 3 for 90 minutes. You can optionally pass in --court and --duration arguments.

`schedule_booking.py` is a Python script that creates two plist files that will schedule the above scripts to run to target a specific time. It takes the same arguments as `reserve.py`. If you pass in a date argument of "2025-05-15", it will schedule an authentication refresh for May 7 at 8:55 AM Central and a booking script at 9:00 AM (targeting May 15). This is the script which has been hardest to debug; it might still need some work. But the idea is that, at any point before May 7, you can say, "I want to schedule court 3 for 11am on Thursday May 15", and running the script as `python3 schedule_booking.py --date 2025-05-08 --time 11:00` will create the tasks that will run at 8:55am and 9:00 am on May 7.

If the scheduler is not working, you can always run `extract_authentication_headers.py` and `reserve.py` manually

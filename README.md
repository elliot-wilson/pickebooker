# Overview

There are three scripts in this directory:

- `extract_authentication_headers.py`
- `reserve.py`
- `schedule_booking.py`

`extract_authentication_headers.py` is a Python script that uses Playwright to log into your Lifetime account (using the username/password you supply in the .env file) and save your authentication headers to a local file. You need these headers in order to make requests to Lifetime's API. This script needs to be run sometime shortly before you attempt to reserve a court. Otherwise, you'll fail Lifetime's authentication. It doesn't have to _immediately_ before, but it should be reasonably close.

`reserve.py` is a Python script that makes requests to Lifetime's API to book a reservation. To run it manually, you need to pass in the following arguments:

- --date: a YYYY-MM-DD date string like "2025-05-01". (You don't literally need ""s.)
- --time: an HH:MM 24-hour time string like "11:00"

By default, it tries to book court 3 for 90 minutes. You can optionally pass in --court and --duration arguments.

`schedule_booking.py` is a Python script that creates two plist files that will schedule the above scripts to run targetting a specific time. It takes the same arguments as `reserve.py`. If you pass in a date argument of "2025-05-15", it will schedule an authentication refresh for May 7 at 8:55 AM Central and a booking script at 9:00 AM (targeting May 15). This is the part which has been hardest to debug; it might still need some work. But the idea is that, at any point before May 7, you can say, "I want to schedule court 3 for 11am on Thursday May 15", and by running the script `python3 schedule_booking.py --date 2025-05-08 --time 11:00`, it will create the authentication and booking tasks that will run at 8:55am and 9:00 am on May 7 respectively.

If the scheduler is not working, you can always run `extract_authentication_headers.py` and `reserve.py` manually. Run `python3 extract_authentication_headers.py` at 8:55ish and `python3 reserve.py --date YYYY-MM-DD --time HH:MM` right at 9am.

## Setting up a local Python environment

1. Install Python from https://www.python.org/downloads/. Afterwards, if you open the Terminal program and run `python3 --version`, it should give you a response like `Python 3.11.x`.

2. Open the current Picklebooker folder in a Terminal. For example, you might be able to do this by opening the Terminal and running `cd ~/Documents/picklebooker`. (The location will depend on where you save this folder.)

3. Create a virtual environment by running these lines in your Terminal.

```
python3 -m venv .venv
source .venv/bin/activate
```

(This will allow you install the packages you need for this script in a contained way.)
You can tell whether it worked by whether you see something like `(.venv)` at the beginning of your terminal lines now.

4. Run `pip install -r requirements.txt`. This will install all the packages you need for this script.

5. Create a `.env` file that stores your username and password. The `extract_authentication_headers` script will use this to log in as you and grab your authentication headers. If you want to do this via command, you can enter this into your terminal from the root of this folder:

```
touch .env
echo "ACCOUNT_USERNAME=username" >> .env
echo "ACCOUNT_PASSWORD=1234Password" >> .env
```

Replace `username` and `password` with the correct values.

6. Add your Python venv path to the `.env` file:

```
echo "PYTHON_PATH:$(which python3)" >> .env
```

Confirm that your `.env` looks similar to the example.

7. Install `direnv` by running

```
brew install direnv
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
source ~/.zshrc
```

If you don't have Homebrew, you can install it here: https://brew.sh/

8. `cd` in and out of the Picklebooker directory:

```
cd ..
cd picklebooker
```

9. Run `direnv allow`.

10. That's it! Your virtual environment should now load whenever you CD into Picklebooker.

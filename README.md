## Prerequisites

To use this program, you'll need to build a local development environment that can run Python.

1. Make sure you have Homebrew installed. Open your `Terminal` and enter the command `brew --version`. If it responds with something like `Homebrew 4.xx.xx`, you have Homebrew. If not, install Homebrew by going to the Homebrew website (https://brew.sh/) and copying the command it gives you into your Terminal. During the installation, it may ask you to copy and paste additional commands. Do what it says. Installing Homebrew may take 15+ minutes.

2. Install Python from https://www.python.org/downloads/. Afterwards, if you open the Terminal program and run `python3 --version`, it should give you a response like `Python 3.xx.xx`.

3. Install some additional tools using Homebrew by running these commands:

- `brew install git`
- `brew install direnv`
- `brew install python-tk`

4. Enable `direnv` by running in your Terminal:

```
echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc
source ~/.zshrc
```

## Initializing this project

1. Download/sync these files from Github. In the Terminal, enter `cd ~/Documents`, then run `git clone https://github.com/elliot-wilson/picklebooker.git`. You should see the files from this website there now.

2. Make sure your Terminal is located in the Picklebooker directory by running `cd ~/Documents/picklebooker`. You might see an error message asking you to enter `direnv allow`. If so, enter `direnv allow`. You can ignore any other error messages (for example, about a missing .venv).

3. Create a virtual environment for this project. Run `python3 -m venv .venv`. Then run `cd ..; cd picklebooker`. You should see the Terminal print something like:

```
direnv: loading ~/Documents/picklebooker/.envrc
direnv: export +VIRTUAL_ENV +VIRTUAL_ENV_PROMPT ~PATH
```

4. Run `pip3 install -r requirements.txt`. This will install all the packages you need for this script.

5. Run `playwright install` to enable the `extract_authentication_headers` script to work.

6. Enter the following commands into your terminal from the root of this folder, replacing `username` and `password` with your username and password. You do not need to add any spaces or `"`s or adjust anything else in the command. Just replace the letters `username` with (e.g.) `elliotwilson`:

```
touch .env
echo "ACCOUNT_USERNAME=username" >> .env
echo "ACCOUNT_PASSWORD=1234Password" >> .env
```

6. Add your Python venv path to the `.env` file:

```
echo "PYTHON_PATH=$(which python3)" >> .env
```

## Using Picklebooker

The simplest way to run Picklebooker is to double-click

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

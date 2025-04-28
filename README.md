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

### Overview

Picklebooker is designed to let you schedule a pickleball court ahead of time. By providing the `date`, `time`, and optional `court` and `duration` values of the slot you'd like to book, you can schedule a Mac task that will attempt to book it at 9am Central 8 days in advance.

### The simple way

The simplest way to run Picklebooker is to double-click the `picklebooker.command` file. That will open a small GUI that lets you enter in the arguments for the scheduler.

If you'd like to move that command file somewhere else on your computer (e.g. to your Desktop), just edit line 2 so that it points to the absolute path of your picklebooker directory (for example, `~/Documents/picklebooker).

### Running the scripts by hand

If you don't want to rely on the scheduler, you can run the tasks by hand. This will fire them immediately.

First, you need to run `python3 extract_authentication_headers.py`. This script logs into your Lifetime account (using the username/password you supplied in the `.env` file) and saves your authentication headers to a local file. You'll need those headers to make requests to Lifetime's API. This script needs to be run shortly before you attempt to reserve a court.

Next, run `python3 reserve.py` with arguments specifying which court you want to book and when. For example, you could run `python3 reserve.py --date 2025-05-06 --time 13:00 --court 3` if you want it to book court 3 at 1:00pm on May 6th. NOTE: This script will run immediately, so if you are trying to book a court on the day of the release, you'll need to press Enter at 9am Central.

The arguments are as follows:

- --date: a YYYY-MM-DD date string like "2025-05-01". (You don't literally need ""s.)
- --time: an HH:MM 24-hour time string like "11:00"
- --court: the court number. allowed values are 1, 2, or 3. 3 is the default, so you do not _have_
- --duration: how long to reserve for. allowed values are 30, 60, or 90. 90 is the default, so you do not _have_ to supply this argument.

#!/bin/bash
set -e
echo "🧹 Cleaning up LaunchAgents and logs"
launchctl list | grep com.picklebooker | awk '{print $3}' | xargs -n 1 launchctl remove || true
rm -f ~/Library/LaunchAgents/picklebooker.*.plist
rm -f /tmp/com.picklebooker.*.out /tmp/com.picklebooker.*.err
echo "✅ Done cleaning up."
exit 0

# this script will remove all picklebooker launch agents and logs

# run chmod +x clear_schedule.command before you run this for the first time

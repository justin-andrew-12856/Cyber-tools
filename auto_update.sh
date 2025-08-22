#!/bin/bash

# =============================================================================
# Automatic Ubuntu Updater Script
#
# Description:
# This script automates the process of updating and upgrading an Ubuntu system.
# It uses 'apt' to refresh the package lists and apply any available upgrades.
# It is designed to be run non-interactively by a scheduler like cron.
#
# Author: Justin
# Date: 2024-08-22
# =============================================================================

# Define the log file path
# All output from this script will be redirected to this file.
LOGFILE="/var/log/auto_update.log"

# Use a timestamp for log entries
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "=================================================" >> $LOGFILE
echo "Auto-update script started at $TIMESTAMP" >> $LOGFILE
echo "=================================================" >> $LOGFILE

# Ensure the script is run as root, otherwise apt will fail.
if [ "$(id -u)" -ne 0 ]; then
  echo "Error: This script must be run as root." >> $LOGFILE
  exit 1
fi

# --- Step 1: Update package lists ---
# The 'apt update' command downloads the package information from all configured sources.
# This is necessary to know what packages have new versions available.
echo "Running 'apt update'..." >> $LOGFILE
apt update >> $LOGFILE 2>&1

# Check the exit code of the last command. 0 means success.
if [ $? -ne 0 ]; then
  echo "Error: 'apt update' failed. Check the log for details." >> $LOGFILE
  exit 1
fi
echo "'apt update' completed successfully." >> $LOGFILE


# --- Step 2: Upgrade installed packages ---
# The 'apt upgrade -y' command upgrades all installed packages to their latest versions.
# The '-y' flag automatically answers 'yes' to any prompts, making the command non-interactive.
echo "Running 'apt upgrade -y'..." >> $LOGFILE
apt upgrade -y >> $LOGFILE 2>&1

if [ $? -ne 0 ]; then
  echo "Error: 'apt upgrade' failed. Check the log for details." >> $LOGFILE
  exit 1
fi
echo "'apt upgrade' completed successfully." >> $LOGFILE


# --- Step 3: Clean up unused packages (Optional but recommended) ---
# The 'apt autoremove -y' command removes packages that were automatically installed
# to satisfy dependencies for other packages and are now no longer needed.
echo "Running 'apt autoremove -y' to clean up..." >> $LOGFILE
apt autoremove -y >> $LOGFILE 2>&1
echo "Cleanup completed." >> $LOGFILE

TIMESTAMP_END=$(date +"%Y-%m-%d %H:%M:%S")
echo "-------------------------------------------------" >> $LOGFILE
echo "Auto-update script finished at $TIMESTAMP_END" >> $LOGFILE
echo "-------------------------------------------------" >> $LOGFILE

exit 0


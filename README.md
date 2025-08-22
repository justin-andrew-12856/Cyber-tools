Automatic Ubuntu Updater
This project provides a simple bash script and instructions to automate the process of running sudo apt update and sudo apt upgrade on an Ubuntu system. This helps keep your system secure and up-to-date with the latest software patches and versions without manual intervention.

The script is configured to run automatically at two intervals:

Every time the system boots up.

Every 12 hours that the system is running.

How It Works
The auto_update.sh script performs the following actions:

Logs everything: It creates and appends to a log file at /var/log/auto_update.log so you can review the history of updates.

Checks for Root Privileges: It ensures it's being run by the root user, as apt requires administrative permissions.

Updates Package Lists: It runs apt update to fetch the latest list of available packages.

Upgrades Packages: It runs apt upgrade -y to install the newest versions of all your software. The -y flag is important as it automatically confirms the installation, allowing the script to run without user input.

Cleans Up: It runs apt autoremove -y to remove any old, unnecessary dependency packages.

We will use cron, the standard Linux task scheduler, to run this script automatically.

⚙️ Installation and Setup
Follow these steps carefully to set up the automated updates.

Step 1: Save the Script
First, you need to create the script file on your system. A standard location for local scripts is /usr/local/bin/.

Open your terminal.

Create and open a new file named auto_update.sh in a text editor like nano:

sudo nano /usr/local/bin/auto_update.sh

Copy the entire content of the auto_update.sh script and paste it into the nano editor.

Save the file and exit the editor by pressing Ctrl+X, then Y, then Enter.

Step 2: Make the Script Executable
By default, new files do not have permission to be executed. We need to grant this permission.

In your terminal, run the following command:

sudo chmod +x /usr/local/bin/auto_update.sh

This command modifies the file's permissions, adding the "execute" flag for all users.

Step 3: Schedule the Script with Cron
Now we'll tell the cron scheduler when to run our script. We need to edit the crontab file for the root user, since our script needs sudo privileges.

Open the root user's crontab for editing:

sudo crontab -e

If it's your first time, you may be asked to choose a default text editor. nano (option 1 or 2) is usually the easiest choice.

Scroll to the bottom of the file and add the following two lines:

# Run the auto-update script at every boot
@reboot /usr/local/bin/auto_update.sh

# Run the auto-update script every 12 hours
0 */12 * * * /usr/local/bin/auto_update.sh

What do these lines mean?

@reboot: This is a special shortcut in cron that means "run this command once, as soon as the system starts up."

0 */12 * * *: This is the standard cron schedule format.

0: At minute 0.

*/12: Every 12 hours (e.g., at 12:00 AM and 12:00 PM).

* * *: Every day of every month of every week.

Save the file and exit the editor (Ctrl+X, Y, Enter).

Cron will automatically apply these new rules. The setup is complete!

Verifying It Works
You can check if the script is running by viewing its log file.

Run this command in your terminal to see the last few entries in the log:

tail -f /var/log/auto_update.log

After a reboot or after the 12-hour mark passes, you should see new entries appear in this file, confirming that the script ran successfully. Press Ctrl+C to stop watching the log.

How to Uninstall
If you wish to stop the automatic updates:

Remove the Cron Jobs:

Open the root crontab again: sudo crontab -e

Delete the two lines you added for the auto_update.sh script.

Save and exit.

Delete the Script (Optional):

You can remove the script file with: sudo rm /usr/local/bin/auto_update.sh

Delete the Log File (Optional):


You can remove the log file with: sudo rm /var/log/auto_update.log

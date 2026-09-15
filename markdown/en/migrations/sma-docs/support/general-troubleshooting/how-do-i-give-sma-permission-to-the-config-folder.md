description:
:   Giving access to the configuration folder for SMA varies from OS.

# Snowpark Migration Accelerator: How do I give SMA permission to the config folder?

SMA requires specific folder permissions to function correctly. It needs read, write, and execute access to:

[![The modal shown when SMA is unable to access the config folder](/static/images/migrations/sma-assets/permission-denied-write-folder.png)](/static/images/migrations/sma-assets/permission-denied-write-folder.png)

- macOS: The `.config` folder
- Windows: The `AppData` folder

These folders store essential SMA files including:

- Temporary files
- Log files

Please ensure SMA has full access to the appropriate folder for your operating system.

## For macOS

1. Open the Terminal by pressing **cmd** + **spacebar**, typing `Terminal`, and pressing **enter**.
2. Navigate to your home directory by typing `cd ~` and pressing enter.
3. Change the permissions of the .config directory by typing `chmod 777 .config`. If you see “Operation not permitted,” use `sudo chmod 777 .config` instead.
4. Close the Terminal and restart the Snowpark Migration Accelerator (SMA).

### For Windows

1. Open the Run dialog window by pressing the Windows key and R key together.
2. Enter `%AppData%` in the Run dialog window and press Enter or click OK.
3. Find the “Snowflake Inc folder”, right-click on it, and verify that the Read-only checkbox under Attributes is unchecked.

[![image (17).png](/static/images/migrations/sma-assets/image(17).png)](/static/images/migrations/sma-assets/image(17).png)

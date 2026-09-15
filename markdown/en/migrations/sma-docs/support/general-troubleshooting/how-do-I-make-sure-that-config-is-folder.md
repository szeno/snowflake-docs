# Snowpark Migration Accelerator: How do I make sure that .config is a folder instead of a file?

*This problem only affects macOS systems.*

[![The modal shown when .config is a file instead of a folder](/static/images/migrations/sma-assets/config-file-not-a-folder.png)](/static/images/migrations/sma-assets/config-file-not-a-folder.png)

SMA requires read, write, and execute permissions for the configuration folder (`.config` on macOS). This folder stores temporary files, log files, and license information.

The `.config` must be a directory (folder). If you find that `.config` exists as a file, you need to convert it to a directory and set the appropriate permissions.

To resolve this issue, follow these steps:

1. Locate the `.config` file in your home directory at `'/Users/[Username]/'`.
2. Delete the `.config` file.
3. Create a new folder called `.config` in the same location.
4. Launch a command terminal.
5. Navigate to your home directory by typing the following command, then pressing Enter:

   `cd ~`
6. Change folder permissions by typing the following command:

   `chmod 777 .config`

   If you see an `Operation not permitted` error, use `sudo chmod 777 .config` instead.
7. Exit the terminal.
8. Start SMA.

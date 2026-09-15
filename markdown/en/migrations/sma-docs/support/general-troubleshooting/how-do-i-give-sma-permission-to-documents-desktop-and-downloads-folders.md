# Snowpark Migration Accelerator: How do I give SMA permission to Documents, Desktop, and Downloads folders?

A known issue exists on macOS where SMA crashes if the project directory lacks proper `read` and `write` permissions.

Please follow these steps:

1. Verify that your project is located in one of these directories:

- `Documents`: Contains your document files
- `Desktop`: Contains files and shortcuts on your desktop
- `Downloads`: Contains downloaded files

To enable access in macOS, adjust your system settings:

1. On your Mac, click the Apple menu icon, select “System Settings,” and then click “Privacy & Security” in the left sidebar.
2. Click “Files and Folders” and grant SMA access to the folders where your project is located.

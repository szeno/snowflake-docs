description:
:   Install the SMA on a Windows machine

# Snowpark Migration Accelerator: MacOS Installation

You can install the Snowpark Migration Accelerator (SMA) on macOS in two ways:

- As a desktop application
- As a Command Line Interface (CLI)

This guide explains both installation methods.

If you need the application or CLI files, please check the [Downloading and License Access page](/migrations/sma-docs/general/getting-started/download-and-access) for detailed instructions on how to obtain them.

## Installing the SMA Application on macOS

Follow these steps to install the Snowpark Migration Accelerator (SMA) application on your Mac:

1. **Open the .dmg File:** Double-click the .dmg file you downloaded.
2. **Accept the Terms:** Review and accept the software’s terms of use by clicking the **Accept** button.

[![SMA Terms of Use](/static/images/migrations/sma-assets/image(508).png)](/static/images/migrations/sma-assets/image(508).png)

1. **Move to Applications Folder:** Move the SMA application to your Applications folder by either dragging the SMA icon or double-clicking the SMA logo.

[![SMA to the Applications Folder](/static/images/migrations/sma-assets/image(509).png)](/static/images/migrations/sma-assets/image(509).png)

Once you’ve completed the installation, you can begin using the SMA application. For detailed instructions on how to use the application, refer to the [SMA User Guide](/migrations/sma-docs/user-guide/overview).

**Important Note:**

When a new version of SMA is available, you will see an “UPDATE NOW” button in the top right corner of your screen. Select this button to download and install the latest version automatically.

If you experience any problems while installing the software, email our support team at [sma-support@snowflake.com](mailto:sma-support@snowflake.com).

## Installing the SMA CLI on macOS

Here’s how to install the Snowpark Migration Accelerator (SMA) Command Line Interface on your Mac:

1. **Verify the Download:** Check that you have downloaded the correct SMA CLI installation file for macOS.
2. **Extract the Files:** Unzip the installation file contents into a folder on your computer. For example, you can use `/Users/<YourUsername>/Documents/dotnet-artifacts`.
3. **Create a Symbolic Link:** Open a terminal and execute the following command. Make sure to replace `/Users/<YourUsername>/Documents/dotnet-artifacts` with your actual extraction path. You may need administrator privileges (sudo) to run this command.

Copy code

```
sudo ln -s /Users/<YourUsername>/Documents/dotnet-artifacts/orchestrator/sma /usr/local/bin/sma
```

**Verify Installation:** Check if you can use the `sma` command by running the version check command below. This will work if `/usr/local/bin` is included in your system’s `PATH` environment variable.

Copy code

```
sma --version
```

**Check the Version:** After installation, verify the current version of the SMA CLI by running the version command.

[![SMA CLI version](/static/images/migrations/sma-assets/image(5).png)](/static/images/migrations/sma-assets/image(5).png)

After installing either the application or Command Line Interface (CLI), you can begin using the Snowpark Migration Accelerator (SMA). For detailed instructions, please refer to the [SMA User Guide](/migrations/sma-docs/user-guide/overview).

If you experience any problems while installing the software, email our support team at [sma-support@snowflake.com](mailto:sma-support@snowflake.com).

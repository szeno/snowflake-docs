description:
:   Install the SMA on a Linux machine

# Snowpark Migration Accelerator: Linux Installation

The Snowpark Migration Accelerator (SMA) offers two installation options:

- Desktop application (available for Windows and macOS users)
- Command Line Interface (CLI, available for Windows, macOS, and Linux users)

Note: Linux users can only use the CLI version.

If you need the CLI files, please check the [Downloading and Accessing page](/migrations/sma-docs/general/getting-started/download-and-access) for detailed instructions on how to get them.

## Installing the SMA CLI on Linux

Here’s how to install the Snowpark Migration Accelerator (SMA) Command Line Interface (CLI) on your Linux system:

1. **Verify the Download:** Download the SMA CLI installation file that matches your Linux system. You can find the correct download link in the [Downloading and Accessing page](/migrations/sma-docs/general/getting-started/download-and-access).
2. **Open a Terminal:** Open a terminal window and navigate to the folder containing the `SMA-CLI-linux.tar` file.
3. **Run Installation Commands:** Enter the following commands in your terminal. Note: You may need administrator privileges (sudo) to execute these commands.

Copy code

```
sudo mkdir /usr/local/share/.SMA-CLI-linux
sudo tar -xf SMA-CLI-linux.tar -C /usr/local/share/.SMA-CLI-linux
sudo ln -s /usr/local/share/.SMA-CLI-linux/orchestrator/sma /usr/local/bin/sma
```

After installation is complete, you can begin using the SMA Command Line Interface (CLI). For detailed instructions, please refer to the [SMA User Guide](/migrations/sma-docs/user-guide/overview).

**Important Note:**

When using SMA on Windows or Mac, you will see an “UPDATE NOW” notification in the top right corner if a newer version is available. Simply click the notification to download and install the latest version.

**Troubleshooting Guide:**

If you experience any problems while installing the software, please email our support team at [sma-support@snowflake.com](mailto:sma-support@snowflake.com).

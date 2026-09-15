description:
:   Install the SMA on a Windows machine

# Snowpark Migration Accelerator: Windows Installation

You can install the Snowpark Migration Accelerator (SMA) on Windows in two ways:

- As a desktop application with a graphical interface
- As a Command Line Interface (CLI)

Instructions for both installation methods are provided below.

If you need the application or CLI files, please check the [Downloading and License Access page](/migrations/sma-docs/general/getting-started/download-and-access) for detailed instructions on how to obtain them.

## Installing the SMA Application on Windows

Follow these steps to install the Snowpark Migration Accelerator (SMA) application on Windows:

1. **Run the Installer:** Double-click the downloaded installer file (with .exe extension).
2. **Follow the Installation Wizard:** A setup wizard will appear. Simply follow the prompts to install the software.
3. **Open the SMA:** After installation completes, launch the Snowpark Migration Accelerator (SMA) from your Windows Start menu.

[![SMA in Windows App Menu](/static/images/migrations/sma-assets/image(506).png)](/static/images/migrations/sma-assets/image(506).png)

After launching the application, you have two options:

- Create a new assessment or conversion project
- Open a project you have previously created

[![SMA Start Screen](/static/images/migrations/sma-assets/image(507).png)](/static/images/migrations/sma-assets/image(507).png)

Great! Now that you’ve completed the installation, you can start using the Snowpark Migration Accelerator (SMA) application. For detailed instructions on how to use SMA, please refer to the [SMA User Guide](/migrations/sma-docs/user-guide/overview).

**Important Note:**

When a newer version of SMA is available, you will see an “UPDATE NOW” button in the top right corner of your screen. Simply click this button to download and install the latest version.

If you experience any problems while installing the software, please email our support team at [sma-support@snowflake.com](mailto:sma-support@snowflake.com).

## Installing the SMA CLI on Windows

Here’s how to install the Snowpark Migration Accelerator (SMA) Command Line Interface on Windows:

1. **Download the .zip File:** Download the SMA CLI `.zip` file from the [Downloading and License Access page](/migrations/sma-docs/general/getting-started/download-and-access).
2. **Extract the Files:** Unzip the downloaded file to a location on your computer (for example, `C:sma-cli`).
3. **Copy the Orchestrator Path:** Find and copy the full path to the `orchestrator` folder in the extracted files.
   [![Orchestrator Folder Path](/static/images/migrations/sma-assets/image(12).png)](/static/images/migrations/sma-assets/image(12).png)
4. **Open Environment Variables:** Type “environment variables for your account” in the Windows search bar and select **Edit environment variables for your account**.
   [![Environment Variables Search](/static/images/migrations/sma-assets/image(11).png)](/static/images/migrations/sma-assets/image(11).png)
5. **Edit the Path Variable:** Find and select the “Path” variable in the “User variables” section, then click **Edit**.
6. **Add the Orchestrator Path:** Click **New** and paste the copied orchestrator path.
   [![Add Path Variable](/static/images/migrations/sma-assets/image.png)](/static/images/migrations/sma-assets/image.png)
7. **Save Changes:** Click **OK** twice to save and close both windows.
8. **Open a Command Prompt:** Launch a new command prompt window.
9. **Verify Installation:** Run `sma --version` to confirm the installation was successful.

[![SMA CLI Version](/static/images/migrations/sma-assets/image(13).png)](/static/images/migrations/sma-assets/image(13).png)

After installing either the application or Command Line Interface (CLI), you can begin using the Snowpark Migration Accelerator (SMA). For detailed instructions, please refer to the [SMA User Guide](/migrations/sma-docs/user-guide/overview).

If you experience any problems while installing the software, please email our support team at [sma-support@snowflake.com](mailto:sma-support@snowflake.com).

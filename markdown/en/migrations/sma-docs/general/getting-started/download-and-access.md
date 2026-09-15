description:
:   Accessing the Accelerator

# Snowpark Migration Accelerator: Downloading and Getting Access

The Snowpark Migration Accelerator (SMA) is a desktop application that helps you to convert your existing code to Snowflake’s Snowpark framework. The application runs on macOS and Windows operating systems.

## System Requirements

Before installing the Snowpark Migration Accelerator (SMA), verify that your system meets the following minimum requirements:

**MacOS:**

- macOS Ventura 13.3.1 or a newer version
- Minimum of 4 GB RAM

**Windows:**

- Windows 11
- Minimum 4 GB of RAM

Note

- Available RAM size affects the speed of conversion process, and the amount of code that can be processed at once. (More RAM is better).
- The Snowpark Migration Accelerator requires .NET and comes as a self-contained package, eliminating the need to install additional dependencies.

For detailed legal information, please review the [End User License Agreement (EULA)](/migrations/sma-docs/general/conversion-software-terms-of-use/README).

## Getting Support

If you experience any difficulties with downloading, installing, or configuring the Snowpark Migration Accelerator (SMA), please reach out to our support team at [sma-support@snowflake.com](mailto:sma-support@snowflake.com). Our team is ready to assist you!

## Downloading the SMA Application

The Snowpark Migration Accelerator (SMA) is a desktop application that runs locally on your computer. You can download the installer from the official Snowflake website:

<https://www.snowflake.com/en/migrate-to-the-cloud/modernization/>

Select the **Download Now** button on this page. This will prompt you to “DOWNLOAD SNOWFLAKE AIM” for database migration or for Spark. The Snowpark Migration Accelerator (SMA) is the “Install packages for Spark to Snowpark” option. Choose the appropriate OS for your machine to download the installer.

For step-by-step guidance on using the Snowpark Migration Accelerator (SMA) application, please refer to the [SMA User Guide](/migrations/sma-docs/user-guide/overview).

## Downloading the SMA Command Line Interface (CLI)

The SMA Command Line Interface (CLI) provides the same functionality as the graphical application but operates through text commands in a terminal. This makes it ideal for automation and scripting tasks.

Download the version that matches your operating system:

- [LINUX X64](https://sitartifacts.z5.web.core.windows.net/linux/prod/cli/SMA-CLI-linux.tar)
- [LINUX ARM](https://sitartifacts.z5.web.core.windows.net/linux/prod/cli/SMA-CLI-arm64-linux.tar)
- [MAC OS X64](https://sitartifacts.z5.web.core.windows.net/darwin_x64/prod/cli/SMA-CLI-mac.tar)
- [MAC OS ARM](https://sitartifacts.z5.web.core.windows.net/darwin_arm64/prod/cli/SMA-CLI-arm64-mac.tar)
- [WINDOWS](https://sitartifacts.z5.web.core.windows.net/windows/prod/cli/SMA-CLI-windows.zip)

For detailed guidance on using the Snowpark Migration Accelerator (SMA) Command Line Interface, refer to the [SMA CLI user guide](/migrations/sma-docs/user-guide/using-the-sma-cli/README).

Note

To migrate from a SQL database to Snowflake, please refer to the [SnowConvert AI documentation](/migrations/snowconvert-docs/overview).

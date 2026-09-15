# SnowConvert AI - Frequently Asked Questions (FAQ)

## What database platforms does SnowConvert AI translate SQL code from?

SnowConvert AI can translate SQL code from Teradata, Oracle, SQL Server, Amazon Redshift, Sybase IQ, Google BigQuery, Azure Synapse, Greenplum, PostgresSQL, Vertica, Hive, Spark, Databricks, Netezza and IBM DB2.

---

## How do I get SnowConvert AI?

SnowConvert AI can be officially downloaded in the Snowsight Snowflake web page.

However, it is highly recommended to take the free course “[SnowConvert AI for Conversion](https://training.snowflake.com/lmt/!clmsLink.dt?site=sf&region=us&lang=en-us&type=O&id=130596852)”. This course is both an overview and a technical hands on training of how to use SnowConvert AI for assessments and conversions.

If you require additional help, please contact our customer support team at [snowconvert-support@snowflake.com](mailto:snowconvert-support@snowflake.com)

---

## What are the system requirements for using SnowConvert AI?

### For MacOS

- macOS Ventura 13.3.1 or newer version
- Minimum 4 GB of RAM

### For Windows

- Windows 11 or newer version of Windows operating system
- Minimum of 4 GB RAM (more memory is recommended)

---

## How do I give permission to SnowConvert AI config folder?

Providing access to the SnowConvert AI configuration folder depends on your operating system.

[![image](/static/images/migrations/sc-assets/image(456).png "image")](/static/images/migrations/sc-assets/image(456).png)

SnowConvert AI requires read, write, and execute permissions for its configuration folder (`.config` on MacOS or `AppData` on Windows). This folder stores temporary files, logs, and license information. To grant SnowConvert AI access to this folder, follow these steps:

### For macOS

1. Open a Terminal window.
2. Navigate to your home directory by typing `cd ~` and pressing Enter.
3. Change the permissions of the .config directory by typing `chmod 777 .config`. If you receive a “Operation not permitted” error, run the command with sudo: `sudo chmod 777 .config`.
4. Close the Terminal window and launch SnowConvert AI.

### For Windows

1. Open the **Run** dialog by pressing the **Windows key + R** on your keyboard.
2. Enter `%AppData%` and press **Enter** or click **OK**.
3. Find the Snowflake Inc folder, right-click on it, and verify that the `Read-only` checkbox under Attributes is unchecked.

[![image](/static/images/migrations/sc-assets/image(455).png "image")](/static/images/migrations/sc-assets/image(455).png)

---

## How do I make sure that .config is a folder instead of a file?

*This problem only affects macOS systems.*

[![The modal shown when .config is a file instead of a folder](/static/images/migrations/sc-assets/image(1).png "image")](/static/images/migrations/sc-assets/image(1).png)

SnowConvert AI requires read, write, and execute permissions for the configuration folder (`.config` on macOS). This folder is used to store temporary files, log files, and license information.

The `.config` must be a directory (folder). If you find that `.config` exists as a file, you need to convert it to a directory and set the appropriate permissions.

To resolve this issue, follow these steps:

1. Find the `.config` file in your home directory at `'/Users/[Username]/'`.
2. Delete the `.config` file.
3. Create a new folder called `.config` in the same location.
4. Launch Terminal.
5. Navigate to your home directory by typing `cd ~` and pressing Enter.
6. Change folder permissions by typing `chmod 777 .config`. If you see an `Operation not permitted` error, use `sudo chmod 777 .config` instead.
7. Exit Terminal and start SnowConvert AI.

## What is a Top-Level Code Unit?

A Code Unit is the smallest independent piece of code that can be executed. While Code Units typically consist of individual statements, they can also be entire script files since these are executed as one unit. Code Units can be hierarchical, with some units contained within others. When a Code Unit is not nested within any other unit, it is referred to as a Top-Level Code Unit.

---

## Does SnowConvert AI provide resources to understand how it translates SQL code?

You can find the translation reference for each source in the following locations:

- [Teradata](../translation-references/teradata/README)
- [Oracle](../translation-references/oracle/README)
- [SQL Server](../translation-references/transact/README)

---

## What is the code completeness metric?

The Code Completeness score shows whether all necessary code components are present in your codebase. A score below 100 indicates that SnowConvert AI has detected missing object references that may be required for successful migration.

---

### Why my files are not being converted and marked with the code SSC-OOS-001?

Depending on the selected encoding, SnowConvert AI will not be able to parse the input; you should validate the correct encoding in the settings options before starting a conversion. [How to use the setting](getting-started/running-snowconvert/conversion/general-conversion-settings#file-encoding-settings).

---

## Are there release notes available for previous versions of SnowConvert AI?

Release notes are available here: [release-notes](../general/release-notes/release-notes/README)

---

## Is SnowConvert AI a free tool, or are there paid plans available?

SnowConvert AI is now free for everyone and allows full conversion functionality of your workload.

Besides, if you need additional support you are provided with the option of a Professional Service Engagement.

---

## Why SnowConvert AI is not auto-updating?

[![image](/static/images/migrations/sc-assets/image(535).png "image")](/static/images/migrations/sc-assets/image(535).png)

### Internet connection

SnowConvert AI automatically checks for new versions when you have an active internet connection. If you receive an error message, first verify that your system is connected to the internet and that the connection is working properly.

If you are still experiencing connection problems, it may be due to a Firewall rule blocking your access.

#### Firewall Blocked

SnowConvert AI checks for updates by connecting to a Snowflake storage service. If your local firewall blocks access to this site, you won’t be able to get updates. If you see a “Destination unreachable” message, ask your network administrator to whitelist the `https://snowconvert.snowflake.com/` website.

---

## How can I remove my licenses ?

To remove all SnowConvert AI licenses, you need to delete the `.profile` file in the config folder. The file location depends on your operating system. Follow the steps specific to your operating system to locate and delete this file.

### Windows

- Exit SnowConvert AI completely.
- Press the Windows key (`⊞ Win`) and ‘R’ key together to open the Run command window. Type `%appdata%Snowflake Inc` and press Enter.
- Find and delete the file named `.profile`.

### MacOS

- Exit SnowConvert AI if it is currently running
- Open Finder and use the keyboard shortcut `⌘ + Shift ⇧ + G` to open “Go to Folder”. Enter `~/.config/Snowflake Inc/` to access the configuration directory
- Look for the “.profile” file. On Mac systems, this is a hidden file. To view hidden files, use the keyboard shortcut `⌘ + Shift ⇧ + .`
- Find and remove the “.profile” file

After deleting the file, when you open SnowConvert AI, you will see an empty license list.

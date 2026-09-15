description:
:   Programmatically assess and convert with the SMA CLI

# Snowpark Migration Accelerator: Using the SMA CLI

## Description

The Snowpark Migration Accelerator (SMA) provides a Command Line Interface (CLI) that allows you to perform various operations. Using this CLI, you can execute the code processor, manage access codes (install or display them), and perform any other task that’s available in the SMA application.

The SMA uses a single code processor that works with all [supported source platforms](/migrations/sma-docs/user-guide/before-using-the-sma/supported-platforms). You don’t need to provide any additional arguments for this processor.

## Installation

Before installing the Command Line Interface (CLI), you need to [download it](/migrations/sma-docs/general/getting-started/download-and-access) to a location you can access. Choose the installation guide that matches your operating system:

- [Linux](/migrations/sma-docs/general/getting-started/installation/linux-installation)
- [Windows](/migrations/sma-docs/general/getting-started/installation/windows-installation)
- [MacOS](/migrations/sma-docs/general/getting-started/installation/macos-installation)

## Commands

To run the tool, you need to set up a sequence of commands based on your requirements. You can use either the **long-command** or **short-command** options with the following syntax:

Copy code

```
sma [command] [argument] [command] [argument] ...
```

The following commands are available. Click any command to view its detailed explanation.

| Long-command | Short-Command | Description |
| --- | --- | --- |
| –help | -h | Displays help documentation. |
| –version | -v | Displays current tool version. |
| install-access-code | install-ac | Installs a new access code. |
| show-access-code | show-ac | Displays all installed access codes. |
| workspace-estimator | we | Workspace Estimator commands. |
| –input | -i | Specifies the input folder location. |
| –output | -o | Specifies the output folder location. |
| –assessment | -a | Runs the tool in assessment mode. |
| [–mapDirectory](/migrations/sma-docs/user-guide/using-the-sma-cli/additional-parameters) | -m | Specifies the folder containing custom mapping files. |
| –enableJupyter | -j | Enables or disables conversion of Databricks notebooks to Jupyter format. |
| –sql | -f | Specifies which database engine syntax to use for SQL commands. |
| –customerEmail | -e | Sets the customer email address. |
| –customerCompany | -c | Sets the customer company name. |
| –projectName | -p | Sets the project name. |
| –yes | -y | Skips confirmation prompts during execution. |

Expand

Show lessSee more

### Installing an access code

With [version 3.4.0](/migrations/sma-docs/general/release-notes/README#version-340-apr-27-2026), **an access code is no longer required to run the SMA CLI**.

However, if you have an earlier version, you may still need to install an access code. You can do this in two ways:

1. Enter the access code directly
2. Provide the path to a file containing the access code (This method is helpful when you’re working offline or behind a restrictive firewall)

You can install the access code by running the following command:

Copy code

```
sma install-access-code <access-code>
```

This command produces the same result as the previous command.

Copy code

```
sma install-ac <access-code>
```

To install an access code from a file, use either the `--file` or `-f` option with your command, like this:

Copy code

```
sma install-access-code --file <path-to-file>
or
sma install-access-code -f <path-to-file>
```

If an error occurs while installing the license, an error message will be displayed.

If you are having issues related to access codes, contact [sma-support@snowflake.com](mailto:sma-support@snowflake.com).

### Checking which access codes are installed

To check which access codes are currently installed on your computer, use this command:

Copy code

```
sma show-access-code
```

This command displays details about all access codes that are currently installed on your computer.

### Converting

The SMA can run an assessment or a deterministic code conversion engine. To start the conversion process, you need to provide the following required arguments:

- **Input path:** The folder containing your original source code
- **Output path:** The folder where you want the converted code to be saved

#### Project Information

When you run the code processor for the first time, you need to provide certain arguments. These arguments will be saved and used for future executions. The required arguments are the same as those needed when [creating a new project in the application](/migrations/sma-docs/user-guide/project-overview/project-setup).

- **Customer Email:** Enter a valid email address
- **Customer Company:** Enter your company name
- **Project Name:** Enter a name for your project

This example demonstrates how to execute the code processor using only the essential requirements:

Copy code

```
sma -i <input-path> -o <output-path> -e <client email> -c <client company> -p <project name> <additional-parameters>
```

After entering the sequence of commands and pressing “Enter”, the tool will display your current settings and ask you to confirm before starting the process.

[![Current configuration before start process.](/static/images/migrations/sma-assets/image(15).png)](/static/images/migrations/sma-assets/image(15).png)

Would you like to add or modify any arguments? Type “n” to cancel or “y” to proceed.

#### Skipping the Project Confirmation

To bypass the confirmation prompt shown above, add either **–yes** or **-y** as an argument. This is particularly important when using the tool programmatically, as the confirmation prompt will appear every time without these parameters.

For more information about all available parameters, please refer to this [link](/migrations/sma-docs/user-guide/using-the-sma-cli/additional-parameters).

### Performing an Assessment

When performing an assessment, add the `--assessment` or `-a` option to the standard conversion commands. Here are examples of how the commands should look:

Copy code

```
sma --input <input-path> --output <output-path> --assessment <additional-parameters>
```

Each of these commands can accept additional parameters. For more details, please refer to the “Converting” section.

### Checking the tool version

To check the tool version and code-processing engine, you can use any of these commands:

Copy code

```
sma --version
sma -v
```

### Enabling conversion of Databricks notebooks to Jupyter Notebooks

This option converts Python (.python) and/or Scala (.scala) source files into Jupyter Notebook (.ipynb) files. The conversion works regardless of whether the original files were exported from notebooks or were regular code files.

To convert Jupyter notebooks, add either the `'--enableJupyter'` flag or its shorthand version `'-j'` to your command.

Copy code

```
sma -i <input-path> -o <output-path> --enableJupyter
```

### Setting the SQL Flavor of the source code

You can specify which SQL syntax to use when a SQL command is detected. Use either the command `'--sql'` or its shortcut `'-f'`. The supported syntax options are ‘SparkSql’ (which is the default), ‘HiveSql’, and ‘Databricks’.

Copy code

```
sma --input <input-path> --output <output-path> --sql SparkSql
sma --input <input-path> --output <output-path> --sql HiveSql
sma --input <input-path> --output <output-path> --sql Databricks
```

### Workspace Estimator

The `workspace-estimator` (or `we`) verb provides commands for estimating Databricks workspace usage. It connects to a Databricks workspace, extracts metadata, and uploads the results to Snowflake for analysis.

The following subcommands are available:

- `sma we dbx run` – Runs both extraction and upload against a Databricks workspace in a single invocation.
- `sma we dbx extract` – Extracts workspace metadata to a local `.zip` file without uploading.
- `sma we dbx upload` – Uploads a previously extracted `.zip` file to Snowflake.

For full option tables and usage examples, refer to [the Workspace Estimator section of the CLI walkthrough](/migrations/sma-docs/use-cases/sma-cli-walkthrough#label-using-the-workspace-estimator).

### Need more help?

To view general help information for the Command Line Interface (CLI), you can use any of these commands:

Copy code

```
sma --help
sma -h
```

[![Help information](/static/images/migrations/sma-assets/image(16).png)](/static/images/migrations/sma-assets/image(16).png)

To learn more about specific commands, you can execute this command:

Copy code

```
sma <command> --help
```

To learn more about installing an access code, run the command `sma install-access-code --help`.

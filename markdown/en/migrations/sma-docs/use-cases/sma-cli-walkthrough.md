description:
:   A walkthrough on using the SMA CLI

# Snowpark Migration Accelerator: SMA CLI Walkthrough

The [Snowpark Migration Accelerator (SMA)](https://www.snowflake.com/en/data-cloud/snowpark/migration-accelerator/) helps developers migrate their Python or Scala Spark code to Snowpark. It analyzes your code and:

1. Evaluates compatibility with Snowpark
2. Automatically converts compatible Spark API calls to Snowpark API
3. Identifies code that cannot be automatically converted
4. Creates an inventory of third-party library imports from scripts and notebooks
5. Generates an editable compatibility report comparing Spark and Snowpark code

Snowflake has released a Command Line Interface (CLI) for the Snowpark Migration Accelerator (SMA). This guide will demonstrate how to use the CLI both as a standalone tool and within a script.

## Using the CLI

You can download the Command Line Interface (CLI) from [the Download and Access section](/migrations/sma-docs/general/getting-started/download-and-access). Select the version that matches your operating system. You can store the CLI in any accessible location on your machine or container.

Note

**NOTE**: While this walkthrough uses screenshots from a Mac computer, the process is similar for Windows and Linux users.

After downloading the package file (.zip or .tar format), extract its contents. The Command Line Interface (CLI) tool is located in the “orchestrator” folder within the extracted files.

[![SMA CLI in the Orchestrator Directory](/static/images/migrations/sma-assets/OrchestratorDirectory.png)](/static/images/migrations/sma-assets/OrchestratorDirectory.png)

Open a terminal or command prompt in the installation folder and verify the CLI installation by running the following command to check its version:

./sma –version

You will see results that look like this:

[![SMA Version Information](/static/images/migrations/sma-assets/versionInformation.png)](/static/images/migrations/sma-assets/versionInformation.png)

The SMA Command Line Interface (CLI) is a local application that runs on your computer, similar to the SMA desktop application. To analyze your code files using the SMA CLI, these files must be stored on your local machine where the CLI can access them. The CLI supports the same file types as the regular SMA application. For a complete list of supported file types, refer to [the supported filetypes in the SMA documentation](/migrations/sma-docs/user-guide/before-using-the-sma/supported-filetypes).

Note

**NOTE**: To test the CLI functionality, you can use the sample codebase provided in [the Assessment](/migrations/sma-docs/use-cases/assessment-walkthrough/walkthrough-setup/README) section or refer to the Conversion walkthroughs in the SMA documentation.

The SMA documentation contains a complete list of CLI arguments. Let’s explore the most important ones in this section.

The SMA CLI runs in [Conversion mode](/migrations/sma-docs/user-guide/snowpark-api-conversion/README) by default, rather than [Assessment mode](/migrations/sma-docs/user-guide/assessment/README). To run the CLI in assessment mode, use [the -a argument](/migrations/sma-docs/use-cases/assessment-walkthrough/README). For conversion operations, you’ll need a valid access code. To verify if you have a valid access code, use the following command:

Copy code

```
./sma show-ac
```

[![License Information](/static/images/migrations/sma-assets/licenseInformation.png)](/static/images/migrations/sma-assets/licenseInformation.png)

To run a conversion, you need to provide:

1. Input directory (required)
2. Output directory (required)

If you haven’t created a project file before, you’ll also need to provide:

- User email
- Organization name
- Project name

Once you’ve set up these parameters for the first time, you only need to specify the input and output directories for future conversions.

Copy code

```
./sma -i '/your/INput/directory/path/here' -o '/your/OUTput/directory/path/here' -e your@email.com -c Your-Organization -p Your-Project-Name
```

This screen displays a summary of your execution settings and prompts you to confirm whether you want to proceed.

[![Project Information Section](/static/images/migrations/sma-assets/informationSection.png)](/static/images/migrations/sma-assets/informationSection.png)

To skip the confirmation prompt, add the –yes or -y parameter. This is particularly important when running the CLI from automated scripts.

The tool provides detailed progress information during its execution.

[![Project Information Printed](/static/images/migrations/sma-assets/informationPrinted.png)](/static/images/migrations/sma-assets/informationPrinted.png)

While the tool is running, it will continuously print output to the screen. When the process is complete, you will see the prompt again. The tool generates detailed output that includes all processes, issues, and completed or failed steps. You don’t need to read through all of this information while it’s running, as you can review it later in [the Logs output folder](/migrations/sma-docs/user-guide/scos-conversion/output-logs).

## Viewing the Output

The SMA CLI produces the same output as the SMA application. When you run the tool, it creates three folders in your specified output directory:

- [Reports](/migrations/sma-docs/user-guide/scos-conversion/output-reports/README)
- [Logs](/migrations/sma-docs/user-guide/scos-conversion/output-logs)
- Output (contains the converted code)

[![Output Directory from the SMA](/static/images/migrations/sma-assets/outputDirectory.png)](/static/images/migrations/sma-assets/outputDirectory.png)

For detailed guidance on working with code that has been converted by the Snowpark Migration Accelerator (SMA), refer to [the conversion walkthrough](/migrations/sma-docs/use-cases/conversion-walkthrough).

## Using the Workspace Estimator

The SMA CLI includes a [Workspace Estimator](/migrations/sma-docs/workspace-estimator/overview) verb (`we` or `workspace-estimator`) that connects to a Databricks workspace, extracts metadata such as clusters, jobs, and runs, and optionally uploads the results to Snowflake for analysis.

### Command hierarchy

The Workspace Estimator currently supports Databricks workspaces through the `dbx` subcommand. Running `sma we dbx` without a subcommand displays help listing the available subcommands:

- `sma we dbx run` – Runs both extraction and upload in a single invocation.
- `sma we dbx extract` – Extracts workspace metadata to a local `.zip` file only.
- `sma we dbx upload` – Uploads a previously extracted `.zip` file to Snowflake.

### Authentication

A Databricks Personal Access Token (PAT) is required for extraction. You can supply it in one of two ways:

1. Pass it directly with `-t` / `--token`.
2. Set the `SMA_DBX_TOKEN` environment variable. If `--token` is omitted, the CLI defaults to this variable.

### Running extraction and upload together

When you provide all required options to `sma we dbx run`, the CLI extracts workspace metadata and uploads the resulting `.zip` file in a single step.

Copy code

```
./sma we dbx run \
  -w https://adb-1234567890.azuredatabricks.net/ \
  -o ~/output/workspace-estimator \
  -n analytics-workspace \
  -c Example-Inc \
  -e user@example.com
```

The following table lists the available options for `sma we dbx run`:

| Option | Short | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--workspace-url` | `-w` | Yes | – | Databricks workspace URL (e.g. `https://adb-1234.azuredatabricks.net`). |
| `--token` | `-t` | No | `SMA_DBX_TOKEN` env var | Databricks Personal Access Token (PAT). |
| `--output-dir` | `-o` | No | Current directory | Directory where the extraction `.zip` file will be written. |
| `--workspace-name` | `-n` | Yes | – | Logical name for the workspace. Cannot be empty or whitespace. |
| `--lookback-days` | `-l` | No | 30 | Number of days to look back for cluster events (15, 30, or 60). |
| `--log-level` | – | No | Information | Minimum log level for diagnostic output (Trace, Debug, Information, Warning, Error, Critical). |
| `--company-name` | `-c` | Yes | – | Company name for this estimation. Cannot be empty or whitespace. |
| `--email` | `-e` | Yes | – | Email of the person performing the estimation. Must be a valid email address. |

Expand

Show lessSee more

### Running extraction only

To extract workspace metadata without uploading, use the `extract` subcommand. This produces a `.zip` file in the specified output directory.

Copy code

```
./sma we dbx extract \
  -w https://adb-1234567890.azuredatabricks.net/ \
  -n analytics-workspace \
  -o ~/output/workspace-estimator
```

The `extract` subcommand accepts the same options listed in the `run` table above except `--company-name` and `--email`, which are only required for upload.

### Uploading a previously extracted file

If you have already extracted workspace metadata to a `.zip` file, you can upload it separately using the `upload` subcommand.

Copy code

```
./sma we dbx upload \
  -i ~/output/workspace-estimator/workspace-extraction.zip \
  -n analytics-workspace \
  -c Example-Inc \
  -e user@example.com
```

The following table lists the available options for `sma we dbx upload`:

| Option | Short | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `--input-zip` | `-i` | Yes | – | Path to an existing `.zip` file to upload. The file must have a `.zip` extension. |
| `--company-name` | `-c` | Yes | – | Company name for this estimation. Cannot be empty or whitespace. |
| `--email` | `-e` | Yes | – | Email of the person performing the estimation. Must be a valid email address. |
| `--workspace-name` | `-n` | Yes | – | Logical name for the workspace. Cannot be empty or whitespace. |
| `--log-level` | – | No | Information | Minimum log level for diagnostic output (Trace, Debug, Information, Warning, Error, Critical). |

Expand

Show lessSee more

## Running the CLI Programmatically

Coming soon! The SMA team will provide a script that enables you to run the SMA Command Line Interface (CLI) automatically across multiple directories.

---

Try out the Command Line Interface (CLI) today. If you need help or have questions, contact the Snowpark Migration Accelerator team at [sma-support@snowflake.com](mailto:sma-support@snowflake.com).

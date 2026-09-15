# Set up the Snowflake CLI to develop an app

Feature — Generally Available

The Snowflake Native App Framework is generally available on supported cloud platforms. For additional information, see
[Support for private connectivity, VPS, and government regions](/developer-guide/native-apps/limitations#label-native-apps-supported-clouds).

This topic describes how providers install and use the Snowflake CLI for developing and managing
Snowflake Native Apps. Snowflake CLI is an open-source command-line tool explicitly designed for developer-centric
workloads in addition to SQL operations.

## Install and configure the Snowflake CLI

To install and configure the Snowflake CLI, follow these steps:

1. Install the Snowflake CLI for your operating system.

   For more information, see [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation).
2. Set up a connection to your Snowflake account.

   For more information, see [Configuring Snowflake CLI](/developer-guide/snowflake-cli/connecting/configure-cli).

## About Snowflake CLI projects and app templates

When using the Snowflake CLI to develop your Snowflake Native App, you work within a project. A project is a directory
that contains all the files and directories required for your Snowflake Native App. Like other code repositories,
these files can be version-controlled using technologies like Git and shared on platforms like Github.

Snowflake provides app templates that you can use to set up your project. These templates are available
in the [snowflake-cli-templates GitHub repository](https://github.com/snowflakedb/snowflake-cli-templates).

The available templates are:

| **Template** | **Description** |
| --- | --- |
| app\_basic | A basic template that includes the essential files and directories required for your app. |
| app\_streamlit\_java | A template that includes the essential files and directories required for your app, Java extension code, and sample Streamlit app. |
| app\_streamlit\_js | A template that includes the essential files and directories required for your app, JavaScript extension code, and sample Streamlit app. |
| app\_streamlit\_python | A template that includes the essential files and directories required for your app, Python extension code, and sample Streamlit app. |

Expand

Show lessSee more

## Set up a new project for your Snowflake Native App

To set up a new project for your Snowflake Native App, follow these steps:

1. Run the `init` command to create a new project:

   Copy code

   ```
   snow init --template <template_name> <project_name>
   ```
2. Enter a value for the project identifier.

   This value is used as a base name for the app components that Snowflake CLI creates, including the
   application package. You can modify or override this value later in the project definition file.

After running this command, a new directory named `<project_name>` is created in the directory
where you ran the command. This directory contains the files and directories required for your Snowflake Native App
with the following directory structure:

```
<project_name>/
├── app/
 ├── manifest.yml
 ├── README.md
 ├── setup_script.sql
├── README.md
├── snowflake.yml
```

The folders and files in this directory are described in the following table:

| **File/Directory** | **Description** |
| --- | --- |
| `app/` | This directory contains the application code and resources for your app. You can modify or add files in this directory as needed. |
| `app/manifest.yml` | This file defines the metadata and configuration for your app, including the app name, version, description, and resources. See [Create the manifest file for an app](/developer-guide/native-apps/manifest-overview) for more information. |
| `app/README.md` | This file provides an overview of your app and instructions for using it. This is the README file that is displayed in the Snowflake Marketplace |
| `app/setup_script.sql` | This SQL script is executed when the app is installed. You can modify this script to include any setup steps required for your app. For more information, see [Create the setup script](/developer-guide/native-apps/creating-setup-script) |
| `README.md` | This file provides an overview of the project and instructions for using the Snowflake CLI with your app. |
| `snowflake.yml` | This is the project definition file that describes the objects that can be deployed to Snowflake. You must modify this file to define the resources that are part of your app. |

Expand

Show lessSee more

## Create the project definition file

Snowflake CLI uses a project definition file to describe objects that can be deployed to Snowflake. This
file must be named `snowflake.yml`. This file determines the name of the application package and
specifies the resources that are part of your Snowflake Native App.

For more information about the project definition file, see
[Project definition files](/developer-guide/snowflake-cli/native-apps/project-definitions).

The following is an example of a simple `snowflake.yml` file used for a Snowflake Native App:

Copy code

```
definition_version: 2
entities:
  hello_snowflake_package:
    type: application package
    stage: stage_content.hello_snowflake_stage
    manifest: app/manifest.yml
    identifier: hello_snowflake_package
    artifacts:
       - src: app/*
         dest: ./
  hello_snowflake_app:
    type: application
    from:
       target: hello_snowflake_package
    debug: false
```

The following table describes the fields in this example:

| **Field** | **Description** |
| --- | --- |
| `definition_version` | The version of the project definition file format. The current version is 2. |
| `entities` | A list of entities that are part of the project. Each entity has a unique identifier and a type. |
| `hello_snowflake_package` | The identifier for the application package entity. This name is used as a base name for the app components that Snowflake CLI creates, including the application package. |
| `type` | The type of entity. In this case, it is an `application package`. |
| `stage` | The stage where the application package is stored. |
| `manifest` | The path to the manifest file that defines the metadata and configuration for your app. |
| `identifier` | The identifier for the application package entity. This name is used as a base name for the app components that Snowflake CLI creates, including the application package. |
| `artifacts` | A list of files and directories that are included in the application package. Each artifact has a source (`src`) and a destination (`dest`). |
| `hello_snowflake_app` | The identifier for the application entity. |
| `from` | Specifies the source of the application. In this case, it is created from the `hello_snowflake_package` application package. |
| `debug` | A boolean value that indicates whether debug mode is enabled for the app. |

Expand

Show lessSee more

## Develop your Snowflake Native App

After setting up your project and creating the project definition file, you can start developing
your Snowflake Native App by creating the application package and modifying the manifest file and setup script.

For more information, see the following topics:

- [Create and manage an application package](/developer-guide/native-apps/creating-app-package)
- [Create the manifest file for an app](/developer-guide/native-apps/manifest-overview)
- [Create the setup script](/developer-guide/native-apps/creating-setup-script)

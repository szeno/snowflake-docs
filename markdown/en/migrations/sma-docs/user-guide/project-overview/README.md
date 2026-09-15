description:
:   Configuration, setup, and everything else you need to know

# Snowpark Migration Accelerator: Project Overview

The Snowpark Migration Accelerator (SMA) helps developers analyze and convert existing Spark code to Snowpark code. This tool simplifies the process of understanding your codebase and automatically translates Spark API references to their Snowpark API equivalents.

How Does SMA Work?

This section explains the core functionality and processes. You will learn about:

- [Project Creation and Setup](/migrations/sma-docs/user-guide/project-overview/project-setup)
- [Configuration and Settings](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings)
- [Running the Tool](/migrations/sma-docs/user-guide/project-overview/tool-execution)

Let’s define two important concepts you’ll encounter when using this tool:

1. Project: This represents a single execution or run of the tool. Each time you use the tool, it creates a new project.
2. Readiness Score: This is the main metric used to evaluate your results. It indicates how prepared your code is for migration.

## What is a SnowConvert Project?

To use this accelerator, you first need to create a project. A project links your tool executions with your configuration settings. When you create a project, the tool generates a .snowct file in your source code directory. This file stores all your project information on your local machine, including:

- The source platform you selected
- Your conversion settings
- The project status

## What is the Readiness Score?

The readiness score measures how well your Spark API code can be mapped to equivalent Snowpark API functions. While a high score indicates good compatibility between Spark and Snowpark elements, it does not guarantee that your entire codebase will run successfully in Snowflake. The readiness score serves as an initial assessment tool, but you should consider additional factors when evaluating if your application is suitable for Snowpark migration.

For additional technical terms and definitions, please refer to our [glossary](/migrations/sma-docs/support/glossary).

Let’s begin with the project setup…

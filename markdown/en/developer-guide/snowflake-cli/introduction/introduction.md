# Introducing Snowflake CLI

Snowflake CLI’s open-source nature means that developers can leverage the community’s collective knowledge and contributions to
improve and enhance the tool. By using Snowflake CLI, developers can expect a streamlined, efficient experience that empowers
them to work with Snowflake in new and innovative ways. Snowflake CLI is a powerful and flexible tool that helps developers
streamline their workflow and optimize their Snowflake experience.

As a command-line interface (CLI), Snowflake CLI provides several benefits for developers, such as:

- Speed and efficiency

  A CLI allows developers to perform tasks quickly and efficiently by executing commands from the
  terminal without needing a graphical user interface. This can save developers significant time and effort, especially
  when performing repetitive or complex tasks.
- Automation

  A CLI can automate tasks and workflows, such as building, testing, CI/CD, and deploying applications.
  A CLI can help developers streamline their development process and reduce the risk of errors or inconsistencies.
- Portability

  A CLI is often platform-independent and can be used across different operating systems and environments.
  Developers can work more easily on multiple projects or collaborate with others who use different systems.
- Version control

  A CLI can be integrated with version control systems like Git to manage changes and track code
  history, which can help developers collaborate more effectively, resolve conflicts, and document changes appropriately.
- Customization

  A CLI can be customized and extended by using modules and scripts, so developers can tailor it to
  their needs and preferences. Automating common tasks and workflows can help developers work more efficiently
  and effectively.
- Accessibility

  A CLI can be accessed remotely, so developers can work on servers and other remote
  systems without a graphical interface.

## How does Snowflake CLI differ from SnowSQL?

Snowflake CLI is the preferred command-line client for running SQL and for managing workloads and applications that
connect to Snowflake. SnowSQL is a legacy command-line client for SQL queries, DDL, DML, and loading or unloading data.
Snowflake will only add new features and enhancements to Snowflake CLI. Snowflake supports SnowSQL 1.5.x through April 16, 2028.

Snowflake CLI also lets you locally run and debug Snowflake apps, with the following benefits:

- You can search, create, and upload Python packages that might not be supported in Anaconda yet.
- Snowflake CLI supports Snowpark Python user-defined functions and stored procedures, warehouses, and Streamlit apps.
- You can define packages by using `requirements.txt`, with dependencies automatically added
  through integration with Anaconda at deployment time.
- Snowflake CLI can include packages that are identified in `requirements.txt`, but aren’t yet in
  Anaconda, in the application package deployed to Snowflake.
  (This feature only works with packages that don’t rely on native libraries.)
- When you update existing applications, code and dependencies are automatically altered as needed.
- Deployment artifacts are automatically managed and uploaded to Snowflake stages.

If you already use SnowSQL, see [Migrating from SnowSQL to Snowflake CLI](/user-guide/snowsql-migrate).

## Security considerations

Caution

Some Snowflake CLI commands execute code from your project directory, including subdirectories, or fetch and execute content from remote URLs. Only run Snowflake CLI commands on projects, packages, and SQL sources you trust.

## Next steps

- [Installing Snowflake CLI](/developer-guide/snowflake-cli/installation/installation)
- [Configuring Snowflake CLI and connecting to Snowflake](/developer-guide/snowflake-cli/connecting/connect)

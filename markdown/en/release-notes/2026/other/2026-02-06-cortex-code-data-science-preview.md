# Feb 06, 2026: Cortex Code data science and machine learning skill (*Preview*)

The Cortex Code CLI now offers the *Data Science and Machine Learning skill*, allowing it to more accurately detect when you want to perform data science or machine learning operations as part of your request. This skill defines how Cortex Code should interact with Snowflake components used for machine learning and data science, including interactions with a Model Registry and running inference on Snowpark Container Services.

This skill is automatically loaded into Cortex Code’s context when needed, allowing you to focus on your agent requests rather than determining up front what information the agent might need to succeed at your task.

The data science and machine learning skill is built in to Cortex Code. [Install the Cortex Code CLI](/user-guide/cortex-code/cortex-code-cli) or run `cortex update` from the command line to update to the latest version. If you’d like to inspect the prompts that make up the data science skill, use the `/skill` command or ask Cortex Code `What does the machine learning and data science skill do?`.

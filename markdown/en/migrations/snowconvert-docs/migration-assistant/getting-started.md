# SnowConvert AI - Migration Assistant - Getting Started

This guide will walk you through the SnowConvert AI Migration Assistant’s basic steps to resolve post-conversion issues in your SQL code.

## Prerequisites

- You have installed the Snowflake Visual Studio Code extension version **GA** **1.14.0** or later.

Warning

Please be aware that the documentation has been updated to reflect changes in version 1.17.0. The streaming feature, along with some instruction changes, e.g, [Billing](#billing), are only available in version 1.17.0 or newer.

- You have **.sql** files that contain EWIs from SnowConvert.
- You have a Snowflake account with access to any of the supported models. For more information, please check the [Model Preference documentation](#model-preference).

## Steps

### 1. Install the Snowflake Visual Studio Code extension

See Snowflake documentation on how to install from the [Visual Studio Marketplace](https://docs.snowflake.com/en/user-guide/vscode-ext#install-the-vs-code-extension-from-visual-studio-marketplace) or from a [.vsix file](https://docs.snowflake.com/en/user-guide/vscode-ext#install-the-vs-code-extension-from-a-vsix-file).

Be sure you’re using version **GA** **1.14.0** or later.

### 2. Sign in to Snowflake with the Visual Studio Code extension

See Snowflake documentation on how to [sign in](https://docs.snowflake.com/en/user-guide/vscode-ext#sign-in-to-snowflake-with-the-vs-code-extension) to Snowflake using the VS Code extension.

### 3. Enable SnowConvert AI Migration Assistant in the Snowflake VS Code Extension Settings

Open the VS Code settings panel and navigate to Extensions. Select the Snowflake extension, and open the settings panel for the Snowflake extension.

[![Settings panel > Extensions](/static/images/migrations/sc-assets/MigrationAssistantSettingsPanelExtension.png "Settings panel > Extensions")](/static/images/migrations/sc-assets/MigrationAssistantSettingsPanelExtension.png)

Settings panel > Extensions

[![Snowflake extension > settings](/static/images/migrations/sc-assets/MigrationAssistantSnowflakeExtensionSettings.png "Snowflake extension > settings")](/static/images/migrations/sc-assets/MigrationAssistantSnowflakeExtensionSettings.png)

Snowflake extension > settings

In the Snowflake extension settings, you must:

- Check “Enable SnowConvert AI Migration Assistant”

[![Enable SnowConvert AI Migration Assistant setting](/static/images/migrations/sc-assets/MigrationAssistantEnableMigrationAssistant.png "Enable SnowConvert AI Migration Assistant setting")](/static/images/migrations/sc-assets/MigrationAssistantEnableMigrationAssistant.png)

Enable SnowConvert AI Migration Assistant setting

### 4. Set up Model Preference

For more information about how to set up the model preference, please check the [Model Preference](#model-preference) documentation.

### 5. Open a workspace folder containing SnowConvert AI migration results

First, ensure you have a workspace folder open in Visual Studio Code. Then, access the Snowflake extension by selecting its icon from the activity bar on the left. A “SnowConvert AI Issues” panel will appear at the bottom within the Snowflake extension’s view. This panel automatically populates with a list of all folders and files in the current workspace that have SnowConvert AI migration issues. If no workspace is selected, the following message is prompted on the SnowConvert AI Issues panel: “No SnowConvert AI Migration issues found.”

[![SnowConvert AI Issue panel](/static/images/migrations/sc-assets/MigrationAssistantSnowConvertIssuePanel.png "SnowConvert AI Issue panel")](/static/images/migrations/sc-assets/MigrationAssistantSnowConvertIssuePanel.png)

SnowConvert AI Issue panel

Once your workspace folder containing SnowConvert AI migration issues is open, you can access the toolbar by hovering over the “SnowConvert AI Issues” panel. This toolbar in the panel’s top-left corner allows you to interact with the list of migration issues identified.

[![SnowConvert AI Issues panel toolbar](/static/images/migrations/sc-assets/MigrationAssistantSnowConvertIssuePanelToolbar.png "SnowConvert AI Issues panel toolbar")](/static/images/migrations/sc-assets/MigrationAssistantSnowConvertIssuePanelToolbar.png)

SnowConvert AI Issues panel toolbar

- **🏠 (Return to Workspace Root):** Clicking this icon resets the view to display the entire workspace folder’s initial state.
- **📁 (Select Folder):** Allows you to navigate to and select a specific subfolder within your workspace to focus the issue list.
- **🔄 (Refresh Issues):** Use this to update the list of SnowConvert AI migration issues manually. The list will also update automatically whenever an issue is resolved or a new one is detected.
- **➖ (Collapse All):** Collapses all expanded items in the issues list for a more compact view.

### 6. See SnowConvert AI Migration Issues and click the sparkles for help resolving

Once you’ve opened a folder containing .sql files with migration issues, you will see a list of all the EWIs, FDMs, and PRFs in that folder and the files containing them. Clicking on a migration issue from the list will focus the code editor on the line of code where the issue was found.

[![SnowConvert AI Migration Issues panel](/static/images/migrations/sc-assets/MigrationAssistantSnowconvertMigrationIssuesPanel.png "SnowConvert AI Migration Issues panel")](/static/images/migrations/sc-assets/MigrationAssistantSnowconvertMigrationIssuesPanel.png)

SnowConvert AI Migration Issues panel

Note

**EWIs** are indicated by the ⚠️ icon.

**FDMs and PRFs** are indicated by the ℹ️ icon.

The folder icon changes from 📁 (collapsed) to 📂 (expanded) to reflect its state.

There are two ways to get AI-powered assistance and recommended solutions for a migration issue:

1. Click the sparkles icon located next to the migration issue in the list.

[![Get explanation and suggestion by sparkles icon](/static/images/migrations/sc-assets/MigrationAssistantSuggestionSparklesIcon.png "Get explanation and suggestion by sparkles icon")](/static/images/migrations/sc-assets/MigrationAssistantSuggestionSparklesIcon.png)

Get explanation and suggestion by sparkles icon

2. Click on the CodeLenses identified by *SnowConvert AI, which are* located above every migration issue.

[![Get explanation and suggestion by CodeLens](/static/images/migrations/sc-assets/MigrationAssistantSuggestionCodeLens.png "Get explanation and suggestion by CodeLens")](/static/images/migrations/sc-assets/MigrationAssistantSuggestionCodeLens.png)

Get explanation and suggestion by CodeLens

### 7. Get help

Once you click the sparkles icon or the CodeLenses, the SnowConvert AI Migration Assistant will query Snowflake Cortex AI with the migration issue and a snippet of the code context surrounding the migration issue. The call to Cortex happens entirely within your Snowflake account, using the connection details you configured in the Snowflake VS Code Extension.

Once a result has been generated, it will appear in a panel to the right of the code editor. The result will contain an explanation of the migration issue in the context of your code, and a suggested fix to make the code run correctly on Snowflake. If the assistant is unable to generate a response with high confidence, it will abstain from providing a recommended solution.

[![Explanation and suggestion panel](/static/images/migrations/sc-assets/MigrationAssistantExplanationSuggestionPanel.png "Explanation and suggestion panel")](/static/images/migrations/sc-assets/MigrationAssistantExplanationSuggestionPanel.png)

Explanation and suggestion panel

### 8. Interacting with the Migration Assistant

- **Refine Solutions:** If an AI suggestion is incorrect or you prefer a different approach, enter your preferred changes or instructions into the chatbox.
- **Ask SQL-Related Questions:** If the suggestion is correct, you can still ask for clarifications or further explanations on any SQL-related topic.
- **Request Code Modifications:** You can also ask for specific code changes, such as adding a header to your script.

[![SnowConvert AI Migration Assistant chat interaction](/static/images/migrations/sc-assets/MigrationAssistantChatInteraction.png "SnowConvert AI Migration Assistant chat interaction")](/static/images/migrations/sc-assets/MigrationAssistantChatInteraction.png)

SnowConvert AI Migration Assistant chat interaction

Note

The assistant will refrain from answering non-SQL-related questions.

[![Non-SQL related question abstention message](/static/images/migrations/sc-assets/MigrationAssistantNonSqlRelatedQuestion.png "Non-SQL related question abstention message")](/static/images/migrations/sc-assets/MigrationAssistantNonSqlRelatedQuestion.png)

Non-SQL related question abstention message

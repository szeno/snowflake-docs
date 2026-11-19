## Quick start for Snowflake AIM for Data Warehouses App

### Prerequisites

Ensure the following are installed on your platform:

1. [Python](https://www.python.org/downloads)
2. [Git](https://git-scm.com/install)
3. [Snowflake CoCo CLI](/user-guide/cortex-code/cortex-code-cli)
4. [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli/installation)
5. Download links for the Snowflake AIM for Data Warehouses app:

- [macOS Apple Silicon](https://snowconvert.snowflake.com/storage/darwin_arm64/beta/aim/Snowflake-AIM-arm64-Pr.dmg)
- [macOS Intel](https://snowconvert.snowflake.com/storage/darwin_x64/beta/aim/Snowflake-AIM-x64-Pr.dmg)
- [Windows x64](https://snowconvert.snowflake.com/storage/windows/beta/aim/Snowflake-AIM-Setup-x64-Pr.exe)
- [Windows arm64](https://snowconvert.snowflake.com/storage/windows_arm64/beta/aim/Snowflake-AIM-Setup-arm64-Pr.exe)

### Starting the Snowflake AIM for Data Warehouses app for the first time

1. After installing and starting the app for the first time, you will see something like this
   [![](/static/images/migrations/migration-agent-assets/quick-start-connect-snowflake.png)](/static/images/migrations/migration-agent-assets/quick-start-connect-snowflake.png)
   If you have been using CoCo or Snowflake locally in your environment, you will see a list of Snowflake connections you’ve defined previously. Otherwise, you’ll need to click “+ Add new connection” to define one.
   Either way, a connection to a Snowflake account that allows you to use CoCo CLI is required.
2. After you click Next, the app will test your connection and make sure you have access to CoCo as shown below:

[![](/static/images/migrations/migration-agent-assets/quick-start-connection-ready.png)](/static/images/migrations/migration-agent-assets/quick-start-connection-ready.png)

3. Once your connection is verified and you click Continue, you will be asked to start a project as show below:
   [![](/static/images/migrations/migration-agent-assets/quick-start-create-project.png)](/static/images/migrations/migration-agent-assets/quick-start-create-project.png)

Since this is the first time you are using this app, click on “Create a new project”. You will be presented with the following dialog
[![](/static/images/migrations/migration-agent-assets/quick-start-point4.png)](/static/images/migrations/migration-agent-assets/quick-start-point4.png)

If you select “Pick one for me”, a new project folder will be created under ~/.scai/projects
If you want to decide where you want the project folder to be, click on “Select a directory…” and in the subsequent dialog, create a new folder in the desired location

To come back to a project you created earlier, select the project name in the app header to open the project menu. Recently opened projects are listed there. To open a project folder that isn’t in the list, select **Open existing project…** and choose the project folder.

4. Once the project folder is determined, AIM will guide you through your project
   [![](/static/images/migrations/migration-agent-assets/quick-start-point5.png)](/static/images/migrations/migration-agent-assets/quick-start-point5.png)

Note the left panel that shows you what stage in the project setup you are at.
Once you complete setup and go through the migration, the left panel will contextually update.

At this point, simply follow the AIM agent’s guidance. If you’re not sure what the project status is or what you should do next, you can always ask the AIM agent a question such as “What’s the current project status?” or “What’s next?”

### Providing feedback

In the screenshots above, you may have noticed a **Feedback** tab at the bottom left of the app. Use it to report a bug or to send any other feedback, which we would greatly appreciate. Select **Feedback**, or press ⌘K (macOS) or Ctrl+K (Windows), to open the **Send feedback** form.
[![](/static/images/migrations/migration-agent-assets/quick-start-point6.png)](/static/images/migrations/migration-agent-assets/quick-start-point6.png)

1. Describe the issue: what you did, what you expected, and what happened.
2. Optionally, select a **Severity**: **Low**, **Medium** or **High**.
3. Select **Submit**.

The app sends the AIM team your description and severity, along with recent diagnostics: the latest SnowConvert AI log, recent Snowflake CoCo and app errors, the versions of the tools AIM uses, and your machine’s CPU count and memory. Before anything is sent, secrets, email addresses and URLs in that text are masked. Your conversation is not sent, and neither is a screenshot.

The app doesn’t save a feedback file for you to send. When your feedback is delivered, the form shows **Sent to the AIM team**. If it can’t be delivered right away, the form shows **Queued — it will send the next time the app connects to Snowflake**. The feedback then stays on your computer until the app can deliver it.

Sending feedback needs a Snowflake connection. If the form has no **Submit** button, add a Snowflake connection in **Settings**, then try again.

### Legal Notices

The Snowflake AIM for Data Warehouses App is Client Software governed by your Agreement with Snowflake. Unlike Snowconvert AI, the Snowflake AIM for Data Warehouses App is not subject to the Conversion Software Terms of Use.

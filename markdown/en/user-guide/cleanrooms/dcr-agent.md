# Snowflake Data Clean Rooms Agent

[Preview Feature](/release-notes/preview-features) — Open

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## Overview

The Snowflake Data Clean Room (DCR) Agent offers a conversational interface in Snowflake CoWork, making data clean rooms intuitive and accessible for business
and non-technical users. It facilitates key workflows, including the effortless execution of
approved analyses, with results presented in an easy-to-understand format.

The agent currently supports the following Snowflake Data Clean Rooms templates:

- **Audience Overlap:** A template that measures how many records overlap between two datasets.
- **Audience Overlap Activation:** A template that generates a list of overlapping records with respective attributes, and exports it to an
  approved account.

See [Overlap and activation](/user-guide/cleanrooms/collab-overlap-and-activation#label-dcr-collab-overlap-activation-downloads) for collaboration roles, sample data, and setup notebooks for this scenario. The notebooks generate sample datasets based on data from the public DCR sample dataset.

The agent uses Claude Sonnet 4.6 as the LLM.

## Supported flows

The DCR Agent can currently perform the following actions in a collaboration:

- Join a collaboration.
- View information about a collaboration, including the status, templates, and data offerings in that collaboration.
- Run an audience overlap analysis in a collaboration.
- Activate data from an overlap analysis.
- View the analysis history for any analyses run using the agent in this account.

## Requirements

- Ensure you are on API version 15.6 or later
- Complete [Agent setup](#label-dcr-agent-setup) and [Access requirements](#label-dcr-access-requirements) in this topic.

### Agent setup

Run the following SQL in an account to enable agent functionality:

Copy code

```
-- Enable cross-region inference.
USE ROLE ACCOUNTADMIN;
ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'AWS_US';

-- Ensure DCR application has the appropriate grants via caller.
GRANT CALLER FULL MANAGEMENT ON ACCOUNT TO APPLICATION SAMOOHA_BY_SNOWFLAKE;
```

Register the DCR agent with Snowflake CoWork so users can access it in the Snowflake CoWork interface:

Copy code

```
USE ROLE ACCOUNTADMIN;
CREATE SNOWFLAKE INTELLIGENCE IF NOT EXISTS SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT;
ALTER SNOWFLAKE INTELLIGENCE SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT
  ADD AGENT SAMOOHA_BY_SNOWFLAKE.AGENTS.SNOWFLAKE_DCR_AGENT;
```

### Access requirements

DCR Agent and Data Clean Rooms permissions are managed separately. To use the agent, you need permissions on both the agent and the collaboration. Grant the proper permissions as follows:

1. Grant the role permission to use the DCR Agent and access it in Snowflake CoWork:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   GRANT USAGE ON SNOWFLAKE INTELLIGENCE SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT
     TO ROLE <your role name>;
   CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.ADMIN.GRANT_PRIVILEGE_ON_ACCOUNT_TO_ROLE(
     'USE DCR AGENT',
     '<your role name>'
   );
   ```
2. Grant the role permission to run analyses in a collaboration by calling [GRANT\_PRIVILEGE\_ON\_OBJECT\_TO\_ROLE](/user-guide/cleanrooms/collaboration-api-reference#label-grant-privilege-on-object-to-role):

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.ADMIN.GRANT_PRIVILEGE_ON_OBJECT_TO_ROLE(
     'RUN',
     'COLLABORATION',
     '<collaboration name>',
     '<your role name>'
   );
   ```

Note

**SAMOOHA\_APP\_ROLE** must still have **USE DCR AGENT** granted separately to use the Snowflake Data Clean Room Agent.

## Usage

After setting up your collaboration, run an analysis and activate results using the agent. There are two ways to access the agent:

- Log in to Snowsight and in the navigation menu, select **AI & ML** » **Snowflake CoWork**.
- Directly navigate to <https://ai.snowflake.com/>.

Note

If a role has all required permissions to join a collaboration, you can also request the agent to join a current collaboration your account is invited to. If any data offerings need to be added, this will need to be done via the Collaboration API or Snowsight UI.

### Run an analysis and activate results

From Snowflake CoWork, ask the agent to run an analysis in the collaboration that you joined. You can also ask the agent what actions you can perform, what data is available, what templates are available, and other contextual questions.

If activation is enabled in your collaboration, you can ask the agent to activate analysis results to available destinations in the collaboration.

### Save analysis results

Ask the agent to save an overlap analysis result by providing a name for the saved analysis. You can later list or fetch your saved analyses by name.

You can view only analyses that you have run yourself. Administrators using the SAMOOHA\_APP\_ROLE role can see analysis results for all analyses.

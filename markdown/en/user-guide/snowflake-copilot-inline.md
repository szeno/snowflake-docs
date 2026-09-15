# Using Snowflake Copilot inline

Important

Snowflake Copilot inline now uses Cortex Code. To learn more about Cortex Code, see [Cortex Code in Snowsight](/user-guide/cortex-code/cortex-code-snowsight).

Snowflake Copilot inline is an expansion of the existing Snowflake Copilot experience that gives you the ability to query Snowflake Copilot from within your SQL code. For information about Snowflake Copilot, see [Using Snowflake Copilot](/user-guide/snowflake-copilot).

Snowflake Copilot inline is only supported in Workspaces. For information about Workspaces, see [Workspaces](/user-guide/ui-snowsight/workspaces).

Note

Snowflake Copilot inline is natively supported in the following regions:

- AWS US West 2 (Oregon)
- AWS US East 1 (N. Virginia)
- Azure US East 2 (Virginia)

To use Snowflake Copilot in other regions, set the `CORTEX_ENABLED_CROSS_REGION` parameter.
Within this parameter, you can either:

- Provide a list of values that include at least one of the supported regions.
- Set it to `ANY_REGION`.

For information about how to use the `CORTEX_ENABLED_CROSS_REGION` parameter, see [Choosing a routing option](/user-guide/snowflake-cortex/cross-region-inference#label-use-cross-region-inference).

## Access control requirements

The COPILOT\_USER database role in the SNOWFLAKE database includes the privileges that allow users to use Snowflake Copilot features. By default,
the COPILOT\_USER role is granted to the PUBLIC role. The PUBLIC role is automatically granted
to all users and roles, so this allows all users in your account to use Snowflake Copilot features.

In addition to the COPILOT\_USER requirement, users must have the CORTEX\_USER role. The CORTEX\_USER database role in the SNOWFLAKE database includes the privileges that allow users to call Snowflake AI functions. By default, the CORTEX\_USER role is granted to the PUBLIC role. The PUBLIC role is automatically granted to all users and roles, so this allows all users in your account to use the Snowflake AI functions.

Snowflake Copilot inline requires that the user has access to the `claude-3.5-sonnet` or `openai-gpt-4.1` model. To ensure all users have access to this model, make sure that `claude-3.5-sonnet` or `openai-gpt-4.1` is included in the model allowlist and is not limited by role-based access control (RBAC). For more information about controlling model access, see [Control model access](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-access-control).

If users have the correct permissions, they see the Snowflake Copilot inline sparkle icon in Workspaces. They can use the inline interface to interact with Snowflake Copilot.

To remove access to Copilot inline, you must revoke access to either CORTEX\_USER or COPILOT\_USER. If you don’t want all users to have this privilege, you can revoke access to the PUBLIC role and grant access to specific roles. For example, to revoke access from the PUBLIC role, use the following query:

Copy code

```
USE ROLE ACCOUNTADMIN;

REVOKE DATABASE ROLE SNOWFLAKE.COPILOT_USER
  FROM ROLE PUBLIC;

REVOKE DATABASE ROLE SNOWFLAKE.CORTEX_USER
  FROM ROLE PUBLIC;
```

You can then grant access as needed. For information about limiting access to Snowflake Copilot, see [Limit access to Copilot](/user-guide/snowflake-copilot#label-snowflake-copilot-limit).

## Supported use cases

- **Explore your data** by asking open-ended questions to learn about the structure and nuances of a new dataset.
- **Generate SQL queries** with questions in natural language.
- **Improve your queries** by asking Snowflake Copilot to help you assess query efficiency, find optimizations, or explain what the query does.
- **Fix syntax errors** by asking Snowflake Copilot to fix your query.

## Limitations

Snowflake Copilot inline has the following limitations:

- **Support for the following languages:**
  - English
  - French
  - German
  - Spanish
  - Italian
  - Portuguese
  - Arabic
  - Hindi
  - Chinese
  - Japanese
  - Korean
  - SQL

No access to your data
:   Snowflake Copilot does not have access to the data inside your tables. If you want to filter on a particular value of a column, you should provide that value. For example, if you ask Snowflake Copilot to return all rows with a column A value equal to “X”, you should provide the value “X” in your request. For more information, see the [Construct and run a SQL Statement](#label-snowflake-copilot-inline-construct-sql-example) example.

Delayed response
:   Snowflake Copilot might take a second to complete a response, depending on the length of the response provided.

SQL suggestions may not always work
:   Snowflake Copilot may sometimes suggest queries that contain invalid SQL syntax or non-existent tables or columns.

Delay in detecting new databases, schemas, and tables
:   It may take up to 3-4 hours for Snowflake Copilot to recognize newly created databases, schemas, and tables.

Limited number of tables and columns considered
:   To generate a response, Snowflake Copilot first searches for tables and columns most relevant for your request. The search results are then ranked by relevancy and only the top 10 tables and top 10 columns from each of those tables in the results are considered when generating a response.

Snowflake Copilot inline does not support feedback
:   You cannot upvote or downvote the suggestions that Snowflake Copilot inline gives you.

## How to use Snowflake Copilot inline

> Snowflake Copilot inline requires no additional setup. Remember the following points when using Snowflake Copilot:

- Each session with Snowflake Copilot inline is associated with a particular file in your Workspace.
- You don’t need to have a database and schema in use during your session to use Snowflake Copilot inline.
- Snowflake Copilot uses the names of your databases, schemas, tables, and columns and also the data types of your columns to determine what
  data is available to query.
- For optimal performance, use meaningful names for databases, schemas, tables, and columns, and ensure that columns are assigned the
  appropriate data type.
- Snowflake Copilot inline considers the following sources, but does not store the data from them:
  - Contents of the current file, including SQL queries and code.
  - Context of the current file, including database, schema, and role.
  - User supplied input.
  - Snowflake documentation or general SQL knowledge.
  - Data from your account.

To begin using Snowflake Copilot inline:

1. Open a Workspace. For information about Workspaces, see [Workspaces](/user-guide/ui-snowsight/workspaces).
2. Enter the `CMD+I` shortcut.
3. In the message dialog, enter your request. Then click the send icon to submit it. Snowflake Copilot provides a
   response inline and shows a diff with the existing code.
4. Choose one of the following:
   - Select **Accept** to accept the suggested changes.
   - Select **Reject** to reject the suggested changes.
   - Select **Close** to end the session.

## Add custom instructions

Snowflake Copilot inline does not accept custom instructions to customize how it responds.

## Examples

The following sections provide examples that demonstrate how to:

- [Construct and run SQL statements](#label-snowflake-copilot-inline-construct-sql-example)
- [Add comments to a SQL statement](#label-snowflake-copilot-inline-add-comments-sql-example)
- [Fix a SQL Statement](#label-snowflake-copilot-inline-fix-sql-example)

These examples use a sample dataset from the Snowflake Marketplace.

### Prerequisites

The examples in this section use the [Cybersyn Github Archive dataset](https://app.snowflake.com/marketplace/listing/GZTSZAS2KJ3/cybersyn-inc-cybersyn-github-archive) from the Snowflake Marketplace:

1. Install the [Cybersyn Github Archive dataset](https://app.snowflake.com/marketplace/listing/GZTSZAS2KJ3/cybersyn-inc-cybersyn-github-archive) in your account.
2. Open a Workspace. For information about Workspaces, see [Workspaces](/user-guide/ui-snowsight/workspaces).
3. Select the Cybersyn Github Archive database and schema.

### Construct and run a SQL Statement

The following example demonstrates how to use Snowflake Copilot inline to generate SQL queries.

1. Enter the following question in the Snowflake Copilot inline message box, and select the send icon to submit it. Snowflake Copilot
   responds with a SQL query that answers your question.

   Copy code

   ```
   How many stars were given in the past year?
   ```
2. Review the changes. Lines highlighted in red are removed and lines highlighted in green are added.
3. Select **Accept** to accept the suggested changes.

Snowflake Copilot does not have access to the data inside your tables. If you want Snowflake Copilot to construct a
SQL statement that filters based on a specific value of a column, you must provide the value
to filter on.

1. Enter the following question in the message box and select the send icon. Snowflake Copilot inline responds with a SQL query that uses the filter value that you provided.

   Copy code

   ```
   What are all of the repo names that start with 'snowflake'?
   ```
2. Review the changes. Lines highlighted in red are removed and lines highlighted in green are added.
3. Select **Accept** to accept the suggested changes.

### Add comments to a SQL statement

The following example demonstrates how to use Snowflake Copilot to add comments to a SQL statement you’re working on.

- In the Snowflake Copilot inline message box, type the following question:

  Copy code

  ```
  Can you add comments to this query?
  ```

Snowflake Copilot responds by adding a comment that explains the purpose of each line in the provided query.

### Fix a SQL Statement

The following example demonstrates how to use Snowflake Copilot inline from a Workspace to fix a SQL statement.

1. Focus your cursor over the target query with a syntax error.
2. Enter the `CMD+I` shortcut to bring up the Snowflake Copilot inline window.
3. Ask Snowflake Copilot to fix your query.
4. Review the changes. Lines highlighted in red are removed and lines highlighted in green are added.
5. Select **Accept** to accept the suggested changes.

## Tips for using Snowflake Copilot

For tips about using Snowflake Copilot, see [Tips for using Snowflake Copilot](/user-guide/snowflake-copilot#label-snowflake-copilot-performance).

## Costs

Snowflake Copilot is currently free to use. Details on pricing and billing are planned but you will be notified before any charges are applied
for this feature.

## Legal notices

This feature leverages third party models and/or services, as previously described on this page. Where the models and/or services used are
provided on the [Snowflake Model and Service Flowdown Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/ai-features/open-source-model-flow-down-terms/) page, use of those models and/or services are also subject to those terms.

For additional information, refer to [Snowflake AI and ML](/guides-overview-ai-features).

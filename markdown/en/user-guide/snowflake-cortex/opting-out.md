# Opt out of Snowflake AI features

Most Snowflake AI features are initially available to all users in your Snowflake account. Access to most features is
controlled by the SNOWFLAKE.CORTEX\_USER database role, which is initially granted to the PUBLIC role. All users are
granted the PUBLIC role, giving them access to Cortex features by default. (Access to Snowflake Copilot is controlled by
the SNOWFLAKE.COPILOT\_USER database role, also granted to PUBLIC by default.) Cortex Analyst is an opt-in feature that is
not accessible to users by default.

## Opt out of default features

To revoke access to all Snowflake AI features that are available to users by default, revoke the SNOWFLAKE.CORTEX\_USER and
SNOWFLAKE.COPILOT\_USER database roles from the PUBLIC role. You can grant these roles to specific roles that you want to have
access to the features, then grant those roles to specific users as needed. (You cannot grant database roles
directly to users, but must grant them to roles that can be assumed by users.)

Use SQL like the following to revoke access to the SNOWFLAKE.CORTEX\_USER and SNOWFLAKE.COPILOT\_USER roles from the PUBLIC role, then grant them
to specific roles and users.

Copy code

```
-- Revoke access to most Snowflake AI features from all users in the account
REVOKE DATABASE ROLE SNOWFLAKE.CORTEX_USER FROM ROLE PUBLIC;
REVOKE DATABASE ROLE SNOWFLAKE.COPILOT_USER FROM ROLE PUBLIC;

-- Optionally, grant access to specific roles
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE my_cortex_role;
GRANT DATABASE ROLE SNOWFLAKE.COPILOT_USER TO ROLE my_copilot_role;

-- Then grant those roles to specific users
GRANT ROLE my_cortex_role TO USER alice;
GRANT ROLE my_copilot_role TO USER bob;
```

Note

If you granted SNOWFLAKE.CORTEX\_USER and SNOWFLAKE.COPILOT\_USER to other roles, revoke them from those roles
to completely block users from using Snowflake AI features.

## Revoke access to opt-in features

Some Snowflake AI features are opt-in. Access to these features is disabled by default, so unless you grant
access to them, your users cannot use them. If you have granted access to any of these features, you can revoke access
to individual features:

- **Cortex Analyst:** Set the ENABLE\_CORTEX\_ANALYST account parameter to FALSE:

  Copy code

  ```
  ALTER ACCOUNT SET ENABLE_CORTEX_ANALYST = FALSE;
  ```
- **Cortex Embedding Functions** (AI\_EMBED, EMBED\_TEXT\_768, and EMBED\_TEXT\_1024): Calling these functions
  requires the SNOWFLAKE.CORTEX\_EMBED\_USER database role if the user does not have the SNOWFLAKE.CORTEX\_USER database role.
  Revoke SNOWFLAKE.CORTEX\_EMBED\_USER role from any roles you have granted it to.

  Copy code

  ```
  REVOKE DATABASE ROLE SNOWFLAKE.CORTEX_EMBED_USER FROM ROLE my_role;
  ```
- **Cortex Fine-tuning:** Revoke the CREATE MODEL privilege on schemas from any roles you have granted it to.

  Copy code

  ```
  REVOKE CREATE MODEL ON SCHEMA my_schema FROM ROLE my_role;
  ```
- **Provisioned Throughput:** Revoke the CREATE PROVISIONED THROUGHPUT privilege on schemas from any roles you have granted it to.

  Copy code

  ```
  REVOKE CREATE PROVISIONED THROUGHPUT ON SCHEMA my_schema FROM ROLE my_role;
  ```

## Access control by feature

The following table has more detailed information on access control for individual Snowflake AI features:

| Feature | Opt in | Main access control method | Additional access control methods |
| --- | --- | --- | --- |
| [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents-setup#label-cortex-agents-access-control) |  | SNOWFLAKE.CORTEX\_USER database role | USAGE on the search service that the agent queries, plus USAGE on the database, schema, and table used by the search service |
| [Cortex AI Functions](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) |  | SNOWFLAKE.CORTEX\_USER database role |  |
| [Cortex Analyst](/user-guide/snowflake-cortex/cortex-analyst#label-analyst-access-control) | ✔ | ENABLE\_CORTEX\_ANALYST account parameter |  |
| [Cortex Fine-tuning](/user-guide/snowflake-cortex/cortex-finetuning#label-cortex-finetune-privileges) | ✔ | CREATE MODEL on the schema where you create fine-tuned models |  |
| [Cortex Knowledge Extensions](/user-guide/snowflake-cortex/cortex-knowledge-extensions/cke-overview) |  | SNOWFLAKE.CORTEX\_USER database role | Relies on access control for the underlying Cortex Search Service |
| [Cortex Provisioned Throughput](/user-guide/snowflake-cortex/provisioned-throughput) | ✔ | CREATE PROVISIONED THROUGHPUT privilege on the schema where you create provisioned throughput objects |  |
| [Cortex Search](/user-guide/snowflake-cortex/cortex-search/cortex-search-overview#label-cortex-search-privileges) |  | SNOWFLAKE.CORTEX\_USER database role | USAGE on the search service, database, schema, and table used by the search service |
| [Snowflake Copilot](/user-guide/snowflake-copilot#label-snowflake-copilot-limit) |  | SNOWFLAKE.COPILOT\_USER database role |  |
| [Snowflake CoWork](/user-guide/snowflake-cortex/snowflake-cowork) |  | SNOWFLAKE.CORTEX\_USER database role | Relies on access control for the underlying Cortex Agent or Search Service |

Expand

Show lessSee more

## Opt out of specific models and AI Functions

Because the cost of using different large language models varies, you can limit access to specific LLMs via an
account-level allowlist, by role-based access control, or by a combination of both. For more information, see
[Control model access](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-access-control).

## ACCOUNTADMIN and AI features

The ACCOUNTADMIN role has complete access to all features in a Snowflake account, including Snowflake AI features.
Revoking the SNOWFLAKE.CORTEX\_USER and SNOWFLAKE.COPILOT\_USER roles from PUBLIC does not prevent ACCOUNTADMIN from using these features.
Even if an ACCOUNTADMIN’s access to AI features is revoked, a user with access to ACCOUNTADMIN can always
grant access to that role (or any other role) again.

For this and other reasons, it is a best practice to grant the ACCOUNTADMIN role to trusted users only, or even more
strictly, to a single user in the account which is not used for any purpose other than Snowflake account administration
and whose login credentials are tightly controlled. Use ACCOUNTADMIN only for account setup and maintenance, and use
other administrative roles with more limited scope (that is, SECURITYADMIN, SYSADMIN, or USERADMIN) for day-to-day
administration.

It is possible to prevent ACCOUNTADMIN from using Snowflake AI features that are gated by means other than role-based
access control. For example, even a user with ACCOUNTADMIN can’t use Cortex Analyst if the ENABLE\_CORTEX\_ANALYST account
parameter is set to FALSE. Of course, this user can always set this parameter to TRUE.

## Monitor AI feature usage

To make sure that Snowflake AI features are not being used, monitor usage of Snowflake AI features using the
Cortex-related views in the [SNOWFLAKE.ACCOUNT\_USAGE](/sql-reference/account-usage) schema. These views are:

- [CORTEX\_ANALYST\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_analyst_usage_history)
- [CORTEX\_DOCUMENT\_PROCESSING\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_document_processing_usage_history)
- [CORTEX\_FINE\_TUNING\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_fine_tuning_usage_history)
- [CORTEX\_FUNCTIONS\_QUERY\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_functions_query_usage_history)
- [CORTEX\_FUNCTIONS\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_functions_usage_history)
- [CORTEX\_PROVISIONED\_THROUGHPUT\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_provisioned_throughput_usage_history)
- [CORTEX\_SEARCH\_DAILY\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_search_daily_usage_history)
- [CORTEX\_SEARCH\_SERVING\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_search_serving_usage_history)

Note

CORTEX\_FUNCTIONS\_QUERY\_USAGE\_HISTORY and CORTEX\_FUNCTIONS\_USAGE\_HISTORY log essentially the same events. It
is not necessary to monitor both.

[Create alerts on new data](/user-guide/alerts#label-alerts-type-streaming) in these views to notify you when new AI features are
used in your account. For example, the following SQL statement creates an alert that sends a Slack message when any AI function is used:

Copy code

```
CREATE ALERT my_alert
  IF (EXISTS (
    SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.CORTEX_FUNCTIONS_QUERY_USAGE_HISTORY))
  THEN
    BEGIN
      CALL SYSTEM$SEND_SNOWFLAKE_NOTIFICATION(
        SNOWFLAKE.NOTIFICATION.TEXT_PLAIN('AI function used in account'),
        '{"my_slack_integration": {}}'
      );
    END;
```

Such alerts incur a nominal compute cost when new data is added to a Cortex usage history view, but if no AI features
are used, there is no cost because no data is ever added and the alert is never triggered.

## Control access to ML features

Snowflake ML features are not AI features, and access to them is not controlled by the SNOWFLAKE.CORTEX\_USER role.

### ML Functions

[ML Functions](/guides-overview-ml-functions) employ classical machine learning techniques for forecasting, anomaly
detection, classification, and other data analysis tasks. Creation of models by ML Functions is opt-in and controlled by
a function-specific privilege, such as CREATE SNOWFLAKE.ML.FORECAST, on schemas. Access to trained models is controlled
by the USAGE privilege on the model object. If you have granted these privileges already, revoke them to prevent users
from creating or using ML Functions models. You may want to DROP any models that have already been created.

Owners of schemas can create ML Functions models in them, regardless of whether they have CREATE privileges for a
specific type of model, so limit ownership and creation of schemas to trusted users. Grant specific privileges to create
models within each schema only to users who need them.

### Snowflake ML

[Snowflake ML](/developer-guide/snowflake-ml/overview) lets you build, deploy, and manage custom machine learning
models developed in Python, at Snowflake scale. Creation and use of Snowflake ML objects, including the model registry,
the feature store, and models and their versions, is not controlled by the SNOWFLAKE.CORTEX\_USER role.

Snowflake ML objects are schema-level objects, which means that users can create Snowflake ML objects in any schema on
which they have OWNERSHIP or an appropriate CREATE privilege (for example, CREATE MODEL REGISTRY). Therefore, access to
Snowflake ML is best controlled by limiting ownership and creation of schemas to trusted users. Grant specific
privileges to create Snowflake ML objects within each schema only to users who need them.

Note

Users with the CREATE MODEL privilege in a schema can also create models using Cortex Fine-tuning. However, actually
using Cortex fine-tuned models requires the SNOWFLAKE.CORTEX\_USER database role.

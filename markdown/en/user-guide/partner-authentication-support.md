# Partner support for Snowflake authentication methods

Use this topic to determine which Snowflake authentication methods you can use to connect to Snowflake from a partner application.

## Supported authentication for `TYPE = PERSON` users

When the Snowflake user is a human user, the `TYPE` property of the user object is set to `PERSON`. This section details which
Snowflake authentication methods are available to human users when connecting from a partner application. For a description of these
authentication methods, see [Overview of authentication methods for applications](/user-guide/security-authentication-overview#label-auth-overview-applications).

Snowflake recommends configuring your partner application to authenticate with OAuth because it is stronger than other authentication
methods. For help choosing between External OAuth and Snowflake OAuth, see [Choosing authentication for interactive applications](/user-guide/security-authentication-overview#label-auth-overview-choose-interactive). A person
authenticates with the OAuth authorization code flow because the user can interact with the authorization server during authentication.

Alternatively, you can use a programmatic access token (PAT) as a replacement for a password when authenticating to Snowflake as long as the
password field accepts 256 characters. However, be aware that PATs aren’t as strong as OAuth.

| Application | External OAuth | Snowflake OAuth | Key pair authentication | Programmatic access token (PAT) |
| --- | --- | --- | --- | --- |
| [PowerBI Cloud (BI)](https://learn.microsoft.com/en-us/fabric/data-factory/connector-snowflake#authentication) | **Yes** (Only Microsoft Entra ID is supported) | No | **Yes** | No |
| [PowerBI Desktop (BI)](https://learn.microsoft.com/en-us/fabric/data-factory/connector-snowflake#authentication) | **Yes** (Only Microsoft Entra ID is supported) | No | **Yes** | No |
| [Tableau Cloud (BI)](https://help.tableau.com/current/pro/desktop/en-us/examples_snowflake.htm) | **Yes** | **Yes** | **Yes** | **Yes** |
| [Tableau Server (BI)](https://help.tableau.com/current/server/en-us/config_oauth_snowflake.htm) | **Yes** | **Yes** | No | No |
| [DBT Cloud (Transform)](https://docs.getdbt.com/docs/cloud/connect-data-platform/connect-snowflake) | No | **Yes** | **Yes** | **Yes** |
| [DBT Core (Transform)](https://docs.getdbt.com/docs/core/connect-data-platform/snowflake-setup) | No | **Yes** | **Yes** | **Yes** |
| [Airflow (Workflow orchestration)](/developer-guide/python-connector/python-connector-connect) | N/A | N/A | **Yes** | **Yes** |
| [Qlik Sense Cloud (BI)](https://help.qlik.com/en-US/connectors/Subsystems/ODBC_connector_help/Content/Connectors_ODBC/Snowflake/Create-Snowflake-connection.htm) | **Yes** | **Yes** | **Yes** | **Yes** |
| [Qlik Sense Desktop (BI)](https://help.qlik.com/en-US/connectors/Subsystems/ODBC_connector_help/Content/Connectors_ODBC/Snowflake/Create-Snowflake-connection.htm) | No | No | **Yes** | **Yes** |
| [Fivetran (EL)](https://fivetran.com/docs/destinations/snowflake/setup-guide#optionalkeypairauthentication) | No | No | **Yes** | No |
| [Matillion (ELT)](https://docs.matillion.com/data-productivity-cloud/administration/docs/snowflake-key-pair-authentication/) | No | No | **Yes** | **Yes** |
| [Informatica (ETL)](https://docs.informatica.com/integration-cloud/data-integration-connectors/current-version/snowflake-data-cloud-connector/part-1--getting-started-with-snowflake-data-cloud-connector/connections-for-snowflake-data-cloud/connect-to-snowflake/authentication-typesdwsnowflakev2conn-authentication.html) | No | **Yes** | **Yes** | **Yes** |
| [ThoughtSpot (BI - interactive)](https://docs.thoughtspot.com/software/10.1.0.sw/connections-snowflake-add) | **Yes** | **Yes** | **Yes** | No |
| Strategy Cloud (BI) | **Yes** | No | **Yes** | **Yes** |
| Strategy Workstation/Developer (BI) | **Yes** | No | No | **Yes** |

Expand

Show lessSee more

## Supported authentication for `TYPE = SERVICE` users

When a service — for example, an application or workflow — is authenticating to Snowflake, the `TYPE` property of the user object is set to `SERVICE`. This section details which Snowflake authentication methods are available when connecting from a partner application as a service. For a description of these authentication methods, see [Overview of authentication methods for applications](/user-guide/security-authentication-overview#label-auth-overview-applications).

Snowflake recommends configuring your partner application to authenticate with OAuth, because it is stronger than other available authentication methods. A service authenticates using the OAuth client credentials flow, because there isn’t a person to interact with the authorization server.

Alternatively, you can use a programmatic access token (PAT) as a replacement for a password when authenticating to Snowflake as long as the
password field accepts 256 characters. However, be aware that PATs aren’t as strong as OAuth.

| Application | External OAuth | Key pair authentication | Programmatic access token (PAT) |
| --- | --- | --- | --- |
| [PowerBI Cloud (BI)](https://learn.microsoft.com/en-us/fabric/data-factory/connector-snowflake#authentication) | No | **Yes** | No |
| [PowerBI Desktop (BI)](https://learn.microsoft.com/en-us/fabric/data-factory/connector-snowflake#authentication) | No | **Yes** | No |
| [Tableau Cloud (BI)](https://help.tableau.com/current/pro/desktop/en-us/examples_snowflake.htm) | No | **Yes** | **Yes** |
| [Tableau Server (BI)](https://help.tableau.com/current/server/en-us/config_oauth_snowflake.htm) | No | No | No |
| [DBT Cloud (Transform)](https://docs.getdbt.com/docs/cloud/connect-data-platform/connect-snowflake) | No | **Yes** | **Yes** |
| [DBT Core (Transform)](https://docs.getdbt.com/docs/core/connect-data-platform/snowflake-setup) | No | **Yes** | **Yes** |
| [Airflow (Workflow orchestration)](/developer-guide/python-connector/python-connector-connect) | **Yes** | **Yes** | **Yes** |
| [Qlik Sense Cloud (BI)](https://help.qlik.com/en-US/connectors/Subsystems/ODBC_connector_help/Content/Connectors_ODBC/Snowflake/Create-Snowflake-connection.htm) | No | **Yes** | **Yes** |
| [Qlik Sense Desktop (BI)](https://help.qlik.com/en-US/connectors/Subsystems/ODBC_connector_help/Content/Connectors_ODBC/Snowflake/Create-Snowflake-connection.htm) | No | **Yes** | **Yes** |
| [Fivetran (EL)](https://fivetran.com/docs/destinations/snowflake/setup-guide#optionalkeypairauthentication) | No | **Yes** | No |
| [Matillion (ELT)](https://docs.matillion.com/data-productivity-cloud/administration/docs/snowflake-key-pair-authentication/) | No | **Yes** | **Yes** |
| [Informatica (ETL)](https://docs.informatica.com/integration-cloud/data-integration-connectors/current-version/snowflake-data-cloud-connector/part-1--getting-started-with-snowflake-data-cloud-connector/connections-for-snowflake-data-cloud/connect-to-snowflake/authentication-typesdwsnowflakev2conn-authentication.html) | **Yes** | **Yes** | **Yes** |
| [ThoughtSpot (BI - interactive)](https://docs.thoughtspot.com/software/10.1.0.sw/connections-snowflake-add) | **Yes** | **Yes** | **No** |
| Strategy Cloud (BI) | No | **Yes** | No |
| Strategy Workstation/Developer (BI) | No | No | No |

Expand

Show lessSee more

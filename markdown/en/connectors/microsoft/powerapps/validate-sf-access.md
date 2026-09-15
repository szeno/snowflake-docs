# Snowflake Connector for Microsoft Power Platform: [Optional] Validate Snowflake access

Validate Snowflake access using either [SnowCLI](/developer-guide/snowflake-cli/index) or [SnowSQL](/user-guide/snowsql).

Open a terminal and execute the following commands:

- For *Delegated Auth*

  Copy code

  ```
  snowsql -a <organization-locator> -u 'user@sandbox.onmicrosoft.com' --rolename <snowflake-role> --authenticator oauth --token "<token-value>"
  ```
- For Service Principal Auth

  Copy code

  ```
  snowsql -a <organization-locator> -u 'sub-value' -r <snowflake-role> --authenticator oauth --token "<token-value>"
  ```

Where:

> - `snowflake-accountname` from [Snowflake Connector for Microsoft Power Platform: [Optional] Validate Entra authorization setup](/connectors/microsoft/powerapps/validate-entra-auth).
> - `snowflake-role` from [Snowflake Connector for Microsoft Power Platform: Create a security integration](/connectors/microsoft/powerapps/create-security-integration).
> - `token-value` from the output from cURL in step [Snowflake Connector for Microsoft Power Platform: [Optional] Validate Entra authorization setup](/connectors/microsoft/powerapps/validate-entra-auth).

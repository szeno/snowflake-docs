# Snowflake Connector for Microsoft Power Platform: [Optional] Validate Snowflake access

Validate Snowflake access using [Snowflake CLI](/developer-guide/snowflake-cli/index).

Open a terminal and run the following commands:

- For *Delegated Auth*

  Copy code

  ```
  snow connection test --temporary-connection --account <account-identifier> --user 'user@sandbox.onmicrosoft.com' --role <snowflake-role> --authenticator oauth --token "<token-value>"
  ```
- For Service Principal Auth

  Copy code

  ```
  snow connection test --temporary-connection --account <account-identifier> --user 'sub-value' --role <snowflake-role> --authenticator oauth --token "<token-value>"
  ```

Where:

> - `account-identifier` is the [account identifier](/user-guide/admin-account-identifier) for your Snowflake account.
> - `snowflake-role` from [Snowflake Connector for Microsoft Power Platform: Create a security integration](/connectors/microsoft/powerapps/create-security-integration).
> - `token-value` from the output from cURL in step [Snowflake Connector for Microsoft Power Platform: [Optional] Validate Entra authorization setup](/connectors/microsoft/powerapps/validate-entra-auth).

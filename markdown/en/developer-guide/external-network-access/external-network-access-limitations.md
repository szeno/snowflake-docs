# External network access limitations

This topic describes limitations for accessing external network locations from user-defined functions and procedures.

## Limitations

- Currently, handlers written only in Java, Python, or Scala may access network locations external to Snowflake.
- When using a wildcard in a VALUE\_LIST value in a [network rule](/sql-reference/sql/create-network-rule), the following are not
  valid wildcard uses:

  - `snowflake.*.google.com`

    Cannot be used to match `snowflake.sub1.sub2.google.com` because the asterisk can only be used to
    match alphanumeric characters and hyphens.
  - `*.*.google.com`

    Invalid because there are multiple asterisks in the wildcard.
  - `*.com`

    Invalid because the asterisk cannot be used to match the secondary level domain.
- When using a [secret](/sql-reference/sql/create-secret#label-create-secret-basic-auth-params) of the PASSWORD type, the colon character (`:`) is not supported in the
  USERNAME or PASSWORD parameters.
- By default, Snowflake does not enable external access for [trial accounts](/user-guide/admin-trial-account). Contact
  your account representative to get external access enabled for a trial account.

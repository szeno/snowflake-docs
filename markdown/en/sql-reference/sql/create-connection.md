# CREATE CONNECTION

[Business Critical Feature](/user-guide/intro-editions)

This command is part of the [client redirect](/user-guide/client-redirect) feature.
It requires Business Critical Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

You use client redirect in combination with the
[account replication](/user-guide/account-replication-intro) feature
for business continuity and disaster recovery.

Creates a new [connection](/user-guide/client-redirect) in the account.

See also:
:   [ALTER CONNECTION](/sql-reference/sql/alter-connection) , [DROP CONNECTION](/sql-reference/sql/drop-connection) , [SHOW CONNECTIONS](/sql-reference/sql/show-connections)

## Syntax

**Primary Connection**

Copy code

```
CREATE CONNECTION [ IF NOT EXISTS ] <name>
  [ COMMENT = '<string_literal>' ]
```

**Secondary Connection**

Copy code

```
CREATE CONNECTION [ IF NOT EXISTS ] <name>
  AS REPLICA OF <organization_name>.<account_name>.<name>
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   String that specifies the identifier (i.e. name) for the connection. It must conform to the following:

    - Must start with an alphabetic character and may only
      contain letters, decimal digits (0-9), and underscores (\_).
    - For a primary connection, the name must be unique across connection names and account names in the organization.
    - For a secondary connection, the name must match the name of its primary connection.

### Secondary connection parameters

`AS REPLICA OF organization_name.account_name.name`
:   Specifies the identifier for a primary connection from which to create a replica (i.e. a secondary connection).

    `organization_name`
    :   Specifies the identifier for the organization.

    `account_name`
    :   Specifies the identifier for the account.

    `name`
    :   Specifies the identifier for the primary connection.

## Optional parameters

`COMMENT = 'string_literal'`
:   Specifies a comment for the connection.

    Default: No value

## Access control requirements

Only account administrators (users with the ACCOUNTADMIN role) can execute this SQL command.

## Usage notes

- If private connectivity to the Snowflake service is enabled for your Snowflake account, your network manager must create and manage
  a DNS CNAME record. For more details, see [Configuring the DNS settings for private connectivity to the Snowflake service](/user-guide/client-redirect#label-client-redirect-configuring-the-dns-cname-record).
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Create a connection. For this example, suppose that you are connected to the account `myaccount1`
in the organization `myorg`.

Copy code

```
CREATE CONNECTION IF NOT EXISTS myconnection;
```

Create a secondary connection as a replica of its primary connection. Substitute your own account and
organization values in the fully qualified name used in the parameter.
You can get the fully qualified value to use from the `primary` column in the output of [SHOW CONNECTIONS](/sql-reference/sql/show-connections).

Copy code

```
CREATE CONNECTION myconnection AS REPLICA OF myorg.myaccount1.myconnection;
```

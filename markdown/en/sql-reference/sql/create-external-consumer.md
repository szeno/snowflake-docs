# CREATE EXTERNAL CONSUMER

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Creates a new external consumer identity, or replaces an existing one, for use with [Open Data Sharing](/user-guide/open-data-sharing).
External consumers represent parties outside of Snowflake that access shared Iceberg data using the Iceberg REST Catalog API.

See also:
:   [ALTER EXTERNAL CONSUMER](/sql-reference/sql/alter-external-consumer) ,
    [DROP EXTERNAL CONSUMER](/sql-reference/sql/drop-external-consumer) ,
    [DESCRIBE EXTERNAL CONSUMER](/sql-reference/sql/desc-external-consumer) ,
    [SHOW EXTERNAL CONSUMERS](/sql-reference/sql/show-external-consumers)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] EXTERNAL CONSUMER [ IF NOT EXISTS ] <name>
  [ COMMENT = '<string_literal>' ]
  [ EMAIL = '<email_address>' ]
```

## Required parameters

`name`
:   Specifies the identifier for the external consumer. Must be unique within the account.

    If the identifier contains spaces, special characters, or mixed-case characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

## Optional parameters

`OR REPLACE`
:   Replaces an existing external consumer with the same name. The existing consumer and its properties are replaced by the new definition.

`IF NOT EXISTS`
:   Creates the external consumer only if one with the same name does not already exist. If one already exists, the command does nothing
    and completes successfully.

    `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.

`COMMENT = 'string_literal'`
:   Specifies a comment for the external consumer.

`EMAIL = 'email_address'`
:   Specifies the email address associated with the external consumer.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE EXTERNAL CONSUMER | Account | Required to create an external consumer. Granted to ACCOUNTADMIN by default. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- External consumers are restricted identities. You cannot grant Snowflake roles or standard user options to an external consumer.
- External consumers must authenticate using Programmatic Access Tokens (PATs). See [ALTER EXTERNAL CONSUMER … ADD PAT](/sql-reference/sql/alter-external-consumer-add-programmatic-access-token).

## Examples

Create an external consumer:

Copy code

```
CREATE EXTERNAL CONSUMER acme_consumer
  COMMENT = 'External consumer for Acme Corp'
  EMAIL = 'data@acme.com';
```

Create an external consumer only if one with the same name does not already exist:

Copy code

```
CREATE EXTERNAL CONSUMER IF NOT EXISTS acme_consumer;
```

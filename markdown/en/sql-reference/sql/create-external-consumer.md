# CREATE EXTERNAL CONSUMER

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
  [ REGION = '<region_group>.<snowflake_region>' ]
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

    The new external consumer doesn’t inherit the PATs or workload identities of the external consumer that it replaces. Add them again
    after you replace the consumer.

`IF NOT EXISTS`
:   Creates the external consumer only if one with the same name does not already exist. If one already exists, the command does nothing
    and completes successfully.

    `OR REPLACE` and `IF NOT EXISTS` are mutually exclusive.

`REGION = 'region_group.snowflake_region'`
:   Specifies the region that Snowflake stores and serves shared data from for the external consumer. For example,
    `'PUBLIC.AWS_EU_CENTRAL_1'`. The region group must be `PUBLIC`. Only AWS and Azure commercial regions are supported; if you specify an
    unsupported region, the command fails. For more information, see
    [Share with external consumers in other regions](/user-guide/open-data-sharing#label-open-data-sharing-regions).

    The region doesn’t restrict where the external consumer’s client connects from.

    If the region is different from your provider account’s region, Snowflake auto-fulfills any listing that targets this external
    consumer to that region, which incurs replication and storage costs. For more information, see
    [Auto-fulfillment for listings](/collaboration/provider-listings-auto-fulfillment).

    If you omit `REGION`, the external consumer uses the region of your provider account.

    You can’t change `REGION` after you create the external consumer. To use a different region, create a new external consumer.

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
- External consumers authenticate with Programmatic Access Tokens (PATs) or workload identity federation (WIF). See
  [ALTER EXTERNAL CONSUMER … ADD PAT](/sql-reference/sql/alter-external-consumer-add-programmatic-access-token) and
  [Workload identity federation for external consumers](/user-guide/open-data-sharing-workload-identity).
- Each external consumer supports only one region. To serve the same party in more than one region, create a separate external consumer
  for each region.
- External consumers don’t support failover or disaster recovery (DR) yet.

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

Create an external consumer in the EU (Frankfurt) region:

Copy code

```
CREATE EXTERNAL CONSUMER acme_eu_consumer REGION = 'PUBLIC.AWS_EU_CENTRAL_1';
```

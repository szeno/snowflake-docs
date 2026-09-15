# DESCRIBE SHARE

Provider sharing not enabled for all accounts

Provider sharing is enabled by default for most, but not all accounts.

If you encounter errors when attempting to share data with consumers, the feature may not be enabled for your account. To inquire about
enabling it, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Describes the data objects that are included in a [share](/user-guide/data-sharing-intro).

DESCRIBE can be abbreviated to DESC.

See also:
:   [DROP SHARE](/sql-reference/sql/drop-share) , [ALTER SHARE](/sql-reference/sql/alter-share) , [CREATE SHARE](/sql-reference/sql/create-share) , [SHOW SHARES](/sql-reference/sql/show-shares)

## Syntax

**Providers (outbound share)**

Copy code

```
DESC[RIBE] SHARE <name>
```

**Consumers (inbound share)**

Copy code

```
DESC[RIBE] SHARE <provider_account>.<share_name>
```

## Parameters

`name`
:   Specifies the identifier for the outbound share to describe. If the identifier contains spaces or special characters, the entire string
    must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

`provider_account.share_name`
:   Specifies the fully-qualified identifier for the inbound share to describe.

## Usage notes

- Only the ACCOUNTADMIN role has the privileges to describe a share. Executing this command with any role other than ACCOUNTADMIN returns
  an error.

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Output

- The output of the command is different depending on whether you are a provider or consumer:

  - For providers, the names of the objects in the share are prefixed with the database name.
  - For consumers, the names of the objects in the share are prefixed with a database name only if a database has been created from the share.
    If a database has not been created from the share, the objects are prefixed with `<DB>`.
- The `kind` column in the output displays the type of the objects in the share.

## Examples

As a provider, display the objects in the `sales_s` share:

> Copy code
>
> ```
> DESC SHARE sales_s;
>
> +----------+--------------------------------------+-------------------------------+
> | kind     | name                                 | shared_on                     |
> |----------+--------------------------------------+-------------------------------|
> | DATABASE | SALES_DB                             | 2017-06-15 17:03:16.642 -0700 |
> | SCHEMA   | SALES_DB.AGGREGATES_EULA             | 2017-06-15 17:03:16.790 -0700 |
> | TABLE    | SALES_DB.AGGREGATES_EULA.AGGREGATE_1 | 2017-06-15 17:03:16.963 -0700 |
> +----------+--------------------------------------+-------------------------------+
> ```

As a consumer, display the objects in the `sales_s` share provided by account `ab67890`:

> Copy code
>
> ```
> DESC SHARE ab67890.sales_s;
>
> +----------+----------------------------------+---------------------------------+
> | kind     | name                             | shared_on                       |
> |----------+----------------------------------+---------------------------------|
> | DATABASE | <DB>                             | Thu, 15 Jun 2017 17:03:16 -0700 |
> | SCHEMA   | <DB>.AGGREGATES_EULA             | Thu, 15 Jun 2017 17:03:16 -0700 |
> | TABLE    | <DB>.AGGREGATES_EULA.AGGREGATE_1 | Thu, 15 Jun 2017 17:03:16 -0700 |
> +----------+----------------------------------+---------------------------------+
> ```
>
> In this example, a database has not yet been created in the consumer’s account from the `sales_s` share.

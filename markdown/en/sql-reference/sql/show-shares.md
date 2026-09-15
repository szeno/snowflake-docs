# SHOW SHARES

Provider sharing not enabled for all accounts

Provider sharing is enabled by default for most, but not all accounts.

If you encounter errors when attempting to share data with consumers, the feature may not be enabled for your account. To inquire about
enabling it, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Lists all [shares](/user-guide/data-sharing-intro) available in the system:

- Outbound shares (to consumers) that have been created in your account (as a provider).
- Inbound shares (from providers) that are available for your account to consume.

See also:
:   [CREATE SHARE](/sql-reference/sql/create-share) , [ALTER SHARE](/sql-reference/sql/alter-share) , [DROP SHARE](/sql-reference/sql/drop-share) , [DESCRIBE SHARE](/sql-reference/sql/desc-share)

## Syntax

Copy code

```
SHOW SHARES [ LIKE '<pattern>' ]
            [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Parameters

`LIKE 'pattern'`
:   Optionally filters the command output by object name. The filter uses case-insensitive pattern matching, with support for SQL
    wildcard characters (`%` and `_`).

    For example, the following patterns return the same results:

    `... LIKE '%testing%' ...`
    `... LIKE '%TESTING%' ...`

    Default: No value (no filtering is applied to the output).

`STARTS WITH 'name_string'`
:   Optionally filters the command output based on the characters that appear at the beginning of
    the object name. The string must be enclosed in single quotes and is case sensitive.

    For example, the following strings return different results:

    `... STARTS WITH 'B' ...`
    `... STARTS WITH 'b' ...`

    Default: No value (no filtering is applied to the output)

`LIMIT rows [ FROM 'name_string' ]`
:   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
    returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.

    The optional `FROM 'name_string'` subclause effectively serves as a “cursor” for the results. This enables fetching the
    specified number of rows following the first row whose object name matches the specified string:

    - The string must be enclosed in single quotes and is case sensitive.
    - The string does not have to include the full object name; partial names are supported.

    Default: No value (no limit is applied to the output)

    Note

    For SHOW commands that support both the `FROM 'name_string'` and `STARTS WITH 'name_string'` clauses, you can combine
    both of these clauses in the same statement. However, both conditions must be met or they cancel out each other and no results are
    returned.

    In addition, objects are returned in lexicographic order by name, so `FROM 'name_string'` only returns rows with a higher
    lexicographic value than the rows returned by `STARTS WITH 'name_string'`.

    For example:

    - `... STARTS WITH 'A' LIMIT ... FROM 'B'` would return no results.
    - `... STARTS WITH 'B' LIMIT ... FROM 'A'` would return no results.
    - `... STARTS WITH 'A' LIMIT ... FROM 'AB'` would return results (if any rows match the input strings).

## Usage notes

- The command lists shares only for users with a role that has the IMPORT SHARE privilege.

  - By default, the ACCOUNTADMIN role has this privilege.

    - For the ACCOUNTADMIN role, this command lists all outbound shares created in the account.
    - For other roles with the IMPORT SHARE privilege, this command lists only the outbound shares owned by the active role of the session.
  - A user with the ACCOUNTADMIN role can delegate this privilege. See [Enable non-ACCOUNTADMIN roles to perform data sharing tasks](/user-guide/security-access-privileges-shares).

  Note

  Executing this command without sufficient privileges returns empty results.

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

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

- The command returns a maximum of ten thousand records for the specified object type, as dictated by the access privileges for the role
  used to execute the command. Any records above the ten thousand records limit aren’t returned, even with a filter applied.

  To view results for which more than ten thousand records exist, query the corresponding view (if one exists) in the [Snowflake Information Schema](/sql-reference/info-schema).

## Output

- The `kind` column displays:

  - `INBOUND` indicates the share is available to your account to consume (i.e. you can create a database from the share).
  - `OUTBOUND` indicates that your account is sharing data with other accounts and this share was created in your account.
- For `OUTBOUND` shares, if accounts have been added to the share, the `to` column displays these accounts. The maximum number
  of accounts displayed in this column is three; however, there is no hard limit on the number of accounts that can be added to a share.

## Examples

Show all shares that have been created in your account or are available to consume by your account:

> Copy code
>
> ```
> SHOW SHARES;
>
> +-------------------------------+----------+----------------------+---------------+-----------------------+------------------+--------------+----------------------------------------+---------------------+
> | created_on                    | kind     | owner_account        | name          | database_name         | to               | owner        | comment                                | listing_global_name |                  |
> |-------------------------------+----------+----------------------+---------------+-----------------------+------------------+--------------+----------------------------------------|---------------------|
> | 2016-07-09 19:18:09.821 -0700 | INBOUND  | SNOW.MY_TEST_ACCOUNT | SAMPLE_DATA   | SNOWFLAKE_SAMPLE_DATA |                  |              | Sample data sets provided by Snowflake |                     |
> | 2017-06-15 17:02:29.625 -0700 | OUTBOUND | SNOW.MY_TEST_ACCOUNT | SALES_S       | SALES_DB              | XY12345, YZ23456 | ACCOUNTADMIN |                                        |                     |
> +-------------------------------+----------+----------------------+---------------+-----------------------+------------------+--------------+----------------------------------------+---------------------+
> ```

Show all shares that have been created in your account or are available to consume by your account that include the string ‘SNOW’:

> Copy code
>
> ```
> SHOW SHARES LIMIT 5 FROM 'SNOW';
>
> +-------------------------------+----------+-------------------------+-----------------+----------------+------------------+--------------+---------+---------------------+
> | created_on                    | kind     | owner_account           | name            | database_name  | to               | owner        | comment | listing_global_name |
> |-------------------------------+----------+-------------------------+-----------------+----------------+------------------+--------------+---------+---------------------|
> | 2020-07-07 19:18:09.821 -0700 | OUTBOUND | SNOW.MY_TEST_ACCOUNT    | SNOW_DATA       | EXAMPLE        |                  | ACCOUNTADMIN |         |                     |
> | 2020-07-10 19:18:09.821 -0700 | OUTBOUND | SNOW.MY_TEST_ACCOUNT    | DATA_SNOWS      | EXAMPLE        |                  | ACCOUNTADMIN |         |                     |
> | 2022-08-18 12:02:29.625 -0700 | OUTBOUND | SNOW.MY_TEST_ACCOUNT    | SNOW_DATA       | ALFALFA_DB     | AB12345, YZ23456 | ACCOUNTADMIN |         |                     |
> | 2022-08-18 13:04:29.625 -0700 | OUTBOUND | SNOW.MY_TEST_ACCOUNT    | SNOW_SHARE      | SALES_DB       | AB12345          | ACCOUNTADMIN |         |                     |
> | 2022-08-18 14:02:40.625 -0700 | OUTBOUND | SNOW.MY_TEST_ACCOUNT    | SNOWIER_SHARE   | SALES_DB       |                  | ACCOUNTADMIN |         |                     |
> +-------------------------------+----------+-------------------------+-----------------+----------------+------------------+--------------+---------+---------------------+
> ```

Show all shares that have been created in your account or are available to consume by your account that start with SNOW, sorted in
lexicographic order:

> Copy code
>
> ```
> SHOW SHARES STARTS WITH 'SNOW' LIMIT 5 FROM 'A';
>
> +-------------------------------+----------+------------------------+------------------------+----------------+------------------+--------------+---------+---------------------+
> | created_on                    | kind     | owner_account          |  name                  | database_name  | to               | owner        | comment | listing_global_name |
> |-------------------------------+----------+------------------------+------------------------+----------------+------------------+--------------+---------+---------------------|
> | 2020-07-07 19:18:09.821 -0700 | OUTBOUND | SNOW.MY_TEST_ACCOUNT   | SNOW_DATA              | EXAMPLE        |                  | ACCOUNTADMIN |         |                     |
> | 2022-08-18 12:02:29.625 -0700 | OUTBOUND | SNOW.MY_TEST_ACCOUNT   | SNOW_DATA              | ALFALFA_DB     | AB12345, YZ23456 | ACCOUNTADMIN |         |                     |
> | 2022-08-18 14:02:40.625 -0700 | OUTBOUND | SNOW.MY_TEST_ACCOUNT   | SNOWIER_SHARE          | SALES_DB       |                  | ACCOUNTADMIN |         |                     |
> | 2022-08-20 15:03:50.625 -0700 | OUTBOUND | SNOW.MY_TEST_ACCOUNT   | SNOWY_SHARE            | SALES_DB       |                  | ACCOUNTADMIN |         |                     |
> | 2022-08-18 13:04:29.625 -0700 | OUTBOUND | SNOW.MY_TEST_ACCOUNT   | SNOW_SHARE             | SALES_DB       | AB12345          | ACCOUNTADMIN |         |                     |
> +-------------------------------+----------+------------------------+------------------------+----------------+------------------+--------------+---------+---------------------+
> ```

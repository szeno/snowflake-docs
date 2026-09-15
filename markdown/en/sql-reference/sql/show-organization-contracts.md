# SHOW ORGANIZATION CONTRACTS

Lists all active contracts currently mapped to the Snowflake accounts within the
customer’s organization.

Note

This command replaces `SHOW ORGANIZATION BILLING ENTITIES`. For more information,
see [Organization accounts: Transition from Billing Entity to Contract Number](/release-notes/bcr-bundles/un-bundled/bcr-2399).

See also:
:   [SHOW ACCOUNTS](/sql-reference/sql/show-accounts), [SHOW ORGANIZATION ACCOUNTS](/sql-reference/sql/show-organization-accounts),
    [CREATE ACCOUNT](/sql-reference/sql/create-account), [CREATE ORGANIZATION ACCOUNT](/sql-reference/sql/create-organization-account),
    [ALTER ACCOUNT](/sql-reference/sql/alter-account), [ALTER ORGANIZATION ACCOUNT](/sql-reference/sql/alter-organization-account)

## Syntax

Copy code

```
SHOW ORGANIZATION CONTRACTS
```

## Usage notes

- Only users with the [ORGADMIN](/user-guide/organization-administrators#label-org-admins-orgadmin) or [GLOBALORGADMIN](/user-guide/organization-administrators#using-the-globalorgadmin-role)
  role can run this command, which means it can only be run from either an account that
  has the ORGADMIN role enabled or the [Organization Account](/user-guide/organization-accounts).
- Returns one row per active contract mapped to the organization.
- This command does not support a LIKE filter.

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

## Output

The command output provides contract properties in the following columns:

| Column | Description |
| --- | --- |
| `contract_number` | Contract identifier number(for example, `155962`). |
| `agreement_type` | The type of the contract that is negotiated with Snowflake (for example, `Capacity`, `On Demand`, `Evaluation`). |
| `contract_start_date` | Contract start time (UTC). NULL if the source timestamp is null or zero. |
| `contract_end_date` | Contract end time (UTC). NULL if the contract is open-ended or if the source timestamp is null or zero. |
| `currency` | Contract currency code (for example, `USD`). |
| `allowed_cross_cloud_providers` | Cloud providers allowed for cross-cloud usage under this contract. NULL when the list is empty. |

Expand

Show lessSee more

## Examples

List all active contracts in the current organization:

Copy code

```
USE ROLE ORGADMIN;

SHOW ORGANIZATION CONTRACTS;
```

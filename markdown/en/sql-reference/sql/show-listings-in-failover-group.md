# SHOW LISTINGS IN FAILOVER GROUP

[Business Critical Feature](/user-guide/intro-editions)

Requires Business Critical Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Shows the listings in a [failover group](/user-guide/account-replication-intro#label-replication-and-failover-groups).

See also:
:   [SHOW DATABASES IN FAILOVER GROUP](/sql-reference/sql/show-databases-in-failover-group), [SHOW SHARES IN FAILOVER GROUP](/sql-reference/sql/show-shares-in-failover-group)

## Syntax

Copy code

```
SHOW LISTINGS IN FAILOVER GROUP <name>
```

## Parameters

`name`
:   Specifies the identifier for the failover group.

## Access control requirements

To review the roles that are required to monitor replication and failover on group objects in the system, see [Replication privileges](/user-guide/account-replication-considerations#label-replication-privileges).

## Usage notes

- Executing this command requires a role with either the OWNERSHIP or MONITOR privilege on the failover group. The command
  only returns objects for which the current user’s current role has been granted at least one access privilege.
- To retrieve the list of failover groups in your organization, use [SHOW FAILOVER GROUPS](/sql-reference/sql/show-failover-groups).

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

The command output provides listing properties and metadata in the following columns:

|  |  |
| --- | --- |
| Column | Description |
| `global_name` | Global name of the listing |
| `name` | Name specified when the listing was created. |
| `title` | Title specified in the listing manifest. |
| `subtitle` | Sub title specified in the listing manifest. |
| `profile` | Provider profile name as specified in the listing manifest. |
| `created_on` | Date and time when the listing was created. |
| `updated_on` | Date and time when the listing was last updated. |
| `published_on` | Date and time when the listing was last published. |
| `state` | State of the listing, one of:   - DRAFT - PUBLISHED - UNPUBLISHED |
| `review_state` | Review state for public listings only, one of:   - UNSENT - PENDING - REJECTED - APPROVED - CANCELLED |
| `comment` | Associated comment, if present. |
| `owner` | Listing owner. |
| `owner_role_type` | Owner role type. |
| `regions` | List of regions where a public listing is available. |
| `target_accounts` | Comma separated list of target accounts. |
| `is_monetized` | Is monetized flag. |
| `is_application` | Is application flag. If `true` a Snowflake Native App is attached to the listing. |
| `is_targeted` | Is targeted flag. |
| `is_limited_trial` | Whether the listing is available for limited trial before purchasing. |
| `is_by_request` | Whether the listing is a personalized listing. |
| `distribution` | Whether the listing is an EXTERNAL or ORGANIZATION listing. |
| `is_mountless_queryable` | Whether the listing can be queried by a consumer without mounting using the Uniform Listing Locator (ULL) for the listing. |
| `rejected_on` | Date and time when the public listing for approval was last rejected. |
| `organization_profile_name` | The profile associated with the ORGANIZATION listing. |
| `uniform_listing_locator` | The ULL tha allows consumers to access the organization listing without mounting. |
| `detailed_target_accounts` | Private listing target account details with company name included. |
| `compliance_badges` | List of compliance certifications that were approved by Snowflake’s compliance team for the listing, if any. Available certifications include:   - SOC2 - HIPAA - ISO27001 |

Expand

Show lessSee more

## Examples

List the listings in the failover group `myfg`:

Copy code

```
SHOW LISTINGS IN FAILOVER GROUP myfg;
```

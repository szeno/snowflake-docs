# SHOW LISTINGS

Lists the [listings](/collaboration/collaboration-listings-about) that you have privileges to access.
Shows only listings where the user running the command has any of USAGE, MODIFY, or OWNERSHIP against the listing.

See also:
:   [CREATE LISTING](/sql-reference/sql/create-listing), [ALTER LISTING](/sql-reference/sql/alter-listing), [DESCRIBE LISTING](/sql-reference/sql/desc-listing), [DROP LISTING](/sql-reference/sql/drop-listing)

## Syntax

Copy code

```
SHOW LISTINGS [ LIKE '<pattern>' ]
              [ STARTS WITH '<name_string>' ]
              [ LIMIT <rows> [ FROM '<name_string>' ] ]
```

## Optional parameters

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

- You can show a listing only if you use a role that has the USAGE, MODIFY, or OWNERSHIP privilege on the listing.

- The value for `LIMIT rows` can’t exceed `10000`. If `LIMIT rows` is omitted, the command results in an error
  if the result set is larger than ten thousand rows.

  To view results for which more than ten thousand records exist, either include `LIMIT rows` or query the corresponding
  view in the [Snowflake Information Schema](/sql-reference/info-schema).

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

Show all the listings with names that start with `MYLISTING`:

> Copy code
>
> ```
> SHOW LISTINGS LIKE 'MYLISTING%'
> ```

Show ten listings starting from listing `MYLISTING`:

> Copy code
>
> ```
> SHOW LISTINGS LIMIT 10 FROM 'MYLISTING%'
> ```

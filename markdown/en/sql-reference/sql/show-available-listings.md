# SHOW AVAILABLE LISTINGS

Lists the listings that are available to the user who runs the command.
For more information, see [Listing availability options](https://other-docs.snowflake.com/collaboration/collaboration-listings-about#label-listing-availability).

See also:
:   [CREATE LISTING](/sql-reference/sql/create-listing), [CREATE APPLICATION](/sql-reference/sql/create-application), [ALTER LISTING](/sql-reference/sql/alter-listing), [DESCRIBE LISTING](/sql-reference/sql/desc-listing), [DROP LISTING](/sql-reference/sql/drop-listing)

## Syntax

Copy code

```
SHOW AVAILABLE LISTINGS

SHOW [ TERSE ] AVAILABLE LISTINGS
    [ LIMIT <rows> ]
    [ IS_IMPORTED = TRUE ]
    [ IS_ORGANIZATION = TRUE ]
    [ IS_SHARED_WITH_ME = TRUE ]
```

## Parameters

`LIMIT rows`
:   Optionally limits the maximum number of rows returned, while also enabling “pagination” of the results. The actual number of rows
    returned might be less than the specified limit. For example, the number of existing objects is less than the specified limit.

`TERSE`
:   Optionally returns output containing only the following columns:

    - `created_on`
    - `global_name`
    - `profile`
    - `title`

`IS_SHARED_WITH_ME = TRUE`
:   Optional, shows only listings shared privately with the current user.

    > | Property value | Behavior |
    > | --- | --- |
    > | Not set | All listings are returned. |
    > | TRUE | Only listings shared privately with the current user are returned. |
    >
    > Expand
    >
    > Show lessSee more

`IS_IMPORTED = TRUE`
:   Optional, shows only imported listings, but filters returned results according to:

    | Property value | Behavior |
    | --- | --- |
    | Not set | All listings are returned. |
    | TRUE | Only imported listings are returned. |

    Expand

    Show lessSee more

`IS_ORGANIZATION = TRUE`
:   Optional, shows only organization level listings.

    | Property value | Behavior |
    | --- | --- |
    | Not set | All listings are returned. |
    | TRUE | Shows organization level listings. |

    Expand

    Show lessSee more

## Usage notes

Only one of filters `IS_IMPORTED`, `IS_ORGANIZATION`, or `IS_SHARED_WITH_ME` may be specified at a time.

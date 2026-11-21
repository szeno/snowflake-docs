# DROP LISTING

Removes the specified [listing](/collaboration/collaboration-listings-about) from the system and immediately revokes access for all consumers.

Important

Before dropping a listing, ensure that:

- The listing is in state DRAFT or UNPUBLISH. For more information about changing listing states, see [ALTER LISTING](/sql-reference/sql/alter-listing).
- Previously published listings are not mounted by any consumers.

See also:

> [CREATE LISTING](/sql-reference/sql/create-listing), [ALTER LISTING](/sql-reference/sql/alter-listing), [DESCRIBE LISTING](/sql-reference/sql/desc-listing), [SHOW LISTINGS](/sql-reference/sql/show-listings), [SHOW VERSIONS IN LISTING](/sql-reference/sql/show-versions-in-listing), [Listing manifest reference](/progaccess/listing-manifest-reference)

## Syntax

Copy code

```
DROP LISTING <name>
```

## Parameters

`name`
:   The identifier of the listing to drop. If the identifier contains spaces, special characters, or mixed-case characters, the
    entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also case-sensitive.

## Usage notes

- Only the listing owner, the role with the OWNERSHIP privilege on the listing, has the privileges to drop a listing.
  Executing this command with any other role returns an error.
- Dropped listings cannot be recovered; they must be recreated.
- Dropping a listing automatically invokes the retirement process for all public and monetized listings.
  Additionally, for other listing types the listing is dropped immediately, and all consumer access automatically revoked.
- When Snowflake detects that a Listing Auto-Fulfillment (LAF) replication group is no longer in use (the replication group has no
  share objects), Snowflake automatically cleans it up. This can happen when you drop a listing, remove regions, or remove all
  consumers in a region. The cleanup process can take several days.

  To remove the replication group immediately, transfer ownership of the replication group to a role you control, and then run
  [DROP REPLICATION GROUP](drop-replication-group). For example:

  Copy code

  ```
  GRANT OWNERSHIP ON REPLICATION GROUP myrg TO ROLE accountadmin
    REVOKE CURRENT GRANTS;
  DROP REPLICATION GROUP myrg;
  ```

## Examples

> Copy code
>
> ```
> DROP LISTING IF EXISTS MYLISTING
> ```
>
> ```
> +----------------------------------+
> | status                           |
> |----------------------------------|
> | MYLISTING successfully dropped. |
> +----------------------------------+
> ```

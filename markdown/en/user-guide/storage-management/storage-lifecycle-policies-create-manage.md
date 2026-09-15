# Create and manage storage lifecycle policies

The following sections explain how to create, recreate, and manage storage lifecycle policies on your tables.

## Create a storage lifecycle policy

To create a storage lifecycle policy, use the [CREATE STORAGE LIFECYCLE POLICY](/sql-reference/sql/create-storage-lifecycle-policy) command.

When you create a storage lifecycle policy, you can choose an [archive tier](/user-guide/storage-management/storage-lifecycle-policies#label-slp-archive-tiers)
and optionally set an archival period in days.
If you set an archival period, Snowflake moves table rows that match the policy expression into a lower-cost storage tier
for the specified number of days before expiring the rows.
Snowflake also enables change tracking on any tables that you attach the policy to.

For example:

Copy code

```
CREATE STORAGE LIFECYCLE POLICY my_slp
  AS (event_ts TIMESTAMP, account_id NUMBER)
  RETURNS BOOLEAN ->
    event_ts < DATEADD(DAY, -60, CURRENT_TIMESTAMP())
    AND EXISTS (
      SELECT 1 FROM closed_accounts
      WHERE id = account_id
    )
  ARCHIVE_TIER = COOL
  ARCHIVE_FOR_DAYS = 90;
```

Note

For considerations when you work with tables that have archival storage policies, see [Archival storage policies](/user-guide/storage-management/storage-lifecycle-policies#label-slp-archive-limitations).

## Recreate a storage lifecycle policy

This feature extends the [GET\_DDL](/sql-reference/functions/get_ddl) command to recreate a
specified storage lifecycle policy. You might do this if you want to change the archival tier for a policy.

To recreate a storage lifecycle policy named `my_slp`, return the DDL, as shown in the following example:

Copy code

```
SELECT GET_DDL('policy','my_slp');
```

Output:

```
---------------------------------------------------------------------+
                      GET_DDL('POLICY','SLP')                        |
---------------------------------------------------------------------+
create or replace storage lifecycle policy SLP as                    |
  (event_ts timestamp, account_id number)
    returns boolean ->
    event_ts < dateadd(day, -60, current_timestamp())
    and exists (
      select 1 from closed_accounts
      where id = account_id
  )
  ARCHIVE_FOR_DAYS = 365                                             |
;                                                                    |
---------------------------------------------------------------------+
```

## Manage storage lifecycle policies on tables

Use the following options to manage storage lifecycle policy attachments.

### Attach a policy to a table

You can manage multiple tables with one storage lifecycle policy. Attach the policy when you create or alter the table.

To create a table and attach the policy to a new table by
using the specified columns, use [CREATE TABLE](/sql-reference/sql/create-table), as shown in the following example.

Note

- You must have the necessary privileges to apply the policy. For information about required privileges, see
  [Storage lifecycle policy privileges](/user-guide/security-access-control-privileges#label-security-access-control-slp-privileges).
- A table can have only one attached storage lifecycle policy.
- The number of columns must match the argument count in the policy function signature, and the column data must be compatible with the argument types.
- Associated policies aren’t affected if you rename table columns. Snowflake associates policies to tables by using the column IDs.
- In order to evaluate and apply storage lifecycle policy expressions, Snowflake internally and temporarily bypasses any governance policies on a table.

Copy code

```
CREATE TABLE my_table
  ...
  WITH STORAGE LIFECYCLE POLICY my_slp ON (col1);
```

To attach the policy to an existing table by using the specified columns, use [ALTER TABLE](/sql-reference/sql/alter-table), as shown in the following example:

Copy code

```
ALTER TABLE my_table ADD STORAGE LIFECYCLE POLICY my_slp
  ON (col1);
```

### Best practices

#### Use date conversions for time-based expressions

To improve performance and ensure consistent policy execution, convert timestamps to dates in your policy expressions
when you compare time values.

For example, consider this policy expression:

Copy code

```
event_time < DATEADD(DAY, -400, CURRENT_TIMESTAMP())
```

This comparison includes the time component of the timestamp, which can cause inconsistent behavior. When data gets inserted
in chronological order by `event_time`, the policy’s execution time affects how many rows get deleted from each file.

To avoid this inconsistent behavior, convert timestamps to dates in your expression:

Copy code

```
event_time < TO_DATE(DATEADD(DAY, -400, CURRENT_TIMESTAMP()))
```

This method provides consistent policy execution regardless of the time of day.

#### Cluster on policy attachment columns

When you attach a storage lifecycle policy, you specify the column values that Snowflake passes to the policy
expression in the `ON (...)` clause. If the table isn’t [clustered](/user-guide/tables-clustering-keys) on those
columns, each daily policy execution might scan more micro-partitions than necessary. That can increase runtime
and [policy execution costs](/user-guide/storage-management/storage-lifecycle-policies-billing).

To improve performance and control cost, define a clustering key that includes the attachment columns, or keys
that align with how your policy expression filters rows.

### Apply a policy as a one-time operation

If you only need to expire or archive historical data once, as a one-time operation, we recommend the following procedure:

1. Create, and then attach a storage lifecycle policy to your table.
2. Wait for the policy to execute, and then archive or expire the data.

   Monitor the [INFORMATION\_SCHEMA.STORAGE\_LIFECYCLE\_POLICY\_HISTORY](/sql-reference/functions/storage_lifecycle_policy_history) table
   function to confirm the process is complete.
3. To prevent recurring charges, [remove the storage lifecycle policy](#label-slp-remove-slp)
   from the table.

   Storage lifecycle policies incur cost *per execution*.

This method ensures that you only pay for a single execution instead of ongoing daily charges for a
policy that has already processed all eligible data. For more information about cost,
see [Billing for storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies-billing).

### Remove a policy from a table

To remove a storage lifecycle policy from a table, use [ALTER TABLE](/sql-reference/sql/alter-table), as shown in the following example:

Copy code

```
ALTER TABLE my_table DROP STORAGE LIFECYCLE POLICY;
```

- This command removes all future policy executions for this table.
- Running policy executions might complete before they are dropped from the table.
- To drop a storage lifecycle policy, you must have the OWNERSHIP privilege on the table the policy is attached to.

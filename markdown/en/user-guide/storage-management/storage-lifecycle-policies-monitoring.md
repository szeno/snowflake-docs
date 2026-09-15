# Monitor storage lifecycle policies

Identify which tables have storage lifecycle policies
attached, and monitor storage lifecycle policy runs by using Snowflake’s built-in functions.

Note

For information about monitoring storage lifecycle policy costs,
see [Billing for storage lifecycle policies](/user-guide/storage-management/storage-lifecycle-policies-billing).

## Monitor policy assignments

To view storage lifecycle policy metadata, use the following views:

- [ACCOUNT\_USAGE.STORAGE\_LIFECYCLE\_POLICIES](/sql-reference/account-usage/storage_lifecycle_policies)
- [ORGANIZATION\_USAGE.STORAGE\_LIFECYCLE\_POLICIES](/sql-reference/organization-usage/storage_lifecycle_policies)
- [ACCOUNT\_USAGE.STORAGE\_LIFECYCLE\_POLICY\_HISTORY](/sql-reference/account-usage/storage_lifecycle_policy_history)
- [ORGANIZATION\_USAGE.STORAGE\_LIFECYCLE\_POLICY\_HISTORY](/sql-reference/organization-usage/storage_lifecycle_policy_history)

## See lifecycle policy attachments

To see which tables a particular lifecycle policy is attached to, call the [POLICY\_REFERENCES](/sql-reference/functions/policy_references) table function in
the [Snowflake Information Schema](/sql-reference/info-schema). The function displays only the tables that you have the OWNERSHIP privilege on.

The function returns a row for each table in a database that has the specified policy attached to it.

### Example: List all tables associated with a policy

The following query retrieves a list of tables with a specified storage lifecycle policy attached:

Copy code

```
SELECT *
  FROM TABLE(
    my_db.INFORMATION_SCHEMA.POLICY_REFERENCES(
    POLICY_NAME => 'my_storage_lifecycle_policy'
  )
);
```

### Example: Find the policy assigned to a table

Retrieve the policy assigned to a specified table:

Copy code

```
SELECT *
  FROM TABLE(
    my_db.INFORMATION_SCHEMA.POLICY_REFERENCES(
      REF_ENTITY_NAME => 'my_db.my_schema.my_table',
      REF_ENTITY_DOMAIN => 'table'))
  WHERE POLICY_KIND = 'STORAGE_LIFECYCLE_POLICY';
```

## Monitor storage lifecycle policy runs

To monitor storage lifecycle policy executions over the last 14 days, use the [STORAGE\_LIFECYCLE\_POLICY\_HISTORY](/sql-reference/functions/storage_lifecycle_policy_history) table function. For information about the function output, see the [STORAGE\_LIFECYCLE\_POLICY\_HISTORY](/sql-reference/functions/storage_lifecycle_policy_history) page.

The following example retrieves the 100 most recent executions for a policy attached to a specified table,
scheduled within the last day:

Copy code

```
SELECT * FROM
  TABLE(
    INFORMATION_SCHEMA.STORAGE_LIFECYCLE_POLICY_HISTORY(
      REF_ENTITY_NAME => 'my_db.my_schema.my_source_table',
      REF_ENTITY_DOMAIN => 'table',
      TIME_RANGE_START => DATEADD('DAY', -1, CURRENT_TIMESTAMP()),
      RESULT_LIMIT => 100
    )
  );
```

Alternatively, to retrieve historical data for storage lifecycle policy runs, use the following views:

- [ACCOUNT\_USAGE.STORAGE\_LIFECYCLE\_POLICY\_HISTORY](/sql-reference/account-usage/storage_lifecycle_policy_history)
- [ORGANIZATION\_USAGE.STORAGE\_LIFECYCLE\_POLICY\_HISTORY](/sql-reference/organization-usage/storage_lifecycle_policy_history)

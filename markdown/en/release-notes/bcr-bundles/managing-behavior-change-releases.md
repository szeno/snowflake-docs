# Behavior change management

This document explains how to check whether a particular
[behavior change bundle](/release-notes/behavior-change-policy#label-behavior-change-bundles) is enabled in your account and how to enable or disable it.

## Overview

Snowflake implements behavior changes monthly in bundles included in regularly-scheduled
[releases](/user-guide/intro-releases). During the testing period and opt-out period for each behavior change bundle,
you can enable or disable the bundle in your account. This document explains how to check whether a particular bundle is enabled
in your account and how to enable or disable it.

In this document, the name of the behavior change bundle is in the form `YYYY_NN`. For the names of the
currently available behavior change bundles, see [Behavior change announcements](/release-notes/behavior-changes).

Note

Behavior changes in bundles cannot be enabled/disabled individually. To enable/disable a behavior change, you must
enable/disable the bundle containing the change.

## Checking the status of a behavior change bundle in your account

To check whether a specific behavior change bundle is enabled in your account, call the
[SYSTEM$BEHAVIOR\_CHANGE\_BUNDLE\_STATUS](/sql-reference/functions/system_behavior_change_bundle_status) function. For example, to check the status of the bundle
named `2024_02`:

Copy code

```
SELECT SYSTEM$BEHAVIOR_CHANGE_BUNDLE_STATUS('2024_02');
```

```
+-------------------------------------------------+
| SYSTEM$BEHAVIOR_CHANGE_BUNDLE_STATUS('2024_02') |
|-------------------------------------------------|
| DISABLED                                        |
+-------------------------------------------------+
```

To check the status of all currently available behavior change bundles, call the
[SYSTEM$SHOW\_ACTIVE\_BEHAVIOR\_CHANGE\_BUNDLES](/sql-reference/functions/system_show_active_behavior_change_bundles) function:

Copy code

```
SELECT SYSTEM$SHOW_ACTIVE_BEHAVIOR_CHANGE_BUNDLES();
```

```
+--------------------------------------------------------------------------------------------------------------+
| SYSTEM$SHOW_ACTIVE_BEHAVIOR_CHANGE_BUNDLES()                                                                 |
|--------------------------------------------------------------------------------------------------------------|
| [{"name":"2023_08","isDefault":true,"isEnabled":true},{"name":"2024_01","isDefault":false,"isEnabled":true}] |
+--------------------------------------------------------------------------------------------------------------+
```

## Enabling a behavior change bundle in your account

To enable a particular behavior change in your account, call the
[SYSTEM$ENABLE\_BEHAVIOR\_CHANGE\_BUNDLE](/sql-reference/functions/system_enable_behavior_change_bundle) function. For example, to enable the bundle
named `2024_02`:

Copy code

```
SELECT SYSTEM$ENABLE_BEHAVIOR_CHANGE_BUNDLE('2024_02');
```

```
+-------------------------------------------------+
| SYSTEM$ENABLE_BEHAVIOR_CHANGE_BUNDLE('2024_02') |
|-------------------------------------------------|
| ENABLED                                         |
+-------------------------------------------------+
```

## Disabling a behavior change bundle in your account

To disable a particular behavior change in your account, call the
[SYSTEM$DISABLE\_BEHAVIOR\_CHANGE\_BUNDLE](/sql-reference/functions/system_disable_behavior_change_bundle). For example, to disable the bundle
named `2024_02`:

Copy code

```
SELECT SYSTEM$DISABLE_BEHAVIOR_CHANGE_BUNDLE('2024_02');
```

```
+-------------------------------------------------+
| SYSTEM$DISABLE_BEHAVIOR_CHANGE_BUNDLE('2024_02')|
|-------------------------------------------------|
| DISABLED                                        |
+-------------------------------------------------+
```

## Determining the current version of your account

To check the current version of Snowflake that is in your account, call the
[CURRENT\_VERSION](/sql-reference/functions/current_version) function. For example:

> Copy code
>
> ```
> SELECT CURRENT_VERSION();
> ```
>
> ```
> +-------------------+
> | CURRENT_VERSION() |
> |-------------------|
> | 8.5.1             |
> +-------------------+
> ```

## Mitigating masking policy return value updates

In the `2024_04` [bundle](/release-notes/bcr-bundles/2024_04/bcr-1355), there are changes to the values for precision and
scale in masking policy conditions (collectively: “return value updates”). A query on a column protected by a masking policy fails when the
following are true:

- The bundle is enabled.
- The masking policy conditions return a value whose precision is greater than the precision of the column to which the masking
  policy is assigned.

If the scale of the return value is larger than the scale of the column, the value is truncated to match the scale of the column.

If you want to apply the new behavior to a pre-existing policy, create a new masking policy and replace the pre-existing policy using the
`FORCE` [keyword](/user-guide/security-column-intro#label-security-column-intro-replace-policy).

When the bundle is enabled, you can test the behavior as follows:

1. Create a policy:

   Copy code

   ```
   CREATE MASKING POLICY MP AS (n NUMBER)
   RETURNS NUMBER -> 12345;
   ```
2. Assign the policy:

   Copy code

   ```
   CREATE TABLE t(col1 NUMBER(2,0));

   ALTER TABLE t MODIFY COLUMN col1 SET MASKING POLICY mp;
   INSERT INTO t VALUES (10);
   ```
3. Query the column (fails):

   Copy code

   ```
   SELECT * FROM t;
   ```

Note

The changes to the values for precision and scale are not applicable to the string data type.

To determine the impact of this change and provide enough time to update the masking policy conditions to protect data, query the
SNOWFLAKE.BCR\_ROLLOUT.BCR\_2024\_03\_DDM\_ROLLOUT view to understand how the future return value updates affect your account.

The BCR\_2024\_03\_DDM\_ROLLOUT view is temporary. Snowflake will remove the view when the return value updates are generally enabled
in a future behavior change bundle. At this point, you will not be able to query the view to determine affected columns and policies or
prevent column query or masking policy assignment operation failures due to return value updates.

The view records data starting from March 2024. If a query on the view takes a long time to complete, you can specify the start date and
end date session variables using a [SET](/sql-reference/sql/set) command. These variables help to reduce the number of rows to evaluate when
you query the view. For example:

> Copy code
>
> ```
> SET DDM_CASTING_BCR_START_DATE = '2024-03-01';
> SET DDM_CASTING_BCR_END_DATE = '2024-04-03';
> ```

### Identify masking policy & column associations

To query the view and mitigate the upcoming return value changes, do the following:

1. Query the SNOWFLAKE.BCR\_ROLLOUT.BCR\_2024\_03\_DDM\_ROLLOUT view. For example:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;
   SET DDM_CASTING_BCR_START_DATE = '2024-03-01';
   SET DDM_CASTING_BCR_END_DATE = '2024-04-03';
   SELECT * FROM SNOWFLAKE.BCR_ROLLOUT.BCR_2024_03_DDM_ROLLOUT;
   ```
2. Evaluate the REASON column in the [BCR\_2024\_03\_DDM\_ROLLOUT View Reference](#bcr-2024-03-ddm-rollout-view-reference) section to determine what update needs to be made to the
   masking policy conditions.
3. Update the masking policy conditions with an [ALTER MASKING POLICY](/sql-reference/sql/alter-masking-policy) statement to ensure the column data remains
   protected and that policy assignment operations or protected column queries do not fail.
4. Test the new policy conditions by querying the table columns to which the masking policies are assigned.

### BCR\_2024\_03\_DDM\_ROLLOUT view reference

The BCR\_2024\_03\_DDM\_ROLLOUT view (in the SNOWFLAKE.BCR\_ROLLOUT schema) records information starting on July 15, 2022 and contains the
following columns:

| Column | Data type | Description |
| --- | --- | --- |
| `policy_name` | VARCHAR | The name of the policy. |
| `policy_id` | NUMBER | Internal/system-generated identifier for the policy. |
| `policy_schema` | VARCHAR | The parent schema of the policy. |
| `policy_database` | VARCHAR | The parent database of the policy. |
| `policy_body` | VARIANT | The conditions of the policy to mask or unmask the column data. |
| `column_name` | VARCHAR | The name of the column that has the policy. |
| COLUMN\_TYPE | VARCHAR | The data type of the column. |
| COLUMN\_LENGTH | NUMBER | The length of the column that has the policy or `[NULL]` if not set for the column. |
| COLUMN\_PRECISION | NUMBER | The precision of the column that has the policy or `[NULL]` if not set for the column. |
| COLUMN\_SCALE | NUMBER | The scale of the column that has the policy or `[NULL]` if not set for the column. |
| TABLE\_NAME | VARCHAR | The name of the table. |
| `table_id` | NUMBER | Internal/system-generated identifier for the table. |
| `table_schema` | VARCHAR | The parent schema of the table. |
| `table_database` | VARCHAR | The parent database of the table. |
| `table_kind` | VARCHAR | The type of table. One of the following: `TABLE`, `LOCAL TEMPORARY`, `VIEW`, `MATERIALIZED VIEW`, `EXTERNAL TABLE`, or `DYNAMIC TABLE`. |
| `reason` | VARCHAR | Possible reason for the mismatch. One of the following: `precision` or `scale`. |
| LARGEST\_MASKED\_SIZE | NUMBER | The maximum length, scale, or precision a masked value can have based on the masking policy assigned to the column. |

Expand

Show lessSee more

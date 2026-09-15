Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# JOIN\_POLICIES view

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts that are Enterprise Edition (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view lists the [join policies](/user-guide/join-policies) in your account.

Each row in this view corresponds to a different join policy.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| POLICY\_ID | NUMBER | Internal/system-generated identifier for the policy. |
| POLICY\_NAME | VARCHAR | Name of the policy. |
| POLICY\_SCHEMA\_ID | NUMBER | Internal/system-generated identifier for the schema in which the policy resides. |
| POLICY\_SCHEMA | VARCHAR | Schema that contains the policy. |
| POLICY\_CATALOG\_ID | NUMBER | Internal/system-generated identifier for the database in which the policy resides. |
| POLICY\_CATALOG | VARCHAR | Database to which the policy belongs. |
| POLICY\_OWNER | VARCHAR | Name of the role that owns the policy. |
| POLICY\_SIGNATURE | VARCHAR | Type signature of the policy’s arguments. |
| POLICY\_RETURN\_TYPE | VARCHAR | Return value data type. |
| POLICY\_BODY | VARCHAR | Policy definition. |
| POLICY\_COMMENT | VARIANT | Comments entered for the policy (if any). |
| CREATED | TIMESTAMP\_LTZ | Date and time when the policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the policy was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the policy was dropped. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Usage notes

- Latency for the view can be up to 120 minutes (2 hours).
- The view only displays objects for which the current role for the session has been granted access privileges.

## Example

Copy code

```
SELECT policy_name, policy_body, created
  FROM SNOWFLAKE.ACCOUNT_USAGE.JOIN_POLICIES
  WHERE policy_name='JP2' AND created LIKE '2024-11-26%';
```

```
+-------------+----------------------------------------------------------+-------------------------------+
| POLICY_NAME | POLICY_BODY                                              | CREATED                       |
|-------------+----------------------------------------------------------+-------------------------------|
| JP2         | CASE                                                     | 2024-11-26 11:22:54.848 -0800 |
|             |           WHEN CURRENT_ROLE() = 'ACCOUNTADMIN'           |                               |
|             |             THEN JOIN_CONSTRAINT(JOIN_REQUIRED => FALSE) |                               |
|             |           ELSE JOIN_CONSTRAINT(JOIN_REQUIRED => TRUE)    |                               |
|             |         END                                              |                               |
+-------------+----------------------------------------------------------+-------------------------------+
```

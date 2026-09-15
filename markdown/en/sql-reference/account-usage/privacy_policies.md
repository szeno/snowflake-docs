Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# PRIVACY\_POLICIES view

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This Account Usage view provides the [privacy policies](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies) in your account.

Each row in this view corresponds to a different privacy policy.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| `policy_id` | NUMBER | Internal/system-generated identifier for the privacy policy. |
| `policy_name` | VARCHAR | Name of the privacy policy. |
| `policy_schema_id` | NUMBER | Internal/system-generated identifier for the schema in which the policy resides. |
| `policy_schema` | VARCHAR | Schema that contains the privacy policy. |
| `policy_catalog_id` | NUMBER | Internal/system-generated identifier for the database in which the policy resides. |
| `policy_catalog` | VARCHAR | Database to which the privacy policy belongs. |
| `policy_owner` | VARCHAR | Name of the role that owns the privacy policy. |
| `policy_signature` | VARCHAR | Type signature of the privacy policy’s arguments. |
| `policy_return_type` | VARCHAR | Return value data type. |
| `policy_body` | VARCHAR | Privacy policy definition. |
| `policy_comment` | VARIANT | Comments entered for the privacy policy (if any). |
| `created` | TIMESTAMP\_LTZ | Date and time when the privacy policy was created. |
| `last_altered` | TIMESTAMP\_LTZ | Date and time when the privacy policy was last altered. |
| `deleted` | TIMESTAMP\_LTZ | Date and time when the privacy policy was dropped. |
| `owner_role_type` | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).
- The view only displays objects for which the current role for the session has been granted access privileges.

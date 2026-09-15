Schema:
:   [ACCOUNT\_USAGE](/sql-reference/account-usage#label-account-usage-views)

# PASSWORD\_POLICIES view

This Account Usage view provides the user-defined [password policies](/user-guide/password-authentication#label-custom-password-policies) in your account.

Each row in this view corresponds to a different password policy.

## Columns

| Column Name | Data Type | Description |
| --- | --- | --- |
| NAME | VARCHAR | Name of the policy. |
| ID | NUMBER | Internal/system-generated identifier for the password policy. |
| SCHEMA\_ID | VARCHAR | Internal/system-generated identifier for the schema in which the policy resides. |
| SCHEMA | VARCHAR | Schema to which the password policy belongs. |
| DATABASE\_ID | VARCHAR | Internal/system-generated identifier for the database in which the policy resides. |
| DATABASE | VARCHAR | Database to which the password policy belongs. |
| OWNER | VARCHAR | Name of the role that owns the password policy. |
| OWNER\_ROLE\_TYPE | VARCHAR | The type of role that owns the object, for example `ROLE`.   If a Snowflake Native App owns the object, the value is `APPLICATION`.   Snowflake returns NULL if you delete the object because a deleted object does not have an owner role. |
| PASSWORD\_MIN\_LENGTH | NUMBER | Minimum password length allowed for the policy. |
| PASSWORD\_MAX\_LENGTH | NUMBER | Maximum password length allowed for the policy. |
| PASSWORD\_MIN\_UPPER\_CASE\_CHARS | NUMBER | Minimum number of uppercase characters allowed for the policy. |
| PASSWORD\_MIN\_LOWER\_CASE\_CHARS | NUMBER | Minimum number of lowercase characters allowed for the policy. |
| PASSWORD\_MIN\_NUMERIC\_CHARS | NUMBER | Minimum number of numeric characters allowed for the policy. |
| PASSWORD\_MIN\_SPECIAL\_CHARS | NUMBER | Minimum number of special characters allowed for the policy. |
| PASSWORD\_MIN\_AGE\_DAYS | NUMBER | The number of days a user must wait before a recently changed password can be changed again. |
| PASSWORD\_MAX\_AGE\_DAYS | NUMBER | Maximum number of days password is valid. |
| PASSWORD\_MAX\_RETRIES | NUMBER | Maximum number of password attempts allowed. |
| PASSWORD\_LOCKOUT\_TIME\_MINS | NUMBER | Minimum time in minutes before password can be retried. |
| COMMENT | VARCHAR | Comments entered for the password policy (if any). |
| CREATED | TIMESTAMP\_LTZ | Date and time when the password policy was created. |
| LAST\_ALTERED | TIMESTAMP\_LTZ | Date and time when the password policy was last altered. |
| DELETED | TIMESTAMP\_LTZ | Date and time when the password policy was dropped. |
| PASSWORD\_HISTORY | NUMBER | The number of the most recent passwords that Snowflake stores. These stored passwords cannot be repeated when a user updates their password value. |

Expand

Show lessSee more

## Usage notes

- Latency for the view may be up to 120 minutes (2 hours).

- The LAST\_ALTERED column is updated when the following operations are performed on an object:

  - DDL operations.
  - DML operations (for tables only). This column is updated even when no rows are affected by the DML statement.
  - Background maintenance operations on metadata performed by Snowflake.

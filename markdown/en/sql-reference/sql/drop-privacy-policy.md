# DROP PRIVACY POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Removes the specified [privacy policy](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies) from the current/specified schema.

See also:
:   [CREATE PRIVACY POLICY](/sql-reference/sql/create-privacy-policy) , [ALTER PRIVACY POLICY](/sql-reference/sql/alter-privacy-policy) , [DESCRIBE PRIVACY POLICY](/sql-reference/sql/desc-privacy-policy) , [SHOW PRIVACY POLICIES](/sql-reference/sql/show-privacy-policies)

## Syntax

Copy code

```
DROP PRIVACY POLICY <name>
```

## Parameters

`name`
:   Specifies the identifier for the privacy policy to drop.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Privacy policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

A privacy policy cannot be dropped successfully if it is currently assigned to a table or view.

Before executing a DROP statement, execute the following statement to determine if the privacy policy is set on any tables or views.

Copy code

```
SELECT * FROM TABLE(mydb.INFORMATION_SCHEMA.POLICY_REFERENCES(POLICY_NAME=>'my_privacy_policy'));
```

For each table or view, use [ALTER TABLE … DROP PRIVACY POLICY …](/sql-reference/sql/alter-table) or
[ALTER VIEW … DROP PRIVACY POLICY …](/sql-reference/sql/alter-view) to [detach the privacy policy](/user-guide/diff-privacy/differential-privacy-admin-privacy-policies#label-diff-privacy-admin-detach) from the
table or view.

## Examples

The following example drops the privacy policy named `myprivpolicy`:

Copy code

```
DROP PRIVACY POLICY myprivpolicy;
```

```
+------------------------------------+
| status                             |
|------------------------------------|
| MYPRIVPOLICY successfully dropped. |
+------------------------------------+
```

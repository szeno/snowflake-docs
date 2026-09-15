# ALTER DATA MOVEMENT POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Modifies the properties of an existing [data movement policy](/user-guide/data-movement-policies). You can replace, add to, or
remove from the rule lists, set or unset the comment, and rename the policy.

Any changes to the policy rules go into effect when the next data movement operation that uses the policy runs.

See also:
:   [CREATE DATA MOVEMENT POLICY](/sql-reference/sql/create-data-movement-policy) , [DROP DATA MOVEMENT POLICY](/sql-reference/sql/drop-data-movement-policy) , [DESCRIBE DATA MOVEMENT POLICY](/sql-reference/sql/desc-data-movement-policy) , [SHOW DATA MOVEMENT POLICIES](/sql-reference/sql/show-data-movement-policies)

    [CREATE DATA MOVEMENT RULE](/sql-reference/sql/create-data-movement-rule) , [ALTER DATA MOVEMENT RULE](/sql-reference/sql/alter-data-movement-rule) , [DROP DATA MOVEMENT RULE](/sql-reference/sql/drop-data-movement-rule)

## Syntax

Copy code

```
ALTER DATA MOVEMENT POLICY [ IF EXISTS ] <name> RENAME TO <new_name>

ALTER DATA MOVEMENT POLICY [ IF EXISTS ] <name> SET ENFORCE_RULES = ( <rule_name> [ , <rule_name> , ... ] )

ALTER DATA MOVEMENT POLICY [ IF EXISTS ] <name> SET ALERT_RULES = ( <rule_name> [ , <rule_name> , ... ] )

ALTER DATA MOVEMENT POLICY [ IF EXISTS ] <name> ADD ENFORCE_RULES = ( <rule_name> [ , <rule_name> , ... ] )

ALTER DATA MOVEMENT POLICY [ IF EXISTS ] <name> ADD ALERT_RULES = ( <rule_name> [ , <rule_name> , ... ] )

ALTER DATA MOVEMENT POLICY [ IF EXISTS ] <name> REMOVE ENFORCE_RULES = ( <rule_name> [ , <rule_name> , ... ] )

ALTER DATA MOVEMENT POLICY [ IF EXISTS ] <name> REMOVE ALERT_RULES = ( <rule_name> [ , <rule_name> , ... ] )

ALTER DATA MOVEMENT POLICY [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'

ALTER DATA MOVEMENT POLICY [ IF EXISTS ] <name> UNSET COMMENT
```

## Parameters

`name`
:   Specifies the identifier for the data movement policy to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Specifies the new identifier for the data movement policy; must be unique for the schema. The new identifier can’t be used if
    the identifier is already in place for a different data movement policy.

    For more details about identifiers, see [Identifier requirements](/sql-reference/identifiers-syntax).

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

    When an object is renamed, other objects that reference it must be updated with the new name.

`SET ...`
:   Replaces the entire contents of the specified rule list, the comment, or both for the data movement policy:

    `ENFORCE_RULES = ( rule_name [ , rule_name , ... ] )`
    :   Replaces the current `ENFORCE_RULES` list with the specified data movement rules. These rules block a data movement operation
        when the operation matches a rule.

    `ALERT_RULES = ( rule_name [ , rule_name , ... ] )`
    :   Replaces the current `ALERT_RULES` list with the specified data movement rules. These rules allow a data movement operation and
        generate an alert when the operation matches a rule.

    `COMMENT = 'string_literal'`
    :   Adds a comment or overwrites the existing comment for the data movement policy.

`ADD ...`
:   Adds the specified data movement rules to the `ENFORCE_RULES` or `ALERT_RULES` list without replacing the rules already in the
    list:

    - `ENFORCE_RULES = ( rule_name [ , rule_name , ... ] )`
    - `ALERT_RULES = ( rule_name [ , rule_name , ... ] )`

`REMOVE ...`
:   Removes the specified data movement rules from the `ENFORCE_RULES` or `ALERT_RULES` list without affecting the other rules in the
    list:

    - `ENFORCE_RULES = ( rule_name [ , rule_name , ... ] )`
    - `ALERT_RULES = ( rule_name [ , rule_name , ... ] )`

    A REMOVE operation succeeds only if the rule is currently in the specified list.

`UNSET ...`
:   Resets the comment to its default:

    - `COMMENT`

    To unset multiple properties or parameters with a single ALTER statement, separate each property or parameter with a comma.

    When unsetting a property or parameter, specify only the property or parameter name (unless the syntax above indicates that you
    should specify the value). Specifying the value returns an error.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Data movement policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- SET replaces the entire contents of a rule list. ADD and REMOVE modify a list incrementally, leaving the other rules in the
  list unchanged.
- A data movement rule can’t appear in both `ENFORCE_RULES` and `ALERT_RULES` at the same time, and each list can include at most
  one rule per data movement type.
- A data movement policy that’s attached to a tag or the account can’t be left empty by a SET or REMOVE operation.
- If you want to see the current definition of the policy, run the [DESCRIBE DATA MOVEMENT POLICY](/sql-reference/sql/desc-data-movement-policy) command or
  [GET\_DDL](/sql-reference/functions/get_ddl) function.
- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Replace the entire `ENFORCE_RULES` list:

Copy code

```
ALTER DATA MOVEMENT POLICY hr_pii_dmp
  SET ENFORCE_RULES = (hr_pii_copy_guard, hr_agent_guard);
```

Add a rule to the `ENFORCE_RULES` list without replacing the existing rules:

Copy code

```
ALTER DATA MOVEMENT POLICY hr_pii_dmp
  ADD ENFORCE_RULES = (hr_ui_download_guard);
```

Remove a rule from the `ALERT_RULES` list:

Copy code

```
ALTER DATA MOVEMENT POLICY hr_pii_dmp
  REMOVE ALERT_RULES = (hr_pii_copy_alert);
```

Rename a data movement policy:

Copy code

```
ALTER DATA MOVEMENT POLICY hr_pii_dmp RENAME TO hr_pii_policy;
```

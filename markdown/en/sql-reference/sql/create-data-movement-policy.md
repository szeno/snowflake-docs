# CREATE DATA MOVEMENT POLICY

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading, please contact
[Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Creates a new [data movement policy](/user-guide/data-movement-policies) in the current/specified schema or replaces an
existing data movement policy.

A data movement policy groups [data movement rules](/sql-reference/sql/create-data-movement-rule) into two lists:
`ENFORCE_RULES`, which can block a data movement operation, and `ALERT_RULES`, which allow the operation and generate an alert.
After you create a data movement policy, attach it to a tag with [ALTER TAG](/sql-reference/sql/alter-tag) or to the account with
[ALTER ACCOUNT](/sql-reference/sql/alter-account).

See also:
:   [ALTER DATA MOVEMENT POLICY](/sql-reference/sql/alter-data-movement-policy) , [DROP DATA MOVEMENT POLICY](/sql-reference/sql/drop-data-movement-policy) , [DESCRIBE DATA MOVEMENT POLICY](/sql-reference/sql/desc-data-movement-policy) , [SHOW DATA MOVEMENT POLICIES](/sql-reference/sql/show-data-movement-policies)

    [CREATE DATA MOVEMENT RULE](/sql-reference/sql/create-data-movement-rule) , [ALTER DATA MOVEMENT RULE](/sql-reference/sql/alter-data-movement-rule) , [DROP DATA MOVEMENT RULE](/sql-reference/sql/drop-data-movement-rule)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] DATA MOVEMENT POLICY [ IF NOT EXISTS ] <name>
  [ ENFORCE_RULES = ( <rule_name> [ , <rule_name> , ... ] ) ]
  [ ALERT_RULES = ( <rule_name> [ , <rule_name> , ... ] ) ]
  [ COMMENT = '<string_literal>' ]
```

## Required parameters

`name`
:   Specifies the identifier for the data movement policy; must be unique for the schema in which the policy is created.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

## Optional parameters

`ENFORCE_RULES = ( rule_name [ , rule_name , ... ] )`
:   Specifies the data movement rules that block a data movement operation when the operation matches a rule.

`ALERT_RULES = ( rule_name [ , rule_name , ... ] )`
:   Specifies the data movement rules that allow a data movement operation and generate an alert when the operation matches a rule.

`COMMENT = 'string_literal'`
:   Specifies a comment for the data movement policy.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE DATA MOVEMENT POLICY | Schema |  |

Expand

Show lessSee more

To attach a data movement policy to a tag or to the account, the role must also have the APPLY DATA MOVEMENT POLICY privilege
on the account. For details, see [ALTER TAG](/sql-reference/sql/alter-tag) and [ALTER ACCOUNT](/sql-reference/sql/alter-account).

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- A data movement policy can be created without any rules (with empty `ENFORCE_RULES` and `ALERT_RULES` lists), but an empty
  policy can’t be attached to a tag or the account.
- A data movement rule can’t appear in both `ENFORCE_RULES` and `ALERT_RULES` at the same time.
- Each list can include at most one rule per data movement type.
- A `UI_DOWNLOAD` rule can only be included in `ENFORCE_RULES`, not in `ALERT_RULES`.
- If you want to update an existing data movement policy and need to see the current definition of the policy, run the
  [DESCRIBE DATA MOVEMENT POLICY](/sql-reference/sql/desc-data-movement-policy) command or [GET\_DDL](/sql-reference/functions/get_ddl) function. The GET\_DDL output
  includes the `ENFORCE_RULES` and `ALERT_RULES` lists.

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

## Examples

Create a data movement policy that blocks operations matching one rule and alerts on operations matching another:

Copy code

```
CREATE OR REPLACE DATA MOVEMENT POLICY hr_pii_dmp
  ENFORCE_RULES = (hr_pii_copy_guard)
  ALERT_RULES = (hr_pii_copy_alert)
  COMMENT = 'PII guardrails for HR data';
```

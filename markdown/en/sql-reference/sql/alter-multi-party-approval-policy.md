# ALTER MULTI PARTY APPROVAL POLICY

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Modifies an existing Multi-party Approval policy by replacing its body with a new
definition.

## Syntax

Copy code

```
ALTER MULTI PARTY APPROVAL POLICY <name> RENAME TO <new_name>

ALTER MULTI PARTY APPROVAL POLICY <name>
  AS $$
  [ description: '<description>' ]
  rules:
    - name: <rule_name>
      [ description: '<description>' ]
      operations: [ <operation> [ , <operation> , ... ] ]
      approvers:
        users: [ '<username>' [ , '<username>' , ... ] ]
      [ required_approvals: <integer> ]
      [ request_duration_days: <integer> ]
      [ self_approval_allowed: { true | false } ]
  $$
```

## Parameters

`name`
:   Specifies the identifier for the Multi-party Approval policy to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`RENAME TO new_name`
:   Changes the name of the policy to *new\_name*. The new identifier must be unique for the
    schema.

    You can move the object to a different database and/or schema while optionally renaming the object. To do so, specify
    a qualified `new_name` value that includes the new database and/or schema name in the form
    `db_name.schema_name.object_name` or `schema_name.object_name`, respectively.

    Note

    - The destination database and/or schema must already exist. In addition, an object with the same name cannot already
      exist in the new location; otherwise, the statement returns an error.
    - Moving an object to a managed access schema is prohibited unless the object owner (that is, the role that has
      the OWNERSHIP privilege on the object) also owns the target schema.

`AS $$ ... $$`
:   YAML body that defines the policy’s approval rules. The new body follows the same
    structure as [CREATE MULTI PARTY APPROVAL POLICY](/sql-reference/sql/create-multi-party-approval-policy).

## Policy parameters

`description: 'description'`
:   An optional description of the policy.

`rules:`
:   A list of one or more approval rules. Each rule specifies which operations require
    approval and who can approve them.

### Rule parameters

Each rule in the `rules` list supports the following parameters.

#### Required rule parameters

`name: rule_name`
:   A unique name for this rule within the policy.

`operations: ( operation [ , operation , ... ] )`
:   A list of protected operations that this rule governs.

    For more information about each operation, see [Protected operations](/user-guide/multi-party-approval#protected-operations). Valid values, organized by group:

    **Admin operations**

    `MODIFY_MULTI_PARTY_APPROVAL`
    :   Requires approval for changes to Multi-party Approval policies, rules, account settings,
        and approver assignments, including attaching or detaching a policy from an account. This
        operation also covers creating, modifying, or dropping SAML2 security integrations, which
        control single sign-on and therefore who can authenticate as an approver.

        Important

        Every policy must have at least one rule that includes `MODIFY_MULTI_PARTY_APPROVAL` in
        its `operations` list. This self-protecting rule prevents a compromised administrator from
        unilaterally disabling or modifying Multi-party Approval itself.

    `DISABLE_MULTI_FACTOR_AUTHENTICATION`
    :   Requires approval for disabling Multi-Factor Authentication or resetting user passwords.

    `MODIFY_TRI_SECRET_SECURE`
    :   Requires approval for activating or deactivating Tri-Secret Secure customer-managed
        encryption keys. This operation requires the Business Critical Edition (or higher).

        Note

        After a policy with this operation has been attached to an account for 72 hours, the
        speed bump for Tri-Secret Secure operations is no longer required.

    `MODIFY_PRIVILEGED_ROLE_GRANTS`
    :   Requires approval for granting or revoking the `ACCOUNTADMIN` or `SECURITYADMIN`
        role, and for granting or revoking the `MANAGE GRANTS` privilege.

    `MODIFY_CORTEX_GUARDRAILS`
    :   Requires approval for modifying Cortex AI guardrail settings on the account.

    `MODIFY_DATA_RETENTION_TIME`
    :   Requires approval for modifying the `DATA_RETENTION_TIME_IN_DAYS` (Time Travel) parameter
        on accounts, databases, schemas, or tables.

    **Policy operations**

    `MODIFY_NETWORK_POLICY`
    :   Requires approval for changes to active network policies, network rules, and policy
        assignments on accounts and users.

    `MODIFY_SESSION_POLICY`
    :   Requires approval for modifying session policy settings or assignments on accounts and
        users.

    `MODIFY_AUTHENTICATION_POLICY`
    :   Requires approval for modifying authentication policy settings or assignments on accounts
        and users.

    `MODIFY_PASSWORD_POLICY`
    :   Requires approval for modifying password policy settings or assignments on accounts and
        users.

    **Security integration operations**

    `MODIFY_OAUTH_INTEGRATION`
    :   Requires approval for creating, modifying, or dropping Snowflake OAuth security
        integrations.

    `MODIFY_EXTERNAL_OAUTH_INTEGRATION`
    :   Requires approval for creating, modifying, or dropping External OAuth security
        integrations.

    `MODIFY_SCIM_INTEGRATION`
    :   Requires approval for creating, modifying, or dropping SCIM security integrations.

`approvers:`
:   Specifies the users authorized to approve requests under this rule.

    `users: ( 'username' [ , 'username' , ... ] )`
    :   A list of Snowflake usernames (quoted strings) who can approve requests for this rule.

#### Optional rule parameters

`description: 'description'`
:   A human-readable description of the rule’s purpose.

`required_approvals: integer`
:   The number of approvals required before the protected operation is authorized. Must be
    less than or equal to the number of users in the `approvers.users` list.

    Default: `2`

`request_duration_days: integer`
:   The number of days an approval request remains open before it expires. If the required
    approvals are not received within this period, the request expires and a new request must
    be created.

    Default: `3`

`self_approval_allowed: { true | false }`
:   Specifies whether the user who initiated the protected operation can also approve their
    own request if they are present in the approvers list.

    Default: `true`

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Multi-party Approval policy |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- Altering a policy replaces the entire body. All existing rules are discarded and
  replaced with the rules defined in the new `AS $$ ... $$` body.
- A rule’s `operations` list can’t be empty; each rule must govern at least one operation.
- Each operation can appear in at most one rule within a policy. Assigning the same
  operation to multiple rules in the same policy causes an error.
- If you need to see the current definition of a policy before altering it, run the
  [DESCRIBE MULTI PARTY APPROVAL POLICY](/sql-reference/sql/desc-multi-party-approval-policy) command.

## Examples

Replace all rules in an existing policy:

Copy code

```
ALTER MULTI PARTY APPROVAL POLICY security_db.policies.mpa_policy
AS $$
rules:
  - name: self_protection_rule
    description: "Self Protection MPA Rule"
    operations: [MODIFY_MULTI_PARTY_APPROVAL]
    approvers:
      users: ['ADMIN1', 'ADMIN2']

  - name: tss_rule
    description: "TSS Rule"
    operations: [MODIFY_TRI_SECRET_SECURE, MODIFY_NETWORK_POLICY]
    approvers:
      users: ['ADMIN1', 'ADMIN2', 'ADMIN3']
    required_approvals: 2
    request_duration_days: 2
    self_approval_allowed: false
$$;
```

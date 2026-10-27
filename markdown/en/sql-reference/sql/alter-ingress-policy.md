# ALTER INGRESS POLICY

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Modifies the body or comment of an existing [ingress policy](/user-guide/ingress-policies).

This command changes the policy object. To attach or detach the policy, use
[ALTER ACCOUNT SET INGRESS POLICY](/sql-reference/sql/alter-account-set-ingress-policy) or
[ALTER USER SET INGRESS POLICY](/sql-reference/sql/alter-user-set-ingress-policy).

See also:
:   [CREATE INGRESS POLICY](/sql-reference/sql/create-ingress-policy),
    [DESCRIBE INGRESS POLICY](/sql-reference/sql/desc-ingress-policy),
    [DROP INGRESS POLICY](/sql-reference/sql/drop-ingress-policy),
    [SHOW INGRESS POLICIES](/sql-reference/sql/show-ingress-policies)

## Syntax

Copy code

```
ALTER INGRESS POLICY [ IF EXISTS ] <name> SET COMMENT = '<string_literal>'

ALTER INGRESS POLICY [ IF EXISTS ] <name> AS $$
  <yaml_body>
$$

ALTER INGRESS POLICY [ IF EXISTS ] <name> SET COMMENT = '<string_literal>' AS $$
  <yaml_body>
$$

ALTER INGRESS POLICY [ IF EXISTS ] <name> UNSET COMMENT
```

## Parameters

`name`
:   Identifier for the ingress policy to alter.

    If the identifier contains spaces or special characters, the entire string must be enclosed in double quotes.
    Identifiers enclosed in double quotes are also case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`SET COMMENT = 'string_literal'`
:   Sets or replaces the comment on the ingress policy.

`AS $$ yaml_body $$`
:   Replaces the YAML body. Snowflake compiles the new body when you run the statement. References in
    the body must resolve at that time.

    You cannot unset the body. To stop enforcing a policy, detach it from the account or user.

`UNSET COMMENT`
:   Removes the comment from the ingress policy.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| OWNERSHIP | Ingress policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege). |

Expand

Show lessSee more

`APPLY` on the policy, and `APPLY INGRESS POLICY` on an account or user, let a role attach that
policy. Those privileges do not allow `ALTER INGRESS POLICY`.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- You cannot rename an ingress policy. Create a new policy and update the attachments.
- As a protective guardrail against misconfiguration and accidental lockouts, Snowflake evaluates
  the updated body against the current request before saving it when the policy currently governs
  the user who runs this command. Snowflake declines the statement when the updated policy would
  block that request.
- The check uses the current request only. It does not verify other users, clients, or
  authentication methods.
- Replacing the body of an attached policy affects the next authenticated request that the policy
  governs, including requests from sessions that are already open.

## Examples

Replace the policy body:

Copy code

```
ALTER INGRESS POLICY security_db.policies.corp_only AS $$
conditions:
  - name: from_corp
    expression: $CLIENT_IP IN ('<approved_cidr>')
actions:
  - type: allow request
    when_any:
      - name: from_corp
$$;
```

Set a comment:

Copy code

```
ALTER INGRESS POLICY security_db.policies.corp_only
  SET COMMENT = 'Allow requests from the corporate network';
```

# CREATE INGRESS POLICY

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Creates a new [ingress policy](/user-guide/ingress-policies) in the current or specified
schema, or replaces an existing ingress policy.

An ingress policy is a schema-level object. Creating it does not enforce the policy. To activate
enforcement, attach it to the account or to a user with
[ALTER ACCOUNT SET INGRESS POLICY](/sql-reference/sql/alter-account-set-ingress-policy) or
[ALTER USER SET INGRESS POLICY](/sql-reference/sql/alter-user-set-ingress-policy).

See also:
:   [ALTER INGRESS POLICY](/sql-reference/sql/alter-ingress-policy),
    [DROP INGRESS POLICY](/sql-reference/sql/drop-ingress-policy),
    [SHOW INGRESS POLICIES](/sql-reference/sql/show-ingress-policies),
    [DESCRIBE INGRESS POLICY](/sql-reference/sql/desc-ingress-policy)

    [ALTER ACCOUNT SET INGRESS POLICY](/sql-reference/sql/alter-account-set-ingress-policy),
    [ALTER USER SET INGRESS POLICY](/sql-reference/sql/alter-user-set-ingress-policy),
    [CREATE NETWORK POLICY](/sql-reference/sql/create-network-policy)

## Syntax

Copy code

```
CREATE [ OR REPLACE ] INGRESS POLICY [ IF NOT EXISTS ] <name>
  [ COMMENT = '<string_literal>' ]
  AS $$
    <yaml_body>
  $$
```

## Required parameters

`name`
:   Identifier for the ingress policy. The name must be unique in the schema.

    In addition, the identifier must start with an alphabetic character and cannot contain spaces or special characters unless the
    entire identifier string is enclosed in double quotes (for example, `"My object"`). Identifiers enclosed in double quotes are also
    case-sensitive.

    For more information, see [Identifier requirements](/sql-reference/identifiers-syntax).

`AS $$ yaml_body $$`
:   YAML body that defines the policy conditions and actions. The body is stored as
    `POLICY_DEFINITION`.

    Snowflake compiles the body when you create the policy. References in the body, such as a network
    rule or a security integration, must resolve at that time.

    For the body structure, conditions, and actions, see
    [Ingress policies](/user-guide/ingress-policies).

## Optional parameters

`COMMENT = 'string_literal'`
:   Specifies a comment for the ingress policy.

    Default: No value

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| CREATE INGRESS POLICY | Schema |  |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- An ingress policy complements a [network policy](/user-guide/network-policies). Snowflake
  evaluates the two independently. A request is admitted only when every applicable policy allows
  it. An `allow request` decision from an ingress policy does not override a denial from a network
  policy or an authentication policy.
- Creating the policy does not attach it. Use
  `ALTER ACCOUNT SET INGRESS POLICY` for an account-level baseline, or
  `ALTER USER <user> SET INGRESS POLICY` for one user. A user-level policy overrides the
  account-level ingress policy for that user. The two ingress policies are not combined.
- You cannot run `CREATE OR REPLACE` for an ingress policy that is attached to an account or a
  user. Detach it first.
- You cannot rename an ingress policy. Create a new policy and update the attachments.
- You cannot attach a policy that has no body.

Attention

Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).

- The OR REPLACE and IF NOT EXISTS clauses are mutually exclusive. They can’t both be used in the same statement.
- CREATE OR REPLACE *<object>* statements are atomic. That is, when an object is replaced, the old object is deleted and the new object is created in a single transaction.

## Examples

Create an allowlist policy that admits requests from an approved CIDR range. Any request that
does not match is denied because the policy contains an `allow request` action:

Copy code

```
CREATE OR REPLACE INGRESS POLICY corp_only
  COMMENT = 'Allow requests from the corporate network'
  AS $$
conditions:
  - name: from_corp
    expression: $CLIENT_IP IN ('<approved_cidr>')
actions:
  - type: allow request
    when_any:
      - name: from_corp
$$;
```

Attach the policy to the account only after you have tested it on a user. For the full workflow,
see [Ingress policies](/user-guide/ingress-policies).

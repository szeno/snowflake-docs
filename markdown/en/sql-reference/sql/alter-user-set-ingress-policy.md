# ALTER USER SET INGRESS POLICY

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Attaches an [ingress policy](/user-guide/ingress-policies) to a user, or removes that
attachment.

This syntax is the ingress-policy clause of [ALTER USER](/sql-reference/sql/alter-user). The rest of ALTER
USER is unchanged.

See also:
:   [ALTER ACCOUNT SET INGRESS POLICY](/sql-reference/sql/alter-account-set-ingress-policy),
    [CREATE INGRESS POLICY](/sql-reference/sql/create-ingress-policy)

## Syntax

Copy code

```
ALTER USER <name> SET INGRESS POLICY <policy_name> [ FORCE ]

ALTER USER <name> UNSET INGRESS POLICY
```

## Parameters

`name`
:   Identifier for the user. The user name is required.

`policy_name`
:   Identifier for the ingress policy to attach. Use a fully qualified name when the policy is outside
    the current schema.

`FORCE`
:   Replaces an ingress policy that is already set on the user without unsetting it first.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY INGRESS POLICY | User | Required on the user to attach or detach the policy. |
| OWNERSHIP | Ingress policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege).. Either this privilege or `APPLY` is required. |
| APPLY | Ingress policy | Required when the role does not own the policy. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- During authentication, and on each subsequent request in the session, the user-level policy overrides
  the account-level ingress policy for that user. The two ingress policies are not combined.
- The user-level binding does not replace the user’s
  [network policy](/user-guide/network-policies). Snowflake still evaluates the network policy
  that applies to the user. A request is admitted only when both the effective network policy and
  the effective ingress policy allow it. An `allow request` decision from the ingress policy
  does not override a denial from the network policy.
- The binding takes effect for the next authenticated request, including a request from a session
  that is already open.
- As a protective guardrail against misconfiguration and accidental lockouts, Snowflake declines
  the statement when the policy would block the current request of the user who runs it, and that
  user is the user you are altering. The check uses the current request only.
- `UNSET INGRESS POLICY` removes the user-level ingress policy. The user then uses the
  account-level ingress policy, if one is set. This does not change the user’s network policy.
- Attach a policy to a test user before you attach it to the account. See
  [ALTER ACCOUNT SET INGRESS POLICY](/sql-reference/sql/alter-account-set-ingress-policy).

## Examples

Attach an ingress policy to one user:

Copy code

```
ALTER USER etl_runner SET INGRESS POLICY security_db.policies.corp_only;
```

Replace the user-level policy:

Copy code

```
ALTER USER etl_runner SET INGRESS POLICY security_db.policies.geo_fence FORCE;
```

Remove the user-level ingress policy so the account-level policy applies again:

Copy code

```
ALTER USER etl_runner UNSET INGRESS POLICY;
```

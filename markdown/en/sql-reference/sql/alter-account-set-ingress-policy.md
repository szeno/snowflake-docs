# ALTER ACCOUNT SET INGRESS POLICY

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Attaches an [ingress policy](/user-guide/ingress-policies) to the current account, or
removes that attachment.

The account-level policy is the baseline for incoming connections from users who do not have their
own ingress policy. This syntax is the ingress-policy clause of
[ALTER ACCOUNT](/sql-reference/sql/alter-account). The rest of ALTER ACCOUNT is unchanged.

See also:
:   [ALTER USER SET INGRESS POLICY](/sql-reference/sql/alter-user-set-ingress-policy),
    [CREATE INGRESS POLICY](/sql-reference/sql/create-ingress-policy)

## Syntax

Copy code

```
ALTER ACCOUNT SET INGRESS POLICY <policy_name> [ FORCE ]

ALTER ACCOUNT UNSET INGRESS POLICY
```

## Parameters

`policy_name`
:   Identifier for the ingress policy to attach. Use a fully qualified name when the policy is outside
    the current schema.

`FORCE`
:   Replaces an ingress policy that is already set on the account without unsetting it first.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| APPLY INGRESS POLICY | Account | Required on the account to attach or detach the policy. |
| OWNERSHIP | Ingress policy | OWNERSHIP is a special privilege on an object that is automatically granted to the role that created the object, but can also be transferred using the [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership) command to a different role by the owning role (or any role with the MANAGE GRANTS privilege).. Either this privilege or `APPLY` is required. |
| APPLY | Ingress policy | Required when the role does not own the policy. |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- An ingress policy does not replace the account [network policy](/user-guide/network-policies).
  Snowflake evaluates the network policy and the ingress policy independently. A request is
  admitted only when both allow it. An `allow request` decision from the ingress policy does not
  override a denial from the network policy.
- At login, Snowflake evaluates the network policy before the ingress policy, and evaluates the
  ingress policy before the session is created. On each subsequent authenticated request, Snowflake
  evaluates the network policy and the ingress policy again.
- A user-level ingress policy overrides this account-level policy for that user. The two ingress
  policies are not combined. Set a user-level policy with
  [ALTER USER SET INGRESS POLICY](/sql-reference/sql/alter-user-set-ingress-policy).
- As a protective guardrail against misconfiguration and accidental lockouts, Snowflake declines
  the statement when the policy would block the current request of the user who runs it, unless
  that user already has a user-level ingress policy. The check uses the current request only.
- Test the policy on a user before you attach it to the account.
- `UNSET INGRESS POLICY` removes the account-level ingress policy. It does not change the account
  network policy.

## Examples

Attach an account-level ingress policy:

Copy code

```
ALTER ACCOUNT SET INGRESS POLICY security_db.policies.corp_only;
```

Replace the account-level policy:

Copy code

```
ALTER ACCOUNT SET INGRESS POLICY security_db.policies.corp_except_cortex_code FORCE;
```

Remove the account-level ingress policy:

Copy code

```
ALTER ACCOUNT UNSET INGRESS POLICY;
```

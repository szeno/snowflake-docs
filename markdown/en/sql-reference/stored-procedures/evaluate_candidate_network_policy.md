# EVALUATE\_CANDIDATE\_NETWORK\_POLICY

Simulates the effect of applying a candidate network policy against historical ingress traffic, without
activating the policy.

Analyzing the output enables administrators to answer the following questions:

- What would this policy have blocked?
- Would legitimate users be affected?

The procedure evaluates all observed ingress client IPs and produces a row-level what-if result.
It doesn’t modify account configuration.

See also:
:   [RECOMMEND\_NETWORK\_POLICY](/sql-reference/stored-procedures/recommend_network_policy)

## Syntax

Copy code

```
SNOWFLAKE.NETWORK_SECURITY.EVALUATE_CANDIDATE_NETWORK_POLICY(
  POLICY_NAME => '<string>'
  [, LOOKBACK_DAYS => <integer> ]
  [, USER_NAME => <string> ])
```

## Arguments

**Required:**

`POLICY_NAME => 'string'`
:   The name of the candidate network policy to evaluate.

**Optional:**

`LOOKBACK_DAYS => 'integer'`
:   The number of days of historical ingress traffic to evaluate against. Controls how far back
    the simulation looks.

    Default: 90

`USER_NAME => 'string'`
:   Filters the evaluation to include only traffic from the specified user.

    Default: No filter; all users are included.

## Returns

Returns a table with (at minimum) the following columns:

| Column name | Data type | Description |
| --- | --- | --- |
| `ACCESS_CLIENT_IP` | VARCHAR | The client IP address observed in historical ingress traffic. This value can be an IPv4 or IPv6 address. |
| `IS_ALLOWED` | VARCHAR | Whether the IP would be allowed (`YES`) or blocked (`NO`) if the candidate policy were activated. |

Expand

Show lessSee more

**Interpretation:**

- `YES` — This IP *would be allowed* if the policy were activated.
- `NO` — This IP *would be blocked* if the policy were activated.

The evaluation results don’t activate the policy. You must activate the recommended network policy if you want to enforce it, by running the
[ALTER ACCOUNT](/sql-reference/sql/alter-account) command. For an example, see step 8 in [Generate and evaluate a candidate network policy](/user-guide/network-policy-advisor#label-gen-and-eval-candidate-network-policy).

## Access control requirements

A user must have the SECURITYADMIN role at a minimum to run this stored procedure.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

### Usage notes

- The procedure is read-only with respect to account configuration. It doesn’t activate or modify
  any network policies.
- This procedure can’t determine which IP addresses are correct or safe for your organization.
  You must validate results with your IT and security teams before activating the policy.
- Execution time might be 1-2 minutes for accounts with large amounts of historical ingress access data.
- Evaluation results might be dense for high-traffic accounts and might require filtering or
  visualization.
- Each row in the output represents a decision point that administrators should review.

### Examples

Evaluate a candidate network policy using the default lookback window:

Copy code

```
USE ROLE SECURITYADMIN;

CALL SNOWFLAKE.NETWORK_SECURITY.EVALUATE_CANDIDATE_NETWORK_POLICY(
  POLICY_NAME => 'MY_INGRESS_POLICY'
  );
```

Evaluate a candidate network policy against the last 90 days of ingress traffic:

Copy code

```
USE ROLE SECURITYADMIN;

CALL SNOWFLAKE.NETWORK_SECURITY.EVALUATE_CANDIDATE_NETWORK_POLICY(
  POLICY_NAME => 'MY_INGRESS_POLICY',
  LOOKBACK_DAYS => 90
  );
```

Evaluate a candidate network policy against the last 90 days of ingress traffic for a user named `user1`:

Copy code

```
USE ROLE SECURITYADMIN;

CALL SNOWFLAKE.NETWORK_SECURITY.EVALUATE_CANDIDATE_NETWORK_POLICY(
  POLICY_NAME => 'MY_INGRESS_POLICY',
  LOOKBACK_DAYS => 90,
  USER_NAME => 'user1'
  );
```

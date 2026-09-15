# RECOMMEND\_NETWORK\_POLICY

Generates a recommended allow-list for an ingress network policy based on successful access within a
specified lookback window.

This stored procedure is intended as a starting point if you don’t currently have a network policy or want to redesign an existing one.

The procedure analyzes successful ingress requests, optimizes individual IPs into CIDR blocks, and returns
human-readable SQL that administrators can review, refine, and execute.

See also:
:   [EVALUATE\_CANDIDATE\_NETWORK\_POLICY](/sql-reference/stored-procedures/evaluate_candidate_network_policy)

## Syntax

Copy code

```
SNOWFLAKE.NETWORK_SECURITY.RECOMMEND_NETWORK_POLICY(
  LOOKBACK_DAYS => <integer>
  [, USER_NAME => '<string>' ]
  )
```

## Arguments

**Required:**

`LOOKBACK_DAYS => 'integer'`
:   The number of days of successful ingress access to analyze.

**Optional:**

`USER_NAME => 'string'`
:   Filters the recommendation to include only traffic from the specified user.

    Default: None (includes all users in an account).

## Returns

Returns human-readable text that contains example SQL statements. The output includes the following information:

- A summary of the number of distinct IP addresses analyzed and the number of CIDR blocks produced.
- An example CREATE OR REPLACE NETWORK RULE statement for an ingress network rule.
- An example CREATE OR REPLACE NETWORK POLICY statement for a network policy that references the rule.

## Access control requirements

A user must have the SECURITYADMIN role at a minimum to run this stored procedure.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

### Usage notes

- The procedure is read-only with respect to account configuration. It does not create or modify
  any network rules or policies.
- Recommendations are based only on historical **successful** ingress. Blocked or failed access is
  not recommended for allow-listing.
- This procedure can’t determine which IP addresses are correct or safe for your organization.
  You must validate results with your IT and security teams before executing the generated SQL.
- SQL is provided as text to support copy-paste workflows.
- Output might vary depending on traffic volume and lookback window.
- The USER\_NAME filter is optional. When omitted, the recommendation covers all users in an account.
- The procedure enforces a hard limit of **1,000 CIDR blocks**. If the recommendation exceeds
  this limit, the procedure returns an error. To stay within the limit, try a shorter lookback window
  or filter by user.
- The generated recommendation uses `TYPE = IPV4` network rules. If your account receives
  IPv6 ingress traffic, you may need to create additional network rules with `TYPE = IPV6`
  to cover IPv6 addresses. For more information, see [Network rules](/user-guide/network-rules).

### Examples

Generate a recommended network policy based on the last 1 day of traffic for a specific user:

Copy code

```
USE ROLE SECURITYADMIN;

CALL SNOWFLAKE.NETWORK_SECURITY.RECOMMEND_NETWORK_POLICY(
  LOOKBACK_DAYS => 1,
  USER_NAME => 'user1'
  );
```

Generate a recommended network policy based on the last 30 days of traffic for all users:

Copy code

```
USE ROLE SECURITYADMIN;

CALL SNOWFLAKE.NETWORK_SECURITY.RECOMMEND_NETWORK_POLICY(
  LOOKBACK_DAYS => 30
  );
```

```
Recommended candidate network policy based on 1,000 distinct IP addresses,
optimized to 99 CIDR blocks from the last 30 days.

You can execute the following statements with appropriate privileges:

-- Create a network rule

CREATE OR REPLACE NETWORK RULE my_ingress_rule
  MODE = INGRESS
  TYPE = IPV4
  VALUE_LIST = ('203.0.113.0/24', ...);

-- Create a network policy

CREATE OR REPLACE NETWORK POLICY my_ingress_policy
  ALLOWED_NETWORK_RULE_LIST = ('my_ingress_rule');
```

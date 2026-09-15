# Network policy advisor

## Overview

Snowflake network policies are a powerful security control, but can be difficult to design correctly, especially when no current policy
exists or when traffic patterns are complex.

The Network Policy Advisor is a [step-wise procedure](#label-gen-and-eval-candidate-network-policy) that guides a *security*
*administrator*, that is a user with the SECURITYADMIN role, to create a recommended candidate for an ingress network policy that is based on
historical ingress-access data. You, as the administrator, then evaluate the recommended policy using a what-if simulation before activating
the policy. You can recommend and evaluate a candidate network policy for a user or for all users in an account. The advisor procedure
involves calling two non-disruptive system stored procedures. These procedures generate human-readable SQL and evaluation results that you
can review, refine, and then apply manually.

## Considerations

The Snowflake Network Policy Advisor doesn’t automatically activate or modify existing network policies. It makes no determination about
whether an IP address is correct or safe for your network environment. The advisor provides recommendations and simulations only. Any final
network policy decisions — that is, any changes to existing network rules and policies — remain the responsibility of the customer.

## Key benefits

The Network Policy Advisor provides the following key benefits:

- Enables you to safely design a first network policy.
- Provides visibility into what traffic would be blocked before enforcement.
- Reduces trial-and-error when tightening security controls.
- Supports iterative refinement and validation workflows.

## Access control requirements

A user must have the SECURITYADMIN role at a minimum to run these stored procedures.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Generate and evaluate a candidate network policy

To generate and evaluate a candidate network policy for an account, log in to Snowsight, open a worksheet, and follow these steps:

1. Generate the SQL syntax for a candidate policy by calling the RECOMMEND\_NETWORK\_POLICY procedure.

   Copy code

   ```
   USE ROLE SECURITYADMIN;

   CALL SNOWFLAKE.NETWORK_SECURITY.RECOMMEND_NETWORK_POLICY(
     LOOKBACK_DAYS => 30,
     );
   ```
2. Review the SQL syntax generated in the previous step.
3. Based on your review, create a candidate network rule and policy by running commands similar to the following
   examples.

   Copy code

   ```
   USE ROLE SECURITYADMIN;

   -- Create a network rule
   CREATE OR REPLACE NETWORK RULE my_ingress_rule
     MODE = INGRESS
     TYPE = IPV4
     VALUE_LIST = ('203.0.113.0/24', ...);

   -- Create a network policy
   CREATE OR REPLACE NETWORK POLICY my_ingress_policy
     ALLOWED_NETWORK_RULE_LIST = ('my_ingress_rule');
   ```

   Note

   If your account receives IPv6 ingress traffic, create an additional network rule with `TYPE = IPV6` and
   add it to the network policy. To enable IPv6 ingress for your account, see
   [IPv6 addresses](/user-guide/network-rules#label-network-rule-ipv6-addresses).
4. Run the EVALUATE\_CANDIDATE\_NETWORK\_POLICY procedure on the candidate policy to simulate which IP addresses
   it would allow or block.

   Copy code

   ```
   USE ROLE SECURITYADMIN;

   CALL SNOWFLAKE.NETWORK_SECURITY.EVALUATE_CANDIDATE_NETWORK_POLICY(
     POLICY_NAME => 'my_ingress_policy'
     );
   ```
5. Analyze the output to confirm which IP addresses would be allowed or blocked by the recommended candidate policy.
6. Refine the candidate policy based on the evaluation results.

   For example, you could add rules to allow legitimate IPs that were blocked and remove rules for unauthorized IPs that were allowed.
7. If necessary, re-evaluate the candidate policy by re-running the EVALUATE\_CANDIDATE\_NETWORK\_POLICY procedure and refining the
   candidate network policy until it returns an acceptable result.
8. (Optional) After you determine that the candidate policy performs successfully, activate it:

   Copy code

   ```
   ALTER ACCOUNT SET NETWORK_POLICY = 'my_ingress_policy';
   ```
9. (Optional) Run a query like this to view the history of ingress traffic in your network:

   Copy code

   ```
   USE ROLE ACCOUNTADMIN;

   SELECT *
     FROM SNOWFLAKE.ACCOUNT_USAGE.INGRESS_NETWORK_ACCESS_HISTORY
     LIMIT 100;
   ```

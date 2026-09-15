# Multi-party Approval

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Multi-party Approval (MPA) introduces a mandatory second-person verification step for
critical Snowflake operations. With MPA enabled, no single administrator can execute a
protected action on their own; at least one additional authorized person must review and
approve the proposed change before it is executed.

Snowflake emphasizes MPA as a critical defense against ransomware and catastrophic data
loss. In a ransomware scenario, a compromised administrator account could be used to
unilaterally disable multi-factor authentication (MFA) or rotate/deactivate
customer-managed encryption keys (Tri-Secret Secure), instantly rendering all data
undecryptable, inaccessible, or vulnerable to unauthorized access. By enforcing a
“four-eyes” principle, MPA acts as a hard stop against an attacker attempting to lock
out an organization or destroy its data, as they would need to compromise multiple
distinct administrative accounts to bypass the quorum.

## Benefits

- **Increased security and ransomware defense:** MPA distributes decision-making for
  critical operations to eliminate single points of failure, protecting against
  compromised accounts or insider threats.
- **Error prevention:** A second approver helps catch misconfigurations, such as overly
  broad role grants or unsafe network changes, before they cause downtime or lockouts.
- **Accountability and auditability:** MPA activity is captured in system logs. Snowflake
  also provides dedicated Account Usage views, [MULTI\_PARTY\_APPROVAL\_REQUESTS view](/sql-reference/account-usage/multi_party_approval_requests)
  and [MULTI\_PARTY\_APPROVAL\_POLICIES view](/sql-reference/account-usage/multi_party_approval_policies), so you
  can query who requested which actions, who approved or rejected them, and when.
- **Compliance:** Many regulatory frameworks require dual-control or four-eyes processes
  for sensitive changes. MPA provides an explicit mechanism to enforce those processes
  for Snowflake operations.

## Protected operations

Protected operations define which sensitive actions require Multi-party Approval before
they can be executed. In Snowsight, the operations are organized into the following
groups.

### Admin operations

**Updating Multi-party Approval configuration and settings** (`MODIFY_MULTI_PARTY_APPROVAL`)

Requires approval for changes to Multi-party Approval policies, rules, account settings,
and approver assignments. This operation also covers creating, modifying, or dropping
SAML2 security integrations, which control single sign-on and therefore who can
authenticate as an approver.

Important

Every policy must include at least one rule with this operation. This self-protecting
rule prevents a compromised administrator from unilaterally disabling or modifying
MPA itself.

**Disabling multi-factor authentication and user security settings** (`DISABLE_MULTI_FACTOR_AUTHENTICATION`)

Requires approval for disabling multi-factor authentication or resetting user passwords.

**Managing Tri-Secret Secure keys** (`MODIFY_TRI_SECRET_SECURE`)

Requires approval for activating or deactivating Tri-Secret Secure customer-managed
encryption keys.

Note

After a policy with this operation has been attached to an account for 72 hours, the
speed bump for Tri-Secret Secure operations is no longer required.

**Granting or revoking administrative roles** (`MODIFY_PRIVILEGED_ROLE_GRANTS`)

Requires approval for granting or revoking the `ACCOUNTADMIN` or `SECURITYADMIN`
role, and for granting or revoking the `MANAGE GRANTS` privilege.

**Managing Cortex AI guardrails** (`MODIFY_CORTEX_GUARDRAILS`)

Requires approval for modifying Cortex AI guardrail settings on the account.

**Modifying data retention (Time Travel) settings** (`MODIFY_DATA_RETENTION_TIME`)

Requires approval for modifying the `DATA_RETENTION_TIME_IN_DAYS` parameter on accounts,
databases, schemas, or tables.

### Policy operations

**Modifying network security policies** (`MODIFY_NETWORK_POLICY`)

Requires approval for changes to active network policies, network rules, and policy
assignments on accounts and users.

**Modifying session policies** (`MODIFY_SESSION_POLICY`)

Requires approval for modifying session policy settings or assignments on accounts and
users.

**Modifying authentication policies** (`MODIFY_AUTHENTICATION_POLICY`)

Requires approval for modifying authentication policy settings or assignments on accounts
and users.

**Modifying password policies** (`MODIFY_PASSWORD_POLICY`)

Requires approval for modifying password policy settings or assignments on accounts and
users.

### Security integration operations

**Modifying OAuth security integrations** (`MODIFY_OAUTH_INTEGRATION`)

Requires approval for creating, modifying, or dropping Snowflake OAuth security
integrations.

**Modifying External OAuth security integrations** (`MODIFY_EXTERNAL_OAUTH_INTEGRATION`)

Requires approval for creating, modifying, or dropping External OAuth security
integrations.

**Modifying SCIM security integrations** (`MODIFY_SCIM_INTEGRATION`)

Requires approval for creating, modifying, or dropping SCIM security integrations.

## Key personas

### Requester

The user who attempts to execute a protected SQL statement or a corresponding
Snowsight action. When the engine intercepts the operation, it returns an
`MPA_APPROVAL_REQUIRED` error containing a unique `request_id`. The Requester then
submits a business justification using the
[SYSTEM$UPDATE\_MULTI\_PARTY\_APPROVAL\_JUSTIFICATION](/sql-reference/functions/system_update_multi_party_approval_justification)
system function, or fills out the justification pop-up in Snowsight if the action was
triggered through the UI.

Once the required approvals are received, the Requester must replay the exact
original SQL statement to execute it. The replay window is 3 days after the
request is approved. Each approved request can be re-executed only once: after a
successful replay, the request moves to the `Executed` state, and running the
operation again requires a new request and new approvals. The Requester can also
self-cancel any of their own pending requests at any time.

Because this flow requires a user to submit a justification and replay the
statement after approval, protected operations fail if they are executed from
tasks or stored procedures. For the same reason, SCIM actions that attempt a
protected operation fail.

### Approver

A user explicitly listed in the policy rule’s `approvers.users` list who reviews
and authorizes changes. Approvers can be local Snowflake users or SCIM-managed users,
and they must have MFA enrolled and a validated email address. Service users can’t be
approvers.

Note

To protect the integrity of the approver quorum, Snowflake restricts changes to a user
while they’re an approver in an active policy:

- Through SCIM, changing an approver’s login name or deprovisioning (dropping) an approver
  is blocked.
- Through SQL, dropping an approver is blocked.
- Other sensitive changes to an approver through SQL, such as changing the login name,
  resetting the password, disabling MFA, or changing the email address, require
  Multi-party Approval and generate an approval request before they take effect.

These protections prevent an attacker from hijacking or removing an approver to bypass the
required quorum.

When a request requires attention, Approvers receive email notifications
with a link to the Snowsight Requests & Approvals page. An Approver casts either an
Approve or Reject vote. A single Reject vote immediately terminates the request.
Approvers must use an active Snowsight session to cast their votes.

## Policy structure

An MPA policy contains one or more rules. Each rule defines which operations require
approval and who can approve them.

A policy supports an optional description. Each rule contains the following:

- **Name** (required): A unique identifier for the rule within the policy.
- **Operations** (required): The protected operations this rule governs. See [Protected operations](#protected-operations).
- **Approvers** (required): The list of Snowflake users authorized to approve requests
  under this rule.
- **Minimum approvals** (optional): The number of approvals required before the
  operation is authorized. Minimum: `1`. Maximum: `20`. Default: `2`.
- **Request duration** (optional): The number of days an approval request remains open
  before it expires. Minimum: `1`. Maximum: `14`. Default: `3`.
- **Self-approval** (optional): Whether the Requester’s own approval counts toward the
  quorum if they are listed as an approver. Default: `true`.

Each operation can only appear in one rule per policy. Assigning the same operation to
multiple rules causes an error.

## Configure MPA

You must use the ACCOUNTADMIN role to configure and manage MPA policies.

### Configure your first policy

1. Sign in to Snowsight.
2. Select **Governance & Security**.
3. Select **Requests & approvals**.
4. Select **Multi-party configuration**.
5. Select **Configure policy**.
6. Fill in the policy name, description, and location.
7. On the default rule, select the pencil icon to edit it, or select **Create rule** to
   add a new rule. For each rule, set the rule name, description, operations, minimum
   approvals required, and approvers.

To configure your first policy using SQL instead, see
[CREATE MULTI PARTY APPROVAL POLICY](/sql-reference/sql/create-multi-party-approval-policy).
To activate it, see [ALTER ACCOUNT](/sql-reference/sql/alter-account).

### Add a policy

1. Sign in to Snowsight.
2. Select **Governance & Security**.
3. Select **Requests & approvals**.
4. Select **Multi-party configuration**.
5. Select **Add policy**.
6. Fill in the policy name, description, and location.
7. On the default rule, select the pencil icon to edit it, or select **Create rule** to
   add a new rule. For each rule, set the rule name, description, operations, minimum
   approvals required, and approvers.

To add a policy using SQL instead, see
[CREATE MULTI PARTY APPROVAL POLICY](/sql-reference/sql/create-multi-party-approval-policy).

### Edit a policy

1. Sign in to Snowsight.
2. Select **Governance & Security**.
3. Select **Requests & approvals**.
4. Select **Multi-party configuration**.
5. Select **…** next to the policy you want to edit.
6. Update the policy name, description, or location, or select the pencil icon on a rule
   to edit it. For each rule, you can update the rule name, description, operations,
   minimum approvals required, and approvers.

To edit a policy using SQL instead, see
[ALTER MULTI PARTY APPROVAL POLICY](/sql-reference/sql/alter-multi-party-approval-policy).

When you alter a policy, Snowflake automatically reconciles any pending requests against
the updated rule configuration.

### Activate a policy

1. Sign in to Snowsight.
2. Select **Governance & Security**.
3. Select **Requests & approvals**.
4. Select **Multi-party configuration**.
5. Select **…** next to the policy you want to activate.
6. Select **Activate**.

To activate a policy using SQL instead, see
[ALTER ACCOUNT](/sql-reference/sql/alter-account).

## Managing requests

### Approve or reject a request

1. Sign in to Snowsight.
2. Select **Governance & Security**.
3. Select **Requests & approvals**.
4. Select **Pending**.
5. Select **Sent to me**.
6. Optionally, filter by **Operation**, **Type**, **Status**, **Requested by**, or **Time**, or use the search bar.
7. Select the request you want to review.
8. Select **Approve** or **Reject**.

### View requests created by me

1. Sign in to Snowsight.
2. Select **Governance & Security**.
3. Select **Requests & approvals**.
4. Select **Pending**.
5. Select **Created by me**.
6. Optionally, filter by **Operation**, **Type**, **Status**, **Requested by**, or **Time**, or use the search bar.
7. Select the request you want to view.

### View request history

1. Sign in to Snowsight.
2. Select **Governance & Security**.
3. Select **Requests & approvals**.
4. Select **History**.
5. Select **Sent to me** or **Created by me**.
6. Optionally, filter by **Operation**, **Type**, **Status**, **Requested by**, or **Time**, or use the search bar.
7. Select the request you want to view.

## MPA workflow

1. **Intercept:** The Requester attempts a protected SQL operation or a corresponding
   Snowsight action. The engine intercepts it, blocks execution, and returns an
   `MPA_APPROVAL_REQUIRED` error with a unique `request_id`.
2. **Justification:** The Requester submits a business justification. If the protected
   action was triggered through Snowsight, you’re prompted to provide a justification
   immediately. If triggered through SQL, submit the justification using the
   [SYSTEM$UPDATE\_MULTI\_PARTY\_APPROVAL\_JUSTIFICATION](/sql-reference/functions/system_update_multi_party_approval_justification)
   system function.

   This transitions the request to `PENDING` and notifies the designated Approvers.
3. **Review:** Approvers evaluate the request independently in Snowsight. Once the
   required quorum of Approve votes is reached, the request status changes to
   `APPROVED`.
4. **Replay:** The system does not auto-execute the operation. The Requester is
   notified and must replay the exact same SQL statement. The engine matches the
   statement to the approved request and executes the change. The replay window is
   3 days after approval. After a successful replay, the request moves to the `Executed`
   state.

   To replay an approved request from Snowsight, select **Governance & Security**, then
   **Requests & approvals**, then **History**, and then **Created by me**. Select the
   approved request, and then select **Rerun action in Workspaces**. Snowsight opens a new
   workspace pre-populated with the SQL from the approved request, which you can run to
   execute the change.

## Request states

A Multi-party Approval request moves through the following states. You can view and filter
requests by state on the Snowsight Requests & Approvals page, and query the state of each
request in the [MULTI\_PARTY\_APPROVAL\_REQUESTS view](/sql-reference/account-usage/multi_party_approval_requests) view.

| State | Description |
| --- | --- |
| Pending | The request has been created and submitted with a justification, and is awaiting Approver votes. |
| Approved | The request received the required number of approvals. The Requester can now replay the original statement to run the operation. |
| Executed | The Requester replayed the approved statement and the protected operation ran successfully. This is the terminal success state. |
| Rejected | An Approver rejected the request. A single rejection immediately terminates the request. |
| Cancelled | The Requester withdrew the request before it was approved. |
| Expired | The request expired: either it didn’t receive the required number of approvals within its request duration window, or it was approved but the Requester didn’t replay the statement within the 3-day replay window. |

Expand

Show lessSee more

## Example: Activating Tri-Secret Secure

This example shows the end-to-end MPA workflow when a Requester attempts to activate
Tri-Secret Secure customer-managed encryption keys.

**Step 1 — Trigger the block (Requester)**

The Requester attempts to activate the CMK. The engine intercepts the call and returns
an `MPA_APPROVAL_REQUIRED` error containing a unique `request_id`:

Copy code

```
SELECT SYSTEM$ACTIVATE_CMK_INFO();
```

The engine returns an error similar to the following:

Copy code

```
Blocked by Multi-party Approval. A request has been created. To proceed, add a
justification: "select SYSTEM$UPDATE_MULTI_PARTY_APPROVAL_JUSTIFICATION(
'a1b2c3d4-e5f6-7890-abcd-ef1234567890', '<reason>');". To cancel: "select
SYSTEM$CAST_MULTI_PARTY_APPROVAL_VOTE('a1b2c3d4-e5f6-7890-abcd-ef1234567890',
'REJECT');". Expires: 2026-01-15 at 4:00:01 PM UTC.
Request-ID: 'a1b2c3d4-e5f6-7890-abcd-ef1234567890'
```

**Step 2 — Submit justification (Requester)**

The Requester submits a business justification using the `request_id` from the error:

Copy code

```
SELECT SYSTEM$UPDATE_MULTI_PARTY_APPROVAL_JUSTIFICATION(
  '<request_id>',
  'Activating CMK as part of scheduled key rotation for compliance.'
);
```

This transitions the request to `PENDING` and notifies the designated Approvers.

**Step 3 — Review and approve (Approver)**

The Approver receives an email notification. They navigate to the Snowsight
Requests & Approvals page, review the request and justification, and cast an Approve
vote. Once the required quorum is reached, the request status changes to `APPROVED`.

**Step 4 — Replay the statement (Requester)**

The Requester is notified that the request is approved and replays the original
statement. The engine matches it to the approved request and executes the change:

Copy code

```
SELECT SYSTEM$ACTIVATE_CMK_INFO();
```

## Multi-party Approval privileges

Snowflake supports the following Multi-party Approval privileges to determine whether
users can create, set, and own Multi-party Approval policies.

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

| Privilege | Usage |
| --- | --- |
| CREATE MULTI PARTY APPROVAL POLICY | Enables creating a new Multi-party Approval policy in a schema. |
| APPLY MULTI PARTY APPROVAL POLICY | Enables applying a Multi-party Approval policy at the account level. Also enables viewing all Multi-party Approval policies in the account. |
| OWNERSHIP | Grants full control over the policy. Required to alter or drop a Multi-party Approval policy. |

Expand

Show lessSee more

### Summary of commands, operations, and privileges

The following table summarizes the relationship between Multi-party Approval DDL
operations and their necessary privileges.

| Operation | Privilege required |
| --- | --- |
| Create policy | A role with the CREATE MULTI PARTY APPROVAL POLICY privilege on the schema. |
| Alter policy | A role with the OWNERSHIP privilege on the policy. |
| Drop policy | A role with the OWNERSHIP privilege on the policy. |
| Describe policy | A role with the OWNERSHIP privilege on the policy, or the APPLY MULTI PARTY APPROVAL POLICY privilege on the account. |
| Show policies | A role with the OWNERSHIP privilege on the policy, or the APPLY MULTI PARTY APPROVAL POLICY privilege on the account. |
| Set & unset policy on account | A role with the APPLY MULTI PARTY APPROVAL POLICY privilege on the account and the OWNERSHIP privilege on the policy, or a role with the APPLY MULTI PARTY APPROVAL POLICY privilege on the account and the APPLY privilege on a specific policy. |

Expand

Show lessSee more

## Best practices

- Ensure the **Updating Multi-party Approval configuration and settings** rule has
  approval requirements at least as strong as your other rules.
- Require a minimum of two approvals for all rules to prevent unilateral actions.
- Set the approval window (`request_duration_days`) to between 1 and 3 days.
- Ensure your account has more than one designated ACCOUNTADMIN to avoid deadlocks.
- Verify that all Approvers have MFA enabled and a validated email address.
- Review your list of designated Approvers on a quarterly cadence.

## Breakglass

In emergencies where the standard approval workflow can’t be completed — for example,
if all Approvers are unavailable, a misconfigured policy has locked out legitimate
administrators, or a critical security incident requires immediate action that can’t
wait for standard review — Snowflake Support can intervene. Breakglass actions require
a formal support ticket. Contact Snowflake Support to initiate a breakglass request.

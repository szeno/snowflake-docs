Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$CAST\_MULTI\_PARTY\_APPROVAL\_VOTE

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Casts a vote on a pending Multi-party Approval request. An approver calls this function
with a decision of `APPROVE` or `REJECT` to vote on a request. A requester can call it
with `REJECT` to cancel their own pending request before it is approved or expires.

## Syntax

Copy code

```
SYSTEM$CAST_MULTI_PARTY_APPROVAL_VOTE( '<request_id>', '<decision>' [ , '<comment>' ] )
```

## Arguments

`'request_id'`
:   The unique identifier for the approval request to vote on. This value is returned in the
    `MPA_APPROVAL_REQUIRED` error when a protected operation is intercepted by the
    Multi-party Approval engine.

`'decision'`
:   The vote to cast. One of the following values:

    `APPROVE`
    :   Records an approval vote for the request. When the number of approval votes reaches the
        rule’s required number of approvals, the request status changes to `APPROVED` and the
        requester can replay the original statement.

    `REJECT`
    :   Records a rejection. A single `REJECT` vote from an approver immediately terminates the
        request. A requester can use `REJECT` to cancel a request that they created.

`'comment'`
:   A comment explaining the vote. This argument is required, except when a requester uses
    `REJECT` to cancel their own request, in which case it’s optional.

## Returns

A confirmation string indicating the vote was recorded successfully.

## Access control requirements

No additional privileges are required to call this function. To cast an `APPROVE` vote or
an approver `REJECT` vote, you must be listed as an approver for the request’s rule. To
cancel a request, you must be the user who created it.

## Usage notes

- Approvers can also review and vote on requests from the Snowsight Requests & Approvals
  page. Casting a vote through the UI is equivalent to calling this function.
- A single `REJECT` vote terminates a request immediately, regardless of how many
  approvals it has already received.
- You can only cancel requests that you created. Attempting to cancel a request created
  by another user fails.
- A comment is required for every vote, except when a requester uses `REJECT` to cancel
  their own request.
- You can vote on or cancel a request at any time while it is in `PENDING` state. To view
  pending requests, go to the Snowsight Requests & Approvals page.

## Examples

Cast an approval vote on a pending request:

Copy code

```
SELECT SYSTEM$CAST_MULTI_PARTY_APPROVAL_VOTE(
  'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
  'APPROVE',
  'Reviewed and approved as part of scheduled key rotation.'
);
```

Reject a pending request:

Copy code

```
SELECT SYSTEM$CAST_MULTI_PARTY_APPROVAL_VOTE(
  'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
  'REJECT',
  'Change is out of scope for the current maintenance window.'
);
```

Cancel a request that you created (no comment required):

Copy code

```
SELECT SYSTEM$CAST_MULTI_PARTY_APPROVAL_VOTE(
  'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
  'REJECT'
);
```

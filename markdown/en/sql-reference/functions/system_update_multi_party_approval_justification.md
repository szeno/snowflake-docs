Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$UPDATE\_MULTI\_PARTY\_APPROVAL\_JUSTIFICATION

[Business Critical Feature](/user-guide/intro-editions)

This feature requires Business Critical (or higher).

To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

Submits or updates the business justification for a Multi-party Approval request.
Call this function after receiving an `MPA_APPROVAL_REQUIRED` error to explain why
the protected operation is needed.

Note

Submitting a justification transitions the request to `PENDING` and sends an email
notification to the designated approvers.

## Syntax

Copy code

```
SYSTEM$UPDATE_MULTI_PARTY_APPROVAL_JUSTIFICATION( '<request_id>', '<justification>' )
```

## Arguments

`'request_id'`
:   The unique identifier for the approval request. This value is returned in the
    `MPA_APPROVAL_REQUIRED` error when a protected operation is intercepted by the
    Multi-party Approval engine.

`'justification'`
:   A plain-text description of the business reason for the requested operation. This
    text is visible to approvers when they review the request in Snowsight.

## Returns

A confirmation string indicating the justification was recorded successfully.

## Access control requirements

No additional privileges are required to call this function.

## Usage notes

- You can call this function again to revise the justification while the request is
  still in `PENDING` state. Once the request is approved, rejected, canceled, or
  expired, the justification can no longer be updated.

## Examples

Submit a justification for a pending approval request:

Copy code

```
SELECT SYSTEM$UPDATE_MULTI_PARTY_APPROVAL_JUSTIFICATION(
  'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
  'Activating CMK as part of scheduled key rotation for compliance.'
);
```

Update the justification after it has already been submitted:

Copy code

```
SELECT SYSTEM$UPDATE_MULTI_PARTY_APPROVAL_JUSTIFICATION(
  'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
  'Updated: Revised justification to include additional business context.'
);
```

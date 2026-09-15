# Aug 4, 2026: Multi-party Approval (*General availability*)

Multi-party Approval (MPA) is now generally available. When a Multi-party Approval policy is attached to your account, MPA enforces a mandatory
second-person (“four-eyes”) verification step for critical account operations.

A Multi-party Approval policy defines which operations require approval and who can
approve them. When an attached policy protects an operation, no single administrator can execute
that operation on their own: at least one additional authorized approver must review and
approve the change before it executes. Protected operations are organized into three
groups:

- **Admin operations**, such as updating Multi-party Approval configuration, disabling
  multi-factor authentication, managing Tri-Secret Secure keys, granting or revoking
  administrative roles, managing Cortex AI guardrails, and modifying data retention
  settings.
- **Policy operations**, such as modifying network, session, authentication, and password
  policies.
- **Security integration operations**, such as modifying OAuth, External OAuth, and SCIM
  security integrations.

For more information, see [Multi-party Approval](/user-guide/multi-party-approval).

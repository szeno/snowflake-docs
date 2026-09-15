# Best practices for shared workspaces

The following recommendations detail how administrators can effectively plan, configure, and maintain shared workspaces.

## Plan and set up shared workspaces

Shared workspaces are created as schema-level objects within a standard database and follow Snowflake’s existing role-based access control (RBAC) model.

To create a shared workspace, users must either own the target schema or have the following privileges:

> - USAGE on the database and schema
> - CREATE WORKSPACE on the schema

### Grant creation privileges

1. As an administrator, to grant the necessary schema-level privileges to a role, run the following command:

   Copy code

   ```
   GRANT USAGE ON DATABASE <database_name> TO ROLE <role_name>;
   GRANT USAGE, CREATE WORKSPACE ON SCHEMA <database_name>.<schema_name> TO ROLE <role_name>;
   ```

## Workspace management commands

Use the following commands to monitor and manage access to existing shared workspaces:

| Action | Syntax |
| --- | --- |
| List all workspaces | `SHOW WORKSPACES IN ACCOUNT;` |
| View workspace permissions | `SHOW GRANTS ON WORKSPACE <workspace_name>;` |
| Grant edit permissions | `GRANT WRITE ON WORKSPACE <workspace_name> TO ROLE <role_name>;` |
| Revoke edit permissions | `REVOKE WRITE ON WORKSPACE <workspace_name> FROM ROLE <role_name>;` |

Expand

Show lessSee more

**Example**

Copy code

```
GRANT WRITE ON WORKSPACE <workspace_name> TO ROLE <role_name>;
REVOKE WRITE ON WORKSPACE <workspace_name> FROM ROLE <role_name>;
```

## Governance best practices

When enabling shared workspaces in your account, consider the following best practices:

- Plan intentionally: Align shared workspaces with specific teams, projects, or use cases. Fewer, well-defined workspaces reduce clutter and user confusion.
- Limit creation privileges: Restrict CREATE WORKSPACE privileges to designated steward roles and schema owners. Broadly granting this privilege can lead to unnecessary
  duplication or workspace sprawl.
- Monitor workspace lifecycle: Periodically review existing shared workspaces and retire stale or unused ones. Establish a lightweight review process
  (for example, quarterly) to ensure that only active and relevant workspaces remain available.

## Organizational models

Administrators can structure shared workspaces in different ways depending on their organization’s collaboration model.

### Centralized collaboration hub

A single database and schema dedicated to shared workspaces for all teams provides a consistent location for cross-team collaboration.

**Example setup**

Copy code

```
CREATE DATABASE IF NOT EXISTS SHARED_WORKSPACES_DB;
CREATE SCHEMA IF NOT EXISTS SHARED_WORKSPACES_SCHEMA;

GRANT USAGE ON DATABASE SHARED_WORKSPACES_DB TO ROLE WORKSPACES_STEWARDS;
GRANT USAGE, CREATE WORKSPACE ON SCHEMA SHARED_WORKSPACES_DB.SHARED_WORKSPACES_SCHEMA TO ROLE WORKSPACES_STEWARDS;
```

**Example structure**

![Centralized shared workspaces structure](/static/images/workspaces/shared-workspaces-centralized.png)

### Team-scoped workspaces

Each team owns its own database or schema and manages shared workspaces within its scope. This model fits organizations that already align
databases and roles by department, discipline, or business unit.

**Example structure**

![Team scoped shared workspaces structure](/static/images/workspaces/shared-workspaces-team-scoped.png)

### Hybrid approach

Use a combined, central schema for cross-team or high-visibility projects with team-specific schemas for daily collaboration. This model balances
flexibility with centralized governance and discoverability.

## Role design and access management considerations

- Shared workspaces can only be shared with **roles** (not individual users).
- Most organizations can use their existing roles to manage access. Avoid creating new roles solely for shared workspaces unless necessary.

### Best practices

- Use existing roles that already represent team membership or function.
- Assign a designated steward role responsible for managing access and maintaining the workplace structure.

## Adoption and maintenance

- **Naming conventions:** To improve discoverability, use clear and consistent patterns such as `TEAM_PROJECT_NAME`.
- **Ownership:** Assign a steward or owner role to each shared workspace to ensure accountability.
- **Documentation:** Maintain an internal directory or wiki listing active shared workspaces and their intended purpose.
- **Consistency:** Encourage users to move from private to shared workspaces when code or queries are ready for collaboration.
- **Review regularly:** Periodically audit roles, schemas, and shared workspaces to ensure that they remain aligned with organizational policies and team structures.

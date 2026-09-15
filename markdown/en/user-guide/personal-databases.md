# Personal Databases

## What is a Personal Database?

A Personal Database (PDB) is a system-owned, user-managed database instance that is automatically provisioned by Snowflake. It serves as a
dedicated, personal storage location where users can create, organize, and manage their own database objects.

Automatic provisioning removes the administrative requirement for users to manually select or request access to a shared database, which
ensures a dedicated development environment. When a user is dropped from the system, their associated PDB and all its objects are
automatically transferred to ACCOUNTADMIN ownership.

### Advantages of a PDB

- **Organize personal projects:** Users can organize their own projects in an isolated environment, reducing clutter and potential naming
  conflicts in shared databases.
- **Governance:** All Personal Database objects are fully governed by RBAC.

## PDB object types

PDBs support the following object types:

- Application services
- Artifact repositories
- Git repositories
- Schemas
- Secrets
- Workspaces

### Workspaces

The PDB is created when a user first interacts with the [Workspaces UI](/user-guide/ui-snowsight/workspaces).
Workspaces are file-based entities and require storage within a Snowflake database.

## Security

The PDB’s architecture is intentionally streamlined and adheres to the principle of least privilege, which ensures that all operations are strictly
limited to the user’s existing security context:

- **No new data access:** PDBs don’t introduce any new or expanded access to data. Users can’t move data from a regular database to a PDB, and PDB objects can’t be shared cross-account using Snowflake data sharing.
- **Permissions context:** Any SQL queries executed within a workspace are run with the exact same set of roles and permissions that the user
  already possesses. This mirrors the execution environment of a standard Snowflake workspace file.

Note

Personal Databases also support personal secrets. [Secret objects](/sql-reference/sql/create-secret) are owned exclusively by the user. This ensures, by default, that the secret
remains private, is accessible only to the user, and is not shared unintentionally.

## Grant privileges to account roles

You can grant non-CREATE privileges on most PDB objects to account roles. This lets you share your workspace files and other personal objects within your account using the same roles you already use elsewhere in Snowflake.

Copy code

```
GRANT READ ON WORKSPACE USER$.PUBLIC.DEFAULT$ TO ROLE some_role;
```

The following restrictions apply when granting privileges on PDB objects to account roles:

- CREATE and OWNERSHIP privileges can’t be granted to account roles on PDB objects.
- Privileges on APPLICATION SERVICE objects in a Personal Database can’t be granted to account roles. To share an Application Service with other roles, deploy it to a standard database instead. For details, see [Deploy to a standard database when sharing with other roles](/developer-guide/snowflake-app-runtime/access-control).

## Use feature policies with Personal Databases

Account administrators can use feature policies to control which object types users are allowed
to create in their Personal Databases. This lets organizations enforce governance rules across
all Personal Databases in the account.

A feature policy can block the creation of any [object type supported in Personal Databases](#label-personal-databases-pdb-object-types).

Note

Account-level object types such as WAREHOUSES, COMPUTE POOLS, and DATABASES have no effect
when a feature policy is bound to Personal Databases. Those types only apply when a feature
policy is bound to native apps.

Important

Feature policies only prevent the creation of new objects. Existing objects are not affected.
To enforce a policy on objects that already exist, remove them
manually before or after applying the policy.

### Applying a feature policy to Personal Databases

To create and apply a feature policy to all Personal Databases in the account, use the
[CREATE FEATURE POLICY](/sql-reference/sql/create-feature-policy) and
[ALTER ACCOUNT](/sql-reference/sql/alter-account) commands:

Copy code

```
CREATE DATABASE feature_policy_db;
CREATE SCHEMA sch;
CREATE FEATURE POLICY feature_policy_db.sch.block_app_services_policy
  BLOCKED_OBJECT_TYPES_FOR_CREATION = (APPLICATION_SERVICE);

ALTER ACCOUNT
  SET FEATURE POLICY feature_policy_db.sch.block_app_services_policy
  FOR ALL PERSONAL DATABASES;
```

After applying this policy, users can no longer create application services in their Personal Databases.

To remove the policy from all Personal Databases:

Copy code

```
ALTER ACCOUNT UNSET FEATURE POLICY FOR ALL PERSONAL DATABASES;
```

Note

You can also apply a feature policy to a specific personal database using
[ALTER DATABASE](/sql-reference/sql/alter-database). A database-level policy takes precedence
over the account-level `FOR ALL PERSONAL DATABASES` policy for that database. For details, see
[Feature policy precedence](/user-guide/feature-policies#label-feature-policy-precedence).

For more information about creating and managing feature policies, see
[Use feature policies to control object creation](/developer-guide/native-apps/ui-consumer-feature-policies).

## PDB management and visibility

Administrators can monitor and control usage of PDBs, which are owned by the system, not by any role. Usage on a PDB is limited
to the user it is assigned to. Users can grant non-CREATE privileges on PDB objects to account roles to share access within the
account, except for APPLICATION SERVICE objects.

### Administrator visibility

Roles with the MANAGE GRANTS privilege have visibility into all objects within the account, including personal objects owned by individual
users. For example, roles like ACCOUNTADMIN can view all databases, including Personal Databases, by default. These roles can also access
details about schemas and their objects within Personal Databases.

- To view details for all Personal Databases within an account, query the [DATABASES Account Usage view](/sql-reference/account-usage/databases):

  Copy code

  ```
  SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.DATABASES
  WHERE DATABASE_NAME LIKE 'USER$%';
  ```
- To view the workspaces that exist in a specific Personal Database, use the following code:

  Copy code

  ```
  SHOW WORKSPACES IN DATABASE "USER$CMEYER";
  ```
- To view a specific user’s Personal Database, use the following code:

  Copy code

  ```
  SHOW DATABASES LIKE 'USER$BOBR';
  ```

  For Personal Databases, the value in the `kind` column is `PERSONAL DATABASE`.
- To view objects in a specific Personal Database, use the following code:

  Copy code

  ```
  SHOW OBJECTS IN DATABASE "USER$<username>";
  ```

### Drop a workspace

- To drop a workspace in a Personal Database, use the following code:

  Copy code

  ```
  DROP WORKSPACE "USER$JSMITH_DROP_WS_TEST".PUBLIC."drop_this_ws";
  ```

## Cost considerations

- Users can’t store data in tables in their PDBs.
- Storage costs reflect only the size of the workspace files and associated metadata.

## Limitations

Administrators can’t perform the following tasks:

- View filenames or file contents that belong to other users.
- View how much storage is used for PDBs. PDBs do not appear in `DATABASE_STORAGE_USAGE_HISTORY`.
- Limit how much storage is used for each PDB.
- Drop PDBs, or prevent individual users from using them.
- Create new PDBs. New PDBs are created on demand when a user creates a workspace.

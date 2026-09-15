# User & security DDL

Snowflake provides a full set of SQL commands for managing users and security. These commands can only be executed by users who are granted roles that have the OWNERSHIP privilege on the managed object. This is usually restricted to the
ACCOUNTADMIN and SECURITYADMIN roles.

However, individual users are able to perform the following tasks for themselves:

- Change their password (only through the web interface).
- View their user information (via [DESCRIBE USER](/sql-reference/sql/desc-user)).
- Change their default role, virtual warehouse, or namespace (via [ALTER USER](/sql-reference/sql/alter-user)).
- Change their session parameters (via [ALTER SESSION](/sql-reference/sql/alter-session)).

## User management

Each user with access to Snowflake is represented by a user object. A user object stores all of the information about the user, including their login name, password, and defaults (role, virtual warehouse, and namespace). Use the following
DDL commands to manage users in the system:

- [CREATE USER](/sql-reference/sql/create-user)
- [ALTER USER](/sql-reference/sql/alter-user)
- [DROP USER](/sql-reference/sql/drop-user)
- [DESCRIBE USER](/sql-reference/sql/desc-user)
- [SHOW USERS](/sql-reference/sql/show-users)

## Role management

Snowflake uses roles to control access to objects in the system:

- Roles are granted access privileges for objects in the system (databases, tables, etc.).
- Roles are granted to users to enable them to create, modify, and use the objects for which the roles have privileges.
- Roles can be granted to other roles to support defining hierarchical access privileges.

Use the following DDL commands to manage roles in the system:

- [CREATE ROLE](/sql-reference/sql/create-role)
- [ALTER ROLE](/sql-reference/sql/alter-role)
- [DROP ROLE](/sql-reference/sql/drop-role)
- [SHOW ROLES](/sql-reference/sql/show-roles)

Use the following DDL commands to manage database roles in the system:

- [CREATE DATABASE ROLE](/sql-reference/sql/create-database-role)
- [ALTER DATABASE ROLE](/sql-reference/sql/alter-database-role)
- [DROP DATABASE ROLE](/sql-reference/sql/drop-database-role)
- [SHOW DATABASE ROLES](/sql-reference/sql/show-database-roles)

Use the following command to activate a primary role or secondary roles within a user session:

- [USE ROLE](/sql-reference/sql/use-role)
- [USE SECONDARY ROLES](/sql-reference/sql/use-secondary-roles)

## Object tagging management

Snowflake supports the following DDL to create and manage tags:

- [CREATE TAG](/sql-reference/sql/create-tag)
- [ALTER TAG](/sql-reference/sql/alter-tag)
- [ALTER <object>](/sql-reference/sql/alter) (to set a tag on a Snowflake object)
- [SHOW TAGS](/sql-reference/sql/show-tags)
- [DROP TAG](/sql-reference/sql/drop-tag)
- [UNDROP TAG](/sql-reference/sql/undrop-tag)

Note that Snowflake does not support the [describe](/sql-reference/sql/desc) operation for the tag object.

## Access control management

Use the following commands to manage access control for objects by granting (and revoking) object privileges to roles and granting roles to users and other roles:

- [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege)
- [REVOKE <privileges> … FROM ROLE](/sql-reference/sql/revoke-privilege)
- [GRANT <privilege> … TO SHARE](/sql-reference/sql/grant-privilege-share)
- [REVOKE <privilege> … FROM SHARE](/sql-reference/sql/revoke-privilege-share)
- [GRANT DATABASE ROLE … TO SHARE](/sql-reference/sql/grant-database-role-share)
- [REVOKE DATABASE ROLE … FROM SHARE](/sql-reference/sql/revoke-database-role-share)
- [GRANT OWNERSHIP](/sql-reference/sql/grant-ownership)
- [GRANT ROLE](/sql-reference/sql/grant-role)
- [GRANT DATABASE ROLE](/sql-reference/sql/grant-database-role)
- [REVOKE ROLE](/sql-reference/sql/revoke-role)
- [REVOKE DATABASE ROLE](/sql-reference/sql/revoke-database-role)
- [SHOW GRANTS](/sql-reference/sql/show-grants)

## Network policy management

A network policy supports restricting access to your account based on user IP address. Use the following commands to create, alter, or drop network policies:

- [ALTER NETWORK POLICY](/sql-reference/sql/alter-network-policy)
- [CREATE NETWORK POLICY](/sql-reference/sql/create-network-policy)
- [DESCRIBE NETWORK POLICY](/sql-reference/sql/desc-network-policy)
- [DROP NETWORK POLICY](/sql-reference/sql/drop-network-policy)
- [SHOW NETWORK POLICIES](/sql-reference/sql/show-network-policies)

## Secret management

Snowflake supports the following DDL commands and operations to manage secrets:

- [CREATE SECRET](/sql-reference/sql/create-secret)
- [ALTER SECRET](/sql-reference/sql/alter-secret)
- [DROP SECRET](/sql-reference/sql/drop-secret)
- [SHOW SECRETS](/sql-reference/sql/show-secrets)
- [DESCRIBE SECRET](/sql-reference/sql/desc-secret)

## Password policy management

Snowflake provides the following DDL commands to manage password policy objects:

- [CREATE PASSWORD POLICY](/sql-reference/sql/create-password-policy)
- [ALTER PASSWORD POLICY](/sql-reference/sql/alter-password-policy)
- [DROP PASSWORD POLICY](/sql-reference/sql/drop-password-policy)
- [SHOW PASSWORD POLICIES](/sql-reference/sql/show-password-policies)
- [DESCRIBE PASSWORD POLICY](/sql-reference/sql/desc-password-policy)

## Session policy management

Snowflake provides the following DDL commands to manage session policy objects:

- [CREATE SESSION POLICY](/sql-reference/sql/create-session-policy)
- [ALTER SESSION POLICY](/sql-reference/sql/alter-session-policy)
- [DROP SESSION POLICY](/sql-reference/sql/drop-session-policy)
- [SHOW SESSION POLICIES](/sql-reference/sql/show-session-policies)
- [DESCRIBE SESSION POLICY](/sql-reference/sql/desc-session-policy)

## Third-party integrations

An integration is a Snowflake object that provides an interface between Snowflake and third-party services. Use the following commands to create, alter, or drop integrations:

### API integrations

- [ALTER API INTEGRATION](/sql-reference/sql/alter-api-integration)
- [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration)
- [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)
- [DROP INTEGRATION](/sql-reference/sql/drop-integration)
- [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations)

### Notification integrations

- [ALTER NOTIFICATION INTEGRATION](/sql-reference/sql/alter-notification-integration)
- [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration)
- [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration)
- [DROP INTEGRATION](/sql-reference/sql/drop-integration)
- [SHOW NOTIFICATION INTEGRATIONS](/sql-reference/sql/show-notification-integrations)

### Security integrations

- [ALTER SECURITY INTEGRATION](/sql-reference/sql/alter-security-integration)
- [CREATE SECURITY INTEGRATION](/sql-reference/sql/create-security-integration)
- [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)
- [DROP INTEGRATION](/sql-reference/sql/drop-integration)
- [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations)
- [SHOW DELEGATED AUTHORIZATIONS](/sql-reference/sql/show-delegated-authorizations)

### Storage integrations

- [ALTER STORAGE INTEGRATION](/sql-reference/sql/alter-storage-integration)
- [CREATE STORAGE INTEGRATION](/sql-reference/sql/create-storage-integration)
- [DESCRIBE INTEGRATION](/sql-reference/sql/desc-integration)
- [DROP INTEGRATION](/sql-reference/sql/drop-integration)
- [SHOW INTEGRATIONS](/sql-reference/sql/show-integrations)

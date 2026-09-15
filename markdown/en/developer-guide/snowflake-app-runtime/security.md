# Securing Snowflake App Runtime applications

Snowflake App Runtime applications automatically inherit Snowflake’s security
perimeter, including SSO, RBAC, and audit logging, without requiring manual
configuration. However, an application’s total security surface area is dynamic,
operating at the intersection of developer-defined logic and the end user’s
execution privileges. Developers naturally tend to prioritize application
functionality and user experience, but their underlying architectural
choices regarding data access and movement can have profound security
implications for the account as a whole. For account administrators,
understanding how these combined permissions interact is essential to
maintaining account security. This topic outlines these security
dynamics and the administrative controls available to govern them.

For guidance on building applications that minimize risk from the start, see
[Developing secure Snowflake App Runtime applications](/developer-guide/snowflake-app-runtime/secure-development).

## Understanding the risk surface

### Owner’s rights: the developer’s data reaches the user’s screen

When an app runs with [owner’s rights](/developer-guide/snowflake-app-runtime/access-control#label-snowflake-app-runtime-access-control-execute-as-role),
every query executes as the service’s execution role (the role
the developer used to create the service or the `EXECUTE_AS_ROLE`
specified for an application in a personal database). All users who
access the app may be exposed to this data, regardless of their own privileges,
and can interact with or modify the Snowflake account as allowed by the app and role.

**Example:** An execution role has `SELECT` on a sensitive payroll table. A user
with no payroll access opens the app. The app’s owner’s-rights queries return
payroll rows, and the developer’s UI displays them. The user now sees data they
wouldn’t have access to outside the app.

### Caller’s rights: the user’s data reaches the developer’s code

When an app uses [caller’s rights](/developer-guide/snowflake-app-runtime/access-control#label-snowflake-app-runtime-access-control-execute-as-role),
queries run as the user who opened the app. The developer’s code receives and
processes the results, so data the user is authorized to see flows through the
application. This, in effect, exposes the caller’s data to the application
developer.

The risk extends beyond data access. A caller’s rights app can potentially
perform actions on the account that the application owner couldn’t perform
directly. If a highly privileged user opens the app, the app can execute
operations using that user’s full scope of access: copying data to an external
location, granting privileges to other users or roles, creating or dropping
objects, or reading tables the developer has no direct access to. The developer
doesn’t need to be granted those privileges themselves. They only need a user
with those privileges to open the app. This applies to any user with elevated
access, not just account admins.

### App services are multi-tenant

An Application Service is a shared container that serves all users who have
access to it. This introduces two isolation risks:

- **Cross-caller leakage:** A bug in session isolation could expose query results
  from one user’s session to another user who’s using the app at the same time.
- **Data movement from caller to owner:** Caller’s rights queries run through the
  developer’s code. The developer can log, store, or forward results, moving data
  from the caller’s access scope to the owner’s, without the caller’s knowledge.

### External access: data can leave the account

An app that declares an [external access integration](/developer-guide/snowflake-app-runtime/app-yml)
can make outbound network calls. If the app passes query results, user inputs, or
other Snowflake data to an external service, that data exits Snowflake’s
governance boundary. Additionally, an app can always execute SQL queries to send
data to an external service regardless of network and most role permission restrictions.

### Sensitive data in logs

Application logs flow into the account’s [event table](/developer-guide/logging-tracing/event-table-setting-up).
Anyone with access to the event table can read log messages from all Application
Services in the account. If the developer’s code logs query results, user inputs,
or other sensitive values, that information is accessible to anyone with access to
the event table, or to anyone with `MONITOR` privilege on the Application Service
through
[SYSTEM$GET\_APPLICATION\_SERVICE\_LOGS](/sql-reference/functions/system_get_application_service_logs).

## Governing execution scope

The controls in this section address both execution-mode risks: the owner’s rights
risk (the execution role’s data reaching users who shouldn’t see it) and the
caller’s rights risk (a user’s privileges being available to the developer’s code).
For caller’s rights, Snowflake uses
[restricted caller’s rights](/developer-guide/restricted-callers-rights): an
operation succeeds only when both the caller’s own privileges and the execution
role’s caller grants permit it.

### Scoping the execution role

For owner’s rights applications, the execution role is the role that created the
Application Service (or the `EXECUTE_AS_ROLE` specified for personal database
apps). Every query the app runs executes as this role, so the data potentially
visible to all users of the app, or the changes the app can make to the Snowflake
account, is bounded by what this role can access.

Administrators can’t directly constrain the privileges of a developer’s execution
role. What they can do is control which roles are permitted to create Application
Services at all. This has the same practical effect: only roles that
administrators have approved for service creation can become execution roles.

The approach has two steps:

1. **Restrict which databases allow Application Service creation** using feature
   policies so services can only be deployed to databases the administrator owns
   and manages, not to arbitrary personal databases or ad-hoc schemas. See
   [Governing app deployment](#label-snowflake-app-runtime-security-deployment).
2. **Grant `CREATE APPLICATION SERVICE` only to approved roles** on the target
   schema. This ensures that only pre-approved, appropriately scoped roles can
   create services (and therefore become execution roles).

Copy code

```
GRANT USAGE ON DATABASE my_app_db TO ROLE approved_deploy_role;
GRANT USAGE ON SCHEMA my_app_db.app_schema TO ROLE approved_deploy_role;
GRANT CREATE APPLICATION SERVICE ON SCHEMA my_app_db.app_schema
  TO ROLE approved_deploy_role;
```

With this pattern, only `approved_deploy_role` (and roles that inherit it)
can create Application Services in `my_app_db.app_schema`. Any attempt to deploy
from a different role fails, preventing an unapproved role from becoming an
execution role.

Note

These steps don’t directly constrain personal databases. By default, any user
can deploy an Application Service to their own personal database, where it runs
under a role they control. Administrators who want to govern personal databases
must take special steps: either block Application Service creation in personal
databases entirely with a feature policy (see
[Restricting app creation in personal databases](#label-snowflake-app-runtime-security-pdb-creation)),
or allow personal-use deployment while restricting the ability to share the app
with other users (see
[Restricting sharing](#label-snowflake-app-runtime-security-restricting-sharing) and
[Revoking BIND SERVICE ENDPOINT from PUBLIC](#label-snowflake-app-runtime-security-bind-service-endpoint-overview)).

### Scoping caller’s rights

By default, an Application Service using caller’s rights has no access to the
caller’s privileges at all. If the execution role has no caller grants, the
app can’t act on the caller’s behalf.

#### Caller grants and the execution role

A caller grant is a special form of grant given to the execution role of
an Application Service (either directly or through a child role). The caller
grant conveys the *privilege to use a caller’s privilege* on a given object.
For example, given an application created by the role `APP_ROLE`:

Copy code

```
USE ROLE APP_ROLE;
CREATE APPLICATION SERVICE my_app ...;
```

the application may be given the ability to read all of the data in the
database `app_data` with the following grant:

Copy code

```
GRANT CALLER DATA READ ON DATABASE app_data TO ROLE APP_ROLE;
```

Important

This grant doesn’t give the application itself the ability to read data in
`app_data`. It gives the application the ability to read data in `app_data`
*on behalf of the caller*. If the caller doesn’t have privileges on
`app_data` (or the specific tables and schemas within it), the application
can’t read that data either. The application’s effective access is always
bounded by the caller’s own privileges.

For personal databases, the execution role may optionally be set explicitly
using the `EXECUTE_AS_ROLE` property in
[CREATE APPLICATION SERVICE](/sql-reference/sql/create-application-service).

#### Types of caller grants

Caller grants are granted on objects (tables, schemas, databases, warehouses) to
the execution role. There are four forms, from broadest to most specific:

**High-level grants**

[High-level caller privileges](/developer-guide/restricted-callers-rights/high-level-caller-privileges)
are named categories of operations rather than individual SQL privileges. Each
one authorizes a broad class of access (for example, all read operations in
a database, or full account-level control) without enumerating every underlying
privilege. Use these when the app needs a well-defined class of access and you
want grants to stay stable as the schema evolves.

Copy code

```
-- Let the app read and write all data in a database on the caller's behalf
GRANT CALLER DATA READ ON DATABASE app_data TO ROLE app_role;
GRANT CALLER DATA WRITE ON DATABASE app_data TO ROLE app_role;
```

**Broad grants (`GRANT ALL CALLER PRIVILEGES` / `GRANT ALL INHERITED CALLER PRIVILEGES`)**

Grants all of the caller’s individual privileges on a named object, or on all
current and future objects of a given type in a container. Use sparingly: this
form conveys every individual privilege the caller happens to hold on the target,
including ones you may not have anticipated.

Copy code

```
-- Grant every privilege the caller holds on tables in a database
GRANT ALL INHERITED CALLER PRIVILEGES ON ALL TABLES IN DATABASE my_db
  TO ROLE my_execution_role;
```

For more information, see
[About caller grants](/developer-guide/restricted-callers-rights#label-restricted-callers-rights-about-grants).

**Container-level grants (`GRANT INHERITED CALLER`)**

Grants the specified privilege on all current and future objects of the given
type in a schema, database, or account. Use this when the app needs caller-level
access across a set of objects without enumerating each one individually.

Copy code

```
-- Let the app read any table the caller can read in a schema
GRANT INHERITED CALLER SELECT ON ALL TABLES IN SCHEMA my_db.my_schema
  TO ROLE my_execution_role;
```

For more information, see
[About caller grants](/developer-guide/restricted-callers-rights#label-restricted-callers-rights-about-grants).

**Object grants (`GRANT CALLER`)**

Grants the specified privilege on one named object. Use this for the narrowest
possible access, where the app needs the caller’s privileges on a specific table
or view.

Copy code

```
-- Let the app query a specific view on the caller's behalf
GRANT CALLER SELECT ON VIEW my_schema.user_summary TO ROLE my_execution_role;
```

For more information, see
[About caller grants](/developer-guide/restricted-callers-rights#label-restricted-callers-rights-about-grants).

For the complete syntax, see [GRANT CALLER](/sql-reference/sql/grant-caller). To audit what
has been granted, use [SHOW CALLER GRANTS](/sql-reference/sql/show-caller-grants).

#### Caller roles

Rather than granting caller grants directly to individual execution roles, consider
creating dedicated roles (either account roles or database roles) whose sole purpose
is to hold a named collection of caller grants. These *caller roles* act as reusable,
auditable bundles of caller access grouped by purpose.

A descriptive naming convention makes the intent of each caller role clear at a glance:

- `PAYROLL_CALLER_RO`: read-only caller access to the payroll database
- `SALES_CALLER_RW_LEADS`: read/write caller access to the sales leads schema

Copy code

```
-- Read-only caller access to the payroll database
CREATE ROLE payroll_caller_ro;
GRANT CALLER DATA READ ON DATABASE payroll_db TO ROLE payroll_caller_ro;

-- Read/write caller access to sales leads
CREATE ROLE sales_caller_rw_leads;
GRANT CALLER DATA READ ON SCHEMA sales_db.leads TO ROLE sales_caller_rw_leads;
GRANT CALLER DATA WRITE ON SCHEMA sales_db.leads TO ROLE sales_caller_rw_leads;
```

Caller roles can then be granted to specific execution roles, or to the account roles
approved to create Application Services, so that any application they deploy inherits
the appropriate caller grants:

Copy code

```
-- Grant a caller role directly to an execution role
GRANT ROLE payroll_caller_ro TO ROLE my_execution_role;

-- Or grant it to the role permitted to create services,
-- so every app that role deploys can act on the caller's behalf
GRANT ROLE payroll_caller_ro TO ROLE approved_deploy_role;
```

This pattern has several advantages over per-execution-role grants:

- **Discoverability:** All caller grants for a given dataset are in one place.
  `SHOW GRANTS TO ROLE payroll_caller_ro` reveals exactly what caller access is bundled.
- **Reuse:** Multiple applications that need the same caller access share one role
  rather than duplicating grants across execution roles.
- **Revocation:** Revoking a caller role from an execution role removes all of its
  associated caller grants in a single operation.
- **Auditability:** Role names encode intent, so it’s immediately clear to a reviewer
  that `SALES_CALLER_RW_LEADS` conveys write access to leads data on the caller’s behalf.

#### Granting caller access to the PUBLIC role

In accounts that sufficiently trust their users, or that already restrict which
roles can develop applications, it can be appropriate to grant caller privileges
to the `PUBLIC` role. Because every user in the account inherits `PUBLIC`, this
allows any execution role to act on the caller’s behalf within the scope of the
grant, without requiring per-role grants for each new application.

This pattern works well for read-only applications. A single grant broadly
enables that class of app without ongoing administrator involvement:

Copy code

```
-- Allow any execution role to read data on the caller's behalf
GRANT CALLER DATA READ ON DATABASE app_data TO ROLE PUBLIC;
```

This approach is well-suited to accounts where one of the following conditions
holds:

- **Trusted user base:** All users in the account are trusted, such as in a
  single-team or internal-tools deployment where broad read access on the
  caller’s behalf is acceptable.
- **Restricted deployment:** Access to the development toolchain is already
  tightly controlled so that only an approved set of roles can create Application
  Services. The grant is broad, but the set of roles that can act on it is narrow.
  See [Scoping the execution role](#label-snowflake-app-runtime-security-owners-rights-controls)
  and [Governing app deployment](#label-snowflake-app-runtime-security-deployment).

## Governing app deployment

Deployment governance covers more than just where an application lands. A fully
governed deployment controls three things:

- **Where** the application is created: which databases and schemas are permitted
  deployment targets. Feature policies enforce this.
- **Who** can create applications: which roles hold `CREATE APPLICATION SERVICE`
  on the target schema. Privilege grants enforce this.
- **What the application executes as:** the execution role’s scope of access, which
  determines what data is reachable through the app. This is addressed in
  [Governing execution scope](#label-snowflake-app-runtime-security-execution-scope).

The controls below address the first two. Used together, they ensure that only
pre-approved roles can deploy, and only to databases the administrator owns and manages.

### Account-wide and per-database restrictions

Feature policies can block App Runtime object creation account-wide, or allow it
only in specific databases. A per-database policy overrides the account-level policy
for that database; the two don’t compose.

To block creation in all databases:

Copy code

```
CREATE FEATURE POLICY block_apps
  BLOCKED_OBJECT_TYPES_FOR_CREATION = (APPLICATION_SERVICES, ARTIFACT_REPOSITORIES);

ALTER ACCOUNT SET FEATURE POLICY block_apps FOR ALL DATABASES;
```

To allow creation in one designated database while blocking it everywhere else, pair
an account-wide blocking policy with a permissive policy on the approved database:

Copy code

```
-- Block everywhere by default
ALTER ACCOUNT SET FEATURE POLICY block_apps FOR ALL DATABASES;

-- Override for the approved deployment target
CREATE FEATURE POLICY allow_apps;  -- no blocked types = no restrictions
ALTER DATABASE my_app_db SET FEATURE POLICY allow_apps;
```

With this configuration, `CREATE APPLICATION SERVICE` and `CREATE ARTIFACT REPOSITORY`
succeed only in `my_app_db`. Attempts in any other database fail.

For conditional rules (for example, blocking Application Services only in a specific
schema), see [Feature policy rules](/LIMITEDACCESS/feature-policy-rules), which is in
private preview.

### Restricting app creation in personal databases

By default, `snow app deploy` targets each user’s
[personal database](/user-guide/personal-databases), so any user with the CLI can
create an Application Service without administrator involvement. To require deployment
to a shared, administrator-managed database instead, block App Runtime object creation
in personal databases:

Copy code

```
CREATE FEATURE POLICY block_apps_in_pdb
  BLOCKED_OBJECT_TYPES_FOR_CREATION = (APPLICATION_SERVICES, ARTIFACT_REPOSITORIES);

ALTER ACCOUNT SET FEATURE POLICY block_apps_in_pdb FOR ALL PERSONAL DATABASES;
```

After the policy is set, attempts to create an Application Service or Artifact
Repository in a personal database fail. Users must deploy to the shared destination
database configured by
[account administrator setup](/developer-guide/snowflake-app-runtime/account-admin-setup).

## Governing app distribution

The controls in this section determine who can access a running Application
Service and which roles it can be shared with.

### Restricting sharing

When a role receives `USAGE` on an Application Service, every user with that
role gains access to the app and its endpoints. In a caller’s rights app, that
means those users can trigger queries that run on their behalf. In an owner’s
rights app, it means they can reach any data the execution role can access.
Without sharing restrictions, any role in the account can be granted access to
any Application Service by whoever holds `OWNERSHIP` on it; the administrator
has no automatic veto.

#### Database or schema-scoped restrictions

The deployment controls described in
[Governing app deployment](#label-snowflake-app-runtime-security-deployment)
do more than restrict where applications are created. When applications are
confined to administrator-owned databases and schemas, the standard Snowflake
privilege hierarchy becomes a second layer of access control.

A role needs `USAGE` on both the containing database and schema before it can
access any object within them, including an Application Service. This means
that even if an application owner grants `USAGE` on an Application Service to
an account role, that role can’t access the application unless the administrator
has also granted `USAGE` on the database and schema that contain it.

Centralizing deployment in a managed database gives the administrator durable
control over the universe of roles that can ever reach those applications:

Copy code

```
-- Only grant database and schema access to approved roles
GRANT USAGE ON DATABASE my_app_db TO ROLE approved_user_role;
GRANT USAGE ON SCHEMA my_app_db.app_schema TO ROLE approved_user_role;
```

Roles not granted `USAGE` on the database or schema can’t access any
Application Service within it, regardless of what the application owner grants.
This is a passive control that requires no policy configuration; it follows
directly from Snowflake’s object hierarchy.

### Auto-sharing

Rather than granting `USAGE` on each Application Service individually, you can use
`GRANT INHERITED USAGE` to share all existing and future Application Services in a
database or schema with a specific role in a single statement. Any Application Service
created in the container after the grant is issued is automatically accessible to that
role without any further action from the app owner.

Copy code

```
-- Share all current and future Application Services in a database
GRANT INHERITED USAGE ON ALL APPLICATION SERVICES IN DATABASE my_app_db
  TO ROLE approved_user_role;

-- Scope auto-sharing to a specific schema instead
GRANT INHERITED USAGE ON ALL APPLICATION SERVICES IN SCHEMA my_app_db.app_schema
  TO ROLE approved_user_role;
```

This pattern pairs well with the database- and schema-scoped controls described in
[Database or schema-scoped restrictions](#label-snowflake-app-runtime-security-db-schema-restrictions).
The administrator grants `USAGE` on the container once (restricting who can enter the
namespace) and then issues a single `GRANT INHERITED USAGE` so that every app
deployed there is immediately reachable by approved roles. New deployments are covered
automatically as they are created, and there’s no risk of an app being deployed but
accidentally left unshared.

### Revoking BIND SERVICE ENDPOINT from PUBLIC

`BIND SERVICE ENDPOINT` is an account-level privilege that enables a service
(either an Application Service or a Snowpark Container Service) to accept
incoming authenticated connections from any Snowflake identity. Without it, the
service’s behavior depends on where it’s deployed:

- **Outside a personal database:** The service won’t start at all. Endpoint
  binding requires the privilege, and the service can’t accept connections
  without a bound endpoint.
- **Inside a personal database:** The service starts and binds its endpoint, but
  only the user who owns it is authorized to access the application.

By default, `BIND SERVICE ENDPOINT` is granted to the `PUBLIC` role, so any
role in the account can deploy a service with a live endpoint accessible to all
Snowflake identities. Revoking the privilege from `PUBLIC` and granting it only
to approved roles creates a clean two-tier deployment model. Developers can
still create services in their personal database for their own personal use.
Those services start and are accessible to the owner without the privilege. Only
roles that have been explicitly granted `BIND SERVICE ENDPOINT` can deploy a
service that accepts connections from any authenticated user.

Copy code

```
REVOKE BIND SERVICE ENDPOINT ON ACCOUNT FROM ROLE PUBLIC;

-- Grant only to roles approved for shared deployment
GRANT BIND SERVICE ENDPOINT ON ACCOUNT TO ROLE approved_deploy_role;
```

Warning

Before revoking from `PUBLIC`, identify every Application Service and Snowpark
Container Service currently running in your account. Any service owned by a role
that doesn’t receive an explicit re-grant will lose endpoint access immediately,
including services that are already running.

## Governing outbound network access

The controls in this section address the external access risk: apps sending
Snowflake data to external services outside Snowflake’s governance boundary.

### Build-time egress to package registries

By default, the remote build that `snow app deploy` runs has scoped outbound
access to public package registries so it can resolve dependencies. Accounts that
prefer tighter egress control can disable most default build-time access. When
disabled, builds that need external packages must reference an explicit
[external access integration](/developer-guide/snowflake-app-runtime/app-yml)
in `app.yml`.

To disable all automatic outbound access during remote builds:

Copy code

```
ALTER ACCOUNT SET ENABLE_REMOTE_BUILD_SERVICE_EGRESS_DESTINATIONS = FALSE;
```

To disable only the default npm and Google Fonts hosts while leaving other
upstream toggles unchanged:

Copy code

```
ALTER ACCOUNT SET ALLOW_NPM_PACKAGE_DOWNLOAD = FALSE;
```

Both parameters require a role with account-level parameter privileges, such as
`ACCOUNTADMIN`. For details on supplying custom egress using `build_eai`, see
[Disabling default build egress](/developer-guide/snowflake-app-runtime/deploy#label-deploy-build-disable-egress).

Warning

If you disable the default build-time egress, builds that depend on external
packages will fail unless developers can reference an explicit external access
integration. Before disabling default access, create an
[external access integration](/sql-reference/sql/create-external-access-integration)
that allows connections to your approved package registries, then grant
`USAGE` on it to the account roles that will be doing development so they can
reference it with `build_eai` in `app.yml`. Without this preparation, developers
have no way to resolve dependencies during remote builds.

### Runtime external access integrations

Apps declare runtime network integrations in `app.yml` under
`external_access_integrations`. At deploy time, the deploying role must have
`USAGE` on each named integration. At runtime, the app can then make direct
network-based outbound calls to the hosts the integration permits beyond basic
SQL queries.

A role with `USAGE` on an overly permissive EAI (one that allows connections to
arbitrary hosts) can deploy an app that sends any data it can reach to any
external endpoint. Scope each EAI to the narrowest set of allowed hosts the app
actually requires, and grant `USAGE` only to the specific roles that need it:

Copy code

```
-- Scope the EAI to a single known API host
CREATE EXTERNAL ACCESS INTEGRATION my_api_integration
  ALLOWED_NETWORK_RULES = (my_api_network_rule)
  ALLOWED_AUTHENTICATION_SECRETS = ()
  ENABLED = TRUE;

-- Grant usage only to the deploy role that references it
GRANT USAGE ON INTEGRATION my_api_integration TO ROLE my_deploy_role;
```

For details on declaring integrations in the app manifest, see
[app.yml reference](/developer-guide/snowflake-app-runtime/app-yml).

## Governing log access

App Runtime applications write log output to the account’s
[event table](/developer-guide/logging-tracing/event-table-setting-up).
There are no platform controls that restrict what an application developer
chooses to log. An app can log query results, user inputs, session tokens, or
any other value it can reach at runtime. This means the event table may contain
sensitive data, and any role with `SELECT` on the event table can read log
output from every Application Service in the account, not just the ones it owns.

Administrators should treat event table access as they would access to any
sensitive data store: grant `SELECT` only to roles that have a clear operational
need, such as dedicated security or observability roles, and avoid granting it
to broad roles like `PUBLIC` or `SYSADMIN`.

In addition, the `MONITOR` privilege on an Application Service grants access to
that service’s logs through
[SYSTEM$GET\_APPLICATION\_SERVICE\_LOGS](/sql-reference/functions/system_get_application_service_logs).
Grant `MONITOR` only to dedicated operations roles rather than to roles with
broad membership, to limit who can retrieve per-service log streams directly.

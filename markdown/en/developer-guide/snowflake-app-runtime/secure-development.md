# Developing secure Snowflake App Runtime applications

The architectural choices you make as a developer determine how much risk your
application introduces to the account. Administrators can apply governance controls
after the fact, but the most effective security comes from the design itself: choosing
the right execution context, handling data carefully, managing credentials properly,
and keeping dependencies clean.

This page walks through the key practices that minimize risk at the source. For the
administrator perspective (the controls available to govern deployed applications), see
[Securing Snowflake App Runtime applications](/developer-guide/snowflake-app-runtime/security).

## Data access design

### Choose the right execution context

App Runtime queries run in one of two modes:

- **Owner’s rights** (default): queries run as the app’s execution role. Every user
  who opens the app can see any data that role can access, regardless of the user’s
  own privileges.
- **Caller’s rights**: queries run as the signed-in user. Snowflake applies that
  user’s own role and privileges, including row-level security policies, column
  masking policies, and object-level access controls.

Where the use case permits, prefer caller’s rights. Because privileges are evaluated
at the user level, you get per-user data isolation automatically, without writing any
access control logic yourself. You also can’t accidentally expose data the user
shouldn’t see through an over-privileged execution role.

Owner’s rights is appropriate when the app queries data that no individual user holds
privileges to, such as a shared analytics dashboard that joins across multiple
restricted data sources. In those cases, scope the execution role carefully (see
[Scope the execution role to least privilege](#label-snowflake-app-runtime-secure-development-least-privilege))
and enforce application-level checks where needed (see
[Enforce application-level access control](#label-snowflake-app-runtime-secure-development-app-acl)).

With `querySnowflake` from `lib/snowflake.ts` (see
[Query Snowflake](/developer-guide/snowflake-app-runtime/query-snowflake)), switching between
modes is one parameter:

Copy code

```
// Owner's rights (default): queries run as the execution role
const rows = await querySnowflake("SELECT * FROM sales.summary");

// Caller's rights: queries run as the signed-in user
const rows = await querySnowflake("SELECT * FROM sales.detail", {
  callersRights: true,
});
```

Caller’s rights requires that the execution role hold caller grants authorizing the
specific operations the app performs on the caller’s behalf. Without those grants,
caller’s rights queries have no access to the caller’s data. An account administrator
sets these up. See
[Scoping caller’s rights](/developer-guide/snowflake-app-runtime/security#label-snowflake-app-runtime-security-callers-rights-controls)
for details.

### Scope the execution role to least privilege

The execution role is the identity your owner’s rights queries run as. Its privileges
define the ceiling of what data all users of the app can potentially reach. Keep that
scope as narrow as possible:

- Use a dedicated role created specifically for this application. Don’t use
  `SYSADMIN`, `ACCOUNTADMIN`, or any other broad administrative role as an execution role.
- Grant access only to the specific databases, schemas, and tables the application
  actually queries.
- Separate read and write privileges into distinct roles when the app performs both
  types of operations, and use the narrowest role appropriate for each.
- Avoid future grants that automatically extend privileges to the role as the schema
  evolves. Review privilege grants explicitly when the schema changes.

A narrow execution role limits the blast radius of a bug or a misconfigured query.
If the app unexpectedly returns data it shouldn’t, the damage is bounded by what
the execution role can access.

### Enforce application-level access control in owner’s rights apps

With owner’s rights, every user who opens the app shares the execution role’s data
access. Snowflake’s privilege system can’t differentiate between them. If your app
serves users with different levels of trust, enforce access control in your
application logic before returning sensitive data.

A reliable approach is to run a quick identity query under caller’s rights before
executing the owner’s rights data query. Because it runs as the caller, it returns
that user’s actual Snowflake identity:

Copy code

```
// Check the caller's identity (runs as the signed-in user)
const [identity] = await querySnowflake(
  `SELECT CURRENT_USER()                         AS username,
          CURRENT_ROLE()                         AS primary_role,
          IS_ROLE_IN_SESSION('DATA_ANALYST')      AS is_analyst`,
  { callersRights: true },
);

if (!identity.IS_ANALYST) {
  return Response.json({ error: 'Access denied' }, { status: 403 });
}

// Proceed with the owner's rights data query
const data = await querySnowflake('SELECT * FROM sensitive_reports');
```

`CURRENT_USER()` returns the signed-in user’s username. `CURRENT_ROLE()` returns
their primary role. `IS_ROLE_IN_SESSION(role_name)` returns `true` if the named role
is active in the caller’s session. The `SYS_CONTEXT('SNOWFLAKE$SESSION', ...)`
function returns the same values and is also available.

Don’t rely solely on hiding UI elements to restrict data. A user who intercepts your
application’s HTTP responses can bypass UI-level controls entirely. Enforce access at
the query level.

## Data handling

### Use bind variables for all queries

Always use bind variables (parameterized queries) instead of constructing SQL by
concatenating user-supplied values into a string. String concatenation is a SQL
injection vector: a user who controls an input can craft a value that alters the
query’s logic.

Bind variables also protect against unintentional data logging. When you embed a
value directly in the SQL string, that literal value becomes part of the query text.
Snowflake records query text in query history, where it’s visible to anyone with
access to `ACCOUNT_USAGE.QUERY_HISTORY`. Bind parameters are passed separately and
are not included in the query text.

Copy code

```
// Don't do this: the user-supplied value appears as plain text in query history
const result = await querySnowflake(
  `SELECT * FROM orders WHERE customer_id = '${customerId}'`,
);

// Do this: the bind value is passed separately and isn't recorded in query text
const result = await querySnowflake(
  'SELECT * FROM orders WHERE customer_id = ?',
  { binds: [customerId] },
);
```

### Avoid logging sensitive data

Application logs flow into the account’s
[event table](/developer-guide/logging-tracing/event-table-setting-up). Any role
with `SELECT` on the event table can read log output from every Application Service
in the account. Anyone with `MONITOR` privilege on your Application Service can also
read per-service logs directly through
[SYSTEM$GET\_APPLICATION\_SERVICE\_LOGS](/sql-reference/functions/system_get_application_service_logs).

Follow these practices:

- Log operational events (request metadata, error codes, latency) rather than data
  values or query results.
- Remove debug log statements that print query results before deploying. They’re
  easy to commit by accident.
- Never log user inputs, personally identifiable information (PII), session tokens,
  or any secret values.
- Keep log verbosity proportional to operational need. High-volume logging increases
  cost and broadens the set of data potentially visible in the event table.

### Return safe error messages to users

Raw Snowflake error messages often include object names, column names, and internal
identifiers. Returning them to the end user leaks information about your schema and
can help an attacker map your data model.

Catch errors at the server, log the full detail internally for debugging, and return
a generic message in the HTTP response:

Copy code

```
export async function GET(request: Request) {
  try {
    const data = await querySnowflake('SELECT ...');
    return Response.json(data);
  } catch (err) {
    // Log full error server-side for debugging
    console.error('Query failed:', err);
    // Return a generic message to the caller
    return Response.json({ error: 'An error occurred' }, { status: 500 });
  }
}
```

## Credential and secret management

### Declare secrets in app.yml, not in source code

If your application uses external credentials, declare them under
[`secrets`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-secrets)
in [`app.yml`](/developer-guide/snowflake-app-runtime/app-yml). Snowflake mounts
each secret as files under `/secrets/<name>/`, not as environment variables.
They’re never embedded in your source tree, committed to version control, or
visible in the container image. For the files each secret type produces and how
to read them, see
[Secret files](/developer-guide/snowflake-app-runtime/runtime-environment#label-runtime-environment-secret-files).

Hardcoded credentials in source code are a persistent breach risk: anyone with read
access to the repository, the build artifact, or the deployed container can extract
them. Credentials stored in `.env` files are similarly vulnerable to shell history
and CI/CD configuration exposure.

Important

Never commit credentials, API keys, or passwords to your repository, even
temporarily. Use `app.yml` secrets or a Snowflake
[secret object](/sql-reference/sql/create-secret) for any value that grants
access to an external system.

### Prefer session tokens over static credentials

When your application authenticates to Snowflake or to external services, prefer
short-lived session tokens and OAuth flows over static passwords or long-lived API keys.

Snowflake handles authentication automatically for App Runtime: an OAuth token is
available inside the container and rotates automatically. You don’t manage Snowflake
credentials at all. For the token paths and how to combine them with a caller token,
see
[Session and caller tokens](/developer-guide/snowflake-app-runtime/runtime-environment#label-runtime-environment-tokens).
For external services, the same principle applies: request short-lived credentials
through the service’s OAuth or credential rotation tooling, rather than embedding a
long-lived secret.

Static long-lived credentials remain valid until manually rotated. If one is ever
exposed, the window of risk is open-ended. Short-lived tokens expire automatically
and limit that window.

### Keep credentials in execution memory only

Credentials and tokens should exist only in execution memory for as long as they’re
needed:

- Don’t write tokens to disk, temporary files, or any path that persists beyond
  the request.
- Don’t log credential values, even at debug level. Log the fact that a credential
  was obtained, not its value.
- Clear sensitive values from variables when no longer needed, particularly in
  long-lived request handlers.

## App sharing and access design

### Scope the USAGE grant to the intended audience

The `USAGE` privilege on an Application Service controls who can open the app. For
owner’s rights applications, granting `USAGE` is also effectively a data access
decision: every user whose role has `USAGE` can see whatever data the execution role
can access.

Be deliberate about who receives `USAGE`:

- Grant it only to roles whose members should have access to the data the app
  surfaces.
- Avoid granting `USAGE` to `PUBLIC` or `SYSADMIN` for applications that query
  sensitive data.
- If the same application should serve users at different data access levels,
  consider deploying separate instances with separate execution roles scoped to
  each audience, rather than serving all users from a single broadly privileged
  instance.

### Use caller’s rights for mixed-audience apps

If you need to serve users with different data access levels from a single app, the
cleanest solution is caller’s rights for data queries. Each query runs as the
signed-in user, so Snowflake’s privilege system handles the differentiation at the
database layer, with no application logic required.

If caller’s rights isn’t available because the necessary caller grants haven’t been
configured, use the identity check pattern from
[Enforce application-level access control](#label-snowflake-app-runtime-secure-development-app-acl)
to gate data queries at the application layer.

In either case, enforce access at the query level. UI-only visibility controls don’t
protect data at the API layer.

## Stateless design and session isolation

### Design for stateless execution

App Runtime is designed for stateless applications. In-memory state (module-level
variables, in-process caches, global singletons) is not guaranteed to survive across
application restarts, upgrades, or auto-suspend and resume cycles. Logic that depends
on that state persisting between requests will behave unpredictably in production.

Store durable application state in Snowflake: write it to a table and read it back at
the start of the next request. In-memory caching is fine for values within a single
request, or for short-lived caches where staleness is acceptable and losing the cache
is handled gracefully. Don’t cache values in a way that assumes the cache is still
populated on the next request from the same user.

### Isolate per-user session state

Multiple users share the same container instance. If you store request-scoped data
in module-level or global variables, a value written during one user’s request can be
read during another user’s concurrent request. This is a cross-user data leakage
bug, and it’s particularly dangerous when the shared value is a user identifier,
query results, or a session token.

Keep all per-request state scoped to the request itself:

Copy code

```
// Don't do this: module-level variable is shared across all concurrent requests
let currentUserId: string | null = null;

export async function GET(request: Request) {
  currentUserId = request.headers.get('sf-context-current-user'); // Overwritten by concurrent requests
  const data = await fetchDataFor(currentUserId);
  return Response.json(data);
}

// Do this: local variable is isolated to this request invocation
export async function GET(request: Request) {
  const userId = request.headers.get('sf-context-current-user'); // Scoped to this call
  const data = await fetchDataFor(userId);
  return Response.json(data);
}
```

In Next.js, use route handler locals, React Server Component request scope, or
per-request closures to carry identity and session data. Avoid module-global state
for anything that varies per user or per request.

## External access and supply chain security

### Minimize external access scope

If your application makes outbound network calls, declare the integrations under
[`external_access_integrations`](/developer-guide/snowflake-app-runtime/app-yml#label-snowflake-apps-manifest-external-access-integrations)
in `app.yml`, and list exactly the hostnames the app contacts in the network
rules for those integrations. An overly
permissive rule is a risk multiplier: any code running in your process, including
npm dependencies and their transitive dependencies, can make outbound requests to
any host the rule permits.

A compromised or malicious dependency can only exfiltrate data if an external access
integration permits the destination. Tight network rules contain that risk to the
specific hosts you’ve approved.

Before deploying to production, review your external access integrations and remove
any hostnames that aren’t strictly required. Prefer specific hostname rules over
broad CIDR ranges or wildcard domains.

### Lock your dependencies

Commit `package-lock.json` to version control and use `npm ci` (not `npm install`)
in your build scripts. `npm ci` installs exactly the versions recorded in the
lockfile and fails on any mismatch, preventing silent version drift between
development and production builds.

Avoid permissive semver ranges in `package.json` for production applications:

Copy code

```
{
  "dependencies": {
    "some-library": "^2.1.0",
    "another-package": "2.3.1"
  }
}
```

The `^` prefix accepts any compatible minor or patch update. If a maintainer
publishes a compromised version within your accepted range, your next build picks it
up without any action on your part. Pinning to an exact version (`"2.3.1"`) means
updates are intentional and auditable.

### Audit dependencies for known vulnerabilities

Run `npm audit` before deploying and as a regular part of your development workflow:

Copy code

```
npm audit
```

Review the full dependency tree with `npm ls --all` to understand what transitive
dependencies your app carries. A direct dependency on a well-maintained library can
still pull in transitive dependencies with known vulnerabilities.

When adding new dependencies, consider:

- Whether the package is actively maintained and has a published security
  disclosure policy.
- The package’s dependency count and scope. A small utility with a large, complex
  dependency tree warrants scrutiny.
- Whether the package makes outbound network calls, reads from the filesystem, or
  executes shell commands. In a data-adjacent, multi-tenant environment, these
  capabilities are higher risk than in an isolated setting.

Consider automating dependency updates with a tool such as GitHub Dependabot or a
similar dependency update service. These tools watch your manifest and lockfile,
open a pull request when an update is available, and surface known vulnerabilities in
the versions you depend on. Automating updates helps you apply security patches
promptly rather than discovering a vulnerable dependency months later during a
manual audit. With an automated update tool in place, still review each proposed
update before merging it, since a compromised dependency can enter your application
the same way a legitimate update does.

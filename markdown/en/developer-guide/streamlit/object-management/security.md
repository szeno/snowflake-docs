# Security overview for Streamlit in Snowflake

This topic provides a security overview for system administrators managing Streamlit in Snowflake in their Snowflake accounts.
Understanding the security model and implementing proper controls ensures that developers can build secure applications
while administrators maintain governance over sensitive data and resources.

## Security model

Streamlit in Snowflake follows Snowflake’s comprehensive security model, which includes authentication, role-based access control,
network policies, and data governance features. Apps are first-class Snowflake objects that integrate with existing
security infrastructure.

### Owner’s rights execution

By default, Streamlit apps run with owner’s rights, similar to stored procedures. This has the following consequences:

- Apps execute queries using the privileges of the app owner, not the viewer.
- The app owner’s role determines what data and operations the app can access.
- Viewers can interact with the app without needing direct access to underlying tables or views.

This model eliminates the need for service account tokens and integrates seamlessly with Snowflake’s authentication
and access control features. For more information, see [Understanding owner’s rights and Streamlit in Snowflake apps](/developer-guide/streamlit/object-management/owners-rights).

As an alternative, you can configure a container-runtime app to use restricted caller’s rights (Preview), which
allows the app to run with the viewer’s privileges instead of the owner’s. For more information, see
[Restricted caller’s rights and Streamlit in Snowflake](/developer-guide/streamlit/features/restricted-callers-rights).

### Shared responsibility model

Security responsibility is shared between Snowflake, account administrators, and app developers:

- Snowflake provides the secure platform, authentication, encryption, and security features.
- Administrators configure account-level security policies, manage roles and privileges, and audit app usage.
- App developers write secure code, handle secrets properly, and follow security best practices.

For more information about Snowflake’s security model, see [Snowflake’s Shared Responsibility Model](https://www.snowflake.com/en/resources/report/snowflake-shared-responsibility-model/).

### Content Security Policy

All Streamlit apps run within a [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP) (CSP)
that restricts which resources can be loaded. This policy provides defense-in-depth protection against cross-site scripting (XSS)
and other code injection attacks. The CSP is not configurable at this time.

The CSP blocks the following external resources:

- Loading code (scripts and styles) from external domains
- Embedding apps in iframes from external domains

The CSP allows the following external resources:

- Images and media from HTTPS sources: Apps can load images and media files from any HTTPS URL, including
  external image hosting services and APIs that return images. This doesn’t require an external access integration.
- Fonts from HTTPS sources: Apps can load web fonts from any HTTPS URL, including external font hosting
  services such as Google Fonts. This doesn’t require an
  external access integration. For the Snowflake Native App Framework exception, see the following note.
- Data URIs and blob URLs: Apps can use embedded data (data URIs) and dynamically generated content (blob URLs)
  for images and media. This supports features like displaying charts, diagrams, or user-uploaded content.
- Mapbox and Carto resources: A limited subset of resources from Mapbox and Carto are permitted to support
  mapping visualizations.

Note

- For warehouse runtimes that use conda to manage dependencies, you must accept the Anaconda terms to use Mapbox.
  For more information, see [Using third-party packages from Anaconda](/developer-guide/udf/python/udf-python-packages#label-python-udfs-anaconda-terms).
- Loading images or media from external domains is supported in Streamlit in Snowflake, but not in Snowflake Native App Framework.
- Loading fonts from external domains is supported in Streamlit in Snowflake, including embedded apps, but not in Snowflake Native App Framework.
  In Snowflake Native App Framework, fonts are restricted to the app’s own asset origin, the Snowflake font CDN, and data URIs.
- The CSP also blocks front-end calls that are generally considered unsafe, such as `eval()`.

This restrictive policy means that most third-party JavaScript libraries and custom components that rely on
external scripts won’t work in Streamlit apps. For more information about CSP limitations, see
[Loading external resources](/developer-guide/streamlit/limitations#label-streamlit-limitations-csp).

## Essential security setup

The following security configurations are essential for a secure and well-functioning Streamlit in Snowflake environment.

### Network access configuration

Configure network access to ensure that apps can communicate with Snowflake.

**For all deployments:**

- Add `*.snowflake.app` to your network allowlist to enable communication between Streamlit apps and Snowflake.
  If your account uses per-account URLs (enabled by setting
  [ENABLE\_PER\_ACCOUNT\_APP\_SERVICE\_URL](/sql-reference/parameters#label-enable-per-account-app-service-url) to `TRUE`),
  you can use the more specific APP\_SERVICE\_PUBLIC\_WILDCARD entry from [SYSTEM$ALLOWLIST](/sql-reference/functions/system_allowlist).
- For Streamlit apps using container runtimes on accounts where
  [ENABLE\_PER\_ACCOUNT\_APP\_SERVICE\_URL](/sql-reference/parameters#label-enable-per-account-app-service-url) is `FALSE`,
  also add `*.snowflakecomputing.app` to your network allowlist.
- Ensure WebSockets are not blocked in your network configuration.

For more information, see [You can’t load the Streamlit app](/developer-guide/streamlit/troubleshooting#label-streamlit-troubleshooting-allowlist).

**For private connectivity:**

If your organization requires private connectivity, configure AWS PrivateLink, Azure Private Link, or
Google Cloud Private Service Connect for both Snowflake access and Streamlit app access. For more information,
see [Private connectivity for Streamlit in Snowflake](/developer-guide/streamlit/object-management/privatelink).

### Role-based access control

Establish a role hierarchy for managing Streamlit apps.

**Recommended role structure:**

- Creator roles: Roles with CREATE STREAMLIT privileges on schemas where apps will be deployed.
- Viewer roles: Roles with USAGE privileges on apps for end users.

The following example shows how to create a role hierarchy for Streamlit apps:

Copy code

```
-- Create dedicated roles for Streamlit
CREATE ROLE streamlit_developer;
CREATE ROLE streamlit_viewer;

-- Grant hierarchy
GRANT ROLE streamlit_viewer TO ROLE streamlit_developer;

-- Grant privileges for app creation
GRANT USAGE ON DATABASE streamlit_db TO ROLE streamlit_developer;
GRANT USAGE ON SCHEMA streamlit_db.apps TO ROLE streamlit_developer;
GRANT CREATE STREAMLIT ON SCHEMA streamlit_db.apps TO ROLE streamlit_developer;
GRANT USAGE ON COMPUTE_POOL streamlit_compute_pool TO ROLE streamlit_developer;
GRANT USAGE ON INTEGRATION python_package_index TO ROLE streamlit_developer;

-- Grant privileges for app viewing
GRANT USAGE ON WAREHOUSE streamlit_wh TO ROLE streamlit_viewer;
GRANT USAGE ON DATABASE streamlit_db TO ROLE streamlit_viewer;
GRANT USAGE ON SCHEMA streamlit_db.apps TO ROLE streamlit_viewer;
GRANT USAGE ON STREAMLIT streamlit_db.apps.my_app TO ROLE streamlit_viewer;
```

The app developer also needs USAGE on `streamlit_wh`, but this is inherited from the
viewer role. For more information about required privileges, see [Privileges required to create and use a Streamlit app](/developer-guide/streamlit/object-management/privileges).

### Secrets management

Configure proper secrets management for apps that access external services or sensitive credentials:

1. Enable secrets access for apps by granting appropriate privileges:

   Copy code

   ```
   -- Grant privileges on secrets to app owner role
   GRANT READ ON SECRET my_secret TO ROLE streamlit_developer;
   GRANT USAGE ON INTEGRATION my_external_access_integration TO ROLE streamlit_developer;
   ```
2. For container runtime apps, create SQL functions to wrap secret access rather than embedding
   secrets in app code.

For more information, see [Manage secrets and configure your Streamlit app](/developer-guide/streamlit/app-development/secrets-and-configuration).

### Context functions and row-level security

In warehouse runtimes, if your apps use context functions (such as `CURRENT_USER()`) or access tables with row access policies,
grant the global READ SESSION privilege to app owner roles:

Copy code

```
USE ROLE ACCOUNTADMIN;
GRANT READ SESSION ON ACCOUNT TO ROLE streamlit_developer;
```

Note

Warehouse-runtime apps using `CURRENT_ROLE()` in row access policies will always return the app owner’s role, not
the viewer’s role, because apps run with owner’s rights by default.

For more information and examples, see [Row access policies in Streamlit in Snowflake](/developer-guide/streamlit/features/row-access).

In container runtimes, context functions on owner’s rights connections will return values from the owner role’s context
and so are not appropriate for user-targeted row access policies. However, restricted caller’s rights connections
return the viewer’s context. For more information, see [Restricted caller’s rights and Streamlit in Snowflake](/developer-guide/streamlit/features/restricted-callers-rights).

### Warehouse runtimes only: External offerings terms

Warehouse runtimes use conda to manage your app’s dependencies. If you want to use
Mapbox in your apps, you must acknowledge the
[External Offerings Terms](https://www.snowflake.com/legal/external-offering-terms/).

For information about using this package, see [Using third-party packages from Anaconda](/developer-guide/udf/python/udf-python-packages#label-python-udfs-anaconda-terms).

## Available security features

The following security features are available to enhance app security and governance.

### External access integrations

Control which external networks and services your apps can access:

- Create network rules to define allowed endpoints, including package indexes.
- Create external access integrations that reference network rules and authentication secrets.
- Assign external access integrations to Streamlit apps.

This prevents apps from making unauthorized outbound connections and provides audit trails for external access.

For more information, see [External network access in Streamlit in Snowflake](/developer-guide/streamlit/features/external-access).

### Git integration

Integrate Streamlit apps with Git repositories for version control and change tracking:

- Grant appropriate privileges on Git repository objects (READ, WRITE, or OWNERSHIP).
- Use Git integration to maintain audit trails of code changes.
- Implement code review processes before deploying changes to production apps.

For more information, see [Sync Streamlit in Snowflake apps with a Git repository](/developer-guide/streamlit/features/git-integration).

### Private connectivity

For organizations with strict network security requirements, configure private connectivity to ensure all
Streamlit traffic remains within your private network. Streamlit in Snowflake supports the following private connectivity options:

- [AWS PrivateLink](/user-guide/admin-security-privatelink)
- [Azure Private Link](/user-guide/privatelink-azure)
- [Google Cloud Private Service Connect](/user-guide/private-service-connect-google)

Private connectivity eliminates exposure to the public internet and provides additional network isolation.

For more information, see [Private connectivity for Streamlit in Snowflake](/developer-guide/streamlit/object-management/privatelink).

### Logging and tracing

Enable logging to monitor app behavior and troubleshoot issues:

- Configure an event table for your account. For more information, see [Event table overview](/developer-guide/logging-tracing/event-table-setting-up).
- For warehouse runtimes, set appropriate log and trace levels for databases containing Streamlit apps.
  For more information, see [Setting levels for logging, metrics, and tracing](/developer-guide/logging-tracing/telemetry-levels).
- Review logs regularly for security events, errors, and unusual behavior.

For container runtimes, Snowflake automatically captures standard output and standard error
from the container and stores them in the account’s event table. No additional configuration is needed.

For more information, see [Logging and tracing for Streamlit in Snowflake](/developer-guide/streamlit/features/logging-tracing).

### Limit a user’s access to only Streamlit in Snowflake

To restrict a user to only access Streamlit in Snowflake and prevent them from accessing other parts of Snowflake, an account
administrator can add a custom user property via SQL or SCIM attribute.

- To restrict a user, use the [ALTER USER](/sql-reference/sql/alter-user) SQL command to set the ALLOWED\_INTERFACES property
  to include STREAMLIT:

  Copy code

  ```
  ALTER USER <user_name> SET ALLOWED_INTERFACES = (STREAMLIT);
  ```

If you’re provisioning users with SCIM APIs, you can set the same setting using the custom attribute `allowedInterfaces`.
For more information about SCIM custom attributes, see [SCIM user API reference](/user-guide/scim-user-api-reference).

After Streamlit-only access is configured, the user can’t access any part of Snowflake except the Streamlit in Snowflake apps for which they have permission.
Additionally, they can only access the app-viewer URL for those apps. If a Streamlit-only user attempts to navigate anywhere in Snowflake,
including any app-builder URL, it results in an access control error.

### Redirect app viewers to your identity provider

An account administrator can configure all app-viewer URLs to redirect to your identity provider (IdP) when an unauthenticated viewer accesses an app.
This process eliminates a step from the user’s login flow.

- To redirect unauthenticated users from app-viewer URLs to your IdP, use the [ALTER ACCOUNT](/sql-reference/sql/alter-account) SQL command to set
  the LOGIN\_IDP\_REDIRECT account property to include STREAMLIT:

  Copy code

  ```
  ALTER ACCOUNT SET LOGIN_IDP_REDIRECT = (STREAMLIT = <your_security_integration>);
  ```

For a full overview of `LOGIN_IDP_REDIRECT`, including the procedure
for reaching the Snowflake sign-in page when the IdP is unavailable, see
[Automatically redirecting users to your identity provider](/user-guide/admin-security-fed-auth-idp-redirect).

For more information about configuring your Snowflake account to use an IdP, see the following topics:

- [Configuring SAML 2.0 federated authentication](/user-guide/admin-security-fed-auth-security-integration).
- [Configuring an identity provider (IdP) for Snowflake](/user-guide/admin-security-fed-auth-configure-idp).

## Best practices for administrators

The following best practices help maintain a secure Streamlit environment.

**Use dedicated roles and schemas:**

- Create separate schemas for development, testing, and production apps.
- Use different roles for each environment to prevent accidental changes to production apps.
- Grant production app ownership to service roles rather than individual user accounts.

**Implement least privilege access:**

- Grant only the minimum required privileges to each role.
- Regularly review and audit role memberships and privileges.
- Avoid granting ACCOUNTADMIN or other powerful roles to app owner roles unless absolutely necessary.

**Manage app lifecycle:**

- Establish processes for app approval and deployment.
- Require code reviews before promoting apps to production.
- Document which apps access sensitive data and require additional scrutiny.
- Regularly review and remove unused or deprecated apps.

**Monitor resource usage:**

- Set appropriate warehouse sizes for app workloads.
- Monitor compute costs and set up alerts for unusual usage patterns.
- For container runtimes, configure compute pools with appropriate MIN\_NODES and MAX\_NODES settings.
- Use separate warehouses for different app environments to isolate costs and resources.

For more information about resource management, see [Managing costs for Streamlit in Snowflake](/developer-guide/streamlit/object-management/billing) and
[Runtime environments for Streamlit apps](/developer-guide/streamlit/app-development/runtime-environments).

**Use secure app development practices:**

- Never embed credentials or API keys directly in app code.
- Use Snowflake secrets for storing sensitive information.
- Validate and sanitize user inputs to prevent SQL injection.
- Limit the data exposed through apps to only what viewers need to see.
- Test apps thoroughly before sharing with wider audiences.

For more information about owner’s rights security considerations, see [Owner’s rights and app security](/developer-guide/streamlit/object-management/owners-rights#label-streamlit-owners-rights-security).

**Perform regular security audits:**

- Review which roles have CREATE STREAMLIT privileges.
- Audit which apps access which data sources.
- Review external access integrations and network rules.
- Check for apps owned by former employees or inactive accounts.
- Review Git repository access and commit history.

Use the following queries to audit your Streamlit apps:

Copy code

```
-- List all Streamlit apps and their owners
SHOW STREAMLITS;

-- Check privileges on a specific app
SHOW GRANTS ON STREAMLIT streamlit_db.apps.my_app;

-- List all roles with CREATE STREAMLIT privileges
SHOW GRANTS OF CREATE STREAMLIT;
```

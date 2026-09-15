# ALTER ACCOUNT

Modifies an account. The ALTER ACCOUNT command has two purposes:

- Allows account administrators (that is, users with the ACCOUNTADMIN role) to modify [parameters](/sql-reference/parameters) and
  other settings at the account level. For example, the account administrator can set the resource monitor or enable a security feature for
  an account. For these actions, the account administrator executes ALTER ACCOUNT from the account being modified.
- Allows [organization administrators](/user-guide/organization-administrators) to modify core characteristics of an account. For example, the
  organization administrator can rename an account. For these actions, the organization administrator executes ALTER ACCOUNT from a
  different account than the one being modified.

Note

While ALTER ACCOUNT is primarily executed by account administrators and organization administrators, users with the SECURITYADMIN
role can use it to set the network policy for the account.

## Syntax

The syntax for ALTER ACCOUNT varies depending on whether you are modifying the [current account](#label-alter-account-current) or a [different account](#label-alter-account-different).

### Altering the current account

Copy code

```
ALTER ACCOUNT SET { [ accountProperties ] | [ accountParams ] | [ objectParams ] | [ sessionParams ] }

ALTER ACCOUNT UNSET <param_name> [ , ... ]

ALTER ACCOUNT SET RESOURCE_MONITOR = <monitor_name>

ALTER ACCOUNT ADD ORGANIZATION USER GROUP <group_name>
ALTER ACCOUNT REMOVE ORGANIZATION USER GROUP <group_name>

ALTER ACCOUNT SET { AUTHENTICATION | SESSION } POLICY <policy_name> [ { FOR ALL PERSON USERS | FOR ALL SERVICE USERS } ] [ FORCE ]

ALTER ACCOUNT UNSET { AUTHENTICATION | SESSION } POLICY [ { FOR ALL PERSON USERS | FOR ALL SERVICE USERS } ]

ALTER ACCOUNT SET FEATURE POLICY <policy_name> FOR ALL APPLICATIONS [ FORCE ]

ALTER ACCOUNT UNSET FEATURE POLICY FOR ALL APPLICATIONS

ALTER ACCOUNT SET FEATURE POLICY <policy_name> FOR ALL DATABASES [ FORCE ]

ALTER ACCOUNT UNSET FEATURE POLICY FOR ALL DATABASES

ALTER ACCOUNT SET FEATURE POLICY <policy_name> FOR ALL PERSONAL DATABASES [ FORCE ]

ALTER ACCOUNT UNSET FEATURE POLICY FOR ALL PERSONAL DATABASES

ALTER ACCOUNT SET MAINTENANCE POLICY <policy_name> [ FORCE ] FOR ALL APPLICATIONS

ALTER ACCOUNT UNSET MAINTENANCE POLICY FOR ALL APPLICATIONS

ALTER ACCOUNT SET DATA MOVEMENT POLICY <policy_name> [ FORCE ]

ALTER ACCOUNT UNSET DATA MOVEMENT POLICY

ALTER ACCOUNT SET { PACKAGES | PASSWORD | MULTI PARTY APPROVAL } POLICY <policy_name> [ FORCE ]

ALTER ACCOUNT UNSET { PACKAGES | PASSWORD | MULTI PARTY APPROVAL } POLICY

ALTER ACCOUNT SET CONTACT <purpose> = <contact_name> [ , <purpose> = <contact_name> ... ]

ALTER ACCOUNT UNSET CONTACT <purpose>

ALTER ACCOUNT SET TAG <tag_name> = '<tag_value>' [ , <tag_name> = '<tag_value>' ... ]

ALTER ACCOUNT UNSET TAG <tag_name> [ , <tag_name> ... ]
```

Where:

Copy code

```
accountProperties ::=
    LOGIN_IDP_REDIRECT = ( <interface> = <security_integration> [ , ... ] )
    OBJECT_VISIBILITY = { <object_visibility_spec> | PRIVILEGED }
```

Copy code

```
accountParams ::=
  ALLOW_ID_TOKEN = TRUE | FALSE
  ALLOWED_SPCS_WORKLOAD_TYPES = { '<list_of_workload_types>' | 'ALL' }
  CLIENT_ENCRYPTION_KEY_SIZE = <integer>
  CORTEX_ENABLED_CROSS_REGION = { 'DISABLED' | 'ANY_REGION' | '<list_of_regions>' }
  DISALLOWED_SPCS_WORKLOAD_TYPES = { '<list_of_workload_types>' | 'ALL' }
  DISABLE_USER_PRIVILEGE_GRANTS = TRUE | FALSE
  DEFAULT_DBT_VERSION = { '<version>' }
  ENABLE_EGRESS_COST_OPTIMIZER = TRUE | FALSE
  ENABLE_INTERNAL_STAGES_PRIVATELINK = TRUE | FALSE
  ENABLE_SNOWFLAKE_MANAGED_STORAGE_VOLUME_PRIVATELINK = TRUE | FALSE
  ENFORCE_NETWORK_RULES_FOR_INTERNAL_STAGES = TRUE | FALSE
  ENFORCE_NETWORK_RULES_FOR_SNOWFLAKE_MANAGED_STORAGE_VOLUME = TRUE | FALSE
  ENFORCE_TAG_PROPAGATION_FOR_DATA_MOVEMENT_POLICIES = TRUE | FALSE
  ENABLE_NOTEBOOK_CREATION_IN_PERSONAL_DB = TRUE | FALSE
  ENABLE_SPCS_BLOCK_STORAGE_SNOWFLAKE_FULL_ENCRYPTION_ENFORCEMENT = TRUE | FALSE
  EXTERNAL_OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST = TRUE | FALSE
  INITIAL_REPLICATION_SIZE_LIMIT_IN_TB = <num>
  LISTING_AUTO_FULFILLMENT_INITIAL_REFRESH_SIZE_LIMIT_IN_TB = <num>
  LISTING_AUTO_FULFILLMENT_REPLICATION_REFRESH_SCHEDULE = <schedule>
  LLM_INFERENCE_PARSE_DOCUMENT_PRESIGNED_URL_EXPIRY_SECONDS = <integer>
  NETWORK_POLICY = <string>
  OAUTH_ADD_PRIVILEGED_ROLES_TO_BLOCKED_LIST = TRUE | FALSE
  PERIODIC_DATA_REKEYING = TRUE | FALSE
  READ_CONSISTENCY_MODE = 'SESSION' | 'GLOBAL'
  REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_CREATION = TRUE | FALSE
  REQUIRE_STORAGE_INTEGRATION_FOR_STAGE_OPERATION = TRUE | FALSE
  SAML_IDENTITY_PROVIDER = <json_object>
  SQL_TRACE_QUERY_TEXT = ON | OFF
  SSO_LOGIN_PAGE = TRUE | FALSE
  USE_WORKSPACES_FOR_SQL = { 'always' | 'never' }
```

Copy code

```
objectParams ::=
  BASE_LOCATION_PREFIX = '<string>'
  CATALOG = <catalog_integration_name>
  CATALOG_SYNC = '<snowflake_open_catalog_integration_name>'
  CORTEX_MODELS_ALLOWLIST = {'<list_of_models>' | 'ALL' | 'NONE'}
  DATA_RETENTION_TIME_IN_DAYS = <integer>
  DEFAULT_DDL_COLLATION = '<collation_specification>'
  DEFAULT_NOTEBOOK_COMPUTE_POOL_CPU = <compute_pool_name>
  DEFAULT_NOTEBOOK_COMPUTE_POOL_GPU = <compute_pool_name>
  DEFAULT_STREAMLIT_COMPUTE_POOL = <compute_pool_name>
  DEFAULT_STREAMLIT_NOTEBOOK_WAREHOUSE = <warehouse_name>
  ENABLE_DATA_COMPACTION = { TRUE | FALSE }
  ICEBERG_MERGE_ON_READ_BEHAVIOR = { 'AUTO' | 'ENABLED' | 'DISABLED' }
  ENABLE_ICEBERG_MERGE_ON_READ = { TRUE | FALSE }
  ENABLE_TAG_PROPAGATION_EVENT_LOGGING = TRUE | FALSE
  ENABLE_UNREDACTED_QUERY_SYNTAX_ERROR = TRUE | FALSE
  ENABLE_UNREDACTED_SECURE_OBJECT_ERROR = TRUE | FALSE
  EVENT_TABLE = <string>
  EXTERNAL_VOLUME = <external_volume_name>
  ICEBERG_DEFAULT_DDL_COLLATION = '<collation_specification>'
  ICEBERG_VERSION_DEFAULT = <integer>
  LOG_LEVEL = <string>
  MAX_CONCURRENCY_LEVEL = <num>
  MAX_DATA_EXTENSION_TIME_IN_DAYS = <integer>
  METRIC_LEVEL = <string>
  NETWORK_POLICY = <string>
  OAUTH_AUTHORIZATION_SERVER = <integration_name>
  OAUTH_SCOPES_SUPPORTED = '<comma_separated_scopes>'
  PIPE_EXECUTION_PAUSED = TRUE | FALSE
  PREVENT_UNLOAD_TO_INLINE_URL = TRUE | FALSE
  PREVENT_UNLOAD_TO_INTERNAL_STAGES = TRUE | FALSE
  REPLACE_INVALID_CHARACTERS = TRUE | FALSE
  STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = <num>
  STATEMENT_TIMEOUT_IN_SECONDS = <num>
  STORAGE_SERIALIZATION_POLICY = COMPATIBLE | OPTIMIZED
  TRACE_LEVEL = <string>
```

Copy code

```
sessionParams ::=
  ABORT_DETACHED_QUERY = TRUE | FALSE
  AUTOCOMMIT = TRUE | FALSE
  BINARY_INPUT_FORMAT = <string>
  BINARY_OUTPUT_FORMAT = <string>
  DATE_INPUT_FORMAT = <string>
  DATE_OUTPUT_FORMAT = <string>
  DEFAULT_NULL_ORDERING = <string>
  ENABLE_GET_DDL_USE_DATA_TYPE_ALIAS = TRUE | FALSE
  ERROR_ON_NONDETERMINISTIC_MERGE = TRUE | FALSE
  ERROR_ON_NONDETERMINISTIC_UPDATE = TRUE | FALSE
  JSON_INDENT = <num>
  LOCK_TIMEOUT = <num>
  OPT_OUT_ERROR_LOGGING = TRUE | FALSE
  QUERY_TAG = <string>
  ROWS_PER_RESULTSET = <num>
  S3_STAGE_VPCE_DNS_NAME = <string>
  SEARCH_PATH = <string>
  SIMULATED_DATA_SHARING_CONSUMER = <string>
  STATEMENT_TIMEOUT_IN_SECONDS = <num>
  STRICT_JSON_OUTPUT = TRUE | FALSE
  TIMESTAMP_DAY_IS_ALWAYS_24H = TRUE | FALSE
  TIMESTAMP_INPUT_FORMAT = <string>
  TIMESTAMP_LTZ_OUTPUT_FORMAT = <string>
  TIMESTAMP_NTZ_OUTPUT_FORMAT = <string>
  TIMESTAMP_OUTPUT_FORMAT = <string>
  TIMESTAMP_TYPE_MAPPING = <string>
  TIMESTAMP_TZ_OUTPUT_FORMAT = <string>
  TIMEZONE = <string>
  TIME_INPUT_FORMAT = <string>
  TIME_OUTPUT_FORMAT = <string>
  TRANSACTION_DEFAULT_ISOLATION_LEVEL = <string>
  TWO_DIGIT_CENTURY_START = <num>
  UNSUPPORTED_DDL_ACTION = <string>
  USE_CACHED_RESULT = TRUE | FALSE
  WEEK_OF_YEAR_POLICY = <num>
  WEEK_START = <num>
```

Note

For readability, the complete list of session parameters that can be set for an account is not included here. For a complete list of all session
parameters, with their descriptions, as well as account and object parameters, see [Parameters](/sql-reference/parameters).

### Altering a different account

Copy code

```
ALTER ACCOUNT <name> SET IS_ORG_ADMIN = { TRUE | FALSE }

ALTER ACCOUNT <name> SET EDITION = { 'STANDARD' | 'ENTERPRISE' | 'BUSINESS_CRITICAL' }

ALTER ACCOUNT <name> SET TENANT_TYPE = { INTERNAL | EXTERNAL }

ALTER ACCOUNT <name> SET DOMAIN_NAMES = ( '<domain>' [ , '<domain>' , ... ] )

ALTER ACCOUNT <name> UNSET DOMAIN_NAMES

ALTER ACCOUNT <name> RENAME TO <new_name> [ SAVE_OLD_URL = { TRUE | FALSE } ]

ALTER ACCOUNT <name> DROP OLD URL

ALTER ACCOUNT <name> DROP OLD ORGANIZATION URL
```

## Account properties

You can set the following properties for the current account.

`SET property`
:   Specifies a property to set for your account:

> `LOGIN_IDP_REDIRECT = ( interface = security_integration [ , ... ] )`
> :   Maps Snowflake interfaces to
>     [SAML2 security integrations](/user-guide/admin-security-fed-auth-security-integration)
>     so that users who access the mapped interfaces are automatically redirected to the third-party identity provider (IdP) for SSO and
>     don’t see the Snowflake sign-in page.
>
>     Supported interface keys are `DEFAULT`, `SNOWFLAKE_INTELLIGENCE`, `STREAMLIT`, and `SPCS`. To opt a specific interface out of
>     the redirect, set that interface to `NULL`.
>
>     For per-interface descriptions, the precedence model, configuration examples, the view-only `LOGIN_IDP_REDIRECT` parameter, and the
>     recovery procedure for reaching the Snowflake sign-in page when the IdP is unavailable, see
>     [Automatically redirecting users to your identity provider](/user-guide/admin-security-fed-auth-idp-redirect).
>
>     Default: Empty list `( )`
>
> `OBJECT_VISIBILITY = { object_visibility_spec | PRIVILEGED }`
> > [![Snowflake logo in black (no text)](/static/images/logo-snowflake-black.png)](/static/images/logo-snowflake-black.png) [Preview Feature](/release-notes/preview-features) — Open
> >
> > Available to all accounts.
> >
> > Specifies the visibility of objects in the account, which controls the [discoverability of the objects](/user-guide/ui-snowsight/object-visibility-universal-search)
> > and enables users without explicit access privileges to find objects and request access.
> >
> > - A YAML specification describing the visibility in one of the following formats:
> >
> >   Copy code
> >
> >   ```
> >   $$
> >   organization_targets:
> >     - all_accounts_including_external
> >   $$
> >   ```
> >
> >   Or
> >
> >   Copy code
> >
> >   ```
> >   $$
> >   organization_targets:
> >     - account: <account_name_1>
> >     - account: <account_name_2>
> >     - ...
> >     - organization_user_group: <org_user_group_1>
> >     - organization_user_group: <org_user_group_2>
> >   $$
> >   ```
> >
> >   In the syntax above:
> >
> >   - `all_accounts_including_external`: Specifies that all users in all accounts in the organization can see the object. This includes
> >     all accounts within the organization, even those to which external parties may have been given access, such as
> >     [reader accounts](/user-guide/data-sharing-reader-create).
> >   - `account: account_name`: Specifies that all users in the specified account can see the object. You can specify multiple accounts.
> >     Note that `account` is the account name, not the account locator. You must specify only the account name, excluding the organization name.09-22
> >   - `organization_user_group: org_user_group`: Specifies that the specified [organization user group](/user-guide/organization-users#label-org-users-groups) can
> >     see the object in all accounts in the organization where the [organization user group has been imported](/user-guide/organization-users#label-org-users-add).
> > - `PRIVILEGED`: Specifies that only roles within the current account that are granted an explicit privilege on the object can see the object.
> >   This is the default behavior in Snowflake.
> >
> > For examples, see [Make database objects discoverable in Universal Search](/user-guide/ui-snowsight/object-visibility-universal-search#label-object-visibility-examples).
> >
> > Default: `'PRIVILEGED'`

`UNSET property`
:   Reverts the specified account property to its default.

## Parameters for altering the current account

Use the following parameters when modifying the current account.

For more information about setting parameters at the account level, see [Parameter management](/user-guide/admin-account-management). For details about a particular parameter, see [Parameters](/sql-reference/parameters).

`SET ...`
:   Specifies one (or more) account, session, and object parameters, and object properties to set for your account (separated by blank spaces, commas, or new lines):

    - Account parameters cannot be changed by any other users.
    - Session and object parameters set at the account level serve only as defaults and can be changed by other users.

    For descriptions of the parameters you can set for your account, see [Parameters](/sql-reference/parameters).

`UNSET ...`
:   Specifies one (or more) account, session, and object parameters to unset for your account, which resets them to the system defaults.

    You can reset multiple properties with a single ALTER statement; however, each property must be separated by a comma. When resetting a
    property, specify only the name; specifying a value for the property will return an error.

`SET RESOURCE_MONITOR resource_monitor_name`
:   Special parameter that specifies the name of the resource monitor used to control all virtual warehouses created in the account.

    Important

    Setting a resource monitor at the account level does not impact any of the Snowflake-provided warehouses that Snowflake uses
    for Snowpipe, automatic reclustering, or materialized views. The credits consumed by these warehouses do not count towards the
    credit quota for an account-level resource monitor.

    For more details, see [Working with resource monitors](/user-guide/resource-monitors).

`ADD ORGANIZATION USER GROUP group_name`
:   Imports an [organization user group](/user-guide/organization-users#label-org-users-groups) into the account. Organization users in the group are added to the
    account as user objects.

`REMOVE ORGANIZATION USER GROUP group_name`
:   Removes an [organization user group](/user-guide/organization-users#label-org-users-groups) from the account.

`SET { AUTHENTICATION | SESSION } POLICY policy_name [ { FOR ALL PERSON USERS | FOR ALL SERVICE USERS } ] [ FORCE ]`
:   Specifies the [authentication policy](/user-guide/authentication-policies) or
    [session policy](/user-guide/session-policies) for the account.

    The `FOR ALL PERSON USERS` clause applies the policy to users with their TYPE property set to NULL or PERSON.

    The `FOR ALL SERVICE USERS` clause applies the policy to users with their TYPE property set to SERVICE or
    LEGACY\_SERVICE.

    If you don’t specify `FOR ALL SERVICE USERS` or `FOR ALL PERSON USERS`, then the policy applies to all users in the account.

    If you explicitly set a policy on a specific user or a specific user type, then that policy takes precedence over a policy applied to `FOR ALL SERVICE USERS` or `FOR ALL PERSON USERS`.

    If you specify FORCE, then policies you set on specific users or specific user types are overridden. You can use
    this if you don’t want to unset policies.

    If a policy is already set on the current account, you can use FORCE to set the policy without having to unset the
    existing policy first.

`SET FEATURE POLICY policy_name FOR ALL APPLICATIONS [ FORCE ]`
:   Specifies the feature policy to set for the account. If a feature policy
    is already set on the current account, you can use FORCE to set the feature policy
    without having to unset the feature policy first.

`UNSET FEATURE POLICY FOR ALL APPLICATIONS`
:   Unsets the feature policy for the account.

    If you already set a policy on the current account, then you can specify FORCE to set the policy without needing to unset an
    existing policy first.

`SET FEATURE POLICY policy_name FOR ALL DATABASES [ FORCE ]`
:   Specifies the feature policy to apply to all regular databases in the account. This policy
    also applies to personal databases as a fallback when no `FOR ALL PERSONAL DATABASES` policy
    is set. It does not apply to native apps (application instances or application packages). If
    a feature policy is already set for all databases, use `FORCE` to replace it without unsetting
    it first.

    For more information, see [Feature policies](/user-guide/feature-policies).

`UNSET FEATURE POLICY FOR ALL DATABASES`
:   Removes the feature policy that was applied to all databases in the account.

`SET FEATURE POLICY policy_name FOR ALL PERSONAL DATABASES [ FORCE ]`
:   Specifies the feature policy to apply to all personal databases in the account.
    Use this clause to restrict the object types that users can create in their
    [personal databases](/user-guide/personal-databases). For example, an account
    administrator can block the creation of
    [Snowflake App Runtime](/developer-guide/snowflake-app-runtime/about-snowflake-app-runtime)
    apps in personal databases by attaching a feature policy whose
    `BLOCKED_OBJECT_TYPES_FOR_CREATION` includes `APPLICATION_SERVICE` and
    `ARTIFACT_REPOSITORY`. If a feature policy is already set on personal
    databases, use `FORCE` to replace it without unsetting it first.

    For information about which entity types can be controlled in personal databases, see
    [Use feature policies with personal databases](/user-guide/personal-databases#label-personal-databases-feature-policies).

`UNSET FEATURE POLICY FOR ALL PERSONAL DATABASES`
:   Removes the feature policy that was applied to all personal databases in the account.

`SET MAINTENANCE POLICY policy_name [ FORCE ] FOR ALL APPLICATIONS`
:   Specifies the [maintenance policy](/developer-guide/native-apps/consumer-maintenance-policies) to apply to all applications in the account. If a maintenance policy is already set on
    the account, you can use FORCE to set the maintenance policy without having to unset the
    maintenance policy first.

`UNSET MAINTENANCE POLICY FOR ALL APPLICATIONS`
:   Removes the maintenance policy from all applications in the account. When a maintenance policy is removed from all applications in an account,
    the account-level maintenance policy, if it exists, is applied.

`SET DATA MOVEMENT POLICY policy_name [ FORCE ]`
:   Specifies the [data movement policy](/user-guide/data-movement-policies) to apply as the account-level baseline. The
    account-level policy governs data movement operations on objects that aren’t covered by a tag-based policy.

    If a data movement policy is already set on the account, use FORCE to replace it without having to unset the existing
    policy first.

`UNSET DATA MOVEMENT POLICY`
:   Removes the data movement policy from the account.

`UNSET { AUTHENTICATION | SESSION } POLICY [ FOR ALL PERSON USERS | FOR ALL SERVICE USERS ]`
:   Unsets the [authentication policy](/user-guide/authentication-policies) or
    [session policy](/user-guide/session-policies) for the account.

    Specifying `FOR ALL SERVICE USERS` or `FOR ALL PERSON USERS` narrows the scope of the command; the policy is unset from the
    specified user type only instead of all users in the account.

`SET { PACKAGES | PASSWORD | MULTI PARTY APPROVAL } POLICY policy_name [ FORCE ]`
:   Specifies the [packages policy](/developer-guide/udf/python/packages-policy),
    [password policy](/user-guide/password-authentication#label-password-policies), or
    [Multi-party Approval policy](/user-guide/multi-party-approval) for the account.

    If you already set a policy on the current account, then you can specify FORCE to set the policy without needing to unset an
    existing policy first.

`UNSET { PACKAGES | PASSWORD | MULTI PARTY APPROVAL } POLICY`
:   Unsets the [packages policy](/developer-guide/udf/python/packages-policy),
    [password policy](/user-guide/password-authentication#label-password-policies), or
    [Multi-party Approval policy](/user-guide/multi-party-approval) for the account.

`SET CONTACT purpose = contact_name [ , purpose = contact_name ... ]`
:   Associates the account with one or more [contacts](/user-guide/contacts-using). For a list of valid purposes, see [Associate a contact with an object](/user-guide/contacts-using#label-contacts-associate).

`UNSET CONTACT {purpose}`
:   Removes the contact that was added to the account for the specified purpose.

`TAG tag_name = 'tag_value' [ , tag_name = 'tag_value' , ... ]`
:   Specifies the [tag](/user-guide/object-tagging/introduction) name and the tag string value.

    The tag value is always a string, and the maximum number of characters for the tag value is 256.

    For information about specifying tags in a statement, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota).

## Parameters for altering a different account

Use the following parameters when using the current account to modify a different account. Only
[organization administrators](/user-guide/organization-administrators) can use these parameters.
For `TENANT_TYPE` and `DOMAIN_NAMES`, you can also use a role that has been granted the
`MANAGE TENANTS` privilege.

`name`
:   Specifies the name of the account that is being modified.

`SET`
:   Specifies an account property to set for the account.

    `IS_ORG_ADMIN = { TRUE | FALSE }`
    :   Sets an account property that determines whether the ORGADMIN role is enabled in the account.

        Note

        Using the ORGADMIN role in a regular account is being phased out. Organization administrators should use the
        [organization account](/user-guide/organization-accounts) to complete organization-level tasks.

        To enable the ORGADMIN role for an account, specify `SET IS_ORG_ADMIN = TRUE`.

        You cannot set the property to `FALSE` from the current account. As a workaround, enable the role in a different account,
        and then switch to that account before executing the ALTER ACCOUNT command.

        By default, the ORGADMIN role can be enabled in a maximum of 8 accounts. If your organization requires more accounts with the ORGADMIN
        role, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

    `EDITION = { 'STANDARD' | 'ENTERPRISE' | 'BUSINESS_CRITICAL' }`
    :   Sets the [Snowflake edition](/user-guide/intro-editions) for the specified account.

        Only [organization administrators](/user-guide/organization-administrators) can change the edition of an account in the organization.
        Run the command from an account other than the account whose edition you’re changing.

        For upgrade and downgrade requirements, same-day downgrade restrictions, VPS Edition, and regional availability, see
        [Working with account editions](/user-guide/organizations-manage-accounts-editions).

        Managed accounts (sometimes referred to as parent accounts), including [reader accounts](/user-guide/data-sharing-reader-create) created by a provider account, cannot use this clause.
        To change the edition on a managed account, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

    `TENANT_TYPE = { INTERNAL | EXTERNAL }`
    :   Sets the tenant type for the specified account. `INTERNAL` identifies an account for your
        organization’s users. `EXTERNAL` identifies an account for a third-party tenant.

        `ACCOUNTADMIN` can’t set tenant type on the current account or on another account. Run this
        statement from the [organization account](/user-guide/organization-accounts) or an `ORGADMIN`
        role-enabled account, using the syntax for altering a different account.

        For tenant type concepts, privileges, and legal requirements when setting `EXTERNAL`, see
        [Third party (publisher–subscriber) accounts](/user-guide/third-party-publisher-subscriber-accounts).

    `DOMAIN_NAMES = ( 'domain' [ , 'domain' , ... ] )`
    :   Sets the allowlist of email domains for users of an external account. Provide domain names as a
        list of string literals.

        Each `ALTER ACCOUNT ... SET DOMAIN_NAMES` statement sets the full list and overrides any
        previously set account-level `DOMAIN_NAMES`. It does not append to an earlier list.

        Organization-level domain allowlists for internal accounts are set with [ALTER ORGANIZATION](/sql-reference/sql/alter-organization).

`UNSET DOMAIN_NAMES`
:   Clears the account-level allowlist of email domains for the specified account.

`RENAME TO new_name`
:   Changes the name of an account to the specified name.

    The new name should conform with all the [requirements for account identifiers](/user-guide/admin-account-identifier#label-note-requirements-account-id).

    Organization administrators cannot rename an account while they are logged in to it, so they must log in to a different account before
    executing the ALTER ACCOUNT command. If your organization consists of a single account that needs to be renamed, contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

    `SAVE_OLD_URL = { TRUE | FALSE }`
    :   Optional parameter used in conjunction with `RENAME TO` that preserves the [account URL](/user-guide/organizations-connect#label-connecting-via-url) used to
        access Snowflake prior to renaming. By default, Snowflake saves the original URL, which means you can access the account with either
        the old URL or the URL that contains the new account name. When set to `FALSE`, you must use the new URL to access the account.

        Default:
        :   TRUE

`DROP OLD URL`
:   Removes the original [account URL](/user-guide/organizations-connect#label-connecting-via-url) of an account that was renamed. Once the old URL is dropped, you must
    access the account with the URL that contains the new account name.

    If an account has an old account URL because it was moved to another organization, had its organization renamed, or was part of an
    organization that was merged, use the ALTER ACCOUNT … DROP OLD ORGANIZATION URL command instead.

[Preview Feature](/release-notes/preview-features) — Open

The `ALTER ACCOUNT ... DROP OLD ORGANIZATION URL` command is in preview, and is available to all accounts.

`DROP OLD ORGANIZATION URL`
:   Removes the original [account URL](/user-guide/organizations-connect#label-connecting-via-url) of an account after one of the following occurs:

    - Account moved to another organization.
    - Account had its organization renamed.
    - Account was part of an organization that was merged with another organization.

    If an account has an old account URL because the account, not the organization, was renamed, use the ALTER ACCOUNT … DROP OLD URL
    command instead.

## Usage notes

- Account parameters can be set only at the account level.
- Session and object parameters that are set using this command serve only as defaults:

  - User parameters can be overridden at the individual user level.
  - Session parameters can be overridden at the individual user and session level.
  - Object parameters can be overridden at the individual object level.
- Setting a resource monitor at the account level controls the credit usage for all virtual warehouses created in the account, but does not impact
  the credit usage for any of the Snowflake-provided warehouses. For more details, see [Working with resource monitors](/user-guide/resource-monitors).

- Regarding metadata:

  Attention

  Customers should ensure that no personal data (other than for a User object), sensitive data, export-controlled data, or other regulated data is entered as metadata when using the Snowflake service. For more information, see [Metadata fields in Snowflake](/sql-reference/metadata).
- Regarding the `OAUTH_AUTHORIZATION_SERVER` and `OAUTH_SCOPES_SUPPORTED` object parameters for MCP servers:

  - **Both parameters are optional.** When neither is set at any level, MCP servers use Snowflake OAuth and advertise
    `session:role:all` as the only supported scope.
  - **Configuration modes:**

    | `OAUTH_AUTHORIZATION_SERVER` | `OAUTH_SCOPES_SUPPORTED` | Behavior |
    | --- | --- | --- |
    | Not set | Not set | Snowflake OAuth; advertises `session:role:all`. |
    | Set | Not set | External identity provider (IdP) authorization. Advertises `session:role-any` if the bound integration has `EXTERNAL_OAUTH_ANY_ROLE_MODE = ENABLE` or `ENABLE_FOR_PRIVILEGE`; otherwise advertises an empty `scopes_supported` list. Doesn’t synthesize `session:role:all`. |
    | Not set | Set | Snowflake OAuth; advertises the configured scopes. |
    | Set | Set | External IdP authorization; advertises the configured scopes. |

    Expand

    Show lessSee more
  - **Lineage resolution:** Each parameter resolves independently. The effective value for an MCP server is
    the nearest non-NULL value in the account → database → schema inheritance chain. Setting one parameter
    does not affect the lineage resolution of the other.
  - For accepted scope values, see [OAUTH\_SCOPES\_SUPPORTED](/sql-reference/parameters#label-oauth-scopes-supported). For a complete workflow, see [Configure External OAuth authentication for MCP servers](/user-guide/snowflake-cortex/cortex-agents-mcp#label-cortex-mcp-external-oauth).

## Examples

Associate a network policy named `mypolicy` with your account:

> Copy code
>
> ```
> ALTER ACCOUNT SET NETWORK_POLICY = mypolicy;
> ```

Disable user privilege grants:

> Copy code
>
> ```
> ALTER ACCOUNT SET DISABLE_USER_PRIVILEGE_GRANTS = TRUE;
> ```

Bind an External OAuth security integration for MCP servers and advertise scopes:

> Copy code
>
> ```
> ALTER ACCOUNT SET OAUTH_AUTHORIZATION_SERVER = external_oauth_okta
>     OAUTH_SCOPES_SUPPORTED = 'session:role:ANALYST,session:role:DATA_ENGINEER';
> ```

Remove the network policy association from your account:

> Copy code
>
> ```
> ALTER ACCOUNT UNSET NETWORK_POLICY;
> ```

Set the packages policy at the account level.

> Copy code
>
> ```
> ALTER ACCOUNT SET PACKAGES POLICY packages_policy_prod_1 FORCE;
> ```
>
> Note
>
> If a packages policy is already set on the current account, you can use FORCE to set the packages policy without
> having to unset the packages policy first.

Unset the packages policy.

> Copy code
>
> ```
> ALTER ACCOUNT UNSET PACKAGES POLICY;
> ```

Change the Snowflake edition of another account in your organization to Enterprise Edition (organization administrator only):

> Copy code
>
> ```
> ALTER ACCOUNT acct_1 SET EDITION = 'ENTERPRISE';
> ```

Set the tenant type of another account to `EXTERNAL` (organization administrator or a role with
the `MANAGE TENANTS` privilege):

> Copy code
>
> ```
> ALTER ACCOUNT acct_1 SET TENANT_TYPE = EXTERNAL;
> ```

Set the allowlist of email domains for an external account:

> Copy code
>
> ```
> ALTER ACCOUNT acct_1 SET DOMAIN_NAMES = ('domain1.com','domain2.org');
> ```

Clear the account-level domain allowlist:

> Copy code
>
> ```
> ALTER ACCOUNT acct_1 UNSET DOMAIN_NAMES;
> ```

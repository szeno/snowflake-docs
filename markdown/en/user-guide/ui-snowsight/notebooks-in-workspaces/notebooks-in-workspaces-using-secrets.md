# Using secrets in Notebooks in Workspaces

Feature — Generally Available

Available to all AWS, Azure, and GCP commercial regions. PrivateLink is supported.

## Secret support in workspace notebooks

Snowflake notebooks running in Workspaces can use [secret objects](/sql-reference/sql/create-secret) together with external access integrations (EAIs)
so that credentials never appear as literals in notebook code. You configure secrets and EAIs in SQL (for example, in a worksheet); you then attach them to
the notebook service, scheduler, or [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle) call.

## Prerequisites: setting up secrets and external access

Before you can use secrets inside a Snowflake notebook, configure the underlying security objects and network rules. These steps are performed outside
of the notebook (for example, in a Snowflake worksheet).

### Documentation links

For detailed configuration options and security workflows, see:

- [CREATE SECRET](/sql-reference/sql/create-secret) (secret types, syntax, and examples)
- [External network access overview](/developer-guide/external-network-access/external-network-access-overview) (external access integrations and network rules)
- [SYSTEM$START\_OAUTH\_FLOW](/sql-reference/functions/system_start_oauth_flow) and [SYSTEM$FINISH\_OAUTH\_FLOW](/sql-reference/functions/system_finish_oauth_flow) (manual OAuth authorization flow)
- [External network access examples](/developer-guide/external-network-access/external-network-access-examples) (OAuth examples with EAIs)
- [Set up external access for Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-external-access) (notebook patterns for external APIs, including GitHub)

## Basic secret setup

To use existing secrets, run [SHOW SECRETS](/sql-reference/sql/show-secrets) (for example, `SHOW SECRETS IN ACCOUNT;`). To create a new secret,
use [CREATE SECRET](/sql-reference/sql/create-secret).

Note

Replace `SNOWPUBLIC` and `NOTEBOOKS` in the examples with your database and schema.

Copy code

```
-- Example: creating a GENERIC_STRING secret
CREATE OR REPLACE SECRET SNOWPUBLIC.NOTEBOOKS.MY_SECRET_STRING
  TYPE = GENERIC_STRING
  SECRET_STRING = 'your_api_key_here';
```

Other common secret types include:

- `PASSWORD`, which requires both `USERNAME` and `PASSWORD`.
- `OAUTH2`, used for integrations with external providers (for example, GitHub).

## External access integration (EAI)

To allow a notebook to use secrets when calling the public internet, connect a [network rule](/sql-reference/sql/create-network-rule) and an
[external access integration](/sql-reference/sql/create-external-access-integration).

Copy code

```
-- 1. Create a network rule to allow egress traffic
CREATE OR REPLACE NETWORK RULE my_api_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('api.example.com:443');

-- 2. Create the integration that bridges the rule and the secret
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION my_api_eai
  ALLOWED_NETWORK_RULES = (my_api_rule)
  ALLOWED_AUTHENTICATION_SECRETS = (SNOWPUBLIC.NOTEBOOKS.MY_SECRET_STRING)
  ENABLED = TRUE;
```

## Advanced authentication (OAuth)

For OAuth-based providers, create a [security integration](/sql-reference/sql/create-security-integration) and complete the
manual OAuth flow using [SYSTEM$START\_OAUTH\_FLOW](/sql-reference/functions/system_start_oauth_flow) (and [SYSTEM$FINISH\_OAUTH\_FLOW](/sql-reference/functions/system_finish_oauth_flow) in the same session).
That flow lets Snowflake exchange tokens with the external provider. For end-to-end examples, see [External network access examples](/developer-guide/external-network-access/external-network-access-examples)
and [Set up external access for Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-external-access).

## Notebook service integration with secrets

You can select secrets in the notebook **create**, **edit**, and **scheduler** dialogs.

1. In the navigation menu, select **Projects** » **Workspaces**.
2. Open **Notebooks**, then start **Create service** (or edit an existing service).
3. In **Service settings**, attach an external access integration and select one or more secrets from the drop-down. You can attach multiple secrets.
4. Verify the service starts successfully, then use Python cells to read secrets with the Snowpark secrets API or from the mount paths shown in the following examples.

Note

If the fully qualified secret name contains special characters (for example, `SNOWPUBLIC.NOTEBOOKS."my secret 1"`), Snowflake normalizes the path
used in Python and in the container. Hyphens, spaces, and similar characters in the secret **name** segment become underscores. Database and schema
segments are case-insensitive.

Example: `SNOWPUBLIC.NOTEBOOKS."my secret 1"` is exposed to Python helpers as `snowpublic/notebooks/my_secret_1` (adjust database and schema
to match where the secret is stored).

The secret files are mounted under `/secrets/` inside the Snowflake-provided container. For example, a generic string secret might appear at:

`/secrets/snowpublic/notebooks/my_secret_1/secret_string`

Replace `snowpublic` and `notebooks` with the database and schema that own your secrets. Database, schema, and secret name matching is case-insensitive.

The Snowpark library exposes different helpers for each secret type, as shown below.

### Calling GENERIC\_STRING secrets from a Python cell

Copy code

```
from snowflake.snowpark.secrets import get_generic_secret_string

secret_1 = get_generic_secret_string('snowpublic/notebooks/my_secret_1')
print(secret_1)

print('Reading from the container mount path:')
print(open('/secrets/snowpublic/notebooks/my_secret_1/secret_string').read())
```

### Calling PASSWORD secrets from a Python cell

Copy code

```
from snowflake.snowpark.secrets import get_username_password

creds = get_username_password('snowpublic/notebooks/my_password_secret')
print('Username: ', creds.username)
print('Password: ', creds.password)

print('Container mount path:')
print(open('/secrets/snowpublic/notebooks/my_password_secret/username').read())
print(open('/secrets/snowpublic/notebooks/my_password_secret/password').read())
```

### Calling OAUTH2 secrets from a Python cell

Copy code

```
from snowflake.snowpark.secrets import get_oauth_access_token

token = get_oauth_access_token('_/_/github_secret')
print(token)

print('Reading from the container mount path:')
print(open('/secrets/_/_/github_secret/access_token').read())
```

Replace `_/_/github_secret` with the normalized path for your OAuth2 secret (database/schema/name), following the same rules as above.

## Scheduling notebooks with secrets

When you schedule a notebook from Snowsight, add the EAIs and secrets the scheduled task should use in the scheduling dialog so the headless run
inherits the same external access and credentials as interactive development.

## Non-interactive runs with `EXECUTE CODE BUNDLE` and secrets

Headless runs need the external access integrations and secrets the notebook depends on. Define them in the `code_bundle.yml` specification of the
Code Bundle (formerly a Notebook Project Object), or inline in the `EXECUTE CODE BUNDLE` statement with a `WITH SPECIFICATION` clause. For full syntax,
see [EXECUTE CODE BUNDLE](/sql-reference/sql/execute-code-bundle).

Copy code

```
# code_bundle.yml
bundle:
  ...
  external_access_integrations:
    - <database_name>.<schema_name>.<integration_name>
  secrets:
    - <database_name>.<schema_name>.<secret_name>
```

Copy code

```
EXECUTE CODE BUNDLE "<database_name>"."<schema_name>"."<bundle_name>"
  ENTRYPOINT = 'notebook.ipynb'
  ARGUMENTS = ( '<arg>' [ , '<arg>' ... ] );
```

Replace the placeholders with the integrations and fully qualified secrets your notebook requires.

# Manage secrets and configure your Streamlit app

Streamlit apps often need to access sensitive information such as API keys, passwords, and other credentials. How you manage
secrets in your Streamlit app depends on the runtime environment you’re using. Streamlit in Snowflake provides secure, built-in mechanisms
for accessing secrets in both warehouse and container runtimes. For Streamlit configuration, each runtime has
different restrictions, too.

In the Streamlit library, apps use a `.streamlit/` directory to store configuration and secrets:

- `.streamlit/config.toml`: Customizes app settings such as theme, layout, and server behavior.
- `.streamlit/secrets.toml`: Stores sensitive information like API keys and credentials (in local development).

Streamlit in Snowflake supports these files with some limitations depending on your runtime environment. The following table
summarizes the support for these files in warehouse and container runtimes:

| Feature | Warehouse runtime | Container runtime |
| --- | --- | --- |
| `config.toml` support | Limited subset of configuration options | Broader subset of configuration options |
| `secrets.toml` support | Not supported | Supported, but only recommended for non-secret environment variables |

Expand

Show lessSee more

For `secrets.toml`, Streamlit in Snowflake provides a more secure, built-in secrets management system that is recommended
for managing sensitive information. The following sections describe how to use Snowflake secrets in your apps.

## Managing your connection to Snowflake

To manage your connection to Snowflake, you can use `st.connection("snowflake")`\_. This allows you to connect to Snowflake from both
your local development environment and your deployed app.

Copy code

```
import streamlit as st

conn = st.connection("snowflake")
session = conn.session()

session.sql("SELECT 1").collect()
```

In warehouse runtimes, you can also use Snowpark’s get\_active\_session() function to get the active session.

Copy code

```
import streamlit as st
from snowflake.snowpark.context import get_active_session

# ONLY IN WAREHOUSE RUNTIMES
session = get_active_session()
session.sql("SELECT 1").collect()
```

Important

`get_active_session()` isn’t thread-safe and can’t be used in container runtimes.

## Secrets in container runtimes

Feature — Generally Available

Not supported in government regions.

You can use [st.secrets](https://docs.streamlit.io/develop/api-reference/connections/st.secrets) to access Snowflake secrets in your container runtime Streamlit in Snowflake apps. This allows you to
securely store and retrieve sensitive information such as API keys, credentials, and other configuration values.
Just like Streamlit does for `.streamlit/secrets.toml` in local development, Streamlit in Snowflake populates
secrets to environment variables, too.

Note

Container runtimes don’t have access to the `_snowflake` module. If you are migrating an older
warehouse-runtime app that uses `_snowflake` secret functions, replace those calls with
[st.secrets](https://docs.streamlit.io/develop/api-reference/connections/st.secrets) as described in this section.

### Access a secret in a container runtime

1. Stage the following Python file in `@my_stage/app_folder/streamlit_app.py`. For information about staging files,
   see [Staging files using Snowsight](/user-guide/data-load-local-file-system-stage-ui).

   Copy code

   ```
   import streamlit as st

   secret_value = st.secrets["my_secret_name"]
   ```
2. Create a secret in your Snowflake account:

   Copy code

   ```
   CREATE OR REPLACE SECRET my_secret
     TYPE = GENERIC_STRING
     SECRET_STRING = 'my_secret_value';
   ```

   For more information, see [CREATE SECRET](/sql-reference/sql/create-secret).
3. Create an external access integration (EAI), and assign the secret to it:

   Copy code

   ```
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION my_eai
     ALLOWED_AUTHENTICATION_SECRETS = (my_secret)
     ENABLED = TRUE;
   ```
4. Create your Streamlit app to reference the secret using the SECRETS parameter:

   Copy code

   ```
   CREATE STREAMLIT my_container_app
     FROM '@my_stage/app_folder'
     MAIN_FILE = 'streamlit_app.py'
     RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
     COMPUTE_POOL = my_compute_pool
     QUERY_WAREHOUSE = my_warehouse
     EXTERNAL_ACCESS_INTEGRATIONS = (my_eai)
     SECRETS = ('my_secret_name' = my_secret);

   ALTER STREAMLIT my_container_app ADD LIVE VERSION FROM LAST;
   ```

   Note

   You must assign both the EAI and the secret to the Streamlit object.
   You can’t assign a secret to a Streamlit object by itself.

   Because the generic-string secret `my_secret` is associated to the string `"my_secret_name"` in the SECRETS parameter, you can access
   the secret in your Streamlit app code using `st.secrets["my_secret_name"]`.

### Supported secret types and environment variables

Container runtimes support generic string and basic authentication secrets. In addition to mapping
secrets to `st.secrets`, Streamlit in Snowflake also maps secrets to environment variables. Environment variable
names are case-sensitive. For basic authentication secrets, two environment variables are created:
one for the username (`_USERNAME` suffix), and one for the password (`_PASSWORD` suffix).

| Secret type | `st.secrets` access | Environment variable access |
| --- | --- | --- |
| Generic string | `st.secrets["my_secret_name"]` | `os.environ["my_secret_name"]` |
| Basic authentication (username) | `st.secrets["my_secret_name"]["username"]` | `os.environ["my_secret_name_USERNAME"]` |
| Basic authentication (password) | `st.secrets["my_secret_name"]["password"]` | `os.environ["my_secret_name_PASSWORD"]` |

Expand

Show lessSee more

Note

Cloud provider, symmetric key, and OAuth secret types aren’t currently supported.

#### Generic string secrets

Generic string secrets are stored as top-level keys in `st.secrets`:

Copy code

```
ALTER STREAMLIT my_container_app
  SET SECRETS = ('my_generic_secret_name' = my_generic_secret);
```

You can access the secret using dictionary or attribute notation:

Copy code

```
import streamlit as st

api_key = st.secrets["my_generic_secret_name"]
api_key = st.secrets.my_generic_secret_name
```

#### Basic authentication secrets

Basic authentication secrets are stored as dict-like objects with `"username"` and `"password"` attributes:

Copy code

```
ALTER STREAMLIT my_container_app
  SET SECRETS = ('my_basic_auth_secret_name' = my_basic_auth_secret);
```

You can access the secret using dictionary or attribute notation:

Copy code

```
import streamlit as st

username = st.secrets["my_basic_auth_secret_name"]["username"]
password = st.secrets["my_basic_auth_secret_name"]["password"]

username = st.secrets.my_basic_auth_secret_name.username
password = st.secrets.my_basic_auth_secret_name.password
```

### Secrets for authenticated package repositories

Secrets are automatically exposed as environment variables. In particular, this enables authentication
with private package repositories like JFrog Artifactory.

For most authenticated package repositories, use a basic authentication secret. The secret is automatically
converted to environment variables with `_USERNAME` and `_PASSWORD` suffixes. If you need a different
naming convention, use generic string secrets, and set the name of each environment variable manually. For more
information about the environment variables that uv uses, see
[Package indexes](https://docs.astral.sh/uv/concepts/indexes/#providing-credentials-directly)
in the uv documentation.

#### Example: Authenticate to a private JFrog Artifactory repository

1. Stage your app’s source files in `@my_stage/app_folder`. Your app’s source files must include a
   `pyproject.toml` file that configures the private package index in the `[[tool.uv.index]]` table:

   Copy code

   ```
   [[tool.uv.index]]
   name = "my_jfrog_repo"
   url = "https://my-org.jfrog.io/artifactory/api/pypi/pypi-local/simple"
   ```

   For more information about declaring your app’s dependencies in a `pyproject.toml` file,
   see [Manage dependencies for your Streamlit app](/developer-guide/streamlit/app-development/dependency-management).
2. Create a basic authentication secret with your JFrog credentials:

   Copy code

   ```
   CREATE OR REPLACE SECRET jfrog_creds
     TYPE = PASSWORD
     USERNAME = 'my_username'
     PASSWORD = 'my_api_token';
   ```
3. Create an external access integration for your private repository:

   Copy code

   ```
   CREATE OR REPLACE NETWORK RULE jfrog_network_rule
     TYPE = HOST_PORT
     MODE = EGRESS
     VALUE_LIST = ('my-org.jfrog.io');

   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION jfrog_eai
     ALLOWED_NETWORK_RULES = (jfrog_network_rule)
     ALLOWED_AUTHENTICATION_SECRETS = (jfrog_creds)
     ENABLED = TRUE;
   ```

   Note

   To avoid a DNS error, you might need to include the cloud provider for your repository
   in the network rule value list. For example, if your repository is on AWS, you might need
   the following value list in your network rule:

   Copy code

   ```
   VALUE_LIST = ('my-org.jfrog.io', '<jfrog-server-name>.s3.amazonaws.com');
   ```
4. Attach the EAI and secret to your Streamlit app:

   Copy code

   ```
   CREATE STREAMLIT my_app
     FROM '@my_stage/app_folder'
     MAIN_FILE = 'streamlit_app.py'
     RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
     COMPUTE_POOL = my_compute_pool
     QUERY_WAREHOUSE = my_warehouse
     EXTERNAL_ACCESS_INTEGRATIONS = (jfrog_eai)
     SECRETS = ('UV_INDEX_MY_JFROG_REPO' = jfrog_creds);

   ALTER STREAMLIT my_app ADD LIVE VERSION FROM LAST;
   ```

   Because the basic authentication secret `jfrog_creds` is associated to the string `"UV_INDEX_MY_JFROG_REPO"` in the
   SECRETS parameter, the runtime automatically injects the `UV_INDEX_MY_JFROG_REPO_USERNAME` and `UV_INDEX_MY_JFROG_REPO_PASSWORD` environment variables
   as required by uv.

### Precedence of a local `.streamlit/secrets.toml` file

You can combine Snowflake-managed secrets with a local `.streamlit/secrets.toml` file in your app’s source directory.
When both are present, the Streamlit library merges them. The locally defined `.streamlit/secrets.toml` file takes precedence over
the Snowflake-managed secrets.

Because `.streamlit/secrets.toml` is stored as plain text in your staged files, it is not a security best practice
to store actual secrets in it. Use Snowflake’s built-in secrets management for sensitive credentials. Use the locally defined
`.streamlit/secrets.toml` file to store non-sensitive configuration values or environment-specific settings.

### Remove or change your Streamlit app’s secrets

- To remove all secrets from a Streamlit in Snowflake app, use the UNSET SECRETS clause with [ALTER STREAMLIT](/sql-reference/sql/alter-streamlit):

  Copy code

  ```
  ALTER STREAMLIT my_database.my_schema.my_app
    UNSET SECRETS;
  ```

  This removes all secret associations from the Streamlit in Snowflake app. The underlying secret objects remain in your Snowflake account
  and can be reassigned later. To also remove any EAI associations, unset the EXTERNAL\_ACCESS\_INTEGRATIONS property, too.
- To update or modify which secrets are attached, use [ALTER STREAMLIT](/sql-reference/sql/alter-streamlit) with SET SECRETS:

  Copy code

  ```
  ALTER STREAMLIT my_database.my_schema.my_app
    SET SECRETS = ('new_secret' = my_new_secret);
  ```

### Example: Create a container-runtime Streamlit app with an authenticated external API

This example demonstrates creating a Streamlit in Snowflake app that calls an external API using a secret API key.

1. Stage the following Python file in `@my_stage/weather_app/streamlit_app.py`:

   Copy code

   ```
   import streamlit as st
   import requests

   api_key = st.secrets["weather_api_name"]

   response = requests.get(
    "https://api.weather.com/v1/current",
    headers={"Authorization": f"Bearer {api_key}"}
   )

   st.write(response.json())
   ```

   Because `requests` is a dependency of `streamlit`, it is included in the runtime base image. Therefore,
   the runtime automatically installs it, even if you don’t include a dependencies file or configure a package index.
2. Create the secret, network rule, and EAI:

   Copy code

   ```
   CREATE OR REPLACE SECRET weather_api_key
     TYPE = GENERIC_STRING
     SECRET_STRING = 'secret_value';

   CREATE OR REPLACE NETWORK RULE weather_api_rule
     TYPE = HOST_PORT
     MODE = EGRESS
     VALUE_LIST = ('api.weather.com');

   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION weather_eai
     ALLOWED_NETWORK_RULES = (weather_api_rule)
     ALLOWED_AUTHENTICATION_SECRETS = (weather_api_key)
     ENABLED = TRUE;
   ```
3. Create the Streamlit object:

   Copy code

   ```
   CREATE STREAMLIT weather_app
     FROM '@my_stage/weather_app'
     MAIN_FILE = 'streamlit_app.py'
     RUNTIME_NAME = 'SYSTEM$ST_CONTAINER_RUNTIME_PY3_11'
     COMPUTE_POOL = my_compute_pool
     QUERY_WAREHOUSE = my_warehouse
     EXTERNAL_ACCESS_INTEGRATIONS = (weather_eai)
     SECRETS = ('weather_api_name' = weather_api_key);

   ALTER STREAMLIT weather_app ADD LIVE VERSION FROM LAST;
   ```

### Calling a Cortex Agent in a container runtime

To call a Cortex Agent in a container-runtime app, read the session token from the
underlying Snowpark Container Services container and then use the `requests` library. This is the
recommended replacement for `_snowflake.send_snow_api_request()`.

Copy code

```
import requests
import json
import os

SNOWFLAKE_HOST = os.getenv("SNOWFLAKE_HOST")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
ANALYST_ENDPOINT = "/api/v2/cortex/analyst/message"
URL = "https://" + SNOWFLAKE_HOST + ANALYST_ENDPOINT

def get_token() -> str:
    """Read the oauth token embedded into SPCS container"""
    return open("/snowflake/session/token", "r").read()

def send_request(semantic_model_file, prompt):
    """Sends the prompt using the semantic model file """
    headers = {
        "Content-Type": "application/json",
        "accept": "application/json",
        "Authorization": f"Bearer {get_token()}",
        "X-Snowflake-Authorization-Token-Type": "OAUTH"
    }
    request_body = {
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
        "semantic_model_file": semantic_model_file,
    }
    return requests.post(URL, headers=headers, data=json.dumps(request_body))
```

## Secrets in warehouse runtimes

In warehouse runtimes, you can use the `_snowflake` module to access secrets directly in your Streamlit app code.
Warehouse runtimes inherit access to the `_snowflake` module from stored procedures, which allows you to retrieve
secrets that are referenced in the Streamlit object.

To use secrets in a warehouse runtime:

1. Create a secret object in Snowflake. For more information, see [CREATE SECRET](/sql-reference/sql/create-secret).

   Copy code

   ```
   CREATE OR REPLACE SECRET my_secret
     TYPE = GENERIC_STRING
     SECRET_STRING = 'my_secret_value';
   ```
2. Create an external access integration and assign the secret to it.

   Copy code

   ```
   CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION my_eai
     ALLOWED_AUTHENTICATION_SECRETS = (my_secret)
     ENABLED = TRUE;
   ```
3. Reference the secret in your Streamlit object using the SECRETS parameter:

   Copy code

   ```
   ALTER STREAMLIT my_warehouse_app
     SET EXTERNAL_ACCESS_INTEGRATIONS = (my_eai)
     SECRETS = ('my_secret_key' = my_secret);
   ```

   You must assign both the external access integration and the secret to the Streamlit object. You can’t assign a
   secret to a Streamlit object by itself.
4. In your Streamlit app code, import the `_snowflake` module and retrieve the secret:

   Copy code

   ```
   import streamlit as st
   import _snowflake

   # Retrieve an API key from a generic string secret
   my_secret = _snowflake.get_generic_secret_string('my_secret_key')
   ```

For more information about accessing secrets with the `_snowflake` module, see [Python API for Secret Access](/developer-guide/external-network-access/secret-api-reference#label-python-api-secret-access).

## Streamlit configuration

Streamlit apps can include a configuration file (`.streamlit/config.toml`). This file allows
you to customize various aspects of your app, such as the theme, layout, and behavior. The configuration
file is written in TOML format. For more information about available configuration options, see the
Streamlit documentation on [config.toml](https://docs.streamlit.io/develop/api-reference/configuration/config.toml).

Support for configuration options varies by runtime environment. Container runtimes generally provide
broader support for configuration options than warehouse runtimes, particularly for static serving.
The following table shows which configuration sections are supported in warehouse and container runtimes:

| Configuration section | Warehouse runtime | Container runtime |
| --- | --- | --- |
| `[global]` | Not supported | Limited support (`disableWidgetStateDuplicationWarning`) |
| `[logger]` | Not supported | Not supported |
| `[client]` | Not supported | Limited support (`showErrorDetails`, `showSidebarNavigation`) |
| `[runner]` | Not supported | Supported |
| `[server]` | Not supported | Not supported |
| `[browser]` | Not supported | Not supported |
| `[mapbox]` | Not supported | Supported (deprecated, use environment variables instead) |
| `[theme]` | Supported | Supported |
| `[theme.sidebar]` | Supported | Supported |
| `[secrets]` | Not supported | Supported (but only recommended for non-secret environment variables) |
| `[snowflake.sleep]` | Supported | Not applicable |

Expand

Show lessSee more

For information about using the `[snowflake.sleep]` section to configure sleep timers in warehouse runtimes, see
[Custom sleep timer for a Streamlit app](/developer-guide/streamlit/features/sleep-timer).

The following directory structure shows an example of a Streamlit app with a configuration file:

Copy code

```
source_directory/
├── .streamlit/
│   └── config.toml
├── pyproject.toml
├── streamlit_app.py
└── uv.lock
```

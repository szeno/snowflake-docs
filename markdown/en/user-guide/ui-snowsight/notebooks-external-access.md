# Set up external access for Snowflake Notebooks

When working with notebooks, you might need to call external services, which often require sensitive credentials such as API keys. To keep
sensitive information secure, you can use secrets managed within Snowflake instead of hardcoding credentials in your notebook.

[External access integrations (EAIs)](/developer-guide/external-network-access/external-network-access-overview) are configured using
network rules and can optionally use Snowflake secrets for authentication.

By default, Snowflake restricts network traffic from external endpoints. To access external endpoints, follow these steps:

1. Create a network rule.
2. Create an [external network access integration](/developer-guide/external-network-access/external-network-access-overview) that uses the rule.
3. Create a secret for authentication (if needed). Generic string secrets also require an EAI.
4. Associate the secret with the EAI.
5. Associate the EAI and secret with the notebook.

Note

EAIs and network rules must be created by an organization administrator. For required privileges, see [Access control requirements](/sql-reference/sql/create-external-access-integration#label-create-external-access-integration-privileges).

## Configure a notebook with external access and secrets

This end-to-end example shows how to configure a notebook to access the OpenAI API using a generic string secret.

Copy code

```
-- Step 1: Create a secret
CREATE SECRET openai_key
  TYPE = GENERIC_STRING
  SECRET_STRING = '<your-api-key>';

-- Step 2: Create a network rule
CREATE OR REPLACE NETWORK RULE openai_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = ('api.openai.com');

-- Step 3: Create an external access integration that uses the network rule and secret
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION openai_integration
  ALLOWED_NETWORK_RULES = (openai_rule)
  ALLOWED_AUTHENTICATION_SECRETS = (openai_key)
  ENABLED = true;

-- Step 4: Associate the integration and secret with the notebook
ALTER NOTEBOOK my_notebook
  SET EXTERNAL_ACCESS_INTEGRATIONS = (openai_integration),
    SECRETS = ('openai_key' = openai_key);
```

Note

Secrets must be associated with both the external access integration (EAI) and the notebook. If a secret is associated with only one, it will not be accessible from notebook code.

## Access the secret inside a notebook

- After associating the secret with the notebook, to access its value in notebook code, use the `st.secrets` object:

Copy code

```
import streamlit as st
api_key = st.secrets['openai_key']
```

## Additional EAI examples

These examples show how to set up external access for common data science and machine learning sites:

### EAI for PyPI

Copy code

```
CREATE OR REPLACE NETWORK RULE pypi_network_rule
MODE = EGRESS
TYPE = HOST_PORT
VALUE_LIST = ('pypi.org', 'pypi.python.org', 'pythonhosted.org', 'files.pythonhosted.org');

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION pypi_access_integration
ALLOWED_NETWORK_RULES = (pypi_network_rule)
ENABLED = true;
```

### EAI for Hugging Face

Copy code

```
CREATE OR REPLACE NETWORK RULE hf_network_rule
MODE = EGRESS
TYPE = HOST_PORT
VALUE_LIST = ('huggingface.co', 'cdn-lfs.huggingface.co');

CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION hf_access_integration
ALLOWED_NETWORK_RULES = (hf_network_rule)
ENABLED = true;
```

## Grant USAGE privileges to use external access integrations

- After you create the EAIs, grant the USAGE privilege on the integration to roles that will use them:

  Copy code

  ```
  GRANT USAGE ON INTEGRATION openai_integration TO ROLE my_notebook_role;
  ```

The role used to create the notebook must have USAGE on the EAI. Granting USAGE to the PUBLIC role will not work.

## Enable external access integrations in Snowsight

After you create and provision EAIs, restart the notebook session in order to see the access integrations you created in
the **External Access** pane.

To enable integrations using Snowsight:

1. In the navigation menu, select **Projects** » **Notebooks**.
2. Open your notebook.
3. Select the [![More actions for worksheet](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-vertical-ellipsis.png) icon at the top right of your notebook.
4. Select **Notebook settings**, and then select **External access**.
5. Toggle on the EAIs you want to enable for the notebook.

## Additional authentication examples

### OAuth access token

Copy code

```
CREATE OR REPLACE SECRET oauth_token
    TYPE = OAUTH2
    API_AUTHENTICATION = google_translate_oauth
    OAUTH_REFRESH_TOKEN = 'my-refresh-token';
```

Copy code

```
# Using the secret as part of an EAI
  ALTER NOTEBOOK google_translate_test
    SET EXTERNAL_ACCESS_INTEGRATIONS=(google_translate_integration)
      SECRETS = ('cred' = oauth_token);
```

### Secret type: GENERIC\_STRING

Use a `GENERIC_STRING` secret to store a single value, such as an API key or token.

Create the secret:

Copy code

```
CREATE SECRET sf_openai_key
  TYPE = GENERIC_STRING
  SECRET_STRING = '<string_literal>';

-- SQL: Associate the secret and EAI with the notebook
ALTER NOTEBOOK openai_test
  SET EXTERNAL_ACCESS_INTEGRATIONS = (openai_access_int),
    SECRETS = ('openai_key' = sf_openai_key);
```

For GENERIC\_STRING secrets, access them by dictionary or attribute style:

Copy code

```
import streamlit as st

# Access the string value directly
my_openai_key = st.secrets['openai_key']
# or using attribute access
my_openai_key = st.secrets.openai_key
```

### Secret type: PASSWORD (example: GitHub Basic Auth)

Use a `PASSWORD` secret to store a username and password pair. These are often required for basic authentication with external APIs.

In this example, the notebook accesses the GitHub REST API using a `PASSWORD` secret and an external access integration.

Create the secret:

Copy code

```
CREATE SECRET password_secret
  TYPE = PASSWORD
  USERNAME = 'my_user_name'
  PASSWORD = 'my_password';
```

Use the secret as part of an EAI:

Copy code

```
ALTER NOTEBOOK github_user_info
SET EXTERNAL_ACCESS_INTEGRATIONS = (github_access_int),
    SECRETS = ('cred' = password_secret);
```

Access the secret in your code:

Copy code

```
import streamlit as st
import requests
from requests.auth import HTTPBasicAuth

# Access credentials from the secret
username = st.secrets.cred.username
password = st.secrets.cred.password

# Make an authenticated request
response = requests.get(
    'https://api.github.com/user',
    auth=HTTPBasicAuth(username, password)
)

print(response.status_code)
print(response.json())
```

## Additional resources

- For detailed syntax, see [External network access overview](/developer-guide/external-network-access/external-network-access-overview).
- For details on using CREATE SECRET, see [Creating a secret to represent credentials](/developer-guide/external-network-access/creating-using-external-network-access#label-creating-using-external-access-integration-secret).
- For additional examples of EAIs, see [External network access examples](/developer-guide/external-network-access/external-network-access-examples) or
  [Setting up External Access for Snowflake Notebooks on Github](https://github.com/Snowflake-Labs/snowflake-demo-notebooks/blob/main/Access%20External%20Endpoints/Access%20External%20Endpoints.ipynb).

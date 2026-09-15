# Connect to Workday and query data from Snowflake

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Note

Workday Live Data Query for Snowflake is in Early Adopter (EA) for Workday and in Preview for Snowflake. To request access, contact your Workday account representative.

This topic describes how to create a Snowflake Notebook, install the Workday Python connector, configure credentials, and run queries against Workday data.

Complete [Set up Snowflake for Workday Live Data Query](/user-guide/data-integration/zero-copy/workday/snowflake-setup) before starting this topic.

## Step 1: Create a notebook

Create a new Python notebook in a Snowflake Workspace. All LDQ connection and query code runs here.

1. In Snowsight, navigate to **Workspaces**.
2. Open an existing workspace or click **+ Workspace** to create one.
3. Inside the workspace, click **+** > **Notebook**.

## Step 2: Attach the external access integration

The notebook needs explicit permission to make outbound calls to Workday. Attach the `WORKDAY_LDQ_TEST_EAI` integration created in [Set up Snowflake for Workday Live Data Query](/user-guide/data-integration/zero-copy/workday/snowflake-setup).

1. Open your notebook.
2. Click the dropdown arrow next to **Connected** at the top of the notebook.
3. In the service details panel, check **Enabled External Access Integrations (EAIs)**. If `WORKDAY_LDQ_TEST_EAI` isn’t listed, click **Manage service** to add it. If you don’t see it there either, click **+ Create new service** to create a new service and attach the EAI.
4. Restart the notebook session if prompted.

Important

Without the EAI attached, all outbound HTTP calls to Workday will fail with a network error.

## Step 3: Install the Python connector

Install the `workday_ldq` package from your stage into the notebook’s runtime environment. This makes the `DataServiceConfig` and `create_connection` APIs available.

The installation is per-session and must be re-run after each notebook restart. The connector’s dependencies (for example, `trino`, `requests`, `lz4`) aren’t bundled: `pip` downloads them from PyPI automatically, which is why the network rule includes `pypi.org` and `files.pythonhosted.org`.

In the **first cell** of your notebook, run:

Copy code

```
import sys
import subprocess

from snowflake.snowpark.context import get_active_session

session = get_active_session()

# Replace with the correct wheel filename
session.file.get(
    "@WORKDAY_LDQ_TEST.LIVEDATA.LDQ_STAGE/ldq_python_client-1.0.3-py3-none-any.whl",
    "/tmp"
)

subprocess.check_call([
    sys.executable, "-m", "pip", "install",
    "/tmp/ldq_python_client-1.0.3-py3-none-any.whl",
    "--quiet"
])

print("Wheel installed successfully!")
```

Important

The wheel doesn’t persist across notebook restarts. Re-run this cell every time you restart or reconnect the notebook. Keep it as the very first cell so it always runs first.

## Step 4: Configure credentials

The connector accepts credentials as an in-memory dictionary via `DataServiceConfig()`. The private key is retrieved at runtime from a Snowflake Secret using a temporary UDF. The key is never written to disk or persisted in the notebook.

In a notebook cell, run:

Copy code

```
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import udf
from workday_ldq import DataServiceConfig

session = get_active_session()
session.sql("USE DATABASE WORKDAY_LDQ_TEST").collect()
session.sql("USE SCHEMA LIVEDATA").collect()

@udf(
    name="get_secret_temp",
    is_permanent=False,
    replace=True,
    external_access_integrations=["WORKDAY_LDQ_TEST_EAI"],
    secrets={"pk": "WORKDAY_LDQ_TEST.LIVEDATA.WORKDAY_PRIVATE_KEY"}
)
def get_secret_temp() -> str:
    import _snowflake
    return _snowflake.get_generic_secret_string("pk")

private_key_pem = session.sql("SELECT get_secret_temp()").collect()[0][0]

config = DataServiceConfig({
    "wd.authn.clientId":            "<your_client_id>",
    "wd.authn.isu":                 "<your_isu_username>",
    "wd.authn.accessTokenEndpoint": "https://<host>/ccx/oauth2/<tenant>/token",
    "wd.authn.privateKey":          private_key_pem,
    "wd.host":                      "<your_workday_host>",
    "wd.port":                      "443"
})

del private_key_pem
session.sql("DROP FUNCTION IF EXISTS get_secret_temp()").collect()
print("Config created successfully!")
```

Replace the placeholder values with those provided by your Workday administrator.

| Property | Description |
| --- | --- |
| `wd.authn.clientId` | Client ID from the Workday Register API Client task. |
| `wd.authn.isu` | ISU username (for example, `snowflake_ldq_user`). |
| `wd.authn.accessTokenEndpoint` | Full OAuth2 token URL in the format `https://<host>/ccx/oauth2/<tenant>/token`. |
| `wd.authn.privateKey` | PEM private key content, retrieved securely from a Snowflake Secret at runtime. |
| `wd.host` | Workday service host. |
| `wd.port` | Always `443`. |

Expand

Show lessSee more

Note

Workspace notebooks can’t directly access Snowflake Secrets via `_snowflake` or `st.secrets`. The temporary UDF runs inside the Snowflake execution environment (where `_snowflake` is available), retrieves the secret, and returns it to the notebook session. The UDF is dropped immediately after use, and the private key is cleared from memory with `del`. The key is never written to disk.

Note

If your Snowflake environment routes traffic through a proxy, set `wd.host` to `<proxy_host>` and update `wd.authn.accessTokenEndpoint` to point to the proxy’s token endpoint.

## Step 5: Connect and run queries

### Connect to the Workday LDQ service

Open a connection using the `config` object. A successful connection confirms that authentication, networking, and configuration are all correct.

Copy code

```
from workday_ldq import create_connection

connection = create_connection(config)
print("Connected successfully!")
```

### Run a query

Use a cursor to send SQL to the Workday data service. Queries run against Workday’s Unified Data Catalog, not Snowflake tables.

Copy code

```
cursor = connection.cursor()
cursor.execute("SELECT COUNT(*) FROM workday_core.public.worker")
results = cursor.fetchall()
print(results)
cursor.close()
```

### Load results into a DataFrame

Copy code

```
import pandas as pd

cursor = connection.cursor()
cursor.execute("SELECT * FROM workday_core.public.worker LIMIT 100")

columns = [desc[0] for desc in cursor.description]
rows    = cursor.fetchall()
df      = pd.DataFrame(rows, columns=columns)
cursor.close()

df.head()
```

### Close the connection

Always close the connection when you’re finished to release resources on both the Snowflake and Workday sides.

Copy code

```
connection.close()
```

## Sample queries

Note

These queries target Workday data, not Snowflake tables, and must be run through the LDQ connector. Paste each query string into a `cursor.execute()` call as shown above, not directly in a Snowflake Worksheet.

The examples below use `workday_core.public` as the catalog and schema. Your environment may use different names. Always run the discovery queries first to confirm what’s available in your tenant.

### Discover available catalogs and schemas

Copy code

```
SHOW CATALOGS
```

Copy code

```
SHOW SCHEMAS IN workday_core
```

Copy code

```
SHOW TABLES IN workday_core.public
```

### Count all workers

Copy code

```
SELECT COUNT(*) AS total_workers
FROM workday_core.public.worker
```

### List active workers with job titles

Copy code

```
SELECT
    w.worker_id,
    w.full_name,
    w.employee_type,
    jp.job_title
FROM workday_core.public.worker w
JOIN workday_core.public.job_profile jp
    ON w.job_profile_id = jp.job_profile_id
WHERE w.active = TRUE
LIMIT 50
```

### Headcount by management level

Copy code

```
SELECT
    management_level,
    COUNT(*) AS headcount
FROM workday_core.public.worker
WHERE active = TRUE
GROUP BY management_level
ORDER BY headcount DESC
```

### Workers hired in the last 90 days

Copy code

```
SELECT
    worker_id,
    full_name,
    hire_date,
    business_title
FROM workday_core.public.worker
WHERE hire_date >= CURRENT_DATE - INTERVAL '90' DAY
ORDER BY hire_date DESC
```

Note

In EA, available objects are limited to Workforce and Talent. Row-level security controls are planned for GA. Table and column-level access is controlled by the ISU’s security group in Workday.

## Next steps

With data in a DataFrame, you can use [Cortex Code](/user-guide/data-integration/zero-copy/workday/cortex-code) to write queries, build visualizations, and get AI-assisted analysis of your Workday data.

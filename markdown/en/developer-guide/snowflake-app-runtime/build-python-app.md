# Build a Python app

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Build a small FastAPI app that displays an HTML page, then deploy it with
the Snowflake CLI. Python apps run on
[serverless compute](/developer-guide/snowflake-app-runtime/serverless)
(Public Preview). For the Python version, dependency installation,
and environment variables, see
[Python](/developer-guide/snowflake-app-runtime/runtime-environment#label-snowflake-app-runtime-runtime-environment-python).

## Before you begin

- [Snowflake CLI](/developer-guide/snowflake-cli/installation) with a
  configured
  [connection](/developer-guide/snowflake-cli/connecting/configure-connections).
- Serverless compute enabled for your account, as described in
  [Create a serverless app](/developer-guide/snowflake-app-runtime/serverless#label-snowflake-app-runtime-serverless-opt-in).
- A role with the privileges described in
  [Deploy with the CLI](/developer-guide/snowflake-app-runtime/privileges#label-snowflake-app-runtime-privileges-cli-deploy).
- To share the app, ask an account administrator to complete
  [account setup](/developer-guide/snowflake-app-runtime/account-admin-setup)
  first. Otherwise you deploy to your personal database.

## Create the project

1. Create a project directory and open it:

   Copy code

   ```
   mkdir hello_python
   cd hello_python
   ```
2. Create `requirements.txt` with these dependencies:

   ```
   fastapi>=0.115
   uvicorn>=0.34
   ```

## Write the app code

Create `app.py`. The app imports dependencies from `.python_packages` and
listens on `0.0.0.0` at the port Snowflake provides in `PORT`:

Copy code

```
import os
import sys
from pathlib import Path

sys.path.insert(1, str(Path(__file__).resolve().parent / ".python_packages"))

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def hello():
    return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Hello from Python</title>
  </head>
  <body>
    <h1>Hello from Python</h1>
    <p>This FastAPI app runs on Snowflake App Runtime.</p>
  </body>
</html>
"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
```

## Configure app.yml

Generate deployment settings. Setup resolves the database, schema, and warehouse
from its options, then account defaults, then your personal database. It
doesn’t fill the database from the active connection. See
[Build with the Snowflake CLI](/developer-guide/snowflake-app-runtime/getting-started#label-getting-started-cli-path).

Copy code

```
snow app setup --app-name hello_python
```

Keep the name, database, schema, warehouse, and ignore entries that setup
writes. Add `compute_resource`, `runtime`, `install`, and `run`
as in the following example, and add `.venv`, `.python_packages`, and `output` to `ignore`.
The following example shows the complete `app.yml`. Replace the placeholders with the
database, schema, and warehouse values from your generated file.

Make sure `compute_resource: SERVERLESS` and `runtime: python` are set; Python
apps run only on serverless compute.

Copy code

```
version: 2

name: HELLO_PYTHON
database: <your_database>
schema: <your_schema>
query_warehouse: <your_warehouse>
compute_resource: SERVERLESS
runtime: python

install:
  commands:
    - ["pip", "install", "--upgrade", "--target", ".python_packages", "-r", "requirements.txt"]

run:
  command: ["python", "app.py"]

ignore:
  - node_modules
  - .env*
  - __pycache__
  - "*.pyc"
  - .next
  - .git
  - snowflake.log
  - .venv
  - .python_packages
  - output
```

`ignore` keeps your local `.python_packages` out of the source upload; the
remote build reinstalls dependencies into `.python_packages` and includes them
in the deployed package. The run command starts `app.py`.

If setup warns that `HELLO_PYTHON` already exists, choose a different app
name before deploying so you don’t replace an existing app.

## Run locally

Install the dependencies into `.python_packages` with the same command the
remote build runs, then start the app:

Copy code

```
pip install --upgrade --target .python_packages -r requirements.txt
python app.py
```

Without `PORT` set, the app listens on port 8080. Open `http://localhost:8080`
to see the page.

## Deploy and open the app

Deploy the app, then open it:

Copy code

```
snow app deploy
snow app open
```

Sign in to Snowflake when prompted. The page displays **Hello from Python**
and **This FastAPI app runs on Snowflake App Runtime.**

The first serverless deploy in an account can stop while Snowflake issues the
TLS certificate. See
[Serverless deploy stops while the TLS certificate is issued](/developer-guide/snowflake-app-runtime/troubleshooting#label-snowflake-app-runtime-troubleshooting-serverless-certificate).

## Next steps

- Query your data: [Query Snowflake from a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/query-snowflake).
- Learn how serverless compute starts and stops: [Serverless compute for Snowflake App Runtime](/developer-guide/snowflake-app-runtime/serverless).
- Share the app with other roles: [Share a Snowflake App Runtime app](/developer-guide/snowflake-app-runtime/access-control).

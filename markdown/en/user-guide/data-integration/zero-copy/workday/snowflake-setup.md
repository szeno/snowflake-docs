# Set up Snowflake for Workday Live Data Query

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Note

Workday Live Data Query for Snowflake is in Early Adopter (EA) for Workday and in Preview for Snowflake. To request access, contact your Workday account representative.

This topic describes how to create the Snowflake objects needed to connect to the Workday Live Data Query (LDQ) service: a dedicated role and user, a database and schema, a stage to hold the Python connector, a network rule to allow outbound traffic to Workday, a secret to store your private key, and an external access integration to tie them together.

Complete these steps before creating a Snowflake Notebook. See [About Workday Live Data Query for Snowflake](/user-guide/data-integration/zero-copy/about-workday-ldq) for the full setup checklist.

## Step 1: Download the Python connector

The Workday LDQ connector ships as a `.whl` (wheel) file. Download it from the Workday Community portal before starting the Snowflake setup so it’s available to upload in a later step.

1. Sign in to [Workday Community](https://community.workday.com) with your Workday credentials.
2. Download the latest `.whl` file (for example, `ldq_python_client-1.0.3-py3-none-any.whl`) to your local computer. The download may be packaged as a zip file named `Datacloud-LiveDataQueryPython.zip`.
3. If you downloaded a zip file, extract it to get the `.whl` file.

Note

You must have a valid Workday customer or partner account to access the download. If you can’t find the file, contact your Workday account representative.

## Step 2: Create a role and user

Create a dedicated role and user for LDQ instead of using `ACCOUNTADMIN`. This role will have only the minimum privileges needed to create and manage the LDQ objects.

Note

This step requires `ACCOUNTADMIN` (or `SECURITYADMIN` + `SYSADMIN`). All subsequent steps use the new `WORKDAY_LDQ_TEST_ROLE` role.

You can complete this step using SQL or Snowsight.

### Using SQL

In Snowsight, go to **Projects** > **Worksheets**, click **+ Worksheet**, set your role to `ACCOUNTADMIN`, and run:

Copy code

```
-- Create the role
CREATE ROLE IF NOT EXISTS WORKDAY_LDQ_TEST_ROLE;

-- Create a dedicated user and assign the role
CREATE USER IF NOT EXISTS WORKDAY_LDQ_TEST_USER
  DEFAULT_ROLE = WORKDAY_LDQ_TEST_ROLE
  MUST_CHANGE_PASSWORD = TRUE
  PASSWORD = '<strong_password>';

GRANT ROLE WORKDAY_LDQ_TEST_ROLE TO USER WORKDAY_LDQ_TEST_USER;

-- Grant account-level privileges needed for setup
GRANT CREATE DATABASE  ON ACCOUNT TO ROLE WORKDAY_LDQ_TEST_ROLE;
GRANT CREATE INTEGRATION ON ACCOUNT TO ROLE WORKDAY_LDQ_TEST_ROLE;
GRANT USAGE ON WAREHOUSE COMPUTE_WH TO ROLE WORKDAY_LDQ_TEST_ROLE;
```

Note

Replace `COMPUTE_WH` with the name of the warehouse you plan to use. After the database and schema are created in the next step, `WORKDAY_LDQ_TEST_ROLE` automatically owns those objects and has full privileges on them.

### Using Snowsight

1. Navigate to **Admin** > **Users & Roles** > **Roles**.
2. Click **+ Role**, enter `WORKDAY_LDQ_TEST_ROLE`, and click **Create Role**.
3. Navigate to **Admin** > **Users & Roles** > **Users**.
4. Click **+ User**, enter `WORKDAY_LDQ_TEST_USER`, set the default role to `WORKDAY_LDQ_TEST_ROLE`, and click **Create User**.
5. Grant the role to the user and the account-level privileges as shown in the SQL above.

Important

Switch to `WORKDAY_LDQ_TEST_ROLE` for all remaining steps. You no longer need `ACCOUNTADMIN`.

## Step 3: Create a database and schema

Create a dedicated database and schema to hold the LDQ stage, network rule, secret, and integration.

### Using SQL

Open a Snowflake worksheet, set your role to `WORKDAY_LDQ_TEST_ROLE`, and run:

Copy code

```
CREATE DATABASE IF NOT EXISTS WORKDAY_LDQ_TEST;
CREATE SCHEMA  IF NOT EXISTS WORKDAY_LDQ_TEST.LIVEDATA;
```

### Using Snowsight

1. Navigate to **Catalog** > **Explorer**.
2. Click **+ Database**, enter `WORKDAY_LDQ_TEST`, and click **Create**.
3. Open the new database, click **+ Schema**, enter `LIVEDATA`, and click **Create**.

## Step 4: Create a stage for the Python connector

Create a Snowflake internal stage to store the wheel file so it can be installed inside your notebook. Create the stage first, then upload the file you downloaded in Step 1.

### Create the stage

1. In Snowsight, navigate to **Catalog** > **Explorer**.
2. Search for `WORKDAY_LDQ_TEST` and click on it.
3. Click **Schemas**, then **LIVEDATA**, then **Stages**.
4. Click **+ Stage** > **Snowflake Managed**.
5. Enter `LDQ_STAGE` as the name, enable **Directory table**, and click **Create**.

### Upload the wheel file

1. Open the `LDQ_STAGE` stage.
2. Click the **Files** tab, then **+ Files**.
3. Select the `.whl` file from your local computer.
4. Click **Upload**.

## Step 5: Create a network rule

By default, Snowflake Notebooks can’t make outbound network calls. A network rule defines which external hosts are permitted. Create one that allows HTTPS traffic to your Workday host (for OAuth2 and the live data service) and to PyPI (so `pip install` can download the connector’s dependencies).

### Using SQL

In the same worksheet (with `WORKDAY_LDQ_TEST_ROLE`), run:

Copy code

```
CREATE OR REPLACE NETWORK RULE WORKDAY_LDQ_TEST.LIVEDATA.WORKDAY_LDQ_TEST_RULE
  MODE       = EGRESS
  TYPE       = HOST_PORT
  VALUE_LIST = (
    'impl-services1.wd12.myworkday.com:443',
    'pypi.org:443',
    'files.pythonhosted.org:443'
  );
```

### Using Snowsight

1. Navigate to **Admin** > **Security** > **Network Rules**.
2. Click **+ Network Rule** and fill in the following fields:
   - **Name:** `WORKDAY_LDQ_TEST_RULE`
   - **Database / Schema:** `WORKDAY_LDQ_TEST` / `LIVEDATA`
   - **Type:** Host & Port
   - **Mode:** Egress
   - **Hosts:** `impl-services1.wd12.myworkday.com:443`, `pypi.org:443`, `files.pythonhosted.org:443`
3. Click **Create Network Rule**.

Note

Replace `impl-services1.wd12.myworkday.com` with the host from your token endpoint URL. The same host serves both the data service and the token endpoint. The `pypi.org` and `files.pythonhosted.org` entries are required so that `pip install` can download the connector’s dependencies at notebook runtime.

## Step 6: Store the private key as a Snowflake secret

Store the RSA private key as a Snowflake secret to prevent it from being hardcoded in notebooks or configuration files. The secret is encrypted at rest and only accessible to notebooks granted access through the external access integration in Step 7.

### Using SQL

In the same worksheet, run:

Copy code

```
CREATE SECRET WORKDAY_LDQ_TEST.LIVEDATA.WORKDAY_PRIVATE_KEY
  TYPE          = GENERIC_STRING
  SECRET_STRING = '-----BEGIN RSA PRIVATE KEY-----
<paste the full contents of your private-key.pem here>
-----END RSA PRIVATE KEY-----';
```

Caution

Paste the PEM content directly into the SQL worksheet. Don’t save it to a file or share it in plain text. Once created, the secret value can’t be retrieved via SQL.

### Using Snowsight

1. Navigate to **Admin** > **Security** > **Secrets**.
2. Click **+ Secret** and fill in the following fields:
   - **Name:** `WORKDAY_PRIVATE_KEY`
   - **Database / Schema:** `WORKDAY_LDQ_TEST` / `LIVEDATA`
   - **Type:** Generic String
   - **Secret value:** paste the full contents of `private-key.pem`, including the `-----BEGIN-----` and `-----END-----` lines
3. Click **Create Secret**.

Caution

The secret value is encrypted at rest and can’t be retrieved after creation through the UI or SQL.

## Step 7: Create an external access integration

An external access integration (EAI) references the network rule and the private key secret, and acts as the Snowflake-level permission grant that allows a notebook to use both. You must attach the EAI to your notebook before any outbound calls to Workday succeed.

Note

Creating an external access integration requires the `CREATE INTEGRATION` privilege on the account, which was granted to `WORKDAY_LDQ_TEST_ROLE` in Step 2.

### Using SQL

In the same worksheet, run:

Copy code

```
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION WORKDAY_LDQ_TEST_EAI
  ALLOWED_NETWORK_RULES        = (WORKDAY_LDQ_TEST.LIVEDATA.WORKDAY_LDQ_TEST_RULE)
  ALLOWED_AUTHENTICATION_SECRETS = (WORKDAY_LDQ_TEST.LIVEDATA.WORKDAY_PRIVATE_KEY)
  ENABLED                      = TRUE;
```

### Using Snowsight

1. Navigate to **Admin** > **Security** > **External Access Integrations**.
2. Click **+ External Access Integration** and fill in the following fields:
   - **Name:** `WORKDAY_LDQ_TEST_EAI`
   - **Allowed Network Rules:** select `WORKDAY_LDQ_TEST.LIVEDATA.WORKDAY_LDQ_TEST_RULE`
   - **Allowed Authentication Secrets:** select `WORKDAY_LDQ_TEST.LIVEDATA.WORKDAY_PRIVATE_KEY`
   - **Enabled:** toggle on
3. Click **Create External Access Integration**.

## Next steps

With the Snowflake setup complete, continue to [Connect to Workday and query data from Snowflake](/user-guide/data-integration/zero-copy/workday/connect-and-query) to create a notebook, install the connector, and run your first queries.

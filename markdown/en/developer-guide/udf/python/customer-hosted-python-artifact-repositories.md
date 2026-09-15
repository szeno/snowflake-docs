# Integrate customer-hosted Python artifact repositories

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Customer-hosted artifact repositories connect private Python artifact repository solutions directly to Snowflake. By integrating these external repositories, you can use the same package management workflows you already apply internally.

Note

Customer-hosted artifact repositories are supported for the following Snowflake Python workloads:

- Python UDFs, UDTFs, and UDAFs
- Python stored procedures
- Snowflake Notebooks
- Snowflake Model Registry models that you serve with SPCS online or batch inference (using `artifact_repository_map` on `log_model`)

They are not currently supported for Streamlit, Snowflake Native Apps, or generic SPCS services that you create with `CREATE SERVICE`.

Customer-hosted artifact repositories let you reuse the same package management and governance systems you already rely on, while making them available to Snowflake Python workloads. You can configure these repositories using API integrations and secrets, even setting them as account-wide defaults to simplify deployment.

Customer-hosted artifact repositories support PrivateLink for enhanced networking. This effectively bridges the gap between internal security standards and cloud-based data science workflows.

Key ways this integration improves security and governance include:

- **Governance in your upstream**: Reuse the package allowlists, quarantine rules, version pins, and access controls already enforced by your Nexus, JFrog, Azure DevOps, GCP Artifact Registry, or AWS CodeArtifact repository. Snowflake Package Policy applies to `snowflake.snowpark.pypi_shared_repository` and `snowflake.snowpark.anaconda_shared_repository` only, so for customer-hosted repositories governance stays in the tools your organization already uses.
- **Security and Compliance**: Use existing package governance and policies in customer-hosted repositories.
- **Consistency**: Customers can manage Snowflake packages using the same repositories they manage other code bases.

## Authentication methods

The supported authentication methods for customer-hosted artifact repositories are:

- Username and password
- Tokens

These credentials must be stored securely within a Snowflake SECRET object.
OAuth and IAM-based authentication are not currently supported.

## Configure a customer-hosted artifact repository

To configure a customer-hosted artifact repository in Snowflake, you must create and link three primary Snowflake objects:

- **Snowflake SECRET**: This object is used to securely store the repository credentials, such as a username and password or a token.
- **API integration**: This object describes the network path to reach the repository, specifying whether the connection should go through the public Internet or via a PrivateLink endpoint for enhanced security.
- **Artifact repository object**: This is the core object that ties together the API integration, the index URL of the repository, and the associated secret.

The following steps outline how to set this up:

1. **Create a Secret for credentials**

   First, you must create a Snowflake SECRET to securely store the credentials (username/password or token) required to access your repository.

   Copy code

   ```
   -- Create a secret for credentials
   CREATE OR REPLACE SECRET my_repo_secret
     TYPE = PASSWORD
     USERNAME = 'your_username'
     PASSWORD = 'your_password_or_token';
   ```
2. **Create an API integration**

   Create an API integration to describe the route to the repository. You have two options:

   - **Public HTTPS**: For repositories accessible over the Internet.

     Copy code

     ```
     CREATE OR REPLACE API INTEGRATION python_repo_integration
       API_PROVIDER = ARTIFACT_REPOSITORY_API
       API_ALLOWED_PREFIXES = ('https://nexus.example.com', 'https://artifactory.example.com')
       ALLOWED_AUTHENTICATION_SECRETS = (my_repo_secret)
       ENABLED = TRUE;
     ```

     [Egress IP](/user-guide/egress-ip/network-egress): You can securely allow ingress access from Snowflake to your package repository by allowing egress IP address ranges generated from Snowflake through the repository’s network firewall. To generate and use Snowflake egress IP addresses, follow these steps:

     > Note
     >
     > Egress IP is available only for external access on AWS.
     >
     > 1. Call [SYSTEM$GET\_SNOWFLAKE\_EGRESS\_IP\_RANGES](/sql-reference/functions/system_get_snowflake_egress_ip_ranges) to get the current and upcoming IP ranges and their expiration times.
     > 2. Use the IP ranges you obtain to update firewall rules by using APIs, CLIs, or configuration management tools, as described in [Automate IP address range refreshes](/user-guide/egress-ip/network-egress#label-network-egress-refreshing).
   - [PrivateLink](/user-guide/private-connectivity-inbound): For internal repositories, use the parameter `USE_PRIVATELINK_ENDPOINT = TRUE` to ensure traffic stays within a VPC/VNet.

     Note

     Private Link requires Business Critical Edition (or higher).

     - Provision a private connectivity endpoint in the Snowflake VPC or VNet to enable Snowflake to connect to your repository service. For information about how to do this, see [SYSTEM$PROVISION\_PRIVATELINK\_ENDPOINT](/sql-reference/functions/system_provision_privatelink_endpoint).
     - Use the following code to create an API integration that uses private connectivity:

     Copy code

     ```
     CREATE OR REPLACE API INTEGRATION python_repo_integration_pl
       API_PROVIDER = ARTIFACT_REPOSITORY_API
       API_ALLOWED_PREFIXES = ('https://nexus-pl.internal.example.com')
       USE_PRIVATELINK_ENDPOINT = TRUE
       ALLOWED_AUTHENTICATION_SECRETS = (my_repo_secret)
       ENABLED = TRUE;
     ```

   The API integration governs Snowflake’s outbound access: `API_ALLOWED_PREFIXES` is the complete list of hosts and path prefixes Snowflake is allowed to fetch from on your behalf, and Snowflake refuses any request to a host that isn’t covered by it.

   This matters most for redirects. Many repositories serve their package index from one host but redirect the actual file download to a different one, such as a CDN, a blob store, or an S3 bucket. Snowflake checks every hop of a redirect chain against `API_ALLOWED_PREFIXES`, so every host your repository might redirect to has to be listed, not just the host in your `INDEX_URL`. If you list only the index host, index requests succeed and package downloads fail with HTTP 400 or 403. The download hosts often aren’t documented by the repository vendor, so it’s usually faster to observe them than to guess: see [Repro #3](#label-customer-hosted-repos-troubleshooting) in the Troubleshooting section for a command that prints every host an install actually touches. You can also use `*` in the leftmost subdomain position of a prefix to cover dynamic subdomains — for example, `'https://*.blob.core.windows.net'` covers every bucket-specific Azure Blob host that an Azure DevOps repository might redirect to.
3. **Create the Artifact Repository object**

   This object ties the previous components together with your repository’s index URL.

   Copy code

   ```
   -- Create the artifact repository object
   CREATE OR REPLACE ARTIFACT REPOSITORY my_python_repo
     TYPE = PYPI
     API_INTEGRATION = python_repo_integration
     INDEX_URL = 'https://nexus.example.com/repository/pypi-proxy/simple/'
     AUTHENTICATION_SECRET = my_repo_secret
     COMMENT = 'Customer-hosted Python package repository (Nexus)';
   ```

Following is an example of a Python UDF:

Copy code

```
CREATE OR REPLACE FUNCTION test_udf()
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.13'
  ARTIFACT_REPOSITORY = my_python_repo
  PACKAGES = ('test_whl_package')
  HANDLER = 'test'
AS $$
import test_whl_package

def test():
  return test_whl_package.say_hello()
$$;

SELECT test_udf();
```

You can use customer-hosted repositories in Python stored procedures too. Note that your repository needs to host [Snowpark](https://pypi.org/project/snowflake-snowpark-python/) for stored procedures to work.

Copy code

```
CREATE OR REPLACE PROCEDURE test_sproc()
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.13'
ARTIFACT_REPOSITORY = my_python_repo
PACKAGES = ('snowflake-snowpark-python', 'test_whl_package')
HANDLER = 'run'
AS $$
def run(session):
  return test_whl_package.say_hello()
$$;

CALL test_sproc();
```

## Package retention and caching

When you create a UDF or stored procedure that installs packages from a customer-hosted repository, Snowflake can *retain* those packages by storing a copy of the exact files in Snowflake-managed storage. After a package is retained, Snowflake serves it from that copy instead of fetching it from your repository at runtime. As a result, your functions keep working even if the upstream repository later changes a package, removes a version, or becomes temporarily unreachable.

Retention applies to the Python UDFs and stored procedures you create against a customer-hosted repository. Packages are pinned when the function or procedure is created and reused on every later execution.

### Control retention with PACKAGE\_RETENTION

The `PACKAGE_RETENTION` property on an artifact repository controls when packages are retained:

- **Default (property not set)**: *Asynchronous retention.* Packages are retained automatically in the background after each `CREATE FUNCTION` or `CREATE PROCEDURE`. Until retention completes, executions are served from your repository; afterward they’re served from the retained copy.
- **`PACKAGE_RETENTION = ON_OBJECT_CREATION`**: *Synchronous retention.* `CREATE FUNCTION` and `CREATE PROCEDURE` download and retain every package before the statement returns. If any package can’t be retained, the statement fails. Use this when you want packages guaranteed to be retained at creation time.

Set the property when you create the repository:

Copy code

```
CREATE OR REPLACE ARTIFACT REPOSITORY my_python_repo
  TYPE = PYPI
  API_INTEGRATION = python_repo_integration
  INDEX_URL = 'https://nexus.example.com/repository/pypi-proxy/simple/'
  AUTHENTICATION_SECRET = my_repo_secret
  PACKAGE_RETENTION = ON_OBJECT_CREATION;
```

You can also change it on an existing repository:

Copy code

```
ALTER ARTIFACT REPOSITORY my_python_repo
  SET PACKAGE_RETENTION = ON_OBJECT_CREATION;
```

Note

Snowflake requires a SHA256 hash for every retained package. If your repository doesn’t publish a SHA256 hash for a package, retention of that package fails. Most PyPI-compatible repositories publish these hashes by default.

### Example: retained packages survive an unreachable repository

The following example creates a repository with synchronous retention, defines a UDF against it, then points the repository at an invalid URL to simulate the upstream becoming unreachable. Because the package was retained when the function was created, the UDF keeps executing — even on a new warehouse with no local cache. The same protection applies to asynchronous retention once background retention has completed.

Copy code

```
-- Retain packages at function-creation time.
CREATE OR REPLACE ARTIFACT REPOSITORY my_python_repo
  TYPE = PYPI
  API_INTEGRATION = python_repo_integration
  INDEX_URL = 'https://nexus.example.com/repository/pypi-proxy/simple/'
  AUTHENTICATION_SECRET = my_repo_secret
  PACKAGE_RETENTION = ON_OBJECT_CREATION;

-- Synchronous retention: this statement downloads and retains test_whl_package
-- before it returns.
CREATE OR REPLACE FUNCTION test_udf()
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.13'
  ARTIFACT_REPOSITORY = my_python_repo
  PACKAGES = ('test_whl_package')
  HANDLER = 'test'
AS $$
import test_whl_package

def test():
  return test_whl_package.say_hello()
$$;

-- Point the repository at an invalid URL to simulate the upstream being unreachable.
ALTER ARTIFACT REPOSITORY my_python_repo
  SET INDEX_URL = 'https://nexus.example.com/repository/does-not-exist/simple/';

-- The UDF still runs: the package is served from the retained copy, not the upstream.
SELECT test_udf();
```

Note

Retention protects *execution*, not *creation*. `CREATE FUNCTION` and `CREATE PROCEDURE` still resolve packages against your upstream repository, so the repository must be reachable whenever you create or replace a function or procedure — even for packages that are already retained. In the example above, defining a *new* function against the invalid URL would fail; only the already-created `test_udf` keeps working.

### Encryption of retained packages

Retained packages are encrypted at rest in Snowflake-managed storage using Snowflake’s client-side encryption. If Tri-Secret Secure is enabled on your account, retained packages are protected by your customer-managed key as well.

## Find objects that depend on a package

To find every Python UDF, UDTF, UDAF, and stored procedure in your account that depends on a given package — including objects in schemas your current role can’t see — query [`SNOWFLAKE.ACCOUNT_USAGE.FUNCTIONS`](/sql-reference/account-usage/functions) and [`SNOWFLAKE.ACCOUNT_USAGE.PROCEDURES`](/sql-reference/account-usage/procedures) on their `INSTALLED_PACKAGES` column, which lists both the packages named in the `PACKAGES` clause and their transitive dependencies.

Substitute the package name into the CTE below and run the query as a role with access to the `SNOWFLAKE` database (the `SNOWFLAKE.ACCOUNT_USAGE` schema is granted to `ACCOUNTADMIN` by default; see [enabling `ACCOUNT_USAGE` for other roles](/sql-reference/account-usage#enabling-the-snowflake-database-usage-for-other-roles)):

Copy code

```
WITH pkg AS (SELECT '<PACKAGE_NAME>'::STRING AS name)
SELECT
    'FUNCTION'          AS object_kind,
    function_catalog    AS database_name,
    function_schema     AS schema_name,
    function_name       AS object_name,
    argument_signature,
    function_language   AS language,
    runtime_version,
    packages            AS declared_packages,
    installed_packages,
    created,
    last_altered
FROM   snowflake.account_usage.functions, pkg
WHERE  deleted IS NULL
   AND function_language = 'PYTHON'
   AND installed_packages ILIKE '%''' || pkg.name || '==%'
UNION ALL
SELECT
    'PROCEDURE',
    procedure_catalog,
    procedure_schema,
    procedure_name,
    argument_signature,
    procedure_language,
    runtime_version,
    packages,
    installed_packages,
    created,
    last_altered
FROM   snowflake.account_usage.procedures, pkg
WHERE  deleted IS NULL
   AND procedure_language = 'PYTHON'
   AND installed_packages ILIKE '%''' || pkg.name || '==%'
ORDER BY database_name, schema_name, object_name;
```

To scope the result to objects tied to a specific artifact repository, use the equivalent query against [`INFORMATION_SCHEMA.FUNCTIONS`](/sql-reference/info-schema/functions) and [`INFORMATION_SCHEMA.PROCEDURES`](/sql-reference/info-schema/procedures) — both views expose an `ARTIFACT_REPOSITORY` column (`ACCOUNT_USAGE` does not). Use the **bare repository name**, not a fully qualified name:

Copy code

```
-- Add to the WHERE clause of the INFORMATION_SCHEMA query above:
AND artifact_repository ILIKE '<MY_REPO>'
```

Note

`ACCOUNT_USAGE` views have latency of up to two hours and are scoped to the whole account. `INFORMATION_SCHEMA` views are near-real-time but scoped to a single database (see [Account Usage vs. Information Schema](/sql-reference/account-usage#differences-between-account-usage-and-information-schema)). Use `ACCOUNT_USAGE` for account-wide sweeps, and `INFORMATION_SCHEMA` when you need repository-level filtering or immediate consistency.

## Set a customer-hosted repository as the default

To avoid specifying `ARTIFACT_REPOSITORY` on every function and procedure, set your customer-hosted repository as the default with the [`DEFAULT_PYTHON_ARTIFACT_REPOSITORY`](/sql-reference/parameters#label-default-python-artifact-repository) parameter. The parameter can be set at the account, database, or schema level, and accepts a customer-hosted artifact repository object in addition to the Snowflake-managed shared repositories.

Copy code

```
-- Account-level default
ALTER ACCOUNT SET DEFAULT_PYTHON_ARTIFACT_REPOSITORY = my_db.my_schema.my_python_repo;

-- Database-level default
ALTER DATABASE my_db SET DEFAULT_PYTHON_ARTIFACT_REPOSITORY = my_db.my_schema.my_python_repo;

-- Schema-level default
ALTER SCHEMA my_db.my_schema SET DEFAULT_PYTHON_ARTIFACT_REPOSITORY = my_db.my_schema.my_python_repo;
```

Use the fully qualified name of the artifact repository object. The priority order for repository resolution is: function-level > schema-level > database-level > account-level.

After a default is set, functions and procedures can omit `ARTIFACT_REPOSITORY`, and Snowflake resolves packages from the default repository:

Copy code

```
CREATE OR REPLACE FUNCTION normalize_phone_number(raw_number STRING, region STRING)
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.13'
  PACKAGES = ('phonenumbers==8.13.40')
  HANDLER = 'normalize_phone_number'
AS $$
import phonenumbers

def normalize_phone_number(raw_number, region):
  parsed = phonenumbers.parse(raw_number, region)
  return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
$$;
```

## Use a customer-hosted repository in Snowflake Notebooks

You can use customer-hosted artifact repositories in Snowflake Notebooks for interactive development and scheduled runs. For details, see [Using artifact repositories](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-artifact-repositories).

## Use a customer-hosted repository with Model Serving

To install packages from a customer-hosted repository when you serve a model on Snowpark Container Services (online
inference or batch inference jobs), pass the repository in `artifact_repository_map` when you log the model. Snowflake
resolves those packages during the model image build. For an explanation and example, see
[Use a private PyPI artifact repository](/developer-guide/snowflake-ml/model-registry/overview#label-snowpark-model-registry-private-pypi).

## Private Link setup

For Business Critical and VPS (Virtual Private Snowflake) customers, Snowflake supports the outbound private connectivity feature, which lets you set up a private connection between your Snowflake account and your cloud infrastructure.

To use this functionality, you must ensure proper setup of all infrastructure components on both sides: the Snowflake console and your own infrastructure.

Note

Snowflake supports only connections within the same cloud provider.
For example, both Snowflake and your components must be in AWS.

### Step 1: Set up Private Link Service and redirect HTTPS traffic to the repository server

On the customer infrastructure side, a Private Link Service needs to be created so the Private Endpoint provisioned in [Step 2](#label-customer-hosted-repos-provision-endpoint) can reach out. If the target Private Link Service is a VPC endpoint service, it needs to accept Snowflake’s principal ARN, which can be obtained from the [SYSTEM$GET\_PRIVATELINK\_CONFIG](/sql-reference/functions/system_get_privatelink_config) system function.

With the Private Link Service, you should add necessary infrastructure components on your side to redirect the traffic to your repository server. The setup depends on where the repository server is located.

#### Repository server outside of the VPC

If the repository server is located outside of the cloud provider, then the traffic that goes from Snowflake to the Private Link Service needs to be redirected to this server. The recommended component for this is an nginx proxy. The proxy redirects all HTTPS (port 443) traffic to the repository server.

[![Architecture diagram showing Snowflake connecting through Private Link to a VM proxy (nginx), which redirects traffic to a repository server outside the VPC.](/static/images/developer-guide/udf/python/customer-hosted-artifact-repos/images/repo-outside-vpc.png)](/static/images/developer-guide/udf/python/customer-hosted-artifact-repos/images/repo-outside-vpc.png)

Note

This setup assumes that the repository server is reachable from your cloud infrastructure. If not, you need to provide a connection between the proxy and the repository server. If the repository server has an IP allow-list, the proxy can have a static IP assigned, and this IP can be added to the allow-list on the repository server side.

For detailed manual setup instructions, see the following guides:

- [AWS](#label-customer-hosted-repos-aws-setup)
- [Azure](#label-customer-hosted-repos-azure-setup)
- [GCP](#label-customer-hosted-repos-gcp-setup)

#### Repository server within the VPC

If the repository server is located within the same cloud (for example, Azure DevOps in Azure cloud), the setup is less complex. You only need to pass the traffic from the Private Link Service to the repository server on HTTPS (port 443).

[![Architecture diagram showing Snowflake connecting through Private Link directly to a repository server within the same VPC.](/static/images/developer-guide/udf/python/customer-hosted-artifact-repos/images/repo-inside-vpc.png)](/static/images/developer-guide/udf/python/customer-hosted-artifact-repos/images/repo-inside-vpc.png)

### Step 2: Provision Private Endpoint

On the Snowflake side, you need to provision a Private Endpoint that reaches your infrastructure through a private IP.

When provisioning the Private Endpoint, you need to provide two arguments: the Private Link Service ID from your cloud provider and the repository server domain name.

Since Snowflake reaches your repository server through the HTTPS protocol, the domain name must have a valid certificate.

Note

Customer-hosted artifact repositories currently do not support self-signed certificates (not CA-signed).

**Private Endpoint provision for AWS:**

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  'com.amazonaws.vpce.us-west-2.vpce-svc-xxx',  -- VPC Endpoint Service Name
  'jfrog_address.com'                            -- Repository server domain
);
```

**Private Endpoint provision for Azure:**

Copy code

```
SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
  '/subscriptions/9217bbdd-434e-4dbb-97c2-0825c627a277/resourceGroups/jfrog-server_group/providers/Microsoft.Network/privateLinkServices/jfrog-server-pl-service',  -- Private Service ID
  'jfrog_address.com'                                                                                                                                                -- Repository server domain
);
```

### Step 3: Accept Private Endpoint request in Private Link Service

After the Private Endpoint is provisioned, you should see the awaiting Private Endpoint connection in your cloud Private Link Service. To finish the Private Endpoint setup, accept the connection request.

You can check the status of provisioning by calling the [SYSTEM$GET\_PRIVATELINK\_ENDPOINTS\_INFO](/sql-reference/functions/system_get_privatelink_endpoints_info) system function. After you accept the Private Endpoint, the status field should change from:

- **AWS**: `Pending` to `Available`
- **Azure**: `Pending` to `APPROVED`
- **GCP**: `Pending` to `ACCEPTED`

### Step-by-step manual config for AWS (repository server outside of the VPC)

1. **Create and set up an EC2 proxy instance**

   Create an EC2 instance with Amazon Linux that allows SSH traffic from your local machine.
   Make sure its Security Group allows inbound traffic on ports 22 (SSH) and 443 (HTTPS).

   Connect to the EC2 instance and install Docker:

   Copy code

   ```
   sudo yum install docker
   sudo service docker start
   ```

   Replace `jfrog_address.com` with your repository server domain and run:

   Copy code

   ```
   echo -e 'events {\n}\nstream {\n    upstream jfrog_server {\n        server jfrog_address.com:443;\n    }\n\n    server {\n        listen 443;\n        proxy_pass jfrog_server;\n    }\n}' > nginx.conf && \
   sudo docker run --rm -d --name my-custom-nginx-container \
     -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
     -p 443:443 nginx
   ```
2. **Create a Target Group for the EC2 proxy instance**

   Create a Target Group that points to the EC2 instance (from the previous step) on TCP port 443.
3. **Create a Network Load Balancer**

   Create a Network Load Balancer of type **Internal** in the same availability zone as the EC2 instance (for example, `us-west-2b`).

   If the Network Load Balancer operates in more than one zone (for example, `us-west-2a` and `us-west-2b`), enable the **Cross-zone load balancing** option so traffic from all zones goes to the EC2 instance.

   The load balancer should listen on TCP port 443 and forward traffic to the Target Group from the previous step.
4. **Create a VPC Endpoint Service**

   Create a VPC Endpoint Service that sends traffic to the Network Load Balancer from the previous step.

   After creating the service, use the **Service Name** value for [Step 2: Provision Private Endpoint](#label-customer-hosted-repos-provision-endpoint).

### Step-by-step manual config for Azure (repository server outside of the VPC)

1. **Create and set up a VM instance**

   Create a VM instance with a VNet that allows SSH traffic from your local machine.
   Make sure network rules allow inbound traffic on ports 22 (SSH) and 443 (HTTPS).

   Connect to the VM instance:

   Copy code

   ```
   ssh -i ~/.ssh/id_rsa.pem username@IP-ADDRESS
   ```

   Install Docker (see [Docker installation for Ubuntu](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)) and start it:

   Copy code

   ```
   sudo service docker start
   ```

   Replace `jfrog_address.com` with your repository server domain and run:

   Copy code

   ```
   echo -e 'events {\n}\nstream {\n    upstream jfrog_server {\n        server jfrog_address.com:443;\n    }\n\n    server {\n        listen 443;\n        proxy_pass jfrog_server;\n    }\n}' > nginx.conf && \
   sudo docker run --rm -d --name my-custom-nginx-container \
     -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
     -p 443:443 nginx
   ```
2. **Create a Load Balancer**

   The load balancer should listen on TCP port 443 and forward traffic to the VM from the previous step.
3. **Create a Private Link Service**

   Create a Private Link Service that sends traffic to the Load Balancer from the previous step.

   After creating the service, use the **ResourceID** value for [Step 2: Provision Private Endpoint](#label-customer-hosted-repos-provision-endpoint).

### Step-by-step manual config for GCP (repository server outside of the VPC)

1. **Create and set up a VM instance**

   Create a VM instance with firewall rules that allow HTTPS (port 443) traffic.

   Connect to the VM instance, install Docker (see [Docker installation for Ubuntu](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)), and start it:

   Copy code

   ```
   sudo service docker start
   ```

   Replace `jfrog_address.com` with your repository server domain and run:

   Copy code

   ```
   echo -e 'events {\n}\nstream {\n    upstream jfrog_server {\n        server jfrog_address.com:443;\n    }\n\n    server {\n        listen 443;\n        proxy_pass jfrog_server;\n    }\n}' > nginx.conf && \
   sudo docker run --rm -d --name my-custom-nginx-container \
     -v $(pwd)/nginx.conf:/etc/nginx/nginx.conf:ro \
     -p 443:443 nginx
   ```
2. **Add the VM to an instance group**

   Create an unmanaged Instance Group that points to the created VM.
3. **Create a Load Balancer**

   Create a Network Passthrough Internal Load Balancer with:

   - **Backend configuration**: TCP protocol with a health check set on port 443.
   - **Frontend configuration**: Receives traffic only on port 443.
4. **Create a Private Service Connect**

   In the Private Service Connect section, publish a service that sends traffic to the Load Balancer from the previous step.

   Reserve a new subnet for your service, or use an existing one. Either automatically accept connections or define projects that will be accepted. Snowflake’s project ID can be retrieved from the result of calling:

   Copy code

   ```
   SELECT SYSTEM$GET_PRIVATELINK_CONFIG();
   ```

   After creating the service, use the **Service attachment** field for [Step 2: Provision Private Endpoint](#label-customer-hosted-repos-provision-endpoint).

## Troubleshooting

Most artifact-repository failures fall into one of a few patterns: a missing entry in `API_ALLOWED_PREFIXES`, incorrect credentials in the `SECRET`, or a package that the upstream repository cannot serve. The HTTP status code in the error message is usually the strongest diagnostic signal. Start with the status-code table below, then run one or more of the four reproduction steps to confirm and narrow down the root cause. If you still need help, the last section lists what information to provide when you contact Snowflake support.

General guidelines:

- **5xx** errors almost always indicate a Snowflake-side issue.
- **401 / 403** errors almost always indicate a repository-side issue.
- **400** errors almost always indicate a missing entry in `API_ALLOWED_PREFIXES`.

### HTTP status code reference

| HTTP status | What it usually means | First thing to try |
| --- | --- | --- |
| **400 Bad Request** | **Snowflake.** The URL Snowflake is about to fetch is not in `API_ALLOWED_PREFIXES`. Most often the wheel URL listed in your repo’s simple-index page points to a CDN/blob host (CloudFront for JFrog Cloud, a CDN host for Azure DevOps Artifacts, S3 for Sonatype Nexus) that isn’t in your allowlist. Look for `error code: 10003`. | **Repro #3** to capture every host involved, then add the missing host(s) to `API_ALLOWED_PREFIXES`. |
| **401 Unauthorized** | **Repository-side.** The credentials in your `SECRET` are not authenticating against your upstream repository. | **Repro #2** with the same credentials. If `curl` also fails, recreate the secret. If `curl` succeeds but Snowflake still returns 401 — particularly with the message `Authentication failed. Please check your credentials.` — contact Snowflake support. |
| **403 Forbidden** | **Either side.** (a) Your upstream repository is blocking that specific package or version (Nexus quarantine, Azure DevOps ACL, JFrog rule). (b) The same `API_ALLOWED_PREFIXES` problem as 400, but caught later: Snowflake began fetching from an allowed URL and the repository redirected (`3xx`) to a host that is not in the allowlist. | **Repro #2** against the failing URL. If `curl` returns 403, the issue is on the repository side — contact your repository administrator. If `curl` succeeds, run **Repro #3** to find the redirect target you need to add to `API_ALLOWED_PREFIXES`. |
| **404 Not Found** | **Either.** (a) Your `ARTIFACT REPOSITORY` object doesn’t exist on this account, or your role lacks `USAGE` on it. (b) The package/version genuinely doesn’t exist on your upstream. | **Repro #1** to rule out (a). If that’s clean, run **Repro #2** and confirm the package is listed in the simple-index page. |
| **422 Unprocessable Entity** | **Snowflake.** Internal request-validation error. You should not normally see this. | Capture the query ID and contact Snowflake support. |
| **500 Internal Server Error** | **Snowflake** in nearly every case. JFrog and Nexus rarely emit 500s in practice. | Retry. If it persists, run **Repro #4** to capture a clean query ID and contact Snowflake support. |
| **502 Bad Gateway** | **Snowflake.** Snowflake could not reach your upstream repository — DNS resolution failed, TLS handshake failed, the connection timed out, the redirect chain exceeded 20 hops, or the repository returned an unparseable `Location` header. | **Repro #2** from a workstation. If `curl` succeeds, the repository is reachable from the public Internet but Snowflake cannot reach it — contact Snowflake support with the query ID. For PrivateLink setups, see the PrivateLink section below. |
| **503 Service Unavailable** | **Snowflake.** Transient backend condition. JFrog and Nexus rarely emit 503 errors. | Retry after a minute. If the error persists across multiple retries, contact Snowflake support. |
| `Unable to connect to the artifact repository server. 'null'` | **Snowflake.** Transient internal connectivity issue. There is typically no query ID attached. | Retry. If the error persists, contact Snowflake support with the timestamp and your account locator. |

Expand

Show lessSee more

### Repro #1 — Verify your Snowflake setup

Run this first. It confirms your four Snowflake objects (secret, API integration, artifact repository, and grants) are wired up correctly, and rules out the simplest causes — including both branches of the 404 row.

Copy code

```
SHOW ARTIFACT REPOSITORIES;
SHOW GRANTS ON ARTIFACT REPOSITORY <your_repo>;

DESCRIBE SECRET <your_secret>;
DESCRIBE INTEGRATION <your_api_integration>;
DESCRIBE ARTIFACT REPOSITORY <your_repo>;

SELECT SYSTEM$GET_ARTIFACT_REPOSITORY_INFO('<your_repo>');
```

Confirm:

- `SHOW GRANTS` shows `USAGE` on the artifact repository for the role that runs the UDF / stored procedure.
- `DESCRIBE INTEGRATION` shows `API_PROVIDER = ARTIFACT_REPOSITORY_API`, `ENABLED = TRUE`, your secret in `ALLOWED_AUTHENTICATION_SECRETS`, and every host from Repro #3 in `API_ALLOWED_PREFIXES`.
- `DESCRIBE ARTIFACT REPOSITORY` shows an `INDEX_URL` ending in `/simple/`, pointing at a host that is in `API_ALLOWED_PREFIXES`, with `AUTHENTICATION_SECRET` set to the same secret as on the API integration.
- `SYSTEM$GET_ARTIFACT_REPOSITORY_INFO` shows the same view of the API integration, secret, and index URL.

**If this did not resolve the issue,** include the output of all of the commands above (with the secret password redacted — `DESCRIBE SECRET` does not display it, but double-check) when you contact Snowflake support.

### Repro #2 — Test your repo’s auth from outside Snowflake

Use this when you suspect an authentication or connectivity problem (typically a 401, 403, 404, or 502 in the table above). The idea is to send the same `Authorization` header Snowflake would send, from a machine that can reach your repo. For PrivateLink-only repositories, run these commands from a machine within your VPC that can reach the repository endpoint. Two styles, depending on which `TYPE` your `SECRET` uses.

**Style A —** `TYPE = PASSWORD` **(username + password or PAT).** This is the typical pattern for JFrog Cloud, Sonatype Nexus, and Azure DevOps Artifacts. The PAT goes in the `PASSWORD` field even though it isn’t a literal password. Snowflake sends `Authorization: Basic base64(USERNAME:PASSWORD)` — exactly what `curl -u "USERNAME:PASSWORD"` does.

Copy code

```
CREATE SECRET my_repo_secret
  TYPE = PASSWORD
  USERNAME = 'jdoe@example.com'
  PASSWORD = 'AKCp1AB...redacted...XYZ';
```

Copy code

```
curl -i -u "jdoe@example.com:AKCp1AB...redacted...XYZ" "<INDEX_URL><package>/"
```

**Style B —** `TYPE = GENERIC_STRING` **(single opaque token).** Use this when your repo expects a single token with no separate username — the form pip configures as `https://<token>@<host>/simple/`. Snowflake sends `Authorization: Basic base64(SECRET_STRING)`.

Copy code

```
CREATE SECRET my_repo_secret
  TYPE = GENERIC_STRING
  SECRET_STRING = 'AKCp1AB...redacted...XYZ';
```

Copy code

```
curl -i "https://AKCp1AB...redacted...XYZ@<host>/<index-path>/<package>/"
```

Note

Redact your credentials before sharing the command or its output with anyone, including Snowflake support.

Interpret what `curl` returns:

- **HTTP 200 + a list of wheels** — auth is good. Move to Repro #3.
- **HTTP 401** — your secret is wrong, the password/PAT has expired, or your repo expects a different username format (some repos want an email, some want an account name, some want the literal string `oauth2`). Recreate the secret with `ALTER SECRET ... SET ...`.
- **HTTP 403** — you can reach the repository but it is refusing to serve this package or path. Contact your repository administrator (quarantine, ACL).
- **Connection refused / timeout** — network or firewall problem, not auth.

**If this did not resolve the issue,** include the exact `curl` command (with credentials redacted), the HTTP status it returned, and the first ~20 lines of the response body (also redacted) when you contact Snowflake support.

### Repro #3 — Capture every host the install actually touches

Use this when the table or Repro #2 points at `API_ALLOWED_PREFIXES` — typically a 400 Bad Request (`error code: 10003`) or a 403 you confirmed isn’t from your repo.

On a clean Python virtualenv, reproduce the install with the same `INDEX_URL` Snowflake uses and ask `pip` to print everything it does:

Copy code

```
python -m venv /tmp/repro && source /tmp/repro/bin/activate
pip install --dry-run -vvv \
  --index-url "https://<user>:<token>@<host>/<index-path>/" \
  <package>==<version>
```

If you’d rather use `curl`, the equivalent is to follow redirects on a wheel URL and print every hop:

Copy code

```
curl -L -i -u "<user>:<token>" "<wheel-url-from-the-index-page>"
```

List every distinct host that appears in the output — the index host, the wheel/blob host, any CDN redirect target. **Every one of those hosts must be in** `API_ALLOWED_PREFIXES` **on your** `API INTEGRATION`.

Examples of hosts that are commonly missed:

- JFrog Cloud — `<tenant>.jfrog.io` *and* a `*.cloudfront.net` host.
- Azure DevOps Artifacts — `pkgs.dev.azure.com` *and* a separate CDN/blob host for downloads.
- Sonatype Nexus with S3 blob storage — the Nexus host *and* the S3 host.

**If this did not resolve the issue,** include the full list of distinct hosts you observed (or the verbose `pip` output, with credentials redacted), and the current value of `API_ALLOWED_PREFIXES` from `DESCRIBE INTEGRATION` when you contact Snowflake support.

### Repro #4 — Smallest possible repro inside Snowflake

Use this once Repro #2 and Repro #3 have confirmed your repository is reachable and configured. The goal is a clean, isolated `query_id` that Snowflake support can trace.

Copy code

```
CREATE OR REPLACE FUNCTION repro_install()
  RETURNS STRING
  LANGUAGE PYTHON
  RUNTIME_VERSION = '3.13'
  ARTIFACT_REPOSITORY = <your_repo>
  PACKAGES = ('<single_package>==<version>')
  HANDLER = 'run'
AS $$
def run(): return "ok"
$$;

SELECT repro_install();
SELECT LAST_QUERY_ID();
```

Tips:

- Test packages **one at a time**. If `setuptools` is blocked upstream, every install will look broken.
- Try a different `RUNTIME_VERSION` (`3.11`, `3.12`, `3.13`) — wheels often exist for one Python version but not another.

**If this did not resolve the issue,** include the failing UDF SQL, the `query_id` from `SELECT LAST_QUERY_ID();`, and the full untruncated error message when you contact Snowflake support.

### Other common pitfalls

- **Upstream-side blocks (quarantine, ACL).** Your repository can refuse to serve specific packages or versions — Nexus quarantine, Azure DevOps ACLs, JFrog repository rules. Snowflake surfaces these as HTTP 403 errors. Confirm with your repository administrator. Snowflake Package Policy does *not* apply to customer-hosted repositories — governance for those objects lives entirely in your upstream.
- **Pinning around blocked transitive deps.** If an indirect dep (e.g. `setuptools<82`) is blocked, pin around it: `PACKAGES = ('mypkg==1.2', 'setuptools<82')`.
- **Python runtime mismatch.** Wheels exist for 3.10 but not 3.11 (or vice versa). Try the other runtime.
- **Trailing slash on** `INDEX_URL`. `pip` cares about the trailing `/simple/`. Re-paste the URL from `DESCRIBE` and visually check it.
- **Token rotated on your side.** Update the secret with `ALTER SECRET ... SET PASSWORD = '<new>'` (re-test with Repro #2 first).
- **Embedded credentials in** `INDEX_URL`. Not allowed. Use a `SECRET`.
- **Handler / file-naming typos.** The package may install fine and the real failure is `ModuleNotFoundError` for *your* code, not the package.

### When you contact Snowflake support

If the steps above have not resolved the issue, [submit a support case](/user-guide/ui-support) and provide as much of the following information as possible:

- Your account locator and region.
- The `query_id` from the failing call (`SELECT LAST_QUERY_ID();` right after the failure).
- The **full** error message — do not truncate. The upstream URL embedded in the error is the most diagnostic single piece of information.
- DDL of the `SECRET` (with `PASSWORD` redacted), the `API INTEGRATION`, and the `ARTIFACT REPOSITORY`, exactly as `DESCRIBE` returns them.
- Output of `SELECT SYSTEM$GET_ARTIFACT_REPOSITORY_INFO('<repo>');`.
- Output of `SELECT SYSTEM$GET_PRIVATELINK_ENDPOINTS_INFO();` if you’re using PrivateLink.
- The exact `curl` and `pip install` commands you ran in Repros #2 and #3, **with credentials redacted**, and their outputs.
- Repository platform and edition (JFrog Cloud, JFrog self-hosted, Sonatype Nexus, Azure DevOps Artifacts, GCP Artifact Registry, AWS CodeArtifact, other).
- Whether the connection is over the public Internet or PrivateLink.

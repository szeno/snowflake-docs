# Migrate from dbt Core to dbt Projects on Snowflake

This is a step-by-step guide for teams moving from standard dbt Core to dbt Projects on Snowflake.
The goal is to take the dbt Core project you run today (in your local IDE, kicked off by an orchestrator such as Airflow)
and get it running natively inside Snowflake, with as little change as possible. Most of your
project files stay exactly the same.

The setup steps require an admin role. Every step shows
copy-pastable SQL, and where possible, the equivalent clicks in Snowsight.

## What changes (and what doesn’t)

Good news first: your `models/`, `seeds/`, `macros/`, `tests/`, `dbt_project.yml`, and
`packages.yml` files don’t need to change. dbt is still dbt.

Here’s the short list of what’s different when dbt runs inside Snowflake:

| Topic | dbt Core today | dbt Projects on Snowflake |
| --- | --- | --- |
| Where you edit and run | Local IDE + terminal | **Snowflake Workspaces** (a web IDE in Snowsight) or Cortex Code Desktop |
| What kicks off runs | Third-party orchestrator such as Airflow | **Snowflake tasks** (scheduled SQL) |
| Connection / auth | `profiles.yml` with account, user, password | [`dbt_projects_profiles.yml`](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file) or `profiles.yml` in the project root, **no account, user, or password needed** |
| dbt engine | Whatever you installed | Choose a Snowflake-managed runtime, for example **1.11.11** (dbt Core) or **2.0.0-preview.186** (dbt Fusion). No installs. |
| Getting packages (`dbt deps`) | Runs locally | Runs in Snowflake using an **external access integration** |
| Deploying | n/a | A **dbt project object** with one mutable live version in Snowflake |

Expand

Show lessSee more

The seven steps this guide walks through:

1. [Set up Workspaces (and pick the dbt runtime)](#label-dbt-migrate-step1)
2. [(Optional) Set up PrivateLink to your Git server](#label-dbt-migrate-step2)
3. [Connect a Git repository with OAuth2](#label-dbt-migrate-step3)
4. [Move your profile file into the project root](#label-dbt-migrate-step4)
5. [Create an external access integration (one-time) and grant USAGE to data engineers](#label-dbt-migrate-step5)
6. [Migrate environment variables](#label-dbt-migrate-step6)
7. [Deploy the project and schedule it with a task](#label-dbt-migrate-step7)

For Git connectivity, steps 2 and 3 cover the two authentication choices: OAuth2 for interactive
development with any provider (recommended), or a personal access token when you’re on PrivateLink
or setting up automated access.

**Related docs:**

- [dbt Projects on Snowflake overview](/user-guide/data-engineering/dbt-projects-on-snowflake)
- [Tutorial: Get started with dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-getting-started-tutorial)
- [Access control for dbt Projects](/user-guide/data-engineering/dbt-projects-on-snowflake-access-control)

## Step 1: Set up Workspaces

Workspaces are a web-based IDE inside Snowsight. They’re the easiest way to get a dbt Core
project running on Snowflake: you can edit files, run `dbt compile` / `dbt run` / `dbt build`,
see the DAG, and deploy, all from the browser. No local install required.

**Related docs:**

- [Workspaces for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-using-workspaces)
- [Workspaces overview](/user-guide/ui-snowsight/workspaces)

### Pick the dbt runtime version

Snowflake runs your project on a managed dbt runtime. The version you choose decides the engine:
a `1.x` version runs dbt Core (Python); a `2.x` version runs dbt Fusion (Rust). Pin to whichever
version your team already has experience with.

You can set the default for the whole account so nobody has to specify it every time. This also
sets the initial runtime version that Workspaces use:

Copy code

```
-- Account-level default (requires an admin role). Workspaces use this as their initial runtime.

-- To default to dbt Core 1.11.11:
ALTER ACCOUNT SET DEFAULT_DBT_VERSION = '1.11.11';

-- Or, to default to dbt Fusion:
ALTER ACCOUNT SET DEFAULT_DBT_VERSION = '2.0.0-preview.186';
```

To see what versions are available at any time:

Copy code

```
SELECT SYSTEM$SUPPORTED_DBT_VERSIONS();
```

You can always override the version on an individual project later (shown in step 6).

If you ever need to move other dbt Core projects to Fusion, see [Migrate to dbt Fusion](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions#label-dbt-fusion-migration).

**Related docs:** [Supported dbt versions](/user-guide/data-engineering/dbt-projects-on-snowflake-dbt-core-versions)

### Things to know before you start

A few things that trip people up with Workspaces:

- **Workspaces are personal by default:** Each user’s workspace lives in their own personal
  database and isn’t shared. If you want several people to collaborate in the same workspace, create
  a **shared workspace** in a regular database and schema instead. See
  [Workspaces overview](/user-guide/ui-snowsight/workspaces).
- **100,000 file limit when you deploy a dbt project object:** The limit applies to the individual
  dbt project folder you deploy, not to the workspace as a whole. It counts everything in that
  folder, including the `target/`, `dbt_packages/`, and `logs/` folders that dbt generates. Large
  projects with big package trees can bump into this. Contact your account representative if your
  team has a project larger than this threshold.
- **A `dbt_projects_profiles.yml` or `profiles.yml` file is required in each project folder** (covered in step 4).
- **Public repos are read-only:** If you connect a public Git repo, you can pull but you can’t
  commit and push back from the workspace. For your real project, connect it as a private
  repo with OAuth2 (step 3).
- **Fusion runs `dbt deps` automatically:** When you’re on Fusion and your `packages.yml` lists
  packages but there’s no `dbt_packages` folder yet, Fusion quietly runs `dbt deps` during
  `dbt compile` / `dbt run`, which needs internet access. Workspaces make this painless: an admin
  creates the external access integration once and grants `USAGE` to your role (step 5). After you select your EAI, it stays pre-selected for every command that might need it, so you don’t have to think about it again.

## Step 2: (Optional) Set up PrivateLink to your Git server

Note

Skip this entire step and go to step 3 unless your Git server is reachable only over PrivateLink
(no public internet access). Most teams connect to their Git provider over the public internet and
don’t need this step.

PrivateLink is a dedicated private network connection between Snowflake and your Git server, so Git
traffic never crosses the public internet. Setting it up is a one-time admin task that must be done
before you connect your repository in step 3, and it only works when Snowflake and your Git server
are in the same cloud and region. Note that OAuth2 doesn’t work over PrivateLink, so on this path you
authenticate with a token instead.

1. On your cloud provider, create a private link service that accepts requests from Snowflake (see
   the walkthrough linked below).
2. In Snowflake, provision the outbound private endpoint with your private link service ID and your
   Git server’s domain (AWS example shown; Azure and Google Cloud use their own service ID format):

   Copy code

   ```
   SELECT SYSTEM$PROVISION_PRIVATELINK_ENDPOINT(
     'com.amazonaws.vpce.us-west-2.vpce-svc-xxxxxxxx',   -- your private link service ID
     'git.example.com'                                   -- your Git server domain
   );
   ```
3. Accept the endpoint on your cloud provider, then check its status:

   Copy code

   ```
   SELECT SYSTEM$GET_PRIVATELINK_ENDPOINTS_INFO();
   ```
4. Create the API integration with `USE_PRIVATELINK_ENDPOINT = TRUE` and token-based
   authentication (a secret holding a personal access token). Add `TLS_TRUSTED_CERTIFICATES` if your
   server uses a self-signed certificate:

   Copy code

   ```
   CREATE OR REPLACE SECRET git_pat_secret
     TYPE = password
     USERNAME = 'your-git-username'
     PASSWORD = 'your-personal-access-token';

   CREATE OR REPLACE API INTEGRATION git_api_integration
     API_PROVIDER = git_https_api
     API_ALLOWED_PREFIXES = ('https://git.example.com/my-workspace')
     ALLOWED_AUTHENTICATION_SECRETS = (git_pat_secret)
     USE_PRIVATELINK_ENDPOINT = TRUE
     ENABLED = TRUE;
   ```

   For most providers, `USERNAME` is your actual Git username. For Bitbucket, set `USERNAME`
   literally to the string `x-token-auth` (a Bitbucket convention) and put your token in `PASSWORD`:

   Copy code

   ```
   -- Bitbucket example
   CREATE OR REPLACE SECRET git_pat_secret
     TYPE = password
     USERNAME = 'x-token-auth'              -- literal value, not your username
     PASSWORD = 'your-bitbucket-access-token';
   ```

   After you finish this step, skip the OAuth options in step 3 and go straight to
   [Create the Git-connected workspace](#label-dbt-migrate-create-workspace). Each developer repeats
   this workspace creation step for themselves: select **Personal access token** as the
   authentication method and point it at the secret.

### Shared token or a token per developer

The secret you created above holds one Git username and one personal access token, so it represents
a single Git identity. Decide how your team uses Git tokens:

- **A secret per developer (individual attribution):** For per-developer attribution and
  per-developer repository permissions, each developer creates their own secret with their own Git
  username and personal access token, then points their workspace at it. In the workspace creation
  dialog, they select **Personal access token** and choose their secret, or create one inline with
  **+ Secret**.
- **One shared secret (service-account model):** Everyone who has READ on the secret authenticates
  and pushes as that one identity, with that identity’s repository permissions. On your Git server,
  pushes are attributed to that account no matter who ran them from Snowflake.

The admin still creates the API integration once. Only the secret is per developer. If you use
per-developer secrets, list each one in `ALLOWED_AUTHENTICATION_SECRETS`, or set it to `ALL`.

Note

The author name and email you set in Workspaces only change the commit metadata. They don’t change
the authenticating identity: the personal access token in the secret still determines which Git
account the push runs as.

**Related docs:**

- [Connect to a Git repository over a private network](/developer-guide/git/git-setting-up-private)

## Step 3: Connect your Git repository with OAuth2

Workspaces sync to a branch in your Git repo, so you keep your normal Git workflow (branches,
commits, pull requests). The cleanest sign-in experience for interactive development is OAuth2:
your team signs in to the Git provider once and Snowflake handles the rest, no tokens to paste or
rotate.

OAuth2 works for every supported provider over the public internet: GitHub, GitLab, Azure DevOps,
Bitbucket Cloud, and any other OAuth2 provider. It isn’t a GitHub-only option. You need a personal
access token instead of OAuth2 in only two cases:

- Your Git server is reachable only over PrivateLink. OAuth2 doesn’t work over a private link, so
  you authenticate with a token instead (see [step 2](#label-dbt-migrate-step2)).
- You’re setting up non-interactive, automated access such as a CI/CD pipeline, where nobody is
  present to complete an interactive sign-in.

Note

If you don’t intend to use Workspaces in your initial onboarding to dbt Projects on Snowflake,
you can skip this section. Your team can still use the Snowflake CLI (shown in step 6) to deploy
dbt project objects and schedule them.

The setup is two parts: an admin creates an **API integration** that tells Snowflake how to talk to
your Git provider, and each user signs in with OAuth when they create a Git-connected workspace.

Tip

If you completed step 2 (PrivateLink), you already created your token-based API integration.
Skip the OAuth options below and go straight to
[Create the Git-connected workspace](#label-dbt-migrate-create-workspace).

### Redirect URI (required for all providers except GitHub)

Most OAuth2 providers ask for a redirect URI (also called a callback URL) when you register an
OAuth application. This is a fixed Snowflake URL based on your account’s region. It is **not**
generated by the API integration. The pattern is:

```
https://apps-api.c1.<region>.<cloud>.app.snowflake.com/oauth/complete-secret
```

For example, an account in AWS US West (Oregon) uses:

```
https://apps-api.c1.us-west-2.aws.app.snowflake.com/oauth/complete-secret
```

You set this URL as the callback when you create the OAuth app, and the provider then gives you the
client ID and client secret that you plug into the API integration. The GitHub option below skips
this. The Snowflake GitHub App handles the redirect URI for you.

To let Snowflake build the whole URL for you, run this and copy the result:

Copy code

```
SHOW REGIONS;
SELECT DISTINCT
  'https://apps-api.c1.' || "region" || '.' || "cloud" || '.app.snowflake.com/oauth/complete-secret'
    AS redirect_uri
FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
WHERE "snowflake_region" = SPLIT_PART(CURRENT_REGION(), '.', -1);
```

### Create the API integration for your Git provider

Pick your Git provider to see the setup steps:

GitHubGitLabAzure DevOpsBitbucket CloudOther provider

GitHub needs the least admin setup. Every provider in the tabs below uses the same OAuth2 sign-in
flow, but GitHub skips the OAuth application registration and redirect URI: Snowflake publishes a
pre-built OAuth app (the **Snowflake GitHub App**), so the admin just creates an API integration
that points at it:

Copy code

```
-- Run as an admin role (needs CREATE API INTEGRATION).
CREATE OR REPLACE API INTEGRATION git_api_integration
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://github.com/my-org')   -- your GitHub org or account URL
  API_USER_AUTHENTICATION = (TYPE = SNOWFLAKE_GITHUB_APP)
  ENABLED = TRUE;
```

On first sign-in, GitHub asks an org admin to authorize the `snowflakedb` app; after that,
everyone in the account can use it.

The Snowflake GitHub App is at [github.com/apps/snowflakedb](https://github.com/apps/snowflakedb).

For GitLab, you register an OAuth application on the GitLab side, then create an API integration
in Snowflake with the OAuth2 details. (OAuth for providers other than GitHub is currently in
preview, but fully usable.)

Register an OAuth application in GitLab, setting its callback URL to the Snowflake redirect URI
described above. Request these scopes: `read_api`, `read_repository`, and `write_repository`.
GitLab gives you a **client ID** and **client secret** to use next.

Then create the API integration (run as an admin role). The endpoints below are for GitLab.com; for
a self-managed GitLab, swap in your own host:

Copy code

```
CREATE OR REPLACE API INTEGRATION git_api_integration
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://gitlab.com/my-group')   -- your GitLab group or account URL
  API_USER_AUTHENTICATION = (
    TYPE = OAUTH2
    OAUTH_AUTHORIZATION_ENDPOINT = 'https://gitlab.com/oauth/authorize'
    OAUTH_TOKEN_ENDPOINT = 'https://gitlab.com/oauth/token'
    OAUTH_CLIENT_ID = '<your_gitlab_client_id>'
    OAUTH_CLIENT_SECRET = '<your_gitlab_client_secret>'
    OAUTH_ACCESS_TOKEN_VALIDITY = 3600
    OAUTH_REFRESH_TOKEN_VALIDITY = 2592000
    OAUTH_ALLOWED_SCOPES = ('read_api', 'read_repository', 'write_repository')
  )
  ENABLED = TRUE;
```

Azure DevOps uses the same generic OAuth2 flow as GitLab. Register an OAuth application in Azure
DevOps, setting its callback URL to the Snowflake redirect URI described above, then create the API
integration with Azure DevOps’s endpoints and scopes. Because those values are provider-specific
(and Microsoft is shifting toward Microsoft Entra ID), get the exact current values from the
[Snowflake quickstart for Azure DevOps OAuth](https://www.snowflake.com/en/developers/guides/snowflake-git-oauth-azure-devops/).

Copy code

```
CREATE OR REPLACE API INTEGRATION git_api_integration
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://dev.azure.com/my-organization')   -- your Azure DevOps org URL
  API_USER_AUTHENTICATION = (
    TYPE = OAUTH2
    OAUTH_AUTHORIZATION_ENDPOINT = '<azure_devops_authorization_endpoint>'
    OAUTH_TOKEN_ENDPOINT = '<azure_devops_token_endpoint>'
    OAUTH_CLIENT_ID = '<your_client_id>'
    OAUTH_CLIENT_SECRET = '<your_client_secret>'
    OAUTH_ACCESS_TOKEN_VALIDITY = 3600
    OAUTH_REFRESH_TOKEN_VALIDITY = 2592000
    OAUTH_ALLOWED_SCOPES = ('<azure_devops_scopes>')
  )
  ENABLED = TRUE;
```

Register an OAuth consumer in Bitbucket under **Workspace settings** > **OAuth consumers** with
the **Write** repository permission, and set its callback URL to the Snowflake redirect URI
described above. The consumer’s **Key** and **Secret** are your `OAUTH_CLIENT_ID` and
`OAUTH_CLIENT_SECRET`.

For a full step-by-step with screenshots, see the
[Connect Snowflake to Bitbucket with OAuth2 quickstart](https://www.snowflake.com/en/developers/guides/snowflake-git-oauth-bitbucket/).

Copy code

```
CREATE OR REPLACE API INTEGRATION git_api_integration
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://bitbucket.org/my-workspace')   -- your Bitbucket workspace URL
  API_USER_AUTHENTICATION = (
    TYPE = OAUTH2
    OAUTH_AUTHORIZATION_ENDPOINT = 'https://bitbucket.org/site/oauth2/authorize'
    OAUTH_TOKEN_ENDPOINT = 'https://bitbucket.org/site/oauth2/access_token'
    OAUTH_CLIENT_ID = '<your-consumer-key>'
    OAUTH_CLIENT_SECRET = '<your-consumer-secret>'
    OAUTH_ACCESS_TOKEN_VALIDITY = 7200
    OAUTH_REFRESH_TOKEN_VALIDITY = 31536000
    OAUTH_ALLOWED_SCOPES = ('repository:write')
    OAUTH_USERNAME = 'x-token-auth'   -- required for Bitbucket; Git ops fail after sign-in without it
  )
  ENABLED = TRUE;
```

Note

Bitbucket behind outbound PrivateLink? OAuth2 is **not supported** over an outbound private link
to a Git provider. Skip this option and use the token-based
[PrivateLink step](#label-dbt-migrate-step2) (step 2) instead. This option is for Bitbucket
Cloud reached over the public internet.

For any other provider that supports OAuth2 (a self-managed Git server, and so on), use the
generic template. Register an OAuth application with your provider, setting its callback URL to
the Snowflake redirect URI described above, then fill in your provider’s endpoints, client
credentials, and scopes:

Copy code

```
CREATE OR REPLACE API INTEGRATION git_api_integration
  API_PROVIDER = git_https_api
  API_ALLOWED_PREFIXES = ('https://git.example.com/my-account')   -- your provider/repo base URL
  API_USER_AUTHENTICATION = (
    TYPE = OAUTH2
    OAUTH_AUTHORIZATION_ENDPOINT = '<your_oauth_authorization_endpoint>'
    OAUTH_TOKEN_ENDPOINT = '<your_oauth_token_endpoint>'
    OAUTH_CLIENT_ID = '<your_client_id>'
    OAUTH_CLIENT_SECRET = '<your_client_secret>'
    OAUTH_ACCESS_TOKEN_VALIDITY = 3600
    OAUTH_REFRESH_TOKEN_VALIDITY = 2592000
    OAUTH_ALLOWED_SCOPES = ('<your_scopes>')
  )
  ENABLED = TRUE;
```

For provider-specific values, see the [Set up OAuth for Git integration by provider](https://community.snowflake.com/s/article/Set-up-OAuth-for-Git-integration-by-provider) article.

### Create the Git-connected workspace

Note

The admin creates the API integration once for the whole account. After that, each developer
repeats the steps below to create their own workspace and sign in with OAuth2. For GitHub, the
first sign-in prompts an organization admin to authorize the `snowflakedb` app once, and then
everyone in the account can sign in.

Once the API integration exists, anyone with USAGE on it can create a workspace from the repo:

1. Sign in to Snowsight.
2. In the navigation menu, select **Projects** > **Workspaces**.
3. In the **Workspaces** menu, select **From Git repository**.
4. Paste the repository URL (for example, `https://github.com/my-org/analytics` or
   `https://gitlab.com/my-group/analytics`).
5. Give the workspace a name.
6. Under **API Integration**, select `git_api_integration`.
7. For the authentication method, select **OAuth2**, then **Sign in** and authorize Snowflake to
   access the repository. Grant read access to metadata and read/write access to code so you can
   pull and push.
8. Select **Create**.

Snowflake clones the repo and opens the workspace with your dbt project files ready to edit.

**Related docs:**

- [Choosing how to set up Git](/developer-guide/git/git-setting-up)
- [OAuth setup details](/developer-guide/git/git-setting-up-public)
- [Connecting a workspace to Git](/user-guide/ui-snowsight/workspaces-git)
- [CREATE API INTEGRATION](/sql-reference/sql/create-api-integration)

## Step 4: Move your profile file into the project root

In dbt Core, your `profiles.yml` usually lives outside the project (in `~/.dbt/`) and holds your
account, user, and password. On Snowflake, you bring that file into the **root of the dbt project
folder**, and drop the sensitive bits.

Why it’s simpler: the project already runs inside Snowflake, under the signed-in user and account.
So dbt doesn’t need an `account`, a `user`, or a `password`. The `account` and `user` keys can be
left as empty or placeholder strings (dbt still expects the keys to exist), and there’s no password
field at all.

For hybrid teams (teams where some members plan to continue using local `dbt` CLI and others want to start using Workspaces), we recommend using the `dbt_projects_profiles.yml` file because it lets you adopt dbt Projects on Snowflake without changing your existing development workflows. Local `dbt` CLI runs continue to read `~/.dbt/profiles.yml` outside the project exactly as before, while `dbt_projects_profiles.yml` inside the project root handles Snowflake-managed runs (Workspaces, Cortex Code Desktop Snowflake-managed mode, dbt project objects). This way, you can move back and forth between local dbt and Snowflake-managed runs without swapping connection settings.

Note

If both files are present in the project root, Snowflake uses `dbt_projects_profiles.yml` in Workspaces, Cortex Code Desktop in Snowflake-managed mode, and the dbt project object. If `dbt_projects_profiles.yml` isn’t present, Snowflake uses `profiles.yml` as before.

Here’s a `dbt_projects_profiles.yml` or `profiles.yml` you can drop in. It defines a `dev` and a `prod` target:

Copy code

```
my_project:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: 'not needed'   # ignored on Snowflake; runs under the current account
      user: 'not needed'      # ignored on Snowflake; runs as the current user
      role: transformer
      database: dev_db
      schema: analytics
      warehouse: dbt_wh
      threads: 8
    prod:
      type: snowflake
      account: 'not needed'
      user: 'not needed'
      role: transformer
      database: prod_db
      schema: analytics
      warehouse: dbt_wh
      threads: 8
```

There’s no `password`, no `authenticator`, no key-pair path. That’s the point: nothing secret
lives in the file.

Once `dbt_projects_profiles.yml` or `profiles.yml` is in the project root with at least one valid target, each target shows up in
the **Profile** picker in the workspace toolbar. Pick a profile, pick a command (`compile`, `run`,
`build`), and run it.

**Related docs:**

- [Use dbt\_projects\_profiles.yml for a unified development-to-production experience](/user-guide/data-engineering/dbt-projects-on-snowflake-best-practices#label-dbt-projects-profiles-file)
- [Workspaces for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-using-workspaces)
- [dbt integration in Cortex Code Desktop](/user-guide/cortex-code/cortex-code-desktop/dbt-integration)

## Step 5: Create an external access integration for dbt packages

If your project uses packages in `packages.yml` (for example, `dbt-labs/dbt_utils`), dbt needs
to reach out to the internet to download them when it runs `dbt deps`. Snowflake blocks outbound
network access by default, so you give dbt a narrow, allowlisted path with an **external access
integration**.

Creating the network rule and external access integration is a **one-time admin operation** for the
account. After that, an admin grants `USAGE` on the integration to the data engineering role.
Engineers then select that integration whenever they run `dbt deps` or deploy a dbt project object that needs
remote packages. This integration never needs to be recreated.

This matters extra for Fusion: as noted in the gotchas, Fusion auto-runs `dbt deps` during
`compile`/`run` when packages are declared but not yet downloaded. Without external access, that
step fails with a network error. Setting this up once avoids that.

Run the following as an admin role:

Copy code

```
-- 1. Allowlist the hosts dbt needs to download packages.
CREATE OR REPLACE NETWORK RULE dbt_network_rule
  MODE = EGRESS
  TYPE = HOST_PORT
  VALUE_LIST = (
    'hub.getdbt.com',       -- dbt Package hub
    'codeload.github.com'   -- packages hosted on GitHub
  );

-- 2. Wrap the rule in an external access integration that dbt can use.
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION dbt_ext_access
  ALLOWED_NETWORK_RULES = (dbt_network_rule)
  ENABLED = TRUE;

-- 3. Grant USAGE so data engineers can select and use the integration.
GRANT USAGE ON INTEGRATION dbt_ext_access TO ROLE data_engineer;
```

Replace `data_engineer` with the role your team uses to run dbt in Workspaces or to deploy dbt
project objects. Grant `USAGE` to each role that needs to run `dbt deps` or attach the integration
at deploy time. You create the integration once, and onboarding a new role after that is just
another `GRANT`.

To populate packages in the workspace, select **Deps** from the command list, choose your external
access integration, and run it. This creates the `dbt_packages` folder and a `package-lock.yml`.

If your team pulls packages from other hosts (a private Git package server, for example), add those
hostnames to the `VALUE_LIST`.

**Related docs:**

- [dbt dependencies and external access](/user-guide/data-engineering/dbt-projects-on-snowflake-dependencies)
- [External network access overview](/developer-guide/external-network-access/creating-using-external-network-access)

## Step 6: Migrate environment variables

If your dbt Core project calls `env_var()` in models, macros, or `profiles.yml`, migrate those variables into an `env.yml` file at the root of your project. Snowflake resolves `env.yml` before each run and injects the values into dbt. Every key must be uppercase and prefixed with `DBT_`.

1. **Scan your project for all `env_var()` calls:** Ask CoCo to list every unique environment variable referenced across your models, macros, and `profiles.yml`.
2. **Add variables to your `env.yml` file:** Use the `env.yml` syntax from [Author your env.yml file](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables#label-dbt-env-vars-author-envyml). Set values to `""` as a placeholder while you decide which ones to hardcode.
3. **Rename each variable to UPPERCASE with the `DBT_` prefix:** For example, `my_schema` becomes `DBT_MY_SCHEMA`. Your values stay the same.
4. **Update the references in your project files:** Ask CoCo to replace every `env_var('OLD_NAME')` call with `env_var('DBT_OLD_NAME')` across your models, macros, and `profiles.yml` in one pass.

For env.yml authoring, environment selection, private Git packages, and the full reference, see [Using SQL environment variables and private Git packages for dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-environment-variables).

## Step 7: Deploy the project and schedule it with a task

Once the project runs cleanly in the workspace, you “ship” it by creating a **dbt project object**.
The object has one mutable live version of your project files in a Snowflake database and schema.
You then schedule it with a **task** (this replaces an Airflow job).

### Deploy as a dbt project object

**Using SQL**: `CREATE DBT PROJECT` copies your code and creates the object’s live version. Point
`FROM` at the workspace’s live version of the project. Attach the external access integration from
step 5 so Fusion can run `dbt deps` during deployment, and pin the Fusion runtime:

Copy code

```
CREATE OR REPLACE DBT PROJECT prod_db.analytics.my_dbt_project
  FROM 'snow://workspace/USER$.PUBLIC."my_dbt_workspace"/versions/live/my_dbt_project'
  DEFAULT_TARGET = 'prod'
  DBT_VERSION = '2.0.0-preview.186'
  EXTERNAL_ACCESS_INTEGRATIONS = (dbt_ext_access)
  COMMENT = 'Analytics dbt project';
```

Note

The `FROM` URL points at your workspace’s live version. The example uses a personal workspace
(the default), whose path is `USER$.PUBLIC."<workspace_name>"`. If you use a shared workspace,
replace `USER$.PUBLIC` with the database and schema that contain the object (for example,
`prod_db.analytics."<workspace_name>"`). The trailing segment (`my_dbt_project`) is the dbt
project folder inside the workspace. The easiest way to get this exactly right is to deploy from
the UI once and copy the `CREATE DBT PROJECT` SQL it prints.

Confirm it exists:

Copy code

```
SHOW DBT PROJECTS IN DATABASE prod_db;
```

To update the live version without replacing the object, run `ALTER DBT PROJECT ... DEPLOY`:

Copy code

```
ALTER DBT PROJECT prod_db.analytics.my_dbt_project
  DEPLOY
  FROM 'snow://workspace/USER$.PUBLIC."my_dbt_workspace"/versions/live/my_dbt_project';
```

**Using the UI**: In the workspace, select **Connect** > **Deploy dbt project**, choose the target
database and schema, choose **Create dbt project**, give it a name, optionally set a default target
and the external access integration, then select **Deploy**. The **Output** tab shows the exact
`CREATE DBT PROJECT` SQL it ran, so the UI and SQL paths produce the same thing.

**CI/CD**: Deploying by hand is the right way to get going. Longer term, we recommend
managing updates to the dbt project object through a CI/CD pipeline using the Snowflake CLI’s
`snow dbt` commands, driven by a GitHub Action or GitLab pipeline. The shape is short and clean:
on a pull request, deploy a tester object to test your code; on merge, update the live production project.

Copy code

```
# CI (on each pull request): deploy a copy to dev, then run + test it
snow dbt deploy my_dbt_project --source ./my_dbt_project --database dev_db --schema analytics --external-access-integration dbt_ext_access
snow dbt execute my_dbt_project --database dev_db --schema analytics build --target dev

# CD (on merge to main): update the live production project object
snow dbt deploy my_dbt_project --source ./my_dbt_project --database prod_db --schema analytics --external-access-integration dbt_ext_access
```

For the full setup (auth, secrets, workflow files), see
[CI/CD integrations on dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-ci-cd)
and the [CI/CD tutorial](/user-guide/tutorials/dbt-projects-on-snowflake-ci-cd-tutorial).

**Related docs:**

- [Deploy dbt project objects](/user-guide/data-engineering/dbt-projects-on-snowflake-deploy)
- [CREATE DBT PROJECT](/sql-reference/sql/create-dbt-project)
- [ALTER DBT PROJECT](/sql-reference/sql/alter-dbt-project)

### Schedule it with a task

A task runs the `EXECUTE DBT PROJECT` command on a schedule. This is the piece that replaces
Airflow. Two rules to remember:

- The task must be in the **same database and schema** as the dbt project object.
- Tasks that run dbt must use a **user-managed warehouse** (serverless tasks aren’t supported).

A daily `run` against the `prod` target:

Copy code

```
CREATE OR ALTER TASK prod_db.analytics.run_dbt_project
  WAREHOUSE = dbt_wh
  SCHEDULE = 'USING CRON 0 6 * * * UTC'   -- every day at 06:00 UTC
AS
  EXECUTE DBT PROJECT prod_db.analytics.my_dbt_project
    ARGS = 'run --target prod';
```

You can chain a `test` run right after the `run` finishes:

Copy code

```
CREATE OR ALTER TASK prod_db.analytics.test_dbt_project
  WAREHOUSE = dbt_wh
  AFTER prod_db.analytics.run_dbt_project
AS
  EXECUTE DBT PROJECT prod_db.analytics.my_dbt_project
    ARGS = 'test --target prod';
```

Tasks are created in a suspended state. Resume them to start the schedule (resume the child first,
then the root):

Copy code

```
ALTER TASK prod_db.analytics.test_dbt_project RESUME;
ALTER TASK prod_db.analytics.run_dbt_project RESUME;
```

You can also run a single execution by hand at any time:

Copy code

```
EXECUTE DBT PROJECT prod_db.analytics.my_dbt_project ARGS = 'run --select my_model --target prod';
```

**Using the UI**: From the dbt project menu, select **Create schedule**, set the frequency,
operation (`run`), profile, and any flags (for example, `--select customer_metrics`). Snowflake
creates the same `CREATE TASK` for you.

**Related docs:**

- [Schedule dbt project runs](/user-guide/data-engineering/dbt-projects-on-snowflake-schedule-project-execution)
- [EXECUTE DBT PROJECT](/sql-reference/sql/execute-dbt-project)
- [CREATE TASK](/sql-reference/sql/create-task)
- [Tasks overview](/user-guide/tasks-intro)

## Where to go next

- [Supported dbt commands and flags](/user-guide/data-engineering/dbt-projects-on-snowflake-supported-commands)
- [Monitor dbt Projects on Snowflake](/user-guide/data-engineering/dbt-projects-on-snowflake-monitoring-observability)
- [Tutorial: Get started with dbt Projects on Snowflake](/user-guide/tutorials/dbt-projects-on-snowflake-getting-started-tutorial)

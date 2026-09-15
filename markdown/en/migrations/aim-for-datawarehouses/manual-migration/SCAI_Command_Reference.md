# SnowConvert AI CLI Command Reference

CLI tool for accelerated database migration to Snowflake.

---

## Global options

| Option | Description |
| --- | --- |
| `-h, --help` | Show help message |
| `-v, --version` | Display version information |
| `--log-debug` | Global flag to enable debug-level logging for any command. Can also be set via SCAI\_LOG\_LEVEL env var (accepts: verbose, debug, information, warning, error, fatal). |
| `--json` | Emit a JSON envelope to stdout (success, warnings, errors, and command-specific result) for automation, CI/CD, and agent-driven workflows that need structured machine context. Recognized anywhere on the command line. |

Expand

Show lessSee more

### JSON output

When –json is present, the CLI writes a single JSON document to stdout at the end of the command (envelope with success, warnings, errors, and an optional result object). Human-oriented tables and markup are suppressed for commands that implement JSON mode.

**Commands with structured result:**

- `scai code extract`
- `scai code convert`
- `scai code deploy`
- `scai code add`
- `scai code resync`
- `scai code find`
- `scai code sync`
- `scai code sync --continue`
- `scai query`
- `scai connection list`
- `scai connection test`
- `scai project info`
- `scai project status`
- `scai settings list`
- `scai settings get`
- `scai settings set`
- `scai settings unset`
- `scai data migrate create-workflow`
- `scai data migrate status`
- `scai data migrate list`
- `scai data migrate generate-config`
- `scai data migrate pause`
- `scai data migrate resume`
- `scai data migrate cancel`
- `scai data validate create-workflow`
- `scai data validate status`
- `scai data validate list`
- `scai data validate generate-config`
- `scai data validate pause`
- `scai data validate resume`
- `scai data validate cancel`
- `scai data orchestrator setup`
- `scai data orchestrator start`
- `scai data orchestrator stop`
- `scai data orchestrator status`
- `scai data worker setup`
- `scai data worker start (--auto-config)`
- `scai data worker stop`
- `scai data worker status`
- `scai data worker generate-config`
- `scai versions`
- `scai versions remove`
- scai code find always sets the envelope result payload (items, total, truncated); when –json is not used, the no-op envelope writer discards it and the table is shown instead.
- Every command in commandsWithStructuredResult attaches a command-specific result when –json is active. Keep this list aligned with GlobalHelpJsonOverview.StructuredEnvelopeResultCommands in the CLI source.

## Quick start

Basic workflow to get started:

1. Create a project (use -c to set default Snowflake connection)

Copy code

```
scai init -n <name> -l <language> -c <connection>
```

2. Add source code (extract from source DB: SqlServer, Redshift, Teradata, Oracle, Postgresql, BigQuery, AzureSynapse)

Copy code

```
scai code extract
```

3. Add source code (other languages)

Copy code

```
scai code add -i <path>
```

4. Convert to Snowflake SQL

Copy code

```
scai code convert
```

5. Deploy to Snowflake

Copy code

```
scai code deploy --all
```

> Using -c `<connection>` saves the Snowflake connection in the project, avoiding the need to specify it for each command.

> For commands that only need Snowflake account/user metadata (for example code extract and code convert), the CLI reads your local Snowflake CLI config (TOML) first without opening a live session. If account and user cannot be read from that config while you are online, it falls back to testing the Snowflake connection. Missing or blank account or user in TOML also triggers a live connection test when online.

> Global –json prints one JSON envelope to stdout (success, warnings, errors, and an optional command-specific result) for automation, CI/CD, and agents. It can appear anywhere on the command line. See jsonOutput.commandsWithStructuredResult for the complete list of commands that attach a structured result payload.

> Run `scai <command> -h` for detailed help on any command.

---

## Commands

| Command | Description |
| --- | --- |
| `scai init` | Create a new migration project |
| `scai project` | View and manage project configuration |
| `scai connection` | Manage source database connections (SqlServer, Redshift, Teradata, Oracle, Postgresql, BigQuery, AzureSynapse) |
| `scai code` | Code operations: extract, convert, add, deploy, find, where |
| `scai data` | Data operations: migrate, validate, worker, orchestrator, doctor |
| `scai assessment` | Generate migration planning insights from source code and SnowConvert reports |
| `scai license` | Install offline license for air-gapped environments |
| `scai terms` | View and accept terms and conditions |
| `scai settings` | View and manage user-level CLI settings |
| `scai versions` | List and remove locally installed CLI version directories (user-local installs) |
| `scai object-selector` | Create selector files for filtering objects |
| `scai query` | Execute SQL queries on source database systems |
| `scai test` | Generate test cases for migrated stored procedures |
| `scai logs` | Show log directory and recent log files |
| `scai update` | Force an immediate self-update on the current channel |

Expand

Show lessSee more

### scai init

Create a new migration project in the specified directory (or current directory if PATH is omitted).

Copy code

```
scai init [PATH] -l <LANGUAGE> [-n <NAME>] [-i <INPUT_PATH>] [--code-already-split] [-c <CONNECTION>]
```

**Prerequisites:**

- Target directory must not contain an existing project
- Valid source language must be specified

**Behavior:**

- Creates the project directory structure and configuration files
- When –input-code-path is provided: SqlServer, Redshift, and Teradata run the arrange and parse-and-assess pipeline, promote processed files to source/, and generate a code unit registry; other languages copy source directly to source/
- When –code-already-split is used with –input-code-path (SqlServer, Redshift, and Teradata), skips the arrange/split phase, promotes raw source directly to source/, runs assessment only for code unit registry generation, and marks the project as project type: Full (new folder structure)
- Redshift and Teradata SQL source files (.sql, .ddl, .dml) require paired SC tags (e.g. `-- <sc-table> table_name </sc-table>`) for the arrange step. Script files (.bteq, .btq, .fl, .fload, .ml, .mld, .mload, .tp, .tpump, .tpt) are exempt from SC-tag requirements. If validation (ADD0010) or arrange (ADD0011) fails, the project is still created but source code is not added. Recovery: fix source files and run `scai code add -i <path>`, or use `--code-already-split` if the code is already split

**Supported languages:**

- full migration: SqlServer, Redshift, Teradata, Postgresql, Oracle, BigQuery, AzureSynapse
- codeConversionOnly: Databricks, Greenplum, Sybase, Netezza, Spark, Vertica, Hive, Db2

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `[PATH]` | Optional directory to create the project in. If omitted, uses the current directory. | No |  |
| `-n, --name <NAME>` | Project name. If omitted, defaults to the target folder name. | No |  |
| `-l, --source-language <LANGUAGE>` | Source language for the project | Yes |  |
| `-i, --input-code-path <PATH>` | Path to source code files to add during initialization. SqlServer, Redshift, and Teradata: processed through the arrange and assess pipeline (same as ‘code add’); other languages: copied directly to source/. | No |  |
| `--code-already-split` | Skip the arrange/split phase when source code is already split (SqlServer, Redshift, and Teradata). Proceeds directly to code unit registry generation and marks the project as project type: Full (new folder structure). Requires –input-code-path. | No | False |
| `-c, --connection <NAME>` | Snowflake connection name to save as project default. Precedence: -c option > project connection > default TOML connection. | No |  |

Expand

Show lessSee more

**Project folder structure:**

| Path | Description |
| --- | --- |
| `.scai/` | Project configuration |
| `.scai/config/` | project.yml (shared), project.local.yml (workspace-local defaults), and related config |
| `artifacts/` | Intermediate processing artifacts (source\_raw, source\_raw\_Processed) |
| `source/` | Processed source code (populated by –input-code-path or ‘code add’) |
| `snowflake/` | Converted code, reports, and logs |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Create a project in a new folder (recommended)
scai init my-project -l Teradata

# Create a project in the current directory
scai init -l Teradata

# Create project with source code
scai init my-project -l Oracle -i /path/to/code

# Create project with pre-split source code (skip arrange phase)
scai init my-project -l SqlServer -i /path/to/code --code-already-split

# Create project with a specific connection
scai init my-project -l Oracle -c my-snowflake-conn
```

---

### scai project

View and manage project configuration

#### scai project info

Display project details including name, source language, and status.

Copy code

```
scai project info
```

**Prerequisites:**

- Must be run from within a migration project directory

**Behavior:**

- With global –json, prints only the JSON envelope; the result object includes project id, name, source language, project type (raw and display strings), explanations, created metadata, optional description and cloud project id, schema version, connectionDefaults (Snowflake and source defaults split into shared project.yml vs workspace-local project.local.yml), and a localYamlNote string.

**Output:** Project details displayed

- Project Name: Name of the migration project
- Project ID: Unique identifier (MIGRATION\_PROJECT\_ prefix)
- Source Language: Source database dialect (e.g., Teradata, Oracle)
- Snowflake Connection: Default connection name (if configured)
- Source Connection: Default source connection name (if configured)
- Project Root: Absolute path to project directory

**Examples:**

Copy code

```
# Show current project details
scai project info

# Machine-readable project details
scai project info --json
```

---

#### scai project status

Show project.yml context and Code Unit Registry snapshot (read-only).

Copy code

```
scai project status [OPTIONS]
```

**Prerequisites:**

- Must be run from within a migration project directory

**Behavior:**

- Shows project context from project.yml: absolute project root, project id, project type, source dialect, created metadata, optional description and cloud project id, default Snowflake connection
- When environments are defined in project.yml, shows a table with Snowflake database, schema, and description per environment (non-secret)
- When the registry is initialized, reads code units from the Code Unit Registry; when not, prints project context with registry metrics zeroed and an uninitialized-registry warning
- Registry overview: one table with registered, converted, deployable; with –full, inventory adds object types from Target.ObjectType and source locations from Source database/schema
- Deployable counts converted code units that pass registry deploy checks (required registry fields and no issues whose codes are in a small explicit deploy-blocking set; registry severity/level fields are not used). Missing references count reflects assessment failures (migration completeness)
- SQL drift from FindSqlFileChanges: modified tracked SQL vs non-modified file-change types and untracked paths; console warns when the drift query fails
- Registry overview includes a dim one-line EWI/FDM/PRF/OOS instance total (category totals)
- Aggregates conversion issues (EWIs, FDMs, PRFs, OOS) from registry issue entries
- Objects ranked by issue load and most common issue codes appear on the console only with –full (row caps 10 / 12 where documented)
- Ranks code units by total conversion issue instances (sum of Count for issues with non-empty codes); top rows shown with –full
- With global –json, prints only the JSON envelope; the result object has full (boolean, same as –full) and status (aggregated ProjectStatusData: registry snapshot, project context, and metrics) instead of formatted tables.

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `--full` | Show extended tables (inventory, issue rankings, most common codes). Default omits these. | No |

Expand

Show lessSee more

**Output:** Teal header. Bold subsection titles directly above tables (no blank line between title and table). Default: project context, environments, registry overview, code unit registry summary. –full adds inventory (object types / source locations, first 12 each), issue rankings (10 rows), most common codes (10 rows), plus extra SQL drift prose when unsynced. Dim footer notes metrics are from the code unit registry.

**Examples:**

Copy code

```
# Show project status
scai project status

# Extended tables (inventory and issues)
scai project status --full

# Machine-readable status snapshot
scai project status --json

# Machine-readable extended status
scai project status --full --json
```

---

### scai project defaults

##### scai project defaults set

Set project-level defaults (Snowflake connection, source connection, warehouse, database, schema). Values are tested before save; saved connection profiles are not modified. Always writes to project.local.yml to prevent credentials from being committed to version control.

Copy code

```
scai project defaults set [[-c <NAME>]] [[-s <NAME>]] [[--warehouse <NAME>]] [[--database <NAME>]] [[--schema <NAME>]] [[--role <NAME>]]
```

**Prerequisites:**

- A migration project initialized with ‘scai init’
- Connections must exist in connections.toml or config.toml

**Behavior:**

- Only provided flags are persisted for the project
- Always writes to project.local.yml (gitignored), never to the shared project.yml
- Snowflake fields: loads saved connection profiles, merges existing project Snowflake defaults to your current connection without modifying it, then tests it
- Source (-s): tests the source connection for the project’s source language and defines it as the project’s default source connection (if valid)

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-c, --connection <NAME>` | Snowflake connection profile name to store as project default. | No |
| `-s, --source-connection <NAME>` | Source connection profile name to store as project default. | No |
| `--warehouse <NAME>` | Project default Snowflake warehouse. | No |
| `--database <NAME>` | Project default Snowflake database. | No |
| `--schema <NAME>` | Project default Snowflake schema. | No |
| `--role <NAME>` | Project default Snowflake role. | No |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Set project Snowflake connection
scai project defaults set -c my-snowflake

# Set project source connection
scai project defaults set -s my-oracle

# Set warehouse default
scai project defaults set --warehouse COMPUTE_WH
```

---

##### scai project defaults unset

Clear project-level defaults for the current project. Always clears from project.local.yml.

Copy code

```
scai project defaults unset [[--connection]] [[--source-connection]] [[--warehouse]] [[--database]] [[--schema]] [[--role]]
```

**Behavior:**

- Only flags you pass clear the matching field; other fields are unchanged
- Always clears from project.local.yml (gitignored), never from the shared project.yml

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `--connection` | Clear project default Snowflake connection name. | No |
| `--source-connection` | Clear project default source connection name. | No |
| `--warehouse` | Clear project default warehouse. | No |
| `--database` | Clear project default database. | No |
| `--schema` | Clear project default schema. | No |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Clear project Snowflake connection
scai project defaults unset --connection

# Clear warehouse default
scai project defaults unset --warehouse
```

---

#### scai project doctor

Check project folders, code unit registry, and connection names without connecting to databases.

Copy code

```
scai project doctor [[OPTIONS]]
```

**Prerequisites:**

- Must be run from within a migration project directory

**Behavior:**

- Runs offline only (does not log in to Snowflake or the source database)
- Lists each expected folder and file (required vs optional) with OK, Warning, or Problem
- Checks the code unit registry can load when present
- Checks Snowflake and source connection names exist in local TOML (not a live connection test)

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `--json` | Write machine-readable JSON to stdout (no markup). | No |

Expand

Show lessSee more

**Output:** Table of findings or JSON with json\_schema\_version and findings[]

**Examples:**

Copy code

```
# Run health checks
scai project doctor

# JSON for automation
scai project doctor --json
```

---

### scai connection

Manage source database connections (SqlServer, Redshift, Teradata, Oracle, Postgresql, BigQuery, AzureSynapse)

#### scai connection add-redshift

Add a new Redshift source database connection.

Copy code

```
scai connection add-redshift [OPTIONS]
```

**Prerequisites:**

- Network access to the Redshift cluster/serverless endpoint
- For IAM auth: AWS credentials configured (AWS CLI or environment variables)
- For standard auth: Username and password

**Authentication methods:**

- IAM Serverless: AWS IAM with Redshift Serverless
- IAM Provisioned: AWS IAM with Provisioned Cluster
- Standard: Username/password authentication

**Operation modes:**

- Interactive: Prompts for all required information (recommended)
- Inline: Use command-line options for automation/CI

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-s, --source-connection <SOURCE_CONNECTION>` | Name for this source connection profile | No |
| `--auth <AUTH>` | Authentication method (iam-serverless, iam-provisioned-cluster, standard) | No |
| `--user <USER>` | Username | No |
| `--database <DATABASE>` | Database name | No |
| `--connection-timeout <SECONDS>` | Connection timeout in seconds | No |
| `--workgroup <NAME>` | Redshift Serverless workgroup name | No |
| `--cluster-id <ID>` | Redshift Provisioned Cluster ID | No |
| `--region <REGION>` | AWS region | No |
| `--access-key-id <KEY>` | AWS Access Key ID | No |
| `--secret-access-key <KEY>` | AWS Secret Access Key | No |
| `--host <HOST>` | Redshift host | No |
| `--port <PORT>` | Port number | No |
| `--password <PASSWORD>` | Password | No |

Expand

Show lessSee more

**Output:** Connection saved to ~/.snowflake/connections.toml (or project-local)

**Examples:**

Copy code

```
# Add connection interactively (recommended)
scai connection add-redshift

# IAM Serverless (inline)
scai connection add-redshift --source-connection my-redshift --auth iam-serverless --workgroup my-workgroup --database mydb --region us-east-1
```

---

#### scai connection add-sql-server

Add a new SQL Server source database connection.

Copy code

```
scai connection add-sql-server [OPTIONS]
```

**Prerequisites:**

- Network access to the SQL Server instance
- For Windows auth: Valid domain credentials
- For standard auth: SQL Server username and password

**Authentication methods:**

- Windows: Windows Authentication (Integrated Security)
- Standard: SQL Server Authentication (username/password)

**Operation modes:**

- Interactive: Prompts for all required information (recommended)
- Inline: Use command-line options for automation/CI

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-s, --source-connection <SOURCE_CONNECTION>` | Name for this source connection profile | No |
| `--auth <AUTH>` | Authentication method (windows, standard) | No |
| `--user <USER>` | Username | No |
| `--database <DATABASE>` | Database name | No |
| `--connection-timeout <SECONDS>` | Connection timeout in seconds | No |
| `--server-url <URL>` | SQL Server URL | No |
| `--port <PORT>` | Port number | No |
| `--password <PASSWORD>` | Password | No |
| `--trust-server-certificate` | Trust server certificate | No |
| `--encrypt` | Encrypt connection | No |

Expand

Show lessSee more

**Output:** Connection saved to ~/.snowflake/connections.toml (or project-local)

**Examples:**

Copy code

```
# Add connection interactively (recommended)
scai connection add-sql-server

# Windows Authentication
scai connection add-sql-server --source-connection my-sqlserver --auth windows --server-url localhost --database mydb

# Standard Authentication
scai connection add-sql-server --source-connection my-sqlserver --auth standard --server-url localhost --database mydb --username sa
```

---

#### scai connection add-teradata

Add a new Teradata source database connection.

Copy code

```
scai connection add-teradata [OPTIONS]
```

**Prerequisites:**

- Network access to the Teradata instance
- For standard auth: Teradata username and password
- For LDAP auth: LDAP-backed username and password

**Authentication methods:**

- Standard: Username/password authentication
- LDAP: LDAP-backed authentication

**Operation modes:**

- Interactive: Prompts for all required information (recommended)
- Inline: Use command-line options for automation/CI

**Output:** Connection saved to ~/.snowflake/connections.toml (or project-local)

| Option | Description | Required |
| --- | --- | --- |
| `-s, --source-connection <SOURCE_CONNECTION>` | Name for this source connection profile | No |
| `--auth <AUTH>` | Authentication method (standard, ldap) | No |
| `--user <USER>` | Username | No |
| `--host <HOST>` | Teradata host | No |
| `--database <DATABASE>` | Database name | No |
| `--port <PORT>` | Port number | No |
| `--password <PASSWORD>` | Password | No |
| `--connection-timeout <SECONDS>` | Connection timeout in seconds | No |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Add connection interactively (recommended)
scai connection add-teradata

# Standard Authentication
scai connection add-teradata --source-connection my-teradata --auth standard --host myhost --database mydb --user dbc

# LDAP Authentication
scai connection add-teradata --source-connection my-teradata --auth ldap --host myhost --database mydb --user ldapuser
```

---

#### scai connection add-oracle

Add a new Oracle source database connection.

Copy code

```
scai connection add-oracle [OPTIONS]
```

**Prerequisites:**

- Network access to the Oracle instance
- Oracle username and password

**Authentication methods:**

- Standard: Username/password authentication

**Operation modes:**

- Interactive: Prompts for all required information (recommended)
- Inline: Use command-line options for automation/CI

**Output:** Connection saved to ~/.snowflake/connections.toml (or project-local)

| Option | Description | Required |
| --- | --- | --- |
| `-s, --source-connection <SOURCE_CONNECTION>` | Name for this source connection profile | No |
| `--auth <AUTH>` | Authentication method (standard) | No |
| `--user <USER>` | Username | No |
| `--host <HOST>` | Oracle host | No |
| `--service-name <SERVICE_NAME>` | Oracle service name | No |
| `--port <PORT>` | Port number (default: 1521) | No |
| `--password <PASSWORD>` | Password | No |
| `--connection-timeout <SECONDS>` | Connection timeout in seconds | No |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Add connection interactively (recommended)
scai connection add-oracle

# Standard Authentication
scai connection add-oracle --source-connection my-oracle --auth standard --host myhost --service-name ORCL --user scott
```

---

#### scai connection add-postgresql

Add a new PostgreSQL source database connection.

Copy code

```
scai connection add-postgresql [OPTIONS]
```

**Prerequisites:**

- Network access to the PostgreSQL host (TCP, default port 5432)
- A PostgreSQL role with CONNECT + USAGE on the target database and SELECT on pg\_catalog
- Username and password for standard authentication

**Authentication methods:**

- Standard: Username/password authentication (MVP: only method supported)

**SSL modes:**

- Disable: No SSL (local / loopback only)
- Prefer: SSL if available, plaintext otherwise
- Require: SSL required, server certificate not verified (default)
- VerifyCA: SSL required, CA validated against trust store
- VerifyFull: SSL required, CA + hostname validated

**Operation modes:**

- Interactive: Prompts for all required information (recommended)
- Inline: Use command-line options for automation/CI

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-s, --source-connection <SOURCE_CONNECTION>` | Name for this source connection profile | No |
| `--auth <AUTH>` | Authentication method (standard) | No |
| `--user <USER>` | Username | No |
| `--host <HOST>` | PostgreSQL host | No |
| `--database <DATABASE>` | Database name | No |
| `--port <PORT>` | Port number (default: 5432) | No |
| `--password <PASSWORD>` | Password | No |
| `--ssl-mode <SSL_MODE>` | SSL mode (default: Require). Values: Disable, Prefer, Require, VerifyCA, VerifyFull | No |
| `--connection-timeout <SECONDS>` | Connection timeout in seconds (default: 30) | No |

Expand

Show lessSee more

**Output:** Connection saved to ~/.snowflake/connections.toml (or project-local)

**Examples:**

Copy code

```
# Add connection interactively (recommended)
scai connection add-postgresql

# Standard authentication (inline)
scai connection add-postgresql --source-connection my-pg --auth standard --host db.example.com --database analytics --user postgres --password ****

# Local Docker (Disable SSL, custom port)
scai connection add-postgresql --source-connection local-pg --auth standard --host localhost --port 5432 --database scai_pg --user scai --password scai --ssl-mode Disable
```

---

#### scai connection add-azuresynapse

Add a new Azure Synapse Analytics source database connection.

Copy code

```
scai connection add-azuresynapse [OPTIONS]
```

**Prerequisites:**

- Network access to the Azure Synapse workspace endpoint
- Appropriate credentials (SQL auth, Service Principal, or Azure AD Interactive)

**Authentication methods:**

- Standard: SQL Authentication (username/password)
- Service Principal: Azure AD App Registration (client ID/secret)
- Interactive: Azure AD Interactive (browser-based login)

**Pool types:**

- Dedicated: Dedicated SQL pools (formerly SQL DW)
- Serverless: Serverless SQL pools (on-demand)

**Operation modes:**

- Interactive: Prompts for all required information (recommended)
- Inline: Use command-line options for automation/CI

**Output:** Connection saved to ~/.snowflake/connections.toml (or project-local)

| Option | Description | Required |
| --- | --- | --- |
| `-s, --source-connection <SOURCE_CONNECTION>` | Name for this source connection profile | No |
| `--auth <AUTH>` | Authentication method (standard, service-principal, interactive) | No |
| `--server-url <SERVER_URL>` | Azure Synapse server URL | No |
| `--port <PORT>` | Port number | No |
| `--database <DATABASE>` | Database name | No |
| `--pool-type <POOL_TYPE>` | Pool type (dedicated, serverless) | No |
| `--user <USER>` | Username or Client ID | No |
| `--password <PASSWORD>` | Password or Client Secret | No |
| `--trust-server-certificate` | Trust server certificate | No |
| `--encrypt` | Encrypt connection | No |
| `--connection-timeout <SECONDS>` | Connection timeout in seconds | No |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Add connection interactively (recommended)
scai connection add-azuresynapse

# Standard Authentication
scai connection add-azuresynapse --source-connection my-synapse --auth standard --server-url myworkspace.sql.azuresynapse.net --database mydb --pool-type dedicated --user admin

# Service Principal
scai connection add-azuresynapse --source-connection my-synapse --auth service-principal --server-url myworkspace.sql.azuresynapse.net --database mydb --pool-type serverless --user my-client-id
```

---

#### scai connection add-bigquery

Add a new BigQuery source database connection.

Copy code

```
scai connection add-bigquery [OPTIONS]
```

**Prerequisites:**

- Network access to the Google Cloud BigQuery API
- GCP project with BigQuery enabled
- Service account JSON key file or Application Default Credentials

**Authentication methods:**

- service-account: Service account JSON key file
- adc: Application Default Credentials (gcloud auth application-default login)

**Operation modes:**

- Interactive: Prompts for all required information (recommended)
- Inline: Use command-line options for automation/CI

**Output:** Connection saved to ~/.snowflake/snowct/bigquery.toml

| Option | Description | Required |
| --- | --- | --- |
| `-s, --source-connection <SOURCE_CONNECTION>` | Name for this source connection profile | No |
| `--auth <AUTH>` | Authentication method (service-account, adc) | No |
| `--project <PROJECT>` | GCP project ID | No |
| `--dataset <DATASET>` | Default BigQuery dataset | No |
| `--location <LOCATION>` | BigQuery location (e.g. US, EU, us-central1) | No |
| `--credentials-file <CREDENTIALS_FILE>` | Path to the service account JSON key file | No |
| `--connection-timeout <SECONDS>` | Connection timeout in seconds | No |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Add connection interactively (recommended)
scai connection add-bigquery

# Service account authentication
scai connection add-bigquery --source-connection my-bq --auth service-account --project my-gcp-project --dataset analytics --credentials-file ~/.gcp/bq-sa.json

# Application Default Credentials
scai connection add-bigquery --source-connection dev-bq --auth adc --project my-gcp-project-dev
```

---

#### scai connection set-default

Set the default source connection for a database type.

Copy code

```
scai connection set-default -l <LANGUAGE> -s <SOURCE_CONNECTION>
```

**Prerequisites:**

- Connection already added with ‘scai connection add-redshift’, ‘scai connection add-sql-server’, ‘scai connection add-teradata’, ‘scai connection add-oracle’, or ‘scai connection add-postgresql’

**Behavior:**

- Marks a configured connection as the default for extraction and validation
- Default source connection is used when no -s/–source-connection option is specified on commands that need a source database

**Supported database types:**

- SqlServer
- Redshift
- Teradata
- Oracle
- Postgresql
- BigQuery
- AzureSynapse

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-l, --source-language <LANGUAGE>` | Database type of the connection | Yes |
| `-s, --source-connection <SOURCE_CONNECTION>` | Name of the source connection profile to set as default | Yes |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Set default Redshift connection
scai connection set-default -l redshift -s prod

# Set default SQL Server connection
scai connection set-default -l sqlserver -s dev
```

---

#### scai connection list

List connections for a given source database.

Copy code

```
scai connection list [-l <LANGUAGE>]
```

**Behavior:**

- Without –source-language: shows Snowflake connections (from Snowflake CLI config) and configured source connections per supported database type.
- With global –json and no –source-language: prints only the JSON envelope; result uses mode summary with hasAnyConnections, snowflake (default name, connection rows, distinct config paths), and sources (per dbType: configPath, defaultConnectionName, connection name rows).
- With –source-language and –json: result uses mode detailed with connections (masked credentials JSON per profile), config path, and default name.

**Supported languages:**

- SqlServer
- Redshift
- Teradata
- Oracle
- Postgresql
- BigQuery
- AzureSynapse

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-l, --source-language <LANGUAGE>` | Source language of the connection. If omitted, shows a summary of all connections. | No |

Expand

Show lessSee more

**Output:** Without –json: tables (summary) or detailed rows. With –json: see behavior for envelope result shapes.

- Name
- Default
- Host
- Database

**Examples:**

Copy code

```
# List all connections summary
scai connection list

# List Redshift connections
scai connection list -l redshift

# List SQL Server connections
scai connection list -l sqlserver

# JSON summary of all connections
scai connection list --json

# JSON detailed list for one source language
scai connection list -l sqlserver --json
```

---

#### scai connection test

Test a source database connection.

Copy code

```
scai connection test -l <LANGUAGE> [-s <SOURCE_CONNECTION>]
```

**Prerequisites:**

- Connection already configured
- Network access to the database

**Behavior:**

- Attempts to connect to the database
- Verifies credentials and network connectivity
- Reports connection success or failure details
- Exits with a non-zero code when the connection test fails so scripts and CI/CD can detect failures
- With global –json on success: prints only the JSON envelope; result includes connectionName, dbType, credentialsMaskedJson (JSON document as a string, secrets redacted), and success true. On failure, errors appear on the envelope and the result table is not used.
- With global –json, the ‘using default connection’ line is omitted to keep stdout as a single JSON document.

**Supported languages:**

- SqlServer
- Redshift
- Teradata
- Oracle
- Postgresql
- BigQuery
- AzureSynapse

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-l, --source-language <LANGUAGE>` | Source language of the connection. Supported languages: SqlServer, Redshift, Teradata, Oracle, Postgresql, BigQuery, and AzureSynapse. | Yes |
| `-s, --source-connection <SOURCE_CONNECTION>` | Name of the source connection profile to test | No |

Expand

Show lessSee more

**Output:**

- Success: ‘Connection successful’ with connection details
- Failure: Error message with troubleshooting hints

**Examples:**

Copy code

```
# Test SQL Server connection
scai connection test -l sqlserver -s my-sqlserver

# Test Redshift connection
scai connection test -l redshift -s my-redshift

# JSON result on successful test
scai connection test -l sqlserver -s my-sqlserver --json
```

---

#### scai connection remove

Remove a source database connection profile.

Copy code

```
scai connection remove -l <LANGUAGE> -s <SOURCE_CONNECTION>
```

**Prerequisites:**

- Connection already added with ‘scai connection add-redshift’, ‘scai connection add-sql-server’, ‘scai connection add-teradata’, ‘scai connection add-oracle’, or ‘scai connection add-postgresql’

**Behavior:**

- Permanently removes the specified connection profile from the TOML configuration file
- Fails with an error if the connection name does not exist for the given database type
- Does not affect other connection profiles or the default connection setting of other profiles

**Supported database types:**

- SqlServer
- Redshift
- Teradata
- Oracle
- Postgresql
- BigQuery
- AzureSynapse

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-l, --source-language <LANGUAGE>` | Database type of the connection to remove | Yes |
| `-s, --source-connection <SOURCE_CONNECTION>` | Name of the source connection profile to remove | Yes |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Remove a Redshift connection
scai connection remove -l redshift -s prod

# Remove a SQL Server connection
scai connection remove -l sqlserver -s dev

# Remove an Oracle connection
scai connection remove -l oracle -s staging
```

---

### scai code

Code operations: extract, convert, add, deploy, find, where

#### scai code extract

Extract code from the source database.

Copy code

```
scai code extract [OPTIONS]
```

**Prerequisites:**

- A migration project initialized with ‘scai init’
- Source database connection configured (use ‘scai connection add-redshift’, ‘scai connection add-sql-server’, ‘scai connection add-teradata’, ‘scai connection add-oracle’, or ‘scai connection add-postgresql’)
- Network access to the source database

**Behavior:**

- Connects to the configured source database connection
- Extracts DDL and writes to source/ folder

**Supported languages:**

- SqlServer
- Redshift
- Teradata
- Oracle
- Postgresql
- BigQuery
- AzureSynapse

**Interactive mode:**

Requirement: Requires an interactive terminal. In non-interactive or CI environments use –schema, –object-type, and –name instead.

- Pre-fetch: prompt for schema (or leave empty for all) and multi-select object types to scope the catalog query.
- Post-fetch: multi-select schemas to include, optional name filter (wildcard \* supported), summary table, then confirm extraction.

> Options –schema, -t/–object-type, and -n/–name pre-fill the interactive prompts when used with -i.

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `-s, --source-connection <NAME>` | Name of the source connection to extract code from | No |  |
| `--schema <SCHEMA>` | Schema name to extract code from | No |  |
| `-t, --object-type <TYPES>` | Object types to extract (comma-separated). E.g., TABLE,VIEW,PROCEDURE | No |  |
| `-n, --name <PATTERN>` | Filter objects by name. Supports substring match or wildcard patterns with \* (e.g., ‘emp’ or ‘Get\*Data’) | No |  |
| `-i, --interactive` | Interactive mode: browse and select schemas, object types, and filter by name | No | False |
| `--source-id <SOURCE_ID>` | Identifier for the source system where the code is extracted from. Recorded in the code unit registry under codeStatus.registration.sourceId. Defaults to the server hostname resolved from the source connection if not provided. | No |  |

Expand

Show lessSee more

**Output:** Extracted SQL files organized by database

```
source/
  └── <database>/        One folder per source database
      └── <schema>/      One folder per database schema
          └── <type>/    One folder per object type
              └── *.sql  DDL files for each object
```

**Examples:**

Copy code

```
# Interactive extraction (browse and select schemas, object types, filter by name)
scai code extract -i

# Interactive with pre-filled schema
scai code extract -i --schema public

# Extract tables from a schema
scai code extract --schema public --object-type TABLE

# Extract tables and views
scai code extract --object-type TABLE,VIEW

# Extract from all schemas
scai code extract

# Extract code with a custom source identifier
scai code extract --source-id prod-redshift-cluster
```

---

#### scai code convert

Transform source database code to Snowflake SQL.

Copy code

```
scai code convert [OPTIONS]
```

> Additional dialect-specific options are dynamically loaded based on the project’s source language. Run ‘scai code convert –help’ within a project to see all available options for that dialect.

**Prerequisites:**

- A migration project initialized with ‘scai init’
- Source code in the ‘source/’ folder (from ‘scai code extract’, ‘scai code add’, or manual copy)

**Behavior:**

- Reads SQL files from source/ folder
- Transforms code to Snowflake-compatible SQL
- Writes converted code and reports to snowflake/ folder

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-h, --help` | Display all the conversion settings available for the specified source language | No |
| `-e, --etl-replatform-sources-path <PATH>` | Path to ETL replatform source files for cross-project code analysis. Must be provided for each conversion run. | No |
| `--simplify-ssis-dataflows` | If set, simple SSIS data flows will be converted to inline Snowflake SQL instead of dbt projects. The DataFlow needs to have a transformation count of less than or equal to 10 and can only have the following transformation types: Sources, Targets, Derived Column, Row Count, and Conditional Split. | No |
| `--consolidate-dbt-model-chains` | If set, consolidates dbt model chains when converting Informatica to dbt to reduce the number of generated dbt model files. | No |
| `-p, --powerbi-repointing <PATH>` | Path to Power BI files for input repointing. Must be provided for each conversion run. | No |
| `-x, --show-ewis` | Show detailed EWI (Early Warning Issues) table instead of summary | No |
| `--context-path <PATH>` | Path to read migration context from. Defaults to .scai/conversion-context. Generated context is always written to .scai/conversion-context. | No |
| `--overwrite-working-directory` | Overwrite the output files in the snowflake/ directory and the Code Unit Registry Files. Off by default. | No |
| `--where <WHERE>` | SQL-like filter to select which code units to convert (e.g. “objectType = ‘procedure’”). Only matched units are transformed; dependencies are still parsed for symbol resolution. | No |

Expand

Show lessSee more

**Dialect-specific conversion settings:**

Each dialect has specific conversion options. Common options across dialects include:

- Supported dialects: BigQuery, Databricks, Db2, Greenplum, Hive, Netezza, Oracle, Postgresql, Redshift, Spark, SqlServer, Sybase, Teradata, Vertica
- Common options include: `-m, --comments`, `--encoding <ENCODING>`, `-s, --customschema <SCHEMA>`, `-d, --database <DATABASE>`, `--useexistingnamequalification`, `--renamingfile <PATH>`, `--arrange`, `-t, --pltargetlanguage <LANGUAGE>`, `-w, --warehouse <NAME>`, `--targetlag <VALUE>`, `--previewflags <FLAGS>`, `--createestimationreports`
- Teradata examples: `--splitperioddatatype`, `--generatestoredproceduretags`, `--disabletopologicallevelreorder`, `--disableCollateForCaseSpecification`, `--disable-use-database-generation`, `--sessionMode <Tera|Ansi>`, `--scripttargetlanguage <Python|SnowScript>`, `--displacedatabaseasschema`
- Oracle examples: `--disablesynonym`, `--disablepackagesasschemas`, `--disabledateastimestamp`, `--outerjoinstoonlyansisyntax`, `--dataTypeCustomizationFile <PATH>`
- SqlServer examples: `--disable-use-database-generation`, `--TargetLag <TargetLag|Downstream>`, `--targetlagnumber <NUMBER>`, `--targetlagtime <seconds|minutes|hours|days>`
- Sybase examples: `--disable-use-database-generation`
- Netezza examples: `--disable-use-database-generation`
- Databricks examples: `--transformexternaltablestoregular`, `--addpartitionedcolumnstotabledefinition`
- Spark examples: `--transformexternaltablestoregular`, `--addpartitionedcolumnstotabledefinition`

**Output:** Converted Snowflake SQL files and reports

```
snowflake/
  ├── Output/                     Converted Snowflake SQL files
  │   └── <schema>/               Organized by schema
  │       └── *.sql               Converted DDL files
  ├── Reports/
  │   ├── TopLevelCodeUnits.csv   List of all converted objects
  │   ├── Issues.csv              Conversion issues/warnings
  │   └── Summary.html            HTML conversion summary
  └── Logs/                       Conversion log files
```

**Examples:**

Copy code

```
# Convert using project defaults
scai code convert

# Convert with custom context path
scai code convert --context-path /path/to/context

# Show all conversion settings for the project's dialect
scai code convert --help

# Convert with custom schema
scai code convert --customschema MY_SCHEMA

# Convert with comment on missing dependencies
scai code convert --comments

# Convert with object renaming file
scai code convert --renamingfile /path/to/renaming.json

# Convert only procedures
scai code convert --where "objectType = 'procedure'"
```

---

#### scai code add

Add source code from an input file or directory to the project’s Source folder.

Copy code

```
scai code add -i <INPUT_PATH> [--code-already-split] [OPTIONS]
```

**Prerequisites:**

- A migration project initialized with ‘scai init’
- Input must be a valid SQL source file or a directory containing SQL source files

**Behavior:**

- Copies the specified file, or all files and directories from the input path, to artifacts/source\_raw/
- SqlServer, Redshift, and Teradata: runs arrange-only, produces artifacts/source\_raw\_Processed/, merges into source/
- Other languages: copies source directly into source/
- When –code-already-split is used (SqlServer, Redshift, and Teradata), skips the arrange/split phase, promotes raw source directly to source/, runs assessment only for code unit registry generation, and marks the project as project type: Full (new folder structure)
- Checks for conflicting files when destination folders are non-empty (unless –overwrite is set)
- Reports up to 10 conflicting file names if conflicts are detected

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `-i, --input-path <PATH>` | Path to a source code file or directory to add to the project | Yes |  |
| `--overwrite` | Overwrite existing files in the project’s Source folder if they conflict with files being added | No | False |
| `--code-already-split` | Skip the arrange/split phase when source code is already split (SqlServer, Redshift, and Teradata). Proceeds directly to code unit registry generation and marks the project as project type: Full (new folder structure). | No | False |
| `--source-id <SOURCE_ID>` | Identifier for the source system where the code originates (e.g., server hostname or instance name). Recorded in the code unit registry under codeStatus.registration.sourceId. Defaults to the local machine name if not provided. | No |  |

Expand

Show lessSee more

**Output:** Original input in artifacts/source\_raw/; source/ contains arranged output (SqlServer, Redshift, and Teradata) or copied source (other languages)

```
artifacts/source_raw/
source/
```

- SqlServer, Redshift, and Teradata: artifacts/source\_raw\_Processed/ is an internal arrange output folder used during processing, then removed after merge into source/
- Other languages: files are copied directly from artifacts/source\_raw/ to source/

**Examples:**

Copy code

```
# Add source code to project
scai code add -i /path/to/source/code

# Add pre-split source code (skip arrange phase)
scai code add -i /path/to/source/code --code-already-split

# Add code using full option name
scai code add --input-path ./my-sql-scripts

# Add a single file
scai code add -i /path/to/script.sql

# Add code overwriting existing files
scai code add -i /path/to/source/code --overwrite

# Add code with a source identifier for traceability
scai code add -i /path/to/source/code --source-id prod-sql-server-01
```

---

#### scai code accept

Accept the latest converted artifact versions into the snowflake output folder.

Copy code

```
scai code accept [OPTIONS]
```

**Prerequisites:**

- A migration project initialized with ‘scai init’
- Source code must be split and registry files must be generated (run ‘scai code add’)
- At least one code conversion run with ‘scai code convert’

**Behavior:**

- Scans the artifacts directory for timestamped conversion outputs
- For each code unit, selects the most recent version based on the timestamp folder name (yyyyMMdd.HHmmss)
- Copies the latest .sql files into the snowflake folder, preserving the directory structure
- Skips source\_raw and source\_raw\_Processed directories

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `--where <WHERE>` | Filter expression to select which objects to accept. Run ‘scai code where’ for syntax reference. | No |

Expand

Show lessSee more

**Output:** Updated snowflake folder with latest artifact versions

```
snowflake/<database>/<schema>/<type>/<name>.sql
```

**Examples:**

Copy code

```
# Accept all latest artifacts
scai code accept
```

---

#### scai code deploy

Deploy SQL code to a target database. Default target (-t snowflake) deploys converted DDL to Snowflake; -t source deploys captured Source DDL to a database of the project’s source dialect.

Copy code

```
scai code deploy [OPTIONS]
```

**Prerequisites:**

- Converted code in ‘snowflake/Output/’ (from ‘scai code convert’)
- Snowflake connection configured (set with ‘scai init -c’ or project settings)
- Appropriate Snowflake privileges (CREATE TABLE, CREATE VIEW, etc.)
- For -t source: a source-database connection (see ‘scai connection add’)

**Behavior:**

- Default target (-t snowflake) deploys converted code to Snowflake
- -t source deploys captured Source DDL to a database of the project’s source dialect
- –replace (-t source only) drops each object before recreating it
- Uses Snowflake connection from connections.toml, config.toml, or project default
- –warehouse, –schema, –role temporarily set missing connection fields (in-memory only, TOML is not modified)
- If the connection already has a value for an overridden field, an error is returned

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `-c, --connection <NAME>` | The name of the Snowflake connection to use. Uses default if not specified. | No |  |
| `-s, --source-connection <NAME>` | Name of the source database connection to use with -t source. Uses the project default if not specified. | No |  |
| `-d, --database <NAME>` | Target database name for deployment. Also sets the connection database if not already configured. Uses converted database name if not specified. | No |  |
| `-t, --target <TARGET>` | Deployment target: ‘snowflake’ (default) deploys the converted DDL to Snowflake; ‘source’ deploys the captured Source DDL to a database of the project’s source dialect. | No | snowflake |
| `--replace` | With -t source, drops each object in the target before recreating it. Useful for re-running an iterative fix loop against the same sandbox database. | No | False |
| `--warehouse <WAREHOUSE>` | Warehouse to use for the Snowflake connection. Only applied if the connection does not already have a warehouse configured. | No |  |
| `--schema <SCHEMA>` | Schema to use for the Snowflake connection. Only applied if the connection does not already have a schema configured. | No |  |
| `--role <ROLE>` | Role to use for the Snowflake connection. Only applied if the connection does not already have a role configured. | No |  |
| `--where <WHERE>` | SQL-like WHERE clause to filter objects to deploy. Run ‘scai code where’ for syntax reference. | No |  |
| `-a, --all` | Deploy all successfully converted objects without selection prompt. | No | False |
| `-r, --retry <N>` | Number of retry attempts for failed object deployments. | No | 1 |
| `--continue-on-error` | Continue deploying remaining objects even if some fail. | No | True |
| `--include-dependencies` | When used with –where, also deploy the dependencies of the filtered code units. Has no effect without –where, since all code units are already included. | No | False |
| `--driver-path <DRIVER_PATH>` | Path to the source database driver (.dll or .nupkg). Required for Oracle and Teradata if not previously cached. | No |  |

Expand

Show lessSee more

**Output:** Console output shows deployment progress and results for each object. Objects are created in the target Snowflake database/schema.

**Examples:**

Copy code

```
# Deploy using default connection
scai code deploy

# Deploy all objects
scai code deploy --all

# Deploy with specific connection
scai code deploy --connection my-snowflake

# Deploy with temporary warehouse override
scai code deploy --warehouse MY_WH

# Deploy filtered objects and their dependencies
scai code deploy --where "source.objectType = 'procedure'" --include-dependencies

# Deploy original-dialect DDL to the source engine
scai code deploy -t source

# Re-run a source deploy, dropping existing objects first
scai code deploy -t source --replace
```

---

#### scai code sync

Import a legacy migration project (.snowct) into the new SnowConvert AI Structure (Code Unit Registry).

Copy code

```
scai code sync <PROJECT_PATH> -l <LANGUAGE> -i <SOURCE_FOLDER> --snowflake <CONVERTED_FOLDER> [-c <CONNECTION>]
```

**Prerequisites:**

- Existing source code directory with SQL files
- Existing converted Snowflake code directory
- Target project directory must not exist or must be empty
- Source language must be SqlServer or Redshift

**Behavior:**

- Creates a new SnowConvert project at the specified path
- Copies source code to the project’s source/ folder
- Validates the code unit registry for duplicate source file paths
- Runs a code conversion to generate full registry information
- Copies converted code to the project’s snowflake/ folder
- If any step fails, the project directory is deleted (rolled back)

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `<PROJECT_PATH>` | Directory where the new project will be created | Yes |
| `-l, --language <SOURCE_LANGUAGE>` | Source dialect (sqlserver or redshift) | Yes |
| `-i, --input <SOURCE_FOLDER>` | Path to existing source code directory | Yes |
| `--snowflake <CONVERTED_FOLDER>` | Path to existing converted Snowflake code directory | Yes |
| `-c, --connection <CONNECTION>` | Snowflake connection name (uses default if not specified) | No |

Expand

Show lessSee more

**Output:** Project directory with source/, snowflake/, .scai/, artifacts/, reports/, and logs/ folders.

**Examples:**

Copy code

```
# Sync a legacy Oracle project
scai code sync my-project -l oracle -i /path/to/source --snowflake /path/to/converted

# Sync with a specific Snowflake connection
scai code sync my-project -l sqlserver -i ./source-code --snowflake ./converted-code -c my-snowflake

# Sync a Teradata project
scai code sync /output/project -l teradata -i /legacy/source --snowflake /legacy/snowflake
```

---

#### scai code where

Show WHERE clause query reference for code unit filtering.

Copy code

```
scai code where
```

**Behavior:**

- Displays all queryable fields, supported operators, and usage examples for WHERE clause filtering
- Does not require a project directory
- Works offline without network access
- When online, Snowflake is optional: account and user are read from local project configuration first when available, with a live connection test as a fallback when metadata is incomplete
- The reference is loaded dynamically from the CodeUnitRegistry native library (field list is auto-generated from the code-unit JSON schema)

**Output:** Printed reference guide including syntax, operators, queryable fields with types and allowed values, and example WHERE expressions. The content is generated at runtime from the CodeUnitRegistry; run the command to see the current field list.

**Examples:**

Copy code

```
# Show WHERE clause reference
scai code where
```

---

#### scai code find

Find code units from project’s Code Unit Registry.

Copy code

```
scai code find [OPTIONS]
```

**Prerequisites:**

- A migration project initialized with ‘scai init’
- An initialized Code Unit Registry (generated after ‘scai code convert’)

**Behavior:**

- Reads code unit information from the Code Unit Registry
- Displays code units in a table with Id, Fully Qualified Name, and Object Type
- Results are limited to 100 by default; use –no-limit to show all
- Can be filtered using a SQL-like WHERE clause

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `--where <WHERE>` | SQL-like WHERE clause to filter objects to find. Run ‘scai code where’ for syntax reference. | No |  |
| `--no-limit` | Disables the limit on the number of objects to display. By default, the number of objects is limited to 100. | No | False |

Expand

Show lessSee more

**Output:** Console output shows code unit information in a table format.

**Examples:**

Copy code

```
# Find all code units
scai code find

# Find code units with a specific name
scai code find --where "source.name = 'my_table'"

# Find all code units without limit
scai code find --no-limit
```

---

#### scai code resync

Re-scan modified converted files and update issue metadata in the Code Unit Registry.

Copy code

```
scai code resync
```

**Prerequisites:**

- A migration project initialized with ‘scai init’
- Code converted with ‘scai code convert’

**Behavior:**

- Detects code units whose converted files have been modified
- Re-scans each modified file for SnowConvert issue codes (EWI, FDM, OOS, PRF)
- Updates the issue metadata in the registry

**Output:** Console output shows the number of modified files resynced

**Examples:**

Copy code

```
# Resync modified converted files
scai code resync
```

---

### scai data

Data operations: migrate, validate, worker, orchestrator, doctor

#### scai data migrate

##### scai data migrate start

Migrate data from the source system into a Snowflake account.

Copy code

```
scai data migrate start [--config <DATA_MIGRATION_CONFIG_PATH>] [-c <CONNECTION>] [OPTIONS]
```

**Prerequisites:**

- Data migration configuration file (YAML); if –config is omitted, an ephemeral default config is auto-generated under the OS temp directory with a unique per-run affinity
- Snowflake connection with appropriate privileges

**Behavior:**

- Reads the migration configuration and runs the data migration workflow
- When –config is omitted, the generated workflow config is written to the OS temp directory and deleted when the run finishes

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `--config` | Path to the YAML configuration file. If omitted, an ephemeral default config is auto-generated under the OS temp directory with a unique per-run affinity and deleted when the run finishes. | No | .scai/config/data-migration-config.yaml |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |  |
| `--warehouse <WAREHOUSE>` | Warehouse to use. Overrides the value specified for the Snowflake connection. | No |  |
| `--role <ROLE>` | Role to use. Overrides the value specified for the Snowflake connection. | No |  |

Expand

Show lessSee more

**Output:** Returns a WORKFLOW\_ID for tracking progress

**Examples:**

Copy code

```
# Start migration with default config
scai data migrate start --connection my-snowflake

# Start migration with custom config
scai data migrate start --config my-data-migration-config.yaml --connection my-snowflake
```

---

##### scai data migrate create-workflow

Create a cloud data migration workflow in Snowflake.

Copy code

```
scai data migrate create-workflow [--config <DATA_MIGRATION_CONFIG_PATH>] [-c <CONNECTION>] [OPTIONS]
```

**Prerequisites:**

- Data migration configuration file (YAML); if –config is omitted, defaults to .scai/config/data-migration-config.yaml
- Orchestrator setup completed (run ‘scai data orchestrator setup’ first)
- Snowflake connection with appropriate privileges

**Behavior:**

- Validates the configuration and creates a Data Migration workflow in Snowflake
- By default, returns immediately after creating the workflow
- Use -w|–watch to wait for the workflow to complete

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `--config` | Path to the YAML configuration file. If omitted, defaults to .scai/config/data-migration-config.yaml. | No | .scai/config/data-migration-config.yaml |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |  |
| `--warehouse <WAREHOUSE>` | Warehouse to use. Overrides the value specified for the Snowflake connection. | No |  |
| `--role <ROLE>` | Role to use. Overrides the value specified for the Snowflake connection. | No |  |
| `-w, --watch` | Wait for the workflow to complete. | No | False |

Expand

Show lessSee more

**Output:** Returns a WORKFLOW\_ID for tracking progress

**Examples:**

Copy code

```
# Create a cloud workflow (default config)
scai data migrate create-workflow --connection my-snowflake

# Create a cloud workflow with custom config
scai data migrate create-workflow --config my-data-migration-config.yaml --connection my-snowflake

# Create workflow and wait for completion
scai data migrate create-workflow --connection my-snowflake --watch
```

---

##### scai data migrate status

Check the status of a Cloud Data Migration workflow.

Copy code

```
scai data migrate status [WORKFLOW_ID] [OPTIONS]
```

**Prerequisites:**

- A workflow started with ‘scai data migrate start’ or ‘scai data migrate create-workflow’
- Snowflake connection with access to the workflow

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `-c, --connection <CONNECTION>` | The Snowflake connection name to use. | No |  |
| `-w, --watch` | Display progress and poll for updates until workflow completes. | No | False |

Expand

Show lessSee more

**Output:** Progress bars for table preprocessing and partition processing. Error details if workflow failed.

**Examples:**

Copy code

```
# Check workflow status
scai data migrate status DATA_MIGRATION_WORKFLOW_xx_yy_zz

# Watch workflow progress
scai data migrate status DATA_MIGRATION_WORKFLOW_xx_yy_zz --watch
```

---

##### scai data migrate list

List all Cloud Data Migration workflows.

Copy code

```
scai data migrate list [OPTIONS]
```

**Prerequisites:**

- Snowflake connection with access to the SNOWCONVERT\_AI database

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `-c, --connection <CONNECTION>` | The Snowflake connection name to use. | No |  |
| `-s, --status <STATUS>` | Filter workflows by status (pending, initializing, running, finished, failed). | No |  |
| `--limit <LIMIT>` | Maximum number of workflows to display. | No | 20 |

Expand

Show lessSee more

**Output:** A table with workflow name, status, creation time, end time, and error message.

**Examples:**

Copy code

```
# List all migration workflows
scai data migrate list

# Filter by status
scai data migrate list --status running

# Use a specific connection
scai data migrate list --connection my-snowflake
```

---

##### scai data migrate generate-config

Generate a YAML configuration file for data migration.

Copy code

```
scai data migrate generate-config [--where <WHERE>] [-o <OUTPUT_PATH>] [--affinity <AFFINITY>]
```

**Prerequisites:**

- A migration project initialized with ‘scai init’
- Code added and converted (‘scai code add’ and ‘scai code convert’)

**Behavior:**

- Resolves source and target table names from the Code Unit Registry
- Generates a YAML config for ‘scai data migrate start’ (–config optional; defaults to .scai/config/data-migration-config.yaml)
- Sets synchronization strategy to ‘none’ and extraction strategy to ‘regular’

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `--where <WHERE>` | SQL-like WHERE clause to filter tables from the Code Unit Registry. Run ‘scai code where’ for syntax reference. | No |  |
| `-o, --output` | Output file path for the generated YAML configuration. Defaults to .scai/config/data-migration-config.yaml. | No | .scai/config/data-migration-config.yaml |
| `--affinity` | Affinity tag written to the workflow YAML. Matching Workers pick up the workflow’s tasks. See [Affinity](/migrations/aim-for-datawarehouses/manual-migration/data-migration-configuration-reference#affinity). | No |  |

Expand

Show lessSee more

**Output:** A YAML file (default: .scai/config/data-migration-config.yaml) with source/target table mappings.

**Examples:**

Copy code

```
# Generate config for all tables
scai data migrate generate-config

# Filter tables by schema
scai data migrate generate-config --where "source.schema = 'public'"

# Custom output path
scai data migrate generate-config -o my-config.yaml

# Set workflow affinity
scai data migrate generate-config --affinity my-team
```

---

##### scai data migrate pause

Pause a running data migration workflow.

Copy code

```
scai data migrate pause <WORKFLOW_NAME> [-c <CONNECTION>]
```

**Prerequisites:**

- An active workflow in ‘executing’ or ‘pending’ state
- Snowflake connection with appropriate privileges

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `<WORKFLOW_NAME>` | The name of the workflow to pause. | Yes |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |

Expand

Show lessSee more

**Output:** Confirmation that the workflow was paused.

**Examples:**

Copy code

```
# Pause a workflow
scai data migrate pause MY_WORKFLOW
```

---

##### scai data migrate resume

Resume a paused data migration workflow.

Copy code

```
scai data migrate resume <WORKFLOW_NAME> [-c <CONNECTION>]
```

**Prerequisites:**

- A workflow in ‘paused’ state
- Snowflake connection with appropriate privileges

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `<WORKFLOW_NAME>` | The name of the workflow to resume. | Yes |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |

Expand

Show lessSee more

**Output:** Confirmation that the workflow was resumed.

**Examples:**

Copy code

```
# Resume a paused workflow
scai data migrate resume MY_WORKFLOW
```

---

##### scai data migrate cancel

Cancel a data migration workflow.

Copy code

```
scai data migrate cancel <WORKFLOW_NAME> [-y] [-c <CONNECTION>]
```

**Prerequisites:**

- A workflow that is not yet completed or already cancelled
- Snowflake connection with appropriate privileges

**Behavior:**

- Prompts for confirmation unless -y is passed

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `<WORKFLOW_NAME>` | The name of the workflow to cancel. | Yes |
| `-y, --yes` | Skip the confirmation prompt. | No |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |

Expand

Show lessSee more

**Output:** Confirmation that the workflow was cancelled.

**Examples:**

Copy code

```
# Cancel a workflow (with prompt)
scai data migrate cancel MY_WORKFLOW

# Cancel a workflow (skip prompt)
scai data migrate cancel MY_WORKFLOW -y
```

---

#### scai data validate

##### scai data validate start

Validate data between source and Snowflake.

Copy code

```
scai data validate start [--config <DATA_VALIDATION_CONFIG_PATH>] [-c <CONNECTION>] [OPTIONS]
```

**Prerequisites:**

- Data validation configuration file (YAML); if –config is omitted, an ephemeral default config is auto-generated under the OS temp directory with a unique per-run affinity
- Snowflake connection with appropriate privileges

**Behavior:**

- Reads the validation configuration and runs the data validation workflow
- When –config is omitted, the generated workflow config is written to the OS temp directory and deleted when the run finishes

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `--config` | Path to the YAML configuration file. If omitted, an ephemeral default config is auto-generated under the OS temp directory with a unique per-run affinity and deleted when the run finishes. | No | .scai/config/data-validation-config.yaml |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |  |
| `--warehouse <WAREHOUSE>` | Warehouse to use. Overrides the value specified for the Snowflake connection. | No |  |
| `--role <ROLE>` | Role to use. Overrides the value specified for the Snowflake connection. | No |  |

Expand

Show lessSee more

**Output:** Returns a WORKFLOW\_ID for tracking progress

**Examples:**

Copy code

```
# Start validation with default config
scai data validate start --connection my-snowflake

# Start validation with custom config
scai data validate start --config my-data-validation-config.yaml --connection my-snowflake
```

---

##### scai data validate create-workflow

Create a cloud data validation workflow in Snowflake.

Copy code

```
scai data validate create-workflow [--config <DATA_VALIDATION_CONFIG_PATH>] [-c <CONNECTION>] [OPTIONS]
```

**Prerequisites:**

- Data validation configuration file (YAML); if –config is omitted, defaults to .scai/config/data-validation-config.yaml
- Snowflake connection with appropriate privileges

**Behavior:**

- Validates the configuration and creates a Data Validation workflow in Snowflake
- By default, returns immediately after creating the workflow
- Use -w|–watch to wait for the workflow to complete

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `--config` | Path to the YAML configuration file. If omitted, defaults to .scai/config/data-validation-config.yaml. | No | .scai/config/data-validation-config.yaml |
| `--custom-image` | Custom container image path to use instead of auto-resolving the latest. Format: /db/schema/repo/image\_name:tag | No |  |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |  |
| `--warehouse <WAREHOUSE>` | Warehouse to use. Overrides the value specified for the Snowflake connection. | No |  |
| `--role <ROLE>` | Role to use. Overrides the value specified for the Snowflake connection. | No |  |
| `-w, --watch` | Wait for the workflow to complete. | No | False |

Expand

Show lessSee more

**Output:** Returns a WORKFLOW\_ID for tracking progress

**Examples:**

Copy code

```
# Create a cloud validation workflow (default config)
scai data validate create-workflow --connection my-snowflake

# Create a cloud validation workflow with custom config
scai data validate create-workflow --config my-data-validation-config.yaml --connection my-snowflake

# Create workflow and wait for completion
scai data validate create-workflow --watch --connection my-snowflake
```

---

##### scai data validate status

Check the status of a Cloud Data Validation workflow.

Copy code

```
scai data validate status [WORKFLOW_NAME] [OPTIONS]
```

**Prerequisites:**

- A workflow started with ‘scai data validate start’ or ‘scai data validate create-workflow’
- Snowflake connection with access to the workflow

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `-c, --connection <CONNECTION>` | The Snowflake connection name to use. | No |  |
| `-w, --watch` | Display progress and poll for updates until workflow completes. | No | False |

Expand

Show lessSee more

**Output:** Per-table validation status showing schema, metrics, and row validation results.

**Examples:**

Copy code

```
# Check workflow status
scai data validate status DATA_VALIDATION_WORKFLOW_xx_yy_zz

# Watch workflow progress
scai data validate status DATA_VALIDATION_WORKFLOW_xx_yy_zz --watch
```

---

##### scai data validate list

List all Cloud Data Validation workflows.

Copy code

```
scai data validate list [OPTIONS]
```

**Prerequisites:**

- Snowflake connection with access to the SNOWCONVERT\_AI database

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `-c, --connection <CONNECTION>` | The Snowflake connection name to use. | No |  |
| `-s, --status <STATUS>` | Filter workflows by status (pending, initializing, running, finished, failed). | No |  |
| `--limit <LIMIT>` | Maximum number of workflows to display. | No | 20 |

Expand

Show lessSee more

**Output:** A table with workflow name, status, creation time, end time, and error message.

**Examples:**

Copy code

```
# List all validation workflows
scai data validate list

# Filter by status
scai data validate list --status failed

# Use a specific connection
scai data validate list --connection my-snowflake
```

---

##### scai data validate generate-config

Generate a YAML configuration file for data validation.

Copy code

```
scai data validate generate-config [--where <WHERE>] [-o <OUTPUT_PATH>] [--affinity <AFFINITY>]
```

**Prerequisites:**

- A migration project initialized with ‘scai init’
- Code added and converted (‘scai code add’ and ‘scai code convert’)

**Behavior:**

- Resolves source and target table names from the Code Unit Registry
- Generates a YAML config for ‘scai data validate start’ (–config optional; defaults to .scai/config/data-validation-config.yaml)

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `--where <WHERE>` | SQL-like WHERE clause to filter tables from the Code Unit Registry. Run ‘scai code where’ for syntax reference. | No |  |
| `-o, --output` | Output file path for the generated YAML configuration. Defaults to .scai/config/data-validation-config.yaml. | No | .scai/config/data-validation-config.yaml |
| `--affinity` | Affinity tag written to the workflow YAML. Matching Workers pick up the workflow’s tasks. See [Affinity](/migrations/aim-for-datawarehouses/manual-migration/data-migration-configuration-reference#affinity). | No |  |

Expand

Show lessSee more

**Output:** A YAML file (default: .scai/config/data-validation-config.yaml) with source/target table mappings.

**Examples:**

Copy code

```
# Generate config for all tables
scai data validate generate-config

# Filter tables by schema
scai data validate generate-config --where "source.schema = 'public'"

# Custom output path
scai data validate generate-config -o my-config.yaml
```

---

##### scai data validate pause

Pause a running data validation workflow.

Copy code

```
scai data validate pause <WORKFLOW_NAME> [-c <CONNECTION>]
```

**Prerequisites:**

- An active workflow in ‘executing’ or ‘pending’ state
- Snowflake connection with appropriate privileges

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `<WORKFLOW_NAME>` | The name of the workflow to pause. | Yes |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |

Expand

Show lessSee more

**Output:** Confirmation that the workflow was paused.

**Examples:**

Copy code

```
# Pause a validation workflow
scai data validate pause MY_WORKFLOW
```

---

##### scai data validate resume

Resume a paused data validation workflow.

Copy code

```
scai data validate resume <WORKFLOW_NAME> [-c <CONNECTION>]
```

**Prerequisites:**

- A workflow in ‘paused’ state
- Snowflake connection with appropriate privileges

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `<WORKFLOW_NAME>` | The name of the workflow to resume. | Yes |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |

Expand

Show lessSee more

**Output:** Confirmation that the workflow was resumed.

**Examples:**

Copy code

```
# Resume a paused validation workflow
scai data validate resume MY_WORKFLOW
```

---

##### scai data validate cancel

Cancel a data validation workflow.

Copy code

```
scai data validate cancel <WORKFLOW_NAME> [-y] [-c <CONNECTION>]
```

**Prerequisites:**

- A workflow that is not yet completed or already cancelled
- Snowflake connection with appropriate privileges

**Behavior:**

- Prompts for confirmation unless -y is passed

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `<WORKFLOW_NAME>` | The name of the workflow to cancel. | Yes |
| `-y, --yes` | Skip the confirmation prompt. | No |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |

Expand

Show lessSee more

**Output:** Confirmation that the workflow was cancelled.

**Examples:**

Copy code

```
# Cancel a workflow (with prompt)
scai data validate cancel MY_WORKFLOW

# Cancel a workflow (skip prompt)
scai data validate cancel MY_WORKFLOW -y
```

---

#### scai data worker

##### scai data worker setup

Create the Data Exchange Worker SPCS service on the specified compute pool.

Copy code

```
scai data worker setup --compute-pool <COMPUTE_POOL> [--connection <SNOWFLAKE_CONNECTION>] [--role <ROLE>] [--warehouse <WAREHOUSE>]
```

**Prerequisites:**

- Snowflake compute pool created and accessible
- Snowflake connection with appropriate privileges

**Behavior:**

- Creates the DEW SPCS service if it does not exist (idempotent)
- Waits for the service to reach a running state

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-p, --compute-pool` | Name of the compute pool on which the Data Exchange Worker service will run. | Yes |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |
| `--warehouse <WAREHOUSE>` | Warehouse to use. Overrides the value specified for the Snowflake connection. | No |
| `--role <ROLE>` | Role to use. Overrides the value specified for the Snowflake connection. | No |
| `--custom-image` | Custom container image path to use instead of auto-resolving the latest. Format: /db/schema/repo/image\_name:tag | No |

Expand

Show lessSee more

**Output:** Status messages indicating progress of each setup step.

**Examples:**

Copy code

```
# Set up DEW service with default connection
scai data worker setup --compute-pool MY_COMPUTE_POOL

# Set up with a specific role
scai data worker setup --compute-pool MY_COMPUTE_POOL --role MY_ROLE
```

---

##### scai data worker start

Resume the Data Exchange Worker SPCS service, or run the local worker process when –local is passed.

Copy code

```
scai data worker start [--local [<CONFIG_FILE> | --auto-config [PATH]]] [-c <CONNECTION>] [--role <ROLE>] [--warehouse <WAREHOUSE>]
```

**Prerequisites:**

- DEW service previously bootstrapped with ‘scai data worker setup’ (cloud mode)
- Python 3.11 or higher installed (local mode)
- A valid data exchange agent configuration file (local mode)

**Behavior:**

- Default (cloud): issues ALTER SERVICE … RESUME on the DEW SPCS service
- –local: installs the data exchange agent (if needed) and starts it as a foreground process

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `--local` | Run the data exchange worker as a local process (requires a DEW config file) instead of resuming the SPCS service. | No | False |
| `--auto-config <PATH>` | Automatically generates the configuration file for the data exchange agent. Optionally accepts a target path; defaults to ~/.snowflake/scai/dew\_configuration.toml. Cannot be used with CONFIG\_FILE. | No |  |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |  |
| `--warehouse <WAREHOUSE>` | Warehouse to use. Overrides the value specified for the Snowflake connection. | No |  |
| `--role <ROLE>` | Role to use. Overrides the value specified for the Snowflake connection. | No |  |

Expand

Show lessSee more

**Output:** Status message (cloud) or real-time agent output (local mode).

**Examples:**

Copy code

```
# Resume cloud DEW service
scai data worker start

# Resume with a specific role
scai data worker start --role MY_ROLE

# Run local worker with config
scai data worker start --local my-agent-config.yaml

# Generate local config template
scai data worker start --local --auto-config
```

---

##### scai data worker generate-config

Generate a TOML configuration template for the local Data Exchange Worker.

Copy code

```
scai data worker generate-config [PATH] [-c <CONNECTION>] [--role <ROLE>] [--warehouse <WAREHOUSE>] [--affinity <AFFINITY>]
```

**Prerequisites:**

- Optionally, a configured Snowflake connection to pre-fill connection fields

**Behavior:**

- Writes a TOML template to the specified path (or ~/.snowflake/scai/dew\_configuration.toml by default)
- Pre-fills the Snowflake connection name when a connection is resolved; otherwise emits `<PLACEHOLDER>` tokens
- Fails if the output file already exists

**Output:** TOML configuration file ready to edit and pass to ‘scai data worker start –local’

| Option | Description | Required |
| --- | --- | --- |
| `[PATH]` | Output path for the generated configuration file (file or directory). Defaults to ~/.snowflake/scai/dew\_configuration.toml. | No |
| `-y, --yes` | Skip the confirmation prompt. | No |
| `--affinity` | Affinity tag written to the Worker TOML (`[application].affinity`). May include `*` wildcards (for example `team-*`). See [Affinity](/migrations/aim-for-datawarehouses/manual-migration/data-migration-configuration-reference#affinity). | No |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |
| `--warehouse <WAREHOUSE>` | Warehouse to use. Overrides the value specified for the Snowflake connection. | No |
| `--role <ROLE>` | Role to use. Overrides the value specified for the Snowflake connection. | No |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Generate config at the default path
scai data worker generate-config

# Generate config at a custom path
scai data worker generate-config /tmp/my-dew.toml

# Generate config with a specific connection
scai data worker generate-config -c my-snowflake
```

---

##### scai data worker stop

Suspend or drop the Data Exchange Worker SPCS service.

Copy code

```
scai data worker stop [--connection <SNOWFLAKE_CONNECTION>] [--role <ROLE>] [--warehouse <WAREHOUSE>] [--drop]
```

**Prerequisites:**

- Snowflake connection with appropriate privileges

**Behavior:**

- By default, suspends the DEW service (can be resumed later)
- Use –drop to permanently remove the service
- –local is advisory only (local worker is a foreground process; use Ctrl-C to stop it)

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `--drop` | Drop the service instead of suspending it. Suspending is the default behavior. | No | False |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |  |
| `--warehouse <WAREHOUSE>` | Warehouse to use. Overrides the value specified for the Snowflake connection. | No |  |
| `--role <ROLE>` | Role to use. Overrides the value specified for the Snowflake connection. | No |  |

Expand

Show lessSee more

**Output:** Status message indicating whether the service was suspended or dropped.

**Examples:**

Copy code

```
# Suspend the DEW service
scai data worker stop

# Suspend with a specific role
scai data worker stop --role MY_ROLE

# Drop the DEW service permanently
scai data worker stop --drop
```

---

#### scai data orchestrator

##### scai data worker status

Report the current SPCS status of the Data Exchange Worker service, including recent container logs.

Copy code

```
scai data worker status [--log-lines [LINES]] [--watch [--poll-interval <SECONDS>]] [--connection <CONNECTION>] [--role <ROLE>] [--warehouse <WAREHOUSE>]
```

**Prerequisites:**

- DEW service previously bootstrapped with ‘scai data worker setup’
- Snowflake connection with read access to the service

**Behavior:**

- Prints the current service status (e.g. RUNNING, SUSPENDED, FAILED) and the last 20 log lines
- –log-lines controls how many log lines are shown (default 20)
- –watch tails the service forever, refreshing status and logs every –poll-interval seconds (default 5). Press Ctrl+C to stop.
- `--poll-interval <SECONDS>` overrides the watch polling cadence (minimum 1). Only valid together with –watch.

**Output:** Service status followed by recent container logs

| Option | Description | Required |
| --- | --- | --- |
| `-w, --watch` | Continuously poll service status and stream container logs. | No |
| `--log-lines [LINES]` | Number of log lines to fetch from the service container (default 20). Logs are always included in the status output. | No |
| `--poll-interval <SECONDS>` | Seconds between polls in –watch mode (default 5; minimum 1). Requires –watch. | No |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |
| `--warehouse <WAREHOUSE>` | Warehouse to use. Overrides the value specified for the Snowflake connection. | No |
| `--role <ROLE>` | Role to use. Overrides the value specified for the Snowflake connection. | No |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Show DEW service status and logs
scai data worker status

# Show last 200 log lines
scai data worker status --log-lines 200

# Watch status and stream logs (Ctrl+C to stop)
scai data worker status --watch

# Watch with a 2-second poll interval
scai data worker status --watch --poll-interval 2
```

---

##### scai data orchestrator setup

Start the Data Migration Service on a compute pool and wait for infrastructure to be ready.

Copy code

```
scai data orchestrator setup --compute-pool <COMPUTE_POOL> [--connection <SNOWFLAKE_CONNECTION>]
```

**Prerequisites:**

- Snowflake compute pool created and accessible
- Snowflake connection with appropriate privileges

**Behavior:**

- Creates the SNOWCONVERT\_AI.DATA\_MIGRATION schema if needed
- Starts the Data Migration Service on the specified compute pool
- Waits for the Data Migration Service to set up the objects in the SNOWCONVERT\_AI.DATA\_MIGRATION schema

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-p, --compute-pool` | Name of the compute pool that the Data Migration Service will run on. | Yes |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |
| `--warehouse <WAREHOUSE>` | Warehouse to use. Overrides the value specified for the Snowflake connection. | No |
| `--role <ROLE>` | Role to use. Overrides the value specified for the Snowflake connection. | No |
| `--custom-image` | Custom container image path to use instead of auto-resolving the latest. Format: /db/schema/repo/image\_name:tag | No |

Expand

Show lessSee more

**Output:** Status messages indicating progress of each setup step.

**Examples:**

Copy code

```
# Set up with default connection
scai data orchestrator setup --compute-pool MY_COMPUTE_POOL

# Set up with specific connection
scai data orchestrator setup --compute-pool MY_COMPUTE_POOL --connection my-snowflake

# Set up with a specific warehouse
scai data orchestrator setup --compute-pool MY_COMPUTE_POOL --warehouse MY_WAREHOUSE
```

---

##### scai data orchestrator start

Resume the cloud Data Migration Service (SPCS), or run the orchestrator locally when –local is passed.

Copy code

```
scai data orchestrator start [--local] [--connection <SNOWFLAKE_CONNECTION>] [--role <ROLE>] [--warehouse <WAREHOUSE>]
```

**Prerequisites:**

- Service previously bootstrapped with ‘scai data orchestrator setup’
- Snowflake connection with appropriate privileges

**Behavior:**

- Default (cloud): issues ALTER SERVICE … RESUME on the Data Migration SPCS service
- –local: starts the orchestrator as a foreground process using the resolved Snowflake connection

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `--local` | Run the orchestrator as a local process instead of resuming the SPCS service. | No | False |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |  |
| `--warehouse <WAREHOUSE>` | Warehouse to use. Overrides the value specified for the Snowflake connection. | No |  |
| `--role <ROLE>` | Role to use. Overrides the value specified for the Snowflake connection. | No |  |

Expand

Show lessSee more

**Output:** Status message indicating whether the service was resumed.

**Examples:**

Copy code

```
# Resume the cloud orchestrator
scai data orchestrator start

# Resume with a specific role
scai data orchestrator start --role MY_ROLE

# Run the orchestrator locally
scai data orchestrator start --local
```

---

##### scai data orchestrator stop

Suspend or drop the Data Migration Service.

Copy code

```
scai data orchestrator stop [--connection <SNOWFLAKE_CONNECTION>] [--role <ROLE>] [--warehouse <WAREHOUSE>] [--drop]
```

**Prerequisites:**

- Snowflake connection with appropriate privileges
- Orchestrator previously started with ‘scai data orchestrator setup’ or ‘scai data migrate start –start-service’

**Behavior:**

- By default, suspends the Data Migration Service (can be resumed later)
- Use –drop to permanently remove the service instead of suspending it

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `--drop` | Drop the service instead of suspending it. Suspending is the default behavior. | No | False |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |  |
| `--warehouse <WAREHOUSE>` | Warehouse to use. Overrides the value specified for the Snowflake connection. | No |  |
| `--role <ROLE>` | Role to use. Overrides the value specified for the Snowflake connection. | No |  |

Expand

Show lessSee more

**Output:** Status message indicating whether the service was suspended or dropped.

**Examples:**

Copy code

```
# Suspend the orchestrator (default)
scai data orchestrator stop

# Suspend with a specific role
scai data orchestrator stop --role MY_ROLE

# Drop the orchestrator permanently
scai data orchestrator stop --drop
```

---

##### scai data orchestrator status

Report the current SPCS status of the Data Migration Orchestrator service, including recent container logs.

Copy code

```
scai data orchestrator status [--log-lines [LINES]] [--watch [--poll-interval <SECONDS>]] [--connection <CONNECTION>] [--role <ROLE>] [--warehouse <WAREHOUSE>]
```

**Prerequisites:**

- Orchestrator previously bootstrapped with ‘scai data orchestrator setup’
- Snowflake connection with read access to the service

**Behavior:**

- Prints the current service status (e.g. RUNNING, SUSPENDED, FAILED) and the last 20 log lines
- –log-lines controls how many log lines are shown (default 20)
- –watch tails the service forever, refreshing status and logs every –poll-interval seconds (default 5). Press Ctrl+C to stop.
- `--poll-interval <SECONDS>` overrides the watch polling cadence (minimum 1). Only valid together with –watch.

**Output:** Service status followed by recent container logs

| Option | Description | Required |
| --- | --- | --- |
| `-w, --watch` | Continuously poll service status and stream container logs. | No |
| `--log-lines [LINES]` | Number of log lines to fetch from the service container (default 20). Logs are always included in the status output. | No |
| `--poll-interval <SECONDS>` | Seconds between polls in –watch mode (default 5; minimum 1). Requires –watch. | No |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (from connections.toml). Uses default if not specified. | No |
| `--warehouse <WAREHOUSE>` | Warehouse to use. Overrides the value specified for the Snowflake connection. | No |
| `--role <ROLE>` | Role to use. Overrides the value specified for the Snowflake connection. | No |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Show orchestrator status and logs
scai data orchestrator status

# Show last 200 log lines
scai data orchestrator status --log-lines 200

# Watch status and stream logs (Ctrl+C to stop)
scai data orchestrator status --watch

# Watch with a 2-second poll interval
scai data orchestrator status --watch --poll-interval 2
```

---

#### scai data doctor

Run health checks for a data migration or validation setup: Snowflake grants, DEW config, orchestrator connectivity, workflow config schema, and partition key feasibility.

Copy code

```
scai data doctor [OPTIONS]
```

**Behavior:**

- Snowflake grants check (CLI-side): verifies the resolved role has the privileges required for cloud data operations. Reports PASS/FAIL/WARN/SKIP.
- DEW health check: spawns the local DEW Python process and validates its configuration file (~/.scai/dew\_configuration.toml).
- Orchestrator health check: spawns the local orchestrator Python process to verify Snowflake connectivity and (when –config is provided) the workflow YAML schema.
- Partition key feasibility (Phase 2.5): when a migration config is resolved, runs NULL-ratio and cardinality queries against the source database for every table that has columnNamesToPartitionBy configured.
- With –analyze-partition-keys: for tables with no configured partition column, suggests a candidate from the table’s primary key (via the Code Unit Registry) and probes it as well.
- Reports PASS, FAIL, WARN, or SKIP for each check across all sections.
- Does not create or modify any objects.
- Snowflake connection is optional; when omitted, Snowflake-side checks are skipped.
- Source connection is optional; when omitted, partition key feasibility probes emit Skipped rows.

**Sections:**

- Snowflake: target-side grants and privilege checks
- DEW: DEW config file validation and system resource checks
- Orchestrator: Snowflake connectivity and workflow config schema validation
- Partition key: NULL-ratio and cardinality feasibility for configured (and suggested) partition columns

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-c, --connection <CONNECTION>` | Snowflake connection name to use for target-side grant checks. Uses the project default when omitted. | No |
| `--source-connection <SOURCE_CONNECTION>` | Source database connection name to use for partition key feasibility probes. Falls back to the project default source connection when omitted. | No |
| `--config <PATH>` | Path to the migration or validation workflow YAML file. Enables workflow config schema validation and (for migration configs) partition key feasibility checks. When –analyze-partition-keys is used without –config, defaults to the project’s standard migration config path. | No |
| `--analyze-partition-keys` | For tables in the migration config that have no columnNamesToPartitionBy configured, suggest a candidate column from the table’s primary key (via the Code Unit Registry) and run partition feasibility analysis (NULL ratio, cardinality) against the source database. Requires –source or a project default source connection. When –config is omitted, falls back to the project default migration config path. | No |

Expand

Show lessSee more

**Output:** Per-check PASS/FAIL/WARN/SKIP results grouped by section, followed by system recommendations (e.g. suggested max\_threads based on available RAM and CPU cores).

**Examples:**

Copy code

```
# Run all health checks with default connections
scai data doctor

# Run with explicit Snowflake and source connections
scai data doctor --connection my-snowflake --source-connection my-sqlserver

# Include workflow config schema validation
scai data doctor --config data-migration-config.yaml

# Probe partition key feasibility for configured columns
scai data doctor --config data-migration-config.yaml --source-connection my-sqlserver

# Suggest and probe partition columns for tables with none configured (uses default config path)
scai data doctor --analyze-partition-keys --source-connection my-sqlserver

# Full check: explicit config, source connection, and partition key suggestion
scai data doctor --config data-migration-config.yaml --source-connection my-sqlserver --analyze-partition-keys
```

---

### scai assessment

Generate migration planning insights from source code and SnowConvert reports

#### scai assessment object-exclusion

Identify database objects that can be excluded from migration based on naming patterns.

Copy code

```
scai assessment object-exclusion --project-dir <PATH> [OPTIONS]
```

**Prerequisites:**

- SnowConvert output (registry JSON files or CSV reports)

**Categories analyzed:**

- Temporary/Staging - Work tables and intermediate data
- Deprecated/Legacy - Old/backup versions
- Testing - Test/demo objects
- Duplicates - Same object in multiple files
- Version conflicts - Multiple versions detected

**Output:** JSON file with detailed analysis results; console summary with statistics and recommendations; breakdown by schema and category

| Option | Description | Required |
| --- | --- | --- |
| `--project-dir <PATH>` | Path to SnowConvert project directory | No |
| `--csv-dir <PATH>` | Path to SnowConvert reports directory (CSV files) | No |
| `-o, --output-dir <PATH>` | Output directory for analysis results (default: current directory) | No |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Analyze project output
scai assessment object-exclusion --project-dir ./my-project

# Specify CSV reports directory explicitly
scai assessment object-exclusion --csv-dir ./output/converted/Reports

# Custom output directory
scai assessment object-exclusion --project-dir ./my-project -o ./analysis-results
```

---

#### scai assessment waves

Analyze code units and generate a wave deployment plan that groups them into ordered migration waves, ensuring each wave can be deployed before the next.

Copy code

```
scai assessment waves [OPTIONS]
```

**Prerequisites:**

- Must run inside a SCAI project

**Modes:**

- Default: leads with type-ordered waves (databases -> schemas -> tables -> views -> functions), then groups the rest by dependency.
- –no-category-waves: builds waves purely by dependency order; each wave may mix object types.

**Behavior:**

- Ordered list of waves, each containing objects safe to deploy together
- Summary of object counts, categories, and dependencies per wave
- Highlights of circular dependencies and top-connected objects
- List of missing code units (referenced but not found in the registry)
- Registry updated so each code unit records its assigned wave

**Output:** `<projectRoot>/assessment/waves_analysis_YYYYMMDD_HHMMSS.json`

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `--min-size <N>` | Minimum target wave size (default: 40) | No | 40 |
| `--max-size <N>` | Maximum wave size (default: 80) | No | 80 |
| `--prioritize <PATTERN>` | Glob patterns for user-prioritized objects (repeatable) | No |  |
| `--no-category-waves` | Disable category-based waves (use pure dependency order) | No |  |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Generate waves with defaults
scai assessment waves

# Customise wave sizes
scai assessment waves --min-size 50 --max-size 100

# Prioritise matching objects
scai assessment waves --prioritize "*invoice*"

# Disable category waves
scai assessment waves --no-category-waves
```

---

### scai license

Install offline license for air-gapped environments

#### scai license install

Install an offline license for running conversions without online activation.

Copy code

```
scai license install -p <LICENSE_PATH>
```

**Prerequisites:**

- A valid offline license file (.lic) from Snowflake

**Behavior:**

- Validates the license file
- Installs it for use by conversion commands

**Use cases:**

- Running in air-gapped environments without internet
- CI/CD pipelines that can’t use online activation
- Environments with restricted network access

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-p, --path <LICENSE_PATH>` | Path to the license file to install | Yes |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Install license
scai license install --path /path/to/license.lic
```

---

### scai terms

Display the terms and conditions text. You must accept the terms before using most CLI commands.

Copy code

```
scai terms
```

**Behavior:**

- Displays the full terms and conditions text in a styled panel
- Does not prompt for acceptance; use ‘scai terms accept’ to accept

**Examples:**

Copy code

```
# View terms and conditions
scai terms
```

#### scai terms accept

Display terms and conditions and prompt for acceptance.

Copy code

```
scai terms accept
```

**Behavior:**

- Displays the full terms and conditions text
- Prompts: Do you accept the terms and conditions?
- Records acceptance to ~/.scai/license-agreement.json when accepted
- If already accepted, reports success without prompting

**Examples:**

Copy code

```
# Accept terms interactively
scai terms accept

# Accept via environment variable (CI/CD)
export SCAI_ACCEPT_TERMS=true
```

---

### scai settings

View and manage user-level CLI settings stored in ~/.snowflake/scai/settings.json.

Copy code

```
scai settings <list|get|set|unset> [...]
```

**Behavior:**

- Resolution order (precedence): SCAI\_\* environment variables, then ~/.snowflake/scai/settings.json, then built-in defaults from appsettings.json. When no layer supplies a value the source is reported as ‘unset’ (e.g. channel when no built-in is shipped).
- Writes are atomic: the file is replaced via a temp-file move so a partial write cannot leave invalid JSON on disk

#### scai settings list

List all settings, their resolved values, and sources.

Copy code

```
scai settings list [--json]
```

**Behavior:**

- Displays every known CLI setting with its currently resolved value and the source that produced it
- Surfaces active SCAI\_\* environment variable overrides explicitly
- Resolution order: SCAI\_\* env vars, then ~/.snowflake/scai/settings.json, then built-in defaults from appsettings.json. Source is reported as ‘unset’ when no layer supplies a value.

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `--json` | Emit the result as a structured JSON envelope (agent-friendly, stable schema). | No |

Expand

Show lessSee more

**Output:** Table with key, resolved value, and source for each setting. With –json, a structured envelope with a stable schema.

**Examples:**

Copy code

```
# List all settings
scai settings list

# Machine-readable output
scai settings list --json
```

---

#### scai settings get

Read a single setting’s resolved value and source.

Copy code

```
scai settings get <KEY> [--json]
```

**Behavior:**

- Reads the resolved value for KEY and reports the source that produced it
- Returns a non-zero exit code when KEY is unknown
- In –json mode emits a single-entry envelope with the same shape as ‘settings list’
- Resolution order: SCAI\_\* env vars, then ~/.snowflake/scai/settings.json, then built-in defaults from appsettings.json. Source is reported as ‘unset’ when no layer supplies a value.

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `<KEY>` | Setting key to read. | Yes |
| `--json` | Emit the result as a structured JSON envelope. | No |

Expand

Show lessSee more

**Output:** Bare resolved value (pipe-friendly), or a single-entry JSON envelope when –json is set.

**Examples:**

Copy code

```
# Read the update channel
scai settings get channel

# Read auto-update preference
scai settings get autoUpdate
```

---

#### scai settings set

Set one or more settings atomically (validate-then-write).

Copy code

```
scai settings set <KEY=VALUE> [<KEY=VALUE>...] [--json]
```

**Behavior:**

- All KEY=VALUE pairs are validated before any write
- If any pair is invalid, no changes are persisted (validate-then-mutate guarantee)
- Each KEY may appear at most once per invocation
- The file is written via a single atomic replace
- SCAI\_\* environment variables override the file, so a successful ‘set’ may not change the resolved value for the current process

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `<KEY=VALUE>` | One or more ‘key=value’ assignments to apply atomically. Each key may appear at most once. | Yes |
| `--json` | Emit the result as a structured JSON envelope. | No |

Expand

Show lessSee more

**Output:** Per-key change report (Updated, Already set). With –json, a structured envelope listing requested, applied, and no-op changes.

**Examples:**

Copy code

```
# Switch to the preview channel
scai settings set channel=preview

# Disable auto-update
scai settings set autoUpdate=false

# Set both atomically
scai settings set channel=stable autoUpdate=true
```

---

#### scai settings unset

Clear one or more settings from the file.

Copy code

```
scai settings unset <KEY> [<KEY>...] [--json]
```

**Behavior:**

- All keys are validated before any write
- Unknown keys fail the whole batch and the file is left untouched
- Already-absent keys are reported as no-ops and skip the write
- Each KEY may appear at most once per invocation
- Built-in defaults take effect once a value is cleared, unless an SCAI\_\* environment variable is also set
- Surfaces active SCAI\_\* overrides so the resolved value is never a surprise

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `<KEY>` | One or more setting keys to clear from the file atomically. Each key may appear at most once. | Yes |
| `--json` | Emit the result as a structured JSON envelope. | No |

Expand

Show lessSee more

**Output:** Per-key clear report (Cleared, was not set). With –json, a structured envelope listing requested, applied, and no-op clears.

**Examples:**

Copy code

```
# Clear the channel override
scai settings unset channel

# Clear both settings
scai settings unset channel autoUpdate
```

---

### scai update

Force an immediate self-update on the current channel.

Copy code

```
scai update [VERSION] [--channel <CHANNEL>]
```

**Behavior:**

- Checks the configured channel for the latest published version
- Downloads, verifies, and installs the archive for user-local installs
- Prints the resolved channel before running

**Channel resolution (precedence):**

- SCAI\_CHANNEL environment variable
- Channel saved in the scai settings file
- Built-in channel from the installed binary

**Requirements:**

- User-local install (system-level installs must update via their package manager)
- Network access to the update channel

| Option | Description | Required |
| --- | --- | --- |
| `[VERSION]` | Specific version to install (e.g., 2.5.0 or 2.6.0-rc.3) | No |
| `--channel <CHANNEL>` | One-shot channel override (stable | preview |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Update to the latest version on the current channel
scai update

# Switch channels for this update via env var
SCAI_CHANNEL=preview scai update

# Request a specific published version
scai update 2.5.0

# One-shot channel override (stable | preview | dev)
scai update --channel preview
```

---

### scai versions

List locally installed CLI version directories for user-local installs and mark the version that matches the running binary; system-level installs print a short package-manager note instead.

Copy code

```
scai versions [--json]
```

**Behavior:**

- Resolves whether the install is user-local (side-by-side version folders under an install root) or system-level (single package-managed binary).
- User-local: scans the install root for SemVer-named directories (skips bin and invalid names), enriches each row with last-activated metadata, and marks the entry that matches the running AppVersion as current.
- User-local with no matching directories: prints guidance to run scai update.
- System-level: explains that updates are owned by the platform installer rather than side-by-side folders.

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `--json` | Emit the standard JSON envelope with the structured versions listing in result (global flag; may appear anywhere on the command line). | No |

Expand

Show lessSee more

**Output:** Human-readable table with install root and a (current) marker on the active row, or a short message for empty user-local layouts and system installs. With –json, the envelope result includes installRoot (null on system installs), installType (user-local | system), currentVersion, and a versions[] array with directory metadata plus isCurrent.

**Examples:**

Copy code

```
# Inspect installed copies next to channel configuration
scai versions

# Machine-readable inventory for scripts or agents
scai versions --json
```

#### scai versions remove

Delete an inactive SemVer install directory under the user-local install root and report how many bytes were freed.

Copy code

```
scai versions remove <VERSION> [[-f|--force]] [--json]
```

**Prerequisites:**

- User-local install only (system-level installs must use the OS package manager)

**Behavior:**

- Validates the version string as SemVer and ensures the directory exists before deletion.
- Refuses to remove the currently running version, non-SemVer strings, or paths that are not present on disk.
- Interactive TTY without –force prompts once for confirmation; non-interactive consoles skip the prompt; –force skips confirmation everywhere.
- Emits freed disk space after a successful delete (human mode) or a JSON result with version, installRoot, and freedBytes when –json is active.

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `<VERSION>` | SemVer directory name to remove (for example 2.5.0). | Yes |
| `-f, --force` | Skip the interactive delete confirmation. | No |
| `--json` | Emit the standard JSON envelope with removal metadata in result (global flag). | No |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Remove an older build after switching channels or updating
scai versions remove 2.4.0

# Non-interactive delete for automation
scai versions remove 2.4.0 --force

# Structured output for auditing reclaimed space
scai versions remove 2.4.0 --force --json
```

---

### scai object-selector

Create selector files for filtering objects

#### scai object-selector create

Create a selector file to filter objects for data migration.

Copy code

```
scai object-selector create [OPTIONS]
```

**Prerequisites:**

- Code converted with ‘scai code convert’ (generates TopLevelCodeUnits report)

**Behavior:**

- Reads the TopLevelCodeUnits report from conversion
- Creates a YAML selector file for filtering objects
- Allows filtering by database, schema, and object type

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-d, --database <NAME>` | Filter objects by source database name. | No |
| `-s, --schema <NAME>` | Filter objects by source schema name. | No |
| `-t, --type <TYPES>` | Filter objects by type (comma-separated, e.g., table,view,procedure). | No |
| `-n, --name <NAME>` | Label for the selector file (becomes `<name>.<timestamp>.yml`), if not provided, it will be called `object-selector.<timestamp>.yml`. | No |

Expand

Show lessSee more

**Output:** selector.yml file with object definitions

```
objects:
  - code_unit_id: <database>.<schema>.<name>
    type: TABLE | VIEW | PROCEDURE | ...
    source: { database, schema, name }
    target: { database, schema, name }
```

**Examples:**

Copy code

```
# Create selector file
scai object-selector create

# Create with custom output path
scai object-selector create -o custom-selector.yml
```

---

### scai query

Execute SQL queries on source database systems.

Copy code

```
scai query -q <QUERY> -s <CONNECTION> [-l <LANGUAGE>]
```

**Prerequisites:**

- Source database connection configured via ‘scai connection add-sql-server’, ‘scai connection add-redshift’, ‘scai connection add-teradata’, ‘scai connection add-oracle’, or ‘scai connection add-postgresql’
- Network access to the source database

**Behavior:**

- Connects to the specified source database connection
- Executes the provided SQL query
- Displays query results in a formatted table
- Limits output to 1000 rows for readability

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-q, --query <QUERY>` | SQL query to execute on the source system. | Yes |
| `-s, --source-connection <CONNECTION>` | Name of the source connection to use for query execution. | Yes |
| `-l, --source-language <LANGUAGE>` | Source database type (SqlServer, Redshift). If omitted, auto-detected from the connection name. | No |

Expand

Show lessSee more

**Output:** Query results printed as a formatted table in the terminal

**Examples:**

Copy code

```
# Execute simple query
scai query -q "SELECT 1;" -s my-sqlserver

# Check table row count
scai query -q "SELECT COUNT(*) FROM customers" -s my-redshift

# Query with filter
scai query -q "SELECT * FROM orders WHERE status = 'pending'" -s my-connection

# Query with explicit source language
scai query -q "SELECT COUNT(*) FROM users" -s my-sqlserver -l SqlServer
```

---

### scai logs

Display the location of CLI log files and list recent entries.

Copy code

```
scai logs [--last <COUNT>] [--open]
```

**Behavior:**

- Shows the log directory path
- Lists the N most recent log files with size and age
- Use –open to open the directory in your file explorer
- Works offline without network access
- When online, Snowflake is optional: account and user are read from local project configuration first when available, with a live connection test as a fallback when metadata is incomplete

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `--last <COUNT>` | Number of recent log files to display. | No | 5 |
| `--open` | Open the log directory in the system file explorer. | No | False |

Expand

Show lessSee more

**Output:** Table of recent log files with name, size, and age. Total log file count.

**Examples:**

Copy code

```
# Show recent log files
scai logs

# Show the last 10 log files
scai logs --last 10

# Open log directory in file explorer
scai logs --open
```

---

### scai test

Generate test cases for migrated stored procedures

#### scai test seed

Generate YAML test case files for converted stored procedures.

Copy code

```
scai test seed [--execution-log <EXECUTION_LOG>] [--source-connection <SOURCE_CONNECTION>] [--connection <CONNECTION>] [OPTIONS]
```

**Prerequisites:**

- A migration project initialized with ‘scai init’
- Code converted with ‘scai code convert’
- Optional: an execution log file produced by running the original stored procedures

**Behavior:**

- When –execution-log is provided: reads it, matches procedure calls to their converted counterparts, and generates one YAML per procedure with up to –max-cases test cases (default: 10)
- When –execution-log is omitted: generates a stub YAML with a commented test\_cases placeholder for every converted code unit
- Validates source connection (–source-connection or default source connection)
- Validates Snowflake connection (–connection, project connection, or default connection)
- By default, existing test files are overwritten (use –append to add instead)

**Options:**

| Option | Description | Required | Default |
| --- | --- | --- | --- |
| `-s, --source-connection <SOURCE_CONNECTION>` | Name of the source connection to use (from configured source connections). Uses default if not specified. | No |  |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use. Uses project/default connection if not specified. | No |  |
| `-m, --max-cases <MAX_CASES>` | Maximum number of test cases to generate per procedure. | No | 10 |
| `-a, --append` | Append test cases to existing test files instead of replacing them. | No |  |
| `-e, --execution-log <EXECUTION_LOG>` | Path to the execution log file produced by running the original stored procedures. Optional : when omitted, every code unit gets a stub YAML with a commented test\_cases placeholder. | No |  |

Expand

Show lessSee more

**Output:** One YAML test case file per procedure, nested under the artifacts folder

```
artifacts/<target_db>/<target_schema>/<object_type>/.../<procedure_name>.yml
```

**Examples:**

Copy code

```
# Generate stub YAMLs (no execution log)
scai test seed

# Generate test cases from an execution log
scai test seed --execution-log artifacts/exec_log.csv

# Limit to 5 cases per procedure
scai test seed --execution-log artifacts/exec_log.csv --max-cases 5

# Append to existing test files
scai test seed --execution-log artifacts/new_exec_log.csv --append
```

---

#### scai test capture

Capture test baselines from the source database.

Copy code

```
scai test capture [--source-connection <SOURCE_CONNECTION>] [--connection <CONNECTION>] [OPTIONS]
```

**Prerequisites:**

- A migration project initialized with ‘scai init’
- Test YAML files in artifacts/\*\*/test/\*.yml (generated by ‘scai test seed’)
- A configured source database connection
- A Snowflake connection (unless –keep-baselines is set)

**Behavior:**

- Executes each test case on the source database
- By default, uploads baselines to the Snowflake stage `@<db>.VALIDATION.BASELINES` and keeps no copy on disk
- With –keep-baselines, also persists baselines locally under `artifacts/**/baselines/<YYYYMMDD>/`

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-s, --source-connection <SOURCE_CONNECTION>` | Name of the source connection to use (from configured source connections). Uses default if not specified. | No |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use (for baseline stage upload). Uses project/default connection if not specified. | No |
| `--keep-baselines` | Also persist baselines locally under `artifacts/**/baselines/<YYYYMMDD>/`. Default: baselines are uploaded to Snowflake only and not written to disk. When set without -c/–connection, capture runs fully offline. | No |

Expand

Show lessSee more

**Output:** By default, baseline JSON files are uploaded to `@<db>.VALIDATION.BASELINES` and removed from disk. With –keep-baselines, copies remain under `artifacts/**/baselines/<YYYYMMDD>/`.

**Examples:**

Copy code

```
# Capture baselines (uploaded to Snowflake only)
scai test capture

# With explicit connections
scai test capture --source-connection my-sqlserver --connection my-snowflake

# Also keep baselines on disk
scai test capture --keep-baselines
```

---

#### scai test validate

Validate Snowflake procedures against captured baselines.

Copy code

```
scai test validate [--connection <CONNECTION>] [OPTIONS]
```

**Prerequisites:**

- A migration project initialized with ‘scai init’
- Baselines captured with ‘scai test capture’
- A configured Snowflake connection

**Behavior:**

- Discovers test YAML files with target steps
- Loads baselines from the implicit Snowflake stage `@<db>.VALIDATION.BASELINES` (or –baseline-stage)
- Executes each test case on Snowflake and compares results
- Reports pass/fail/error status for each test case

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `-c, --connection <CONNECTION>` | Name of the Snowflake connection to use. Uses project/default connection if not specified. | No |
| `--baseline-stage <BASELINE_STAGE>` | Snowflake stage containing baselines. Uses implicit default stage if not specified. | No |
| `--create-schema` | Create the VALIDATION schema and objects before running. | No |

Expand

Show lessSee more

**Output:** Pass/fail/error status report for each test case

**Examples:**

Copy code

```
# Validate all procedures
scai test validate

# Create validation schema first
scai test validate --create-schema

# Use an explicit baseline stage
scai test validate --baseline-stage @MY_DB.VALIDATION.BASELINES
```

---

#### scai test doctor

Show testing-infrastructure setup guidance. Currently emits BTEQ bindings checklist and TTU install instructions; built to host more checks.

Copy code

```
scai test doctor [--json]
```

**Prerequisites:**

- None: runs anywhere; no project or network connection required

**Behavior:**

- Each registered ITestDoctorCheck contributes one or more findings; today the only check covers BTEQ
- BTEQ check: renders a setup checklist for the bindings model (project.yml dialect, scriptBindings on script CURs, bindings: blocks in test YAML, **REPLACE\_ME** handling, credential placement)
- BTEQ check: renders OS-aware TTU install instructions (macOS Homebrew, Windows Chocolatey, Linux RPM/DEB) with the host-OS block printed first, plus a Vantage Express alternative
- Pure informational; no diagnostics are run and no failures are reported. Always exits 0
- Future test-doctor checks (e.g. binary probes, scriptBindings validation) plug in as additional ITestDoctorCheck implementations and appear here automatically

**Options:**

| Option | Description | Required |
| --- | --- | --- |
| `--json` | Emit machine-readable JSON on stdout (no Spectre markup). | No |

Expand

Show lessSee more

**Output:** Spectre table grouped under area ‘Testing: BTEQ’ (one row per finding), or a JSON array with id, severity, message, detail entries when –json is set

**Examples:**

Copy code

```
# Show testing-infrastructure setup guidance
scai test doctor

# JSON for automation
scai test doctor --json
```

---

#### scai test etl-validate

Run a converted ETL package on Snowflake, optionally launch the original SSIS package on SQL Server, and compare outputs.

Copy code

```
scai test etl-validate [--connection <CONNECTION>] [--source-connection <SOURCE_CONNECTION>] [OPTIONS]
```

**Supported languages:**

- SqlServer

**Prerequisites:**

- A migration project initialized with ‘scai init’ and converted with ‘scai code convert’
- ETL test YAML files generated via ‘scai test seed’ (or hand-authored under artifacts/\*\*/etl-tests/)
- A configured Snowflake connection that hosts the converted task DAG
- A configured SQL Server connection that hosts the SSIS catalog and source tables (unless –skip-ssis-execution is used)

**Behavior:**

- Discovers ETL packages from the CodeUnitRegistry (filtered by –platform / –where / –part-type)
- Launches the SSIS package via SSISDB.catalog or SQL Agent jobs (skippable)
- Executes the Snowflake task DAG and verifies every task reaches SUCCEEDED
- Runs cross-platform DVF comparisons on every declared source/target table pair
- Persists per-step status to `{validation_database}.VALIDATION.ETL_EXECUTION_LOG`

| Option | Description | Required |
| --- | --- | --- |
| `--platform <PLATFORM>` | ETL source platform to validate against (e.g. informatica, ssis). | No |
| `--where <WHERE>` | SQL-like WHERE clause to filter ETL code units (same syntax as ‘scai code deploy –where’). | No |
| `--check-env` | Run environment qualification checks (connectivity + platform access) instead of the full validate pipeline. Recommended before long runs to surface misconfigured connections early. | No |
| `--skip-ssis-execution` | Skip the source-platform execution step and only run Snowflake-side validation tracks. | No |
| `-c, --connection <CONNECTION>` | Named Snowflake connection to use (from connections.toml). Overrides the value in test\_config.yaml when supplied. | No |
| `-s, --source-connection <SOURCE_CONNECTION>` | Named source-database connection to use. Overrides the value in test\_config.yaml when supplied. | No |

Expand

Show lessSee more

**Examples:**

Copy code

```
# Validate all ETL units (SSIS by default)
scai test etl-validate

# With explicit connections
scai test etl-validate --source-connection my-sqlserver --connection my-snowflake

# Skip the SSIS launch branch
scai test etl-validate --skip-ssis-execution

# Filter to a single unit
scai test etl-validate --where "id = 'pkg:LoadCustomers'"
```

---

## Snowflake connections

SnowConvert AI uses the Snowflake CLI for Snowflake connections. This is separate from the scai CLI.

**Configuration commands:**

Copy code

```
# Add a Snowflake connection
snow connection add

# Set default Snowflake connection
snow connection set-default <connection-name>
```

**Use connections in scai:**

Copy code

```
# Deploy with specific connection
scai code deploy -c my-snowflake
```

For more information, see [Configure Snowflake CLI connections](https://docs.snowflake.com/en/developer-guide/snowflake-cli/connecting/configure-connections).

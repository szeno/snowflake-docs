# Configure a gen 2 connector with SQL

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

This topic describes how to **create and configure** a gen 2 connector using SQL and stage
commands—the programmatic alternative to the [Configure a connector with the setup wizard](/user-guide/data-integration/openflow/gen2/setup-connector-wizard).
Use this workflow when you want to automate connector setup, manage configuration as code, or
integrate with CI/CD.

The same connector objects can also be managed from the Openflow UI; changes made in one interface
are visible in the other.

## Prerequisites

Before you begin:

- A gen 2 **deployment** and **runtime**. See [Quickstart: gen 2 Openflow](/user-guide/data-integration/openflow/gen2/quickstart) if you need to create them.
- `CREATE OPENFLOW CONNECTOR` on the schema and `USAGE` on the runtime.
- Complete any connector-specific source database prerequisites first:
  [PostgreSQL CDC](/user-guide/data-integration/openflow/connectors/postgres/setup#source-database-setup) |
  [MySQL and MariaDB CDC](/user-guide/data-integration/openflow/connectors/mysql/setup#source-database-setup).
  For Snowflake account setup (destination database, warehouse, and secrets), follow the
  [Snowflake account setup](/user-guide/data-integration/openflow/connectors/postgres/setup#snowflake-account-setup)
  on those pages.
- A client that supports `GET` and `PUT` on stages. Snowsight does **not** support `GET`/`PUT`
  on connector stages; use Snowflake CLI or another supported client.

Tip

For your first connector configuration, use the
[Configure a connector with the setup wizard](/user-guide/data-integration/openflow/gen2/setup-connector-wizard). When you need a template for SQL or
automation, create a draft with the wizard and download `config.json` from the live version (see
[Upload and commit configuration](#label-openflow-configure-connector-sql-configure)).

## Create the connector

The SQL examples in this topic assume you created a database and schema (see
[Quickstart: gen 2 Openflow](/user-guide/data-integration/openflow/gen2/quickstart)) and set the session context:

Copy code

```
USE DATABASE my_db;
USE SCHEMA my_schema;
```

Connectors and runtimes are schema-level objects; the examples below use simple names. `snow://`
URI paths use the connector’s fully qualified name.

Create a connector in a gen 2 runtime from a catalog **definition ID**. Each gen 2 catalog entry
maps to a definition ID—the value you pass to `FROM DEFINITION`.

To find definition IDs available in your account:

- Run `SHOW OPENFLOW CONNECTOR DEFINITIONS` (optionally with `LIKE` to filter). The `name`
  column is the definition ID. See [SHOW OPENFLOW CONNECTOR DEFINITIONS](/sql-reference/sql/show-openflow-connector-definitions).
- Browse **gen 2** entries in the Openflow connector catalog (see
  [Configure a connector with the setup wizard](/user-guide/data-integration/openflow/gen2/setup-connector-wizard)).

Example for PostgreSQL CDC:

Copy code

```
CREATE OPENFLOW CONNECTOR my_connector
  IN RUNTIME my_runtime
  FROM DEFINITION OPENFLOW_POSTGRES_CDC
  DISPLAY_NAME = 'My Postgres CDC Connector';
```

The connector is created in **STOPPED** state with a **Draft** status: a **live** configuration
version exists, but no committed **default** version yet. You must configure and commit before
starting. See [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning).

## Upload and commit configuration

Gen 2 connectors store configuration in `config.json` on the connector’s
[internal versioned stage](/user-guide/data-integration/openflow/gen2/connector-versioning#label-openflow-fbe-versioned-stage). The
standard workflow is download → edit → upload → commit.

1. List files in the live version:

   Copy code

   ```
   LS 'snow://openflow_connector/my_db.my_schema.my_connector/versions/live';
   ```
2. Download `config.json` to your local machine:

   Copy code

   ```
   GET 'snow://openflow_connector/my_db.my_schema.my_connector/versions/live/config.json'
     file:///path/to/local/;
   ```

   Or with Snowflake CLI:

   Copy code

   ```
   snow stage copy 'snow://openflow_connector/my_db.my_schema.my_connector/versions/live/config.json' .
   ```
3. Edit `config.json` locally. Reference passwords and other secrets with
   `valueType = SECRET_REFERENCE` (see [Secrets in configuration](#label-openflow-configure-connector-sql-secrets)).
4. Upload the updated file to the live version:

   Copy code

   ```
   PUT 'file:///path/to/config.json'
     'snow://openflow_connector/my_db.my_schema.my_connector/versions/live/'
     AUTO_COMPRESS = FALSE
     OVERWRITE = TRUE;
   ```

   Warning

   The destination is the live version **directory**, not the file path. `PUT` appends the
   source file name automatically. If you include `config.json` in the destination, it creates
   a nested `config.json/config.json` object that shadows the real file.
5. Commit the live version to create the default:

   Copy code

   ```
   ALTER OPENFLOW CONNECTOR my_connector COMMIT;

   SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_CONNECTORS(600, 'my_connector');
   ```

For full details on live, default, and `LAST` versions, see [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning).

## Start the connector

After configuration is committed:

Copy code

```
ALTER OPENFLOW CONNECTOR my_connector START;

SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_CONNECTORS(600, 'my_connector');
```

To stop or remove the connector, see [Manage the gen 2 Openflow connector lifecycle](/user-guide/data-integration/openflow/gen2/manage-connector-lifecycle).
To monitor connector health and ingestion status, see
[Monitor connectors using the Openflow Connectors Dashboard](/user-guide/data-integration/openflow/connectors-dashboard).

## Edit an existing connector

To change configuration after a commit:

1. Create a new live version from the current default:

   Copy code

   ```
   ALTER OPENFLOW CONNECTOR my_connector ADD LIVE VERSION FROM LAST;
   ```
2. Download, edit, and upload `config.json` as in
   [Upload and commit configuration](#label-openflow-configure-connector-sql-configure).
3. Commit or abort:

   Copy code

   ```
   ALTER OPENFLOW CONNECTOR my_connector COMMIT;

   -- Or discard changes:
   ALTER OPENFLOW CONNECTOR my_connector ABORT;
   ```

## Secrets in configuration

Do not store passwords as plain text in `config.json`. Create a
[Snowflake secret](/sql-reference/sql/create-secret) and reference it with
`valueType = SECRET_REFERENCE`. Most connectors require secrets with `TYPE = GENERIC_STRING`. Check
the setup topic for your connector to confirm the required type.

The setup wizard generates the correct `SECRET_REFERENCE` structure for you. For SQL workflows,
create a connector draft with the wizard, download `config.json` from the live version, and reuse
that structure when you edit secrets and connection settings for additional connectors.

Example `SECRET_REFERENCE` (PostgreSQL CDC):

Copy code

```
"Source Database Password": {
  "valueType": "SECRET_REFERENCE",
  "fullyQualifiedSecretName": "openflow_db.openflow_schema.MY_SECRET"
}
```

Grant **READ** on each referenced secret to the runtime’s `EXECUTE_AS_ROLE`. The role also
needs **USAGE** on the secret’s database and schema. Grant these privileges before you start the
connector.

## Create from a known configuration (optional)

For your first connector, use `FROM DEFINITION` (above) or the setup wizard. When you already
have a validated `config.json` and want to stand up another connector with the same settings—for
example in a different runtime or environment—see [Create from a known configuration](/user-guide/data-integration/openflow/gen2/connector-versioning#label-openflow-fbe-git-create) in [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning).

## Wizard vs SQL

| Approach | When to use it |
| --- | --- |
| [Configure a connector with the setup wizard](/user-guide/data-integration/openflow/gen2/setup-connector-wizard) | Interactive setup with step-by-step validation; best for first-time configuration of connector types that support the setup wizard. |
| SQL (this topic) | Automation, repeat deployments, CI/CD, and bulk connector creation; required for clients that manage Openflow programmatically. |

Expand

Show lessSee more

Both approaches create the same gen 2 connector object and `config.json` format.

## Next steps

- [CREATE OPENFLOW CONNECTOR](/sql-reference/sql/create-openflow-connector), [ALTER OPENFLOW CONNECTOR](/sql-reference/sql/alter-openflow-connector) — Full `CREATE` and `ALTER` syntax for connectors.
- [gen 2 connector configuration and versioning](/user-guide/data-integration/openflow/gen2/connector-versioning) — Version states, UI labels, and [create from a known configuration](/user-guide/data-integration/openflow/gen2/connector-versioning#label-openflow-fbe-git-create).
- [Manage the gen 2 Openflow connector lifecycle](/user-guide/data-integration/openflow/gen2/manage-connector-lifecycle) — Start, stop, and remove gen 2 connectors.

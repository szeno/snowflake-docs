# Gen 2 connector configuration and versioning

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Tip

**Using the setup wizard or** **Installed Connectors** **only?** You do not need this topic for
day-to-day work. The Openflow UI creates and manages configuration versions automatically as you
install, edit, and save connector settings. Labels such as **Draft** and **Edits not applied**
reflect the same version states described below—you can follow the wizard and UI prompts without
reading about stages or `COMMIT`.

Read this topic if you configure connectors with SQL, `GET`/`PUT` on stages, Git, or other
automation—or if you want to understand what the UI is doing under the hood.

Gen 2 Openflow connectors are **File Based Entities (FBEs)**: Snowflake objects whose
configuration is stored as files on an internal **versioned stage** that Snowflake creates and
manages on the connector object. You do not create this stage with `CREATE STAGE`—it is attached
automatically when the connector is created. Configuration files (for example, `config.json`)
and assets (for example, JDBC driver JARs) live under versioned paths on that stage.

This topic explains the version states, UI labels, SQL workflow for editing connector configuration,
and how to list, download, and upload files on the connector stage. Other Snowflake object types
(for example, dbt projects and Cortex agents) use a similar versioned-stage model with their own
`snow://` URI schemes; here we cover Openflow connectors only.

## Access the connector’s versioned stage

Each connector version is an immutable snapshot in the connector’s version history. Versions behave
similarly to Git commits: if a new version does not change a file, both versions can reference the
same underlying file. Use the `snow://openflow_connector/` URI scheme to reference files:

Copy code

```
snow://openflow_connector/<database>.<schema>.<connector_name>/versions/<version>/[<file_name>]
```

`version` is one of:

- `live` — writable working copy (see [Version states](#label-openflow-fbe-version-states) below)
- `LAST` — alias for the most recently committed (default) version
- `VERSION$N` — a specific committed version (for example, `VERSION$1`)
- A user-assigned name — set when you commit; preserved for later reference (for example,
  `production-config`)

You can use a user-assigned name or `VERSION$N` in `snow://` paths and SQL when referencing a
committed version.

List, download, and upload files with the standard stage commands documented in
[File staging commands](/sql-reference/commands-file) (`LIST`, `GET`, and `PUT`). Pass the URI as a quoted string (for
example, `GET 'snow://openflow_connector/...'`).

Note

Snowsight does not support `GET` or `PUT` on connector stages. Use Snowflake CLI or another client
that supports stage file operations.

You can also inspect version metadata with `SHOW VERSIONS IN OPENFLOW CONNECTOR` and connector
properties (including the active version) with `DESCRIBE OPENFLOW CONNECTOR`. See
[SHOW VERSIONS IN OPENFLOW CONNECTOR](/sql-reference/sql/show-versions-in-openflow-connector) and [DESCRIBE OPENFLOW CONNECTOR](/sql-reference/sql/desc-openflow-connector).

## Version states

| Term | Description | SQL path |
| --- | --- | --- |
| **live** | In-progress edits (writable stage). Created automatically when a connector is created via UI or SQL `FROM DEFINITION`. | `versions/live` |
| **default** | The committed version the runtime runs when the connector starts. | `versions/LAST` (alias) |
| **LAST** | Alias for the most recently committed (default) version. | `versions/LAST` |

Expand

Show lessSee more

The **live** version is your working copy. The **default** version is what runs when the connector
starts in the target runtime. In stage paths, `versions/LAST` points to the **default** (committed)
version. Committing the live version creates a new immutable default and removes the live version.

While a connector is **RUNNING**, you can still edit the live version. Changes are not applied to
the running connector until you **COMMIT** (UI **Apply** or SQL `COMMIT`).

## UI labels

| UI label | Meaning |
| --- | --- |
| **Draft** | Live version exists; no default version yet. The connector was created but never committed. Commit before starting. |
| **Edits not applied** | Both live and default versions exist. Changes are in progress but not committed. |
| *(no label)* | Only a default version exists. Stable state. |

Expand

Show lessSee more

## Configuration workflow

New connectors created with `CREATE OPENFLOW CONNECTOR ... FROM DEFINITION` or the setup wizard
start with a live version and no default (**Draft**).

1. Upload or edit files in the live version (skip `ADD LIVE VERSION` on a new connector—it already
   has a live version).
2. Commit to promote live to default:

   Copy code

   ```
   ALTER OPENFLOW CONNECTOR my_db.my_schema.my_connector COMMIT;
   ```
3. To discard uncommitted changes:

   Copy code

   ```
   ALTER OPENFLOW CONNECTOR my_db.my_schema.my_connector ABORT;
   ```
4. To edit a committed connector, create a new live version seeded from the current default:

   Copy code

   ```
   ALTER OPENFLOW CONNECTOR my_db.my_schema.my_connector ADD LIVE VERSION FROM LAST;
   ```

## Stage file operations

The following examples use the [snow://openflow\_connector/ URI](#label-openflow-fbe-versioned-stage).
Replace `my_db.my_schema.my_connector` with your connector’s fully qualified name.

List files in the live version:

Copy code

```
LS 'snow://openflow_connector/my_db.my_schema.my_connector/versions/live';
```

Download the last committed `config.json` (use `snow sql` or another client that supports
`GET` on stages; Snowsight does not support `GET`/`PUT` on stages):

Copy code

```
GET 'snow://openflow_connector/my_db.my_schema.my_connector/versions/LAST/config.json'
  file:///path/to/local/;
```

Upload to the live version:

Copy code

```
PUT 'file:///path/to/config.json'
  'snow://openflow_connector/my_db.my_schema.my_connector/versions/live/config.json'
  AUTO_COMPRESS = FALSE
  OVERWRITE = TRUE;
```

After uploading, commit:

Copy code

```
ALTER OPENFLOW CONNECTOR my_db.my_schema.my_connector COMMIT;

SELECT SYSTEM$WAIT_FOR_STABLE_OPENFLOW_CONNECTORS(600, 'my_db.my_schema.my_connector');
```

## Create from a known configuration

Use this workflow when you already have a **validated** connector configuration and want to create
another connector with the same settings—for example, standing up a matching connector in a second
runtime, or automating repeat deployments with CI/CD.

This is **not** the path for your first connector. Create and configure a connector once with the
setup wizard or `CREATE OPENFLOW CONNECTOR ... FROM DEFINITION`, then export the configuration.

### Definition vs configuration

A catalog **definition** (for example, `OPENFLOW_POSTGRES_CDC`) and instance **configuration**
(`config.json`) are separate:

- `FROM DEFINITION` in `CREATE OPENFLOW CONNECTOR` selects the catalog connector type. You then
  edit `config.json` on the connector’s versioned stage and **COMMIT**.
- `FROM` a stage path supplies a complete configuration bundle from any stage reference—a Git
  repository stage (`@my_git_repo/...`), another connector’s stage in the same account
  (`snow://openflow_connector/...`), or another internal stage. The catalog definition is named
  inside `config.json` as `connectorDefinitionId`—there is no `FROM DEFINITION` clause in the
  `CREATE` command.

When you use `FROM` with a stage path, Openflow reads `connectorDefinitionId` from `config.json`
to determine the connector type—you do not use `FROM DEFINITION` in `CREATE`. The stage holds only
instance configuration: `config.json`, asset files (such as JDBC drivers), and metadata. Snowflake
supplies the catalog connector package at create time; you do not copy it onto the stage.

Before you run `CREATE`, update connection URLs, secret references, and destination settings for
the target runtime.

### Initial state difference

| Created via | Initial state |
| --- | --- |
| UI or SQL `FROM DEFINITION` | Live version exists; no default (**Draft**). Commit before starting. |
| Stage `FROM '@<stage>[/path/]'` or `snow://...` | Default version exists; no live version. Ready to start immediately (no **COMMIT** step). |

Expand

Show lessSee more

### Workflow

1. Create and configure a connector with the wizard or `FROM DEFINITION`. Commit the configuration
   when it works in your source environment.
2. Register a Git repository in Snowflake if you do not already have one. See
   [Using a Git repository in Snowflake](/developer-guide/git/git-overview).
3. Export the connector configuration:

   Copy code

   ```
   ALTER OPENFLOW CONNECTOR my_db.my_schema.my_connector PUSH TO
     '@my_git_repo/branches/main/connectors/my_connector'
     USERNAME = 'my-git-username'
     PASSWORD = 'my-git-token'
     NAME = 'My Name'
     EMAIL = 'my.email@example.com'
     COMMENT = 'Export connector config';
   ```
4. Review and update `config.json` in the repository for the target environment (secrets, URLs,
   destination settings).
5. Create the new connector from the stage path:

   Copy code

   ```
   CREATE OPENFLOW CONNECTOR my_db.my_schema.my_connector_prod
     IN RUNTIME my_db.my_schema.my_prod_runtime
     FROM '@my_git_repo/branches/main/connectors/my_connector/'
     COMMENT = 'Created from validated stage config';
   ```

   You can also use a `snow://openflow_connector/.../versions/LAST/` URI to clone a connector in
   the same account without Git—for example,
   `'snow://openflow_connector/my_db.my_schema.my_connector/versions/LAST/'`.

For `CREATE`, `ADD VERSION FROM`, `PUSH`, and `PULL` syntax, see [CREATE OPENFLOW CONNECTOR](/sql-reference/sql/create-openflow-connector) and [ALTER OPENFLOW CONNECTOR](/sql-reference/sql/alter-openflow-connector).

## Secrets in configuration

Sensitive values (for example, database passwords) should reference
[Snowflake secrets](/sql-reference/sql/create-secret) rather than plain text in
`config.json`. See [Secrets in configuration](/user-guide/data-integration/openflow/gen2/configure-connector-sql#label-openflow-configure-connector-sql-secrets) in [Configure a gen 2 connector with SQL](/user-guide/data-integration/openflow/gen2/configure-connector-sql).

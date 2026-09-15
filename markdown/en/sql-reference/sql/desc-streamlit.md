# DESCRIBE STREAMLIT

Describes the columns in a Streamlit object.

DESCRIBE can be abbreviated to DESC.

See also:
:   [CREATE STREAMLIT](/sql-reference/sql/create-streamlit), [SHOW STREAMLITS](/sql-reference/sql/show-streamlits), [ALTER STREAMLIT](/sql-reference/sql/alter-streamlit), [DROP STREAMLIT](/sql-reference/sql/drop-streamlit)

## Syntax

Copy code

```
DESC[RIBE] STREAMLIT <name>
```

## Required parameters

`name`
:   Specifies the identifier for the Streamlit object to describe. If the identifier contains spaces or special
    characters, the entire string must be enclosed in double quotes. Identifiers enclosed in double quotes are also
    case-sensitive.

## Access control requirements

If your role does not own the objects in the following table, then your role
must have the listed
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) on those objects:

| Privilege | Object |
| --- | --- |
| USAGE | Streamlit object that you describe |

Expand

Show lessSee more

Operating on an object in a schema requires at least one privilege on the parent database and at least one privilege on the parent schema.

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Usage notes

- To post-process the output of this command, you can use the [pipe operator](/sql-reference/operators-flow)
  (`->>`) or the [RESULT\_SCAN](/sql-reference/functions/result_scan) function. Both constructs treat the output as a
  result set that you can query.

  For example, you can use the pipe operator or RESULT\_SCAN function to select specific columns from the SHOW
  command output or filter the rows.

  When you refer to the output columns, use [double-quoted identifiers](/sql-reference/identifiers-syntax#label-delimited-identifier) for
  the column names. For example, to select the output column `type`, specify `SELECT "type"`.

  You must use double-quoted identifiers because the output column names for SHOW commands are in lowercase.
  The double quotes ensure that the column names in the SELECT list or WHERE clause match the column names
  in the SHOW command output that was scanned.

## Output

The command output provides information about a Streamlit object in the following columns:

| Column | Description |
| --- | --- |
| `title` | Title of the Streamlit object that displays in Snowsight. |
| `main_file` | Name of the Streamlit app’s entrypoint file. |
| `query_warehouse` | Warehouse where queries issued by the Streamlit app are run. |
| `runtime_name` | Runtime environment for the Streamlit app, like `SYSTEM$WAREHOUSE_RUNTIME` or `SYSTEM$ST_CONTAINER_RUNTIME_PY3_11`. |
| `compute_pool` | Compute pool where the Streamlit app runs. This is only used for container runtimes and ignored for warehouse runtimes. |
| `url_id` | Unique ID associated with the Streamlit object. |
| `default_packages` | Default Python packages for the Streamlit application. |
| `user_packages` | Python packages that the user specified in the `environment.yml` file. This is empty if there is no `environment.yml` file and doesn’t apply to container runtimes. |
| `import_urls` | List of URLs that the Streamlit app imports. This doesn’t apply to container runtimes. |
| `external_access_integrations` | List of external access integrations associated with the Streamlit object. |
| `external_access_secrets` | List of external access secrets associated with the Streamlit object. |
| `name` | Unique name of the Streamlit object within its schema. |
| `comment` | Comment associated with the Streamlit object. |
| `default_version` | Default version of the Streamlit object to use when there is no live version. If your app doesn’t already have a live version and the owner opens the app on Snowsight, this is the version that is copied to the live version. |
| `default_version_name` | Name of the default version directory within the Streamlit object’s file system. |
| `default_version_alias` | Unsupported and always null. |
| `default_version_location_uri` | Location URI of the default version’s app files. This is read only. |
| `default_version_source_location_uri` | Location URI of the default version’s source files in its Git object. If the Streamlit object is not connected to a Git object, this is null. |
| `default_version_git_commit_hash` | Git commit hash of the default version of the Streamlit object. If the Streamlit object is not connected to a Git object, this is null. |
| `last_version_name` | Name of the last version directory within the Streamlit object’s file system. |
| `last_version_alias` | Unsupported and always null. |
| `last_version_location_uri` | Location URI of the last version’s app files. This is read only. |
| `last_version_source_location_uri` | Location URI of the last version’s source files in its Git object. If the Streamlit object is not connected to a Git object, this is null. |
| `last_version_git_commit_hash` | Git commit hash of the last version of the Streamlit object. If the Streamlit object is not connected to a Git object, this is null. |
| `live_version_location_uri` | Location URI of the live version of the Streamlit object. This location is readable and writable. Edits in Snowsight are saved in this location. You can remotely update a live app by copying files to this location. |

Expand

Show lessSee more

For Streamlit objects created using the `ROOT_LOCATION` parameter, the command output provides information in the following columns:

| Column | Description |
| --- | --- |
| `name` | Unique name of the Streamlit object within its schema. |
| `title` | Title of the Streamlit object that displays in Snowsight. |
| `root_location` | Location of the Streamlit object’s files. |
| `main_file` | Path to the Streamlit app’s entrypoint file, relative to the root location. |
| `query_warehouse` | Warehouse where queries issued by the Streamlit app are run. |
| `url_id` | Unique ID associated with the Streamlit object. |
| `default_packages` | Default Python packages for the Streamlit app. |
| `user_packages` | Python packages that the user specified in the `environment.yml` file. This is empty if there is no `environment.yml` file. |
| `import_urls` | List of URLs that the Streamlit app imports. |
| `external_access_integrations` | List of external access integrations associated with the Streamlit object. |
| `external_access_secrets` | List of external access secrets associated with the Streamlit object. |

Expand

Show lessSee more

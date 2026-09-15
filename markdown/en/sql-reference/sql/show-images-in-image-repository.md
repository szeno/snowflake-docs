# SHOW IMAGES IN IMAGE REPOSITORY

Feature — Generally Available

Snowpark Container Services is available to accounts in [AWS, Microsoft Azure, and Google Cloud Platform commercial regions](/user-guide/intro-regions#label-na-general-regions), with some exceptions. For more information, see [Available regions and considerations](/developer-guide/snowpark-container-services/overview#label-snowpark-containers-overview-available-regions).

Lists the images in an [image repository](/developer-guide/snowpark-container-services/working-with-registry-repository).

See also:
:   [CREATE IMAGE REPOSITORY](/sql-reference/sql/create-image-repository), [DROP IMAGE REPOSITORY](/sql-reference/sql/drop-image-repository),
    [SHOW IMAGE REPOSITORIES](/sql-reference/sql/show-image-repositories)

## Syntax

Copy code

```
SHOW IMAGES IN IMAGE REPOSITORY <name>
```

## Parameters

`name`
:   Name of the image repository.

## Access control requirements

A [role](/user-guide/security-access-control-overview#label-access-control-overview-roles) used to execute this operation must have the following
[privileges](/user-guide/security-access-control-overview#label-access-control-overview-privileges) at a minimum:

| Privilege | Object | Notes |
| --- | --- | --- |
| READ | Image repository |  |

Expand

Show lessSee more

For instructions on creating a custom role with a specified set of privileges, see [Creating custom roles](/user-guide/security-access-control-configure#label-security-custom-role).

For general information about roles and privilege grants for performing SQL actions on
[securable objects](/user-guide/security-access-control-overview#label-access-control-securable-objects), see [Overview of Access Control](/user-guide/security-access-control-overview).

## Output

The command output provides the following columns:

| Column | Description |
| --- | --- |
| `created_on` | Date and time when the image was uploaded to the image repository. |
| `image_name` | Image name |
| `tags` | Image tags |
| `digest` | SHA256 digest of the image |
| `image_path` | Image path (`database_name/schema_name/repository_name/image_name:image_tag`) |

Expand

Show lessSee more

## Usage notes

- The command doesn’t require a running warehouse to execute.
- The command only returns objects for which the current user’s current role has been granted at least one access privilege.
- The MANAGE GRANTS access privilege implicitly allows its holder to see every object in the account. By default, only the account
  administrator (users with the ACCOUNTADMIN role) and security administrator (users with the SECURITYADMIN role) have the
  MANAGE GRANTS privilege.

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

## Examples

List the images in the `tutorial_repository` image repository.

Copy code

```
SHOW IMAGES IN IMAGE REPOSITORY tutorial_db.data_schema.tutorial_repository;
```

```
+-------------------------------+-----------------------+--------+-------------------------------------------------------------------------+--------------------------------------------------------------------------+
| created_on                    | image_name            | tags   | digest                                                                  | image_path                                                               |
|-------------------------------+-----------------------+--------+-------------------------------------------------------------------------+--------------------------------------------------------------------------|
| 2024-04-18 13:51:35.000 -0700 | my_echo_service_image | latest | sha256:70421668b2635b2996c6d5bc80627cf6d98c0716948b5f60d198d6411d4b4681 | tutorial_db/data_schema/tutorial_repository/my_echo_service_image:latest |
+-------------------------------+-----------------------+--------+-------------------------------------------------------------------------+--------------------------------------------------------------------------+
```

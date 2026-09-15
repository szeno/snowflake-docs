# Data loading / unloading DDL

Stages and file formats are named database objects that can be used to simplify and streamline bulk loading data into and unloading data out of database tables.

Pipes are named database objects that define COPY statements for loading micro-batches of data using Snowpipe.

## Stage management

Snowflake supports two types of stages for storing data files used for loading/unloading:

- Internal stages store the files internally within Snowflake.
- External stages store the files in an external location (i.e. S3 bucket) that is referenced by the stage. An external stage specifies location and credential information, if required, for the S3 bucket.

Both external and internal stages can include file format and copy options.

- [CREATE STAGE](/sql-reference/sql/create-stage)
- [CREATE STAGE … CLONE](/sql-reference/sql/create-clone)
- [ALTER STAGE](/sql-reference/sql/alter-stage)
- [DROP STAGE](/sql-reference/sql/drop-stage)
- [DESCRIBE STAGE](/sql-reference/sql/desc-stage)
- [SHOW STAGES](/sql-reference/sql/show-stages)

## File format management

A file format encapsulates information, such as file type (CSV, JSON, etc.) and formatting options specific to each type, for data files used for bulk loading/unloading.

- [CREATE FILE FORMAT](/sql-reference/sql/create-file-format)
- [CREATE FILE FORMAT … CLONE](/sql-reference/sql/create-clone)
- [ALTER FILE FORMAT](/sql-reference/sql/alter-file-format)
- [DROP FILE FORMAT](/sql-reference/sql/drop-file-format)
- [DESCRIBE FILE FORMAT](/sql-reference/sql/desc-file-format)
- [SHOW FILE FORMATS](/sql-reference/sql/show-file-formats)

## Git repository management

A Snowflake [Git repository stage](/developer-guide/git/git-overview) represents a local Git repository in Snowflake.

- [CREATE GIT REPOSITORY](/sql-reference/sql/create-git-repository)
- [ALTER GIT REPOSITORY](/sql-reference/sql/alter-git-repository)
- [DROP GIT REPOSITORY](/sql-reference/sql/drop-git-repository)
- [DESCRIBE GIT REPOSITORY](/sql-reference/sql/desc-git-repository)
- [SHOW GIT BRANCHES](/sql-reference/sql/show-git-branches)
- [SHOW GIT REPOSITORIES](/sql-reference/sql/show-git-repositories)
- [SHOW GIT TAGS](/sql-reference/sql/show-git-tags)

## Pipe management

A pipe encapsulates a single COPY statement for loading a set of data files from an ingestion queue into a table.

- [CREATE PIPE](/sql-reference/sql/create-pipe)
- [ALTER PIPE](/sql-reference/sql/alter-pipe)
- [DROP PIPE](/sql-reference/sql/drop-pipe)
- [DESCRIBE PIPE](/sql-reference/sql/desc-pipe)
- [SHOW PIPES](/sql-reference/sql/show-pipes)

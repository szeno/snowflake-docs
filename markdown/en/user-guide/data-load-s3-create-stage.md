# Create an S3 stage

An external (that is, Amazon S3) stage specifies where data files are stored so that the data in the files can be loaded into a table.

Data can be loaded directly from files in a specified S3 bucket, with or without a folder path (or prefix, in S3 terminology). If the path ends with `/`, all of the objects in the corresponding S3 folder are loaded.

Note

In the [previous step](/user-guide/data-load-s3-config), if you followed the instructions to configure an AWS IAM role with the required policies and permissions
to access your external S3 bucket, you have already created an S3 stage. You can skip this step and continue to [Copying data from an S3 stage](/user-guide/data-load-s3-copy).

## External stages

In addition to loading directly from files in S3 buckets, Snowflake supports creating named external stages, which encapsulate all of the required information for staging files, including:

- The S3 bucket where the files are staged.
- The named storage integration object or S3 credentials for the bucket (if it is protected).
- An encryption key (if the files in the bucket have been encrypted).

Named external stages are optional, but recommended when you plan to load data regularly from the same location.

Note

Snowflake uses multipart uploads when uploading to Amazon S3 and Google Cloud Storage.
This process might leave incomplete uploads in the storage location for your external stage.

To prevent incomplete uploads from accumulating, we recommend that you set a lifecycle rule.
For instructions, see the [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpu-abort-incomplete-mpu-lifecycle-config.html)
or [Google Cloud Storage](https://cloud.google.com/storage/docs/lifecycle#abort-mpu) documentation.

## Create an external stage

You can create a named external stage using SQL or the web interface.

Note

To create a stage, you must use a role that is granted or inherits the necessary privileges.
For more information, see [Access control requirements](/sql-reference/sql/create-stage#label-create-stage-privileges) for [CREATE STAGE](/sql-reference/sql/create-stage).

### Create an external stage using SQL

Use the [CREATE STAGE](/sql-reference/sql/create-stage) command to create an external stage using SQL.

The following example uses SQL to create an external stage named `my_s3_stage` that references a private/protected S3 bucket
named `mybucket` with a folder path named `encrypted_files/`. The CREATE statement includes the `s3_int` storage integration
that was created in [Option 1: Configure a Snowflake storage integration to access Amazon S3](/user-guide/data-load-s3-config-storage-integration) to access the S3 bucket. The stage references a named file
format object named `my_csv_format`, which describes the data in the files stored in the bucket path:

> Copy code
>
> ```
> CREATE STAGE my_s3_stage
>   STORAGE_INTEGRATION = s3_int
>   URL = 's3://mybucket/encrypted_files/'
>   FILE_FORMAT = my_csv_format;
> ```

Note

By specifying a named file format object (or individual file format options) for the stage, it is not necessary to later specify the same file format options in the COPY command used to load data from the stage.

### Create an external stage using Python

Use the [StageCollection.create](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.stage.StageCollection#snowflake.core.stage.StageCollection.create)
method of the [Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview) to create an external stage.

Similar to the preceding SQL example, the following Python example creates an external stage named `my_s3_stage` that references an S3
bucket named `mybucket` with a folder path named `encrypted_files/`:

Copy code

```
from snowflake.core.stage import Stage

my_stage = Stage(
  name="my_s3_stage",
  storage_integration="s3_int",
  url="s3://mybucket/encrypted_files/"
)
root.databases["<database>"].schemas["<schema>"].stages.create(my_stage)
```

Note

The Python API currently does not support the FILE\_FORMAT parameter of the [CREATE STAGE](/sql-reference/sql/create-stage) SQL command.

### Create an external stage using Snowsight

To use Snowsight to create a named external stage, do the following:

1. sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. at the top of the navigation menu, select [![Add a dashboard tile](/static/images/snowsight/snowsight-dashboards-add-tile-icon.png)](/static/images/snowsight/snowsight-dashboards-add-tile-icon.png) (**Create**) » **Stage** » **External Stage**.
3. Select your external cloud storage provider: **Amazon S3**, **Microsoft Azure**, or **Google Cloud Platform**.
4. In the **Create Stage** dialog, enter a **Stage Name**.
5. Select the database and schema where you want to create the stage.
6. Enter the **URL** of your external cloud storage location.
7. If your external storage isn’t public, enable **Authentication** and enter your details. For more information,
   see [CREATE STAGE](/sql-reference/sql/create-stage).
8. Optionally deselect **Directory table**. Directory tables let you see files on the stage,
   but require a warehouse and thus incur a cost. You can choose to deselect this option for now and enable a directory table later.

   > If you enable **Directory table**, optionally select **Enable auto-refresh**, and then select your event notification or
   > notification integration to automatically refresh the directory table when files are added or removed.
   > For more information, see [Data Load Dirtables Auto](data-load-dirtables-auto).
9. If your files are encrypted, enable **Encryption**, and then enter your details.
10. (Optional) To view a generated SQL statement, expand the **SQL Preview**.
    To specify additional options for your stage, such as AUTO\_REFRESH, you can open this SQL preview in a worksheet.
11. Select **Create**.

**Next:** [Copying data from an S3 stage](/user-guide/data-load-s3-copy)

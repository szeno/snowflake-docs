# Create an Azure stage

A stage specifies where data files are stored (that is, “staged”) so that the data in the files can be loaded into a table.

Data can be loaded directly from files in a specified Azure container or in an Azure “folder” path (i.e. key value prefix). If the path ends with `/`, all of the objects in the corresponding Azure folder are loaded.

## External stages

In addition to loading directly from files in Azure containers, Snowflake supports creating named external stages, which encapsulate all of the required information for staging files, including:

- The Azure container where the files are staged.
- The named storage integration object or Azure credentials for the container (if it is protected).
- An encryption key (if the files in the container have been encrypted).

Named external stages are optional, but recommended when you plan to load data regularly from the same location. For instructions for creating an external stage, see [Create an external stage](#create-an-external-stage) below.

Note

To improve query performance for an Azure external stage, configure your network routing to use
[Microsoft network routing](https://learn.microsoft.com/en-us/azure/storage/common/network-routing-preference#microsoft-global-network-versus-internet-routing).
For instructions, see the [Azure documentation](https://learn.microsoft.com/en-us/azure/storage/common/configure-network-routing-preference?tabs=azure-portal).

## Create an external stage

You can create a named external stage using SQL or the web interface.

Note

To create a stage, you must use a role that is granted or inherits the necessary privileges.
For more information, see [Access control requirements](/sql-reference/sql/create-stage#label-create-stage-privileges) for [CREATE STAGE](/sql-reference/sql/create-stage).

### Create an external stage using SQL

Use the [CREATE STAGE](/sql-reference/sql/create-stage) command to create an external stage.

The following example creates an external stage named `my_azure_stage`. The CREATE statement includes the `azure_int` storage
integration that was created in [Configure an Azure container for loading data](/user-guide/data-load-azure-config) to access the Azure container `container1` in the `myaccount`
account.

The data files are stored in the `load/files/` path. The stage references a named file format object named `my_csv_format`, which
describes the data in the files stored in the path:

Copy code

```
CREATE STAGE my_azure_stage
  STORAGE_INTEGRATION = azure_int
  URL = 'azure://myaccount.blob.core.windows.net/mycontainer/load/files/'
  FILE_FORMAT = my_csv_format;
```

Note

Use the `blob.core.windows.net` endpoint for all supported types of Azure blob storage accounts, including Data Lake Storage Gen2.

Note

By specifying a named file format object (or individual file format options) for the stage, it is not necessary to later specify the same file format options in the COPY command used to load data from
the stage. For more information about file format objects and options, see [CREATE FILE FORMAT](/sql-reference/sql/create-file-format).

### Create an external stage using Python

Use the [StageCollection.create](/developer-guide/snowflake-python-api/reference/latest/_autosummary/snowflake.core.stage.StageCollection#snowflake.core.stage.StageCollection.create)
method of the [Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-overview) to create an external stage.

Similar to the preceding SQL example, the following Python example creates an external stage named `my_azure_stage`:

Copy code

```
from snowflake.core.stage import Stage

my_stage = Stage(
  name="my_azure_stage",
  storage_integration="azure_int",
  url="azure://myaccount.blob.core.windows.net/mycontainer/load/files/"
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

**Next:** [Copy data from an Azure stage](/user-guide/data-load-azure-copy)

# Managing data loading and unloading resources with Python

You can use Python to manage data loading and unloading resources in Snowflake, including external volumes, pipes, and stages.

## Prerequisites

The examples in this topic assume that you’ve added code to connect with Snowflake and to create a `Root` object from which to use the
Snowflake Python APIs.

For example, the following code uses connection parameters defined in a configuration file to create a connection to Snowflake:

Copy code

```
from snowflake.core import Root
from snowflake.snowpark import Session

session = Session.builder.config("connection_name", "myconnection").create()
root = Root(session)
```

Using the resulting `Session` object, the code creates a `Root` object to use the API’s types and methods. For more information,
see [Connect to Snowflake with the Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-connecting-snowflake).

## Managing stages

You can manage Snowflake stages, which are locations of data files in cloud storage. For an overview of stages, see
[Overview of data loading](/user-guide/data-load-overview).

The Snowflake Python APIs represents stages with two separate types:

- `Stage`: Exposes a stage’s properties such as its name, encryption type, credentials, and directory table settings.
- `StageResource`: Exposes methods you can use to fetch a corresponding `Stage` object, upload and list files on the stage, and
  drop the stage.

### Creating a stage

To create a stage, first create a `Stage` object, and then create a `StageCollection` object from the API `Root`
object. Using `StageCollection.create`, add the new stage to Snowflake.

Code in the following example creates a `Stage` object that represents a stage named `my_stage` with an encryption type of
`SNOWFLAKE_SSE` (server-side encryption only):

Copy code

```
from snowflake.core.stage import Stage, StageEncryption

my_stage = Stage(
  name="my_stage",
  encryption=StageEncryption(type="SNOWFLAKE_SSE")
)
stages = root.databases["my_db"].schemas["my_schema"].stages
stages.create(my_stage)
```

The code creates a `StageCollection` variable `stages` and uses `StageCollection.create` to create a new stage in Snowflake.

### Getting stage details

You can get information about a stage by calling the `StageResource.fetch` method, which returns a `Stage` object.

Code in the following example gets information about a stage named `my_stage`:

Copy code

```
my_stage = root.databases["my_db"].schemas["my_schema"].stages["my_stage"].fetch()
print(my_stage.to_dict())
```

### Listing stages

You can list stages using the `StageCollection.iter` method, which returns a `PagedIter` iterator of `Stage` objects.

Code in the following example lists stages whose name includes the text `my` and prints the name of each:

Copy code

```
from snowflake.core.stage import StageCollection

stages: StageCollection = root.databases["my_db"].schemas["my_schema"].stages
stage_iter = stages.iter(like="my%")  # returns a PagedIter[Stage]
for stage_obj in stage_iter:
  print(stage_obj.name)
```

### Performing stage operations

You can perform common stage operations—such as uploading a file to a stage and listing files on a stage—with a `StageResource`
object.

To demonstrate some operations you can do with a stage resource, code in the following example does the following:

1. Uploads a file named `my-file.yaml` to the `my_stage` stage with the specified auto-compress and overwrite options.
2. Lists all files on the stage to verify that the file was uploaded successfully.
3. Drops the stage.

Copy code

```
my_stage_res = root.databases["my_db"].schemas["my_schema"].stages["my_stage"]

my_stage_res.put("./my-file.yaml", "/", auto_compress=False, overwrite=True)

stageFiles = root.databases["my_db"].schemas["my_schema"].stages["my_stage"].list_files()
for stageFile in stageFiles:
  print(stageFile)

my_stage_res.drop()
```

## Managing pipes

You can manage Snowflake pipes, which are named, first-class Snowflake objects that contain a COPY INTO statement used by Snowpipe to load
data from an ingestion queue into tables. For an overview of pipes, see [Snowpipe](/user-guide/data-load-snowpipe-intro).

The Snowflake Python APIs represents pipes with two separate types:

- `Pipe`: Exposes a pipe’s properties such as its name and the COPY INTO statement to be used by Snowpipe.
- `PipeResource`: Exposes methods you can use to fetch a corresponding `Pipe` object, refresh the pipe with staged data files,
  and drop the pipe.

### Creating a pipe

To create a pipe, first create a `Pipe` object, and then create a `PipeCollection` object from the API `Root`
object. Using `PipeCollection.create`, add the new pipe to Snowflake.

Code in the following example creates a `Pipe` object that represents a pipe named `my_pipe` with the specified COPY INTO
statement:

Copy code

```
from snowflake.core.pipe import Pipe

my_pipe = Pipe(
  name="my_pipe",
  comment="creating my pipe",
  copy_statement="COPY INTO my_table FROM @mystage FILE_FORMAT = (TYPE = 'JSON')",
)

pipes = root.databases["my_db"].schemas["my_schema"].pipes
pipes.create(my_pipe)
```

The code creates a `PipeCollection` variable `pipes` and uses `PipeCollection.create` to create a new pipe in Snowflake.

### Getting pipe details

You can get information about a pipe by calling the `PipeResource.fetch` method, which returns a `Pipe` object.

Code in the following example gets information about a pipe named `my_pipe`:

Copy code

```
my_pipe = root.databases["my_db"].schemas["my_schema"].pipes["my_pipe"].fetch()
print(my_pipe.to_dict())
```

### Listing pipes

You can list pipes using the `PipeCollection.iter` method, which returns a `PagedIter` iterator of `Pipe` objects.

Code in the following example lists pipes whose name starts with `my` and prints the name of each:

Copy code

```
from snowflake.core.pipe import PipeCollection

pipes: PipeCollection = root.databases["my_db"].schemas["my_schema"].pipes
pipe_iter = pipes.iter(like="my%")  # returns a PagedIter[Pipe]
for pipe_obj in pipe_iter:
  print(pipe_obj.name)
```

### Performing pipe operations

You can perform common pipe operations—such as refreshing a pipe and dropping a pipe—with a `PipeResource` object.

Note

Only the REFRESH functionality of [ALTER PIPE](/sql-reference/sql/alter-pipe) is currently supported.

To demonstrate operations you can do with a pipe resource, code in the following example does the following:

1. Gets the `my_pipe` pipe resource object.
2. Refreshes the pipe with staged data files with the specified, optional prefix (or path).
3. Drops the pipe.

Copy code

```
my_pipe_res = root.databases["my_db"].schemas["my_schema"].pipes["my_pipe"]

# equivalent to: ALTER PIPE my_pipe REFRESH PREFIX = 'dir3/'
my_pipe_res.refresh(prefix="dir3/")

my_pipe_res.drop()
```

## Managing external volumes

You can manage external volumes, which are named, account-level Snowflake objects that you use to connect Snowflake to your external cloud
storage for Apache Iceberg™ tables. For more information, see the [External volume](/user-guide/tables-iceberg#label-tables-iceberg-external-volume-def) section of
[Apache Iceberg™ tables](/user-guide/tables-iceberg).

The Snowflake Python APIs represents external volumes with two separate types:

- `ExternalVolume`: Exposes an external volume’s properties, such as its name and storage locations.
- `ExternalVolumeResource`: Exposes methods you can use to fetch a corresponding `ExternalVolume` object and drop or restore
  the external volume.

### Creating an external volume

To create an external volume, first create an `ExternalVolume` object, and then create an `ExternalVolumeCollection` object
from the API `Root` object. Using `ExternalVolumeCollection.create`, add the new external volume to Snowflake.

Code in the following example creates an `ExternalVolume` object that represents an external volume named `my_external_volume`
with the specified AWS S3 storage locations:

Copy code

```
from snowflake.core.external_volume import (
    ExternalVolume,
    StorageLocationS3,
)

my_external_volume = ExternalVolume(
    name="my_external_volume",
    storage_locations=[
        StorageLocationS3(
            name="my-s3-us-west-1",
            storage_base_url="s3://MY_EXAMPLE_BUCKET/",
            storage_aws_role_arn="arn:aws:iam::123456789012:role/myrole",
            encryption=Encryption(type="AWS_SSE_KMS", kms_key_id="1234abcd-12ab-34cd-56ef-1234567890ab"),
        ),
        StorageLocationS3(
            name="my-s3-us-west-2",
            storage_base_url="s3://MY_EXAMPLE_BUCKET/",
            storage_aws_role_arn="arn:aws:iam::123456789012:role/myrole",
            encryption=Encryption(type="AWS_SSE_KMS", kms_key_id="1234abcd-12ab-34cd-56ef-1234567890ab"),
        ),
    ]
)

root.external_volumes.create(my_external_volume)
```

### Getting external volume details

You can get information about an external volume by calling the `ExternalVolumeResource.fetch` method, which returns an
`ExternalVolume` object.

Code in the following example gets information about an external volume named `my_external_volume`:

Copy code

```
my_external_volume = root.external_volumes["my_external_volume"].fetch()
print(my_external_volume.to_dict())
```

### Listing external volumes

You can list external volumes using the `ExternalVolumeCollection.iter` method, which returns a `PagedIter` iterator of
`ExternalVolume` objects.

Code in the following example lists external volumes whose name starts with `my` and prints the name of each:

Copy code

```
external_volume_iter = root.external_volumes.iter(like="my%")
for external_volume_obj in external_volume_iter:
  print(external_volume_obj.name)
```

### Performing external volume operations

You can perform common external volume operations—such as dropping and restoring an external volume—with an
`ExternalVolumeResource` object.

To demonstrate operations you can do with an external volume resource, code in the following example does the following:

1. Gets the `my_external_volume` external volume resource object.
2. Drops the external volume.
3. Restores the most recent version of the dropped external volume.

Copy code

```
my_external_volume_res = root.external_volumes["my_external_volume"]
my_external_volume_res.drop()
my_external_volume_res.undrop()
```

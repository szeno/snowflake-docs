# Checkpoints in Databricks

Snowpark Checkpoints writes files about collected results and reads these same files to validate DataFrames. Some of these files are generated using PySpark; others using Python packages such as `os` or `glob`. This type of file handling behavior can lead to inconsistencies in a Databricks environment, where the file system differs from traditional environments. Therefore, you must adapt the package to ensure correct file reading and writing.

The following section demonstrates how to configure Snowpark Checkpoints to work seamlessly in a Databricks environment, thus enabling efficient DataFrame validation.

## Prerequisites

Before using Snowpark Checkpoints in Databricks, ensure that your environment meets the following requirements:

- *PySpark:* Version 3.5.0 or higher.
- *Python:* Version 3.9, 3.10 and 3.11

The Databricks Runtime versions that satisfy these requirements are:

- *Databricks Runtime 14.3 LTS*
- *Databricks Runtime 15.4 LTS*

## Input/output (I/O) strategies

To ensure that Snowpark Checkpoints works correctly across various environments, you can use the interface `EnvStrategy` and its implementation classes for file read and write operations. This allows I/O operations to be adaptable and customizable.

- With Snowpark Checkpoints, you can implement your own custom input/output methods by creating a class that implements the `EnvStrategy` interface. You can then tailor operations to your specific execution environment and expectations.
- Internally, the package uses a default class (`IODefaultStrategy`) that implements the `EnvStrategy` interface and provides a basic implementation of I/O operations. You can replace this default strategy with a custom implementation suited to your environment’s specific needs.

Important

Each Snowpark Checkpoints package (`snowpark-checkpoints-collectors`, `snowpark-checkpoints-validators`, `snowpark-checkpoints-hypothesis`) includes its own copy of the file handling classes. Therefore, any changes to file configurations must be applied to each package separately. Be sure to import the configuration from the package you are using.

## I/O functions

These file read and write methods can be customized:

- `mkdir`: Creates a folder.
- `folder_exists`: Checks whether a folder exists.
- `file_exists`: Checks whether a file exists.
- `write`: Writes content to a file.
- `read`: Reads content from a file.
- `read_bytes`: Reads binary content from a file.
- `ls`: Lists the contents of a directory.
- `getcwd`: Gets the current working directory.
- `remove_dir`: Removes a directory and its contents. This function is exclusively used in the `snowpark-checkpoints-collectors` module.
- `telemetry_path_files`: Gets the path to the telemetry files.

## Databricks strategy

The Databricks strategy is a configuration that knows how to work with DBFS file paths. It uses the `normalize_dbfs_path` function to ensure that all paths begin with `/dbfs/`.

## How to use it

To use the Databricks strategy, you must explicitly configure it in the code. Here’s how:

1. Import the necessary classes:

   Copy code

   ```
   from typing import Optional, BinaryIO
   from pathlib import Path
   from snowflake.snowpark_checkpoints_collector.io_utils import EnvStrategy, IODefaultStrategy
   from snowflake.snowpark_checkpoints_collector.io_utils.io_file_manager import get_io_file_manager
   ```
2. Define the Databricks strategy:

   Copy code

   ```
   class IODatabricksStrategy(EnvStrategy):

     def __init__(self):
      self.default_strategy = IODefaultStrategy()

     def mkdir(self, path: str, exist_ok: bool = False) -> None:
      path = normalize_dbfs_path(path)
      self.default_strategy.mkdir(path, exist_ok=exist_ok)

     def folder_exists(self, path: str) -> bool:
      path = normalize_dbfs_path(path)
      return self.default_strategy.folder_exists(path)

     def file_exists(self, path: str) -> bool:
      path = normalize_dbfs_path(path)
      return self.default_strategy.file_exists(path)

     def write(self, file_path: str, file_content: str, overwrite: bool = True) -> None:
      file_path = normalize_dbfs_path(file_path)
      self.default_strategy.write(file_path, file_content, overwrite=overwrite)

     def read(
      self, file_path: str, mode: str = "r", encoding: Optional[str] = None
     ) -> str:
      file_path = normalize_dbfs_path(file_path)
      return self.default_strategy.read(file_path, mode=mode, encoding=encoding)

     def read_bytes(self, file_path: str) -> bytes:
      file_path = normalize_dbfs_path(file_path)
      return self.default_strategy.read_bytes(file_path)

     def ls(self, path: str, recursive: bool = False) -> list[str]:
      file_path = normalize_dbfs_path(path)
      list_of_files = self.default_strategy.ls(file_path, recursive=recursive)
      return [content.replace("/dbfs","") for content in list_of_files]

     def getcwd(self) -> str:
      try:
          parent_folder = "/snowpark_checkpoints"
          self.mkdir(parent_folder, exist_ok=True)
          return parent_folder
      except Exception:
          return ""

     def remove_dir(self, path:str) -> None:
      path = normalize_dbfs_path(path)
      self.default_strategy.remove_dir(path)

     def telemetry_path_files(self, path:str) -> Path:
      path = normalize_dbfs_path(path)
      return self.default_strategy.telemetry_path_files(path)

   def normalize_dbfs_path(path: str) -> str:
    if isinstance(path, Path):
        path = str(path)
    if not path.startswith("/"):
        path = "/" + path
    if not path.startswith("/dbfs/"):
        path = f'/dbfs{path}'
    return path
   ```
3. Configure the Databricks strategy:

   Copy code

   ```
   get_io_file_manager().set_strategy(IODatabricksStrategy())
   ```

Executing this code at the start of your Databricks script or notebook configures Snowpark Checkpoints to use the defined I/O strategy for correct file handling in DBFS.

## Optional customization

For more specialized input/output operations, a custom strategy can be designed and implemented. This approach offers complete control and flexibility over the I/O behavior. It allows developers to tailor the strategy precisely to their specific requirements and constraints, potentially optimizing performance, resource utilization, or other relevant factors.

Important

When using custom strategies, it is your responsibility to ensure that I/O operations function correctly.

Categories:
:   [File functions](/sql-reference/functions-file)

# GET\_ABSOLUTE\_PATH

Retrieves the absolute path of a staged file using the stage name and path of the file relative to its location in the stage as inputs.

## Syntax

Copy code

```
GET_ABSOLUTE_PATH( @<stage_name> , '<relative_file_path>' )
```

## Arguments

`stage_name`
:   Name of the internal or external stage where the file is stored.

    Note

    If the stage name includes spaces or special characters, it must be enclosed in single quotes (e.g. `'@"my stage"'` for a stage
    named `"my stage"`).

`relative_file_path`
:   Path and filename of the file relative to its location in the stage.

## Returns

Absolute path of the file in cloud storage.

## Usage notes

- This SQL function returns a value for any role that has the following privilege on the stage:

  External stage:
  :   USAGE

  Internal stage:
  :   READ

- If files downloaded from an internal stage are corrupted, verify with the stage creator that `ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')` is set for the stage.

## Examples

Retrieve the absolute path of a bitmap format image file in an external stage:

Copy code

```
SELECT GET_ABSOLUTE_PATH(@images_stage, 'us/yosemite/half_dome.jpg');

+------------------------------------------------------------------------------------------+
| GET_ABSOLUTE_PATH(@IMAGES_STAGE, 'US/YOSEMITE/HALF_DOME.JPG')                            |
+------------------------------------------------------------------------------------------+
| s3://photos/national_parks/us/yosemite/half_dome.jpg                                     |
+------------------------------------------------------------------------------------------+
```

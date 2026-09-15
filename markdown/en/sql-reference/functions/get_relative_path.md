Categories:
:   [File functions](/sql-reference/functions-file)

# GET\_RELATIVE\_PATH

Extracts the path of a staged file relative to its location in the stage using the stage name and absolute file path in cloud storage as inputs.

## Syntax

Copy code

```
GET_RELATIVE_PATH( @<stage_name> , '<absolute_file_path>' )
```

## Arguments

`stage_name`
:   Name of the internal or external stage where the file is stored.

    Note

    If the stage name includes spaces or special characters, it must be enclosed in single quotes (e.g. `'@"my stage"'` for a stage
    named `"my stage"`).

`absolute_file_path`
:   Stage location, including the path and filename, of the file in cloud storage.

## Returns

Path of the file relative to the stage location.

## Usage notes

- This SQL function returns a value for any role that has the following privilege on the stage:

  External stage:
  :   USAGE

  Internal stage:
  :   READ

- If files downloaded from an internal stage are corrupted, verify with the stage creator that `ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')` is set for the stage.

## Examples

Retrieve the relative path of a bitmap format image file in an external stage, where the `@images_stage` stage references the
`s3://photos/national_parks/` bucket and path:

Copy code

```
SELECT GET_RELATIVE_PATH(@images_stage, 's3://photos/national_parks/us/yosemite/half_dome.jpg');
+================================================================================---------------------+
| GET_RELATIVE_PATH(@IMAGES_STAGE, 'S3://PHOTOS/NATIONAL_PARKS/US/YOSEMITE/HALF_DOME.JPG')  |
+================================================================================---------------------+
| us/yosemite/half_dome.jpg                                                                 |
+================================================================================---------------------+
```

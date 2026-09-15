Categories:
:   [File functions](/sql-reference/functions-file)

# GET\_STAGE\_LOCATION

Retrieves the URL for an external or internal named stage using the stage name as the input.

## Syntax

Copy code

```
GET_STAGE_LOCATION( @<stage_name> )
```

## Arguments

`stage_name`
:   Name of an external or internal named stage.

    Note

    If the stage name includes spaces or special characters, it must be enclosed in single quotes (e.g. `'@"my stage"'` for a stage
    named `"my stage"`).

## Returns

URL of the cloud storage location in the stage definition.

## Usage notes

- This SQL function returns a value for any role that has the USAGE privilege on the stage.

- If files downloaded from an internal stage are corrupted, verify with the stage creator that `ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')` is set for the stage.

## Examples

Retrieve the URL for an external stage:

Copy code

```
CREATE STAGE images_stage URL = 's3://photos/national_parks/us/yosemite/';

SELECT GET_STAGE_LOCATION(@images_stage);

+----------------------------------------------------------+
| GET_STAGE_LOCATION(@IMAGES_STAGE)                        |
+----------------------------------------------------------+
| s3://photos/national_parks/us/yosemite/                  |
+----------------------------------------------------------+
```

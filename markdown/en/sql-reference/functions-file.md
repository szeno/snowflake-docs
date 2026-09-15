# File functions

File functions enable you to access files staged in cloud storage.

## List of functions

| Function Name | Notes |
| --- | --- |
| **Stages** |  |
| [GET\_STAGE\_LOCATION](/sql-reference/functions/get_stage_location) | Returns the URL for an external or internal named stage using the stage name as the input. |
| [GET\_RELATIVE\_PATH](/sql-reference/functions/get_relative_path) | Extracts the path of a staged file relative to its location in the stage using the stage name and absolute file path in cloud storage as inputs. |
| [GET\_ABSOLUTE\_PATH](/sql-reference/functions/get_absolute_path) | Returns the absolute path of a staged file using the stage name and path of the file relative to its location in the stage as inputs. |
| [GET\_PRESIGNED\_URL](/sql-reference/functions/get_presigned_url) | Generates the pre-signed URL to a staged file using the stage name and relative file path as inputs. Access files in an external stage using the function. |
| [BUILD\_SCOPED\_FILE\_URL](/sql-reference/functions/build_scoped_file_url) | Generates a scoped Snowflake file URL to a staged file using the stage name and relative file path as inputs. |
| [BUILD\_STAGE\_FILE\_URL](/sql-reference/functions/build_stage_file_url) | Generates a Snowflake file URL to a staged file using the stage name and relative file path as inputs. |
| **AI Functions** |  |
| [AI\_COMPLETE](/sql-reference/functions/ai_complete) | Generates a response (completion) from text or an image using a supported language model. |
| [AI\_PARSE\_DOCUMENT](/sql-reference/functions/ai_parse_document) | Returns the extracted content from a document on a Snowflake stage as a JSON-formatted string. |
| [AI\_TRANSCRIBE](/sql-reference/functions/ai_transcribe) | Transcribes text from an audio file with optional timestamps and speaker labels. |

Expand

Show lessSee more

The following functions are for use with the FILE data type. For more information, see [Unstructured data types](/sql-reference/data-types-unstructured).

| Sub-category | Function |
| --- | --- |
| Constructor | [TO\_FILE](/sql-reference/functions/to_file) |
|  | [TRY\_TO\_FILE](/sql-reference/functions/try_to_file) |
| Accessors | [FL\_GET\_CONTENT\_TYPE](/sql-reference/functions/fl_get_content_type) |
|  | [FL\_GET\_ETAG](/sql-reference/functions/fl_get_etag) |
|  | [FL\_GET\_FILE\_TYPE](/sql-reference/functions/fl_get_file_type) |
|  | [FL\_GET\_LAST\_MODIFIED](/sql-reference/functions/fl_get_last_modified) |
|  | [FL\_GET\_RELATIVE\_PATH](/sql-reference/functions/fl_get_relative_path) |
|  | [FL\_GET\_SCOPED\_FILE\_URL](/sql-reference/functions/fl_get_scoped_file_url) |
|  | [FL\_GET\_SIZE](/sql-reference/functions/fl_get_size) |
|  | [FL\_GET\_STAGE](/sql-reference/functions/fl_get_stage) |
|  | [FL\_GET\_STAGE\_FILE\_URL](/sql-reference/functions/fl_get_stage_file_url) |
| Utility Functions | [FL\_IS\_AUDIO](/sql-reference/functions/fl_is_audio) |
|  | [FL\_IS\_COMPRESSED](/sql-reference/functions/fl_is_compressed) |
|  | [FL\_IS\_DOCUMENT](/sql-reference/functions/fl_is_document) |
|  | [FL\_IS\_IMAGE](/sql-reference/functions/fl_is_image) |
|  | [FL\_IS\_VIDEO](/sql-reference/functions/fl_is_video) |

Expand

Show lessSee more

## Usage notes

- GET\_PRESIGNED\_URL and BUILD\_SCOPED\_FILE\_URL are non-deterministic functions; the others are deterministic.

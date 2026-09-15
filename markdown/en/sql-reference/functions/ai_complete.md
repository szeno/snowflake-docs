Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions) ,
    [File functions](/sql-reference/functions-file) (AI Functions)

# AI\_COMPLETE

Generates a response (completion) from text or an image using a supported language model. You can provide:

- A text prompt, to generate a response from the model. For more information, see [AI\_COMPLETE (Single string)](/sql-reference/functions/ai_complete-single-string).
- A single image and a text prompt, to generate a response based on the image and prompt. For more information, see [AI\_COMPLETE (Single image)](/sql-reference/functions/ai_complete-single-file).
- A prompt object that can support multiple images and text. For more information, see [AI\_COMPLETE (Prompt object)](/sql-reference/functions/ai_complete-prompt-object).

## Syntax

The syntax for the function depends on the type of input that you provide. For information about the syntax, see the following sections:

- [Single string arguments](/sql-reference/functions/ai_complete-single-string)
- [Single image arguments](/sql-reference/functions/ai_complete-single-file)
- [Prompt object arguments](/sql-reference/functions/ai_complete-prompt-object)

All syntax variations accept an optional `return_error_details` BOOLEAN argument as the final parameter.
When set to TRUE, the function returns an OBJECT that contains the value and the error message, one of which
is NULL depending on whether the function succeeded or failed. See [Error behavior](#error-behavior) for details.

## Error behavior

By default, if AI\_COMPLETE can’t process the input, the function returns NULL. If the query processes multiple rows,
rows with errors return NULL and don’t prevent the query from completing.

The return value on error depends on the `return_error_details`
argument. The following table shows the return value based on the `return_error_details` argument:

> | `return_error_details` | Return value | Description |
> | --- | --- | --- |
> | FALSE Not passed | NULL |  |
> | TRUE | OBJECT with `value` and `error` fields | `value`: The completion response (same type as the normal return value), or NULL if an error occurred. `error`: A VARCHAR value that contains the error message if an error occurred, or NULL if the function succeeded. |
>
> Expand
>
> Show lessSee more

For more information about error handling for AI functions, see [Snowflake Cortex AI Function: Multirow error handling improvements](/release-notes/bcr-bundles/2026_02/bcr-2184).

## Access control requirements

Users must use a role that has been granted the [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
See [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) for more information on this privilege.

Note

AI\_COMPLETE is the updated version of [COMPLETE](/sql-reference/functions/complete-snowflake-cortex).
For the latest functionality, use AI\_COMPLETE.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features) for legal notices.

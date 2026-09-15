Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# COMPLETE (SNOWFLAKE.CORTEX) (multimodal)

Notice

This page is provided for backward compatibility. For new use cases, start with
[AI\_COMPLETE](/sql-reference/functions/ai_complete), which is the canonical surface going forward.
This legacy function will be deprecated by the end of 2026.

Given an image and a prompt, generates a response (completion) using a language model. This function variant supports
image models along with text models, and processes images stored in an internal Snowflake stage or an external stage.
COMPLETE can be used to process a single image, multiple images in a batch fashion, applying the same or a different
prompt to each image, or multiple images in a single operation (for example, comparison).

## Syntax

Use one of the following:

Copy code

```
SNOWFLAKE.CORTEX.COMPLETE(
    '<model>', '<prompt>', <file_object>)
FROM <table>
```

Copy code

```
SNOWFLAKE.CORTEX.COMPLETE(
    '<model>', <prompt_object> )
FROM <table>
```

## Arguments

`model`
:   A string specifying the model to be used. See supported [models](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability).

    Supported models might have different costs and context windows.

`prompt`
:   A string containing a question about the image and optionally specifying an output format, such as JSON. Either
    this or the `prompt_object` argument is required.

`prompt_object`
:   A SQL OBJECT containing a string prompt with numbered placeholders (*{0}*, *{1}*, and so on) and one or more text or
    FILE values that are inserted into the prompt. The [PROMPT](/sql-reference/functions/prompt) function is a convenient way to create an object
    with the required layout. Either this argument or `prompt` is required.

`file_object`
:   A FILE object that contains an image file to be processed. Use the [TO\_FILE](/sql-reference/functions/to_file) function to
    create FILE objects from a stage path. Required when using a string prompt.

`FROM table`
:   An optional table containing image paths and an optional prompt for each image, allowing images to be batch-processed
    in a single call to COMPLETE.

## Returns

A string containing the language model’s response.

## Usage notes

- Inputs exceeding the context window limit result in an error. Output which would exceed the context window limit is truncated.
- To process multiple images, the prompt must be an object (typically created using the PROMPT function) that specifies a prompt
  template and the files to be processed.
- Only text and images are supported. Video and audio files are not supported.
- Images with filename extensions `.jpg`, `.jpeg`, `.png`, `.gif`, and `.webp` are supported. `pixtral-large` also supports `.bmp`.
- Maximum image size is 10 MB for `pixtral-large` and 3.75 MB for Claude models. Additionally, Claude models do not support images with a resolution greater than 8000x8000.
- The stage containing the images must have server-side encryption enabled. Client-side encrypted stages are not supported.
- The function does not support custom network policies.
- Stage names are not case-sensitive, but paths are.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features).

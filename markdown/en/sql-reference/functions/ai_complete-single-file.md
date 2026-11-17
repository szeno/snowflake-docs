Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AI\_COMPLETE (Single file)

Generates a response (completion) for a text prompt and a single file using a supported model. Depending on the model,
the file can be an image, a document, an audio file, or a video file. This overload accepts exactly one file per call.
To pass multiple files, or to combine files of different types, use
[AI\_COMPLETE (Prompt object)](/sql-reference/functions/ai_complete-prompt-object).

For limits by model and input type, see
[Model limitations](/user-guide/snowflake-cortex/ai-multimodal#model-limitations) and
[document limits](/user-guide/snowflake-cortex/ai-complete-document-intelligence#supported-models-and-limitations).

## Syntax

The function has three required arguments and one optional argument.
The function can be used with either positional or named argument syntax.

Using AI\_COMPLETE with a single file input:

Copy code

```
AI_COMPLETE(
    <model>, <predicate>, <file> [, <model_parameters> ] )
```

## Arguments

`model`
:   A string specifying the model to be used. The models you can use depend on the type of file.

    For image files, you can use one of the following models:

    - `claude-haiku-4-5`
    - `claude-opus-4-5`
    - `claude-opus-4-6`
    - `claude-opus-4-7`
    - `claude-opus-4-8`
    - `claude-opus-5`
    - `claude-sonnet-4-5`
    - `claude-sonnet-4-6`
    - `claude-sonnet-5`
    - `gemini-3.1-pro`
    - `gemini-3.7-flash`
    - `gemini-3.8-flash`
    - `gemini-4-argon`
    - `openai-gpt-5`
    - `openai-gpt-5-mini`
    - `openai-gpt-5-nano`
    - `openai-gpt-5.1`
    - `openai-gpt-5.2`
    - `openai-gpt-5.4`

    For document files, you can use one of the following models:

    - `claude-haiku-4-5`
    - `claude-opus-4-5`
    - `claude-opus-4-6`
    - `claude-opus-4-7`
    - `claude-opus-4-8`
    - `claude-opus-5`
    - `claude-sonnet-4-5`
    - `claude-sonnet-4-6`
    - `claude-sonnet-5`
    - `gemini-3.1-pro`
    - `gemini-3.7-flash`
    - `gemini-3.8-flash`
    - `gemini-4-argon`

    For audio and video files, you can use one of the following models:

    - `gemini-3.1-pro`
    - `gemini-3.7-flash`
    - `gemini-3.8-flash`
    - `gemini-4-argon`

    Supported models might have different [costs](/user-guide/snowflake-cortex/aisql-cost#label-cortex-llm-cost-considerations).

    Bring-your-own model: Open preview

    Alternatively, specify the name of a Snowpark Container Services model inference service that hosts your own text generation or vision-language model. Image inputs require a vision-language model. For supported file types, availability, prerequisites, and access requirements, see [Bring-your-own model for AI\_COMPLETE](/developer-guide/snowflake-ml/inference/spcs-ai-complete).

`predicate`
:   A string prompt.

`file`
:   A [FILE](/sql-reference/functions/to_file) object representing a single image, document, audio, or video file. The
    file type must be supported by the model that you specify; see the model lists for the *model* argument.

`model_parameters`
:   An [object](/sql-reference/data-types-semistructured#label-data-type-object) containing zero or more of the following options that affect the model’s
    hyperparameters. See [LLM Settings](https://www.promptingguide.ai/introduction/settings).

    - `temperature`: A value from 0 to 1 (inclusive) that controls the randomness of the output of the language model. A
      higher temperature (for example, 0.7) results in more diverse and random output, while a lower temperature (such as
      0.2) makes the output more deterministic and focused.

      Default: 0
    - `top_p`: A value from 0 to 1 (inclusive) that controls the randomness and diversity of the language model,
      generally used as an alternative to `temperature`. The difference is that `top_p` restricts the set of possible tokens
      that the model outputs, while `temperature` influences which tokens are chosen at each step.

      Default: 0
    - `max_tokens`: Sets the maximum number of output tokens in the response. Small values can result in truncated responses.

      Default: 4096
    - `guardrails`: Filters potentially unsafe and harmful responses from a language model using [Cortex Guard](/sql-reference/functions/ai_complete-single-string#label-cortex-llm-complete-cortex-guard).
      Either `TRUE` or `FALSE`. The default value is `FALSE`.

## Returns

Returns the string response from the language model.

## Examples

The following examples demonstrate the basic capabilities of the AI\_COMPLETE function with images. For audio and video
examples, see [Cortex AI Functions: Multimodal](/user-guide/snowflake-cortex/ai-multimodal).

### Visual question answering

A chart of inflation rates is used to answer a question about the data.

![Graph of inflation rates in 2023 with estimates for 2024](/static/images/cortex-llm/inflation-forecast.png)

Comparison between inflation rates in 2023 and in 2024 ([Statista](https://www.statista.com/))

Copy code

```
SELECT AI_COMPLETE('gemini-3.1-pro',
    'Which country will observe the largest inflation change in 2024 compared to 2023?',
    TO_FILE('@myimages', 'highest-inflation.png'));
```

Response:

```
Looking at the data, Venezuela will experience the largest change in inflation rates between 2023 and 2024.
The inflation rate in Venezuela is projected to decrease significantly from 337.46% in 2023 to 99.98% in 2024,
representing a reduction of approximately 237.48 percentage points. This is the most dramatic change among
all countries shown in the chart, even though Zimbabwe has higher absolute inflation rates.
```

### Entity extraction from an image

This example extracts the entities (objects) from an image and returns the results in JSON format.

![Photograph of kitchen after remodeling](/static/images/cortex-image/kitchen-remodel.png)

Copy code

```
SELECT AI_COMPLETE('claude-opus-4-6',
    'Extract the kitchen appliances identified in this image. Respond in JSON only with the identified appliances.',
    TO_FILE('@myimages', 'kitchen.png'));
```

Response:

```
{
    "appliances": [ "microwave","electric stove","oven","refrigerator" ]
}
```

## Usage notes

The following notes apply to Snowflake-hosted Cortex models. For models deployed on Snowpark Container Services, see [Usage notes for processing images](/developer-guide/snowflake-ml/inference/spcs-ai-complete#supported-file-types).

- This overload accepts exactly one file per call. To process multiple files in one call, use
  [AI\_COMPLETE (Prompt object)](/sql-reference/functions/ai_complete-prompt-object).
- The supported file types depend on the model. See the model lists for the *model* argument under
  [Arguments](#arguments).
- The stage containing the file must have server-side encryption enabled. Client-side encrypted stages are not supported.
- The function does not support custom network policies.
- Stage names are case-insensitive; paths are case-sensitive.

### Images

- Supported image formats:

  - `.jpg`
  - `.jpeg`
  - `.png`
  - `.gif`
  - `.webp`
  - `pixtral` and `llama4` models also support `.bmp`.
- The maximum image size is 10 MB for most models, and 3.75 MB for `claude` models. `claude` models do not support images with resolutions above 8000x8000.

### Documents

- All models listed for document files support these formats: `.txt`, `.md`, and `.pdf`. Claude models also support
  `.doc`, `.docx`, `.xls`, `.xlsx`, `.csv`, and `.xhtml`.
- Claude models have a maximum document size of 22 MB. Gemini models have a maximum document size of 37.5 MB.
- For context windows and page limits, see
  [Supported models and limitations](/user-guide/snowflake-cortex/ai-complete-document-intelligence#supported-models-and-limitations)
  in [AI\_COMPLETE with documents](/user-guide/snowflake-cortex/ai-complete-document-intelligence).

### Audio and video

- Only the Gemini models listed for audio and video files accept audio and video.
- Supported audio formats: `.wav`, `.mp3`, `.aiff`, `.aac`, `.ogg`, `.flac`, `.m4a`, `.mp4`, `.pcm`, and `.webm`.
- Supported video formats: `.mp4`, `.mpeg`, `.mov`, `.avi`, `.flv`, `.mpg`, `.webm`, `.wmv`, and `.3gpp`.
- The maximum file size is 100 MB. For context windows, see
  [Model limitations](/user-guide/snowflake-cortex/ai-multimodal#model-limitations).

Note

AI\_COMPLETE is the updated version of [COMPLETE](/sql-reference/functions/complete-snowflake-cortex).
For the latest functionality, use AI\_COMPLETE.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features) for legal notices.

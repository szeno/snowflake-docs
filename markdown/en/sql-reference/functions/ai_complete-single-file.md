Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# AI\_COMPLETE (Single image)

Generates a response (completion) for a text prompt using a supported language model. This variant of the function enhances AI\_COMPLETE with document understanding capabilities. The prompt can reference information or images found in a file containing a document. The function supports a single document input.

## Syntax

The function has three required arguments and one optional argument.
The function can be used with either positional or named argument syntax.

Using AI\_COMPLETE with a single image input:

Copy code

```
AI_COMPLETE(
    <model>, <predicate>, <file> [, <model_parameters> ] )
```

## Arguments

`model`
:   A string specifying the model to be used. Specify one of the following models:

    > - `claude-3-7-sonnet`
    > - `claude-4-opus`
    > - `claude-4-sonnet`
    > - `claude-haiku-4-5`
    > - `claude-opus-4-5`
    > - `claude-opus-4-6`
    > - `claude-opus-4-7`
    > - `claude-opus-4-8`
    > - `claude-opus-5`
    > - `claude-sonnet-4-5`
    > - `claude-sonnet-4-6`
    > - `claude-sonnet-5`
    > - `gemini-3.1-pro`
    > - `llama4-maverick`
    > - `llama4-scout`
    > - `openai-gpt-4.1`
    > - `openai-gpt-5`
    > - `openai-gpt-5-chat`
    > - `openai-gpt-5-mini`
    > - `openai-gpt-5-nano`
    > - `openai-gpt-5.1`
    > - `openai-gpt-5.2`
    > - `openai-gpt-5.4`
    > - `pixtral-large`

    Supported models might have different [costs](/user-guide/snowflake-cortex/aisql-cost#label-cortex-llm-cost-considerations).

`predicate`
:   A string prompt.

`file`
:   A FILE type object representing an image.

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

The following examples demonstrate the basic capabilities of the AI\_COMPLETE function with images.

### Visual question answering

A chart of inflation rates is used to answer a question about the data.

![Graph of inflation rates in 2023 with estimates for 2024](/static/images/cortex-llm/inflation-forecast.png)

Comparison between inflation rates in 2023 and in 2024 ([Statista](https://www.statista.com/))

Copy code

```
SELECT AI_COMPLETE('claude-sonnet-4-6',
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
SELECT AI_COMPLETE('claude-sonnet-4-6',
    'Extract the kitchen appliances identified in this image. Respond in JSON only with the identified appliances.',
    TO_FILE('@myimages', 'kitchen.png'));
```

Response:

```
{
    "appliances": [ "microwave","electric stove","oven","refrigerator" ]
}
```

## Usage notes for processing images

- Only text and images are supported. Video and audio files are not supported.
- Supported image formats:

  - `.jpg`
  - `.jpeg`
  - `.png`
  - `.gif`
  - `.webp`
  - `pixtral` and `llama4` models also support `.bmp`.
- The maximum image size is 10 MB for most models, and 3.75 MB for `claude` models. `claude` models do not support images with resolutions above 8000x8000.
- The stage containing the images must have server-side encryption enabled. Client-side encrypted stages are not supported.
- The function does not support custom network policies.
- Stage names are case-insensitive; paths are case-sensitive.

Note

AI\_COMPLETE is the updated version of [COMPLETE](/sql-reference/functions/complete-snowflake-cortex).
For the latest functionality, use AI\_COMPLETE.

## Legal notices

Refer to [Snowflake AI and ML](/guides-overview-ai-features) for legal notices.

Categories:
:   [String & binary functions](/sql-reference/functions-string) (AI Functions)

# COMPLETE (SNOWFLAKE.CORTEX)

Notice

This page is provided for backward compatibility. For new use cases, start with
[AI\_COMPLETE](/sql-reference/functions/ai_complete), which is the canonical surface going forward.
This legacy function will be deprecated by the end of 2026.

Given a prompt, generates a response (completion) using your choice of supported language model.

Note

A variant of this function allows COMPLETE to produce responses to images, including:

- Comparing images
- Captioning images
- Classifying images
- Extracting entities from images
- Answering questions using data in graphs and charts

See [COMPLETE (SNOWFLAKE.CORTEX) (multimodal)](/sql-reference/functions/complete-snowflake-cortex-multimodal) for more information.

## Syntax

Copy code

```
SNOWFLAKE.CORTEX.COMPLETE(
    <model>, <prompt_or_history> [ , <options> ] )
```

## Arguments

**Required:**

`model`
:   A string specifying the model to be used. See supported [models](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability).

    Supported models might have different [costs](/user-guide/snowflake-cortex/aisql-cost#label-cortex-llm-cost-considerations).

`prompt_or_history`
:   The prompt or conversation history to be used to generate a completion.

    If `options` is not present, the prompt given must be a string.

    If `options` is present, the argument must be an [array](/sql-reference/data-types-semistructured#label-data-type-array) of objects representing a
    conversation in chronological order. Each [object](/sql-reference/data-types-semistructured#label-data-type-object) must contain a `role` key and a
    `content` key. The `content` value is a prompt or a response, depending on the role. The role must be one of the
    following.

    | `role` value | `content` value |
    | --- | --- |
    | `'system'` | An initial plain-English prompt to the language model to provide it with background information and instructions for a response style. For example, “Respond in the style of a pirate.” The model does not generate a response to a system prompt. Only one system prompt may be provided, and if it is present, it must be the first in the array. |
    | `'user'` | A prompt provided by the user. Must follow the system prompt (if there is one) or an assistant response. |
    | `'assistant'` | A response previously provided by the language model. Must follow a user prompt. Past responses can be used to provide a stateful conversational experience; see [Usage notes](#usage-notes). |

    Expand

    Show lessSee more

**Optional:**

`options`
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
      Maximum allowed value: 8192
    - `guardrails`: Filters potentially unsafe and harmful responses from a language model using [Cortex Guard](/sql-reference/functions/ai_complete-single-string#label-cortex-llm-complete-cortex-guard).
      Either TRUE or FALSE.

      Default: FALSE
    - `response_format`: A [JSON schema](https://json-schema.org/) that the response should follow. This is a SQL
      sub-object, not a string. If `response_format` is not specified, the response is a string containing either the
      response or a serialized JSON object containing the response and information about it.

      For more information, see [AI\_COMPLETE (Structured outputs)](/sql-reference/functions/ai_complete-structured-outputs).

    Specifying the `options` argument, even if it is an empty object (`{}`), affects how the `prompt` argument is
    interpreted and how the response is formatted.

## Returns

When the `options` argument is not specified, returns a string containing the response.

When the `options` argument is given, and this object contains the `response_format` key, returns a string
representation of a JSON object adhering to the specified JSON schema.

When the `options` argument is given, and this object *does not* contain the `response_format` key, returns a
string representation of a JSON object containing the following keys.

- `"choices"`: An array of the model’s responses. (Currently, only one response is provided.) Each response is
  an object containing a `"messages"` key whose value is the model’s response to the latest prompt.
- `"created"`: UNIX timestamp (seconds since midnight, January 1, 1970) when the response was generated.
- `"model"`: The name of the model that created the response.
- `"usage"`: An object recording the number of tokens consumed and generated by this completion. Includes
  the following sub-keys:
  - `"completion_tokens"`: The number of tokens in the generated response.
  - `"prompt_tokens"`: The number of tokens in the prompt.
  - `"total_tokens"`: The total number of tokens consumed, which is the sum of the other two values.

## Access control requirements

Users must use a role that has been granted the [SNOWFLAKE.CORTEX\_USER database role](/sql-reference/snowflake-db-roles#label-snowflake-db-roles-cortex-user).
See [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges) for more information on this privilege.

## Usage notes

COMPLETE does not retain any state from one call to the next. To use the COMPLETE function to provide a stateful,
conversational experience, pass all previous user prompts and model responses in the conversation as part of the `prompt_or_history`
array (see [Templates for Chat Models](https://huggingface.co/docs/transformers/en/chat_templating#templates-for-chat-models)).
Keep in mind that the number of tokens processed increases for each “round,” and costs increase proportionally.

## Legal notices

The following notice applies to Cortex COMPLETE Structured Output functionality only:

Use of models provided on the [Snowflake Model and Service Flow-Down Terms](https://www.snowflake.com/en/legal/optional-offerings/offering-specific-terms/ai-features/open-source-model-flow-down-terms/)
page are subject to the terms specified therein. The data classification of inputs and outputs are as set forth in the following table.

| Input data classification | Output data classification | Designation |
| --- | --- | --- |
| Usage Data | Customer Data | Covered AI Feature |

Expand

Show lessSee more

For the rest of COMPLETE functionality, refer to [Snowflake AI and ML](/guides-overview-ai-features) for legal notices.

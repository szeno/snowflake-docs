# Cortex Agent ask user question tool

The Cortex Agent ask user question tool is a built-in tool that lets an agent pause mid-response to ask the user a structured multiple-choice question instead of guessing at an ambiguous request.

Unlike most agent tools, it executes entirely on the client. The service advertises the tool and emits the tool use, but does no work on the server, so an agent that asks a question can’t progress until your client answers it.

## How the ask user question tool works

The agent emits a tool use for `ask_user_question` containing one to four questions, then stops and waits. Your client:

1. Renders the questions, adding a free-text **Something else** choice to each one so the user isn’t confined to the listed options. The agent is instructed not to supply its own equivalent option, so don’t expect one.
2. Collects the user’s selection for each question.
3. Returns the selections as the tool result, continuing the conversation.

## Enabling the ask user question tool

You don’t usually enable this tool yourself: it’s injected automatically when you use [Deep Research](/user-guide/snowflake-cortex/snowflake-cowork#label-snowflake-cowork-deep-research) or [Profiles](/LIMITEDACCESS/snowflake-cortex/about-cowork-profiles), both of which need a way to come back to the user for a decision. Requests in those modes get the tool whether or not it’s declared.

To make the tool available outside those modes, declare it in the request’s `tools` array. It takes no resources, so it needs no `tool_resources` entry:

Copy code

```
tools:
  - tool_spec:
      type: ask_user_question
      name: ask_user_question
```

Because it’s a built-in tool, any `description` or `input_schema` you supply alongside the tool spec is ignored; the service always advertises its own schema, documented in [Input schema](#label-ask-user-question-schema).

For full information on the agent specification format and instructions on how to modify an existing agent’s specification, see [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage).

### When the tool is unavailable

The service drops the tool from requests with no user present to answer. A tool you declared explicitly is removed from unattended runs. The automatic paths are stricter: they also skip subagent requests and evaluation runs. Either way, write your agent instructions so the agent can still finish its task without asking.

## Input schema

The tool use contains a single required `questions` array of one to four question objects.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `question` | string | Yes | The complete question to show the user, phrased as a question. For example, `Which library should we use for date formatting?` |
| `header` | string | Yes | A very short label for the question, suitable for display as a chip or tag. Maximum 12 characters. For example, `Auth method` or `Approach`. |
| `options` | array | Yes | The choices for this question. Must contain 2–6 option objects. |
| `multiSelect` | boolean | Yes | Whether the user may select more than one option. Set for choices that aren’t mutually exclusive. |

Expand

Show lessSee more

Each entry in `options` is an object with the following fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `label` | string | Yes | The display text for the choice, 1–5 words. |
| `description` | string | Yes | An explanation of what the option means, or what happens if the user picks it. Use this to convey trade-offs. |
| `preview` | string | No | Preview content to render beside the question when the option is focused, such as a code snippet, config block, or ASCII mockup. Rendered as monospaced markdown. Single-select only — the agent does not supply previews when `multiSelect` is `true`. |

Expand

Show lessSee more

The tool use may also carry an `answers` object, a map of string keys to string values, holding answers collected by the client’s permission component. Clients that render their own question UI return the tool result directly and don’t set it.

### Example tool use

Copy code

```
{
  "questions": [
    {
      "header": "Database",
      "question": "Which database should we use for the new service?",
      "multiSelect": false,
      "options": [
        {
          "label": "postgres",
          "description": "Managed Postgres. Best fit for relational joins and strong consistency."
        },
        {
          "label": "sqlite",
          "description": "Embedded, zero-operations. Suits a single-writer local workload."
        }
      ]
    },
    {
      "header": "Features",
      "question": "Which optional features should be enabled at launch?",
      "multiSelect": true,
      "options": [
        {
          "label": "Audit logging",
          "description": "Record every write to a separate audit table."
        },
        {
          "label": "Soft deletes",
          "description": "Mark rows deleted instead of removing them."
        }
      ]
    }
  ]
}
```

Render all questions from one tool use together, so the user answers a single form rather than a sequence of prompts.

## Known limitations

The Cortex Agent ask user question tool is subject to the following known limitations:

- **No free-form-only questions**: Every question carries 2–6 options. The only free-text path is the **Something else** choice your client adds.
- **Not offered in non-interactive contexts**: The tool is removed from unattended runs, subagent requests, and evaluation runs. See [When the tool is unavailable](#label-ask-user-question-unavailable).

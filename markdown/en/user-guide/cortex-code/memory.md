# Memory in CoCo

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Memory lets CoCo keep useful context from one session to the next, such as your preferences, decisions about a
project, and rules that you want it to follow. In a new session, CoCo recalls the memories that are relevant to
your request, so you don’t need to repeat them.

This page describes memory in the CoCo CLI, in CoCo in Snowsight (including CoCo mode), and in CoCo Desktop. On
each surface, you can ask CoCo to remember something during a session. In the CoCo CLI, you can also manage memory
yourself with the `cortex memory` commands. In CoCo Desktop, you manage memory from the Memory section of the
Personalization page in Agent Settings. For more information, see
[Memory in CoCo Desktop](/user-guide/cortex-code/cortex-code-desktop/memory).

## Memory types

Each memory item has one of the following types:

| Type | Use it for |
| --- | --- |
| `preference` | How you like to work, such as a default warehouse or a coding style. |
| `lesson` | Guidance that you gave CoCo, such as an approach to avoid or to keep using. |
| `context` | Background on ongoing work, such as a deadline or the reason for a decision. |
| `pointer` | Where to find information, such as a dashboard or a project tracker. |
| `rule` | A standing instruction that CoCo always follows. |
| `other` | Anything else. An item that you save without a type has this type. |

Expand

Show lessSee more

Memory is for durable context, not for the details of the task that you’re working on now.

## Memory scopes

- **Project memory** applies only to the current project. This is the default scope.
- **Global memory** applies to all of your projects. To save or manage global memory, add the `--global` (or `-g`)
  option.

## Save a memory

To save a memory during a session, ask CoCo in your own words. For example:

```
Remember that our dbt models live in the ANALYTICS database.
```

To save a memory item from the command line, run the following command:

Copy code

```
cortex memory remember "Use the ANALYTICS_WH warehouse for ad hoc queries"
```

To save a global rule with a title and tags, run the following command:

Copy code

```
cortex memory remember "Ask before running DROP statements" \
  --rule --global --title "Confirm drops" --tags safety
```

If a similar item already exists, CoCo doesn’t save a duplicate. Edit the existing item instead.

## Use memory in CoCo in Snowsight

In CoCo in Snowsight, you manage memory by asking CoCo in the chat. For example:

```
Remember that I prefer the ANALYTICS_WH warehouse.
What do you remember about this project?
Forget the note about the old staging database.
```

In a workspace, project memory applies to that workspace.

## Find and view memories

To list memory items, run one of the following commands:

Copy code

```
cortex memory list
cortex memory list --global-only
cortex memory list --project-only --type rule
cortex memory list --json
```

To search memory items, run one of the following commands:

Copy code

```
cortex memory recall "warehouse preference"
cortex memory recall "^dbt" --query-type REGEX
```

The `--query-type` option accepts `FUZZY` (the default) or `REGEX`.

To show the full content of one or more items, run the following command:

Copy code

```
cortex memory show <id> [<id> ...]
```

## Edit or delete a memory

To edit or delete a memory item, run one of the following commands:

Copy code

```
cortex memory edit <id> "Use ANALYTICS_WH_XS for ad hoc queries"
cortex memory edit <id> --type preference --title "Default warehouse"
cortex memory drop <id>
```

To edit or delete a global item, add the `--global` option. With `edit`, the `--tags` option replaces all of the
item’s tags.

## Apply tags by default

To apply the same tags to every item that you save and every search that you run, set the `CORTEX_MEMORY_TAGS`
environment variable to a comma-separated list of tags. The `--tags` option overrides this variable.

For a full list of commands and options, see the
[memory commands in the CoCo CLI reference](/user-guide/cortex-code/cli-reference#label-coco-cli-memory-subcommands).

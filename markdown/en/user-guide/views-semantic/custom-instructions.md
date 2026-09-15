# Custom instructions in Cortex Analyst

Custom instructions let you have greater control over SQL generation. Using natural language, you can tell Cortex Analyst
exactly how to generate SQL queries from within your semantic model YAML file. For example, use custom instructions
to tell Cortex Analyst what you mean by *performance* or *financial year*. In this way, you can improve the accuracy of the generated SQL
by incorporating custom logic or additional elements.

For more granular control, you can also specify custom instructions for individual modules in the SQL generation pipeline. See
[Module custom instructions](#label-cortex-analyst-module-custom-instructions) for more information.

## How custom instructions work

Cortex Analyst introduces the `custom_instructions` field into the semantic model YAML file.
This field enables you to apply defining modifications or additions to SQL generation.

For more information about the semantic model syntax, see [Using SQL commands to create and manage semantic views](/user-guide/views-semantic/sql).

## Examples

To explore possible use cases for custom instructions, consider the following examples.

### Formatting data output

Ensure that all numbers in the output are rounded to two decimal points.

#### The `custom_instructions` field in the semantic model YAML file

Copy code

```
custom_instructions: "Ensure that all numeric columns are rounded to 2 decimal points in the output."
```

#### Generated SQL query

Copy code

```
SELECT
  ROUND(column_name, 2) AS column_name,
  ...
FROM
  your_table;
```

### Adjusting percentages

Automatically multiply percentage or rate calculations by 100 for consistency.

#### The `custom_instructions` field in the semantic model YAML file

Copy code

```
custom_instructions: "For any percentage or rate calculation, multiply the result by 100."
```

#### Generated SQL query

Copy code

```
SELECT
  (column_a / column_b) * 100 AS percentage_rate,
  ...
FROM
  your_table;
```

### Adding default filters

Apply a filter if the user doesn’t specify one (for example, default to the last year).

#### The `custom_instructions` field in the semantic model YAML file

Copy code

```
custom_instructions: "If no date filter is provided, apply a filter for the last year."
```

#### Generated SQL query

Copy code

```
SELECT
  ...
FROM
  your_table
WHERE
  date_column >= DATEADD(YEAR, -1, CURRENT_DATE);
```

### Linking column filters

Apply additional filters on related columns based on user input.

#### The `custom_instructions` field in the semantic model YAML file

Copy code

```
custom_instructions: "If a filter is applied on column X, ensure that the same filter is applied to dimension Y."
```

#### Generated SQL query

Copy code

```
SELECT
  ...
FROM
  your_table
WHERE
  column_x = 'filter_value' AND
  dimension_y = 'filter_value';
```

## Module custom instructions

Set the `module_custom_instructions` key in the top level of your semantic model to define custom instructions for specific components in the SQL generation pipeline.
This feature is useful for use cases like the following:

- Define logic that influences how user questions are interpreted before SQL is generated
- Maintain separate, more structured instructions for different parts of the Analyst workflow
- Transition from existing `custom_instructions` to a more modular format as your usage grows

Currently, `module_custom_instructions` supports the following components:

- `question_categorization`: Define how Cortex Analyst should classify user questions (for example, by blocking certain topics or guiding user behavior).
- `sql_generation`: Specify how SQL should be generated (for example, data formatting and filtering).

Instructions for either or both of these components can be set under the `module_custom_instructions` key.

Important

Migrate any existing `custom_instructions` to the `sql_generation` component, as shown in the following example.

### Migrating existing custom instructions

If your model already has a `custom_instructions` field, migrate its content to the `sql_generation` field
under `module_custom_instructions`.

Before:

Copy code

```
custom_instructions: "Ensure that all numeric columns are rounded to 2 decimal points."
```

After:

Copy code

```
module_custom_instructions:
  sql_generation: |
     "Ensure that all numeric columns are rounded to 2 decimal points."
```

### Blocking questions about specific topics

You can use the `question_categorization` component to block questions about specific topics. For example, if you want
to block questions about users, you might set the following instructions. Cortex Analyst then rejects questions about
users with a message telling them to contact their administrator.

Copy code

```
module_custom_instructions:
  question_categorization: |
     Reject all questions asking about users. Ask users to contact their admin.
```

You can also use question categorization instructions to ask for missing details. In the following example, Cortex Analyst asks the user to
provide a product type if they ask about users and do not specify one.

Copy code

```
module_custom_instructions:
  question_categorization: |
    - If the question asks for users without providing a product_type, consider this question UNCLEAR and ask the user to specify product_type.
```

### Custom instructions through Cortex Agents

When Cortex Analyst is used as a tool within a [Cortex Agent](/user-guide/snowflake-cortex/cortex-agents),
the agent follows your custom instructions with higher fidelity. In this mode, the agent interprets your
natural-language instructions directly, rather than relying on specific state keywords like `UNCLEAR`.

You can write custom instructions in plain language without referencing categorization states. For example:

Copy code

```
module_custom_instructions:
  question_categorization: |
    - If the question asks for users without providing a product_type, ask the user to specify product_type.
    - Reject all questions about salary data and tell the user this information is not available.
```

The categorization state keywords (such as `UNCLEAR`) continue to work when using the Cortex Analyst API directly.
However, when your semantic model is accessed through a Cortex Agent, writing instructions in plain natural language
is recommended, as the agent can follow nuanced instructions more precisely.

## Best practices

Be specific.
:   Clearly describe the modifications; for example, “Add a column with a fixed value of 42” or “Include a sum calculation for column X.”

Start small.
:   Start with simple modifications, such as adding a static column or default filters, before moving to more complex scenarios.

Preview the generated SQL query.
:   Ensure that the instructions apply as intended and that the generated SQL query is correct.

Iterate gradually.
:   Experiment with more complex use cases as your familiarity with the feature grows.

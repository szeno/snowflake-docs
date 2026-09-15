# Cortex Analyst Verified Query Repository

The Cortex Analyst Verified Query Repository (VQR) can help improve the accuracy and trustworthiness of results by
providing a collection of questions and corresponding SQL queries to answer them. Cortex Analyst then leverages
relevant SQL queries from the repository when answering similar questions. You can specify verified queries in your
semantic model YAML file.

Important

Verified SQL queries must use the names of the logical tables and columns defined in the semantic model, not those
in the underlying dataset. See the [example query and its discussion](/user-guide/views-semantic/verified-query-repository#label-cortex-analyst-example-verified-query)
for more information.

Verified queries are specified in the `verified_queries` section of the semantic model, as shown here.

Copy code

```
verified_queries:

# Verified Query 1
- name:                         # A descriptive name of the query.
  question:                     # The natural language question that this query answers.
  verified_at:                  # Optional: Time (in seconds since the UNIX epoch, January 1, 1970) when the query was verified.
  verified_by:                  # Optional: Name of the person who verified the query.
  use_as_onboarding_question:   # Optional: Marks this question as an onboarding question for the end user.
  sql:                          # The SQL query for answering the question.

# Verified Query 2
- name:
  question:
  verified_at:
  verified_by:
  use_as_onboarding_question:
  sql:
```

Below is a sample semantic model that includes a verified query.

Copy code

```
name: Sales Data
tables:
- name: sales_data
  base_table:
    database: sales
    schema: public
    table: sd_data

  dimensions:
    - name: state
      description: The state where the sale took place.
      expr: d_state
      data_type: TEXT
        unique: false
        sample_values:
          - "CA"
          - "IL"

    # Time dimension columns in the logical table.
    time_dimensions:
      - name: sale_timestamp
        synonyms:
          - "time_of_sale"
          - "transaction_time"
        description: The time when the sale occurred. In UTC.
        expr: dt
        data_type: TIMESTAMP
        unique: false

    # Measure columns in the logical table.
    measures:
      - name: profit
        synonyms:
          - "earnings"
          - "net income"
        description: The profit generated from a sale.
        expr: amt - cst
        data_type: NUMBER
        default_aggregation: sum

verified_queries:
  - name: "California profit"
    question: "What was the profit from California last month?"
    verified_at: 1714497970
    verified_by: Jane Doe
    use_as_onboarding_question: true
    sql: "
SELECT sum(profit)
FROM __sales_data
WHERE state = 'CA'
    AND sale_timestamp >= DATE_TRUNC('month', DATEADD('month', -1, CURRENT_DATE))
    AND sale_timestamp < DATE_TRUNC('month', CURRENT_DATE)
"
```

In the example above, `__sales_data` corresponds to the `sales_data` table defined in the
model. To avoid name conflicts, the name of the logical table is prefixed with two underscores. The columns used
in the query (`state`, `sale_timestamp`, and `profit`) are the logical columns defined in the model’s
`sale_data` table. The names of the underlying columns (`d_state`, `dt`, `amt`, and `cst`) are not used
directly in the query.

As illustrated in the example, the question doesn’t need to be a complete sentence, or actually in the form of a
question, but it should reflect something a user might ask. Ensure that the SQL queries are syntactically correct and
actually answer the posed questions; this is the essence of a “verified query.” Invalid or inaccurate queries can
negatively impact Cortex Analyst’s performance and accuracy.

Tip

Use the open-source semantic model generator app, described in the next section, to help add verified queries to
your semantic model, without needing to concern yourself with SQL or YAML syntax.

## Adding verified queries using the semantic model generator

Snowflake provides an open-source Streamlit app to help add verified queries to your model. To
install and use this app, follow these instructions.

1. **Clone the repository.** Start by cloning the [semantic-model-generator](https://github.com/Snowflake-Labs/semantic-model-generator)
   repository.
2. **Configure credentials and install the app.** Follow the setup instructions in the repo’s [README](https://github.com/Snowflake-Labs/semantic-model-generator/blob/main/README.md) to provide your Snowflake credentials and run the app either on Snowflake or locally.
3. **Configure the app.** Once the app is running, enter the database, schema, and stage location of your semantic model YAML
   file into the provided fields. The YAML file will appear in an interactive editor on the left side of the window.
4. **Generate a Query.** On the right side of the window, use the chat interface to ask a question that will generate a SQL
   query.
5. **Verify and Save the Query.**

> - Inspect the generated query and the results it produces. If it works as expected, select the **Save as verified query**
>   button below the assistant’s answer to add the query to your semantic model.
> - If the generated query is incorrect, select the **Edit** button to modify the query. Run the modified query to check if
>   it produces the intended results. Continue editing and testing until the query works as desired. Then select
>   **Save as verified query** to add it to your semantic model.

1. **Update the Semantic Model.** Select the **Save** button in the bottom left of the window to update the semantic model.
   Repeat the process to add more queries.
2. **Upload the new YAML file.** Once you’re satisfied with the queries you’ve added, select the **Upload** button, enter a file
   name for your new YAML file, and select **Submit Upload**.

When you return to your stage in Snowsight, you’ll see the new semantic model YAML file with your verified queries.

## Adding suggested Cortex Analyst Verified Query entries

Cortex Analyst also provides the Verified Query Suggestion interface in Snowsight, which offers potential new verified queries based on user behavior. For information about adding verified query suggestions, see [Suggestions for semantic models and views](/user-guide/views-semantic/verified-query-suggestions).

## Viewing verified queries used in the Cortex Analyst response

When the user’s question is similar to a query in the Verified Query Repository (VQR), Cortex Analyst uses that query to generate
the SQL query in its response. To see which verified query was used, see the [confidence field](/user-guide/snowflake-cortex/cortex-analyst/rest-api#label-cortex-analyst-rest-api-response)
in the API response.

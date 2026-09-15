# Custom clean room template reference

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## About clean room templates

Clean room templates are written in [JinjaSQL](https://github.com/sripathikrishnan/jinjasql). JinjaSQL is an extension to the Jinja
templating language that generates a SQL query as output. This allows templates to use logic statements and run-time variable resolution to
let the user specify table names, table columns, and custom values used in the query at run time.

Snowflake provides some pre-designed templates for common use cases.
However, most users prefer to create custom query templates for their clean rooms. Custom templates are created using the clean rooms API, but can be run either in code or using the clean rooms UI.

There are two general types of templates:

- **Analysis templates**, which evaluate to a SELECT statement (or a set of SELECT operations) that show results to the template runner.
- **Activation templates**, which are used to activate results to a Snowflake account or a third-party, rather than showing results
  in the immediate environment. An activation template is very similar to an analysis template with [a few extra requirements](#label-dcr-v1-custom-templates-activation).

  In the clean rooms UI, an analysis template can be associated with an activation template to enable the caller to run an analysis, see
  results, and then activate data to themselves or a third party. The activation template does not need to resolve to the same query as the
  associated analysis template.

## Creating and running a custom template

In a clean room with default settings, the provider adds a template to a clean room and the consumer runs the template, as described in the [custom template usage documentation](/user-guide/cleanrooms/demo-flows/custom-templates).

### A quick example

Here is a simple SQL example that joins a provider and a consumer table by email and shows the overlap count per city:

Copy code

```
SELECT COUNT(*), city FROM consumer_table
  INNER consumer_table
  ON consumer_table.hashed_email = provider_table.hashed_email
  GROUP BY city;
```

Here is how that query would look as a JinjaSQL template that allows the caller to choose the JOIN and GROUP BY columns, as well as the tables used:

Copy code

```
SELECT COUNT(*), IDENTIFIER({{ group_by_col | column_policy }})
  FROM IDENTIFIER({{ my_table[0] }}) AS c
  INNER JOIN IDENTIFIER({{ source_table[0] }}) AS p
  ON IDENTIFIER({{ consumer_join_col | join_policy }}) = IDENTIFIER({{ provider_join_col | join_policy }})
  GROUP BY IDENTIFIER({{ group_by_col | column_policy }});
```

**Notes on the template:**

- Values within {{ double bracket pairs }} are custom variables. `group_by_col`, `my_table`, `source_table`,
  `consumer_join_col`, `provider_join_col`, and `group_by_col` are all custom variables populated by the caller.
- `source_table` and `my_table` are Snowflake-defined string array variables populated by the caller. Array members are
  fully-qualified names of provider and consumer tables linked into the clean room. The caller specifies which tables should be
  included in each array.
- Provider tables must be aliased as lowercase `p` and consumer tables as lowercase `c` in a template. If you have
  multiple tables, you can index them as `p1`, `p2`, `c1`, `c2`, and so on.
- IDENTIFIER is needed for all column and table names, because variables in {{ double brackets }} evaluate to string literals, which aren’t
  valid identifiers.
- JinjaSQL *filters* can be applied to variables to enforce any [join or column policies](/user-guide/cleanrooms/v1/policies) set by
  either side. Snowflake implements custom filters *join\_policy* and *column\_policy*, which
  verify whether a column complies with join or column policies in the clean room respectively, and fail the query if it does not. A
  filter is applied to a column name as `{{ column_name | filter_name }}`.

All these points will be discussed in detail later.

Here is how a consumer might run this template in code. Note how column names are qualified by the table aliases
declared in the template.

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.CONSUMER.RUN_ANALYSIS(
  $cleanroom_name,
  $template_name,
  ['my_db.my_sch.consumer_table],       -- Populates the my_table variable
  ['my_db.my_sch.provider_table'],      -- Populates the source_table variable
  OBJECT_CONSTRUCT(                     -- Populates custom named variables
    'consumer_join_col','c.age_band',
    'provider_join_col','p.age_band',
    'group_by_col','p.device_type'
  )
);
```

To be able to use this template in the clean rooms UI, the provider must
[create a custom UI form for the template](#dcr-provider-add-ui-form-customizations). The UI form has named
form elements that correspond to template variable names, and the values provided in the form are passed into the template.

### Developing a custom template

Clean room templates are JinjaSQL templates. To create a template, you should be familiar with the following topics:

- [Jinja templating basics](https://jinja.palletsprojects.com/en/stable/)
- The [JinjaSQL extension to Jinja](https://github.com/sripathikrishnan/jinjasql).

Use the [consumer.get\_jinja\_sql](/user-guide/cleanrooms/consumer#label-dcr-sproc-consumer-get-sql-request) procedure to test the validity of your template,
then run the rendered template to see that it produces the results that you expect. Note that this procedure doesn’t support clean room filter extensions, such as `join_policy`, so you must test your template without those filters, and add them later.

**Example:**

Copy code

```
-- Template to test
SELECT {{ col1 | sqlsafe }}, {{ col2 | sqlsafe }}
  FROM IDENTIFIER({{ source_table[0] }}) AS p
  JOIN IDENTIFIER({{ my_table[0] }}) AS c
  ON {{ provider_join_col | sqlsafe }} = {{ consumer_join_col | sqlsafe}}
  {% if where_phrase %} WHERE {{ where_phrase | sqlsafe}}{% endif %};

-- Render the template.
USE WAREHOUSE app_wh;
USE ROLE SAMOOHA_APP_ROLE;

CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.CONSUMER.GET_SQL_JINJA(
$$
SELECT {{ col1 | sqlsafe }}, {{ col2 | sqlsafe }}
  FROM IDENTIFIER({{ source_table[0] }}) AS p
  JOIN IDENTIFIER({{ my_table[0] }}) AS c
  ON IDENTIFIER({{ provider_join_col }}) = IDENTIFIER({{ consumer_join_col }})
  {% if where_phrase %} WHERE {{ where_phrase | sqlsafe }}{% endif %};
  $$,
  object_construct(
'col1', 'c.status',
'col2', 'c.age_band',
'where_phrase', 'p.household_size > 2',
'consumer_join_col', 'c.age_band',
'provider_join_col', 'p.age_band',
'source_table', ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS'],
'my_table', ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS']
));
```

The rendered template looks like this:

```
SELECT c.status, c.age_band
  FROM IDENTIFIER('SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS') AS p
  JOIN IDENTIFIER('SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS') AS c
  ON p.age_band = c.age_band
  WHERE p.household_size > 2;
```

Try running the SQL statement above in your environment to see if it works, and gets the expected results.

Then test your template without a WHERE clause:

Copy code

```
-- Render the template without a WHERE clause
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.CONSUMER.GET_SQL_JINJA(
$$
SELECT {{ col1 | sqlsafe }}, {{ col2 | sqlsafe }}
  FROM IDENTIFIER({{ source_table[0] }}) AS p
  JOIN IDENTIFIER({{ my_table[0] }}) AS c
  ON {{ provider_join_col | sqlsafe }} = {{ consumer_join_col | sqlsafe}}
  {% if where_phrase %} WHERE {{ where_phrase | sqlsafe }}{% endif %};
  $$,
  object_construct(
'col1', 'c.status',
'col2', 'c.age_band',
'consumer_join_col', 'c.age_band',
'provider_join_col', 'p.age_band',
'source_table', ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS'],
'my_table', ['SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS']
));
```

Rendered template:

```
SELECT c.status, c.age_band
  FROM IDENTIFIER('SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS') AS p
  JOIN IDENTIFIER('SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS') AS c
  ON p.age_band = c.age_band
  ;
```

Add the policy filters to the template, and add the template to your clean room:

Copy code

```
CALL samooha_by_snowflake_local_db.provider.add_custom_sql_template(
    $cleanroom_name,
    'simple_template',
    $$
    SELECT {{ col1 | sqlsafe | column_policy }}, {{ col2 | sqlsafe | column_policy }}
      FROM IDENTIFIER({{ source_table[0] }}) AS p
      JOIN IDENTIFIER({{ my_table[0] }}) AS c
      ON {{ provider_join_col | sqlsafe | join_policy }} = {{ consumer_join_col | sqlsafe | join_policy }}
      {% if where_phrase %} WHERE {{ where_phrase | sqlsafe }}{% endif %};
    $$,
);
```

### Data protection

Templates can access only datasets linked into the clean room by the provider and consumer.

Both the provider and consumer can set join, column, and activation policies on their data to protect which columns can be
joined on, projected, or activated; however, the template must include
[the appropriate JinjaSQL policy filter](#label-dcr-v1-template-filters) on a column for the policy to be applied.

## Custom template syntax

Snowflake Data Clean Rooms supports V3 JinjaSQL, with a few extensions as noted.

This section includes the following topics:

- [Template naming rules](#template-naming-rules)
- [Template variables](#template-variables)
- [Required table aliases](#required-table-aliases)
- [Custom clean room template filters](#custom-clean-room-template-filters)
- [Enforcing clean room policies](#enforcing-clean-room-policies)
- [Running custom Python code](#running-custom-python-code)

### Template naming rules

When creating a template, names must be all lowercase letters, numbers, spaces, or underscores.
Activation templates (except for consumer-run provider activation) must have a name beginning with `activation_`. Template names are
assigned when you call `provider.add_custom_sql_template` or `consumer.create_template_request`.

**Example valid names:**

- `my_template`
- `activation_template_1`

**Example invalid names:**

- `my template` - Spaces not allowed
- `My_Template` - Only lowercase templates allowed

### Template variables

Template callers can pass in values to template variables. JinjaSQL syntax enables variable binding for any variable name
within {{ double\_brackets }}, but Snowflake reserves a few variable names that you should not override, as described below.

Caution

All variables, whether Snowflake-defined or custom, are populated by the user and should be treated with appropriate caution.
Snowflake Data Clean Rooms templates must resolve to a single SELECT statement, but you should still remember that all variables are
passed in by the caller.

#### Snowflake-defined variables

All clean room templates have access to the following global variables defined by Snowflake, but passed in by the caller:

`source_table`:
:   A zero-based string array of provider-linked tables and views in the clean room that can be used by the template. Table
    names are fully qualified, for example: `my_db.my_sch.provider_customers`

    **Example:** *SELECT col1 FROM IDENTIFIER({{ source\_table[0] }}) AS p;*

`my_table`:
:   A zero-based string array of consumer tables and views in the clean room that can be used by the template. Table names are
    fully qualified, for example: `my_db.my_sch.consumer_customers`

    **Example:** *SELECT col1 FROM IDENTIFIER({{ my\_table[0] }}) AS c;*

`privacy`:
:   A set of privacy-related values associated with users and templates.
    [See the list of available child fields](/user-guide/cleanrooms/differential-privacy#label-dcr-available-privacy-settings).
    These values can be [set explicitly](/user-guide/cleanrooms/differential-privacy) for the user, but you might want to set default
    values in the template. Access the child fields directly in your template, such as `privacy.threshold`.

    **Example:** Here is an example snippet of a template that uses `threshold_value` to enforce a minimum group size in an aggregation
    clause.

    Copy code

    ```
    SELECT
      IFF(a.overlap > ( {{ privacy.threshold_value | default(2)  | sqlsafe }} ),
                        a.overlap,1 ) AS overlap,
      c.total_count AS total_count
      ...
    ```

`measure_column`:

`dimensions`:

`where_clause`:
:   Legacy clean room global variables. They are no longer recommended for use, but are still defined and appear in some legacy templates
    and documentation, so you should not alias tables or columns using either of these names to avoid naming collisions.

    If your template uses `measure_column` or `dimensions`, the column policy is checked against any columns passed into these variables.

    If your template uses a `where_clause` that has a join condition (for example, `table1.column1 = table2.column2`), the join policy is checked against any columns named there; otherwise, the column policy is checked against any columns named there.

#### Custom variables

Template creators can include arbitrary variables in a template that can be populated by the caller. These variables can have any
arbitrary Jinja-compliant name except for the Snowflake-defined variables or table alias names. If you want your template to be usable
in the clean rooms UI, you must also provide a UI form for clean rooms UI users. For API users, you should provide good documentation for the
required and optional variables.

Custom variables can be accessed by your template, as shown here for the custom variable `max_income`:

Copy code

```
SELECT income FROM my_db.my_sch.customers WHERE income < {{ max_income }};
```

Users can pass variables to a template in two different ways:

- **In the clean rooms UI,** by selecting or providing values through a UI form created by the template developer. This UI form contains
  form elements where the user can provide values for your template. The name of the form element is the name of the variable. The template
  simply uses the name of the form element to access the value. Create the UI form using [provider.add\_ui\_form\_customizations](#dcr-provider-add-ui-form-customizations).
- **In code,** a consumer calls [consumer.run\_analysis](#dcr-consumer-run-analysis) and passes in table names as argument arrays, and
  custom variables as name-value pairs into the *analysis\_arguments* argument.

Note

If you need to access user-provided values in any custom Python code uploaded to the clean room, you must
[explicitly pass variable values](#label-dcr-v1-template-custom-python-code) in to the code through Python function arguments; template
variables are not directly accessible within the Python code using `{{jinja variable binding syntax}}`.

#### Resolving variables correctly

String values passed into the template resolve to a string literal in the final template. This can cause SQL parsing or logical errors if
you don’t handle bound variables appropriately:

- `SELECT {{ my_col }} FROM P;` - This resolves to `SELECT 'my_col' from P;` which simply returns the string “my\_col” - probably not
  what you want.
- `SELECT age FROM {{ my_table[0] }} AS P;` - This resolves to `SELECT age FROM 'somedb.somesch.my_table' AS P;`, which causes a
  parsing error because a table must be an identifier, not a literal string.
- `SELECT age FROM IDENTIFIER({{ my_table[0] }}) AS P {{ where_clause }};` - Passing in “WHERE age < 50” evaluates to
  `SELECT age FROM mytable AS P 'WHERE age < 50';`, which is a parsing error because of the literal string WHERE clause.

Therefore, where appropriate, you must resolve variables. Here is how to resolve variables properly in your template:

Resolving table and column names
:   Variables that specify table or column names must be converted to identifiers in your template in one of two ways:

    - [IDENTIFIER](/sql-reference/identifier-literal): For example: *SELECT IDENTIFIER({{ my\_column }}) FROM P;*
    - [sqlsafe](https://github.com/sripathikrishnan/jinjasql?tab=readme-ov-file#sql-safe-strings): This JinjaSQL filter resolves identifier
      strings to SQL text. An equivalent statement to the previous bullet is *SELECT {{ my\_column | sqlsafe }} FROM P;*

    Your particular usage dictates when to use IDENTIFIER or `sqlsafe`. For example, *c.{{ my\_column | sqlsafe }}* can’t easily be
    rewritten using IDENTIFIER.

Resolving dynamic SQL
:   When you have a string variable that should be used as literal SQL, such as a WHERE clause, use the `sqlsafe` filter in your template.
    For example:

    Copy code

    ```
    SELECT age FROM IDENTIFIER({{ my_table[0] }}) AS C WHERE {{ where_clause }};
    ```

    If a user passes in “age < 50” to *where\_clause*, the query would resolve to `SELECT age FROM sometable AS C WHERE 'age < 50';`
    which is invalid SQL because of the literal string WHERE condition. In this case you should use the `sqlsafe` filter:

    Copy code

    ```
    SELECT age FROM IDENTIFIER( {{ my_table[0] }} ) as c {{ where_clause | sqlsafe }};
    ```

### Required table aliases

At the top level of your query, all tables or subqueries must be aliased as either `p` (for provider-tables) or `c` (for consumer
tables) in order for Snowflake to validate join and column policies correctly in the query. Any column that must be verified against join
or column policies must be qualified with the lowercase `p` or `c` table alias. (Specifying `p` or `c` tells the back end
whether to validate a column against the provider or the consumer policy respectively.)

If you use multiple provider or consumer tables in your query, add a numeric, sequential 1-based suffix to each table alias after the
first. So: *p*, `p1`, `p2`, and so on for the first, second, and third provider tables, and `c`, `c1`, `c2`, and so on for the
first, second, and third consumer tables. The `p` or `c` index should be sequential without gaps (that is, create the aliases `p`,
`p1`, and `p2`, not `p`, `p2`, and `p4`).

**Example**

Copy code

```
SELECT p.col1 FROM IDENTIFIER({{ source_table[0] }}) AS P
UNION
SELECT p1.col1 FROM IDENTIFIER({{ source_table[1] }}) AS P1;
```

### Custom clean room template filters

Snowflake supports all the [standard Jinja filters](https://jinja.palletsprojects.com/en/stable/templates/#builtin-filters) and most of
the standard
[JinjaSQL filters](https://github.com/search?q=repo%3Asripathikrishnan%2Fjinjasql+self.env.filters+path%3Ajinjasql%2Fcore.py&type=code&path+jinjasql%2Fcore.py=),
along with a few extensions:

- `join_policy`: Succeeds if the column is in the join policy of the data owner; fails otherwise.
- `column_policy`: Succeeds if the column is in the column policy of the data owner; fails otherwise.
- `activation_policy`: Succeeds if the column is in the activation policy of the data owner; fails otherwise.
- *join\_and\_column\_policy*: Succeeds if the column is in the join or column policy of the data owner; fails otherwise.
- The `identifier` JinjaSQL filter is **not supported** by Snowflake templates.

Tip

JinjaSQL statements are evaluated left to right:

- `{{ my_col | column_policy }}` **Correct**
- `{{ my_col | sqlsafe | column_policy }}` **Correct**
- `{{ column_policy | my_col }}` **Incorrect**
- `{{ my_col | column_policy | sqlsafe }}` **Incorrect:** `column_policy` will be checked against the `my_col` value as string,
  which is an error.

### Enforcing clean room policies

Clean rooms do not automatically check clean room policies against columns used in a template. If you want to enforce a policy against a
column:

- You must apply the appropriate [policy filter](#label-dcr-v1-template-filters) to that column in the template. For example:

Copy code

```
JOIN IDENTIFIER({{ source_table[0] }}) AS p
  ON IDENTIFIER({{ c_join_col | join_policy }}) = IDENTIFIER({{ p_join_col | join_policy }})
```

- You must alias the table as lowercase p or c. See [Required table aliases](/user-guide/cleanrooms/v1/custom-templates#label-dcr-v1-required-template-table-aliases).

Policies are checked only against columns owned by other collaborators; policies are not checked for your own data.

Note that column names cannot be ambiguous when testing policies. So if you have columns with the same
name in two tables, you must qualify the column name in order to test the policy against that column.

### Running custom Python code

Templates can run Python code uploaded to the clean room. The template can call a Python function that
accepts values from a row of data and returns values to use or project in the query.

- When a **provider** uploads custom Python code into a clean room, the template calls Python functions with the syntax
  `cleanroom.function_name`. [More details here.](/user-guide/cleanrooms/demo-flows/custom-code)
- When a **consumer** uploads custom Python code into a clean room, the template calls the function with the bare `function_name` value
  passed to `consumer.generate_python_request_template` (not scoped to *cleanroom* as provider code is). [More details here.](/user-guide/cleanrooms/demo-flows/custom-code)

**Provider code example:**

Copy code

```
-- Provider uploads a Python function that takes two numbers and returns the sum.
CALL samooha_by_snowflake_local_db.provider.load_python_into_cleanroom(
  $cleanroom_name,
  'simple_addition',                        -- Function name to use in the template
  ['someval integer', 'added_val integer'], -- Arguments
  [],                                       -- No packages needed
  'integer',                                -- Return type
  'main',                                   -- Handler for function name
  $$

def main(input, added_val):
  return input + int(added_val)
    $$
);

-- Template passes value from each row to the function, along with a
-- caller-supplied argument named 'increment'
CALL samooha_by_snowflake_local_db.provider.add_custom_sql_template(
    $cleanroom_name,
    'simple_python_example',
$$
    SELECT val, cleanroom.simple_addition(val, {{ increment | sqlsafe }})
    FROM VALUES (5),(8),(12),(39) AS P(val);
$$
);
```

## Security considerations

A clean room template is not executed with the identity of the current user.

The user does not have direct access to any data within the clean room; all access is through the native application via the template
results.

Apply a policy filter any time a column is used in your template to ensure that your policies, and the policies of all collaborators, are
respected.

Wrap user-provided variables with IDENTIFIER() when possible to strengthen your templates against SQL injection attacks.

## Activation templates

A template can also be used to save query results to a table outside of the clean room; this is called *activation*. Currently the only
forms of activation supported for custom templates are provider activation and consumer activation (storing results to the provider or
consumer’s Snowflake account, respectively). [Learn how to implement activation.](/user-guide/cleanrooms/activation)

An activation template is an analysis template with the following additional requirements:

- Activation templates are JinjaSQL statements that evaluate to a SQL script block, unlike analysis templates, which can be simple SELECT
  statements.
- Activation templates create a table in the clean room to store results, and return the table name (or a fragment of the name) to the
  template caller.
- The script block should end with a RETURN statement that returns the name of the generated table, minus any
  `cleanroom.` or `cleanroom.activation_data_` prefix.
- The name of the template, the name of the internal table that the template creates, and the table name the template returns follow these
  patterns:

| Activation type | Template name prefix | Table name prefix | Returned table name |
| --- | --- | --- | --- |
| Consumer-run consumer | `activation_` | `cleanroom.activation_data_*` | Table name without prefix |
| Consumer-run provider | No prefix required | `cleanroom.activation_data_*` | Table name without prefix |
| Provider-run provider | `activation_` | `cleanroom.temp_result_data` is the full table name. | `temp_result_data` |

Expand

Show lessSee more

- Any columns being activated must be listed in the [activation policy](/user-guide/cleanrooms/v1/policies#label-dcr-activation-policies) of the provider or consumer
  who linked the data, and should have the `activation_policy` filter applied to it. Note that a column can be both an activation and
  a join column.
- If the template is to be run from the clean rooms UI, you should
  [provide a web form](/user-guide/cleanrooms/demo-flows/custom-templates#label-dcr-define-user-form) that includes the *activation\_template\_name* and
  *enabled\_activations* fields. Templates for use in the UI must have both an analysis template and an associated activation template.
- All calculated columns must be explicitly aliased, rather than having inferred names, because a table is being generated. That is:
  `SELECT COUNT(*), p.status from T AS P;` FAILS, because the COUNT column name is inferred.

  `SELECT COUNT(*) AS COUNT_OF_ITEMS, p.status from T AS P;` SUCCEEDS, because it explicitly aliases the COUNT column.

Here are two sample basic activation templates. One is for provider-run server activation, the other is for other activation types. They
differ in the two highlighted lines, which contain the results table name.

Provider-run provider activation templateOther activation templates

Table must be named `cleanroom.temp_result_data`:

Copy code

```
BEGIN
  CREATE OR REPLACE TABLE cleanroom.temp_result_data AS
    SELECT COUNT(c.status) AS ITEM_COUNT, c.status, c.age_band
      FROM IDENTIFIER({{ my_table[0] }}) AS c
    JOIN IDENTIFIER({{ source_table[0] }}) AS p
      ON {{ c_join_col | sqlsafe | activation_policy }} = {{ p_join_col | sqlsafe | activation_policy }}
    GROUP BY c.status, c.age_band
    ORDER BY c.age_band;
  RETURN 'temp_result_data';
END;
```

Table name needs prefix `cleanroom.activation_data`:

Copy code

```
BEGIN
  CREATE OR REPLACE TABLE cleanroom.activation_data_analysis_results AS
    SELECT COUNT(c.status) AS ITEM_COUNT, c.status, c.age_band
      FROM IDENTIFIER({{ my_table[0] }}) AS c
    JOIN IDENTIFIER({{ source_table[0] }}) AS p
      ON {{ c_join_col | sqlsafe | activation_policy }} = {{ p_join_col | sqlsafe | activation_policy }}
    GROUP BY c.status, c.age_band
    ORDER BY c.age_band;
  RETURN 'analysis_results';
END;
```

## Next steps

After you’ve mastered the templating system, read the specifics for implementing a clean room with your template type:

- [Provider templates](/user-guide/cleanrooms/demo-flows/provider-run-analysis) are templates written by the provider. This is the
  default use case.
- [Consumer templates](/user-guide/cleanrooms/demo-flows/custom-templates#label-dcr-consumer-written-templates) are templates written by the consumer. In some cases, a
  clean room creator wants to enable the consumer to create, upload, and run their own templates to the clean room.
- [Activation templates](/user-guide/cleanrooms/activation) create a results table after a successful run.
  Depending on the activation template, the results table can either be saved to the provider or consumer’s account outside the clean room,
  or sent to a third-party activation provider listed in the Activation Hub.
- [Chained templates](/user-guide/cleanrooms/developer-template-chains) allow you to chain together multiple templates where the
  output of each template is used by the next template in the chain.

## More information

- [Jinja documentation](https://jinja.palletsprojects.com/en/stable/)
- [JinjaSQL documentation](https://github.com/sripathikrishnan/jinjasql)

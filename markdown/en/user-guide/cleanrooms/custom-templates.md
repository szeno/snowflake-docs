# Design custom templates

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## About clean room templates

Clean room templates are written in [JinjaSQL](https://github.com/sripathikrishnan/jinjasql). JinjaSQL is an extension to the Jinja
templating language. A JinjaSQL template evaluates to a SQL statement when run in a clean room. The JinjaSQL templating language provides logic statements and run-time variable replacement, which enables the template to be customized at run time. For example, a user can provide table and column names when they run the template, and the template can adjust itself based on the values passed in.

There are two general types of templates:

- **Analysis templates**, which evaluate to a SQL DQL statement (a SELECT statement) that returns query results immediately to the template runner.
- **Activation templates**, which are used to activate results to a Snowflake account, rather than showing results
  in the immediate environment. An activation template is very similar to an analysis template with [a few extra requirements](#label-dcr-custom-templates-activation), and it evaluates to a DDL statement (CREATE TABLE).

## Creating, sharing, and running a custom template

Any collaborator can [register and share templates](/user-guide/cleanrooms/resources-templates#label-dcr-collaboration-add-templates-to-collaboration) with specific analysis runners in a collaboration.

Let’s start by looking at a simple SQL query, and how it would be written as a template.

### 1. The JinjaSQL template

Here is a simple SQL query that joins two tables by email and shows the overlap count per city:

Copy code

```
SELECT COUNT(*), city FROM table_1
  INNER JOIN table_2
  ON table_1.hashed_email = table_2.hashed_email
  GROUP BY city;
```

Here is how that query would look as a JinjaSQL template that allows the caller to choose the JOIN and GROUP BY columns, as well as the tables used. The template includes some filters that enforce [Snowflake Data Clean Room policies](/user-guide/cleanrooms/resources-data-offerings#label-dcr-collaborations-policies).

Copy code

```
SELECT COUNT(*), IDENTIFIER({{ group_by_col | column_policy }})
  FROM IDENTIFIER({{ source_table[0] }}) AS p1
  INNER JOIN IDENTIFIER({{ source_table[1] }}) AS p2
  ON IDENTIFIER({{ p1_join_col | join_policy }}) = IDENTIFIER({{ p2_join_col | join_policy }})
  GROUP BY IDENTIFIER({{ group_by_col | column_policy }});
```

**Notes on the template:**

- Values within {{ double bracket pairs }} are variables. The values are populated by the caller.
- `group_by_col`, `source_table`, `p1_join_col`, and `p2_join_col` are all variables
  populated by the caller. These variables have arbitrary names chosen by the template designer.
- `source_table` is a standard Snowflake-defined variable. This variable defines the views to use in the query. These views are datasets
  within data offerings that are linked into the clean room. Collaborators can list available datasets by calling VIEW\_DATA\_OFFERINGS.
- A dataset must be aliased as lowercase `p` if you want to enforce Snowflake Data Clean Room policies on it. If a template uses
  multiple datasets, the first is `p` or `p1`, and additional datasets are indexed as `p2`, `p3`, and so on.
- IDENTIFIER is needed for all column and table names, because variables in {{ double brackets }} evaluate to string literals, which aren’t
  valid identifiers.
- JinjaSQL *filters* are applied to columns to enforce Snowflake Data Clean Room policies on the column. Snowflake implements custom
  filters `join_policy` and `column_policy`, which verify whether a column complies with join or column policies in the clean room
  respectively, and fail the query if it doesn’t. A filter is applied to a column name as `{{ column_name | filter_name }}`.

All these points will be discussed in detail later.

### 2. The Collaboration template

A template is added to a collaboration by embedding it in a YAML specification and registering it, then linking it.

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_TEMPLATE(
  $$
  api_version: 2.0.0
  spec_type: template
  name: my_test_template
  version: 2026_01_12_V1
  type: sql_analysis
  description: A test template
  methodology: Join on single column with a single group by value
  parameters:
  - name: source_tables
    description: Tables from both sides which can be listed in any order, aliased with p1 or p2
    required: true
  - name: p1_join_col
    description: Column to join on from first table specified under source_tables, aliased with p1
    required: true
  - name: p2_join_col
    description: Column to join on from second table specified under source_tables, aliased with p2
    required: true
  - name: group_by_col
    description: Column which results should be grouped group aliased with respective table p1 or p2
    required: true

  template:
    SELECT COUNT(*), IDENTIFIER({{ group_by_col | column_policy }})
    FROM IDENTIFIER({{ source_table[0] }}) AS p1
    INNER JOIN IDENTIFIER({{ source_table[1] }}) AS p2
    ON IDENTIFIER({{ p1_join_col | join_policy }}) = IDENTIFIER({{ p2_join_col | join_policy }})
    GROUP BY IDENTIFIER({{ group_by_col | column_policy }});

$$);
```

You must request to share a template with a given analysis runner, who can accept or reject the request. Additionally, all data providers for that analysis runner must accept the request for the template to be shared.

Copy code

```
-- Request to share template with only Collaborator3.
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.ADD_TEMPLATE_REQUEST(
  $collaboration_name,
  $template_id,
  ['Collaborator3']
);
```

### 3. Running the template

Here is how an analysis runner might run this template in code. Note how column names are qualified by the table aliases
declared in the template.

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN( $collaboration_name,
$$
api_version: 2.0.0
spec_type: analysis
name: example_run
description: Example run for template
template: $template_id

template_configuration:
  view_mappings:
    source_tables:
      - collaborator_1.data_offering_1.dataset_1
      - collaborator_2.data_offering_2.dataset_2
  arguments:
     p1_join_col: p1.hashed_email
     p2_join_col: p2.hashed_email
     group_by_col: p2.device_type

$$ );
```

### Developing a custom template

Clean room templates are JinjaSQL templates. To create a template, you should be familiar with the following topics:

- [Jinja templating basics](https://jinja.palletsprojects.com/en/stable/)
- The [JinjaSQL extension to Jinja](https://github.com/sripathikrishnan/jinjasql).

You can use Cortex Code to validate the SQL output of your JinjaSQL templates based on variable inputs that should be provided. See example prompts below that you can copy into Cortex Code to get final SQL outputs you can test:

**Example:**

```
Resolve the following Jinja template into SQL based on the variables defined:

Jinja Template:
 SELECT IDENTIFIER({{ col1 | column_policy }}), IDENTIFIER({{ col2 | column_policy }})
  FROM IDENTIFIER({{ source_table[0] }}) AS p1
  JOIN IDENTIFIER({{ source_table[1] }}) AS p2
  ON  IDENTIFIER({{ p1_join_col | join_policy }}) = IDENTIFIER({{ p2_join_col | join_policy }})
  {% if where_phrase %} WHERE {{ where_phrase | sqlsafe }}{% endif %};

Variable Inputs:
source_table: SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS, SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS
col1: p1.status
col2: p1.age_band
p1_join_col: p1.hashed_email
p2_join_col: p2.hashed_email
where_phrase: p1.household_size > 2
```

The rendered template looks like this:

```
SELECT IDENTIFIER('p1.status'), IDENTIFIER('p1.age_band')
FROM IDENTIFIER('SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS') AS p1
JOIN IDENTIFIER('SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS') AS p2
ON  IDENTIFIER('p1.hashed_email') = IDENTIFIER('p2.hashed_email')
WHERE p1.household_size > 2;
```

Try running the SQL statement above in your environment to see if it works and gets the expected results.

Then test your template without a WHERE clause:

```
Resolve the following Jinja template into SQL based on the variables defined:

Jinja Template:
 SELECT IDENTIFIER({{ col1 | column_policy }}), IDENTIFIER({{ col2 | column_policy }})
  FROM IDENTIFIER({{ source_table[0] }}) AS p1
  JOIN IDENTIFIER({{ source_table[1] }}) AS p2
  ON  IDENTIFIER({{ p1_join_col | join_policy }}) = IDENTIFIER({{ p2_join_col | join_policy }})
  {% if where_phrase %} WHERE {{ where_phrase | sqlsafe }}{% endif %};

Variable Inputs:
source_table: SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS, SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS
col1: p1.status
col2: p1.age_band
p1_join_col: p1.hashed_email
p2_join_col: p2.hashed_email
```

Rendered template:

```
SELECT IDENTIFIER('p1.status'), IDENTIFIER('p1.age_band')
FROM IDENTIFIER('SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS') AS p1
JOIN IDENTIFIER('SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS') AS p2
ON  IDENTIFIER('p1.hashed_email') = IDENTIFIER('p2.hashed_email');
```

Add the template into your clean room, and test with an analysis run spec.

### Data protection

Templates can access only datasets linked into the clean room by collaborators.

Collaborators specify join, column, and activation policies on their datasets to ensure that only those columns can be used as an input for a template variable.

Important

The template must include
[the appropriate JinjaSQL policy filter](#label-dcr-template-filters) on a column for the policy to be applied.

## Custom template syntax

Snowflake Data Clean Rooms supports V3 JinjaSQL, with a few extensions as noted.

This section includes the following topics:

- [Template naming rules](#template-naming-rules)
- [Template variables](#template-variables)
- [Required table aliases](#required-table-aliases)
- [Custom clean room template filters](#custom-clean-room-template-filters)
- [Enforcing clean room policies](#enforcing-clean-room-policies)

### Template naming rules

When creating a template, names must contain only letters, numbers, or underscores.
Template names are assigned in the template specification’s `name` field when you register the template.

**Example valid names:**

- `my_template`
- `activation_template_1`

**Example invalid names:**

- `my template` - Spaces not allowed
- `my_template!` - Special characters not allowed

### Template variables

Template callers can pass in values to template variables. JinjaSQL syntax enables variable binding for any variable name
within {{ double\_brackets }}, but Snowflake reserves a few variable names that you shouldn’t override, as described below.

Caution

All variables, whether Snowflake-defined or custom, are populated by the user and should be treated with appropriate caution.
Analysis templates must resolve to a single SELECT statement (activation templates resolve to a script block). Remember that all
variables are passed in by the caller.

#### Snowflake-defined variables

All clean room templates have access to the following global variables defined by Snowflake. The analysis runner passes in `source_table`
and `my_table`; the template author defines `preset_tables`.

`source_table`:
:   A zero-based string array of tables and views from data offerings linked into the collaboration via LINK\_DATA\_OFFERING that can be used by the template.

    **Example:** `SELECT col1 FROM IDENTIFIER({{ source_table[0] }}) AS p;`

`my_table`:
:   In a Collaboration clean room, `my_table` is used only by Snowflake Standard Edition users. For these users, `my_table` is a zero-based string array of datasets that the analysis runner linked by calling LINK\_LOCAL\_DATA\_OFFERING.

    **Example:** `SELECT col1 FROM IDENTIFIER({{ my_table[0] }}) AS c;`

`preset_tables`:
:   A map of datasets that the template author [presets in the template](#label-dcr-template-preset-tables) (preview), rather than the
    analysis runner supplying them at run time. Each dataset is keyed by the alias declared in the `preset_tables` block.

    **Example:** `SELECT publisher.col1 FROM IDENTIFIER({{ preset_tables['publisher'] }}) AS publisher;`

#### Custom variables

Template creators can include arbitrary variables in a template that can be populated by the analysis runner. These variables can have any Jinja-compliant name except for the Snowflake-defined variables or table alias names. You should provide guidance in the parameter section of the template for required and optional variables.

Custom variables can be accessed by your template, as shown here for the custom variable `max_income`:

Copy code

```
SELECT income FROM my_db.my_sch.customers WHERE income < {{ max_income }};
```

Analysis runners pass variables when calling RUN as defined in the [analysis run spec](/user-guide/cleanrooms/spec-analysis).

#### Resolving variables correctly

String values passed into the template resolve to a string literal in the final template. This can cause SQL parsing or logical errors if
you don’t handle bound variables appropriately:

- `SELECT {{ my_col }} FROM p;` - This resolves to `SELECT 'my_col' from p;` which simply returns the string “my\_col” - probably not
  what you want.
- `SELECT age FROM {{ source_table[0] }} AS p;` - This resolves to `SELECT age FROM 'somedb.somesch.source_table' AS p;`, which causes a
  parsing error because a table must be an identifier, not a literal string.
- `SELECT age FROM IDENTIFIER({{ source_table[0] }}) AS p {{ where_clause }};` - Passing in “WHERE age < 50” evaluates to
  `SELECT age FROM mytable AS p 'WHERE age < 50';`, which is a parsing error because of the literal string WHERE clause.

Therefore, where appropriate, you must resolve variables. Here is how to resolve variables properly in your template:

Resolving table and column names
:   Variables that specify table or column names must be converted to identifiers in your template in one of two ways:

    - [IDENTIFIER](/sql-reference/identifier-literal): For example: `SELECT IDENTIFIER({{ my_column }}) FROM p;`
    - [sqlsafe](https://github.com/sripathikrishnan/jinjasql?tab=readme-ov-file#sql-safe-strings): This JinjaSQL filter resolves identifier
      strings to SQL text. An equivalent statement to the previous bullet is `SELECT {{ my_column | sqlsafe }} FROM p;`

    Your particular usage dictates when to use IDENTIFIER or `sqlsafe`. For example, `p.{{ my_column | sqlsafe }}` can’t easily be
    rewritten using IDENTIFIER.

Resolving dynamic SQL
:   When you have a string variable that should be used as literal SQL, such as a WHERE clause, use the `sqlsafe` filter in your template.
    For example:

    Copy code

    ```
    SELECT age FROM IDENTIFIER({{ source_table[0] }}) AS p WHERE {{ where_clause }};
    ```

    If a user passes in “age < 50” to `where_clause`, the query would resolve to `SELECT age FROM sometable AS p WHERE 'age < 50';`
    which is invalid SQL because of the literal string WHERE condition. In this case, you should use the `sqlsafe` filter:

    Copy code

    ```
    SELECT age FROM IDENTIFIER( {{ source_table[0] }} ) as p {{ where_clause | sqlsafe }};
    ```

### Required table aliases

At the top level of your query, all `source_table` datasets must be aliased as `p`, and all `my_table` datasets must be aliased as
`c`, in order for Snowflake to validate join and column policies correctly in the query. Any column that must be verified against join
or column policies must be qualified with the lowercase `p` or `c` table alias.

If you use multiple `source_table` or `my_table` datasets in your query, add a numeric, sequential 1-based suffix to each table alias
after the first. So: `p` or `p1`, `p2`, `p3`, and so on for the first, second, and third `source_table` datasets, and `c` or `c1`, `c2`,
`c3`, and so on for the first, second, and third `my_table` datasets. The `p` or `c` index should be sequential without gaps (that
is, create the aliases `p1`, `p2`, and `p3`, not `p1`, `p2`, and `p4`).

Because `p` and `c` aliases are reserved, a [preset table](#label-dcr-template-preset-tables) (preview) can’t use them in the template
body. Give a preset table any other SQL alias that is a valid [Snowflake identifier](/sql-reference/identifiers-syntax).

**Example**

Copy code

```
SELECT p1.col1 FROM IDENTIFIER({{ source_table[0] }}) AS p1
UNION
SELECT p2.col1 FROM IDENTIFIER({{ source_table[1] }}) AS p2;
```

### Custom clean room template filters

Snowflake supports all the [standard Jinja filters](https://jinja.palletsprojects.com/en/stable/templates/#builtin-filters) and most of
the standard
[JinjaSQL filters](https://github.com/search?q=repo%3Asripathikrishnan%2Fjinjasql+self.env.filters+path%3Ajinjasql%2Fcore.py&type=code&path+jinjasql%2Fcore.py=),
along with a few extensions:

`join_policy`:
:   Succeeds if the column is in the join policy of the data owner; fails otherwise. See [Applying data protection policies to data offerings](/user-guide/cleanrooms/resources-data-offerings#label-dcr-apply-usage-policies-to-collaboration).

`column_policy`:
:   Succeeds if the column is in the column policy of the data owner; fails otherwise. See [Applying data protection policies to data offerings](/user-guide/cleanrooms/resources-data-offerings#label-dcr-apply-usage-policies-to-collaboration).

`activation_policy`:
:   Succeeds if the column is in the activation policy of the data owner; fails otherwise. See [Applying data protection policies to data offerings](/user-guide/cleanrooms/resources-data-offerings#label-dcr-apply-usage-policies-to-collaboration).

`join_and_column_policy`:
:   Succeeds if the column is in the join or column policy of the data owner; fails otherwise. See [Applying data protection policies to data offerings](/user-guide/cleanrooms/resources-data-offerings#label-dcr-apply-usage-policies-to-collaboration).

`identifier`:
:   This JinjaSQL filter is **not supported** by Snowflake templates.

Tip

JinjaSQL statements are evaluated left to right:

- `{{ my_col | column_policy }}` **Correct**
- `{{ my_col | sqlsafe | column_policy }}` **Correct**
- `{{ column_policy | my_col }}` **Incorrect**
- `{{ my_col | column_policy | sqlsafe }}` **Incorrect:** `column_policy` will be checked against the `my_col` value as a string,
  which is an error.

### Enforcing clean room policies

Clean rooms don’t automatically check clean room policies against columns used in a template. If you want to enforce a policy against a
column:

- You must apply the appropriate [policy filter](#label-dcr-template-filters) to that column in the template. For example:

Copy code

```
FROM IDENTIFIER({{ source_table[0] }}) AS p1
JOIN IDENTIFIER({{ source_table[1] }}) AS p2
  ON IDENTIFIER({{ p1_join_col | join_policy }}) = IDENTIFIER({{ p2_join_col | join_policy }})
```

- You must alias the table as lowercase `p` or `c`. See [Required table aliases](#label-dcr-required-template-table-aliases).

Policies are checked only against columns of tables referenced in a **source\_table** variable, which refer
to views shared within the clean room. Policies are not checked against columns of tables referenced in
a **my\_table** variable, which are local tables not shared within the clean room.

Note that column names can’t be ambiguous when testing policies. So if you have columns with the same
name in two tables, you must qualify the column name in order to test the policy against that column.

## Preset tables

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

An analysis runner chooses every dataset a template reads by passing it in `source_tables` when they call RUN. As a template author,
you can instead preset a dataset in the template, so that the template always reads that dataset and the analysis runner doesn’t
supply it. Use a preset table when you want to do either of the following:

- Guarantee which dataset a template reads, so that an analysis runner can’t substitute a different one.
- Simplify the RUN call, so that the analysis runner supplies only run-time values such as filters and dimensions, and doesn’t need to
  know the provider’s dataset names.

A template can preset some datasets and take others from the analysis runner.

### Declare and reference a preset table

Declare each preset table in the [`preset_tables` block](/user-guide/cleanrooms/spec-template#label-dcr-collaboration-template-yaml)
of the template specification. Each entry maps an `alias` that you choose to the `template_view_name` of the dataset you’re presetting,
in the format `collaborator_alias.data_offering_ID.dataset_alias`. Where the data
offering is already linked into a collaboration, you can copy the value from the TEMPLATE\_VIEW\_NAME column returned by
VIEW\_DATA\_OFFERINGS. You can register a template that presets a dataset either before or after the collaboration exists, because a
preset `template_view_name` is resolved when the template is added to a collaboration and again when the analysis runs.

Reference a preset table in the template body by its alias, using either subscript or dot notation. Both forms are equivalent:

- `{{ preset_tables['alias'] }}`
- `{{ preset_tables.alias }}`

Like `source_table`, a preset table resolves to a string literal, so wrap it in IDENTIFIER to use it as a table name.

The following template presets the publisher’s audience dataset and joins it to a table that the analysis runner supplies:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_TEMPLATE(
  $$
  api_version: 2.0.0
  spec_type: template
  name: preset_overlap_template
  version: 2026_08_18_V1
  type: sql_analysis
  description: Overlap count against a fixed publisher audience
  methodology: Joins the preset publisher audience to a runner-supplied table on hashed email
  parameters:
  - name: source_tables
    description: The advertiser table to compare against the publisher audience
    required: true

  preset_tables:
  - alias: publisher
    template_view_name: pub.pub_audience_v2.AUDIENCE

  template:
    SELECT COUNT(DISTINCT publisher.hashed_email) AS overlap_count
    FROM IDENTIFIER({{ preset_tables['publisher'] }}) AS publisher
    INNER JOIN IDENTIFIER({{ source_table[0] }}) AS p1
    ON publisher.hashed_email = p1.hashed_email;

$$);
```

The analysis runner supplies only the advertiser table, and nothing for the preset publisher dataset:

Copy code

```
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.COLLABORATION.RUN( $collaboration_name,
$$
api_version: 2.0.0
spec_type: analysis
template: $template_id

template_configuration:
  view_mappings:
    source_tables:
      - adv.adv_customers_v1.CUSTOMERS

$$ );
```

If a template presets every dataset it reads, the analysis runner omits `source_tables` from the analysis spec entirely. In the
parameter form of RUN, they pass an empty array for `template_view_names` instead.

A template can also pass a preset table to a [custom function](/user-guide/cleanrooms/resources-code-specs) as an argument, the same
way it passes a `source_table` dataset. A preset table resolves to the same view name string that `source_table` resolves to, so pass
it directly:

Copy code

```
SELECT cleanroom.audience_stats$row_count({{ preset_tables['publisher'] }}) AS publisher_rows;
```

As with any template that calls a custom function, list the function’s code spec in the template’s `code_specs` field.

### Column access and data protection

[DCR policy filters](#label-dcr-template-filters) don’t apply to preset tables. You can’t apply `join_policy`, `column_policy`, or any
other policy filter to a column of a preset table, because policies are evaluated only against the datasets that the analysis runner
supplies. Policies exist to constrain datasets that the template author doesn’t control, and a preset table is chosen by the template
author.

Reference a preset table’s columns as ordinary SQL, qualified by the SQL alias you gave the table in the query. Applying a policy
filter to one of those columns doesn’t restrict the analysis, it fails it with
`PresetTableUnsupportedReferenceError`:

Copy code

```
-- Supported
SELECT publisher.hashed_email FROM IDENTIFIER({{ preset_tables['publisher'] }}) AS publisher;

-- Not supported
SELECT IDENTIFIER({{ publisher.hashed_email | column_policy }}) FROM IDENTIFIER({{ preset_tables['publisher'] }}) AS publisher;
```

That leaves the template body as the only control over which columns of a preset table an analysis can read. Keep the following
practices in mind:

- Be careful with column substitution. Snowflake rejects a caller-supplied column that carries a policy filter, but a caller-supplied
  column with no filter is passed through. So if your template applies an unfiltered variable to a preset table, the analysis runner can
  name any column that the data offering exposes. For example,
  `SELECT IDENTIFIER({{ my_col }}) FROM IDENTIFIER({{ preset_tables['publisher'] }}) AS publisher;` lets the runner read any exposed
  column of the publisher’s dataset. Name the columns you intend to expose in the template body instead.
- If callers must be able to choose a column of a dataset, have the analysis runner supply that dataset in `source_tables` and apply the
  appropriate policy filter to it, rather than presetting it. A template can still apply policy filters to the columns of its
  `source_table` datasets.

### Limitations

In the template body, give a preset table any SQL alias that is a valid [Snowflake identifier](/sql-reference/identifiers-syntax),
except `p`, `c`, or `p` or `c` followed by a number. [Those aliases are reserved](#label-dcr-required-template-table-aliases) for
`source_table` and `my_table` datasets. Template registration fails if a preset table uses a reserved SQL alias.

Data providers keep approval rights over templates that preset their datasets. As with any template, every data provider for an
analysis runner must approve the [request to share the template](/user-guide/cleanrooms/resources-templates#label-dcr-collaboration-add-template-post-creation) with that runner.

## Access considerations and best practices

A template is always executed in context to the clean room application role. A collaborator does not have direct access to any data within the clean room that is restricted to template access only; all access is through the native application roles and the template outputs.

As best practice, you should follow the below for templates you create or use in a clean room:

- Ensure a policy filter is applied any time a column variable is used in a template, so that collaborator policies are respected.
- Wrap user-provided variables with IDENTIFIER() when possible to strengthen templates against SQL injection attacks.

## Activation templates

A template can also be used to save query results to a table outside of the clean room; this is called *activation*. An activation template is an analysis template with the following additional requirements:

- Activation templates are JinjaSQL statements that evaluate to a SQL script block, unlike analysis templates, which can be simple SELECT
  statements.
- Activation templates must create an internal table in the clean room to store results. The table generated by the template must have the
  prefix `cleanroom.activation_data_`, for example: `cleanroom.activation_data_my_results`
- All columns in the internal results table should have the value `activation_allowed: TRUE` in their data offering specification.
- The script block should end with a RETURN statement that returns the name of the generated table without the
  `cleanroom.activation_data_` prefix, for example: `RETURN 'my_results'`.
- The template itself has no naming requirements.

Here is an example activation template specification:

Copy code

```
api_version: 2.0.0
spec_type: template
name: my_activation_template
version: v0
type: sql_activation
description: Activation template that creates segment data
parameters:
  - name: p1_join_column
    description: Join policy column in the first (provider) table, such as a hashed email column
    required: true
  - name: p2_join_column
    description: Join policy column in the second (consumer) table, such as a hashed email column
    required: true
  - name: activation_column
    description: Activation column in the first table (customer ID)
    required: true
template: |
  BEGIN
      CREATE OR REPLACE TABLE cleanroom.activation_data_analysis_results AS
      SELECT
          p1.{{ activation_column | sqlsafe | activation_policy }} AS customer_id
      FROM IDENTIFIER({{ source_table[0] }}) AS p1
      JOIN IDENTIFIER({{ source_table[1] }}) AS p2
          ON p1.{{ p1_join_column | sqlsafe | join_policy }} = p2.{{ p2_join_column | sqlsafe | join_policy }};
      RETURN 'analysis_results';
  END;
```

### Running activations concurrently

Each run of an activation template executes `CREATE OR REPLACE TABLE` against the results table. The preceding example writes to a *fixed* table
name (`cleanroom.activation_data_analysis_results`). If multiple runs of that template execute concurrently, they collide: one run can replace or
drop the table while another run is still using it, causing some runs to fail. (For the error that this produces, see
[Troubleshooting](/user-guide/cleanrooms/v2/troubleshooting#label-dcr-troubleshooting-concurrent-activation).)

To run activations concurrently against the same clean room, give each run a unique results table name. Generate a UUID inside the template,
append it to the `cleanroom.activation_data_` prefix, and return that unique suffix so the runner can locate the results table. The following
template is identical to the previous example, except that it builds a collision-free table name for each run:

Copy code

```
api_version: 2.0.0
spec_type: template
name: my_concurrent_activation_template
version: v0
type: sql_activation
description: Activation template that writes to a unique results table for each run
parameters:
  - name: p1_join_column
    description: Join policy column in the first (provider) table, such as a hashed email column
    required: true
  - name: p2_join_column
    description: Join policy column in the second (consumer) table, such as a hashed email column
    required: true
  - name: activation_column
    description: Activation column in the first table (customer ID)
    required: true
template: |
  DECLARE
      activation_uuid STRING;
      table_name_suffix STRING;
      table_name STRING;
  BEGIN
      SELECT REGEXP_REPLACE(UUID_STRING(), '[^a-zA-Z0-9]', '') INTO :activation_uuid;
      SELECT ('analysis_results_' || :activation_uuid) INTO :table_name_suffix;
      SELECT ('cleanroom.activation_data_' || :table_name_suffix) INTO :table_name;

      CREATE OR REPLACE TABLE IDENTIFIER(:table_name) AS
      SELECT
          p1.{{ activation_column | sqlsafe | activation_policy }} AS customer_id
      FROM IDENTIFIER({{ source_table[0] }}) AS p1
      JOIN IDENTIFIER({{ source_table[1] }}) AS p2
          ON p1.{{ p1_join_column | sqlsafe | join_policy }} = p2.{{ p2_join_column | sqlsafe | join_policy }};

      RETURN :table_name_suffix;
  END;
```

If you don’t need to run activations concurrently, you can use a fixed table name and run them sequentially.

Learn how to implement activation in a collaboration: [Activating query results](/user-guide/cleanrooms/activation).

## Next steps

After you’ve mastered the templating system, read the specifics for implementing a clean room with your template type:

- [Activation templates](/user-guide/cleanrooms/activation) create a results table after a successful run and is shared outside of the clean room. Depending on the collaboration specification, the results table can be shared to the analysis runner or other collaborators.
- [Code specs](/user-guide/cleanrooms/resources-code-specs) are used to upload custom Python UDFs and UDTFs into a collaboration. Templates in the collaboration can run these functions to perform complex data actions.
- [Internal tables](/user-guide/cleanrooms/multistep-flows) are used to store intermediary or persistent results, which can be used downstream to support multistep workflows. These tables are accessible to templates or custom uploaded code inside the clean room.

## More information

- [Jinja documentation](https://jinja.palletsprojects.com/en/stable/)
- [JinjaSQL documentation](https://github.com/sripathikrishnan/jinjasql)

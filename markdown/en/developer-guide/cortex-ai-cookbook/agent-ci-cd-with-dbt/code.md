# Agent CI/CD with dbt: per-PR builds, versioned deploys, and an evaluation gate: code

Every file in the [Agent CI/CD with dbt: per-PR builds, versioned deploys, and an evaluation gate](/developer-guide/cortex-ai-cookbook/agent-ci-cd-with-dbt) recipe. To run the recipe, download [agent-ci-cd-with-dbt.zip](/static/samples/cortex-ai-cookbook/agent-ci-cd-with-dbt.zip), unzip it, and run the scripts from the `agent-ci-cd-with-dbt/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/agent-ci-cd-with-dbt); the zip includes it as `README.md`.

## `agent/`

### `agent/agent_spec.yaml`

Copy code

```
# Agent specification template. ci/scripts/render.sh replaces __DATABASE__,
# __SCHEMA__ and __WAREHOUSE__ per environment, then the rendered file is
# uploaded as agent_spec.yaml to a stage directory and imported with
# CREATE AGENT ... FROM @stage/dir/ or ALTER AGENT ... ADD VERSION FROM @stage/dir/.
#
# The orchestration model is named explicitly instead of `auto` so that an
# evaluation score change is caused by your change, not by a model swap.
models:
  orchestration: claude-sonnet-4-6

orchestration:
  budget:
    seconds: 60
    tokens: 32000

instructions:
  orchestration: >-
    Use the retail_data tool for every question about orders, revenue, customers,
    products, categories, or units sold. If a question is outside retail order data,
    say so instead of guessing.
  response: >-
    Answer with specific numbers. Format currency in US dollars with two decimals.
    When the answer depends on a date range, state the range you used.
  sample_questions:
    - question: "What was total revenue in March 2023?"
    - question: "Which product category has the most revenue?"

tools:
  - tool_spec:
      type: cortex_analyst_text_to_sql
      name: retail_data
      description: >-
        Orders, order lines, customers, and products for the retail store. Use for
        revenue, order counts, average order value, units sold, and breakdowns by
        product, category, customer, state, status, or month.

tool_resources:
  retail_data:
    semantic_view: __DATABASE__.__SCHEMA__.RETAIL_ANALYTICS
    execution_environment:
      type: warehouse
      warehouse: __WAREHOUSE__
```

## `ci/`

### `ci/scripts/cleanup_pr.sh`

Copy code

```
#!/usr/bin/env bash
# Remove everything a pull request created: its schema (tables, semantic view,
# agent), its dbt project object, and its staged files.
#
#   ci/scripts/cleanup_pr.sh PR_42
set -euo pipefail

target="${1:?usage: cleanup_pr.sh PR_<number>}"
[[ "$target" =~ ^PR_[0-9]{1,6}$ ]] || { echo "target must be PR_<number>; this script never touches PROD" >&2; exit 1; }

db="${COOKBOOK_DB:-COOKBOOK_AGENT_CI_CD_WITH_DBT}"
wh="${COOKBOOK_WH:-COOKBOOK_AGENT_CI_CD_WITH_DBT_WH}"
role="${DEPLOYER_ROLE:-COOKBOOK_AGENT_CI_CD_WITH_DBT_DEPLOYER}"
for v in "$db" "$wh" "$role"; do [[ "$v" =~ ^[A-Z0-9_]+$ ]] || { echo "invalid identifier: $v" >&2; exit 1; }; done

read -r -a conn <<< "${SNOW_CONN_FLAGS:--x}"
ctx=("${conn[@]}" --role "$role" --warehouse "$wh" --database "$db" --schema OPS)

snow sql "${ctx[@]}" -q "DROP SCHEMA IF EXISTS ${db}.${target} CASCADE"
snow sql "${ctx[@]}" -q "DROP DBT PROJECT IF EXISTS ${db}.OPS.RETAIL_DBT_${target}"
snow sql "${ctx[@]}" -q "REMOVE @${db}.OPS.AGENT_SPECS/${target}/"
snow sql "${ctx[@]}" -q "REMOVE @${db}.OPS.EVAL_CONFIGS/${target}/"
```

### `ci/scripts/deploy.sh`

Copy code

```
#!/usr/bin/env bash
# Build, deploy, and gate one environment. CI runs exactly this script; you can
# run it locally too.
#
#   ci/scripts/deploy.sh PR_42   # pull request: isolated schema, gate only
#   ci/scripts/deploy.sh PROD    # main: gate, then promote
#
# Connection: SNOW_CONN_FLAGS defaults to "-x" (temporary connection built from
# SNOWFLAKE_* environment variables, which the GitHub Action sets up with OIDC).
# Locally, use a named connection: SNOW_CONN_FLAGS="-c my_connection".
set -euo pipefail

recipe_dir="$(cd "$(dirname "$0")/../.." && pwd)"
target="${1:?usage: deploy.sh <PROD|PR_number>}"
[[ "$target" =~ ^(PROD|PR_[0-9]{1,6})$ ]] || { echo "target must be PROD or PR_<number>" >&2; exit 1; }

db="${COOKBOOK_DB:-COOKBOOK_AGENT_CI_CD_WITH_DBT}"
wh="${COOKBOOK_WH:-COOKBOOK_AGENT_CI_CD_WITH_DBT_WH}"
role="${DEPLOYER_ROLE:-COOKBOOK_AGENT_CI_CD_WITH_DBT_DEPLOYER}"
dbt_version="${DBT_VERSION:-1.11.11}"
min_ac="${MIN_ANSWER_CORRECTNESS:-0.8}"
min_lc="${MIN_LOGICAL_CONSISTENCY:-0.8}"
run_id="${RUN_ID:-${GITHUB_RUN_ID:-local}_${GITHUB_RUN_ATTEMPT:-$(date +%s)}}"
sha="${GITHUB_SHA:-$(git -C "$recipe_dir" rev-parse HEAD 2>/dev/null || echo local)}"
sha="${sha:0:12}"

for v in "$db" "$wh" "$role"; do [[ "$v" =~ ^[A-Z0-9_]+$ ]] || { echo "invalid identifier: $v" >&2; exit 1; }; done
[[ "$run_id" =~ ^[A-Za-z0-9_-]{1,64}$ ]] || { echo "invalid RUN_ID" >&2; exit 1; }
[[ "$sha" =~ ^[A-Za-z0-9]{1,12}$ ]] || { echo "invalid commit sha" >&2; exit 1; }
[[ "$min_ac" =~ ^(0(\.[0-9]+)?|1(\.0+)?)$ && "$min_lc" =~ ^(0(\.[0-9]+)?|1(\.0+)?)$ ]] || { echo "thresholds must be between 0 and 1" >&2; exit 1; }

read -r -a conn <<< "${SNOW_CONN_FLAGS:--x}"
ctx=("${conn[@]}" --role "$role" --warehouse "$wh" --database "$db" --schema OPS)
project="RETAIL_DBT_${target}"
spec_dir="@${db}.OPS.AGENT_SPECS/${target}/${run_id}/"
config_path="@${db}.OPS.EVAL_CONFIGS/${target}/${run_id}/eval_config.yaml"
run_name="ci_${target}_${run_id}"
work="$(mktemp -d)"; trap 'rm -rf "$work"' EXIT

sql() { snow sql "${ctx[@]}" -q "$1"; }
scalar() { snow sql "${ctx[@]}" --format JSON -q "$1" | python3 -c 'import json,sys; print(next(iter(json.load(sys.stdin)[0].values())))'; }

echo "== 1/6 schema ${db}.${target}"
sql "CREATE SCHEMA IF NOT EXISTS ${db}.${target}"

echo "== 2/6 dbt build into ${target}"
snow dbt deploy "$project" --source "$recipe_dir/dbt" --dbt-version "$dbt_version" "${ctx[@]}"
snow dbt execute "${ctx[@]}" "$project" build --vars "{\"deploy_schema\": \"${target}\"}"

echo "== 3/6 stage agent spec"
"$recipe_dir/ci/scripts/render.sh" "$recipe_dir/agent/agent_spec.yaml" "$work/spec/agent_spec.yaml" \
  DATABASE="$db" SCHEMA="$target" WAREHOUSE="$wh"
snow stage copy "$work/spec/agent_spec.yaml" "$spec_dir" --overwrite "${ctx[@]}"

echo "== 4/6 import agent version"
version="$(scalar "CALL ${db}.OPS.DEPLOY_AGENT_VERSION('${target}', '${spec_dir}', 'ci ${sha} run ${run_id}')")"
echo "candidate version: ${version}"

echo "== 5/6 evaluation gate on ${version}"
"$recipe_dir/ci/scripts/render.sh" "$recipe_dir/evaluation/eval_config.yaml" "$work/eval/eval_config.yaml" \
  AGENT_FQN="${db}.${target}.RETAIL_ASSISTANT" AGENT_VERSION="$version" \
  RUN_DESCRIPTION="commit ${sha} run ${run_id}" DATABASE="$db"
snow stage copy "$work/eval/eval_config.yaml" "${config_path%/*}/" --overwrite "${ctx[@]}"
if ! sql "CALL ${db}.OPS.RUN_EVAL_GATE('${run_name}', '${config_path}', '${target}', ${min_ac}, ${min_lc}, 1800)"; then
  sql "SELECT run_name, run_status, scores, thresholds, records_errored, passed FROM ${db}.OPS.EVAL_GATE_RESULTS WHERE run_name = '${run_name}'" || true
  echo "Evaluation gate failed for ${target} ${version}. Nothing was promoted." >&2
  exit 1
fi

if [[ "$target" == "PROD" ]]; then
  echo "== 6/6 promote ${version}"
  sql "CALL ${db}.OPS.PROMOTE_AGENT_VERSION('PROD', '${version}')"
else
  echo "== 6/6 pull request build: nothing to promote"
fi

if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then
  {
    echo "### Agent deploy: ${target}"
    echo "- Version: \`${version}\`"
    echo "- Evaluation run: \`${run_name}\` (answer_correctness >= ${min_ac}, logical_consistency >= ${min_lc})"
  } >> "$GITHUB_STEP_SUMMARY"
fi
```

### `ci/scripts/render.sh`

Copy code

```
#!/usr/bin/env bash
# Render a template by replacing __KEY__ placeholders with values passed as KEY=value.
# Values are restricted to identifier-like characters so a branch name or PR title
# can never inject YAML or SQL.
#
# Usage: ci/scripts/render.sh <template> <output> KEY=value [KEY=value ...]
set -euo pipefail

template="$1"; output="$2"; shift 2
content="$(cat "$template")"
key_re='^[A-Z_]+$'
value_re='^[A-Za-z0-9_.$ -]+$'   # identifiers, VERSION$N, and short descriptions

for pair in "$@"; do
  key="${pair%%=*}"
  value="${pair#*=}"
  if [[ ! "$key" =~ $key_re ]]; then
    echo "render.sh: invalid key '$key'" >&2; exit 1
  fi
  if [[ ! "$value" =~ $value_re ]]; then
    echo "render.sh: value for $key contains unsupported characters" >&2; exit 1
  fi
  content="${content//__${key}__/$value}"
done

if grep -q '__[A-Z_]*__' <<<"$content"; then
  echo "render.sh: unreplaced placeholders in $template:" >&2
  grep -o '__[A-Z_]*__' <<<"$content" | sort -u >&2
  exit 1
fi

mkdir -p "$(dirname "$output")"
printf '%s\n' "$content" > "$output"
```

### `ci/workflows/agent-main.yml`

Copy code

```
# Main-branch workflow: rebuild PROD with dbt, import the merged agent spec as
# a new named version, run the evaluation gate against that version, and move
# the PRODUCTION alias only if the gate passes. If the gate fails, production
# keeps serving the previously promoted version.
#
# Copy to .github/workflows/ in your repository and set RECIPE_DIR to the path
# of this recipe folder.
name: Agent CD (main)

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  id-token: write

concurrency:
  group: agent-prod
  cancel-in-progress: false # never interrupt a production deploy midway

env:
  RECIPE_DIR: recipes/cortex-agents/agent-ci-cd-with-dbt
  SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}

jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment: snowflake-ci # must match the SUBJECT of the service user
    timeout-minutes: 60
    steps:
      - uses: actions/checkout@v7
        with:
          persist-credentials: false

      - uses: snowflakedb/snowflake-actions@v3
        with:
          use-oidc: true
          cli-version: "3.28.0"

      - name: Test the OIDC connection
        run: snow connection test -x

      - name: Build, deploy, gate, and promote PROD
        working-directory: ${{ env.RECIPE_DIR }}
        run: ci/scripts/deploy.sh PROD
```

### `ci/workflows/agent-pr.yml`

Copy code

```
# Pull request workflow: build the change into an isolated PR_<number> schema,
# import the agent spec as a new version, and fail the check if the evaluation
# gate fails. When the PR closes, drop everything the PR created.
#
# Copy to .github/workflows/ in your repository and set RECIPE_DIR to the path
# of this recipe folder. Authentication is GitHub OIDC (workload identity
# federation): no Snowflake password, key, or token is stored in GitHub.
name: Agent CI (pull request)

on:
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches: [main]

permissions:
  contents: read
  id-token: write # required to mint the OIDC token

concurrency:
  group: agent-pr-${{ github.event.pull_request.number }}
  cancel-in-progress: true

env:
  RECIPE_DIR: recipes/cortex-agents/agent-ci-cd-with-dbt
  SNOWFLAKE_ACCOUNT: ${{ secrets.SNOWFLAKE_ACCOUNT }}

jobs:
  build-and-gate:
    if: github.event.action != 'closed'
    runs-on: ubuntu-latest
    environment: snowflake-ci # must match the SUBJECT of the service user
    timeout-minutes: 60
    steps:
      - uses: actions/checkout@v7
        with:
          persist-credentials: false

      - uses: snowflakedb/snowflake-actions@v3
        with:
          use-oidc: true
          cli-version: "3.28.0"

      - name: Test the OIDC connection
        run: snow connection test -x

      - name: Build, deploy, and gate PR_${{ github.event.pull_request.number }}
        working-directory: ${{ env.RECIPE_DIR }}
        env:
          PR_NUMBER: ${{ github.event.pull_request.number }}
        run: ci/scripts/deploy.sh "PR_${PR_NUMBER}"

  cleanup:
    if: github.event.action == 'closed'
    runs-on: ubuntu-latest
    environment: snowflake-ci
    steps:
      - uses: actions/checkout@v7
        with:
          persist-credentials: false

      - uses: snowflakedb/snowflake-actions@v3
        with:
          use-oidc: true
          cli-version: "3.28.0"

      - name: Drop PR_${{ github.event.pull_request.number }} objects
        working-directory: ${{ env.RECIPE_DIR }}
        env:
          PR_NUMBER: ${{ github.event.pull_request.number }}
        run: ci/scripts/cleanup_pr.sh "PR_${PR_NUMBER}"
```

## `dbt/`

### `dbt/dbt_project.yml`

Copy code

```
name: retail_agent
version: "1.0.0"
config-version: 2
profile: retail_agent

model-paths: ["models"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
test-paths: ["tests"]

clean-targets:
  - target
  - dbt_packages

# Every node lands in one schema per environment: PROD for main, PR_<number> for
# a pull request. The schema comes from the deploy_schema var (see
# macros/generate_schema_name.sql), so the same project serves every environment.
vars:
  deploy_schema: PROD

seeds:
  retail_agent:
    +quote_columns: false

models:
  retail_agent:
    staging:
      +materialized: view
    marts:
      +materialized: table
    semantic:
      +materialized: semantic_view
```

### `dbt/macros/generate_schema_name.sql`

Copy code

```
{#-
  Route every node to one schema per environment.
  CI passes --vars '{"deploy_schema": "PR_42"}'; main uses the PROD default.
  The value is validated so a malformed var cannot become an arbitrary identifier.
-#}
{% macro generate_schema_name(custom_schema_name, node) -%}
    {%- set schema = var('deploy_schema', target.schema) | string | upper -%}
    {%- if not modules.re.match('^(PROD|PR_[0-9]{1,6})$', schema) -%}
        {{ exceptions.raise_compiler_error("deploy_schema must be PROD or PR_<number>, got: " ~ schema) }}
    {%- endif -%}
    {{ schema }}
{%- endmacro %}
```

### `dbt/macros/semantic_view.sql`

Copy code

```
{#-
  Minimal semantic view materialization. The model body is the semantic view
  DDL body (TABLES ... METRICS ... COMMENT). CREATE OR ALTER keeps grants on the
  semantic view across runs, which CREATE OR REPLACE would drop.

  The Snowflake-Labs dbt_semantic_view package provides a fuller version of
  this materialization; it needs an external access integration so that
  dbt deps can download it inside Snowflake. This recipe avoids that.
-#}
{% materialization semantic_view, adapter='snowflake' %}
    {%- set target_relation = api.Relation.create(
        database=this.database, schema=this.schema, identifier=this.identifier, type='view') -%}

    {{ run_hooks(pre_hooks) }}

    {% call statement('main') -%}
        CREATE OR ALTER SEMANTIC VIEW {{ target_relation }}
        {{ sql }}
    {%- endcall %}

    {{ run_hooks(post_hooks) }}

    {{ return({'relations': [target_relation]}) }}
{% endmaterialization %}
```

### `dbt/models/marts/dim_customers.sql`

Copy code

```
select
    customer_id,
    customer_name,
    email,
    city,
    state,
    country,
    customer_created_date
from {{ ref('stg_customers') }}
```

### `dbt/models/marts/dim_products.sql`

Copy code

```
select
    product_id,
    product_name,
    category,
    subcategory,
    unit_price
from {{ ref('stg_products') }}
```

### `dbt/models/marts/fct_order_lines.sql`

Copy code

```
-- One row per order line: the grain for product and category revenue.
select
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    discount_amount,
    line_total
from {{ ref('stg_order_items') }}
```

### `dbt/models/marts/fct_orders.sql`

Copy code

```
-- One row per order. Totals are pre-aggregated from line items so order-level
-- metrics never fan out when joined to lines.
with line_totals as (
    select
        order_id,
        sum(quantity) as total_quantity,
        sum(line_total) as order_total,
        sum(discount_amount) as total_discount
    from {{ ref('stg_order_items') }}
    group by order_id
)

select
    o.order_id,
    o.customer_id,
    o.order_date,
    o.order_status,
    o.shipping_address_state,
    coalesce(l.total_quantity, 0) as total_quantity,
    coalesce(l.order_total, 0) as order_total,
    coalesce(l.total_discount, 0) as total_discount
from {{ ref('stg_orders') }} o
left join line_totals l on o.order_id = l.order_id
```

### `dbt/models/marts/schema.yml`

Copy code

```
version: 2

models:
  - name: dim_customers
    description: "One row per customer."
    columns:
      - name: customer_id
        data_tests: [unique, not_null]
  - name: dim_products
    description: "One row per product."
    columns:
      - name: product_id
        data_tests: [unique, not_null]
  - name: fct_orders
    description: "One row per order, with totals rolled up from order lines."
    columns:
      - name: order_id
        data_tests: [unique, not_null]
      - name: customer_id
        data_tests:
          - not_null
          - relationships:
              arguments:
                to: ref('dim_customers')
                field: customer_id
  - name: fct_order_lines
    description: "One row per order line."
    columns:
      - name: order_item_id
        data_tests: [unique, not_null]
      - name: product_id
        data_tests:
          - relationships:
              arguments:
                to: ref('dim_products')
                field: product_id
```

### `dbt/models/semantic/retail_analytics.sql`

Copy code

```
-- Body of CREATE OR ALTER SEMANTIC VIEW (see macros/semantic_view.sql).
-- ref() resolves to the tables dbt built in this environment's schema and
-- orders this model after them in the DAG.
TABLES (
    customers AS {{ ref('dim_customers') }} PRIMARY KEY (customer_id)
        COMMENT = 'One row per customer',
    products AS {{ ref('dim_products') }} PRIMARY KEY (product_id)
        COMMENT = 'One row per product',
    orders AS {{ ref('fct_orders') }} PRIMARY KEY (order_id)
        COMMENT = 'One row per order; totals already rolled up from lines',
    order_lines AS {{ ref('fct_order_lines') }} PRIMARY KEY (order_item_id)
        COMMENT = 'One row per order line; use for product and category revenue'
)
RELATIONSHIPS (
    orders_to_customers AS orders (customer_id) REFERENCES customers (customer_id),
    lines_to_orders AS order_lines (order_id) REFERENCES orders (order_id),
    lines_to_products AS order_lines (product_id) REFERENCES products (product_id)
)
FACTS (
    orders.order_total AS order_total COMMENT = 'Order amount after discounts',
    order_lines.line_total AS line_total COMMENT = 'Line amount after discounts',
    order_lines.quantity AS quantity COMMENT = 'Units on the line'
)
DIMENSIONS (
    customers.customer_name AS customer_name
        WITH SYNONYMS = ('customer', 'buyer') COMMENT = 'Customer full name',
    customers.customer_state AS state COMMENT = 'Two-letter US state of the customer',
    customers.customer_city AS city COMMENT = 'Customer city',
    products.product_name AS product_name
        WITH SYNONYMS = ('product', 'item') COMMENT = 'Product name',
    products.category AS category
        WITH SYNONYMS = ('product category', 'department') COMMENT = 'Product category',
    orders.order_date AS order_date COMMENT = 'Date the order was placed',
    orders.order_month AS DATE_TRUNC('month', order_date) COMMENT = 'First day of the order month',
    orders.order_status AS order_status
        COMMENT = 'Order status: completed, shipped, processing, or cancelled'
)
METRICS (
    orders.total_orders AS COUNT(orders.order_id)
        WITH SYNONYMS = ('order count', 'number of orders') COMMENT = 'Number of orders',
    orders.total_revenue AS SUM(orders.order_total)
        WITH SYNONYMS = ('revenue', 'sales') COMMENT = 'Sum of order totals after discounts',
    orders.average_order_value AS AVG(orders.order_total)
        WITH SYNONYMS = ('AOV') COMMENT = 'Average order total after discounts',
    order_lines.product_revenue AS SUM(order_lines.line_total)
        COMMENT = 'Revenue at line grain; use when grouping by product or category',
    order_lines.units_sold AS SUM(order_lines.quantity)
        WITH SYNONYMS = ('units', 'items sold') COMMENT = 'Units sold',
    customers.customer_count AS COUNT(customers.customer_id)
        COMMENT = 'Number of customers'
)
COMMENT = 'Retail orders, customers, and products for the retail assistant agent'
```

### `dbt/models/staging/schema.yml`

Copy code

```
version: 2

models:
  - name: stg_customers
    columns:
      - name: customer_id
        data_tests: [unique, not_null]
  - name: stg_orders
    columns:
      - name: order_id
        data_tests: [unique, not_null]
      - name: order_status
        data_tests:
          - accepted_values:
              arguments:
                values: ["completed", "shipped", "processing", "cancelled"]
  - name: stg_products
    columns:
      - name: product_id
        data_tests: [unique, not_null]
  - name: stg_order_items
    columns:
      - name: order_item_id
        data_tests: [unique, not_null]
```

### `dbt/models/staging/stg_customers.sql`

Copy code

```
select
    customer_id,
    first_name || ' ' || last_name as customer_name,
    email,
    city,
    state,
    country,
    created_at::date as customer_created_date
from {{ ref('raw_customers') }}
```

### `dbt/models/staging/stg_order_items.sql`

Copy code

```
select
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price::number(10, 2) as unit_price,
    discount_amount::number(10, 2) as discount_amount,
    (quantity * unit_price::number(10, 2)) - discount_amount::number(10, 2) as line_total
from {{ ref('raw_order_items') }}
```

### `dbt/models/staging/stg_orders.sql`

Copy code

```
select
    order_id,
    customer_id,
    order_date::date as order_date,
    status as order_status,
    shipping_address_city,
    shipping_address_state
from {{ ref('raw_orders') }}
```

### `dbt/models/staging/stg_products.sql`

Copy code

```
select
    product_id,
    product_name,
    category,
    subcategory,
    unit_price::number(10, 2) as unit_price
from {{ ref('raw_products') }}
```

### `dbt/profiles.yml`

Copy code

```
# Profile for dbt Projects on Snowflake. The dbt project object runs inside a
# Snowflake session, so account and user are placeholders and no credential
# fields are allowed. The schema here is only a fallback: generate_schema_name
# routes every node to var('deploy_schema').
retail_agent:
  target: ci
  outputs:
    ci:
      type: snowflake
      account: "_"
      user: "_"
      role: COOKBOOK_AGENT_CI_CD_WITH_DBT_DEPLOYER
      warehouse: COOKBOOK_AGENT_CI_CD_WITH_DBT_WH
      database: COOKBOOK_AGENT_CI_CD_WITH_DBT
      schema: PROD
      threads: 8
```

### `dbt/seeds/raw_customers.csv`

```
customer_id,first_name,last_name,email,city,state,country,created_at
1,James,Wilson,james.wilson@example.com,Austin,TX,US,2022-03-15
2,Sarah,Chen,sarah.chen@example.com,Seattle,WA,US,2022-04-22
3,Michael,Johnson,michael.johnson@example.com,Denver,CO,US,2022-06-10
4,Emily,Davis,emily.davis@example.com,Portland,OR,US,2022-07-18
5,Robert,Martinez,robert.martinez@example.com,Chicago,IL,US,2022-08-05
6,Jessica,Thompson,jessica.thompson@example.com,Nashville,TN,US,2022-09-12
7,David,Anderson,david.anderson@example.com,San Francisco,CA,US,2022-10-30
8,Amanda,Garcia,amanda.garcia@example.com,Miami,FL,US,2022-11-14
9,Christopher,Lee,christopher.lee@example.com,Boston,MA,US,2023-01-08
10,Lauren,Robinson,lauren.robinson@example.com,Phoenix,AZ,US,2023-02-20
11,Daniel,Harris,daniel.harris@example.com,Atlanta,GA,US,2023-03-17
12,Rachel,Clark,rachel.clark@example.com,Minneapolis,MN,US,2023-04-25
13,Andrew,Lewis,andrew.lewis@example.com,San Diego,CA,US,2023-05-11
14,Megan,Walker,megan.walker@example.com,Dallas,TX,US,2023-06-29
15,Joshua,Hall,joshua.hall@example.com,Philadelphia,PA,US,2023-07-15
16,Stephanie,Allen,stephanie.allen@example.com,Charlotte,NC,US,2023-08-22
17,Kevin,Young,kevin.young@example.com,Detroit,MI,US,2023-09-10
18,Nicole,King,nicole.king@example.com,Salt Lake City,UT,US,2023-10-05
19,Brian,Wright,brian.wright@example.com,Las Vegas,NV,US,2023-11-18
20,Ashley,Scott,ashley.scott@example.com,Raleigh,NC,US,2024-01-07
21,Matthew,Green,matthew.green@example.com,Columbus,OH,US,2024-02-14
22,Jennifer,Adams,jennifer.adams@example.com,Indianapolis,IN,US,2024-03-03
23,Ryan,Nelson,ryan.nelson@example.com,Tampa,FL,US,2024-04-11
24,Samantha,Hill,samantha.hill@example.com,Kansas City,MO,US,2024-05-19
25,Tyler,Moore,tyler.moore@example.com,San Antonio,TX,US,2024-06-01
```

### `dbt/seeds/raw_order_items.csv`

```
order_item_id,order_id,product_id,quantity,unit_price,discount_amount
1,1,1,1,79.99,0.00
2,1,4,1,149.99,15.00
3,2,2,1,129.99,0.00
4,2,7,2,39.99,8.00
5,3,3,2,34.99,7.00
6,3,12,1,24.99,0.00
7,4,5,1,45.99,0.00
8,4,10,2,28.99,5.80
9,5,6,3,14.99,4.50
10,5,16,1,18.99,0.00
11,6,9,1,59.99,6.00
12,6,13,1,34.99,3.50
13,7,17,1,99.99,10.00
14,7,11,2,29.99,6.00
15,8,14,1,199.99,20.00
16,8,18,1,54.99,5.50
17,9,20,2,49.99,10.00
18,9,15,1,42.99,0.00
19,10,8,1,89.99,9.00
20,10,3,1,34.99,0.00
21,11,1,1,79.99,8.00
22,11,9,1,59.99,0.00
23,12,2,1,129.99,13.00
24,12,19,2,22.99,4.60
25,13,4,1,149.99,0.00
26,13,15,1,42.99,4.30
27,14,17,1,99.99,10.00
28,14,13,2,34.99,7.00
29,15,6,2,14.99,3.00
30,15,12,1,24.99,2.50
31,16,5,2,45.99,9.20
32,16,10,1,28.99,0.00
33,17,14,1,199.99,20.00
34,17,8,1,89.99,9.00
35,18,20,1,49.99,5.00
36,18,11,3,29.99,9.00
37,19,7,1,39.99,4.00
38,19,19,2,22.99,0.00
39,20,1,2,79.99,16.00
40,20,4,1,149.99,0.00
41,21,3,3,34.99,10.50
42,21,18,1,54.99,5.50
43,22,16,2,18.99,3.80
44,22,6,1,14.99,0.00
45,23,9,1,59.99,0.00
46,23,17,1,99.99,10.00
47,24,2,1,129.99,13.00
48,24,7,1,39.99,4.00
49,25,15,2,42.99,8.60
50,25,5,1,45.99,4.60
51,26,20,1,49.99,5.00
52,26,13,1,34.99,0.00
53,27,14,1,199.99,0.00
54,27,8,1,89.99,9.00
55,28,11,2,29.99,6.00
56,28,19,1,22.99,0.00
57,29,1,1,79.99,8.00
58,29,4,1,149.99,15.00
59,30,12,2,24.99,5.00
60,30,16,1,18.99,0.00
61,31,17,1,99.99,0.00
62,31,9,2,59.99,12.00
63,32,3,1,34.99,3.50
64,32,18,2,54.99,11.00
65,33,5,1,45.99,0.00
66,33,10,3,28.99,8.70
67,34,2,1,129.99,13.00
68,34,7,2,39.99,8.00
69,35,20,1,49.99,0.00
70,35,15,1,42.99,4.30
71,36,6,2,14.99,0.00
72,36,12,1,24.99,2.50
73,37,4,1,149.99,15.00
74,37,1,1,79.99,8.00
75,38,14,1,199.99,20.00
76,38,8,1,89.99,0.00
77,39,11,1,29.99,3.00
78,39,19,3,22.99,6.90
79,40,13,2,34.99,7.00
80,40,9,1,59.99,6.00
81,41,17,1,99.99,10.00
82,41,2,1,129.99,0.00
83,42,3,2,34.99,7.00
84,42,18,1,54.99,5.50
85,43,5,1,45.99,4.60
86,43,10,1,28.99,0.00
87,44,20,2,49.99,10.00
88,44,15,1,42.99,0.00
89,45,7,2,39.99,8.00
90,45,19,1,22.99,0.00
91,46,1,1,79.99,0.00
92,46,4,1,149.99,15.00
93,47,16,3,18.99,5.70
94,47,6,2,14.99,3.00
95,48,9,1,59.99,6.00
96,48,13,1,34.99,0.00
97,49,14,1,199.99,20.00
98,49,8,1,89.99,9.00
99,50,17,1,99.99,10.00
100,50,11,2,29.99,6.00
```

### `dbt/seeds/raw_orders.csv`

```
order_id,customer_id,order_date,status,shipping_address_city,shipping_address_state
1,3,2023-01-05,completed,San Francisco,CA
2,1,2023-01-18,completed,Austin,TX
3,7,2023-02-02,completed,Nashville,TN
4,5,2023-02-14,completed,Chicago,IL
5,12,2023-02-28,completed,Atlanta,GA
6,2,2023-03-10,completed,Portland,OR
7,9,2023-03-22,completed,Boston,MA
8,4,2023-04-05,completed,Denver,CO
9,14,2023-04-19,completed,Dallas,TX
10,6,2023-05-01,completed,Seattle,WA
11,10,2023-05-15,completed,Phoenix,AZ
12,8,2023-06-02,completed,Miami,FL
13,17,2023-06-18,completed,Columbus,OH
14,3,2023-07-04,completed,San Francisco,CA
15,11,2023-07-20,completed,Minneapolis,MN
16,1,2023-08-03,completed,Austin,TX
17,15,2023-08-19,completed,Philadelphia,PA
18,13,2023-09-01,completed,San Diego,CA
19,5,2023-09-15,shipped,Chicago,IL
20,21,2023-09-29,completed,Sacramento,CA
21,7,2023-10-12,completed,Nashville,TN
22,16,2023-10-26,completed,Charlotte,NC
23,2,2023-11-08,completed,Portland,OR
24,19,2023-11-22,shipped,Salt Lake City,UT
25,23,2023-12-05,completed,Indianapolis,IN
26,4,2023-12-18,completed,Denver,CO
27,20,2024-01-10,completed,Raleigh,NC
28,12,2024-01-24,completed,Atlanta,GA
29,6,2024-02-07,shipped,Seattle,WA
30,22,2024-02-21,completed,Las Vegas,NV
31,9,2024-03-06,completed,Boston,MA
32,18,2024-03-20,processing,Detroit,MI
33,14,2024-04-03,completed,Dallas,TX
34,8,2024-04-17,completed,Miami,FL
35,25,2024-05-01,processing,Kansas City,MO
36,11,2024-05-15,completed,Minneapolis,MN
37,3,2024-06-01,shipped,San Francisco,CA
38,24,2024-06-15,processing,Tampa,FL
39,1,2024-07-01,completed,Austin,TX
40,16,2024-07-15,shipped,Charlotte,NC
41,5,2024-08-01,processing,Chicago,IL
42,21,2024-08-15,completed,Sacramento,CA
43,7,2024-09-01,cancelled,Nashville,TN
44,13,2024-09-15,shipped,San Diego,CA
45,19,2024-10-01,processing,Salt Lake City,UT
46,2,2024-10-15,completed,Portland,OR
47,10,2024-11-01,shipped,Phoenix,AZ
48,15,2024-11-15,cancelled,Philadelphia,PA
49,22,2024-12-01,processing,Las Vegas,NV
50,4,2024-12-15,shipped,Denver,CO
```

### `dbt/seeds/raw_products.csv`

```
product_id,product_name,category,subcategory,unit_price,created_at
1,Wireless Bluetooth Headphones,Electronics,Audio,79.99,2022-01-15
2,Cotton Crew Neck T-Shirt,Clothing,Tops,24.99,2022-02-10
3,Stainless Steel Water Bottle,Sports,Accessories,34.99,2022-03-05
4,LED Desk Lamp,Home & Garden,Lighting,45.99,2022-03-20
5,Running Shoes Pro,Sports,Footwear,129.99,2022-04-12
6,Organic Coffee Beans 1lb,Home & Garden,Kitchen,18.99,2022-05-01
7,Laptop Stand Adjustable,Electronics,Accessories,59.99,2022-06-15
8,Yoga Mat Premium,Sports,Fitness,39.99,2022-07-22
9,Mystery Novel Collection,Books,Fiction,14.99,2022-08-10
10,Wireless Mouse,Electronics,Peripherals,29.99,2022-09-05
11,Winter Parka Jacket,Clothing,Outerwear,189.99,2022-10-18
12,Smart Watch Series 5,Electronics,Wearables,299.99,2022-11-01
13,Garden Tool Set,Home & Garden,Outdoor,54.99,2023-01-12
14,Programming Handbook,Books,Technical,49.99,2023-02-20
15,Denim Jeans Slim Fit,Clothing,Bottoms,64.99,2023-03-15
16,Portable Bluetooth Speaker,Electronics,Audio,89.99,2023-04-08
17,Indoor Plant Pot Set,Home & Garden,Decor,32.99,2023-05-22
18,Basketball Official Size,Sports,Equipment,27.99,2023-06-30
19,Science Fiction Anthology,Books,Fiction,12.99,2023-08-14
20,4K Webcam HD,Electronics,Peripherals,149.99,2023-09-25
```

## `evaluation/`

### `evaluation/eval_config.yaml`

Copy code

```
# Evaluation config template. ci/scripts/render.sh fills in the agent and version
# for each run. There is no `dataset:` block on purpose: 03_eval_dataset.sql
# creates the dataset once, and a `dataset:` block would try to recreate it on
# every START and fail once it exists.
evaluation:
  agent_params:
    agent_name: "__AGENT_FQN__"
    agent_type: "CORTEX AGENT"
    agent_version: "__AGENT_VERSION__"
  run_params:
    label: "ci-gate"
    description: "__RUN_DESCRIPTION__"
  source_metadata:
    type: "dataset"
    dataset_name: "__DATABASE__.OPS.RETAIL_EVAL_DATASET"

# Pin metric versions. Scores from different metric versions are not comparable,
# and unpinned metrics roll forward when a judge model is deprecated.
metrics:
  - name: "answer_correctness"
    version: "v3"
  - name: "logical_consistency"
    version: "v3"
```

## `sql/`

### `sql/01_setup.sql`

Copy code

```
-- 01_setup.sql
-- Creates the roles, warehouse, database, schemas, and stages the pipeline uses.
-- Run once as ACCOUNTADMIN (or a role with CREATE ROLE, CREATE DATABASE,
-- CREATE WAREHOUSE, and MANAGE GRANTS). Everything after this runs as the
-- COOKBOOK_AGENT_CI_CD_WITH_DBT_DEPLOYER role.

SET cookbook_db       = 'COOKBOOK_AGENT_CI_CD_WITH_DBT';
SET cookbook_wh       = 'COOKBOOK_AGENT_CI_CD_WITH_DBT_WH';
SET deployer_role     = 'COOKBOOK_AGENT_CI_CD_WITH_DBT_DEPLOYER';  -- CI/CD service role
SET consumer_role     = 'COOKBOOK_AGENT_CI_CD_WITH_DBT_USER';      -- people who chat with the prod agent
SET ops_schema        = 'COOKBOOK_AGENT_CI_CD_WITH_DBT.OPS';
SET prod_schema       = 'COOKBOOK_AGENT_CI_CD_WITH_DBT.PROD';
SET me                = '"' || CURRENT_USER() || '"';

USE ROLE ACCOUNTADMIN;

-- Roles ----------------------------------------------------------------------
CREATE ROLE IF NOT EXISTS IDENTIFIER($deployer_role)
  COMMENT = 'Cookbook agent-ci-cd-with-dbt: CI/CD deployer';
CREATE ROLE IF NOT EXISTS IDENTIFIER($consumer_role)
  COMMENT = 'Cookbook agent-ci-cd-with-dbt: uses the production agent';
GRANT ROLE IDENTIFIER($deployer_role) TO ROLE SYSADMIN;
GRANT ROLE IDENTIFIER($consumer_role) TO ROLE SYSADMIN;
GRANT ROLE IDENTIFIER($deployer_role) TO USER IDENTIFIER($me);
GRANT ROLE IDENTIFIER($consumer_role) TO USER IDENTIFIER($me);

-- Warehouse ------------------------------------------------------------------
CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
  WAREHOUSE_SIZE = XSMALL AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE;
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($deployer_role);
GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($consumer_role);

-- Database and schemas -------------------------------------------------------
-- OPS holds pipeline plumbing (dbt project objects, stages, eval dataset, gate
-- procedures). PROD holds the production tables, semantic view, and agent.
-- Each pull request gets its own PR_<number> schema, created and dropped by CI.
CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db);
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($ops_schema);
CREATE SCHEMA IF NOT EXISTS IDENTIFIER($prod_schema);
GRANT OWNERSHIP ON SCHEMA IDENTIFIER($ops_schema) TO ROLE IDENTIFIER($deployer_role) COPY CURRENT GRANTS;
GRANT OWNERSHIP ON SCHEMA IDENTIFIER($prod_schema) TO ROLE IDENTIFIER($deployer_role) COPY CURRENT GRANTS;
GRANT OWNERSHIP ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($deployer_role) COPY CURRENT GRANTS;

-- Cortex and evaluation privileges for the deployer --------------------------
-- Evaluations need CORTEX_USER and EXECUTE TASK (runs are managed by tasks).
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE IDENTIFIER($deployer_role);
GRANT EXECUTE TASK ON ACCOUNT TO ROLE IDENTIFIER($deployer_role);

-- Consumer access to production only -----------------------------------------
-- CORTEX_AGENT_USER is enough to chat with an agent; CORTEX_USER also works.
-- Future grants apply to the semantic view and agent the pipeline creates later.
-- Because the pipeline adds versions to one agent object (it never replaces it),
-- these grants survive every deployment.
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_AGENT_USER TO ROLE IDENTIFIER($consumer_role);
GRANT USAGE ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($consumer_role);
GRANT USAGE ON SCHEMA IDENTIFIER($prod_schema) TO ROLE IDENTIFIER($consumer_role);
GRANT SELECT ON FUTURE SEMANTIC VIEWS IN SCHEMA IDENTIFIER($prod_schema) TO ROLE IDENTIFIER($consumer_role);
GRANT USAGE ON FUTURE AGENTS IN SCHEMA IDENTIFIER($prod_schema) TO ROLE IDENTIFIER($consumer_role);
-- Cortex Analyst runs the SQL it generates against the semantic view's base
-- tables with the caller's role, so the consumer also needs SELECT on them.
-- dbt recreates the mart tables on every build; the future grant applies to
-- each new table, and the ALL grant covers tables that exist when 01 is rerun.
GRANT SELECT ON FUTURE TABLES IN SCHEMA IDENTIFIER($prod_schema) TO ROLE IDENTIFIER($consumer_role);
GRANT SELECT ON ALL TABLES IN SCHEMA IDENTIFIER($prod_schema) TO ROLE IDENTIFIER($consumer_role);

-- Pipeline plumbing, owned by the deployer ------------------------------------
USE ROLE IDENTIFIER($deployer_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($ops_schema);

-- Evaluation configs must be read as single-column text, so the stage uses a
-- CSV format with FIELD_DELIMITER = NONE.
CREATE FILE FORMAT IF NOT EXISTS YAML_FILE_FORMAT
  TYPE = 'CSV'
  FIELD_DELIMITER = NONE
  RECORD_DELIMITER = '\n'
  SKIP_HEADER = 0
  FIELD_OPTIONALLY_ENCLOSED_BY = NONE
  ESCAPE_UNENCLOSED_FIELD = NONE;

-- CREATE AGENT ... FROM @stage and ADD VERSION FROM @stage read agent_spec.yaml
-- server-side; with the default client-side encryption they fail with
-- "No spec file present for the agent". Use server-side encryption.
CREATE STAGE IF NOT EXISTS AGENT_SPECS
  ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
  DIRECTORY = (ENABLE = TRUE)
  COMMENT = 'Rendered agent_spec.yaml files, one directory per deployment';
CREATE STAGE IF NOT EXISTS EVAL_CONFIGS
  FILE_FORMAT = YAML_FILE_FORMAT
  COMMENT = 'Rendered evaluation configs, one directory per deployment';

SHOW SCHEMAS IN DATABASE IDENTIFIER($cookbook_db);
```

### `sql/02_pipeline_procedures.sql`

Copy code

```
-- 02_pipeline_procedures.sql
-- Three caller's-rights procedures that the CI script calls, plus a results log.
--   DEPLOY_AGENT_VERSION  import a spec directory from the AGENT_SPECS stage as a new named version
--   RUN_EVAL_GATE         run an evaluation, wait for it, and raise an error if scores are below threshold
--   PROMOTE_AGENT_VERSION move the PRODUCTION alias and the default version to a gated version
--
-- These procedures build DDL from their inputs (agent and stage names cannot be
-- bind variables), so every input is checked against a strict pattern first.
-- They run with caller's rights: the CI role needs the privileges, not the
-- procedure owner. Run as the deployer role after 01_setup.sql.

SET cookbook_wh   = 'COOKBOOK_AGENT_CI_CD_WITH_DBT_WH';
SET deployer_role = 'COOKBOOK_AGENT_CI_CD_WITH_DBT_DEPLOYER';
SET ops_schema    = 'COOKBOOK_AGENT_CI_CD_WITH_DBT.OPS';

USE ROLE IDENTIFIER($deployer_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($ops_schema);

-- One row per gate decision, pass or fail. Use it to learn the normal score
-- range for your dataset before you tighten thresholds.
CREATE TABLE IF NOT EXISTS EVAL_GATE_RESULTS (
    evaluated_at      TIMESTAMP_LTZ DEFAULT CURRENT_TIMESTAMP(),
    run_name          VARCHAR,
    target_schema     VARCHAR,
    run_status        VARCHAR,
    scores            VARIANT,
    thresholds        VARIANT,
    records_evaluated INTEGER,
    records_errored   INTEGER,
    passed            BOOLEAN
);

CREATE OR REPLACE PROCEDURE DEPLOY_AGENT_VERSION(
    TARGET_SCHEMA VARCHAR, SPEC_DIR VARCHAR, VERSION_COMMENT VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = 'Create the agent from a staged spec, or add a named version from it. Returns the new version name.'
EXECUTE AS CALLER
AS
$$
DECLARE
    spec_prefix VARCHAR;
    agent_fqn   VARCHAR;
    agent_count INTEGER;
    live_count  INTEGER;
    new_version VARCHAR;
    bad_input   EXCEPTION (-20001, 'DEPLOY_AGENT_VERSION: invalid TARGET_SCHEMA, SPEC_DIR, or VERSION_COMMENT');
BEGIN
    spec_prefix := '@' || CURRENT_DATABASE() || '.OPS.AGENT_SPECS/';
    IF (NOT REGEXP_LIKE(TARGET_SCHEMA, '^(PROD|PR_[0-9]{1,6})$')
        OR NOT STARTSWITH(SPEC_DIR, spec_prefix)
        OR NOT REGEXP_LIKE(SUBSTR(SPEC_DIR, LENGTH(spec_prefix) + 1), '^[A-Za-z0-9_-]+(/[A-Za-z0-9_-]+)*/$')
        OR NOT REGEXP_LIKE(VERSION_COMMENT, '^[A-Za-z0-9 _.-]{1,200}$')) THEN
        RAISE bad_input;
    END IF;
    agent_fqn := CURRENT_DATABASE() || '.' || TARGET_SCHEMA || '.RETAIL_ASSISTANT';

    EXECUTE IMMEDIATE 'SHOW AGENTS LIKE ''RETAIL_ASSISTANT'' IN SCHEMA ' || CURRENT_DATABASE() || '.' || TARGET_SCHEMA;
    SELECT COUNT(*) INTO :agent_count FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));

    IF (agent_count = 0) THEN
        -- First deployment: creates VERSION$1 plus a LIVE version from the spec.
        EXECUTE IMMEDIATE 'CREATE AGENT ' || agent_fqn
            || ' COMMENT = ''Retail assistant. Versions are imported by CI; do not edit in place.'''
            || ' FROM ' || SPEC_DIR;
    ELSE
        -- ADD VERSION FROM a stage fails while a LIVE version exists. Commit it
        -- first so any Snowsight edits are preserved as a named version. That
        -- version is never promoted: only versions imported from Git are.
        EXECUTE IMMEDIATE 'SHOW VERSIONS IN AGENT ' || agent_fqn;
        SELECT COUNT(*) INTO :live_count FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
            WHERE "spec_file_path" ILIKE '%/versions/live/';
        IF (live_count > 0) THEN
            EXECUTE IMMEDIATE 'ALTER AGENT ' || agent_fqn
                || ' COMMIT COMMENT = ''Live version committed by CI before import; not promoted''';
        END IF;
        EXECUTE IMMEDIATE 'ALTER AGENT ' || agent_fqn || ' ADD VERSION FROM ' || SPEC_DIR
            || ' COMMENT = ''' || VERSION_COMMENT || '''';
    END IF;

    EXECUTE IMMEDIATE 'SHOW VERSIONS IN AGENT ' || agent_fqn;
    SELECT 'VERSION$' || MAX(TRY_TO_NUMBER(SPLIT_PART("name", '$', 2)))
        INTO :new_version
        FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()))
        WHERE "name" IS NOT NULL;
    RETURN new_version;
END;
$$;

CREATE OR REPLACE PROCEDURE RUN_EVAL_GATE(
    RUN_NAME VARCHAR, CONFIG_PATH VARCHAR, TARGET_SCHEMA VARCHAR,
    MIN_ANSWER_CORRECTNESS FLOAT, MIN_LOGICAL_CONSISTENCY FLOAT, TIMEOUT_SECONDS INTEGER)
RETURNS VARIANT
LANGUAGE SQL
COMMENT = 'Start an agent evaluation, wait for it, log scores, and raise if any score is below its threshold.'
EXECUTE AS CALLER
AS
$$
DECLARE
    config_prefix VARCHAR;
    run_status    VARCHAR DEFAULT 'CREATED';
    waited        INTEGER DEFAULT 0;
    partial_since INTEGER DEFAULT -1;
    scores        VARIANT;
    n_records     INTEGER;
    n_errors      INTEGER;
    ac            FLOAT;
    lc            FLOAT;
    passed        BOOLEAN;
    bad_input     EXCEPTION (-20001, 'RUN_EVAL_GATE: invalid RUN_NAME, CONFIG_PATH, or TARGET_SCHEMA');
    timed_out     EXCEPTION (-20002, 'RUN_EVAL_GATE: evaluation did not finish before TIMEOUT_SECONDS');
    gate_failed   EXCEPTION (-20003, 'RUN_EVAL_GATE: scores below threshold; see OPS.EVAL_GATE_RESULTS');
BEGIN
    config_prefix := '@' || CURRENT_DATABASE() || '.OPS.EVAL_CONFIGS/';
    IF (NOT REGEXP_LIKE(RUN_NAME, '^[A-Za-z0-9_-]{1,128}$')
        OR NOT REGEXP_LIKE(TARGET_SCHEMA, '^(PROD|PR_[0-9]{1,6})$')
        OR NOT STARTSWITH(CONFIG_PATH, config_prefix)
        OR NOT REGEXP_LIKE(SUBSTR(CONFIG_PATH, LENGTH(config_prefix) + 1), '^([A-Za-z0-9_-]+/)+[A-Za-z0-9_-]+[.]yaml$')) THEN
        RAISE bad_input;
    END IF;

    -- Evaluations run in the session's current database and schema (OPS).
    CALL EXECUTE_AI_EVALUATION('START', OBJECT_CONSTRUCT('run_name', :RUN_NAME), :CONFIG_PATH);

    LOOP
        CALL EXECUTE_AI_EVALUATION('STATUS', OBJECT_CONSTRUCT('run_name', :RUN_NAME), :CONFIG_PATH);
        SELECT "STATUS" INTO :run_status FROM TABLE(RESULT_SCAN(LAST_QUERY_ID()));
        IF (run_status IN ('COMPLETED', 'CANCELLED')) THEN
            BREAK;
        END IF;
        -- PARTIALLY_COMPLETED is documented as final, but a run can report it
        -- for a short time and then move to COMPLETED. Keep polling for up to
        -- 120 seconds before treating it as final; the gate still fails closed
        -- on anything but COMPLETED.
        IF (run_status = 'PARTIALLY_COMPLETED') THEN
            IF (partial_since < 0) THEN
                partial_since := waited;
            END IF;
            IF (waited - partial_since >= 120) THEN
                BREAK;
            END IF;
        ELSE
            partial_since := -1;
        END IF;
        IF (waited >= TIMEOUT_SECONDS) THEN
            RAISE timed_out;
        END IF;
        SELECT SYSTEM$WAIT(20);
        waited := waited + 20;
    END LOOP;

    -- Average each metric over all records. A record without a score (for
    -- example, an agent error) counts as 0 so failures cannot raise the average.
    SELECT OBJECT_AGG(metric_name, avg_score::VARIANT), MAX(n_records), MAX(n_errors)
      INTO :scores, :n_records, :n_errors
      FROM (
        SELECT METRIC_NAME AS metric_name,
               ROUND(AVG(COALESCE(EVAL_AGG_SCORE, 0)), 3) AS avg_score,
               COUNT(DISTINCT RECORD_ID) AS n_records,
               COUNT(DISTINCT IFF(ERROR IS NOT NULL AND ERROR <> '', RECORD_ID, NULL)) AS n_errors
          FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_EVALUATION_DATA(
                 CURRENT_DATABASE(), :TARGET_SCHEMA, 'RETAIL_ASSISTANT', 'CORTEX AGENT', :RUN_NAME))
         WHERE METRIC_NAME IS NOT NULL
         GROUP BY METRIC_NAME);

    ac := GET(scores, 'answer_correctness')::FLOAT;
    lc := GET(scores, 'logical_consistency')::FLOAT;
    -- Fail closed: a missing metric, a partial run, or a NULL comparison is a failure.
    passed := COALESCE(run_status = 'COMPLETED'
              AND ac IS NOT NULL AND ac >= MIN_ANSWER_CORRECTNESS
              AND lc IS NOT NULL AND lc >= MIN_LOGICAL_CONSISTENCY, FALSE);

    INSERT INTO EVAL_GATE_RESULTS
        (run_name, target_schema, run_status, scores, thresholds, records_evaluated, records_errored, passed)
    SELECT :RUN_NAME, :TARGET_SCHEMA, :run_status, :scores,
           OBJECT_CONSTRUCT('answer_correctness', :MIN_ANSWER_CORRECTNESS,
                            'logical_consistency', :MIN_LOGICAL_CONSISTENCY),
           :n_records, :n_errors, :passed;

    IF (NOT passed) THEN
        RAISE gate_failed;
    END IF;
    RETURN OBJECT_CONSTRUCT('run_name', RUN_NAME, 'status', run_status, 'scores', scores, 'passed', passed);
END;
$$;

CREATE OR REPLACE PROCEDURE PROMOTE_AGENT_VERSION(TARGET_SCHEMA VARCHAR, VERSION_NAME VARCHAR)
RETURNS VARCHAR
LANGUAGE SQL
COMMENT = 'Point the PRODUCTION alias and the default version at a gated version.'
EXECUTE AS CALLER
AS
$$
DECLARE
    agent_fqn VARCHAR;
    bad_input EXCEPTION (-20001, 'PROMOTE_AGENT_VERSION: invalid TARGET_SCHEMA or VERSION_NAME');
BEGIN
    IF (NOT REGEXP_LIKE(TARGET_SCHEMA, '^(PROD|PR_[0-9]{1,6})$')
        OR NOT REGEXP_LIKE(VERSION_NAME, '^VERSION[$][0-9]{1,6}$')) THEN
        RAISE bad_input;
    END IF;
    agent_fqn := CURRENT_DATABASE() || '.' || TARGET_SCHEMA || '.RETAIL_ASSISTANT';
    -- Reassigning an alias moves it off the previous version in one statement.
    EXECUTE IMMEDIATE 'ALTER AGENT ' || agent_fqn || ' MODIFY VERSION ' || VERSION_NAME || ' SET ALIAS = PRODUCTION';
    -- Pin the default so the next ADD VERSION does not become the default before it is gated.
    EXECUTE IMMEDIATE 'ALTER AGENT ' || agent_fqn || ' SET DEFAULT_VERSION = ''' || VERSION_NAME || '''';
    RETURN agent_fqn || ' PRODUCTION -> ' || VERSION_NAME;
END;
$$;

SHOW PROCEDURES IN SCHEMA IDENTIFIER($ops_schema);
```

### `sql/03_eval_dataset.sql`

Copy code

```
-- 03_eval_dataset.sql
-- Creates the evaluation input table and registers it as an evaluation dataset.
-- Every PR and every production deploy is scored against this same dataset, so
-- scores are comparable across runs. Ground truth states literal values from
-- the seed data and scopes each question to absolute dates so answers do not drift.
-- Run as the deployer role after 01_setup.sql.

SET cookbook_db   = 'COOKBOOK_AGENT_CI_CD_WITH_DBT';
SET cookbook_wh   = 'COOKBOOK_AGENT_CI_CD_WITH_DBT_WH';
SET deployer_role = 'COOKBOOK_AGENT_CI_CD_WITH_DBT_DEPLOYER';
SET ops_schema    = 'COOKBOOK_AGENT_CI_CD_WITH_DBT.OPS';

USE ROLE IDENTIFIER($deployer_role);
USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA IDENTIFIER($ops_schema);

CREATE OR REPLACE TABLE RETAIL_EVAL_QUESTIONS (
    input_query  VARCHAR,
    ground_truth VARIANT
);

INSERT INTO RETAIL_EVAL_QUESTIONS
SELECT column1, PARSE_JSON(column2) FROM VALUES
  ('What was total revenue across all orders?',
   '{"ground_truth_output": "Total revenue across all 50 orders is $7,144.03 after discounts. Rounding to the nearest dollar is acceptable."}'),
  ('How many orders were placed in September 2023, and what was their total revenue?',
   '{"ground_truth_output": "3 orders were placed between September 1 and September 30, 2023, with total revenue of $501.90."}'),
  ('Which product category had the highest revenue?',
   '{"ground_truth_output": "Home & Garden had the highest revenue at $1,756.71. Electronics was second at $1,554.59. The answer must name Home & Garden."}'),
  ('How many orders are in processing status?',
   '{"ground_truth_output": "6 orders have status processing."}'),
  ('What was total revenue for orders placed between January 1 and December 31, 2024?',
   '{"ground_truth_output": "Total revenue for orders placed in calendar year 2024 is $3,522.64 across 24 orders."}'),
  ('What will the weather be in Austin tomorrow?',
   '{"ground_truth_output": "The response should say that weather is outside the retail data the agent can access. It must not invent a forecast."}');

-- Recreate the dataset so this script stays idempotent. The dataset is a
-- snapshot of the table; rerun this script after you change the questions.
DROP DATASET IF EXISTS RETAIL_EVAL_DATASET;

CALL SYSTEM$CREATE_EVALUATION_DATASET(
  'Cortex Agent',
  'COOKBOOK_AGENT_CI_CD_WITH_DBT.OPS.RETAIL_EVAL_QUESTIONS',
  'COOKBOOK_AGENT_CI_CD_WITH_DBT.OPS.RETAIL_EVAL_DATASET',
  OBJECT_CONSTRUCT('query_text', 'INPUT_QUERY', 'expected_tools', 'GROUND_TRUTH')
);

SHOW DATASETS IN SCHEMA IDENTIFIER($ops_schema);
```

### `sql/04_ci_service_user.sql`

Copy code

```
-- 04_ci_service_user.sql
-- The GitHub Actions identity: a SERVICE user that authenticates with GitHub's
-- OIDC token (workload identity federation). No password, key pair, or PAT is
-- created, so there is no secret to store in GitHub or rotate.
--
-- SUBJECT must match the `sub` claim GitHub puts in the token exactly. Both
-- workflows run in the GitHub environment `snowflake-ci`, so one subject covers
-- pull requests and main. Replace example-org/example-repo with your repository.
-- Run as ACCOUNTADMIN or USERADMIN (CREATE USER).

SET ci_user        = 'COOKBOOK_AGENT_CI_CD_WITH_DBT_CI';
SET deployer_role  = 'COOKBOOK_AGENT_CI_CD_WITH_DBT_DEPLOYER';
SET cookbook_wh    = 'COOKBOOK_AGENT_CI_CD_WITH_DBT_WH';
SET github_subject = 'repo:example-org/example-repo:environment:snowflake-ci';

USE ROLE ACCOUNTADMIN;

CREATE USER IF NOT EXISTS IDENTIFIER($ci_user)
  TYPE = SERVICE
  WORKLOAD_IDENTITY = (
    TYPE = OIDC
    ISSUER = 'https://token.actions.githubusercontent.com'
    SUBJECT = $github_subject
  )
  DEFAULT_ROLE = $deployer_role
  DEFAULT_WAREHOUSE = $cookbook_wh
  COMMENT = 'Cookbook agent-ci-cd-with-dbt: GitHub Actions deployer (OIDC)';

-- DEFAULT_ROLE selects the role but does not grant it.
GRANT ROLE IDENTIFIER($deployer_role) TO USER IDENTIFIER($ci_user);

SHOW USER WORKLOAD IDENTITY AUTHENTICATION METHODS FOR USER IDENTIFIER($ci_user);
```

### `sql/99_teardown.sql`

Copy code

```
-- 99_teardown.sql
-- Removes everything this recipe created: the database (every schema, table,
-- semantic view, agent, dbt project object, stage, dataset, and procedure),
-- the warehouse, the CI service user, and both roles. Dropping the roles also
-- removes the account-level EXECUTE TASK grant made in 01_setup.sql.
-- No account parameters were changed, so there is nothing to restore.
-- Run as ACCOUNTADMIN.

SET cookbook_db   = 'COOKBOOK_AGENT_CI_CD_WITH_DBT';
SET cookbook_wh   = 'COOKBOOK_AGENT_CI_CD_WITH_DBT_WH';
SET deployer_role = 'COOKBOOK_AGENT_CI_CD_WITH_DBT_DEPLOYER';
SET consumer_role = 'COOKBOOK_AGENT_CI_CD_WITH_DBT_USER';
SET ci_user       = 'COOKBOOK_AGENT_CI_CD_WITH_DBT_CI';

USE ROLE ACCOUNTADMIN;

DROP DATABASE IF EXISTS IDENTIFIER($cookbook_db);
DROP WAREHOUSE IF EXISTS IDENTIFIER($cookbook_wh);
DROP USER IF EXISTS IDENTIFIER($ci_user);
DROP ROLE IF EXISTS IDENTIFIER($consumer_role);
DROP ROLE IF EXISTS IDENTIFIER($deployer_role);

SHOW DATABASES LIKE 'COOKBOOK_AGENT_CI_CD_WITH_DBT%';
SHOW WAREHOUSES LIKE 'COOKBOOK_AGENT_CI_CD_WITH_DBT%';
SHOW ROLES LIKE 'COOKBOOK_AGENT_CI_CD_WITH_DBT%';
SHOW USERS LIKE 'COOKBOOK_AGENT_CI_CD_WITH_DBT%';
```

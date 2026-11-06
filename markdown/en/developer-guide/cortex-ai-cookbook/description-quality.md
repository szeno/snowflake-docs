# Semantic view description quality: a rubric, a linter, and how to apply fixes

Grade semantic view descriptions on preciseness, conciseness, non-circularity, and correctness, lint them in SQL, and apply fixes with CREATE OR ALTER or the YAML procedure.

|  |  |
| --- | --- |
| Stage | Evaluate |
| Topics | Semantic Views, Cortex AI Functions |
| Status | GA |
| Time to complete | 20min |
| Edition | Any edition with semantic views |
| Regions | Any region with semantic views; the optional model grader needs AI\_COMPLETE and the chosen model |
| Privileges | ACCOUNTADMIN only in 01\_example\_setup.sql (the example role, warehouse, and database) and 99\_teardown.sql; to lint your own view, any role with a privilege on it |
| Related skills | `agent-studio` (bundled with Cortex Code), `semantic-view-patterns` ([Snowflake-Labs/coco-skills](https://github.com/Snowflake-Labs/coco-skills)) |
| Last verified | 2026-10-04 |
| Authors | Parker Erickson |
| Code | [View all files](/developer-guide/cortex-ai-cookbook/description-quality/code) or download [description-quality.zip](/static/samples/cortex-ai-cookbook/description-quality.zip), which includes this page as `README.md`. Teardown: [sql/99\_teardown.sql](/developer-guide/cortex-ai-cookbook/description-quality/code#label-cookbook-description-quality-sql-99-teardown-sql) |

Expand

Show lessSee more

This recipe is a reference implementation: review the code and adapt it to your environment before production use.

Snowflake’s modeling guidance calls descriptions the single most important element for accuracy in a semantic view:
the model cannot reliably infer proprietary terms, abbreviations, or business logic, so what you write in `COMMENT`
(DDL) or `description` (YAML) is what it works from. This recipe gives you four criteria for judging a description, a
SQL linter that flags the mechanical failures in any semantic view, an optional `AI_COMPLETE` grader for the rest, and
the two ways to write the fixes back without losing grants.

## When to use this

- You are reviewing a semantic view before putting it behind Cortex Analyst or an agent.
- A view was generated or bulk-imported and nobody has read the descriptions.
- Answers are wrong in ways that trace to a misunderstood column or metric (as opposed to a join or grain problem).

When not to use it:

- Answers are off by a clean multiple, or a join fans out. Fix the model first: see
  [mixed-grain tables](/developer-guide/cortex-ai-cookbook/mixed-grain-and-verified-queries) and the `sv_diagnostics` snippet under
  [Related skills](#related-skills).
- You need an accuracy number. This recipe improves inputs; measure outcomes with an evaluation set.

## How it works

[![Diagram: How it works](/static/images/cortex-ai-cookbook/description-quality/diagram-dfc789a4.svg)](/static/images/cortex-ai-cookbook/description-quality/diagram-dfc789a4.svg)

- **Four criteria, graded separately.** Precise (tells this element apart from similar ones), concise (every word adds
  meaning), non-circular (says more than the name), correct (matches the expression). These are review heuristics,
  not a Snowflake scoring system; they operationalize the docs guidance to write explicit, business-level
  descriptions and explain proprietary terms.
- **Lint what is mechanical.** Missing, circular, padded, and “says total but the expression is `AVG`” are all
  detectable in SQL from `INFORMATION_SCHEMA`, with no model call.
- **Grade what needs judgment.** A model can grade preciseness and propose a rewrite, but it cannot know that `W`
  means web or which statuses count as sales. The grader is told to write `UNKNOWN` for those; a person fills them in.
- **Apply by redefining.** `ALTER SEMANTIC VIEW` changes only the view-level comment. Element descriptions change
  through `CREATE OR ALTER SEMANTIC VIEW`, which keeps grants and removes anything you omit, or through the YAML
  procedure with `create_or_alter = TRUE`.

## The rubric

| Grade | Precise | Concise | Non-circular | Correct |
| --- | --- | --- | --- | --- |
| A | Scope, units, filters, and exclusions stated; could not be confused with a sibling | Nothing to cut | Reads as a definition with the name hidden | Aggregation, columns, and grain match the expression |
| B | Small gaps that would not cause misuse | A few filler words | Adds real information | Right, with minor omissions |
| C | Could describe several elements in the view | Could lose half its length | Partly restates the name | Right idea, wrong aggregation or a missing key detail |
| D | Almost no distinguishing detail | Meaning buried in boilerplate | Mostly the name plus filler | Would lead to wrong SQL |
| F | Missing, or generic (“a metric”) | Missing | The name reworded | Contradicts the expression |

Expand

Show lessSee more

Examples from the sample view, before and after:

| Element | Before | Problem | After |
| --- | --- | --- | --- |
| `avg_order_value` = `AVG(net_amount)` | Total value of all orders | Says total; the SQL averages | Average NET\_AMOUNT per order, in USD, across all order statuses. |
| `total_revenue` = `SUM(net_amount)` | The total revenue | Circular; no unit, no scope | Sum of NET\_AMOUNT in USD across all order statuses. Filter STATUS = SHIPPED for recognized sales. |
| `order_date` | This field represents the date on which the order was placed by the customer in the system and recorded in the database | Padded | Date the order was placed. |
| `ord_chnl` | Channel | Hides a legacy code | Exposed as `order_channel` (Web, Store, Phone), decoded from the legacy ORD\_CHNL code (W, S, P). |
| `status` | (missing) | Which values count as sales? | Fulfillment status. SHIPPED orders count as sales; RETURNED and CANCELLED orders do not. |

Expand

Show lessSee more

Writing tips that follow from the criteria:

- Lead with what it is, then the unit, then scope and exclusions. Drop “This field represents” and “in the system”.
- For metrics, name the aggregation and the column it aggregates, and say which rows are included.
- For codes and abbreviations, list the values and their meaning, or decode them in the expression and add
  `SAMPLE_VALUES` with `IS_ENUM`.
- Describe the table too: what one row is, and the time range or population it covers.

## Synonyms

Current Snowflake guidance is to avoid synonyms unless a term is proprietary, an abbreviation, or a legacy name the
model is unlikely to know, and to add them by hand rather than generating them. The sample view starts with six
generated synonyms on `total_revenue` (`revenue`, `sales`, `income`, `turnover`, `money`, `amount`) and ends with one
synonym in the whole view: `ord_chnl`, the legacy column name users still type. The linter flags every synonym so each
one gets a deliberate keep-or-drop decision.

## Prerequisites

| Requirement | Notes |
| --- | --- |
| A semantic view | The example creates `COOKBOOK_DESCRIPTION_QUALITY.SALES.ORDERS_SV`. To lint your own, set `DB`, `SCHEMA_NAME`, and `SV_NAME` in `02` to the view, and `ROLE_NAME` and `WH` to a role with any privilege on it and a warehouse that role can use. These are the only names in the recipe meant to change; `02` creates nothing, so the role needs no `CREATE` privilege in your schema. |
| Privileges | Any privilege on the view lets you read it through `INFORMATION_SCHEMA`; changing it needs `OWNERSHIP`. The example setup and teardown run as ACCOUNTADMIN for the role, warehouse, and database. |
| Model (optional) | Part 2 of the linter calls `AI_COMPLETE` with `claude-sonnet-4-6` (`MODEL` in `02`). |

Expand

Show lessSee more

## Quickstart

1. [sql/01\_example\_setup.sql](/developer-guide/cortex-ai-cookbook/description-quality/code#label-cookbook-description-quality-sql-01-example-setup-sql): a 40-row orders table and a view with weak descriptions.
2. [sql/02\_lint\_descriptions.sql](/developer-guide/cortex-ai-cookbook/description-quality/code#label-cookbook-description-quality-sql-02-lint-descriptions-sql): Part 1 heuristic flags, Part 2 model grades and rewrites.
3. [sql/03\_apply\_descriptions.sql](/developer-guide/cortex-ai-cookbook/description-quality/code#label-cookbook-description-quality-sql-03-apply-descriptions-sql): apply fixes with `CREATE OR ALTER`, then validate the
   YAML route with `verify_only = TRUE`.
4. Re-run Part 1 of `02`.
5. [sql/99\_teardown.sql](/developer-guide/cortex-ai-cookbook/description-quality/code#label-cookbook-description-quality-sql-99-teardown-sql).

## Walkthrough

### 1. Heuristic lint

The linter reads all three element types from `INFORMATION_SCHEMA` and flags them:

Copy code

```
SELECT 'METRIC' AS KIND, NAME, EXPRESSION, COMMENT, SYNONYMS
FROM INFORMATION_SCHEMA.SEMANTIC_METRICS
WHERE SEMANTIC_VIEW_NAME = 'ORDERS_SV'
-- UNION ALL the same from SEMANTIC_DIMENSIONS and SEMANTIC_FACTS
```

On the sample view it flags 8 of 9 elements:

| Element | Flags |
| --- | --- |
| TOTAL\_REVENUE | CIRCULAR, UNIT, SYNONYMS: 6 |
| AVG\_ORDER\_VALUE | CONTRADICTS SQL: says total, expression is AVG; UNIT |
| CUSTOMER\_NAME, DISCOUNT\_AMOUNT | CIRCULAR |
| ORDER\_DATE | PADDED |
| STATUS, NET\_AMOUNT | MISSING |
| ORDER\_COUNT | UNIT |

Expand

Show lessSee more

The one it misses is `ORD_CHNL` (“Channel”), because a word list cannot know that the column holds a legacy code.
That is the job of the model grader, and ultimately of a person.

### 2. Model grades

Part 2 sends each element’s name, expression, and description to `AI_COMPLETE` with a `response_format` whose grades
are an `enum` of A to F, and asks for a rewrite that uses only visible facts. On the sample view it graded
`AVG_ORDER_VALUE` F for correctness (“The word Total directly contradicts the AVG aggregation”) and `ORD_CHNL` D on
three criteria, and its rewrites marked the channel values and status meanings `UNKNOWN`. Treat the grades as a
triage order and the rewrites as drafts.

### 3. Apply the fixes

Route A redefines the view in place:

Copy code

```
CREATE OR ALTER SEMANTIC VIEW ORDERS_SV
  TABLES (orders AS ORDERS PRIMARY KEY (ORDER_ID)
            COMMENT = 'One row per customer order placed with Contoso Outdoor, January to March 2026, all statuses.')
  ...
  METRICS (
    orders.avg_order_value AS AVG(net_amount)
      COMMENT = 'Average NET_AMOUNT per order, in USD, across all order statuses.',
  ...
```

`CREATE OR ALTER` keeps grants, and it also removes what you leave out. Rerunning the linter after Route A shows the
six synonyms gone, because the new definition omits them. Include every element and property you want to keep.

Route B uses YAML. Export with `SYSTEM$READ_YAML_FROM_SEMANTIC_VIEW`, edit the `description` fields, and call:

Copy code

```
CALL SYSTEM$CREATE_SEMANTIC_VIEW_FROM_YAML('<db>.<schema>', $$ ...yaml... $$, TRUE, TRUE);   -- validate only
CALL SYSTEM$CREATE_SEMANTIC_VIEW_FROM_YAML('<db>.<schema>', $$ ...yaml... $$, FALSE, TRUE);  -- apply with CREATE OR ALTER
```

The third argument is `verify_only`; the fourth, `create_or_alter`, applies the change with CREATE OR ALTER semantics
instead of replacing the view. CREATE OR ALTER semantics apply to the YAML too: an element missing from the YAML is
removed from the view. The YAML in `03` is the complete view, the same nine elements as Route A, so setting
`verify_only` to `FALSE` applies it and keeps all nine, including the `ord_chnl` synonym. For your own view, start from
the `SYSTEM$READ_YAML_FROM_SEMANTIC_VIEW` export and change only the `description` fields.

## Verify

After `03`, Part 1 of the linter returns an empty `FLAGS` array for every element except `ORDER_CHANNEL`, which keeps
its one deliberate synonym. The YAML call returns
`YAML file is valid for creating a semantic view. No object has been created yet.`

## Gotchas

| Symptom | Cause | Fix |
| --- | --- | --- |
| No `ALTER` option for a dimension, fact, or metric comment | `ALTER SEMANTIC VIEW` changes only the view-level comment | Use `CREATE OR ALTER` or the YAML procedure |
| Synonyms, sample values, or verified queries disappear after a fix | `CREATE OR ALTER`, and the YAML procedure with `create_or_alter = TRUE`, remove omitted elements and properties | Start from `GET_DDL('SEMANTIC_VIEW', ...)` or the exported YAML, not from memory or a partial file |
| Linter shows no flags but answers are still wrong | Heuristics catch form, not meaning | Run the model grader, then check the view against an evaluation set |
| Model rewrite invents business rules | It was asked to describe what it cannot see | Keep `UNKNOWN` in the prompt and have an owner fill it in |
| Six generated synonyms on one metric | Synonym auto-generation | Keep only proprietary, abbreviated, or legacy terms |
| Descriptions change but grants are lost | `CREATE OR REPLACE` without `COPY GRANTS` | Use `CREATE OR ALTER` |

Expand

Show lessSee more

## Teardown

Copy code

```
-- sql/99_teardown.sql
DROP DATABASE IF EXISTS COOKBOOK_DESCRIPTION_QUALITY;
DROP WAREHOUSE IF EXISTS COOKBOOK_DESCRIPTION_QUALITY_WH;
DROP ROLE IF EXISTS COOKBOOK_DESCRIPTION_QUALITY_ROLE;
```

## Adapt this recipe

Keep these, so a customized version keeps the recipe’s security model:

- Least privilege: `ACCOUNTADMIN` only for the scripts listed under Privileges; everything else runs as the recipe’s own role.
- No grants to `PUBLIC`.
- Credentials: create keys, tokens, and secrets yourself, in a separate terminal, and read them from environment variables. Never put them in a script or give them to an agent.
- Dynamic SQL, if you add any, uses bind variables or an allowlist of identifiers, never text concatenated from user or model input.

Change these to fit your use case:

- Object names. Rename them in every script, including teardown, then check that teardown still removes everything.
- Roles, personas, and users: map them to your own, each granted no more than the recipe grants.
- Data: point the scripts at your tables instead of the sample data, then run Verify again.
- Models and warehouse sizes.

To have a coding agent adapt it:

```
Adapt the description-quality recipe in description-quality/ (unzipped from description-quality.zip) to <describe your use case>.
Read README.md first. Keep everything the "Adapt this recipe" section says to keep.
Change only names, roles and personas, data, and models.
Show me each changed file before you run anything, then run the recipe's Verify steps.
```

## Run it with a coding agent

```
Install or enable the bundled agent-studio skill and the semantic-view-patterns skill from Snowflake-Labs/coco-skills.

Use description-quality/ to review the descriptions in my semantic view <DB>.<SCHEMA>.<VIEW>.
1. Confirm the account and role with SELECT CURRENT_ACCOUNT(), CURRENT_ROLE() and show me before continuing.
2. If I have no view to review, use the example instead: show me sql/01_example_setup.sql and ask before running it,
   because it runs as ACCOUNTADMIN to create a role, a warehouse, and a database. Then use
   COOKBOOK_DESCRIPTION_QUALITY.SALES.ORDERS_SV as the view.
3. Run Part 1 of sql/02_lint_descriptions.sql against the view (set DB, SCHEMA_NAME, SV_NAME, ROLE_NAME, and WH)
   and show the flags.
4. Run Part 2 for the flagged elements only and show the grades and draft rewrites.
5. Ask me for every value marked UNKNOWN. Do not invent business meaning.
6. Produce a CREATE OR ALTER SEMANTIC VIEW statement from GET_DDL with only the descriptions changed, show me the
   diff, and apply it only after I approve.
7. Re-run Part 1 and confirm the flags are cleared.
8. If you ran the example setup, run sql/99_teardown.sql when I say so and confirm nothing named
   COOKBOOK_DESCRIPTION_QUALITY remains. Never drop anything else.
```

## Related skills

- `agent-studio` (bundled): creating, auditing, and optimizing semantic views, including their descriptions.
- `semantic-view-patterns` (coco-skills): the `ai_metadata` snippet covers custom instructions and verified queries,
  the next layer after descriptions.

## References

- [Best practices for modeling semantic views](/user-guide/views-semantic/best-practices-modeling)
- [Using SQL commands to create and manage semantic views](/user-guide/views-semantic/sql)
- [YAML specification for semantic views](/user-guide/views-semantic/semantic-view-yaml-spec)
- [SYSTEM$CREATE\_SEMANTIC\_VIEW\_FROM\_YAML](/sql-reference/stored-procedures/system_create_semantic_view_from_yaml)
- [SEMANTIC\_DIMENSIONS view](/sql-reference/info-schema/semantic_dimensions)
- [AI\_COMPLETE (Structured outputs)](/sql-reference/functions/ai_complete-structured-outputs)

# Make ML predictions human-interpretable with a Cortex Agent

[Preview Feature](/release-notes/preview-features) — Open

This recipe uses features in preview: undefined.

Turn a Model Registry prediction into an explanation people can use: why the model scored a member high, what each driver means, and how much to trust the score.

|  |  |
| --- | --- |
| Stage | Build, Evaluate |
| Topics | Cortex Agents |
| Status | Preview |
| Time to complete | 45min |
| Edition | Any edition with Cortex Agents |
| Regions | Any region with Cortex Agents; warehouse Python with the Snowflake Anaconda channel |
| Privileges | ACCOUNTADMIN for sql/01\_setup.sql and sql/99\_teardown.sql; 02 to 07 run as COOKBOOK\_EXPLAIN\_MODEL\_PREDICTIONS\_ADMIN |
| Related skills | `machine-learning` (bundled with Cortex Code), `agent-studio` (bundled with Cortex Code) |
| Last verified | 2026-11-10 |
| Authors | Chris Caudill |
| Code | [View all files](/developer-guide/cortex-ai-cookbook/explain-model-predictions/code) or download [explain-model-predictions.zip](/static/samples/cortex-ai-cookbook/explain-model-predictions.zip), which includes this page as `README.md`. Teardown: [sql/99\_teardown.sql](/developer-guide/cortex-ai-cookbook/explain-model-predictions/code#label-cookbook-explain-model-predictions-sql-99-teardown-sql) |

Expand

Show lessSee more

This recipe is a reference implementation: review the code and adapt it to your environment before production use.

A model score on its own tells a care manager nothing about why. This recipe
turns each prediction into a plain-language explanation: what drove the score,
what each driver means, and how much to trust it. Ask the agent “why was member
M000003 flagged as a likely high-cost claimant?” and it answers with the score,
how often members with similar scores really were high-cost, and the three
things that pushed the score up most, each compared with a typical member and
described in your plan’s own terms. Underneath, a classifier in the Snowflake
Model Registry supplies the prediction and its Shapley values through
`PREDICT_PROBA` and `EXPLAIN`, a feature dictionary you control supplies what
each feature means, and holdout calibration supplies the confidence. The agent
is instructed never to present a driver as a cause.

## When to use this

- A classifier already drives a workflow (care management outreach, fraud
  review, credit decisions) and the people acting on its scores ask “why this
  one?”.
- You need answers grounded in the model’s own attributions rather than an LLM’s
  guess about what usually drives the outcome.
- You need to report confidence honestly: what a score of 0.74 meant on members
  the model never saw, not the raw probability.

When not to use it:

- You need to know what will happen if you intervene (“will outreach lower this
  member’s cost?”). Shapley values describe the model, not the world. Use a
  causal design such as the [causally grounded agent](/developer-guide/cortex-ai-cookbook/agent-causal-grounding).
- The model is PyTorch, TensorFlow, or a Hugging Face pipeline. The registry’s
  `EXPLAIN` method covers scikit-learn, XGBoost, LightGBM, and CatBoost only.
- The model only runs on Snowpark Container Services. `EXPLAIN` runs in a
  warehouse.

## How it works

[![Diagram: How it works](/static/images/cortex-ai-cookbook/explain-model-predictions/diagram-5772268b.svg)](/static/images/cortex-ai-cookbook/explain-model-predictions/diagram-5772268b.svg)

Key concepts:

1. **Explainability is decided when you log the model.** `log_model` creates an
   `EXPLAIN` method when the model type supports it, `sample_input_data` is
   given, and the target platforms include `WAREHOUSE`. This recipe also sets
   `options={"enable_explainability": True}` explicitly. A version cannot gain
   explainability later; you log a new version.
2. **Shapley values are relative to background data.** The rows passed as
   `sample_input_data` (500 training members here) define the “average” member
   each explanation is measured against. For this XGBoost classifier the
   values are log-odds contributions: `LN(p / (1 - p))` equals the base value
   (about -2.10, a score of 0.11) plus the sum of the nine contributions, to six
   decimal places on every holdout row.
3. **A score is not a confidence.** 04 scores the 20% holdout and records, per
   score band, how often members in that band actually were high-cost. The
   agent reports that observed rate and, when asked how confident it is, the
   holdout AUC and the precision at the flag threshold.
4. **Meaning comes from a table, not from the model’s general knowledge.**
   `EXPLAIN` returns a number per column name; it says nothing about what
   `OPEN_CARE_GAPS` means. `FEATURE_DICTIONARY` holds, per feature, a label, a
   unit, a definition (what it measures and how it is counted), and
   `HOW_TO_EXPLAIN` guidance (what it is a signal of and what not to say). The
   tools return those fields with every driver, a third tool returns the whole
   dictionary, and the instructions tell the agent to define features only from
   them and to say when a question goes beyond them. Each tool result stays
   around 5 KB.
5. **Least privilege through caller’s rights.** The user role gets USAGE on the
   agent, the three procedures, and the model, and SELECT on four tables. USAGE
   on a model allows inference without exposing its internals; READ would also
   expose metadata. There is no Cortex Analyst tool, so the agent cannot compute
   its own numbers from raw rows.

## Prerequisites

| Requirement | Notes |
| --- | --- |
| A region with Cortex Agents | The orchestration model is `auto`. Change it in `06_agent.sql` if your account restricts models. |
| `ACCOUNTADMIN` for `01_setup.sql` and `99_teardown.sql` | 01 creates the two roles, the warehouse, and the database, and grants `SNOWFLAKE.CORTEX_USER`. 02 to 06 run as `COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_ADMIN`; 07 runs as `COOKBOOK_EXPLAIN_MODEL_PREDICTIONS_USER`. |
| Warehouse Python 3.11 with the Snowflake Anaconda channel | `03` trains in a procedure using `snowflake-ml-python`, `xgboost`, `scikit-learn`, and `pandas`. No local Python environment and no artifact repository are needed. |
| Snowflake CLI (`snow sql`) | Each script runs as written with `snow sql -f`. |

Expand

Show lessSee more

Model Registry explainability is documented as a preview feature, so this recipe
is marked preview.

## Quickstart

From `explain-model-predictions/`:

1. `snow sql -f sql/01_setup.sql`: roles, warehouse, database, schema.
2. `snow sql -f sql/02_data.sql`: 20,000 synthetic members (11% high-cost), a
   20% holdout, and the feature dictionary with definitions.
3. `snow sql -f sql/03_train_and_register.sql`: train XGBoost and log
   `HIGH_COST_CLAIMANT` V1 with `EXPLAIN`. Takes a few minutes.
4. `snow sql -f sql/04_calibrate.sql`: score the holdout, write
   `SCORE_CALIBRATION` and `MODEL_CARD`, and check that the explanations are in
   log-odds.
5. `snow sql -f sql/05_tools.sql`: the three tool procedures, plus four test
   calls.
6. `snow sql -f sql/06_agent.sql`: the agent and the user role’s grants.
7. `snow sql -f sql/07_ask_agent.sql`: five questions to the agent as the user
   role, then the raw tool output.
8. `snow sql -f sql/99_teardown.sql`.

## Walkthrough

### Logging the model with explainability

Copy code

```
background = train_df.sort(col("MEMBER_ID")).select(FEATURES).limit(500)

mv = reg.log_model(
    model,
    model_name="HIGH_COST_CLAIMANT",
    version_name="V1",
    sample_input_data=background,          # signature, background data, lineage
    target_platforms=["WAREHOUSE"],        # EXPLAIN runs only in a warehouse
    task=task.Task.TABULAR_BINARY_CLASSIFICATION,
    options={"enable_explainability": True},
    metrics={"holdout_auc": holdout_auc},
)
```

`background` is a Snowpark DataFrame, not pandas, so the registry also records
lineage back to `MEMBER_FEATURES`. The trees are shallow and regularized
(`max_depth=3`, `min_child_weight=20`). A deeper first attempt gave the
pure-noise `PORTAL_LOGINS_12M` more attribution than two real features, and an
explanation built on that model would have told care managers that portal logins
matter.

### Calling EXPLAIN from SQL

`EXPLAIN` is a table function, so it goes in `FROM` with a lateral join, one
output column per feature named `<FEATURE>_EXPLANATION`:

Copy code

```
SELECT f.MEMBER_ID, e.*
FROM MEMBER_FEATURES f,
     TABLE(MODEL(COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.CARE_MGMT.HIGH_COST_CLAIMANT, V1)!EXPLAIN(
       f.AGE, f.PRIOR_YEAR_COST, f.CHRONIC_CONDITIONS, f.ER_VISITS_12M, f.INPATIENT_ADMITS_12M,
       f.RX_CLASSES, f.SPECIALIST_VISITS_12M, f.OPEN_CARE_GAPS, f.PORTAL_LOGINS_12M)) e
WHERE f.MEMBER_ID = 'M000003';
```

The documented `WITH mv AS MODEL ... VERSION V1` alias works in a single SELECT,
but not from a later CTE (“Unknown table function MV!EXPLAIN”). The tools use the
inline `MODEL(<name>, V1)!` form, which works anywhere.

### Turning columns into ranked drivers

`SCORE_AND_EXPLAIN_MEMBER` packs the nine contributions into an object,
flattens it, joins the feature dictionary, and keeps the top five by absolute
value:

Copy code

```
SELECT c.KEY AS FEATURE_NAME, c.VALUE::DOUBLE AS CONTRIBUTION,
       ABS(c.VALUE::DOUBLE) / SUM(ABS(c.VALUE::DOUBLE)) OVER () AS SHARE,
       ROW_NUMBER() OVER (ORDER BY ABS(c.VALUE::DOUBLE) DESC) AS RANK
FROM s, LATERAL FLATTEN(INPUT => s.CONTRIBUTIONS) c
JOIN FEATURE_DICTIONARY d ON d.FEATURE_NAME = c.KEY
```

Each driver in the result carries `label`, `unit`, `definition`,
`how_to_explain`, `member_value`, `population_median`, `effect_on_score` (raises
or lowers), `shapley_logodds`, and `share_of_total_attribution`. The share is
what the agent uses to compare drivers; it is not converted into percentage
points of probability, because log-odds contributions do not add up in
probability space.

### The feature dictionary

The model only knows column names, and an LLM asked to explain
`CHRONIC_CONDITIONS` or `OPEN_CARE_GAPS` will fill in a plausible meaning from
general knowledge, which may not match how your plan counts them.
`FEATURE_DICTIONARY` in `02_data.sql` pins the meaning down:

Copy code

```
('OPEN_CARE_GAPS', 'Open preventive care gaps', 'gaps',
 'Recommended preventive or chronic-care services the member is due for but has no claim for, such as an annual diabetic eye exam, a cancer screening, or a medication review.',
 'Say the member is due for that many recommended services. Do not say that closing the gaps would lower the member''s cost or score in real life; the model does not show that.',
 0, 10)
```

`DEFINITION` is what the feature measures and how it is counted, including
look-back windows and, for counts, what is counted (the seven chronic conditions
on a fixed list). `HOW_TO_EXPLAIN` is guidance for the agent: what the feature
is usually a signal of, and the wrong conclusion to avoid. For the noise feature
it says to call any weight “a minor statistical effect of the model”, so an
imperfect model does not produce a confident wrong reason.

The definitions describe this synthetic data. When you point the recipe at real
features, write the dictionary from your data documentation: the agent repeats
it, so it is where your plan’s terminology and review rules live.
`DESCRIBE_FEATURES()` returns the whole dictionary, which lets the agent answer
“what counts as a care gap?” without a member ID.

### What-if without dynamic SQL

`WHAT_IF_MEMBER` checks the feature name against `FEATURE_DICTIONARY` and the
value against that row’s range, then swaps the one column with `IFF`:

Copy code

```
SELECT 'after',
       IFF(:feature = 'AGE',           :NEW_VALUE, AGE),
       IFF(:feature = 'ER_VISITS_12M', :NEW_VALUE, ER_VISITS_12M),
       ...
```

Nothing the user or the model writes is concatenated into SQL. The result is
labeled model sensitivity: the score’s response to one input with everything
else held fixed. A member’s ER visits cannot drop to zero while everything else
stays the same, so the instructions forbid presenting it as an intervention
effect.

### The agent instructions

The response instructions fix the shape of an explanation (score, then what the
score meant on holdout members, then three drivers against the median, each with
a clause from its `how_to_explain`) and the words: drivers “contributed to” or
“pushed up” the score; AUC measures ranking across all members, not certainty
about one. Features are named by label and defined only from tool results, and
the agent says when a question goes beyond them (for example which conditions a
member has, when the model only sees the count). `how_to_explain` is addressed
to the agent, so the instructions also tell it not to read that guidance back to
the user as instructions; without that line, a test answer did. The
orchestration instructions also tell the agent not to use the built-in chart
tool, which every agent has.

## Verify

- `02` returns 20,000 members, a high-cost rate of 0.111, and 4,001 holdout
  members. The data is generated from hashes, so these numbers are the same on
  every run.
- `03` returns `functions: ["EXPLAIN", "PREDICT", "PREDICT_PROBA"]` and a holdout
  AUC of 0.8446. `SHOW FUNCTIONS IN MODEL ... VERSION V1` lists `EXPLAIN` as a
  table function.
- `04` returns a `BASE_VALUE_SPREAD` of about 1e-6 and six calibration bands. The
  ‘very low’ band (under 0.05) holds 2,326 holdout members with an observed rate
  of 0.028; the ‘very high’ band (0.50 and above) holds 205 with an observed rate
  of 0.698. The middle bands run slightly hot: ‘elevated’ has a mean score of
  0.259 against 0.185 observed, which is why the agent quotes the observed rate.
  `MODEL_CARD` shows a base value of -2.094 log-odds (a score of 0.11), and
  precision 0.56 and recall 0.45 at the 0.35 flag threshold.
- `05`’s first call returns member M000003 with a score of 0.74, band ‘very
  high’, and drivers led by chronic conditions (5 against a median of 1, 41% of
  the attribution) and ER visits (5 against 0, 32%). The second call, ER visits
  set to 0, returns 0.324 in ‘elevated’. The third returns an `error` listing the
  allowed features. The fourth, `DESCRIBE_FEATURES()`, returns nine features,
  each with a definition and explanation guidance. Each result is about 5 KB.
- `07` returns five rows:

  - 1 and 2 call `score_and_explain_member`. The answers quote the score and the
    band’s observed rate, name the drivers by label against medians with a short
    note on what each signals, and describe AUC as a ranking measure.
  - 3 calls `what_if_member` with `ER_VISITS_12M` and `0` and calls the result
    model sensitivity.
  - 4 calls `describe_features` and defines care gaps and prior-year allowed cost
    from the dictionary, in plain language.
  - 5 asks which chronic conditions the member has. The agent says the model
    only sees the count (5 of the 7 listed conditions) and points to the claims
    history for names.

  None says a feature causes high cost. Agent wording varies between runs; the
  numbers and definitions in it come from the tools and do not.
- `DATA_AGENT_RUN` runs under the session role that `07` sets with `USE ROLE`,
  even when the user’s default role is PUBLIC.

## Gotchas

| Symptom | Cause | Fix |
| --- | --- | --- |
| The version has no `EXPLAIN` method | Logged with `signatures` instead of `sample_input_data`, with an SPCS-only target, or with explainability off | Log a new version with `sample_input_data`, a `WAREHOUSE` target, and `enable_explainability: True`. Existing versions cannot be changed. |
| “Unknown table function MV!EXPLAIN” | A `WITH mv AS MODEL ...` alias referenced from another CTE | Use `TABLE(MODEL(<db.schema.model>, V1)!EXPLAIN(...))` inline |
| Contributions do not add up to the probability | XGBoost explanations are in log-odds | Compare `LN(p / (1 - p))` with the base value plus the sum; `04` checks this |
| An irrelevant feature appears among the drivers | The model fit noise, and the explanation is faithful to the model | Regularize or remove the feature. Explanations show what the model uses, not what is true. Its `HOW_TO_EXPLAIN` can tell the agent to call it a minor statistical effect, as `PORTAL_LOGINS_12M`’s does |
| The agent defines a feature differently from how your plan counts it | The dictionary is missing the feature or its `DEFINITION` is vague, so the model falls back on general knowledge | Write the definition from your data documentation, including look-back window and what is counted; rerun 02 and 06 |
| An answer tells the user “say…” or “do not say…” | The agent read `HOW_TO_EXPLAIN` back as text for the user | Keep the instruction in `06_agent.sql` that the guidance is for the agent and must not be repeated as instructions |
| `CREATE PROCEDURE` fails with “unexpected ‘COMMENT’” | `COMMENT` placed after `EXECUTE AS` | Put `COMMENT` before `EXECUTE AS CALLER` |
| “Function MAX does not support ARRAY argument type” | Pivoting an ARRAY column with `MAX(IFF(...))` | Build one object per row and combine them with `OBJECT_AGG`, as `WHAT_IF_MEMBER` does |
| The tool calls fail with “does not exist or not authorized” for the user role | 02 to 04 recreated the tables or the model, which drops their grants | Rerun `06_agent.sql` after rerunning any of 02 to 04 |
| The agent draws a chart | Every agent has a built-in chart tool | The orchestration instructions forbid it; filter in the client as well |
| A custom tool rejects an OBJECT or VARIANT argument | Custom tools take scalar parameters | Pass scalars, as these tools do, or a JSON string parsed inside the procedure |
| `snow sql` echoes `if MODEL_NAME in :` for the procedure body | The CLI’s display treats `[...]` as markup | Display only; the statement sent to Snowflake is intact |

Expand

Show lessSee more

## Teardown

`sql/99_teardown.sql` runs as ACCOUNTADMIN and drops the database (model and
versions, agent, procedures, tables), the warehouse, and both roles, then lists
anything left with a `COOKBOOK_EXPLAIN_MODEL_PREDICTIONS` prefix. No
account-level settings are changed by this recipe.

## Run it with a coding agent

```
Install or enable the bundled machine-learning and agent-studio skills if they
are not already available. Then, from explain-model-predictions/:
1. Confirm the target account with SELECT CURRENT_ACCOUNT(), CURRENT_REGION(),
   CURRENT_ROLE(), CURRENT_WAREHOUSE(); and show me the result before creating
   anything.
2. sql/01_setup.sql runs as ACCOUNTADMIN to create two COOKBOOK_ roles, a
   warehouse, and a database. Show me those statements and wait for my
   confirmation, then run it with snow sql -f.
3. Run sql/02_data.sql through sql/06_agent.sql in order with snow sql -f.
   Report the holdout AUC from 03, the BASE_VALUE_SPREAD and calibration bands
   from 04, and the first tool result from 05.
4. Run sql/07_ask_agent.sql and summarize each of the five answers: which tools
   ran, the score, the band's observed rate, the drivers named, and how each
   feature was defined. Flag any answer that describes a feature as a cause or
   defines a feature with facts that are not in the FEATURE_DICTIONARY row.
5. Only touch objects whose names start with COOKBOOK_EXPLAIN_MODEL_PREDICTIONS.
   Run sql/99_teardown.sql when I say so; it uses ACCOUNTADMIN for the drops.
```

## Related skills

- `machine-learning` (bundled with Cortex Code): its model-registry sub-skill
  covers logging other model types, explainability options, and visualizing
  Shapley values with `snowflake.ml.monitoring.explain_visualize`.
- `agent-studio` (bundled with Cortex Code): build an evaluation set for this
  agent and check that answers keep the score, the band rate, and the
  non-causal wording.

## References

- [Model Explainability](/developer-guide/snowflake-ml/model-registry/model-explainability)
- [Snowflake Model Registry](/developer-guide/snowflake-ml/model-registry/overview)
- [XGBoost in the Model Registry](/developer-guide/snowflake-ml/model-registry/built-in-models/xgboost)
- [Model commands](/sql-reference/commands-model)
- [Cortex Agents](/user-guide/snowflake-cortex/cortex-agents)
- [CREATE AGENT](/sql-reference/sql/create-agent)
- [Caller’s rights and owner’s rights stored procedures](/developer-guide/stored-procedure/stored-procedures-rights)

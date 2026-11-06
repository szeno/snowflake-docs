# Causally grounded Cortex Agent that refuses when the data cannot answer: Design

Part of the [Causally grounded Cortex Agent that refuses when the data cannot answer](/developer-guide/cortex-ai-cookbook/agent-causal-grounding) recipe.

Read this before changing anything. It explains what each piece is for, and more
usefully, what you can delete.

## The thesis, once

A risk model tells you **who will have a bad outcome**. It does not tell you **who
you can help**. Those are different rankings. Acting on the first one, which is
what nearly every intervention program does, spends a fixed budget on units that
cannot benefit.

This framework estimates who is *movable*, allocates a constrained budget to
those units, and produces an audit trail for the decision.

## Product vs synthetic scaffolding

This distinction matters more than anything else in this document. Roughly half
this repository exists to prove the method works, not to do the work.

| Component | What it is | Keep for real data? |
| --- | --- | --- |
| `framework/causal_core/spec.py` | Use case contract loader | Yes, core |
| `framework/causal_core/data.py` | Reads the five canonical tables | Yes, core |
| `framework/causal_core/causal.py` | Propensity, AIPW, CATE, diff-in-diff | Yes, core |
| `framework/causal_core/naive.py` | The unadjusted estimates | Yes, as a baseline |
| `framework/causal_core/results.py` `EstimateResult` | Shared result shape | Yes, core |
| `framework/causal_core/results.py` `Leaderboard` | Grades against truth | **No, scaffolding** |
| `usecases/*/01_contract.sql` | The five tables, documented | Yes, this is the contract |
| `usecases/*/02_generate_synthetic.sql` | 600 to 900 lines fabricating data | **No, scaffolding** |
| `usecases/*/TRUTH` schema | Planted answer key | **No, scaffolding** |
| `MODELS.CALIBRATION_CHECKS` | Asserts the synthetic data proves something | **No, scaffolding** |
| `load_analysis_frame(include_truth=True)` | Joins the answer key | **No, scaffolding** |

Expand

Show lessSee more

Everything scaffolding-flagged is labelled `SYNTHETIC SCAFFOLDING` in its docstring or
header comment. Grep for it.

**Why keep scaffolding at all?** Because on real data you can never check whether
a causal estimate was correct. There is no answer key. The synthetic use cases are
the only place a method can be graded, so they are how you earn the right to
trust the same code on real data.

## The contract

Every use case supplies five objects in its `DATA` schema. Tables or views, the
framework does not care.

| Object | Grain | Required columns beyond the spec |
| --- | --- | --- |
| `UNIT` | one per decision subject | unit id |
| `UNIT_PERIOD` | one per unit per period | unit id, `PERIOD_INDEX`, `IS_PRE`, period column |
| `TREATMENT` | one per unit | unit id; the boolean flag is named by `treatment.column` (`TREATED` in the bundled use cases) |
| `OUTCOME` | one per unit | unit id, outcome columns |
| `CAPACITY` | one per group per period | group column, slots column |

Expand

Show lessSee more

Schema names are fixed (`DATA`, `TRUTH`, `MODELS`, `AGENT`, `APP`) so code never
guesses. Only the database name varies, which is what guarantees two use cases
cannot collide.

`PERIOD_INDEX` and `IS_PRE` are the only two column names the framework hardcodes.
Everything else it learns from `usecase.yaml`.

## How domain knowledge stays out of the code

```
usecase.yaml                     the ONLY place domain names live
    |
    v
spec.py  ->  UseCaseSpec  ------> every other module reads this
    |
    +-- unit.id_column           what to join on
    +-- treatment.column         what the intervention is
    +-- outcome.direction        WHICH WAY IS GOOD
    +-- outcome.value_per_event  how to turn an effect into money
    +-- covariates.observed      what to adjust for
    +-- fairness.*               who must not be quietly deprioritized
    +-- capacity.*               the binding constraint
```

`outcome.direction` is the piece that does the most work. Readmission should go
down, revenue should go up. Rather than every module knowing which, the spec
exposes `outcome.sign` and `outcome.benefit()`, and callers multiply. That single
indirection is why the churn use case needs no Python changes.

If you find yourself writing a domain column name inside `framework/`, the
abstraction has leaked. Add it to the spec instead.

## The analysis flow

```
                    01_contract.sql          (or 03_bring_your_own_data.sql)
                           |
                     five canonical objects
                           |
                 load_analysis_frame()
                 - snapshots time-varying covariates at the
                   LAST PRE-TREATMENT period
                           |
     +---------------------+---------------------+
     |                                           |
LAYER A (naive)                          LAYER B (causal)
raw_difference                           fit_propensity
s_learner_simulation                     overlap_report  <-- can refuse here
     |                                   balance_table
     |                                   dr_ate
     |                                   causal_forest_cate
     |                                   did_estimate
     |                                           |
     +---------------------+---------------------+
                           |
                  MODELS.CATE_SCORES
                  MODELS.DIAGNOSTICS
                           |
     +---------------------+---------------------+
     |                     |                     |
allocation           agent tools           Streamlit
+ equity gate        (warehouse procs)     (reads tables)
```

Note where `overlap_report` sits. It runs *before* any estimate, because it can
invalidate everything after it. If a cohort has no comparable untreated units, no
method recovers the effect and the only honest output is a refusal.

## Design decisions and why

**Covariates are snapshotted at the last pre-treatment period, automatically.**
Using a post-treatment covariate is the most common way to silently destroy a
causal estimate, and it is invisible in the output. The framework removes the
opportunity to get it wrong rather than documenting the hazard.

**dowhy runs in its own stored procedure, not in Python.** `refute.py` is a thin
client for `AGENT.REFUTE_ESTIMATE`. dowhy requires
`numpy>2`, econml requires `numpy<2`. They cannot share a process, in a warehouse
or in a notebook. So dowhy is encapsulated behind SQL and reached with `CALL`, and
data crosses that boundary as tables, never pickles (the two sides run different
pandas major versions). Useful side effect: the core path needs no compute pool
and no SPCS, just an XSMALL warehouse. Full detail in
[runtime-and-packages.md](/developer-guide/cortex-ai-cookbook/agent-causal-grounding/runtime-and-packages).

**Agent tools read precomputed scores and never fit a model.** Fitting inside a
chat turn is slow, non-deterministic, and impossible to audit. Notebook 02 writes
`CATE_SCORES` once; everything downstream reads it.

**The panel is aggregated in SQL, not pandas.** A 100k-unit panel is 2.4M rows.
Pulling them back to average them is pointless. `load_did_frame` does the
aggregation in Snowflake and returns one row per unit. The first-differences form
it produces is algebraically identical to two-way fixed effects diff-in-diff, and
is unit-clustered by construction.

**Synthetic randomness is hash-derived, not `RANDOM()`.** `RANDOM()` depends on
row processing order and therefore on parallelism, so it does not reproduce. The
generator produces byte-identical data on every account, every time.

**The generator uses `INSERT`, not `CREATE OR REPLACE`.** The contract lives in
`01_contract.sql` as DDL with a comment on every column. `CREATE OR REPLACE` would
discard those comments, so the contract would only exist in a file rather than in
the database where `DESCRIBE TABLE` can find it.

**The treatment column is `TREAT`, not `T`.** pandas exposes `DataFrame.T` as the
transpose property, so a column named `T` cannot be reached by attribute access
and silently returns a transposed frame.

## Two hazards this repo has already hit

Both were found by execution, both would recur, and both now have a calibration
check guarding them. They are worth knowing because they are properties of the
problem, not of this code.

**Statistical power.** A one-shot binary outcome at a ~20% base rate does not
carry enough information per unit to estimate per-unit effects at a realistic
panel size. At 25k units a causal forest honestly reported it could rank nobody
(3.7% of units individually significant) and performed at random. Fixing it needed
an annualized rate outcome (mean of 12 periods, about 3.5x less noise) and 100k
units. **If you want per-unit uplift on a rare binary outcome, you probably do not
have enough data, and this is the number that shows it.**

**Effect heterogeneity that is only prognosis in disguise.** The first generator
built the treatment effect as a function of baseline risk alone. Measured R² of
the true effect on baseline risk was 0.84. In that world a plain outcome model
ranks as well as a causal forest, because knowing how sick someone is tells it
everything. Real programs are not like that: whether an intervention lands depends
on reachability and fit, which are largely orthogonal to severity. Adding one
genuine effect modifier dropped that R² to 0.40 and restored the gap between
methods. `MODELS.CALIBRATION_CHECKS` now asserts
`effect_heterogeneity_not_just_risk`.

**The general lesson:** before building any uplift use case, measure
`R²(true_effect ~ baseline_risk)`. If it is high, no amount of tuning the
estimator will make causal ML look better than plain ML on ranking, because there
is nothing there for it to find.

## What the notebooks are for

| Notebook | Question it answers | Needs TRUTH? |
| --- | --- | --- |
| `01_naive.ipynb` | What would we conclude without causal inference? | For grading only |
| `02_causal.ipynb` | What is the effect, and should we believe it? | For grading only |
| `03_allocation_equity.ipynb` | Who do we treat, and is that fair? | For pricing against truth only |

Expand

Show lessSee more

They are generated from `framework/render_notebooks.py` rather than edited
directly. Notebook JSON is painful to review and merge, so the cell content lives
in Python and the `.ipynb` files are committed build artifacts. Edit the renderer,
run it, commit both.

## What works without planted truth

Worth being precise about, because it determines what survives contact with real data.

| Capability | Needs truth? |
| --- | --- |
| Propensity, overlap, balance diagnostics | No |
| Doubly-robust ATE and its confidence interval | No |
| Difference-in-differences and pre-trend test | No |
| CATE estimates and the resulting ranking | No |
| **Qini curve and AUUC** | **No.** Computed from observed outcomes |
| Allocation, capacity constraints, equity gate | No |
| Projected value of a policy | No, uses estimated effects |
| *Realized* value of a policy | Yes |
| Estimator error, bias, coverage | Yes |

Expand

Show lessSee more

Qini is the only ranking check here that works without an answer key, which makes it
the one to run in production. Everything in the leaderboard and every “priced with
truth” table is synthetic scaffolding.

## Agent design

Six procedures in the `AGENT` schema, one Cortex Agent, one deployable source with
`@DATABASE@` / `@UNIT_ID@` / `@WAREHOUSE@` substituted per use case by
`framework/deploy_agent.py`. Five live in `agent/01_tools.sql`; `REFUTE_ESTIMATE`
is separate because it needs its own package environment.

| Tool | Answers | Can refuse |
| --- | --- | --- |
| `EXPLAIN_ASSUMPTIONS` | what must be true for these numbers to hold | n/a |
| `CHECK_IDENTIFICATION` | is a cohort answerable at all | **yes, that is its job** |
| `RUN_SCENARIO` | value of treating N units, optionally in a cohort | **yes, checks first** |
| `OPTIMIZE_ALLOCATION` | how many are worth treating; what binds | reports “none” |
| `COMPARE_TARGETING_STRATEGIES` | does the ranking beat risk, and is it fair | n/a |
| `REFUTE_ESTIMATE` | do three attacks break the estimate | n/a, but it can fail |

Expand

Show lessSee more

Four decisions worth stating.

**Tools read, they never fit.** Fitting happens once in notebook 02 and is
persisted. This is not about latency. It is what makes a number quoted in chat, a
number on a dashboard, and a number in a notebook the same number.

**Refusal is a tool, not a disclaimer.** `CHECK_IDENTIFICATION` is a separate tool
so the orchestrator can be told to call it first, and so a refusal is a first-class
answer. `RUN_SCENARIO` re-checks internally rather than trusting the caller.

**The identification rule is shared with the framework.** It mirrors
`causal_core.causal.is_identified` exactly. An earlier version invented a stricter
rule and refused to answer for the full population that notebook 02 had already
reported on. An agent applying a different standard than the pipeline behind it is
not being careful, it is being inconsistent.

**There is deliberately no Cortex Analyst tool.** Text-to-SQL over these tables
would let the agent compute a raw treated-versus-untreated difference and present it
as an effect. On this data that answer is +0.0846 when the truth is -0.0452.
Restricting the agent to procedures that encapsulate the correct estimator is the
point, not a limitation.

### Snowflake constraints found the hard way

- **Custom tools cannot take OBJECT or VARIANT parameters.** Cohort filters are
  passed as a JSON string and parsed inside the procedure.
- **SQL NULL arrives in Python as `sqlNullWrapper`, not `None`, and it is truthy.**
  A plain falsiness check treats an explicit NULL as a malformed argument.
- **Changing a parameter type creates an overload rather than replacing.** The agent
  then sees two tools with one name. Drop the old signature explicitly.
- **`DATA_AGENT_RUN` requires constant arguments**, so the payload must be a string
  literal rather than `PARSE_JSON(...)`.
- **An output alias shadows the column in `ORDER BY`.** `MAX(AUUC) AS AUUC` ordered
  by `MAX(AUUC)` becomes `MAX(MAX(AUUC))`. Use an ordinal.

## Console design

One file, `app/causal_console.py`, spec-driven from `MODELS.SPEC_SNAPSHOT` so it
serves any use case with no per-use-case code. Five tabs: Decide, Why believe it,
Targeting, Equity, Receipt.

**It shares the agent’s implementation rather than writing its own.** Where a number
takes computation it calls the same procedure the agent calls, `RUN_SCENARIO` for the
scenario projection and `EXPLAIN_ASSUMPTIONS` for the assumption list. Where a panel
is a straight read it reads the same `MODELS.*` table the tools read. Nothing here
recomputes anything, which is what makes a figure on the dashboard and the same
figure in a chat answer provably identical.

**The refusal is enforced in the layout, not in a caption.** When the cohort cannot
support an estimate, the Decide tab withholds the metrics entirely. A warning beside a
number is read as a formality; an absent number is read as an answer.

**Gating is scoped to the tab that needs it.** An early version called `st.stop()`,
which halts the whole Streamlit script and left the population-level tabs blank. Blank
tabs read as breakage rather than as a refusal, so the gate is now an if/else around
the Decide body only.

**Database context differs between environments.** Every query is schema-qualified but
database-unqualified, which is what makes one file serve every use case. In Streamlit
in Snowflake the session inherits the database from the STREAMLIT object, which
`deploy_app.py` creates inside the use case database. Running locally there is no such
context and the first query fails with “This session does not have a current database”
before any UI exists, so the local path sets it explicitly from `CAUSAL_DATABASE` or
the spec on disk.

**`MODELS.SPEC_SNAPSHOT` exists because the app cannot read `usecase.yaml`.** It runs
inside Snowflake. Without the snapshot the console would need its own hardcoded copy
of every label, cost, and protected attribute, and that copy would drift silently. It
doubles as the provenance record on the Receipt tab.

## Known limits

- **Two use cases, and the second one was the test.** The abstraction was extracted
  from payer care management alone, so `usecases/subscription_churn` was built to
  find out whether it generalized. It runs end to end with zero edits under
  `framework/`, and switching between them is one line in `config.yaml`. Adding it
  surfaced exactly one defect: notebook 01 had hardcoded payer covariate names in a
  summary table. Only a second instance finds that, which is the argument for
  having one.
- **Residual bias is real.** The synthetic data contains a deliberate unobserved
  confounder worth roughly 22% of the true effect, and AIPW lands about that far
  off. That is the honest best case for observational data, not a defect.
- **No survival or time-to-event support.** Outcomes are levels or rates measured
  over a fixed window. A time-to-event outcome would need a different estimator.
- **Single binary treatment only.** No dose response, no multi-arm.

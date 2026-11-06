# Causally grounded Cortex Agent that refuses when the data cannot answer: Adding a use case

Part of the [Causally grounded Cortex Agent that refuses when the data cannot answer](/developer-guide/cortex-ai-cookbook/agent-causal-grounding) recipe.

A use case is a `usecase.yaml` plus five objects in a `DATA` schema. Nothing else.
If you find yourself editing anything under `framework/`, stop: the spec is
probably missing a field, and adding it there is the fix.

Two paths. Pick one.

- **[Real data](#path-a-real-data)** you already have in Snowflake. This is the
  normal case.
- **[Synthetic data](#path-b-synthetic-data)** with a planted answer key. Use this
  when you need to prove a method works before trusting it on real data.

---

## Path A: real data

### 1. Answer six questions

Write them down before touching SQL. Every one of them becomes a spec field, and
getting them wrong is far more expensive than getting the SQL wrong.

| Question | Spec field |
| --- | --- |
| What is the unit a decision is made about? | `unit.id_column` |
| What intervention, and what does one cost? | `treatment.*` |
| What outcome, which direction is good, what is an event worth? | `outcome.primary.*` |
| What was measured **before** treatment that might confound it? | `covariates.observed` |
| Which groups must not be quietly deprioritized? | `fairness.protected_attributes` |
| What limits how many units can be treated? | `capacity.*` |

Expand

Show lessSee more

The one people get wrong is the fourth. A covariate measured *after* the
intervention started will silently destroy the estimate and nothing in the output
will warn you. If you are unsure whether a column is pre-treatment, leave it out.

### 2. Copy the template

Copy code

```
cp -r usecases/_template usecases/my_case
```

Rename `name:` inside `usecase.yaml` to match the directory. The loader enforces
that they are identical, so rendered SQL and tables stay traceable.

### 3. Fill in the spec

`usecases/_template/usecase.yaml` is commented field by field. The two worth extra
thought:

**`outcome.direction`** is `minimize` or `maximize`. This is what keeps the
framework domain-blind: rather than every module knowing whether a negative effect
is good news, they multiply by `outcome.sign`. Get it wrong and every dollar
figure inverts.

**`outcome.value_per_event`** converts an effect into money. For a binary or rate
outcome it is the value of preventing one event. For an outcome already measured
in currency, set it to `1`.

### 4. Map your tables

Copy `usecases/_template/03_bring_your_own_data.sql` into your directory and
replace the `<<PLACEHOLDER>>` names. It creates the five canonical objects as
**views**, so there is no data movement, no storage cost, no refresh pipeline, and
your existing governance policies keep applying.

The only real decision in that file is the treatment start date, and it explains
why a single fixed date beats each unit’s own enrollment date (immortal time
bias).

### 5. Point config at it

Copy code

```
# config.yaml
active_usecase: my_case
```

### 6. Verify the contract

Copy code

```
from causal_core import load_spec, get_session, validate_tables
spec = load_spec()
print(validate_tables(get_session(spec), spec))
```

This raises `DataError` listing every problem at once: missing tables, missing
columns, covariates that exist in neither `UNIT` nor `UNIT_PERIOD`. Fix until it
returns a report.

Then run the sanity checks at the bottom of `03_bring_your_own_data.sql`. The
third one, pre-treatment trends, is the one that most often reveals a broken
design.

### 7. Delete the scaffolding

Copy code

```
DROP SCHEMA IF EXISTS MY_DB.TRUTH;
```

In the notebooks, drop `include_truth=True` and remove every cell that reads
`TRUE_ITE`, `TRUE_ATE` or `TRUE_ATT`: the planted-truth and `Leaderboard` cells in
01 and 02, and the cells priced against planted truth in 03. There is no answer key
for real data, so those sections have nothing to grade against, and with `TRUTH`
dropped they fail rather than skip. See [design.md](/developer-guide/cortex-ai-cookbook/agent-causal-grounding/design) for the complete
scaffolding list.

### 8. Run the notebooks

Copy code

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

Then `notebooks/01` through `03`, with only the truth cells from step 7 removed. If
any of them needs another edit to run your use case, that is a framework bug worth
reporting rather than a local fix.

---

## Path B: synthetic data

Only worth the effort when you need to *prove* a method works. Because you control
the generating process, you know the true effect for every unit and can grade
every estimator. That is impossible on real data.

Copy `usecases/payer_care_management/02_generate_synthetic.sql` and adapt it. Read
the header first; it explains what is planted and why.

### Get these three right or the exercise is pointless

**1. Bake in confounding, and make the naive answer visibly wrong.**
If treatment is assigned at random, an unadjusted comparison is already correct and
there is nothing to demonstrate. Make assignment depend on prognosis, the way real
referral does, and the raw comparison will land on the wrong side of zero.

**2. Make the effect depend on something other than baseline risk.**
This is the trap. If the true effect is a function of severity alone, a plain
outcome model ranks as well as any causal method, because severity tells it
everything. Measure it:

Copy code

```
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import HistGradientBoostingRegressor
r2 = cross_val_score(HistGradientBoostingRegressor(), frame[["BASELINE_RISK"]],
                     frame.TRUE_EFFECT, cv=3, scoring="r2").mean()
```

Above roughly 0.6 and causal estimation cannot beat plain ML on ranking, no matter
which estimator you reach for. Fix it by adding an **effect modifier**: a variable
with a large effect on the treatment effect and a near-zero effect on the outcome
level. Reachability, engagement, language match, service availability. Things that
change whether an intervention lands without changing how sick you are.

**3. Check you have the statistical power.**
A one-shot binary outcome at a low base rate cannot support per-unit effect
estimation. Rule of thumb: leaf-level noise is `outcome_sd * sqrt(2 / n_per_leaf)`
and it must be smaller than the true spread of per-unit effects. For a binary at
p=0.2 that means leaves of about 1,000 units, so tens of thousands of units
minimum. An outcome averaged over several periods cuts the noise substantially and
is usually the cheaper fix.

### Then assert all of it

Add checks to `MODELS.CALIBRATION_CHECKS` and make `ASSERT_CALIBRATION()` fail
loudly. Every check in the payer use case exists because that specific thing went
wrong once. Without them a generator tweak can quietly make the naive estimate right
and nothing will tell you.

Two useful conventions from the payer generator:

- **Hash-derived randomness, not `RANDOM()`.** `RANDOM()` depends on row processing
  order and does not reproduce.
- **Rescale the effect to hit your target exactly** rather than hand-tuning
  coefficients: generate a raw effect, then multiply by
  `target_relative * AVG(baseline) / AVG(raw_effect)`. Makes the calibration
  assertion deterministic instead of a guessing game.

---

## Checklist

- `usecase.yaml` `name` matches the directory name
- `outcome.direction` is correct (get this wrong and dollars invert)
- No covariate is measured after treatment started
- `fairness.protected_attributes` is populated, the loader rejects an empty list
- `validate_tables()` returns a report rather than raising
- Both treatment arms are non-empty and comparable in size
- Every unit has a complete panel
- Pre-treatment trends are flat
- `TRUTH` dropped, if using real data
- Notebooks 01 to 03 run with zero edits to `framework/`

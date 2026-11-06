# Causally grounded Cortex Agent that refuses when the data cannot answer: code

Every file in the [Causally grounded Cortex Agent that refuses when the data cannot answer](/developer-guide/cortex-ai-cookbook/agent-causal-grounding) recipe. To run the recipe, download [agent-causal-grounding.zip](/static/samples/cortex-ai-cookbook/agent-causal-grounding.zip), unzip it, and run the scripts from the `agent-causal-grounding/` folder as the recipe describes. Comments in the files that say “see README” refer to the [recipe page](/developer-guide/cortex-ai-cookbook/agent-causal-grounding); the zip includes it as `README.md`.

## Top-level files

### `config.yaml`

Copy code

```
# Causal Decision Framework - runtime configuration
#
# This file holds only environment-level settings. Everything domain-specific
# lives in usecases/<active_usecase>/usecase.yaml, which is the source of truth
# for a use case. To switch domains, change active_usecase and nothing else.

active_usecase: payer_care_management

snowflake:
  # Local runs only. Inside Snowflake, get_active_session() is used instead.
  # Leave connection_name unset to use SNOWFLAKE_CONNECTION_NAME,
  # SNOWFLAKE_DEFAULT_CONNECTION_NAME, or the default connection in
  # connections.toml, in that order. Set it only to pin a specific connection:
  # connection_name: <your-connection>
  warehouse: COOKBOOK_AGENT_CAUSAL_GROUNDING_WH
  # database is intentionally NOT set here - it comes from the use case spec,
  # so two use cases can never collide in the same database.

# Established by running sql/00_verify_packages.sql. See
# docs/runtime-and-packages.md for how and why they matter. Do not change these
# without re-running that script.
runtime:
  warehouse_python: "3.11"
  warehouse_arch: aarch64

  # econml has no aarch64 wheel on PyPI and fails to build from source against
  # numpy 2.x headers. The Snowflake Anaconda channel ships a working aarch64
  # build, so econml must always come from Anaconda.
  econml_source: anaconda

  # dowhy is a pure-Python py3-none-any wheel, so it installs cleanly from the
  # PyPI artifact repository. It pins numpy>2, which is incompatible with
  # econml's numpy<2, so it is isolated in its own stored procedure.
  dowhy_source: pypi_artifact_repository
  dowhy_version: "0.14"
  artifact_repository: snowflake.snowpark.pypi_shared_repository

# Thresholds that gate the build. 02_generate_synthetic.sql asserts the
# calibration targets in the use case spec; these are the framework-level
# tolerances applied to them.
tolerances:
  # How close the doubly-robust estimate must land to the planted true ATE.
  dr_relative_error_max: 0.10
  # How wrong the naive estimate must be for the synthetic use case to show the failure.
  naive_relative_error_min: 0.50
```

### `pyproject.toml`

Copy code

```
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "causal-decision-framework"
version = "0.1.0"
description = "Domain-blind counterfactual decision framework on Snowflake"
requires-python = ">=3.10"
dependencies = [
    "snowflake-snowpark-python>=1.24.0",
    "econml==0.15.0",
    "scikit-learn==1.4.2",
    "statsmodels==0.14.6",
    "numpy==1.26.4",
    "pandas==2.3.3",
    "pyyaml>=6.0",
]

# dowhy is deliberately absent. It requires numpy>2 while econml requires
# numpy<2, so the two cannot share an environment. dowhy is reached by calling
# AGENT.REFUTE_ESTIMATE, which runs in its own isolated stored procedure.
# See docs/runtime-and-packages.md.

[tool.setuptools]
package-dir = {"" = "framework"}

[tool.setuptools.packages.find]
where = ["framework"]
include = ["causal_core*"]

# Ruff settings for this pattern only. The repo root has no ruff config, so
# defaults apply everywhere else, and this file is the nearest config for
# anything underneath it. Nothing here changes a rule or the line length; it
# only carves out the generated notebooks.
[tool.ruff]
# pre-commit passes file paths explicitly, and ruff ignores `exclude` for
# explicit paths unless this is set. Without it the format exclude below is
# silently inert under the hook, which is the failure mode this whole block
# exists to prevent.
force-exclude = true

[tool.ruff.format]
# The .ipynb files are BUILD ARTIFACTS of framework/render_notebooks.py, whose
# cell bodies are plain strings. Formatting them here and regenerating them
# there produce different bytes, so leaving both enabled means every commit
# churns the notebooks and neither tool ever wins. The generator owns their
# shape; run it, do not reformat its output.
exclude = ["notebooks/*.ipynb"]

# Linting stays ON for the notebooks, because it still catches real errors in a
# cell (an undefined name, a bad comparison). Only the two rules that flag
# correct dual-mode idioms are silenced:
#
#   E402  The bootstrap must walk up the tree and set sys.path before
#         `causal_core` is importable at all, so those imports cannot come first.
#   F401  The bootstrap imports the full working set from causal_core once so
#         every notebook has the same names available interactively. Not every
#         notebook uses every name.
[tool.ruff.lint.per-file-ignores]
"notebooks/*.ipynb" = ["E402", "F401"]
```

### `pytest.ini`

Copy code

```
[pytest]
testpaths = tests
pythonpath = framework tests
markers =
    snowflake: requires a live Snowflake connection and the deployed fixture
    slow: takes more than a few seconds
filterwarnings =
    ignore::FutureWarning
    ignore::DeprecationWarning
```

### `requirements.txt`

```
# Local development only. Inside Snowflake, packages resolve from the Anaconda
# channel (warehouse procs, Streamlit) or the PyPI artifact repository (dowhy
# proc only). See docs/runtime-and-packages.md.
#
# IMPORTANT: do NOT add dowhy here. dowhy requires numpy>2 and econml requires
# numpy<2, so they cannot coexist in one environment. dowhy is reached by
# CALLing AGENT.REFUTE_ESTIMATE, which runs in its own isolated procedure.

snowflake-snowpark-python>=1.24.0
snowflake-ml-python>=1.9.2
snowflake-connector-python>=3.12.0

# Pinned to match the Snowflake Anaconda channel versions verified in the
# account, so local results reproduce what the warehouse produces.
econml==0.15.0
scikit-learn==1.4.2
statsmodels==0.14.6
numpy==1.26.4
pandas==2.3.3
scipy>=1.11

pyyaml>=6.0
matplotlib>=3.8

# econml 0.15.0 imports pkg_resources at fit time (econml/utilities.py,
# one_hot_encoder). Modern virtualenvs do not ship setuptools, so without this
# CausalForestDML.fit() dies with ModuleNotFoundError: No module named
# 'pkg_resources'. Pinned below 81 because pkg_resources is removed there.
setuptools<81
```

## `agent/`

### `agent/01_tools.sql`

Copy code

```
-- =====================================================================
-- Agent tools.
--
-- One file, deployed per use case. @DATABASE@ is substituted at deploy time by
-- framework/deploy_agent.py along with @UNIT_ID@ and @UNIT_LABEL@, which is why
-- every table reference below is fully
-- qualified: a stored procedure called from a Cortex Agent cannot rely on the
-- caller's session having the right database set.
--
-- DESIGN RULES, and the reasoning behind each.
--
-- 1. Tools READ from MODELS.*, they never fit a model. Fitting happens once in
--    notebook 02 and is persisted. This is not a performance choice. It is what
--    guarantees that a number quoted in chat, a number on the Streamlit console,
--    and a number in the notebook are the same number. Recomputation is how those
--    three drift apart.
--
-- 2. Every tool that returns an estimate also returns the caveat that belongs to
--    it, in the SAME object. An LLM handed {"net_value": 5185691} will quote it
--    without qualification. Handed {"net_value": ..., "identified": false,
--    "refusal": "..."} it has to deal with the caveat to use the number at all.
--
-- 3. Cohort filters are STRUCTURED, never raw SQL. The agent passes
--    {"INSURANCE_TYPE": "DUAL", "AGE": {"min": 65}} and the procedure validates
--    every column against INFORMATION_SCHEMA and binds every value. An LLM
--    writing a WHERE clause into a procedure that runs as owner is an injection
--    vector, and "it is only sample code" is how that pattern reaches production.
--
-- 4. Tools cap their own output. A large tool result costs orchestration tokens,
--    and a truncated JSON payload is worse than a small one because the model
--    will confidently read the fragment.
--
-- Packages come from the Anaconda channel only. Nothing here imports econml or
-- dowhy; per-unit effects are already in MODELS.CATE_SCORES. The one procedure
-- that does need dowhy is deployed separately, in 03_refute.sql, because dowhy and
-- econml cannot coexist in one environment.
-- =====================================================================

-- WHY EXECUTE AS OWNER. Each tool is the only sanctioned path from the agent to
-- the estimates. With owner's rights, a user role needs USAGE on the procedure
-- and nothing on DATA or MODELS, so it can ask the agent but cannot run the raw
-- treated-versus-untreated comparison itself (sql/10_agent_user_role.sql grants
-- exactly that). The trade-off: anyone with USAGE on a procedure reads these
-- tables with the OWNER's privileges, so grant USAGE only to the intended role.
-- See Gotchas in the README.
--
-- COPY GRANTS on each procedure keeps those USAGE grants across re-deploys.
--
-- NOTE on changing a signature. Snowflake keys procedures by argument types, so
-- CREATE OR REPLACE with a different parameter type creates an ADDITIONAL overload
-- rather than replacing the old one. An agent then sees two tools with the same name
-- and different schemas. If you change a parameter type here, DROP the old signature
-- explicitly.
--
USE DATABASE @DATABASE@;
USE SCHEMA AGENT;

-- ---------------------------------------------------------------------
-- Shared helpers (_identification, _parse_cohort, _validate_cohort), inlined
-- into the two procedures that take a cohort: CHECK_IDENTIFICATION and
-- RUN_SCENARIO.
--
-- Kept inline rather than in a separate module because a Snowflake stored
-- procedure with inline code cannot import a sibling procedure. The
-- alternative is a stage-based package, which adds a build step for about 150
-- lines.
-- ---------------------------------------------------------------------

CREATE OR REPLACE PROCEDURE AGENT.EXPLAIN_ASSUMPTIONS()
COPY GRANTS
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python')
HANDLER = 'run'
EXECUTE AS OWNER
AS
$$
def run(session):
    """State what must be true for the estimates to mean anything.

    Deliberately the first tool in the agent's list. An agent that can produce a
    treatment effect but cannot say what it assumed is a liability, because the
    assumptions are where these estimates actually fail.
    """
    diag = session.sql("""
        SELECT METHOD, ESTIMATE, CI_LOW, CI_HIGH, IDENTIFIED, VERDICT, TARGET
        FROM @DATABASE@.MODELS.DIAGNOSTICS
        ORDER BY METHOD
    """).collect()

    if not diag:
        return ("No estimates have been produced yet. Run notebook 02 "
                "(02_causal.ipynb) before asking about effects.")

    lines = [
        "WHAT THESE ESTIMATES ASSUME",
        "",
        "1. No unmeasured confounding (for the AIPW and causal-forest numbers).",
        "   Every factor that drives BOTH treatment assignment and the outcome must",
        "   be in the covariate set. This is an assumption, not a finding, and it",
        "   cannot be verified from the data. It can only be argued from how",
        "   treatment was assigned, and probed with refutation tests.",
        "",
        "2. Common support. Treated and untreated units must be comparable. Where",
        "   propensity approaches 0 or 1 there is no counterfactual to compare",
        "   against and no method recovers an effect. Ask CHECK_IDENTIFICATION",
        "   before trusting any number for a narrow cohort.",
        "",
        "3. Parallel trends (for the difference-in-differences number only). Absent",
        "   treatment, treated and untreated groups would have moved together. This",
        "   one IS partly testable, via the pre-treatment trend.",
        "",
        "4. No interference. One unit's treatment does not change another's outcome.",
        "",
        "CURRENT ESTIMATES",
        "",
    ]
    for r in diag:
        est = "n/a" if r["ESTIMATE"] is None else f"{r['ESTIMATE']:+.4f}"
        ci = ""
        if r["CI_LOW"] is not None and r["CI_HIGH"] is not None:
            ci = f"  95% CI [{r['CI_LOW']:+.4f}, {r['CI_HIGH']:+.4f}]"
        flag = "" if r["IDENTIFIED"] else "   <-- NOT IDENTIFIED"
        lines.append(f"  {r['METHOD']:<28} {est}{ci}{flag}")
        if r["VERDICT"]:
            lines.append(f"      {r['VERDICT']}")

    lines += [
        "",
        "HOW TO READ THE SPREAD BETWEEN METHODS",
        "",
        "These methods do not disagree because one is broken. They target different",
        "quantities under different assumptions. The raw difference is not an effect",
        "estimate at all, it is the selection pattern plus the effect, and it is",
        "reported only to show what the naive answer would have been.",
    ]
    return "\n".join(lines)
$$;

CREATE OR REPLACE PROCEDURE AGENT.CHECK_IDENTIFICATION(COHORT_JSON STRING)
COPY GRANTS
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python', 'pandas', 'numpy')
HANDLER = 'run'
EXECUTE AS OWNER
AS
$$
import json

ALLOWED_OPS = {"min", "max"}

def _identification(session, where, binds, description):
    """Decide whether this cohort supports an honest estimate.

    MIRRORS causal_core.causal.is_identified EXACTLY, and must keep doing so. An
    earlier version of this procedure invented its own rule (at least 80% of the
    cohort with propensity in [0.05, 0.95]) and consequently refused to answer for
    the FULL population that notebook 02 had already reported an estimate for. An
    agent that applies a stricter standard than the pipeline behind it is not being
    careful, it is being inconsistent, and the user cannot tell which number to
    believe.

    The rule that matters is the share of TREATED units with propensity above 0.95.
    Those are the units with no plausible untreated counterpart. A large number of
    untreated units at very low propensity is normal when treatment is rare and does
    not threaten identification; it is the treated units off the end of the support
    that do.
    """
    r = session.sql(
        f"""
        SELECT
            COUNT(*)                                                    AS N,
            SUM(c.TREATED)                                              AS N_TREATED,
            SUM(IFF(c.TREATED = 1 AND c.PROPENSITY > 0.95, 1, 0))       AS N_TREATED_EXTREME,
            MIN(c.PROPENSITY)                                           AS MIN_PS,
            MAX(c.PROPENSITY)                                           AS MAX_PS,
            MAX(IFF(c.TREATED = 1, c.PROPENSITY, NULL))                 AS MAX_PS_TREATED,
            MIN(IFF(c.TREATED = 0, c.PROPENSITY, NULL))                 AS MIN_PS_CONTROL
        FROM @DATABASE@.MODELS.CATE_SCORES c
        JOIN @DATABASE@.DATA.UNIT u USING (@UNIT_ID@)
        WHERE {where}
        """,
        params=binds,
    ).collect()[0]

    n = int(r["N"] or 0)
    if n == 0:
        return {
            "identified": False,
            "n": 0,
            "cohort": description,
            "reason": f"no units match {description}",
        }

    n_treated = int(r["N_TREATED"] or 0)
    extreme_share = (int(r["N_TREATED_EXTREME"] or 0) / n_treated) if n_treated else 1.0

    reasons = []
    # Same thresholds as is_identified(max_extreme_share=0.25).
    if extreme_share > 0.25:
        reasons.append(
            f"{extreme_share:.1%} of treated units have a propensity above 0.95, so "
            "there is effectively no comparable untreated group"
        )
    if n_treated < 100:
        reasons.append(f"only {n_treated} treated units, too few for a stable estimate")

    return {
        "identified": not reasons,
        "n": n,
        "n_treated": n_treated,
        "n_untreated": n - n_treated,
        "cohort": description,
        "share_treated_without_counterpart": round(extreme_share, 4),
        "propensity_range": [round(float(r["MIN_PS"]), 4), round(float(r["MAX_PS"]), 4)],
        "reason": "; ".join(reasons),
    }

def _parse_cohort(cohort_json):
    """Parse the cohort argument, which arrives as a JSON string.

    A STRING rather than an OBJECT/VARIANT parameter because Cortex custom tools do
    not support object-typed parameters. That constraint is not obvious until an
    agent silently fails to call the tool, so the signature is STRING everywhere and
    parsing happens here.

    Also absorbs the SQL NULL problem: Snowflake hands a SQL NULL to a Python
    procedure as a `sqlNullWrapper` instance, not as Python None, and that object is
    truthy. A plain falsiness check therefore treats an explicit NULL as a malformed
    argument, which is how CALL ...(NULL) first came back as an error instead of a
    population-level answer.

    Returns (cohort_dict, error_message). An absent cohort yields {}, meaning the
    whole population.
    """
    if cohort_json is None or type(cohort_json).__name__ == "sqlNullWrapper":
        return {}, None

    text = str(cohort_json).strip()
    if not text or text.lower() in {"null", "none", "{}"}:
        return {}, None

    try:
        parsed = json.loads(text)
    except (ValueError, TypeError) as exc:
        return None, (
            f"cohort must be valid JSON, for example "
            '{"INSURANCE_TYPE": "DUAL", "AGE": {"min": 65}}. Parse error: ' + str(exc)
        )

    if parsed is None:
        return {}, None
    if not isinstance(parsed, dict):
        return None, (
            "cohort must be a JSON object mapping column names to a value or to "
            '{"min": x, "max": y}. Received a ' + type(parsed).__name__
        )
    return parsed, None

def _validate_cohort(session, cohort):
    """Turn a structured cohort spec into a validated WHERE clause plus bindings.

    Returns (where_sql, bind_values, description, error).

    Every column is checked against INFORMATION_SCHEMA and every value is bound,
    so a hallucinated column name produces a clean error and a malicious string
    produces a literal rather than SQL. The agent never gets to write SQL.
    """
    if not cohort:
        return "TRUE", [], "the whole population", None

    if not isinstance(cohort, dict):
        return None, None, None, (
            "cohort must be an object mapping column names to either a value or "
            '{"min": x, "max": y}. Received: ' + type(cohort).__name__
        )

    known = {
        r["COLUMN_NAME"].upper(): r["DATA_TYPE"]
        for r in session.sql("""
            SELECT COLUMN_NAME, DATA_TYPE
            FROM @DATABASE@.INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'DATA' AND TABLE_NAME = 'UNIT'
        """).collect()
    }

    clauses, binds, described = [], [], []
    for raw_col, condition in cohort.items():
        col = str(raw_col).upper()
        if col not in known:
            return None, None, None, (
                f"unknown column '{raw_col}'. Available columns on DATA.UNIT are: "
                + ", ".join(sorted(known))
            )
        if isinstance(condition, dict):
            bad = set(condition) - ALLOWED_OPS
            if bad:
                return None, None, None, (
                    f"unsupported operators {sorted(bad)} for column '{col}'. "
                    f"Only {sorted(ALLOWED_OPS)} are supported."
                )
            for op, value in condition.items():
                clauses.append(f'u."{col}" {">=" if op == "min" else "<="} ?')
                binds.append(value)
                described.append(f"{col} {'at least' if op == 'min' else 'at most'} {value}")
        else:
            clauses.append(f'u."{col}" = ?')
            binds.append(condition)
            described.append(f"{col} = {condition}")

    return " AND ".join(clauses), binds, " and ".join(described), None

def run(session, cohort_json):
    """Decide whether an honest effect estimate exists for this cohort.

    This is the procedure that lets the agent say no. It is a separate tool from the
    scenario procedures on purpose, so the agent can be instructed to call it first
    and so a refusal is a first-class answer rather than an error path.

    Overlap is judged on the cohort's OWN propensity distribution, not inherited
    from the population. A population with adequate average overlap can still
    contain slices with none, and those slices are exactly the ones people ask
    about.
    """
    cohort, parse_error = _parse_cohort(cohort_json)
    if parse_error:
        return {"ok": False, "error": parse_error}

    where, binds, description, error = _validate_cohort(session, cohort)
    if error:
        return {"ok": False, "error": error}

    result = _identification(session, where, binds, description)
    out = {"ok": True, **result}

    if result["n"] == 0:
        out["refusal"] = (
            f"No units match {description}. There is nothing to estimate. Do not "
            "report an effect for this cohort."
        )
    elif result["identified"]:
        out["verdict"] = (
            f"Identified. {description} has {result['n']:,} units "
            f"({result['n_treated']:,} treated) with adequate overlap, so a causal "
            "estimate is defensible for this cohort, subject to the "
            "no-unmeasured-confounding assumption that EXPLAIN_ASSUMPTIONS describes."
        )
    else:
        out["refusal"] = (
            f"NOT identified for {description}: {result['reason']}. Report this "
            "refusal to the user. Do NOT substitute the population-level estimate "
            "for this cohort, and do not present a number as approximate or "
            "indicative. Without comparable untreated units no method recovers the "
            "effect, so any figure would be an extrapolation from the model rather "
            "than a measurement."
        )
    return out
$$;

CREATE OR REPLACE PROCEDURE AGENT.RUN_SCENARIO(
    CAPACITY INT,
    COHORT_JSON STRING,
    RESPECT_EQUITY BOOLEAN
)
COPY GRANTS
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python', 'pandas', 'numpy')
HANDLER = 'run'
EXECUTE AS OWNER
AS
$$
import json

import numpy as np
import pandas as pd

ALLOWED_OPS = {"min", "max"}

def _identification(session, where, binds, description):
    """Decide whether this cohort supports an honest estimate.

    MIRRORS causal_core.causal.is_identified EXACTLY, and must keep doing so. An
    earlier version of this procedure invented its own rule (at least 80% of the
    cohort with propensity in [0.05, 0.95]) and consequently refused to answer for
    the FULL population that notebook 02 had already reported an estimate for. An
    agent that applies a stricter standard than the pipeline behind it is not being
    careful, it is being inconsistent, and the user cannot tell which number to
    believe.

    The rule that matters is the share of TREATED units with propensity above 0.95.
    Those are the units with no plausible untreated counterpart. A large number of
    untreated units at very low propensity is normal when treatment is rare and does
    not threaten identification; it is the treated units off the end of the support
    that do.
    """
    r = session.sql(
        f"""
        SELECT
            COUNT(*)                                                    AS N,
            SUM(c.TREATED)                                              AS N_TREATED,
            SUM(IFF(c.TREATED = 1 AND c.PROPENSITY > 0.95, 1, 0))       AS N_TREATED_EXTREME,
            MIN(c.PROPENSITY)                                           AS MIN_PS,
            MAX(c.PROPENSITY)                                           AS MAX_PS,
            MAX(IFF(c.TREATED = 1, c.PROPENSITY, NULL))                 AS MAX_PS_TREATED,
            MIN(IFF(c.TREATED = 0, c.PROPENSITY, NULL))                 AS MIN_PS_CONTROL
        FROM @DATABASE@.MODELS.CATE_SCORES c
        JOIN @DATABASE@.DATA.UNIT u USING (@UNIT_ID@)
        WHERE {where}
        """,
        params=binds,
    ).collect()[0]

    n = int(r["N"] or 0)
    if n == 0:
        return {
            "identified": False,
            "n": 0,
            "cohort": description,
            "reason": f"no units match {description}",
        }

    n_treated = int(r["N_TREATED"] or 0)
    extreme_share = (int(r["N_TREATED_EXTREME"] or 0) / n_treated) if n_treated else 1.0

    reasons = []
    # Same thresholds as is_identified(max_extreme_share=0.25).
    if extreme_share > 0.25:
        reasons.append(
            f"{extreme_share:.1%} of treated units have a propensity above 0.95, so "
            "there is effectively no comparable untreated group"
        )
    if n_treated < 100:
        reasons.append(f"only {n_treated} treated units, too few for a stable estimate")

    return {
        "identified": not reasons,
        "n": n,
        "n_treated": n_treated,
        "n_untreated": n - n_treated,
        "cohort": description,
        "share_treated_without_counterpart": round(extreme_share, 4),
        "propensity_range": [round(float(r["MIN_PS"]), 4), round(float(r["MAX_PS"]), 4)],
        "reason": "; ".join(reasons),
    }

def _parse_cohort(cohort_json):
    """Parse the cohort argument, which arrives as a JSON string.

    A STRING rather than an OBJECT/VARIANT parameter because Cortex custom tools do
    not support object-typed parameters. That constraint is not obvious until an
    agent silently fails to call the tool, so the signature is STRING everywhere and
    parsing happens here.

    Also absorbs the SQL NULL problem: Snowflake hands a SQL NULL to a Python
    procedure as a `sqlNullWrapper` instance, not as Python None, and that object is
    truthy. A plain falsiness check therefore treats an explicit NULL as a malformed
    argument, which is how CALL ...(NULL) first came back as an error instead of a
    population-level answer.

    Returns (cohort_dict, error_message). An absent cohort yields {}, meaning the
    whole population.
    """
    if cohort_json is None or type(cohort_json).__name__ == "sqlNullWrapper":
        return {}, None

    text = str(cohort_json).strip()
    if not text or text.lower() in {"null", "none", "{}"}:
        return {}, None

    try:
        parsed = json.loads(text)
    except (ValueError, TypeError) as exc:
        return None, (
            f"cohort must be valid JSON, for example "
            '{"INSURANCE_TYPE": "DUAL", "AGE": {"min": 65}}. Parse error: ' + str(exc)
        )

    if parsed is None:
        return {}, None
    if not isinstance(parsed, dict):
        return None, (
            "cohort must be a JSON object mapping column names to a value or to "
            '{"min": x, "max": y}. Received a ' + type(parsed).__name__
        )
    return parsed, None

def _validate_cohort(session, cohort):
    if not cohort:
        return "TRUE", [], "the whole population", None
    if not isinstance(cohort, dict):
        return None, None, None, (
            "cohort must be an object mapping column names to a value or "
            '{"min": x, "max": y}'
        )
    known = {
        r["COLUMN_NAME"].upper()
        for r in session.sql("""
            SELECT COLUMN_NAME FROM @DATABASE@.INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'DATA' AND TABLE_NAME = 'UNIT'
        """).collect()
    }
    clauses, binds, described = [], [], []
    for raw_col, condition in cohort.items():
        col = str(raw_col).upper()
        if col not in known:
            return None, None, None, (
                f"unknown column '{raw_col}'. Available: " + ", ".join(sorted(known))
            )
        if isinstance(condition, dict):
            bad = set(condition) - ALLOWED_OPS
            if bad:
                return None, None, None, f"unsupported operators {sorted(bad)}"
            for op, value in condition.items():
                clauses.append(f'u."{col}" {">=" if op == "min" else "<="} ?')
                binds.append(value)
                described.append(f"{col} {'>=' if op == 'min' else '<='} {value}")
        else:
            clauses.append(f'u."{col}" = ?')
            binds.append(condition)
            described.append(f"{col} = {condition}")
    return " AND ".join(clauses), binds, " and ".join(described), None

def run(session, capacity, cohort_json, respect_equity):
    """Project the outcome of treating `capacity` units within a cohort.

    Refuses before it computes. The identification check runs first and returns a
    refusal instead of a number, because a tool that returns both a number and a
    warning invites the model to quote the number and drop the warning.
    """
    if capacity is None or capacity <= 0:
        return {"ok": False, "error": "capacity must be a positive integer"}

    cohort, parse_error = _parse_cohort(cohort_json)
    if parse_error:
        return {"ok": False, "error": parse_error}

    where, binds, description, error = _validate_cohort(session, cohort)
    if error:
        return {"ok": False, "error": error}

    ident = _identification(session, where, binds, description)
    n_cohort = ident["n"]
    if not ident["identified"]:
        return {
            "ok": True,
            "refused": True,
            "cohort": description,
            "reason": ident["reason"],
            "identification": ident,
            "refusal": (
                f"Refusing to project a scenario for {description}: "
                f"{ident['reason']}. "
                "Report this refusal verbatim. Do not fall back to the "
                "population-level estimate, and do not present a number as a rough "
                "guide. There is no comparable untreated group in this cohort."
            ),
        }

    scores = session.sql(
        f"""
        SELECT c.BENEFIT, c.VALUE_PER_UNIT, c.COST_PER_UNIT, c.NET_VALUE_PER_UNIT
        FROM @DATABASE@.MODELS.CATE_SCORES c
        JOIN @DATABASE@.DATA.UNIT u USING (@UNIT_ID@)
        WHERE {where}
        """,
        params=binds,
    ).to_pandas()

    take = int(min(capacity, len(scores)))
    chosen = scores.nlargest(take, "BENEFIT")

    cost = float(chosen["COST_PER_UNIT"].sum())
    gross = float(chosen["VALUE_PER_UNIT"].sum())
    out = {
        "ok": True,
        "refused": False,
        "cohort": description,
        "cohort_size": n_cohort,
        "units_treated": take,
        "capacity_requested": int(capacity),
        "expected_events_avoided_or_gained": round(float(chosen["BENEFIT"].sum()), 2),
        "program_cost": round(cost, 2),
        "expected_gross_value": round(gross, 2),
        "expected_net_value": round(gross - cost, 2),
        "roi": round((gross - cost) / cost, 3) if cost else None,
        "units_with_positive_net_value": int((scores["NET_VALUE_PER_UNIT"] > 0).sum()),
        "basis": (
            "Projected from per-unit effects in MODELS.CATE_SCORES, estimated by a "
            "causal forest. These are ESTIMATES with real uncertainty, not "
            "guarantees, and they assume no unmeasured confounding."
        ),
    }
    if take < capacity:
        out["note"] = (
            f"Requested capacity {capacity:,} exceeds the cohort size {n_cohort:,}, "
            f"so only {take:,} units could be treated."
        )
    if respect_equity:
        out["equity"] = _equity_status(session)
    return out

def _equity_status(session):
    """Report the persisted gate result rather than recomputing an allocation.

    The agent should not be able to invent a new allocation policy on the fly and
    claim it is fair. It reports what the pipeline actually gated on.
    """
    rows = session.sql("""
        SELECT ATTRIBUTE, MAX(OBSERVED_RATIO) AS RATIO,
               MAX(THRESHOLD) AS THRESHOLD, MIN(IFF(PASSED, 1, 0)) AS PASSED
        FROM @DATABASE@.MODELS.EQUITY_REPORT
        GROUP BY ATTRIBUTE ORDER BY ATTRIBUTE
    """).collect()
    if not rows:
        return {
            "available": False,
            "note": "No equity report has been written. Run notebook 03.",
        }
    return {
        "available": True,
        "policy_gated": "equity_constrained_uplift",
        "attributes": [
            {
                "attribute": r["ATTRIBUTE"],
                "disparity_ratio": round(float(r["RATIO"]), 3),
                "threshold": float(r["THRESHOLD"]),
                "passed": bool(r["PASSED"]),
            }
            for r in rows
        ],
        "note": (
            "These ratios describe the allocation policy the pipeline gated on. A "
            "scenario that treats a different set of units has NOT been gated, and "
            "its fairness is unknown until notebook 03 is re-run for it."
        ),
    }
$$;

CREATE OR REPLACE PROCEDURE AGENT.OPTIMIZE_ALLOCATION(MAX_BUDGET FLOAT)
COPY GRANTS
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python', 'pandas', 'numpy')
HANDLER = 'run'
EXECUTE AS OWNER
AS
$$
import numpy as np

def run(session, max_budget):
    """Find the spend level that maximizes expected net value.

    The answer is almost never "spend the whole budget". Marginal net value falls
    as you move down the ranking, and the optimum is where it crosses zero. A tool
    that only answers "who are the top N" cannot express that, which is why this
    exists separately from RUN_SCENARIO.
    """
    scores = session.sql("""
        SELECT NET_VALUE_PER_UNIT, COST_PER_UNIT
        FROM @DATABASE@.MODELS.CATE_SCORES
        ORDER BY NET_VALUE_PER_UNIT DESC
    """).to_pandas()

    if scores.empty:
        return {"ok": False, "error": "MODELS.CATE_SCORES is empty. Run notebook 02."}

    unit_cost = float(scores["COST_PER_UNIT"].iloc[0])
    cumulative_net = scores["NET_VALUE_PER_UNIT"].cumsum().to_numpy()

    # Unconstrained optimum: treat while the next unit still adds value.
    n_profitable = int((scores["NET_VALUE_PER_UNIT"] > 0).sum())

    budget_cap = None
    if max_budget is not None and max_budget > 0 and unit_cost > 0:
        budget_cap = int(max_budget // unit_cost)

    recommended = n_profitable if budget_cap is None else min(n_profitable, budget_cap)
    recommended = max(recommended, 0)

    out = {
        "ok": True,
        "recommended_units_to_treat": recommended,
        "recommended_spend": round(recommended * unit_cost, 2),
        "expected_net_value": round(float(cumulative_net[recommended - 1]), 2)
        if recommended > 0
        else 0.0,
        "cost_per_unit": unit_cost,
        "units_with_positive_expected_value": n_profitable,
        "population": int(len(scores)),
    }

    if budget_cap is not None:
        out["budget_allows_units"] = budget_cap
        if budget_cap < n_profitable:
            forgone = float(cumulative_net[n_profitable - 1] - cumulative_net[budget_cap - 1])
            out["binding_constraint"] = "budget"
            out["value_forgone_to_budget"] = round(forgone, 2)
            out["interpretation"] = (
                f"The budget binds. {n_profitable:,} units are worth treating but the "
                f"budget covers {budget_cap:,}, leaving about "
                f"{forgone:,.0f} of expected value on the table. Raising the budget "
                "is justified on these estimates."
            )
        else:
            out["binding_constraint"] = "value"
            out["unspent_budget"] = round(max_budget - recommended * unit_cost, 2)
            out["interpretation"] = (
                f"The budget does NOT bind. Only {n_profitable:,} units have positive "
                f"expected net value, so treating more would destroy value. Do not "
                "spend the remainder on this intervention."
            )
    else:
        out["interpretation"] = (
            f"{n_profitable:,} of {len(scores):,} units have positive expected net "
            "value. Treating beyond that reduces total value."
        )

    if n_profitable == 0:
        out["interpretation"] = (
            "NO units have positive expected net value at the current cost. On these "
            "estimates the intervention does not pay for itself for anyone, and the "
            "defensible recommendation is not to run it, or to reduce its unit cost. "
            "Note that unmeasured confounding attenuates estimated effects, so a "
            "genuinely worthwhile programme can look unworthwhile here."
        )

    out["caveat"] = (
        "Based on estimated effects, which carry uncertainty and assume no "
        "unmeasured confounding. Treat as a planning figure, not a forecast."
    )
    return out
$$;

CREATE OR REPLACE PROCEDURE AGENT.COMPARE_TARGETING_STRATEGIES()
COPY GRANTS
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python', 'pandas', 'numpy')
HANDLER = 'run'
EXECUTE AS OWNER
AS
$$
def run(session):
    """Report the persisted ranking comparison: does uplift targeting beat risk?

    Reads MODELS.QINI_CURVE rather than recomputing, so the answer matches the
    notebook and the console exactly.
    """
    rows = session.sql("""
        SELECT MODEL,
               MAX(AUUC)  AS AUUC,
               MAX(QINI)  AS PEAK_QINI
        FROM @DATABASE@.MODELS.QINI_CURVE
        GROUP BY MODEL
        -- Ordinal, not ORDER BY MAX(AUUC): the output alias AUUC shadows the column,
        -- so Snowflake reads that as MAX(MAX(AUUC)) and rejects the nested aggregate.
        ORDER BY 2 DESC
    """).collect()

    if not rows:
        return {
            "ok": False,
            "error": "MODELS.QINI_CURVE is empty. Run notebook 03 first.",
        }

    equity = session.sql("""
        SELECT ATTRIBUTE, MAX(OBSERVED_RATIO) AS RATIO, MAX(THRESHOLD) AS THRESHOLD,
               MIN(IFF(PASSED, 1, 0)) AS PASSED
        FROM @DATABASE@.MODELS.EQUITY_REPORT GROUP BY ATTRIBUTE ORDER BY ATTRIBUTE
    """).collect()

    return {
        "ok": True,
        "rankings_evaluated": [
            {
                "model": r["MODEL"],
                # The headline number. Positive beats random, zero is no signal,
                # NEGATIVE is worse than random and is a real outcome for risk
                # ranking. Report the sign explicitly.
                "auuc": round(float(r["AUUC"]), 4),
                "peak_qini": round(float(r["PEAK_QINI"]), 3),
                "verdict": (
                    "beats random" if float(r["AUUC"]) > 0.02
                    else "no better than random" if float(r["AUUC"]) >= -0.02
                    else "WORSE than random"
                ),
            }
            for r in rows
        ],
        "equity_gate": [
            {
                "attribute": r["ATTRIBUTE"],
                "disparity_ratio": round(float(r["RATIO"]), 3),
                "threshold": float(r["THRESHOLD"]),
                "passed": bool(r["PASSED"]),
            }
            for r in equity
        ],
        "how_to_read": (
            "The Qini curve measures incremental outcome from treating the top-ranked "
            "units, computed from OBSERVED outcomes rather than ground truth, so it is "
            "the one evaluation here that would work on real data. A ranking that "
            "tracks the random line carries no signal. Because treatment was assigned "
            "observationally rather than randomised, use these curves to compare "
            "rankings against each other, not to read an absolute effect. AUUC is the "
            "summary: positive beats random, zero means no signal, and NEGATIVE means "
            "the ranking is actively worse than random. If a ranking is negative, say "
            "so plainly rather than describing it as merely weaker."
        ),
    }
$$;
```

### `agent/02_agent.sql`

Copy code

```
-- =====================================================================
-- The Cortex Agent.
--
-- Deployed by framework/deploy_agent.py with @DATABASE@ substituted.
--
-- COPY GRANTS keeps any USAGE granted on the agent (sql/10_agent_user_role.sql)
-- when this file is re-deployed. A plain CREATE OR REPLACE AGENT drops every
-- grant on the object. COPY GRANTS must come after COMMENT and PROFILE, right
-- before FROM SPECIFICATION; placed straight after the agent name, ahead of
-- COMMENT, it fails to parse ("unexpected 'COMMENT'"). That differs from the
-- published syntax, which lists COPY GRANTS first:
-- https://docs.snowflake.com/en/sql-reference/sql/create-agent
--
-- The orchestration instructions are the substantive part of this file, not
-- boilerplate. The tools can refuse, but a tool that returns a refusal is only
-- useful if the orchestrator honours it, and the default behaviour of a capable
-- model handed a refusal plus a population-level estimate is to helpfully offer the
-- population number as an approximation. That is precisely the failure this whole
-- pipeline exists to prevent, so the instructions forbid it explicitly and by name.
--
-- Note the deliberate omission: no cortex_analyst tool. Text-to-SQL over these
-- tables would let the agent compute a raw treated-vs-untreated difference and
-- present it as an effect. On this data that answer is +0.0846 when the truth is
-- -0.0452, i.e. confidently backwards. Restricting the agent to procedures that
-- encapsulate the correct estimator is a feature.
-- =====================================================================

USE DATABASE @DATABASE@;
USE SCHEMA AGENT;

CREATE OR REPLACE AGENT @DATABASE@.AGENT.DECISION_AGENT
  COMMENT = 'Counterfactual decision agent. Answers what-if questions about @UNIT_LABEL@ using causal estimates, and refuses when the data cannot support an answer.'
  PROFILE = '{"display_name": "Causal Decision Agent", "color": "blue"}'
  COPY GRANTS
  FROM SPECIFICATION
$$
models:
  orchestration: auto

orchestration:
  budget:
    seconds: 120
    tokens: 32000

instructions:
  response: |
    Be concise and concrete. Lead with the number the user asked for, then state
    what it assumes.

    Always distinguish an ESTIMATE from a MEASUREMENT. These figures come from
    observational data with a causal model on top, not from a randomised
    experiment. Say "estimated" and give the uncertainty when you have it.

    Never present the raw treated-versus-untreated difference as a treatment
    effect. On this data that comparison has the WRONG SIGN, because units were
    selected for treatment on the basis of the very outcome being measured. If a
    user quotes such a number, explain why it is misleading rather than
    reconciling it.

    When a tool returns a refusal, report it as the answer. Do not soften it, do
    not substitute a number from a wider population, and do not describe an
    unavailable estimate as "roughly" or "approximately" anything. A refusal is a
    correct and complete answer.

    Money and counts: round sensibly and state the unit. Do not imply precision
    that estimated effects do not have.

  orchestration: |
    Tool selection rules, in priority order.

    1. If the user asks about a SPECIFIC SUBGROUP or cohort (an insurance type, a
       region, an age band, a severity level, a market, a price tier), call
       check_identification FIRST with that cohort before any other tool. If it
       returns identified=false, report the refusal and STOP. Do not call
       run_scenario for that cohort, and do not answer from the population-level
       estimate.

    2. For "what happens if we treat N units" or "what if we expand or cut the
       programme", use run_scenario. Pass the cohort as a JSON string, or omit it
       for the whole population.

    3. For "how many should we treat", "what is the optimal budget", "should we
       spend more", use optimize_allocation. This tool answers whether the budget
       or the value ceiling is the binding constraint, which is usually the real
       question behind a budget request.

    4. For "does our targeting work", "should we target by risk", "is the model
       better than what we do today", use compare_targeting_strategies.

    5. For "why should I believe this", "what are the assumptions", "how was this
       estimated", or any challenge to validity, use explain_assumptions.

    6. If the user challenges the result, asks how robust it is, or is about to
       commit budget, call refute_estimate. Report its verdict WITH its caveat: a
       pass is weak evidence, not validation.

    7. If a user asks a question that would require a raw comparison of treated
       versus untreated outcomes, do NOT attempt it. Explain that the comparison is
       confounded and use explain_assumptions to show why.

    Always call explain_assumptions before giving a final answer to a question
    that will inform a funding or policy decision, and fold its caveats into the
    response.

  sample_questions:
    - question: "What would happen if we could enroll 3,000 more @UNIT_LABEL@?"
    - question: "How many should we treat to maximize net value?"
    - question: "Is targeting by risk score good enough, or do we need the causal model?"
    - question: "What is the effect for the sickest cohort, with 7 or more comorbidities?"
    - question: "Why should I believe these numbers?"

tools:
  - tool_spec:
      type: "generic"
      name: "check_identification"
      description: |
        Decide whether a defensible causal estimate exists for a cohort, BEFORE
        quoting any number for it. Call this first whenever the user asks about a
        specific subgroup.

        Returns identified=true with a verdict, or identified=false with a
        refusal explaining which condition failed. When it returns false there is
        no comparable untreated group in that cohort, so no method can recover the
        effect and any figure would be fabricated. Report the refusal and stop.

        Use for: questions scoped to a subgroup, and any challenge about whether a
        subgroup answer is trustworthy.
        Do NOT use for: projecting value (use run_scenario) or choosing a budget
        (use optimize_allocation).
      input_schema:
        type: "object"
        properties:
          cohort_json:
            type: "string"
            description: |
              JSON object mapping column names to a required value, or to
              {"min": x, "max": y} for a range. Pass an empty string for the whole
              population. Column names must exist on the DATA.UNIT table; if you
              pass an unknown column the tool returns the list of valid ones.
              Examples: {"INSURANCE_TYPE": "DUAL"} or
              {"COMORBIDITY_COUNT": {"min": 7}} or
              {"REGION": "WEST", "AGE": {"min": 65, "max": 80}}.
        required: ["cohort_json"]

  - tool_spec:
      type: "generic"
      name: "run_scenario"
      description: |
        Project the outcome of treating a given number of units, optionally within
        a cohort. Returns expected events avoided or gained, programme cost, gross
        and net value, ROI, and how many units have positive expected net value.

        Units are chosen best-first by estimated per-unit benefit, so this is the
        value of a WELL-TARGETED programme at that capacity, not of a random one.

        Refuses, returning refused=true, when the cohort lacks common support. It
        checks identification internally, so a refusal here is authoritative.

        Use for: "what if we treat N", "what if we expand to N", capacity changes,
        cohort-specific projections.
        Do NOT use for: choosing the best N (use optimize_allocation) or comparing
        targeting strategies (use compare_targeting_strategies).
      input_schema:
        type: "object"
        properties:
          capacity:
            type: "integer"
            description: "Number of units to treat. Must be positive."
          cohort_json:
            type: "string"
            description: |
              Same format as check_identification. Empty string means the whole
              population.
          respect_equity:
            type: "boolean"
            description: |
              When true, include the fairness gate status for the allocation policy
              the pipeline gated on. Set true for anything that informs a real
              policy decision.
        required: ["capacity", "cohort_json", "respect_equity"]

  - tool_spec:
      type: "generic"
      name: "optimize_allocation"
      description: |
        Find how many units are worth treating and what that costs, given an
        optional budget ceiling. Answers the question behind most budget requests:
        is the BUDGET the binding constraint, or the number of units that are
        actually worth treating?

        Returns the recommended number to treat, the spend, expected net value,
        which constraint binds, and either the value forgone to the budget or the
        budget that should be left unspent.

        Note the possible answer that no units are worth treating. That is a
        legitimate result meaning the intervention does not pay for itself at its
        current cost, and it should be reported plainly rather than worked around.

        Use for: "how many should we treat", "should we increase the budget",
        "what is the optimal spend", "is this programme worth running".
        Do NOT use for: a fixed capacity the user has already chosen (use
        run_scenario).
      input_schema:
        type: "object"
        properties:
          max_budget:
            type: "number"
            description: |
              Budget ceiling in currency units. Pass 0 or a very large number for
              the unconstrained optimum.
        required: ["max_budget"]

  - tool_spec:
      type: "generic"
      name: "compare_targeting_strategies"
      description: |
        Compare how well different ways of ranking units actually work, using Qini
        curves computed from OBSERVED outcomes rather than from ground truth. Also
        returns the fairness gate result.

        This is the tool for "is our current approach good enough". It shows
        whether ranking by predicted risk carries real signal, which is the
        assumption most existing targeting programmes are built on and which
        frequently does not hold: risk ranking can perform worse than random,
        because who is sickest is not the same question as who is most helped.

        Use for: "does our targeting work", "risk score versus causal model",
        "is the model better than what we do today", fairness questions.
        Do NOT use for: projecting value (use run_scenario).
      input_schema:
        type: "object"
        properties: {}

  - tool_spec:
      type: "generic"
      name: "explain_assumptions"
      description: |
        State what must be true for these estimates to be valid, and list every
        estimate produced with its confidence interval and identification status.

        Call this whenever a user challenges the numbers, asks how they were
        produced, or is about to make a funding decision. It also explains why the
        methods differ from each other, which pre-empts the natural but wrong
        conclusion that the spread means one of them is broken.

        Use for: "why should I believe this", "what are the assumptions", "how
        confident are you", "these numbers disagree".
      input_schema:
        type: "object"
        properties: {}

  - tool_spec:
      type: "generic"
      name: "refute_estimate"
      description: |
        Stress-test the estimate with refutation tests, and report whether it
        survived. Runs three attacks: replacing treatment with a permuted copy (a real
        effect must collapse to zero), adding an irrelevant covariate (a stable
        estimate barely moves), and re-estimating on random subsets.

        Report the asymmetry honestly: passing all three is WEAK evidence for the
        estimate, while failing any is STRONG evidence against it. Never describe a
        pass as proof or validation, and never imply the tests confirm the
        no-unmeasured-confounding assumption, which no test can check.

        Slow, roughly a minute. Use when the user challenges the result, asks how
        robust it is, or is about to commit budget to it.

        Use for: "how robust is this", "stress test it", "could this be spurious",
        "prove it is not a coincidence".
        Do NOT use for: listing the assumptions (use explain_assumptions) or for
        subgroup validity (use check_identification).
      input_schema:
        type: "object"
        properties:
          sample_size:
            type: "integer"
            description: |
              Units to test on. Use 15000 or more; below that the placebo test carries
              enough of its own noise to report a spurious failure.
          num_simulations:
            type: "integer"
            description: "Repetitions per test. Use 10 or more."
        required: ["sample_size", "num_simulations"]

tool_resources:
  check_identification:
    type: "procedure"
    identifier: "@DATABASE@.AGENT.CHECK_IDENTIFICATION"
    name: "CHECK_IDENTIFICATION(VARCHAR)"
    execution_environment:
      type: "warehouse"
      warehouse: "@WAREHOUSE@"
  run_scenario:
    type: "procedure"
    identifier: "@DATABASE@.AGENT.RUN_SCENARIO"
    name: "RUN_SCENARIO(NUMBER, VARCHAR, BOOLEAN)"
    execution_environment:
      type: "warehouse"
      warehouse: "@WAREHOUSE@"
  optimize_allocation:
    type: "procedure"
    identifier: "@DATABASE@.AGENT.OPTIMIZE_ALLOCATION"
    name: "OPTIMIZE_ALLOCATION(FLOAT)"
    execution_environment:
      type: "warehouse"
      warehouse: "@WAREHOUSE@"
  compare_targeting_strategies:
    type: "procedure"
    identifier: "@DATABASE@.AGENT.COMPARE_TARGETING_STRATEGIES"
    name: "COMPARE_TARGETING_STRATEGIES()"
    execution_environment:
      type: "warehouse"
      warehouse: "@WAREHOUSE@"
  explain_assumptions:
    type: "procedure"
    identifier: "@DATABASE@.AGENT.EXPLAIN_ASSUMPTIONS"
    name: "EXPLAIN_ASSUMPTIONS()"
    execution_environment:
      type: "warehouse"
      warehouse: "@WAREHOUSE@"
  refute_estimate:
    type: "procedure"
    identifier: "@DATABASE@.AGENT.REFUTE_ESTIMATE"
    name: "REFUTE_ESTIMATE(NUMBER, NUMBER)"
    execution_environment:
      type: "warehouse"
      warehouse: "@WAREHOUSE@"
$$;
```

### `agent/03_refute.sql`

Copy code

```
-- =====================================================================
-- Refutation tests, in an isolated dowhy environment.
--
-- Deployed separately from 01_tools.sql because dowhy CANNOT coexist with econml:
-- dowhy requires numpy>=2 and econml requires numpy<2, so putting both in one
-- PACKAGES list fails at CREATE time with a dependency resolution error.
-- sql/00_verify_packages.sql demonstrates that failure deliberately.
--
-- The two environments therefore communicate through tables, which is the same
-- pattern used everywhere else a boundary is crossed:
--
--   notebook 02 (econml)  ->  MODELS.CATE_SCORES, MODELS.DIAGNOSTICS
--   create_analysis_view  ->  MODELS.V_ANALYSIS_FRAME
--   this procedure (dowhy) -> MODELS.REFUTATION
--
-- WHAT REFUTATION IS AND IS NOT
--
-- These tests cannot prove an estimate correct. No test can, because the central
-- assumption -- that every common cause of treatment and outcome is measured -- is
-- not testable from the data. What they can do is try to break the estimate in ways
-- that a spurious result would not survive:
--
--   placebo treatment    replace treatment with a permuted copy. A real effect must
--                        collapse to zero. If it does not, the pipeline is finding
--                        structure that has nothing to do with the treatment.
--   random common cause  add an irrelevant covariate. A stable estimate should barely
--                        move.
--   data subset          re-estimate on random subsets. A fragile estimate wanders.
--
-- Passing all three is weak evidence FOR the estimate. Failing any is strong evidence
-- against it. That asymmetry is the honest way to read the output, and the procedure
-- says so in its own return value.
--
-- Owner's rights for the same reason as the tools in 01_tools.sql. Note that this
-- procedure also WRITES: it overwrites MODELS.REFUTATION, so any role with USAGE
-- on it can replace the persisted verdict (with a freshly computed one).
-- =====================================================================

USE DATABASE @DATABASE@;
USE SCHEMA AGENT;

CREATE OR REPLACE PROCEDURE AGENT.REFUTE_ESTIMATE(SAMPLE_SIZE INT, NUM_SIMULATIONS INT)
COPY GRANTS
RETURNS VARIANT
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
ARTIFACT_REPOSITORY = snowflake.snowpark.pypi_shared_repository
PACKAGES = ('snowflake-snowpark-python', 'dowhy==0.14')
HANDLER = 'run'
EXECUTE AS OWNER
AS
$$
import json
import logging

import numpy as np
import pandas as pd

logging.getLogger("dowhy").setLevel(logging.ERROR)
logging.getLogger("py.warnings").setLevel(logging.ERROR)

def _load_spec(session):
    """Learn the column names from the persisted spec, so this stays domain-blind."""
    rows = session.sql(
        "SELECT SPEC_JSON FROM @DATABASE@.MODELS.SPEC_SNAPSHOT "
        "ORDER BY SNAPSHOT_AT DESC LIMIT 1"
    ).collect()
    if not rows:
        return None
    return json.loads(rows[0]["SPEC_JSON"])

def run(session, sample_size, num_simulations):
    from dowhy import CausalModel

    sample_size = int(sample_size or 20000)
    num_simulations = int(num_simulations or 10)

    spec = _load_spec(session)
    if spec is None:
        return {
            "ok": False,
            "error": "MODELS.SPEC_SNAPSHOT is empty. Run causal_core.write_spec_snapshot() first.",
        }

    observed = [c.upper() for c in spec["covariates"]["observed"]]
    categorical = {c.upper() for c in spec["covariates"]["categorical"]}

    # Sampled deliberately. Refutation asks whether a conclusion is FRAGILE, and each
    # refuter re-estimates num_simulations times, so the full panel would cost far more
    # compute for no change in the verdict. Reported in the output so the reader can
    # judge rather than having to trust it.
    # ORDER BY HASH(id) rather than SAMPLE(): hashing the unit id gives a
    # deterministic pseudo-random subset, so re-running the procedure reproduces the
    # same verdict. A refutation result that changes between runs is not usable as
    # evidence for anything.
    #
    # Built from .collect() rather than .to_pandas(). The connector's to_pandas path
    # needs the pyarrow bridge, which is absent from this ARTIFACT_REPOSITORY
    # environment even though pandas itself arrives with dowhy. Adding pyarrow here
    # would mean another pin to keep compatible with numpy>=2 for no benefit, and
    # collect() has no such dependency.
    rows = session.sql(
        f"SELECT * FROM @DATABASE@.MODELS.V_ANALYSIS_FRAME "
        f"ORDER BY HASH(UNIT_ID) LIMIT {sample_size}"
    ).collect()
    if not rows:
        return {"ok": False, "error": "MODELS.V_ANALYSIS_FRAME is empty"}
    frame = pd.DataFrame([r.as_dict() for r in rows])

    present = [c for c in observed if c in frame.columns]
    missing = [c for c in observed if c not in frame.columns]

    # One-hot encode here rather than relying on dowhy to infer types, so the
    # covariate set is explicit and reproducible.
    to_encode = [c for c in present if c in categorical]
    design = pd.get_dummies(frame[present], columns=to_encode, drop_first=True)
    design.columns = [
        str(c).replace(" ", "_").replace("-", "_").replace(".", "_") for c in design.columns
    ]
    common_causes = list(design.columns)

    data = design.astype(float).copy()
    data["TREAT"] = frame["TREAT"].astype(int).to_numpy()
    data["Y"] = frame["Y"].astype(float).to_numpy()
    data = data.dropna()

    if data["TREAT"].nunique() < 2 or len(data) < 500:
        return {
            "ok": False,
            "error": (
                f"insufficient usable rows for refutation: {len(data)} rows, "
                f"{int(data['TREAT'].nunique())} treatment level(s)"
            ),
        }

    model = CausalModel(
        data=data, treatment="TREAT", outcome="Y", common_causes=common_causes
    )

    # Reuse ONE estimand object across estimate_effect and every refute_estimate call.
    # estimate_effect() sets identifier_method on it; handing refute_estimate a freshly
    # identified estimand raises AttributeError on NoneType. Verified the hard way in
    # sql/00_verify_packages.sql.
    estimand = model.identify_effect(proceed_when_unidentifiable=True)
    estimate = model.estimate_effect(
        estimand, method_name="backdoor.linear_regression", target_units="ate"
    )
    base = float(estimate.value)

    results = []

    def record(name, description, value, expectation, verdict_fn, error=None):
        if error is not None:
            results.append(
                {
                    "test": name,
                    "status": "error",
                    "description": description,
                    "detail": str(error)[:300],
                }
            )
            return
        shift = float(value) - base
        relative = abs(shift) / abs(base) if base else float("inf")
        passed, note = verdict_fn(float(value), shift, relative)
        results.append(
            {
                "test": name,
                "status": "pass" if passed else "FAIL",
                "description": description,
                "expectation": expectation,
                "new_estimate": round(float(value), 6),
                "shift_from_base": round(shift, 6),
                "relative_shift": round(relative, 4),
                "note": note,
            }
        )

    # --- placebo treatment: the strongest of the three ---------------------
    try:
        placebo = model.refute_estimate(
            estimand, estimate, method_name="placebo_treatment_refuter",
            placebo_type="permute", num_simulations=num_simulations,
        )
        record(
            "placebo_treatment",
            "Treatment replaced by a permuted copy, so it can carry no real effect.",
            placebo.new_effect,
            "should collapse to approximately zero",
            # 30%, not a tighter bound, because the placebo estimate carries its own
            # sampling noise: it is an average over num_simulations permutations, each
            # with roughly the same standard error as the real estimate. At small
            # samples that noise alone can exceed a 20% bound and produce a spurious
            # FAIL. Use sample_size >= 15,000 and num_simulations >= 10 for a verdict
            # worth quoting; a genuinely non-collapsing placebo sits near 100%, so the
            # looser bound costs no real detection power.
            lambda v, shift, rel: (
                abs(v) < 0.30 * abs(base),
                (
                    f"placebo effect {v:+.5f} is {abs(v) / abs(base):.1%} of the real "
                    f"estimate {base:+.5f}"
                    if base
                    else f"placebo effect {v:+.5f}"
                ),
            ),
        )
    except Exception as exc:  # noqa: BLE001
        record("placebo_treatment", "Treatment replaced by a permuted copy.", None, None, None, exc)

    # --- random common cause ----------------------------------------------
    try:
        rcc = model.refute_estimate(
            estimand, estimate, method_name="random_common_cause",
            num_simulations=max(3, num_simulations // 2),
        )
        record(
            "random_common_cause",
            "An irrelevant random covariate added to the adjustment set.",
            rcc.new_effect,
            "should barely move the estimate",
            lambda v, shift, rel: (
                rel < 0.10,
                f"estimate moved {rel:.2%} when noise was added to the adjustment set",
            ),
        )
    except Exception as exc:  # noqa: BLE001
        record("random_common_cause", "An irrelevant random covariate added.", None, None, None, exc)

    # --- data subset -------------------------------------------------------
    try:
        subset = model.refute_estimate(
            estimand, estimate, method_name="data_subset_refuter",
            subset_fraction=0.8, num_simulations=max(3, num_simulations // 2),
        )
        record(
            "data_subset",
            "Re-estimated on random 80% subsets of the data.",
            subset.new_effect,
            "should be stable across subsets",
            lambda v, shift, rel: (
                rel < 0.15,
                f"estimate moved {rel:.2%} across random subsets",
            ),
        )
    except Exception as exc:  # noqa: BLE001
        record("data_subset", "Re-estimated on random 80% subsets.", None, None, None, exc)

    passed = [r for r in results if r["status"] == "pass"]
    failed = [r for r in results if r["status"] == "FAIL"]
    errored = [r for r in results if r["status"] == "error"]

    # Persist so the console and the agent read one shared verdict. Written via
    # create_dataframe rather than write_pandas for the same pyarrow reason as above.
    columns = [
        "TEST_NAME", "STATUS", "BASE_ESTIMATE", "NEW_ESTIMATE", "SHIFT_FROM_BASE",
        "RELATIVE_SHIFT", "DESCRIPTION", "NOTE", "SAMPLE_SIZE", "NUM_SIMULATIONS",
    ]
    payload = [
        [
            r["test"],
            r["status"],
            float(round(base, 6)),
            None if r.get("new_estimate") is None else float(r["new_estimate"]),
            None if r.get("shift_from_base") is None else float(r["shift_from_base"]),
            None if r.get("relative_shift") is None else float(r["relative_shift"]),
            r["description"],
            (r.get("note") or r.get("detail") or "")[:1000],
            int(len(data)),
            int(num_simulations),
        ]
        for r in results
    ]
    session.create_dataframe(payload, schema=columns).write.mode("overwrite").save_as_table(
        "@DATABASE@.MODELS.REFUTATION"
    )

    verdict = (
        "Refutation tests did not overturn the estimate. Read that as weak support, "
        "not proof: these tests can only detect certain kinds of spurious result, and "
        "none of them can test the assumption that matters most, which is that every "
        "common cause of treatment and outcome was measured."
        if not failed and not errored
        else (
            f"{len(failed)} of {len(results)} refutation tests FAILED. Treat the "
            "estimate as unreliable until the cause is understood. A failing placebo "
            "test in particular means the pipeline is detecting something other than "
            "the treatment."
            if failed
            else f"{len(errored)} test(s) could not be run; the remainder passed."
        )
    )

    # Report the primary estimate alongside, so the difference between the two is
    # visible rather than left for the reader to trip over. Linear adjustment is
    # typically MORE attenuated than the cross-fitted doubly-robust estimate, because
    # it cannot represent the nonlinearity the forest-based nuisance models capture.
    primary = None
    try:
        rows = session.sql(
            "SELECT ESTIMATE FROM @DATABASE@.MODELS.DIAGNOSTICS "
            "WHERE LOWER(METHOD) LIKE '%robust%' LIMIT 1"
        ).collect()
        if rows and rows[0]["ESTIMATE"] is not None:
            primary = float(rows[0]["ESTIMATE"])
    except Exception:  # noqa: BLE001
        primary = None

    return {
        "ok": True,
        "base_estimate": round(base, 6),
        "estimator": "backdoor.linear_regression (dowhy)",
        "primary_estimate_from_diagnostics": (
            None if primary is None else round(primary, 6)
        ),
        "estimator_comparison": (
            None
            if primary is None
            else (
                f"This refutation ran against a linear adjustment giving {base:+.5f}, "
                f"while the primary doubly-robust estimate is {primary:+.5f}. Linear "
                "adjustment is usually the more attenuated of the two. What is being "
                "tested here is whether the IDENTIFICATION STRATEGY survives attack, "
                "not which estimator is closer to the truth."
            )
        ),
        "sample_size": len(data),
        "num_simulations": num_simulations,
        "covariates_used": len(common_causes),
        "covariates_missing_from_view": missing,
        "tests_passed": len(passed),
        "tests_failed": len(failed),
        "tests_errored": len(errored),
        "results": results,
        "verdict": verdict,
        "how_to_read": (
            "Passing all three tests is weak evidence FOR the estimate. Failing any is "
            "strong evidence against it. The asymmetry is real and should not be "
            "smoothed over: refutation can find a broken result but cannot certify a "
            "sound one."
        ),
        "note_on_estimator": (
            "dowhy fits a linear-regression adjustment here, so this base estimate will "
            "not match the doubly-robust figure in MODELS.DIAGNOSTICS exactly. The "
            "purpose is to test whether the identification strategy survives being "
            "attacked, not to reproduce the primary estimate."
        ),
    }
$$;
```

## `app/`

### `app/causal_console.py`

Copy code

```
"""Causal decision console.

Runs as a Streamlit app inside Snowflake. One file, no use-case-specific code: every
label, cost, and protected attribute comes from MODELS.SPEC_SNAPSHOT, so the same
app serves any use case built on this framework.

THE ARCHITECTURAL POINT WORTH NOTICING

This app does not compute anything. It calls five of the six stored procedures in
the AGENT schema that the Cortex Agent calls, and reads the same MODELS tables the
notebooks wrote. That is deliberate and it is the whole reason the design holds
together: a figure shown here, a figure quoted in chat, and a figure printed in a
notebook are the same figure, because there is exactly one implementation of each.
The moment a console recomputes "net value" its own way, you have two definitions of
net value and no way to know which one a screenshot came from.

THE REFUSAL IS ENFORCED IN THE UI, NOT CAPTIONED

When the selected cohort cannot support an estimate, this app does not show the
numbers with a warning next to them. It withholds them. A warning beside a number is
read as a formality; an absent number is read as an answer. That behaviour is the
point of the whole pipeline, so it gets to shape the layout.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

def _connect():
    """Return a session that has a current database, in either environment.

    Every query below uses schema-qualified but database-UNQUALIFIED names
    (MODELS.CATE_SCORES, DATA.UNIT, AGENT.RUN_SCENARIO, INFORMATION_SCHEMA.COLUMNS),
    which is what lets one app file serve every use case.

    In Streamlit in Snowflake that resolves for free: the session inherits the
    database of the STREAMLIT object, which deploy_app.py creates inside the use
    case's own database. Running locally there is no such context, and the first
    query fails with "This session does not have a current database" before any UI
    is built. So set it explicitly, from CAUSAL_DATABASE if given, otherwise from the
    spec on disk.
    """
    try:
        from snowflake.snowpark.context import get_active_session

        return get_active_session(), True
    except Exception:
        from snowflake.snowpark import Session

        # Same precedence as causal_core.session: env vars, otherwise the default
        # connection in connections.toml. Never a hard-coded name.
        connection = os.environ.get("SNOWFLAKE_CONNECTION_NAME") or os.environ.get(
            "SNOWFLAKE_DEFAULT_CONNECTION_NAME"
        )
        builder = Session.builder
        if connection:
            builder = builder.config("connection_name", connection)
        session = builder.getOrCreate()

        database = os.environ.get("CAUSAL_DATABASE")
        if not database:
            sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "framework"))
            from causal_core import load_spec

            database = load_spec().database
        # Snowpark validates the name rather than splicing it into SQL text.
        session.use_database(database)
        return session, False

SESSION, IN_SNOWFLAKE = _connect()

if not SESSION.get_current_database():
    raise RuntimeError(
        "This session has no current database, so the console's unqualified table "
        "references cannot resolve. In Snowflake, create the STREAMLIT object inside "
        "the use case database (framework/deploy_app.py does this). Locally, set "
        "CAUSAL_DATABASE."
    )

st.set_page_config(page_title="Causal decision console", layout="wide")

# ---------------------------------------------------------------------------
# Spec and data loading
# ---------------------------------------------------------------------------

@st.cache_data(ttl=600, show_spinner=False)
def load_spec_row() -> dict:
    """Read the spec snapshot. Everything domain-specific in this app comes from here."""
    rows = SESSION.sql(
        "SELECT * FROM MODELS.SPEC_SNAPSHOT ORDER BY SNAPSHOT_AT DESC LIMIT 1"
    ).collect()
    if not rows:
        st.error(
            "MODELS.SPEC_SNAPSHOT is empty. Run causal_core.write_spec_snapshot() or "
            "framework/deploy_app.py before opening the console."
        )
        st.stop()
    return rows[0].as_dict()

@st.cache_data(ttl=600, show_spinner=False)
def sql_df(query: str) -> pd.DataFrame:
    return SESSION.sql(query).to_pandas()

@st.cache_data(ttl=600, show_spinner=False)
def unit_columns() -> pd.DataFrame:
    return SESSION.sql(
        """
        SELECT COLUMN_NAME, DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'DATA' AND TABLE_NAME = 'UNIT'
        ORDER BY ORDINAL_POSITION
        """
    ).to_pandas()

# The procedures the console may call. The name is checked against this set and
# every argument is a bind parameter, so nothing a user picks in the sidebar (a
# category value such as O'Neil, for example) is ever spliced into SQL text.
PROCEDURES = {
    "CHECK_IDENTIFICATION",
    "RUN_SCENARIO",
    "OPTIMIZE_ALLOCATION",
    "COMPARE_TARGETING_STRATEGIES",
    "EXPLAIN_ASSUMPTIONS",
}

def call_proc_raw(name: str, *args):
    """Call an AGENT procedure with bound arguments and return its raw result."""
    if name not in PROCEDURES:
        raise ValueError(f"unknown procedure {name!r}")
    placeholders = ", ".join("?" for _ in args)
    return SESSION.sql(
        f"CALL AGENT.{name}({placeholders})", params=list(args)
    ).collect()[0][0]

def call_proc(name: str, *args) -> dict:
    """Call an AGENT procedure and parse its VARIANT result.

    Not cached: these are the live decision surface, and a stale scenario is worse
    than a slow one.
    """
    raw = call_proc_raw(name, *args)
    if raw is None:
        return {}
    return json.loads(raw) if isinstance(raw, str) else raw

SPEC = load_spec_row()
UNIT_PLURAL = SPEC["UNIT_LABEL_PLURAL"]
UNIT_SINGULAR = SPEC["UNIT_LABEL_SINGULAR"]
OUTCOME_LABEL = SPEC["OUTCOME_LABEL"]
DIRECTION = SPEC["OUTCOME_DIRECTION"]
COST = float(SPEC["COST_PER_UNIT"])
PROTECTED = [a for a in (SPEC["PROTECTED_ATTRIBUTES"] or "").split(",") if a]
MAX_RATIO = float(SPEC["MAX_DISPARITY_RATIO"])

def money(value) -> str:
    if value is None:
        return "n/a"
    return f"${float(value):,.0f}"

# ---------------------------------------------------------------------------
# Sidebar: cohort and capacity
# ---------------------------------------------------------------------------

st.sidebar.title(SPEC["LABEL"])
st.sidebar.caption(
    f"{UNIT_PLURAL} · {SPEC['TREATMENT_LABEL']} at {money(COST)} each · "
    f"outcome: {OUTCOME_LABEL} ({DIRECTION})"
)

st.sidebar.subheader("Cohort")
st.sidebar.caption(
    "Narrow the population to ask a subgroup question. Some subgroups cannot be "
    "answered at all, which the console will tell you rather than guess."
)

def quote_ident(name: str) -> str:
    """Double-quote an identifier taken from INFORMATION_SCHEMA."""
    return '"' + name.replace('"', '""') + '"'

cols = unit_columns()
filterable = [
    c for c in cols.COLUMN_NAME.tolist() if c.upper() != SPEC["UNIT_ID_COLUMN"].upper()
]
chosen_cols = st.sidebar.multiselect(
    "Filter on",
    filterable,
    max_selections=3,
    help="Leave empty for the whole population.",
)

cohort: dict = {}
for column in chosen_cols:
    dtype = cols.loc[cols.COLUMN_NAME == column, "DATA_TYPE"].iloc[0]
    numeric = dtype.upper() in {"NUMBER", "FLOAT", "DECIMAL", "INTEGER", "DOUBLE"}
    # column comes from the INFORMATION_SCHEMA list above, never from free text.
    distinct = sql_df(
        f"SELECT DISTINCT {quote_ident(column)} AS V FROM DATA.UNIT ORDER BY V"
    )["V"].tolist()

    if not numeric or len(distinct) <= 12:
        picked = st.sidebar.selectbox(
            f"{column} =", ["(any)"] + distinct, key=f"eq_{column}"
        )
        if picked != "(any)":
            cohort[column] = picked
    else:
        lo, hi = float(min(distinct)), float(max(distinct))
        floor = st.sidebar.slider(f"{column} at least", lo, hi, lo, key=f"min_{column}")
        if floor > lo:
            cohort[column] = {"min": floor}

cohort_json = json.dumps(cohort) if cohort else ""

st.sidebar.subheader("Capacity")
capacity = st.sidebar.number_input(
    f"{UNIT_PLURAL} to treat", min_value=1, max_value=200_000, value=8000, step=500
)
budget = st.sidebar.number_input(
    "Budget ceiling",
    min_value=0,
    max_value=500_000_000,
    value=int(capacity * COST),
    step=100_000,
    help="Used by the allocation optimiser to decide whether budget or value binds.",
)

# ---------------------------------------------------------------------------
# The identification gate, evaluated once and applied everywhere
# ---------------------------------------------------------------------------

ident = call_proc("CHECK_IDENTIFICATION", cohort_json)
ANSWERABLE = bool(ident.get("identified")) and ident.get("ok", True)

st.title("Causal decision console")

if ident.get("error"):
    st.error(ident["error"])
    st.stop()

if not ANSWERABLE:
    st.error("This cohort cannot be answered. No estimate is available.")
    st.markdown(f"**Cohort:** {ident.get('cohort', 'n/a')}")
    st.markdown(ident.get("refusal", ""))
    left, mid, right = st.columns(3)
    left.metric(f"{UNIT_PLURAL} in cohort", f"{ident.get('n', 0):,}")
    mid.metric("treated", f"{ident.get('n_treated', 0):,}")
    right.metric(
        "treated with no comparable counterpart",
        f"{float(ident.get('share_treated_without_counterpart') or 0):.1%}",
    )
    st.info(
        "The **scenario** is withheld for this cohort on purpose: showing numbers "
        "next to a refusal invites reading them anyway. The other tabs still apply, "
        "because they describe the population and the method rather than this cohort. "
        "Widen the cohort in the sidebar to get a scenario."
    )
else:
    st.success(
        f"Cohort is answerable: {ident.get('cohort')}: {ident.get('n', 0):,} "
        f"{UNIT_PLURAL}, {ident.get('n_treated', 0):,} treated."
    )

tab_decide, tab_believe, tab_target, tab_equity, tab_receipt = st.tabs(
    ["Decide", "Why believe it", "Targeting", "Equity", "Receipt"]
)

# ---------------------------------------------------------------------------
# Decide
# ---------------------------------------------------------------------------

with tab_decide:
    # Gate THIS tab only. The remaining tabs describe the population and the method
    # rather than the selected cohort, so they stay available. A blanket st.stop()
    # here would halt the whole script and leave them blank, which reads as breakage
    # rather than as a refusal.
    scenario: dict = {}
    optimum: dict = {}
    if ANSWERABLE:
        scenario = call_proc("RUN_SCENARIO", int(capacity), cohort_json, True)
        optimum = call_proc("OPTIMIZE_ALLOCATION", float(budget))

    if not ANSWERABLE or scenario.get("refused"):
        st.error(
            "No scenario is shown for this cohort, because no defensible estimate "
            "exists for it.",
            icon="\U0001f6ab",
        )
        st.markdown(scenario.get("refusal") or ident.get("refusal", ""))
        st.caption(
            "The other tabs remain available. They describe the population and the "
            "method rather than this cohort, so the refusal does not affect them."
        )
    else:
        st.subheader("If you treat the top-ranked units at this capacity")
        a, b, c, d = st.columns(4)
        a.metric(f"{UNIT_PLURAL} treated", f"{scenario.get('units_treated', 0):,}")
        b.metric("programme cost", money(scenario.get("program_cost")))
        c.metric("expected net value", money(scenario.get("expected_net_value")))
        roi = scenario.get("roi")
        d.metric("ROI", "n/a" if roi is None else f"{roi:.2f}x")

        st.caption(scenario.get("basis", ""))
        if scenario.get("note"):
            st.warning(scenario["note"])

        st.divider()
        st.subheader("How many are actually worth treating?")
        st.markdown(
            "The answer is rarely *spend the whole budget*. Marginal value falls as "
            "you move down the ranking, and the optimum is where it crosses zero."
        )
        e, f, g = st.columns(3)
        e.metric(
            "worth treating",
            f"{optimum.get('units_with_positive_expected_value', 0):,}",
        )
        f.metric(
            "recommended to treat",
            f"{optimum.get('recommended_units_to_treat', 0):,}",
        )
        g.metric("binding constraint", str(optimum.get("binding_constraint", "n/a")))
        st.info(optimum.get("interpretation", ""), icon="\U0001f4a1")

        # The shape that makes "do not spend it all" obvious at a glance.
        marginal = sql_df(
            """
            -- Cumulative net value walking down the ranking, sampled every 250 units
            -- so the chart stays small. A window function cannot be nested inside
            -- another window function's PARTITION BY, hence the CTE.
            WITH ranked AS (
                SELECT ROW_NUMBER() OVER (ORDER BY NET_VALUE_PER_UNIT DESC) AS RN,
                       SUM(NET_VALUE_PER_UNIT) OVER (
                           ORDER BY NET_VALUE_PER_UNIT DESC
                           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                       ) AS CUM
                FROM MODELS.CATE_SCORES
            )
            SELECT RN AS UNITS_TREATED, CUM AS CUMULATIVE_NET_VALUE
            FROM ranked
            WHERE RN % 250 = 0 OR RN = 1
            ORDER BY RN
            """
        )
        if not marginal.empty:
            peak = marginal.loc[marginal.CUMULATIVE_NET_VALUE.idxmax()]
            line = (
                alt.Chart(marginal)
                .mark_line()
                .encode(
                    x=alt.X(
                        "UNITS_TREATED:Q",
                        title=f"{UNIT_PLURAL} treated, best first",
                    ),
                    y=alt.Y(
                        "CUMULATIVE_NET_VALUE:Q",
                        title="cumulative expected net value",
                    ),
                )
            )
            at_peak = (
                alt.Chart(pd.DataFrame({"x": [peak.UNITS_TREATED]}))
                .mark_rule(strokeDash=[6, 4])
                .encode(x="x:Q")
            )
            zero = (
                alt.Chart(pd.DataFrame({"y": [0]}))
                .mark_rule(color="grey")
                .encode(y="y:Q")
            )
            st.altair_chart(line + at_peak + zero, use_container_width=True)
            st.caption(
                f"Dashed line marks the peak, at about "
                f"{int(peak.UNITS_TREATED):,} {UNIT_PLURAL}. Treating past it "
                "destroys value: those units cost more than they return."
            )

# ---------------------------------------------------------------------------
# Why believe it
# ---------------------------------------------------------------------------

with tab_believe:
    st.subheader("The same question, answered several ways")
    st.markdown(
        "These methods do not disagree because one is broken. They target different "
        "quantities under different assumptions. **The raw difference is not an effect "
        "estimate at all**; it is the selection pattern plus the effect, and it is "
        "shown only to make the naive answer visible."
    )

    diag = sql_df(
        """
        SELECT METHOD, ESTIMATE, CI_LOW, CI_HIGH, IDENTIFIED, VERDICT, N, N_TREATED
        FROM MODELS.DIAGNOSTICS ORDER BY ESTIMATE
        """
    )
    if not diag.empty:
        base = alt.Chart(diag).encode(
            y=alt.Y("METHOD:N", sort=None, title=None),
            color=alt.condition(
                alt.datum.ESTIMATE > 0
                if DIRECTION == "minimize"
                else alt.datum.ESTIMATE < 0,
                alt.value("#d62728"),  # the sign that would mean "intervention hurts"
                alt.value("#1f77b4"),
            ),
        )
        st.altair_chart(
            base.mark_rule(size=3).encode(x="CI_LOW:Q", x2="CI_HIGH:Q")
            + base.mark_point(size=110, filled=True).encode(
                x=alt.X("ESTIMATE:Q", title=f"estimated effect on {OUTCOME_LABEL}")
            )
            + alt.Chart(pd.DataFrame({"x": [0]}))
            .mark_rule(color="grey")
            .encode(x="x:Q"),
            use_container_width=True,
        )
        st.caption(
            "Red marks an estimate whose sign implies the intervention is harmful. "
            f"For a {DIRECTION} outcome, only the naive comparison should land there."
        )
        st.dataframe(diag, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("Do comparable untreated units exist?")
    st.markdown(
        "Every adjustment method depends on finding untreated units that look like "
        "treated ones. Where the two distributions do not overlap, there is nothing "
        "to compare against and no method can fix it."
    )
    overlap = sql_df(
        """
        SELECT ROUND(PROPENSITY, 2) AS PROPENSITY,
               IFF(TREATED = 1, 'treated', 'untreated') AS ARM,
               COUNT(*) AS N
        FROM MODELS.CATE_SCORES GROUP BY 1, 2 ORDER BY 1
        """
    )
    if not overlap.empty:
        st.altair_chart(
            alt.Chart(overlap)
            .mark_area(opacity=0.55, interpolate="step")
            .encode(
                x=alt.X("PROPENSITY:Q", title="estimated probability of treatment"),
                y=alt.Y("N:Q", stack=None, title=f"{UNIT_PLURAL}"),
                color=alt.Color("ARM:N", title=None),
            ),
            use_container_width=True,
        )
        st.caption(
            "Where the treated area extends beyond the untreated one, those units have "
            "no counterpart. That region is what CHECK_IDENTIFICATION refuses on."
        )

    st.divider()
    st.subheader("What the pipeline asserts about itself")
    checks = sql_df(
        "SELECT CHECK_NAME, PASSED, DETAIL FROM MODELS.CALIBRATION_CHECKS ORDER BY 1"
    )
    if not checks.empty:
        passed = int(checks.PASSED.sum())
        st.metric("calibration checks passing", f"{passed} of {len(checks)}")
        st.dataframe(checks, use_container_width=True, hide_index=True)
    st.warning(
        "Read these honestly: they verify properties of the **synthetic data**, not the "
        "correctness of the estimators. They confirm the test fixture still poses the "
        "problem it was built to pose. Estimator correctness is covered separately, "
        "by the tests in tests/."
    )

    st.divider()
    st.subheader("Did the estimate survive being attacked?")
    st.markdown(
        "Refutation tests try to break the result in ways a spurious finding would not "
        "survive. **Passing them is weak evidence for the estimate; failing any is "
        "strong evidence against it.** That asymmetry is real: refutation can find a "
        "broken result but cannot certify a sound one."
    )
    refutation = sql_df(
        """
        SELECT TEST_NAME, STATUS, BASE_ESTIMATE, NEW_ESTIMATE, RELATIVE_SHIFT, NOTE
        FROM MODELS.REFUTATION ORDER BY TEST_NAME
        """
    )
    if refutation.empty:
        st.info(
            "No refutation results yet. These run in a separate environment, because "
            "dowhy needs numpy>=2 while econml needs numpy<2. Run "
            "`causal_core.refute.refute(session, spec)`."
        )
    else:
        failed = int((refutation.STATUS != "pass").sum())
        if failed:
            st.error(f"{failed} of {len(refutation)} refutation tests FAILED.")
        else:
            st.success(
                f"All {len(refutation)} refutation tests passed; the estimate was not "
                "overturned. Weak support, not proof."
            )
        st.dataframe(refutation, use_container_width=True, hide_index=True)

    with st.expander("Full assumption statement (from the agent's own tool)"):
        st.code(call_proc_raw("EXPLAIN_ASSUMPTIONS"), language=None)

# ---------------------------------------------------------------------------
# Targeting
# ---------------------------------------------------------------------------

with tab_target:
    st.subheader("Does the ranking carry signal?")
    st.markdown(
        "Qini curves computed from **observed outcomes**, not from ground truth. This "
        "is the one evaluation here that would work on real data, which makes it the "
        "one you would actually run in production."
    )

    comparison = call_proc("COMPARE_TARGETING_STRATEGIES")
    rankings = comparison.get("rankings_evaluated", [])
    if rankings:
        cols_ = st.columns(len(rankings))
        for col, r in zip(cols_, rankings):
            col.metric(
                r["model"],
                f"{r['auuc']:+.3f}",
                r["verdict"],
                delta_color="normal" if r["auuc"] > 0 else "inverse",
            )

    qini = sql_df(
        """
        SELECT MODEL, SHARE_TARGETED, QINI, QINI_RANDOM
        FROM MODELS.QINI_CURVE ORDER BY MODEL, SHARE_TARGETED
        """
    )
    if not qini.empty:
        curves = (
            alt.Chart(qini)
            .mark_line(size=2)
            .encode(
                x=alt.X(
                    "SHARE_TARGETED:Q",
                    axis=alt.Axis(format="%"),
                    title="share of population targeted",
                ),
                y=alt.Y("QINI:Q", title=f"cumulative incremental {OUTCOME_LABEL}"),
                color=alt.Color("MODEL:N", title="ranking"),
            )
        )
        random_line = (
            alt.Chart(qini[qini.MODEL == qini.MODEL.iloc[0]])
            .mark_line(strokeDash=[6, 4], color="grey")
            .encode(x="SHARE_TARGETED:Q", y="QINI_RANDOM:Q")
        )
        st.altair_chart(curves + random_line, use_container_width=True)
        st.caption(
            "The dashed line is what a ranking with no signal traces. A curve BELOW it "
            "is worse than random, a real and common outcome for risk-score ranking, "
            "because who is worst off is a different question from who is most helped."
        )
    st.info(comparison.get("how_to_read", ""))

# ---------------------------------------------------------------------------
# Equity
# ---------------------------------------------------------------------------

with tab_equity:
    st.subheader("The fairness gate")
    st.markdown(
        "Impactability correlates with being reachable, and reachability correlates "
        "with advantage. A model optimised for measured impact will concentrate help "
        "on whoever was already easiest to help, and nothing in the accuracy metrics "
        "shows it. This is the failure mode documented in Obermeyer et al., "
        "*Science* 2019."
    )

    equity = sql_df(
        """
        SELECT POLICY, ATTRIBUTE, GROUP_VALUE, POPULATION, SELECTED, SELECTION_RATE,
               REPRESENTATION_INDEX, OBSERVED_RATIO, THRESHOLD, PASSED
        FROM MODELS.EQUITY_REPORT ORDER BY ATTRIBUTE, GROUP_VALUE
        """
    )
    if equity.empty:
        st.info("No equity report yet. Run notebook 03.")
    else:
        summary = (
            equity.groupby("ATTRIBUTE")
            .agg(
                ratio=("OBSERVED_RATIO", "max"),
                threshold=("THRESHOLD", "max"),
                passed=("PASSED", "min"),
            )
            .reset_index()
        )
        cols_ = st.columns(len(summary))
        for col, row in zip(cols_, summary.itertuples()):
            col.metric(
                row.ATTRIBUTE,
                f"{row.ratio:.2f}x",
                f"threshold {row.threshold:.2f}x: {'PASS' if row.passed else 'FAIL'}",
                delta_color="normal" if row.passed else "inverse",
            )

        attribute = st.selectbox("Break down by", sorted(equity.ATTRIBUTE.unique()))
        subset = equity[equity.ATTRIBUTE == attribute]
        st.altair_chart(
            alt.Chart(subset)
            .mark_bar()
            .encode(
                x=alt.X("GROUP_VALUE:N", title=attribute, sort=None),
                y=alt.Y(
                    "SELECTION_RATE:Q",
                    axis=alt.Axis(format="%"),
                    title="share selected for treatment",
                ),
                color=alt.condition(
                    alt.datum.REPRESENTATION_INDEX < 1,
                    alt.value("#d62728"),
                    alt.value("#1f77b4"),
                ),
            ),
            use_container_width=True,
        )
        st.caption(
            "Red bars are groups under-represented among those selected, relative to "
            "their share of the population."
        )
        st.dataframe(subset, use_container_width=True, hide_index=True)
        st.markdown(
            f"The gated policy constrains the **intersection** of "
            f"{', '.join(PROTECTED)} so every marginal disparity ratio stays under "
            f"{MAX_RATIO:.2f}x. Notebook 03 prices what that constraint costs rather "
            "than presenting fairness as free."
        )

# ---------------------------------------------------------------------------
# Receipt
# ---------------------------------------------------------------------------

with tab_receipt:
    st.subheader("What produced these numbers")
    st.markdown(
        "Everything on the other tabs comes from tables written by the notebooks, read "
        "through the same procedures the Cortex Agent uses. Nothing is recomputed here, "
        "so a screenshot from this console and an answer from the agent cannot disagree."
    )

    meta = {k: v for k, v in SPEC.items() if k != "SPEC_JSON"}
    st.dataframe(
        pd.DataFrame({"field": list(meta), "value": [str(v) for v in meta.values()]}),
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Table freshness")
    freshness = sql_df(
        """
        SELECT TABLE_NAME, ROW_COUNT, LAST_ALTERED
        FROM INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'MODELS' ORDER BY LAST_ALTERED DESC
        """
    )
    st.dataframe(freshness, use_container_width=True, hide_index=True)

    st.subheader("What would survive on real data")
    st.markdown(
        """
| Capability | Needs planted truth? |
|---|---|
| Propensity, overlap, identification gate | No |
| Doubly-robust ATE and its confidence interval | No |
| Difference-in-differences and the pre-trend test | No |
| Per-unit effects and the resulting ranking | No |
| **Qini curves and AUUC** | **No**, computed from observed outcomes |
| Allocation, capacity constraints, equity gate | No |
| Projected value of a policy | No, uses estimated effects |
| *Realised* value of a policy | Yes |
| Estimator error, bias, CI coverage | Yes |

The synthetic data is a **test fixture**, not evidence. Its magnitudes are
consequences of constants chosen in the generator and should not be quoted as
findings. What it establishes is that this pipeline recovers a known answer and
refuses when it cannot.
"""
    )

    with st.expander("Full spec JSON"):
        st.json(json.loads(SPEC["SPEC_JSON"]))
```

### `app/environment.yml`

Copy code

```
# Packages for Streamlit in Snowflake.
#
# Anaconda channel only. The console deliberately needs nothing beyond what SiS
# already ships: it computes nothing, so it needs no estimator libraries. econml
# never appears here, which is what keeps the app immune to the numpy conflict that
# forces dowhy into a separate stored procedure.
name: sf_env
channels:
  - snowflake
dependencies:
  - streamlit
  - pandas
  - altair
```

## `framework/`

### `framework/causal_core/__init__.py`

Copy code

```
"""Causal decision framework: domain-blind causal inference on Snowflake.

Nothing in this package contains a domain-specific column name, label, or
dollar figure. Domain knowledge arrives through a use case spec.

Typical notebook opening:

    from causal_core import load_spec, get_session, load_analysis_frame

    spec = load_spec()                      # reads config.yaml active_usecase
    session = get_session(spec)
    frame = load_analysis_frame(session, spec)
"""

from .allocate import (
    allocate_by_group,
    allocate_positive_value,
    allocate_top_n,
    auuc,
    benefit_scores,
    compare_policies,
    net_value_per_unit,
    policy_economics,
    qini_curve,
    write_allocation,
    write_qini,
)
from .data import (
    create_analysis_view,
    COL_OUTCOME,
    COL_PRE_OUTCOME,
    COL_TREATMENT,
    COL_UNIT_ID,
    DataError,
    analysis_frame_sql,
    design_matrix,
    feature_columns,
    load_analysis_frame,
    load_capacity,
    load_did_frame,
    load_event_study,
    load_panel,
    load_truth,
    validate_tables,
)
from .equity import (
    DisparityReport,
    EquityGateFailure,
    allocate_with_floor,
    min_achievable_disparity_ratio,
    check_equity,
    disparity_report,
    write_equity_report,
)
from .session import describe_session, get_session, resolve_connection_name
from .spec import (
    write_spec_snapshot,
    CANONICAL_TABLES,
    SCHEMAS,
    Outcome,
    SpecError,
    UseCaseSpec,
    available_usecases,
    load_config,
    load_copy,
    load_spec,
)

__all__ = [
    # spec
    "UseCaseSpec",
    "Outcome",
    "SpecError",
    "load_spec",
    "load_config",
    "load_copy",
    "available_usecases",
    "CANONICAL_TABLES",
    "SCHEMAS",
    # session
    "get_session",
    "describe_session",
    "resolve_connection_name",
    # data
    "validate_tables",
    "load_analysis_frame",
    "analysis_frame_sql",
    "load_panel",
    "load_did_frame",
    "load_event_study",
    "load_capacity",
    "load_truth",
    "feature_columns",
    "design_matrix",
    "write_spec_snapshot",
    "create_analysis_view",
    "refute",
    "refutation_table",
    "RefutationUnavailable",
    "DataError",
    # allocation
    "benefit_scores",
    "net_value_per_unit",
    "allocate_top_n",
    "allocate_by_group",
    "allocate_positive_value",
    "policy_economics",
    "compare_policies",
    "qini_curve",
    "auuc",
    "write_allocation",
    "write_qini",
    # equity
    "check_equity",
    "disparity_report",
    "allocate_with_floor",
    "min_achievable_disparity_ratio",
    "write_equity_report",
    "DisparityReport",
    "EquityGateFailure",
    "COL_UNIT_ID",
    "COL_TREATMENT",
    "COL_OUTCOME",
    "COL_PRE_OUTCOME",
]
```

### `framework/causal_core/allocate.py`

Copy code

```
"""Turn a ranking into a decision, and price it.

A ranked list is not a decision. The decision is which units to treat given a
fixed budget, and whether doing so is worth more than it costs. That is where an
uplift model either earns its keep or does not.

Three things live here:

**Allocation.** Selecting units under a capacity constraint, optionally per group,
optionally requiring positive net value per unit. Real-data usable: it consumes
estimated effects.

**Policy comparison.** Pricing a selection using an effect estimate. Pass the
estimated CATE to get what you would have projected; pass planted truth to get what
actually would have happened. The gap between those two is worth looking at.

**Qini curves.** The standard uplift evaluation, computed from *observed outcomes*
rather than from ground truth, so it works on real data. This is the honest way to
check whether a ranking has any signal when there is no answer key.

Nothing here knows what the outcome means. Direction and monetary value come from
the spec, so a use case that maximizes revenue and one that minimizes readmission
run through identical code.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from .data import COL_OUTCOME, COL_TREATMENT, COL_UNIT_ID
from .spec import Outcome, UseCaseSpec

# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

def benefit_scores(
    spec: UseCaseSpec,
    effect: pd.Series,
    outcome: Outcome | None = None,
) -> pd.Series:
    """Re-express per-unit effects so that larger is always better.

    This single call is what lets everything below ignore whether the outcome is
    being minimized or maximized.
    """
    outcome = outcome or spec.outcome
    return effect.apply(outcome.benefit).rename("benefit")

def net_value_per_unit(
    spec: UseCaseSpec,
    effect: pd.Series,
    outcome: Outcome | None = None,
) -> pd.Series:
    """Expected value of treating each unit, minus what treating it costs.

    Units with a negative value here are ones you would lose money on even if the
    effect estimate is exactly right, so treating them is not a close call.
    """
    outcome = outcome or spec.outcome
    gross = benefit_scores(spec, effect, outcome) * outcome.value_per_event
    return (gross - spec.treatment.cost_per_unit).rename("net_value")

# ---------------------------------------------------------------------------
# Allocation
# ---------------------------------------------------------------------------

def allocate_top_n(scores: pd.Series, capacity: int) -> pd.Series:
    """Take the highest-scoring units up to capacity."""
    selected = pd.Series(False, index=scores.index, name="selected")
    if capacity > 0:
        selected.loc[scores.nlargest(min(capacity, len(scores))).index] = True
    return selected

def allocate_by_group(
    frame: pd.DataFrame,
    spec: UseCaseSpec,
    scores: pd.Series,
    group_capacity: dict[str, int],
) -> pd.Series:
    """Take the highest-scoring units within each group, up to that group's slots.

    This is what a real constraint usually looks like: nurses are hired per region
    and offer budgets are set per market, so capacity does not pool globally. It
    matters, because a globally optimal list is frequently unimplementable.
    """
    group_col = _resolve(frame, spec.capacity.group_column)
    selected = pd.Series(False, index=frame.index, name="selected")

    for group, slots in group_capacity.items():
        rows = frame.index[frame[group_col] == group]
        if len(rows) == 0 or slots <= 0:
            continue
        take = scores.loc[rows].nlargest(min(int(slots), len(rows))).index
        selected.loc[take] = True
    return selected

def allocate_positive_value(
    spec: UseCaseSpec,
    effect: pd.Series,
    capacity: int | None = None,
    outcome: Outcome | None = None,
) -> pd.Series:
    """Treat only units expected to return more than they cost, up to capacity.

    Distinct from top-N in a way that matters: if fewer units clear the bar than
    there is capacity for, this leaves capacity unused rather than spending it on
    units it expects to lose money on. Spending the whole budget is not the goal.
    """
    value = net_value_per_unit(spec, effect, outcome)
    worth_it = value > 0
    if capacity is None:
        return worth_it.rename("selected")
    ranked = value.where(worth_it, other=-np.inf)
    return allocate_top_n(ranked, min(capacity, int(worth_it.sum())))

# ---------------------------------------------------------------------------
# Pricing a policy
# ---------------------------------------------------------------------------

def policy_economics(
    spec: UseCaseSpec,
    selected: pd.Series,
    effect: pd.Series,
    outcome: Outcome | None = None,
    label: str = "policy",
) -> dict[str, float | str]:
    """Price a selection using a given set of per-unit effects.

    ``effect`` decides what question is being answered. Estimated effects give the
    business case you would have written. Planted truth gives what would actually
    have happened. Reporting only the first is how overconfident programs get
    funded.
    """
    outcome = outcome or spec.outcome
    chosen = selected.astype(bool)
    n = int(chosen.sum())

    if n == 0:
        return {
            "policy": label,
            "units_treated": 0,
            "avg_benefit_per_unit": 0.0,
            "total_benefit": 0.0,
            "program_cost": 0.0,
            "gross_value": 0.0,
            "net_value": 0.0,
            "roi": float("nan"),
            "cost_per_event": float("inf"),
        }

    benefit = benefit_scores(spec, effect, outcome).loc[chosen[chosen].index]
    total_benefit = float(benefit.sum())
    cost = float(n * spec.treatment.cost_per_unit)

    out: dict[str, float | str] = {
        "policy": label,
        "units_treated": n,
        "avg_benefit_per_unit": float(benefit.mean()),
        "total_benefit": total_benefit,
        "program_cost": cost,
    }
    if outcome.value_per_event is not None:
        gross = total_benefit * outcome.value_per_event
        out.update(
            gross_value=float(gross),
            net_value=float(gross - cost),
            roi=float((gross - cost) / cost) if cost else float("nan"),
            cost_per_event=float(cost / total_benefit)
            if total_benefit
            else float("inf"),
        )
    return out

def compare_policies(
    spec: UseCaseSpec,
    policies: dict[str, pd.Series],
    effect: pd.Series,
    outcome: Outcome | None = None,
) -> pd.DataFrame:
    """Price several selections side by side against the same effects."""
    rows = [
        policy_economics(spec, sel, effect, outcome, label)
        for label, sel in policies.items()
    ]
    frame = pd.DataFrame(rows)
    if "net_value" in frame.columns:
        frame = frame.sort_values("net_value", ascending=False).reset_index(drop=True)
    return frame

# ---------------------------------------------------------------------------
# Qini: evaluating a ranking without an answer key
# ---------------------------------------------------------------------------

def qini_curve(
    frame: pd.DataFrame,
    spec: UseCaseSpec,
    scores: pd.Series,
    n_points: int = 25,
    outcome: Outcome | None = None,
) -> pd.DataFrame:
    """Qini curve computed from observed outcomes, not from ground truth.

    At each depth k, take the top k units by score and compute

        qini(k) = Y_treated(k) - Y_control(k) * N_treated(k) / N_control(k)

    which is the incremental outcome attributable to treating that group, scaling
    the control arm up to the treated arm's size. Signs are applied through the
    spec so a minimized outcome reads the same way as a maximized one.

    This matters because it is the only ranking evaluation here that works on real
    data. The policy comparisons against planted truth are synthetic scaffolding; this
    is what you would actually run in production to check a model still ranks.

    Caveat worth stating out loud: this is unbiased for a randomized treatment. On
    observationally assigned treatment, as in both bundled use cases, it inherits
    the same confounding as any raw comparison. Use it to compare rankings against
    each other, not to estimate an absolute effect.
    """
    outcome = outcome or spec.outcome
    work = pd.DataFrame(
        {
            "score": scores.to_numpy(),
            "t": frame[COL_TREATMENT].to_numpy(),
            "y": frame[COL_OUTCOME].to_numpy(dtype=float) * outcome.sign,
        }
    ).sort_values("score", ascending=False, kind="mergesort")

    cum_t = work["t"].cumsum().to_numpy()
    cum_c = (1 - work["t"]).cumsum().to_numpy()
    cum_yt = (work["y"] * work["t"]).cumsum().to_numpy()
    cum_yc = (work["y"] * (1 - work["t"])).cumsum().to_numpy()

    n = len(work)
    depths = np.unique(np.linspace(1, n, n_points).astype(int))

    with np.errstate(divide="ignore", invalid="ignore"):
        qini = cum_yt - np.where(cum_c > 0, cum_yc * cum_t / np.maximum(cum_c, 1), 0.0)

    total = float(qini[-1])
    rows = []
    for k in depths:
        i = k - 1
        rows.append(
            {
                "depth": int(k),
                "share_targeted": k / n,
                "n_treated_in_group": int(cum_t[i]),
                "n_control_in_group": int(cum_c[i]),
                "qini": float(qini[i]),
                # A ranking with no signal traces this straight line.
                "qini_random": total * (k / n),
            }
        )
    return pd.DataFrame(rows)

def auuc(curve: pd.DataFrame) -> float:
    """Area between the Qini curve and the random line, normalized.

    Positive means the ranking beats random. Zero means it carries no signal.
    Negative means it is actively worse than random, which does happen and is worth
    knowing before shipping.
    """
    x = curve["share_targeted"].to_numpy()
    lift = curve["qini"].to_numpy() - curve["qini_random"].to_numpy()
    area = float(np.trapz(lift, x))
    scale = abs(float(curve["qini"].iloc[-1]))
    return area / scale if scale else 0.0

# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def write_allocation(
    session,
    spec: UseCaseSpec,
    frame: pd.DataFrame,
    selected: pd.Series,
    effect: pd.Series,
    policy_label: str,
    table: str = "ALLOCATION",
) -> str:
    """Persist a selection so the agent and app read one shared decision.

    Written as a table rather than recomputed downstream, so the number quoted in a
    chat answer and the number on a dashboard cannot drift apart.
    """
    out = pd.DataFrame(
        {
            spec.unit.id_column: frame[COL_UNIT_ID].to_numpy(),
            "POLICY": policy_label,
            "SELECTED": selected.astype(bool).to_numpy(),
            "CATE": effect.to_numpy(dtype=float),
            "BENEFIT": benefit_scores(spec, effect).to_numpy(dtype=float),
            "NET_VALUE": net_value_per_unit(spec, effect).to_numpy(dtype=float)
            if spec.outcome.value_per_event is not None
            else np.nan,
        }
    )
    session.write_pandas(
        out,
        table,
        database=spec.database,
        schema="MODELS",
        auto_create_table=True,
        overwrite=True,
        quote_identifiers=False,
    )
    return spec.models(table)

def write_qini(
    session,
    spec: UseCaseSpec,
    curve: pd.DataFrame,
    label: str | None = None,
    table: str = "QINI_CURVE",
) -> str:
    """Persist one or more Qini curves.

    ``label`` names a single-model frame. Pass None when the frame already carries a
    MODEL column, which is how several rankings are stored together. Storing every
    ranking that was evaluated matters for the agent: asked whether risk targeting
    is good enough, it can only answer with a number if the risk curve is actually
    in the table. With only the winning curve persisted it hedges, which reads as
    evasion even though the underlying result is decisive.
    """
    out = curve.copy()
    out.columns = [c.upper() for c in out.columns]
    if label is not None:
        out["MODEL"] = label
    elif "MODEL" not in out.columns:
        raise ValueError("pass a label, or include a MODEL column in the frame")
    session.write_pandas(
        out,
        table,
        database=spec.database,
        schema="MODELS",
        auto_create_table=True,
        overwrite=True,
        quote_identifiers=False,
    )
    return spec.models(table)

def _resolve(frame: pd.DataFrame, column: str) -> str:
    """Case-insensitive column lookup, so specs need not match Snowflake casing."""
    available = {c.upper(): c for c in frame.columns}
    if column.upper() not in available:
        raise KeyError(
            f"column '{column}' is not in the analysis frame. Available: {sorted(frame.columns)}"
        )
    return available[column.upper()]
```

### `framework/causal_core/causal.py`

Copy code

```
"""Layer B: estimators that adjust for selection and can be attacked.

Three methods, chosen so they lean on *different* assumptions:

``dr_ate``
    Augmented inverse propensity weighting with cross-fitting. Consistent if
    either the propensity model or the outcome model is right, which is why it is
    the headline number rather than plain regression adjustment.

``causal_forest_cate``
    econml's ``CausalForestDML``. Produces per-unit effects with honest
    intervals, which is what the allocation layer needs. This is the only
    estimator here whose output can rank units.

``did_estimate``
    Difference-in-differences on the panel. Assumes parallel pre-trends rather
    than no unobserved confounding, so it is a genuinely independent check.
    Targets the effect among the treated, not the population average.

Agreement between methods that rest on different assumptions is far stronger
evidence than a small p-value from any one of them.

Everything here uses econml and scikit-learn from the Snowflake Anaconda channel.
dowhy is NOT importable alongside econml (numpy>2 vs numpy<2); refutation lives
in :mod:`causal_core.refute`, which calls an isolated stored procedure.
"""

from __future__ import annotations

import json

import numpy as np
import pandas as pd
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
)
from sklearn.model_selection import StratifiedKFold

from .data import COL_OUTCOME, COL_TREATMENT, COL_UNIT_ID, design_matrix
from .results import EstimateResult, normal_ci
from .spec import Outcome, UseCaseSpec

DEFAULT_TRIM = 0.02
DEFAULT_FOLDS = 5

# ---------------------------------------------------------------------------
# Propensity and overlap
# ---------------------------------------------------------------------------

def fit_propensity(
    frame: pd.DataFrame,
    spec: UseCaseSpec,
    n_folds: int = DEFAULT_FOLDS,
    random_state: int = 11,
) -> pd.Series:
    """Cross-fitted probability of treatment for every unit.

    Cross-fitting matters. An in-sample propensity score is overfitted toward the
    observed treatment, which pushes weights toward 1 and quietly reintroduces
    exactly the bias the weighting was supposed to remove.
    """
    X = design_matrix(spec, frame)
    t = frame[COL_TREATMENT].to_numpy()
    out = np.zeros(len(frame), dtype=float)

    splitter = StratifiedKFold(
        n_splits=n_folds, shuffle=True, random_state=random_state
    )
    for train_idx, test_idx in splitter.split(X, t):
        model = HistGradientBoostingClassifier(
            max_iter=200, learning_rate=0.08, max_depth=6, random_state=random_state
        )
        model.fit(X.iloc[train_idx], t[train_idx])
        out[test_idx] = model.predict_proba(X.iloc[test_idx])[:, 1]

    return pd.Series(out, index=frame.index, name="propensity")

def overlap_report(
    frame: pd.DataFrame,
    propensity: pd.Series,
    trim: float = DEFAULT_TRIM,
) -> dict[str, float | int]:
    """Whether comparable untreated units actually exist.

    This is the diagnostic that decides whether a question is answerable at all.
    When a cohort has almost no untreated units, no method recovers the effect and
    the honest response is to refuse rather than to report a number.
    """
    t = frame[COL_TREATMENT].to_numpy()
    e = propensity.to_numpy()

    treated_e, control_e = e[t == 1], e[t == 0]
    outside = (e < trim) | (e > 1 - trim)

    # Common support: the propensity range where both arms are represented.
    lo = max(treated_e.min(), control_e.min())
    hi = min(treated_e.max(), control_e.max())

    return {
        "n": int(len(frame)),
        "n_treated": int(t.sum()),
        "treated_share": float(t.mean()),
        "propensity_min": float(e.min()),
        "propensity_max": float(e.max()),
        "treated_propensity_mean": float(treated_e.mean()),
        "control_propensity_mean": float(control_e.mean()),
        "common_support_low": float(lo),
        "common_support_high": float(hi),
        "n_outside_trim": int(outside.sum()),
        "share_outside_trim": float(outside.mean()),
        # The single number to look at: how many treated units have no plausible
        # untreated counterpart.
        "share_treated_above_0_95": float((treated_e > 0.95).mean()),
        "trim": float(trim),
    }

def is_identified(
    overlap: dict[str, float | int], max_extreme_share: float = 0.25
) -> tuple[bool, str]:
    """Decide whether an effect is estimable, and say why if not.

    Used by the agent tools so refusal is a property of the data rather than a
    scripted behavior.
    """
    share = float(overlap["share_treated_above_0_95"])
    if share > max_extreme_share:
        return False, (
            f"{share:.1%} of treated units have a propensity above 0.95, meaning "
            "there is effectively no comparable untreated group. No adjustment "
            "method can recover the effect here, so any point estimate would be "
            "an extrapolation from the model rather than a measurement."
        )
    if int(overlap["n_treated"]) < 100:
        return False, (
            f"only {overlap['n_treated']} treated units in this cohort, which is too "
            "few for a stable estimate."
        )
    return (
        True,
        "overlap is adequate: comparable untreated units exist across the propensity range.",
    )

def balance_table(
    frame: pd.DataFrame,
    spec: UseCaseSpec,
    propensity: pd.Series,
    trim: float = DEFAULT_TRIM,
) -> pd.DataFrame:
    """Standardized mean differences before and after IPW.

    A standardized difference above about 0.1 after weighting is the conventional
    signal that a covariate is still imbalanced and the adjustment has not done
    its job.
    """
    X = design_matrix(spec, frame)
    t = frame[COL_TREATMENT].to_numpy()
    e = propensity.to_numpy().clip(trim, 1 - trim)
    w = np.where(t == 1, 1 / e, 1 / (1 - e))

    rows = []
    for col in X.columns:
        x = X[col].to_numpy()
        m1, m0 = x[t == 1].mean(), x[t == 0].mean()
        pooled = np.sqrt((x[t == 1].var() + x[t == 0].var()) / 2)
        raw = (m1 - m0) / pooled if pooled > 0 else 0.0

        w1, w0 = w[t == 1], w[t == 0]
        wm1 = np.average(x[t == 1], weights=w1)
        wm0 = np.average(x[t == 0], weights=w0)
        weighted = (wm1 - wm0) / pooled if pooled > 0 else 0.0

        rows.append(
            {
                "covariate": col,
                "smd_unadjusted": raw,
                "smd_weighted": weighted,
                "still_imbalanced": abs(weighted) > 0.10,
            }
        )
    return pd.DataFrame(rows).sort_values("smd_weighted", key=np.abs, ascending=False)

# ---------------------------------------------------------------------------
# Doubly robust ATE
# ---------------------------------------------------------------------------

def dr_ate(
    frame: pd.DataFrame,
    spec: UseCaseSpec,
    outcome: Outcome | None = None,
    propensity: pd.Series | None = None,
    trim: float = DEFAULT_TRIM,
    n_folds: int = DEFAULT_FOLDS,
    random_state: int = 11,
) -> EstimateResult:
    """Cross-fitted AIPW estimate of the average treatment effect.

    The influence-function form gives a standard error that reflects both the
    outcome model and the weighting, so unlike the naive intervals in
    :mod:`causal_core.naive` this one widens when the data is genuinely
    uninformative.
    """
    outcome = outcome or spec.outcome
    X = design_matrix(spec, frame)
    t = frame[COL_TREATMENT].to_numpy()
    y = frame[COL_OUTCOME].to_numpy(dtype=float)

    if propensity is None:
        propensity = fit_propensity(
            frame, spec, n_folds=n_folds, random_state=random_state
        )
    e = propensity.to_numpy().clip(trim, 1 - trim)

    mu1, mu0 = _cross_fit_outcome_models(X, t, y, outcome, n_folds, random_state)

    keep = (propensity.to_numpy() >= trim) & (propensity.to_numpy() <= 1 - trim)
    n_dropped = int((~keep).sum())

    # AIPW influence function.
    psi = (mu1 - mu0) + t * (y - mu1) / e - (1 - t) * (y - mu0) / (1 - e)
    psi = psi[keep]

    estimate = float(psi.mean())
    se = float(psi.std(ddof=1) / np.sqrt(len(psi)))
    low, high = normal_ci(estimate, se)

    overlap = overlap_report(frame, propensity, trim=trim)
    identified, reason = is_identified(overlap)

    notes = [
        "Doubly robust: consistent if either the propensity model or the outcome "
        "model is correctly specified, rather than requiring both.",
        "Nuisance models are cross-fitted, so the propensity scores are not "
        "overfitted toward the observed treatment.",
        f"Trimmed {n_dropped} units with propensity outside [{trim}, {1 - trim}].",
        "Still assumes no unobserved confounding. Run the refutation suite before "
        "acting on it.",
    ]
    if not identified:
        notes.append(f"OVERLAP WARNING: {reason}")

    return EstimateResult(
        method="doubly robust (AIPW)",
        outcome_column=outcome.column,
        estimate=estimate,
        se=se,
        ci_low=low,
        ci_high=high,
        baseline=float(mu0[keep].mean()),
        n=int(keep.sum()),
        n_treated=int(t[keep].sum()),
        identified=identified,
        diagnostics={
            "target": "ate",
            "n_dropped_by_trim": n_dropped,
            "identification_reason": reason,
            **overlap,
        },
        notes=notes,
    )

# ---------------------------------------------------------------------------
# Heterogeneous effects
# ---------------------------------------------------------------------------

def causal_forest_cate(
    frame: pd.DataFrame,
    spec: UseCaseSpec,
    outcome: Outcome | None = None,
    n_estimators: int = 300,
    min_samples_leaf: int = 30,
    random_state: int = 11,
) -> EstimateResult:
    """Per-unit treatment effects via econml's CausalForestDML.

    This is the estimator the decision actually depends on. The ATE can be right
    while the per-unit effects are useless, so what matters here is whether the
    per-unit estimates can rank units, which the notebook tests against a policy
    comparison rather than assuming.
    """
    from econml.dml import CausalForestDML

    outcome = outcome or spec.outcome
    X = design_matrix(spec, frame)
    t = frame[COL_TREATMENT].to_numpy()
    y = frame[COL_OUTCOME].to_numpy(dtype=float)

    # model_y must be a REGRESSOR even when the outcome is binary. DML
    # residualizes the outcome rather than classifying it, so it needs E[Y|X] as a
    # continuous prediction. Passing a classifier here fails with
    # "Cannot use a classifier as a first stage model when the target is
    # continuous!". Only the treatment model is a classifier, paired with
    # discrete_treatment=True.
    est = CausalForestDML(
        model_y=HistGradientBoostingRegressor(max_iter=150, random_state=random_state),
        model_t=HistGradientBoostingClassifier(max_iter=150, random_state=random_state),
        discrete_treatment=True,
        n_estimators=n_estimators,
        min_samples_leaf=min_samples_leaf,
        random_state=random_state,
    )
    est.fit(y, t, X=X)

    cate = pd.Series(est.effect(X).ravel(), index=frame.index, name="cate")
    lb, ub = est.effect_interval(X, alpha=0.05)
    ate = float(est.ate(X))
    ate_lb, ate_ub = est.ate_interval(X, alpha=0.05)

    return EstimateResult(
        method="causal forest (DML)",
        outcome_column=outcome.column,
        estimate=ate,
        se=None,
        ci_low=float(ate_lb),
        ci_high=float(ate_ub),
        baseline=float(frame.loc[frame[COL_TREATMENT] == 0, COL_OUTCOME].mean()),
        n=len(frame),
        n_treated=int(t.sum()),
        cate=cate,
        diagnostics={
            "target": "ate",
            "n_estimators": n_estimators,
            "cate_p10": float(np.percentile(cate, 10)),
            "cate_p50": float(np.percentile(cate, 50)),
            "cate_p90": float(np.percentile(cate, 90)),
            "cate_interval_mean_width": float(np.mean(ub - lb)),
            # Share of units whose individual interval excludes zero. If this is
            # near zero the model found no unit it can confidently say anything
            # about, regardless of how much spread the point estimates show.
            "share_individually_significant": float(np.mean((lb > 0) | (ub < 0))),
        },
        notes=[
            "Orthogonalized: outcome and treatment are both residualized before "
            "the effect is fit, so confounding enters through the nuisance models "
            "rather than the effect estimate.",
            "Per-unit intervals are honest but wide. Use the ranking, not the "
            "individual numbers, for allocation.",
        ],
    )

# ---------------------------------------------------------------------------
# Difference in differences
# ---------------------------------------------------------------------------

def did_estimate(
    did_frame: pd.DataFrame,
    spec: UseCaseSpec,
    event_study: pd.DataFrame | None = None,
) -> EstimateResult:
    """Difference-in-differences from unit-level pre/post means.

    Takes the frame produced by :func:`causal_core.data.load_did_frame`, which has
    one row per unit with its mean outcome before and after treatment.

    Comparing the change in those means across arms is algebraically identical to
    a two-way fixed effects regression on the full panel, but it runs on
    thousands of rows instead of millions, and the standard error is already
    clustered at the unit level because each unit contributes one observation.

    Rests on parallel pre-trends rather than on no unobserved confounding, so it
    is a genuinely independent check on the AIPW estimate rather than a
    restatement of it. Targets the effect among the treated.
    """
    treated = did_frame.loc[did_frame[COL_TREATMENT] == 1, "DELTA"].dropna()
    control = did_frame.loc[did_frame[COL_TREATMENT] == 0, "DELTA"].dropna()

    estimate = float(treated.mean() - control.mean())
    se = float(
        np.sqrt(treated.var(ddof=1) / len(treated) + control.var(ddof=1) / len(control))
    )
    low, high = normal_ci(estimate, se)

    notes = [
        "Assumes parallel pre-treatment trends. That is a different assumption "
        "from no unobserved confounding, so agreement with AIPW is meaningful.",
        "Unit-level differences, so the standard error is clustered by unit by "
        "construction rather than by a correction.",
    ]
    diagnostics: dict[str, float | str | int] = {
        "target": "att",
        "n_treated_units": int(len(treated)),
        "n_control_units": int(len(control)),
        "pre_mean_treated": float(
            did_frame.loc[did_frame[COL_TREATMENT] == 1, "PRE_MEAN"].mean()
        ),
        "pre_mean_control": float(
            did_frame.loc[did_frame[COL_TREATMENT] == 0, "PRE_MEAN"].mean()
        ),
    }

    if event_study is not None and len(event_study):
        pre_trend = _pre_trend_test(event_study)
        diagnostics.update(
            pre_trend_slope=pre_trend["slope"], pre_trend_p_value=pre_trend["p_value"]
        )
        notes.append(
            f"Pre-trend test: the treated-minus-control gap moves by "
            f"{pre_trend['slope']:+.5f} per period before treatment "
            f"(p={pre_trend['p_value']:.3f})."
        )
        if pre_trend["p_value"] < 0.05:
            notes.append(
                "PRE-TREND WARNING: the gap was already moving before treatment, "
                "which undermines the parallel trends assumption."
            )

    return EstimateResult(
        method="difference in differences",
        outcome_column=spec.outcome.column,
        estimate=estimate,
        se=se,
        ci_low=low,
        ci_high=high,
        baseline=float(
            did_frame.loc[did_frame[COL_TREATMENT] == 0, "POST_MEAN"].mean()
        ),
        n=int(len(did_frame)),
        n_treated=int(len(treated)),
        diagnostics=diagnostics,
        notes=notes,
    )

# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def write_cate_scores(
    session,
    spec: UseCaseSpec,
    frame: pd.DataFrame,
    result: EstimateResult,
    table: str = "CATE_SCORES",
    propensity: pd.Series | None = None,
) -> str:
    """Persist per-unit effects so the agent and app never refit a model.

    This is the handoff between the econml world and everything else. Data moves
    through tables rather than pickles, which is mandatory here because the dowhy
    procedure runs on a different numpy and pandas major version.

    ``propensity`` is written alongside because it is what makes cohort-level
    refusal possible downstream. An agent asked about a narrow slice needs to know
    whether that slice has common support, and that question cannot be answered
    from an average treatment effect or a per-unit CATE alone. Without this column
    the agent can only report the whole-population verdict, which is exactly the
    kind of overconfident generalisation the gate exists to prevent.
    """
    if result.cate is None:
        raise ValueError(f"{result.method} produced no per-unit effects to write")

    out = pd.DataFrame(
        {
            spec.unit.id_column: frame[COL_UNIT_ID].to_numpy(),
            "CATE": result.cate.to_numpy(dtype=float),
            "BENEFIT": [
                spec.outcome.benefit(v) for v in result.cate.to_numpy(dtype=float)
            ],
            "METHOD": result.method,
            "OUTCOME_COLUMN": result.outcome_column,
        }
    )
    if propensity is not None:
        out["PROPENSITY"] = propensity.to_numpy(dtype=float)
        out["TREATED"] = frame[COL_TREATMENT].to_numpy(dtype=int)
    out["VALUE_PER_UNIT"] = (
        out["BENEFIT"] * spec.outcome.value_per_event
        if spec.outcome.value_per_event is not None
        else np.nan
    )
    out["COST_PER_UNIT"] = spec.treatment.cost_per_unit
    out["NET_VALUE_PER_UNIT"] = out["VALUE_PER_UNIT"] - out["COST_PER_UNIT"]

    fqn = spec.models(table)
    session.write_pandas(
        out,
        table,
        database=spec.database,
        schema="MODELS",
        auto_create_table=True,
        overwrite=True,
        quote_identifiers=False,
    )
    return fqn

def write_diagnostics(
    session,
    spec: UseCaseSpec,
    results: list[EstimateResult],
    table: str = "DIAGNOSTICS",
) -> str:
    """Persist one row per estimator so the receipt and app can read them."""
    rows = []
    for r in results:
        rows.append(
            {
                "METHOD": r.method,
                "OUTCOME_COLUMN": r.outcome_column,
                "ESTIMATE": float(r.estimate),
                "CI_LOW": None if r.ci_low is None else float(r.ci_low),
                "CI_HIGH": None if r.ci_high is None else float(r.ci_high),
                "TARGET": str(r.diagnostics.get("target", "ate")),
                "IDENTIFIED": bool(r.identified),
                "N": int(r.n),
                "N_TREATED": int(r.n_treated),
                "CATE_SPREAD": None if r.cate_spread is None else float(r.cate_spread),
                "VERDICT": r.direction_verdict(spec.outcome),
                "DIAGNOSTICS_JSON": json.dumps(r.diagnostics, default=float),
                "NOTES": " | ".join(r.notes),
            }
        )
    out = pd.DataFrame(rows)
    session.write_pandas(
        out,
        table,
        database=spec.database,
        schema="MODELS",
        auto_create_table=True,
        overwrite=True,
        quote_identifiers=False,
    )
    return spec.models(table)

# ---------------------------------------------------------------------------
# internals
# ---------------------------------------------------------------------------

def _cross_fit_outcome_models(
    X: pd.DataFrame,
    t: np.ndarray,
    y: np.ndarray,
    outcome: Outcome,
    n_folds: int,
    random_state: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Out-of-fold predictions of the treated and untreated response surfaces."""
    mu1 = np.zeros(len(y), dtype=float)
    mu0 = np.zeros(len(y), dtype=float)
    splitter = StratifiedKFold(
        n_splits=n_folds, shuffle=True, random_state=random_state
    )

    for train_idx, test_idx in splitter.split(X, t):
        for arm, target in ((1, mu1), (0, mu0)):
            arm_rows = train_idx[t[train_idx] == arm]
            model = _outcome_model(outcome, random_state)
            model.fit(X.iloc[arm_rows], y[arm_rows])
            target[test_idx] = _predict(model, X.iloc[test_idx])
    return mu1, mu0

def _outcome_model(outcome: Outcome, random_state: int):
    if outcome.is_binary:
        return HistGradientBoostingClassifier(
            max_iter=200, learning_rate=0.08, max_depth=6, random_state=random_state
        )
    return HistGradientBoostingRegressor(
        max_iter=200, learning_rate=0.08, max_depth=6, random_state=random_state
    )

def _predict(model, X: pd.DataFrame) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]
    return model.predict(X)

def _pre_trend_test(event_study: pd.DataFrame) -> dict[str, float]:
    """Regress the treated-minus-control gap on time, using pre-periods only."""
    import statsmodels.formula.api as smf

    pre = event_study[event_study["IS_PRE"].astype(bool)].copy()
    fit = smf.ols("GAP ~ PERIOD_INDEX", data=pre).fit()
    return {
        "slope": float(fit.params["PERIOD_INDEX"]),
        "p_value": float(fit.pvalues["PERIOD_INDEX"]),
    }
```

### `framework/causal_core/data.py`

Copy code

```
"""Read the five canonical tables and assemble a domain-blind analysis frame.

Downstream estimators never see domain column names. They receive a frame with
standardized names:

    UNIT_ID   the identifier
    TREAT     treatment indicator, 0 or 1
    Y         the outcome being estimated
    Y_PRE     the same outcome measured in the pre-treatment window
    <covariates>  under their own spec-declared names

Covariates may live in either ``UNIT`` (time-invariant) or ``UNIT_PERIOD``
(time-varying). The author does not declare which: this module looks them up in
the information schema and builds the right join. Time-varying covariates are
snapshotted at the **last pre-treatment period**, which is what keeps the
estimate free of post-treatment leakage.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pandas as pd

from .spec import (
    CAPACITY,
    DATA_SCHEMA,
    OUTCOME,
    TREATMENT,
    UNIT,
    UNIT_PERIOD,
    Outcome,
    UseCaseSpec,
)

if TYPE_CHECKING:  # pragma: no cover
    from snowflake.snowpark import Session

COL_UNIT_ID = "UNIT_ID"
# Deliberately not "T": pandas DataFrames expose .T as the transpose property,
# so a column named T cannot be reached by attribute access and silently returns
# a transposed frame instead. "TREAT" avoids that collision entirely.
COL_TREATMENT = "TREAT"
COL_OUTCOME = "Y"
COL_PRE_OUTCOME = "Y_PRE"

# Columns each canonical table must expose, beyond the spec-declared ones.
PERIOD_INDEX = "PERIOD_INDEX"
IS_PRE = "IS_PRE"
# The boolean treatment flag in TREATMENT is not fixed: its name is
# spec.treatment.column (TREATED in the bundled use cases).
TREATMENT_PERIOD = "TREATMENT_PERIOD"

class DataError(RuntimeError):
    """Raised when the canonical tables do not satisfy the framework contract."""

# ---------------------------------------------------------------------------
# Introspection
# ---------------------------------------------------------------------------

def _schema_columns(session: "Session", spec: UseCaseSpec) -> dict[str, set[str]]:
    """Map of table name to its column names, for the DATA schema."""
    rows = session.sql(
        f"""
        SELECT TABLE_NAME, COLUMN_NAME
        FROM {spec.database}.INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{DATA_SCHEMA}'
        """
    ).collect()
    out: dict[str, set[str]] = {}
    for row in rows:
        out.setdefault(row["TABLE_NAME"].upper(), set()).add(row["COLUMN_NAME"].upper())
    return out

def validate_tables(session: "Session", spec: UseCaseSpec) -> dict[str, Any]:
    """Check the contract and fail with a message that says how to fix it.

    Returns a report dict on success so a notebook can display it.
    """
    columns = _schema_columns(session, spec)

    missing_tables = [
        t for t in (UNIT, UNIT_PERIOD, TREATMENT, OUTCOME, CAPACITY) if t not in columns
    ]
    if missing_tables:
        raise DataError(
            f"{spec.database}.{DATA_SCHEMA} is missing canonical tables: {missing_tables}. "
            f"Run usecases/{spec.name}/01_contract.sql first, then either "
            f"02_generate_synthetic.sql (synthetic) or 03_bring_your_own_data.sql (real data)."
        )

    unit_id = spec.unit.id_column.upper()
    problems: list[str] = []

    for table in (UNIT, UNIT_PERIOD, TREATMENT, OUTCOME):
        if unit_id not in columns[table]:
            problems.append(f"{table} is missing the unit id column '{unit_id}'")

    for required, table in (
        (PERIOD_INDEX, UNIT_PERIOD),
        (IS_PRE, UNIT_PERIOD),
        (spec.panel.period_column.upper(), UNIT_PERIOD),
    ):
        if required not in columns[table]:
            problems.append(f"{table} is missing required column '{required}'")

    treated = spec.treatment.column.upper()
    if treated not in columns[TREATMENT]:
        problems.append(
            f"{TREATMENT} is missing the treatment column '{treated}' "
            "(treatment.column in usecase.yaml)"
        )

    for outcome in spec.all_outcomes:
        if outcome.column.upper() not in columns[OUTCOME]:
            problems.append(f"{OUTCOME} is missing outcome column '{outcome.column}'")

    if spec.outcome.periodic_column.upper() not in columns[UNIT_PERIOD]:
        problems.append(
            f"{UNIT_PERIOD} is missing '{spec.outcome.periodic_column}'. The outcome must "
            "be present per period or diff-in-diff cannot run. If the unit-level "
            "outcome is an aggregate, set outcome.panel_column in the spec to the "
            "per-period measure it aggregates."
        )

    for column in (
        spec.capacity.group_column.upper(),
        spec.capacity.slots_column.upper(),
    ):
        if column not in columns[CAPACITY]:
            problems.append(f"{CAPACITY} is missing required column '{column}'")

    known = columns[UNIT] | columns[UNIT_PERIOD]
    for covariate in spec.covariates.observed:
        if covariate.upper() not in known:
            problems.append(
                f"covariate '{covariate}' is in neither {UNIT} nor {UNIT_PERIOD}"
            )

    for attribute in spec.fairness.protected_attributes:
        if attribute.upper() not in known:
            problems.append(
                f"protected attribute '{attribute}' is in neither {UNIT} nor {UNIT_PERIOD}"
            )

    if problems:
        raise DataError(
            "canonical table contract not satisfied:\n  - " + "\n  - ".join(problems)
        )

    return {
        "database": spec.database,
        "tables": {
            t: len(columns[t])
            for t in (UNIT, UNIT_PERIOD, TREATMENT, OUTCOME, CAPACITY)
        },
        "covariates_from_unit": sorted(
            c for c in spec.covariates.observed if c.upper() in columns[UNIT]
        ),
        "covariates_from_panel": sorted(
            c
            for c in spec.covariates.observed
            if c.upper() not in columns[UNIT] and c.upper() in columns[UNIT_PERIOD]
        ),
    }

# ---------------------------------------------------------------------------
# Analysis frame
# ---------------------------------------------------------------------------

def analysis_frame_sql(
    session: "Session",
    spec: UseCaseSpec,
    outcome: Outcome | None = None,
    include_truth: bool = False,
) -> str:
    """Build the SQL for the unit-level analysis frame.

    Exposed separately from :func:`load_analysis_frame` so the agent tool
    procedures and the Streamlit app can reuse the identical definition instead
    of reimplementing the join.
    """
    outcome = outcome or spec.outcome
    columns = _schema_columns(session, spec)
    unit_id = spec.unit.id_column
    treated = spec.treatment.column

    attributes = list(
        dict.fromkeys(spec.covariates.observed + spec.fairness.protected_attributes)
    )
    from_unit = [c for c in attributes if c.upper() in columns[UNIT]]
    from_panel = [
        c
        for c in attributes
        if c.upper() not in columns[UNIT] and c.upper() in columns[UNIT_PERIOD]
    ]

    # Capacity group may live on either table; it is needed for allocation.
    group_col = spec.capacity.group_column
    if group_col.upper() in columns[UNIT] and group_col not in from_unit:
        from_unit.append(group_col)
    elif group_col.upper() in columns[UNIT_PERIOD] and group_col not in from_panel:
        from_panel.append(group_col)

    unit_selects = "".join(f",\n        u.{c}" for c in from_unit)
    panel_selects = "".join(f",\n        b.{c}" for c in from_panel)

    pre_outcome = (
        f"o.{outcome.pre_column}"
        if outcome.pre_column and outcome.pre_column.upper() in columns[OUTCOME]
        else f"b.{spec.outcome.column}"
    )

    truth_join = ""
    truth_select = ""
    if include_truth:
        truth_select = ",\n        tr.TRUE_ITE"
        truth_join = f"""
    LEFT JOIN {spec.truth("TRUE_ITE")} tr
        ON tr.{unit_id} = u.{unit_id}"""

    return f"""
    WITH baseline AS (
        -- Last pre-treatment period per unit. This snapshot is what prevents
        -- post-treatment information leaking into the covariates.
        SELECT *
        FROM (
            SELECT
                p.*,
                ROW_NUMBER() OVER (
                    PARTITION BY p.{unit_id}
                    ORDER BY p.{PERIOD_INDEX} DESC
                ) AS rn
            FROM {spec.data(UNIT_PERIOD)} p
            WHERE p.{IS_PRE}
        )
        WHERE rn = 1
    )
    SELECT
        u.{unit_id}                        AS {COL_UNIT_ID},
        t.{treated}::INT                   AS {COL_TREATMENT},
        o.{outcome.column}                 AS {COL_OUTCOME},
        {pre_outcome}                      AS {COL_PRE_OUTCOME}{unit_selects}{panel_selects}{truth_select}
    FROM {spec.data(UNIT)} u
    JOIN {spec.data(TREATMENT)} t ON t.{unit_id} = u.{unit_id}
    JOIN {spec.data(OUTCOME)}   o ON o.{unit_id} = u.{unit_id}
    JOIN baseline b              ON b.{unit_id} = u.{unit_id}{truth_join}
    """

def load_analysis_frame(
    session: "Session",
    spec: UseCaseSpec,
    outcome: Outcome | None = None,
    include_truth: bool = False,
) -> pd.DataFrame:
    """Unit-level frame ready for estimation.

    ``include_truth`` joins the planted per-unit effect. That column exists only
    in the synthetic use cases and must never be passed to an estimator: it is
    for grading after the fact.
    """
    sql = analysis_frame_sql(
        session, spec, outcome=outcome, include_truth=include_truth
    )
    frame = session.sql(sql).to_pandas()

    if frame.empty:
        raise DataError(
            f"analysis frame is empty for {spec.database}. The canonical tables exist but "
            "have no rows. Run 02_generate_synthetic.sql, or check the WHERE clauses in "
            "03_bring_your_own_data.sql."
        )
    if frame[COL_TREATMENT].nunique() < 2:
        raise DataError(
            f"analysis frame has only one treatment arm "
            f"({frame[COL_TREATMENT].unique().tolist()}). No effect is estimable."
        )
    return frame

def feature_columns(spec: UseCaseSpec, frame: pd.DataFrame) -> list[str]:
    """Covariate columns present in the frame, in spec order.

    Protected attributes are included only when the spec also lists them as
    covariates. Excluding them is a legitimate modeling choice, and the fairness
    audit reads them from the frame regardless.
    """
    available = {c.upper(): c for c in frame.columns}
    return [
        available[c.upper()] for c in spec.covariates.observed if c.upper() in available
    ]

def design_matrix(spec: UseCaseSpec, frame: pd.DataFrame) -> pd.DataFrame:
    """One-hot encode categoricals and return a numeric matrix.

    ``drop_first`` avoids the dummy trap for the linear nuisance models, and
    forest-based learners are indifferent to it.
    """
    features = feature_columns(spec, frame)
    categorical = [
        c
        for c in features
        if c.upper() in {x.upper() for x in spec.covariates.categorical}
    ]
    matrix = pd.get_dummies(frame[features], columns=categorical, drop_first=True)
    return matrix.astype(float)

# ---------------------------------------------------------------------------
# Panel and truth
# ---------------------------------------------------------------------------

def load_panel(session: "Session", spec: UseCaseSpec) -> pd.DataFrame:
    """Long panel for diff-in-diff, one row per unit per period."""
    unit_id = spec.unit.id_column
    treated = spec.treatment.column
    sql = f"""
    SELECT
        p.{unit_id}                        AS {COL_UNIT_ID},
        p.{spec.panel.period_column}       AS PERIOD,
        p.{PERIOD_INDEX}                   AS {PERIOD_INDEX},
        p.{IS_PRE}                         AS {IS_PRE},
        p.{spec.outcome.periodic_column}   AS {COL_OUTCOME},
        t.{treated}::INT                   AS {COL_TREATMENT}
    FROM {spec.data(UNIT_PERIOD)} p
    JOIN {spec.data(TREATMENT)} t ON t.{unit_id} = p.{unit_id}
    ORDER BY {COL_UNIT_ID}, {PERIOD_INDEX}
    """
    return session.sql(sql).to_pandas()

def load_did_frame(session: "Session", spec: "UseCaseSpec") -> pd.DataFrame:
    """One row per unit: mean outcome before and after, plus treatment.

    Aggregation happens in Snowflake rather than in pandas. A 100k-unit panel is
    millions of rows, and pulling all of them back only to average them is both
    slow and pointless.

    The difference of these two means, compared across arms, is algebraically the
    same as a two-way fixed effects diff-in-diff on the full panel. Because each
    unit contributes exactly one row, the resulting standard error is already
    clustered at the unit level with no extra machinery.
    """
    unit_id = spec.unit.id_column
    treated = spec.treatment.column
    sql = f"""
    SELECT
        p.{unit_id}                                                   AS {COL_UNIT_ID},
        t.{treated}::INT                                              AS {COL_TREATMENT},
        AVG(IFF(p.{IS_PRE}, p.{spec.outcome.periodic_column}, NULL))      AS PRE_MEAN,
        AVG(IFF(NOT p.{IS_PRE}, p.{spec.outcome.periodic_column}, NULL))  AS POST_MEAN,
        COUNT(IFF(p.{IS_PRE}, 1, NULL))                               AS N_PRE,
        COUNT(IFF(NOT p.{IS_PRE}, 1, NULL))                           AS N_POST
    FROM {spec.data(UNIT_PERIOD)} p
    JOIN {spec.data(TREATMENT)} t ON t.{unit_id} = p.{unit_id}
    GROUP BY 1, 2
    """
    frame = session.sql(sql).to_pandas()
    frame["DELTA"] = frame["POST_MEAN"] - frame["PRE_MEAN"]
    return frame

def load_event_study(session: "Session", spec: "UseCaseSpec") -> pd.DataFrame:
    """Treated-minus-control gap by period, aggregated in SQL.

    A flat line before treatment and a step after is the visual the entire
    diff-in-diff argument rests on.
    """
    unit_id = spec.unit.id_column
    treated = spec.treatment.column
    sql = f"""
    SELECT
        p.{PERIOD_INDEX}                                                  AS {PERIOD_INDEX},
        ANY_VALUE(p.{IS_PRE})                                             AS {IS_PRE},
        AVG(IFF(t.{treated}, p.{spec.outcome.periodic_column}, NULL))     AS TREATED_MEAN,
        AVG(IFF(NOT t.{treated}, p.{spec.outcome.periodic_column}, NULL)) AS CONTROL_MEAN
    FROM {spec.data(UNIT_PERIOD)} p
    JOIN {spec.data(TREATMENT)} t ON t.{unit_id} = p.{unit_id}
    GROUP BY 1
    ORDER BY 1
    """
    frame = session.sql(sql).to_pandas()
    frame["GAP"] = frame["TREATED_MEAN"] - frame["CONTROL_MEAN"]
    return frame

def load_capacity(session: "Session", spec: UseCaseSpec) -> pd.DataFrame:
    """Available slots by group, aggregated across periods."""
    sql = f"""
    SELECT
        {spec.capacity.group_column} AS GROUP_KEY,
        SUM({spec.capacity.slots_column}) AS SLOTS
    FROM {spec.data(CAPACITY)}
    GROUP BY 1
    ORDER BY 1
    """
    return session.sql(sql).to_pandas()

def load_truth(session: "Session", spec: UseCaseSpec) -> pd.DataFrame | None:
    """SYNTHETIC SCAFFOLDING. Planted per-unit effects, or None if TRUTH is unavailable.

    Returning None rather than raising is deliberate: revoking access to TRUTH is
    a supported way to prove an estimate was produced blind, and every notebook
    should degrade gracefully when that happens.
    """
    try:
        return session.sql(f"SELECT * FROM {spec.truth('TRUE_ITE')}").to_pandas()
    except Exception:
        return None

def create_analysis_view(
    session: "Session",
    spec: UseCaseSpec,
    outcome: Outcome | None = None,
    view: str = "V_ANALYSIS_FRAME",
) -> str:
    """Publish the analysis frame as a view so isolated procedures can read it.

    The dowhy refutation procedure cannot import this module. dowhy requires numpy>=2
    and econml requires numpy<2, so the two live in separate environments and cannot
    share a process, let alone an in-memory DataFrame.

    Rather than duplicating the frame-building SQL inside that procedure, where it
    would drift from this one, publish it once as a view. The procedure then selects
    from a stable contract and stays domain-blind: it learns the treatment, outcome and
    covariate names from MODELS.SPEC_SNAPSHOT at run time.

    This is the same table-as-interface pattern the whole repo uses for crossing an
    environment boundary.
    """
    fqn = spec.models(view)
    session.sql(
        f"CREATE OR REPLACE VIEW {fqn} AS\n"
        + analysis_frame_sql(session, spec, outcome=outcome, include_truth=False)
    ).collect()
    return fqn
```

### `framework/causal_core/equity.py`

Copy code

```
"""The fairness gate. Fails the pipeline rather than printing a warning.

Targeting by estimated impact has a specific, predictable failure mode: units that
are easier to reach look more impactable, and reachability correlates with
advantage. A model trained to maximize measured impact will therefore learn to
concentrate help on the people who were already easiest to help, and the
disparity is invisible in aggregate accuracy metrics.

This is the mechanism documented in Obermeyer et al., *Science* 2019, which found a
widely deployed commercial care-management algorithm systematically under-referred
Black patients because it used healthcare spending as a proxy for illness. The
model was not wrong about spending. It was answering a different question from the
one the program needed answered.

Both bundled use cases plant this on purpose. In the payer case, harder-to-reach
members answer outreach less often, so they genuinely have smaller measured
effects. In the churn case, one market is systematically under-targeted. In both,
an uplift-optimal policy will quietly deprioritize a protected group, and the
check below is what catches it.

A note on what this can and cannot do: parity of *selection rate* is one fairness
definition among several, and it is not always the right one. A group with
genuinely lower treatment effects is not being wronged by receiving fewer
treatments, and forcing parity there costs real outcomes. What this module
provides is the measurement and an explicit, logged choice. It does not pretend the
tradeoff is free.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .spec import UseCaseSpec

class EquityGateFailure(RuntimeError):
    """Raised when a selection breaches the spec's disparity threshold.

    Deliberately an exception rather than a return value: a fairness check that
    can be ignored by not reading the output is not a gate.
    """

@dataclass
class DisparityReport:
    """Selection rates by protected group, and whether the gate passes."""

    attribute: str
    max_disparity_ratio: float
    table: pd.DataFrame
    observed_ratio: float
    passed: bool
    worst_group: str
    best_group: str
    notes: list[str] = field(default_factory=list)

    def summary(self) -> dict[str, object]:
        return {
            "attribute": self.attribute,
            "observed_ratio": round(self.observed_ratio, 4),
            "threshold": self.max_disparity_ratio,
            "passed": self.passed,
            "most_favoured": self.best_group,
            "least_favoured": self.worst_group,
        }

def disparity_report(
    frame: pd.DataFrame,
    spec: UseCaseSpec,
    selected: pd.Series,
    attribute: str,
) -> DisparityReport:
    """Selection rate per level of one protected attribute.

    The ratio reported is highest selection rate over lowest, across levels with
    enough population to be meaningful. Tiny groups are excluded from the ratio
    because a group of 30 units can produce a wild rate from noise alone, and
    failing a build on that is not useful.
    """
    col = _resolve(frame, attribute)
    chosen = selected.astype(bool)

    grouped = (
        pd.DataFrame({"group": frame[col].to_numpy(), "selected": chosen.to_numpy()})
        .groupby("group", dropna=False)
        .agg(population=("selected", "size"), selected=("selected", "sum"))
    )
    grouped["selection_rate"] = grouped["selected"] / grouped["population"]
    grouped["population_share"] = grouped["population"] / grouped["population"].sum()
    grouped["share_of_selected"] = grouped["selected"] / max(
        int(grouped["selected"].sum()), 1
    )
    # Above 1.0 means the group is over-represented among those chosen relative to
    # its size, below 1.0 means under-represented.
    grouped["representation_index"] = (
        grouped["share_of_selected"] / grouped["population_share"]
    )

    min_pop = max(50, int(0.01 * len(frame)))
    eligible = grouped[grouped["population"] >= min_pop]
    notes: list[str] = []
    excluded = grouped.index.difference(eligible.index).tolist()
    if excluded:
        notes.append(
            f"excluded from the ratio for having fewer than {min_pop} units: {excluded}"
        )

    if eligible.empty or eligible["selection_rate"].max() == 0:
        return DisparityReport(
            attribute=attribute,
            max_disparity_ratio=spec.fairness.max_disparity_ratio,
            table=grouped.round(4),
            observed_ratio=float("nan"),
            passed=True,
            worst_group="n/a",
            best_group="n/a",
            notes=notes + ["no group was selected, so disparity is undefined"],
        )

    rates = eligible["selection_rate"]
    best, worst = str(rates.idxmax()), str(rates.idxmin())
    lowest = float(rates.min())
    ratio = float("inf") if lowest == 0 else float(rates.max() / lowest)

    if lowest == 0:
        notes.append(
            f"group '{worst}' received ZERO treatments. That is total exclusion "
            "rather than a disparity of degree, and no ratio threshold can express it."
        )

    return DisparityReport(
        attribute=attribute,
        max_disparity_ratio=spec.fairness.max_disparity_ratio,
        table=grouped.round(4),
        observed_ratio=ratio,
        passed=bool(ratio <= spec.fairness.max_disparity_ratio),
        worst_group=worst,
        best_group=best,
        notes=notes,
    )

def check_equity(
    frame: pd.DataFrame,
    spec: UseCaseSpec,
    selected: pd.Series,
    raise_on_failure: bool = True,
) -> list[DisparityReport]:
    """Run the gate across every protected attribute in the spec.

    Raises :class:`EquityGateFailure` by default. Pass ``raise_on_failure=False``
    only when you intend to inspect and then act on the result, for example when
    comparing an unconstrained policy against a constrained one.
    """
    reports = [
        disparity_report(frame, spec, selected, attribute)
        for attribute in spec.fairness.protected_attributes
    ]
    failures = [r for r in reports if not r.passed]

    if failures and raise_on_failure:
        detail = "; ".join(
            f"{r.attribute}: rate ratio {r.observed_ratio:.2f} "
            f"(threshold {r.max_disparity_ratio}), '{r.best_group}' favoured over '{r.worst_group}'"
            for r in failures
        )
        raise EquityGateFailure(
            f"selection breaches the disparity threshold on "
            f"{len(failures)} of {len(reports)} protected attributes. {detail}. "
            "Either accept the disparity explicitly and record why, or re-allocate "
            "with equity.allocate_with_floor()."
        )
    return reports

def allocate_with_floor(
    frame: pd.DataFrame,
    spec: UseCaseSpec,
    scores: pd.Series,
    capacity: int,
    attributes: str | list[str] | None = None,
    strict: bool = True,
) -> pd.Series:
    """Allocate under capacity while keeping every protected group inside the threshold.

    Two wrong versions preceded this one, and both failures are instructive.

    **A floor alone does not work.** Guaranteeing each group a minimum leaves the
    remaining capacity to be allocated purely by score, and that remainder piles
    into whichever group scores highest, so the rate ratio reopens. This reduced
    disparity from 13.6x to 2.1x and still failed a 1.25x threshold.

    **Constraining each attribute separately does not work either.** Satisfying
    floors on insurance type while only capping deprivation quintile left
    deprivation at 6.3x, worse than constraining deprivation alone. Fairness on one
    axis does not give fairness on another, and enforcing them one at a time lets
    the first constraint consume the capacity the second one needed.

    What works is constraining the **intersection**. Units are bucketed by the
    combination of all protected attribute values, and each bucket gets

        floor_rate   = overall_rate / sqrt(R)
        ceiling_rate = overall_rate * sqrt(R)

    Every marginal selection rate is then a population-weighted average of bucket
    rates that all sit inside that band, so every marginal ratio is bounded by
    ceiling/floor = R. That is a guarantee rather than an empirical hope.

    The cost is real: slots move from higher-scoring units to satisfy the
    constraint, so total expected benefit falls. Notebook 03 prices it rather than
    hiding it, which is the only defensible way to hand this to a business owner.

    Raises :class:`EquityGateFailure` when the threshold cannot be met, rather than
    returning a selection that breaches it. See
    :func:`min_achievable_disparity_ratio` for what is reachable at a given capacity.
    Pass ``strict=False`` to get the best-effort allocation without the check.
    """
    if attributes is None:
        attributes = list(spec.fairness.protected_attributes)
    elif isinstance(attributes, str):
        attributes = [attributes]

    cols = [_resolve(frame, a) for a in attributes]
    ratio = spec.fairness.max_disparity_ratio
    # A 2% safety margin on the band, plus conservative rounding below (ceil for
    # floors, floor for ceilings). Without it, integer rounding of bucket sizes
    # lands the realised ratio a hair OVER the threshold: an earlier version
    # produced 1.2503 against a limit of 1.25 and failed its own gate. Rounding
    # that can only tighten the constraint is worth the fraction of a percent of
    # benefit it costs.
    band = float(np.sqrt(ratio)) * 0.98
    overall_rate = capacity / len(frame)

    # Bucket on the intersection of every protected attribute.
    cell = frame[cols].astype(str).agg("|".join, axis=1).rename("cell")
    populations = cell.value_counts()

    quotas = populations * overall_rate
    floors = np.ceil(quotas / band).astype(int)
    ceilings = np.floor(quotas * band).astype(int)

    # When a bucket's quota is small, the integer grid is coarser than the band and
    # the floor can land ABOVE the ceiling. A property test caught this at threshold
    # 1.05 with capacity 200 over 15 buckets: quota 13.3, floor 14, ceiling 13. The
    # old code used the inverted pair and quietly returned a selection that breached
    # its own gate. Where that happens no integer allocation can honour the band, so
    # fall back to proportional allocation, which is the closest to parity available.
    discretisation_limited = bool((floors > ceilings).any())

    selected = pd.Series(False, index=frame.index, name="selected")

    def fill(bucket: str, target: int) -> int:
        """Take the highest-scoring `target` units from one bucket."""
        rows = frame.index[(cell == bucket) & (~selected)]
        take = int(min(target, len(rows)))
        if take > 0:
            selected.loc[scores.loc[rows].nlargest(take).index] = True
        return take

    if discretisation_limited:
        # Parity-optimal integer allocation, by largest fractional remainder: floor
        # every bucket, then hand the leftover slots to the buckets whose quota was
        # cut by the most. Distributing that leftover BY SCORE instead re-concentrates
        # it and pushes the ratio back up, measured at 1.053 against a 1.05 threshold
        # where this approach reaches 1.02. Selection WITHIN a bucket is still by
        # score, so the best units are chosen; only the bucket sizes are equalised.
        base = np.floor(quotas).astype(int)
        leftover = max(0, capacity - int(base.sum()))
        remainders = (quotas - np.floor(quotas)).sort_values(ascending=False)
        bonus = set(remainders.index[:leftover])
        for bucket in populations.index:
            fill(bucket, int(base[bucket]) + (1 if bucket in bonus else 0))
    else:
        # Pass 1: every bucket gets its floor, filled by score within the bucket.
        room: dict[str, int] = {}
        for bucket in populations.index:
            allowed = max(0, min(int(floors[bucket]), capacity - int(selected.sum())))
            taken = fill(bucket, allowed)
            room[bucket] = max(
                0, min(int(ceilings[bucket]), int(populations[bucket])) - taken
            )

        # Pass 2: spend what is left by global score, drawing only as many candidates
        # per bucket as that bucket has headroom, so no ceiling can be breached.
        remaining = capacity - int(selected.sum())
        if remaining > 0:
            pool_parts = []
            for bucket, headroom in room.items():
                if headroom <= 0:
                    continue
                rows = frame.index[(cell == bucket) & (~selected)]
                if len(rows):
                    pool_parts.append(
                        scores.loc[rows].nlargest(min(headroom, len(rows)))
                    )
            if pool_parts:
                pool = pd.concat(pool_parts)
                selected.loc[pool.nlargest(min(remaining, len(pool))).index] = True

    # Verify the guarantee rather than assuming it. Returning a selection that
    # breaches the threshold would defeat the purpose of the whole module, so this
    # either honours the bound or says plainly that it cannot.
    if strict:
        breaches = [
            r
            for r in (disparity_report(frame, spec, selected, a) for a in attributes)
            if not r.passed
        ]
        if breaches:
            detail = "; ".join(
                f"{r.attribute} reached {r.observed_ratio:.4f}" for r in breaches
            )
            hint = (
                f"At capacity {capacity:,} across {len(populations)} intersection "
                f"buckets each bucket is allotted about {float(quotas.min()):.1f} "
                "slots, and a whole-number allocation cannot subdivide finely enough "
                "to honour so tight a band. Raise the capacity, loosen "
                "fairness.max_disparity_ratio, or constrain fewer attributes jointly."
                if discretisation_limited
                else "Check that the protected attributes are not near-collinear with "
                "one another, which can leave some intersection buckets empty."
            )
            raise EquityGateFailure(
                f"cannot satisfy a disparity threshold of {ratio} for this "
                f"allocation: {detail}. {hint}"
            )

    return selected

def min_achievable_disparity_ratio(
    frame: pd.DataFrame,
    spec: UseCaseSpec,
    capacity: int,
    attributes: str | list[str] | None = None,
) -> float:
    """The tightest disparity ratio a whole-number allocation can reach here.

    Ask this before setting ``fairness.max_disparity_ratio``, because the limit is not
    always the algorithm: with many intersection buckets and little capacity, each
    bucket is allotted only a handful of slots and rounding alone can produce a ratio
    above a tight threshold. Constructive rather than theoretical, it measures the
    ratio produced by proportional allocation, which is an allocation that exists.
    """
    if attributes is None:
        attributes = list(spec.fairness.protected_attributes)
    elif isinstance(attributes, str):
        attributes = [attributes]

    cols = [_resolve(frame, a) for a in attributes]
    cell = frame[cols].astype(str).agg("|".join, axis=1)
    populations = cell.value_counts()
    quotas = populations * (capacity / len(frame))

    selected = pd.Series(False, index=frame.index)
    # Deterministic ordering so the answer does not depend on score, only on counts.
    order = pd.Series(range(len(frame)), index=frame.index).astype(float)
    for bucket in populations.index:
        rows = frame.index[cell == bucket]
        take = int(min(round(float(quotas[bucket])), len(rows)))
        if take > 0:
            selected.loc[order.loc[rows].nsmallest(take).index] = True

    ratios = [
        disparity_report(frame, spec, selected, a).observed_ratio for a in attributes
    ]
    finite = [r for r in ratios if np.isfinite(r)]
    return max(finite) if finite else float("nan")
    return selected

def write_equity_report(
    session,
    spec: UseCaseSpec,
    reports: list[DisparityReport],
    policy_label: str,
    table: str = "EQUITY_REPORT",
) -> str:
    """Persist the gate result. This is audit evidence, not a diagnostic."""
    rows = []
    for r in reports:
        for group, row in r.table.iterrows():
            rows.append(
                {
                    "POLICY": policy_label,
                    "ATTRIBUTE": r.attribute,
                    "GROUP_VALUE": str(group),
                    "POPULATION": int(row["population"]),
                    "SELECTED": int(row["selected"]),
                    "SELECTION_RATE": float(row["selection_rate"]),
                    "POPULATION_SHARE": float(row["population_share"]),
                    "REPRESENTATION_INDEX": float(row["representation_index"]),
                    "OBSERVED_RATIO": float(r.observed_ratio),
                    "THRESHOLD": float(r.max_disparity_ratio),
                    "PASSED": bool(r.passed),
                    "NOTES": " | ".join(r.notes),
                }
            )
    out = pd.DataFrame(rows)
    session.write_pandas(
        out,
        table,
        database=spec.database,
        schema="MODELS",
        auto_create_table=True,
        overwrite=True,
        quote_identifiers=False,
    )
    return spec.models(table)

def _resolve(frame: pd.DataFrame, column: str) -> str:
    available = {c.upper(): c for c in frame.columns}
    if column.upper() not in available:
        raise KeyError(
            f"protected attribute '{column}' is not in the analysis frame. "
            f"Available: {sorted(frame.columns)}. Protected attributes must exist on "
            "UNIT or UNIT_PERIOD even when they are excluded from the model covariates."
        )
    return available[column.upper()]
```

### `framework/causal_core/naive.py`

Copy code

```
"""Layer A: the estimates a team ships before anyone says the word "causal".

Two of them, because they fail in different and instructive ways.

``raw_difference`` is the comparison most program evaluations actually run:
outcome rate among the enrolled against everyone else. On confounded data it is
catastrophically wrong, often with the sign reversed, and it comes with a tight
confidence interval that makes it look authoritative.

``s_learner_simulation`` is the modern version: fit a model on all the
covariates plus a treatment flag, then flip the flag and re-score everyone.
People call this simulation. It does adjust for observed confounders, so it is a
real improvement, and on this data it moves the estimate substantially toward
the truth while still landing on the wrong side of zero.

Its more dangerous failure is on heterogeneity. An S-learner regularizes the
treatment indicator like any other feature, so the per-unit contrasts it
produces are dominated by whatever the outcome model happened to fit. The spread
of those contrasts is not the diagnostic people assume it is: it can come out
larger than the true spread and still carry no signal at all. What matters is
whether the per-unit estimates correlate with the real ones, which is why the
notebook checks that against planted truth rather than trusting the spread.

Both are honest implementations. The point is not that they are stupid, it is
that neither one tells you whether to believe it.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
)

from .data import COL_OUTCOME, COL_TREATMENT, design_matrix
from .results import EstimateResult, normal_ci
from .spec import Outcome, UseCaseSpec

def raw_difference(
    frame: pd.DataFrame,
    spec: UseCaseSpec,
    outcome: Outcome | None = None,
) -> EstimateResult:
    """Difference in mean outcome between treated and untreated. No adjustment.

    Included because it is the baseline every stakeholder has already seen, and
    because the gap between this and the truth is the entire motivation for
    everything that follows.
    """
    outcome = outcome or spec.outcome
    treated = frame.loc[frame[COL_TREATMENT] == 1, COL_OUTCOME]
    control = frame.loc[frame[COL_TREATMENT] == 0, COL_OUTCOME]

    estimate = float(treated.mean() - control.mean())

    if outcome.is_binary:
        p1, p0 = treated.mean(), control.mean()
        se = float(np.sqrt(p1 * (1 - p1) / len(treated) + p0 * (1 - p0) / len(control)))
    else:
        se = float(
            np.sqrt(
                treated.var(ddof=1) / len(treated) + control.var(ddof=1) / len(control)
            )
        )

    low, high = normal_ci(estimate, se)
    return EstimateResult(
        method="raw difference",
        outcome_column=outcome.column,
        estimate=estimate,
        se=se,
        ci_low=low,
        ci_high=high,
        baseline=float(control.mean()),
        n=len(frame),
        n_treated=int(frame[COL_TREATMENT].sum()),
        diagnostics={"target": "ate", "adjusts_for_confounding": 0},
        notes=[
            "No adjustment for who gets treated. If assignment depends on "
            "prognosis, this measures selection, not effect.",
            "The interval is narrow because it only reflects sampling noise. "
            "It carries no information about bias, which is the dominant error here.",
        ],
    )

def s_learner_simulation(
    frame: pd.DataFrame,
    spec: UseCaseSpec,
    outcome: Outcome | None = None,
    n_boot: int = 0,
    random_state: int = 7,
) -> EstimateResult:
    """Fit one model on covariates plus treatment, flip the flag, re-score.

    This is the "what if we enrolled everyone" simulation, done the way it is
    usually done. The per-unit differences are returned as a CATE estimate, but
    treat them with suspicion: their spread is not evidence that the model has
    found real heterogeneity. Grade them against truth, or against a holdout
    policy comparison, before using them to rank anyone.

    ``n_boot=0`` reports the standard error of the mean of the individual
    predicted differences, which is what a practitioner typically reports and
    which is badly understated because it ignores model uncertainty entirely.
    Set ``n_boot`` to something like 25 for an honest, slower bootstrap interval.
    """
    outcome = outcome or spec.outcome
    X = design_matrix(spec, frame)
    t = frame[COL_TREATMENT].to_numpy()
    y = frame[COL_OUTCOME].to_numpy()

    design = X.copy()
    design[COL_TREATMENT] = t

    def fit_and_contrast(
        d: pd.DataFrame, target: np.ndarray, rs: int
    ) -> tuple[np.ndarray, object]:
        model = _make_model(outcome, rs)
        model.fit(d, target)
        treated_all = d.copy()
        control_all = d.copy()
        treated_all[COL_TREATMENT] = 1
        control_all[COL_TREATMENT] = 0
        return _predict(model, treated_all) - _predict(model, control_all), model

    per_unit, _ = fit_and_contrast(design, y, random_state)
    estimate = float(per_unit.mean())

    if n_boot and n_boot > 1:
        rng = np.random.default_rng(random_state)
        draws = []
        for i in range(n_boot):
            idx = rng.integers(0, len(design), len(design))
            boot_effects, _ = fit_and_contrast(
                design.iloc[idx].reset_index(drop=True), y[idx], random_state + i + 1
            )
            draws.append(boot_effects.mean())
        se = float(np.std(draws, ddof=1))
        ci_note = f"bootstrap interval over {n_boot} refits"
    else:
        se = float(per_unit.std(ddof=1) / np.sqrt(len(per_unit)))
        ci_note = (
            "Interval is the standard error of the mean of the per-unit predicted "
            "differences. It ignores model uncertainty entirely and is therefore "
            "far too narrow. This is the interval most practitioners report."
        )

    low, high = normal_ci(estimate, se)
    cate = pd.Series(per_unit, index=frame.index, name="cate_s_learner")

    notes = [
        "Adjusts for observed covariates, so it is a real improvement on the raw "
        "difference. It cannot adjust for anything unobserved.",
        "The spread of the per-unit contrasts is not evidence of real heterogeneity. "
        "It can exceed the true spread while correlating with it at roughly zero, in "
        "which case ranking by it is no better than ranking at random.",
        ci_note,
        "No overlap diagnostic, no balance check, no refutation. Nothing here tells "
        "you whether the estimate should be believed.",
    ]

    return EstimateResult(
        method="S-learner flip-the-flag",
        outcome_column=outcome.column,
        estimate=estimate,
        se=se,
        ci_low=low,
        ci_high=high,
        baseline=float(frame.loc[frame[COL_TREATMENT] == 0, COL_OUTCOME].mean()),
        n=len(frame),
        n_treated=int(t.sum()),
        cate=cate,
        diagnostics={
            "target": "ate",
            "adjusts_for_confounding": 1,
            "cate_min": float(per_unit.min()),
            "cate_max": float(per_unit.max()),
            "cate_p10": float(np.percentile(per_unit, 10)),
            "cate_p90": float(np.percentile(per_unit, 90)),
        },
        notes=notes,
    )

def scenario_projection(
    result: EstimateResult,
    spec: UseCaseSpec,
    n_units: int,
    outcome: Outcome | None = None,
) -> dict[str, float]:
    """Project an estimate forward onto a proposed rollout.

    This is the part that genuinely is simulation: given a measured per-unit
    effect, what happens if the program is extended to ``n_units`` more units.
    Garbage in, garbage out, which is why the layer above it matters.
    """
    outcome = outcome or spec.outcome
    benefit_per_unit = result.benefit(outcome)
    events = benefit_per_unit * n_units
    cost = spec.treatment.cost_per_unit * n_units

    out = {
        "units_treated": float(n_units),
        "events_avoided": float(events),
        "program_cost": float(cost),
        "cost_per_unit": float(spec.treatment.cost_per_unit),
    }
    if outcome.value_per_event is not None:
        gross = events * outcome.value_per_event
        out.update(
            {
                "gross_value": float(gross),
                "net_value": float(gross - cost),
                "roi": float((gross - cost) / cost) if cost else float("nan"),
                "cost_per_event_avoided": float(cost / events)
                if events
                else float("inf"),
            }
        )
    if result.ci_low is not None:
        out["events_avoided_low"] = float(
            min(outcome.benefit(result.ci_low), outcome.benefit(result.ci_high))
            * n_units
        )
        out["events_avoided_high"] = float(
            max(outcome.benefit(result.ci_low), outcome.benefit(result.ci_high))
            * n_units
        )
    return out

# ---------------------------------------------------------------------------
# internals
# ---------------------------------------------------------------------------

def _make_model(outcome: Outcome, random_state: int):
    common = dict(
        max_iter=200, learning_rate=0.08, max_depth=6, random_state=random_state
    )
    if outcome.is_binary:
        return HistGradientBoostingClassifier(**common)
    return HistGradientBoostingRegressor(**common)

def _predict(model, X: pd.DataFrame) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return model.predict_proba(X)[:, 1]
    return model.predict(X)
```

### `framework/causal_core/refute.py`

Copy code

```
"""Client for the dowhy refutation procedure.

Thin on purpose. The work happens in ``AGENT.REFUTE_ESTIMATE``, which runs in an
isolated environment because dowhy requires numpy>=2 while econml requires numpy<2.
That conflict is not a packaging inconvenience to be worked around; it is why the
boundary exists, and why this module calls a procedure instead of importing dowhy.

Trying to ``import dowhy`` in the same process as econml will either fail or silently
break one of them. If you find yourself wanting to, read
``docs/runtime-and-packages.md`` first.

Usage::

    from causal_core import get_session, load_spec
    from causal_core.refute import refute, refutation_table

    spec = load_spec()
    session = get_session(spec)
    result = refute(session, spec)
    print(result["verdict"])
    refutation_table(session, spec)      # the persisted detail
"""

from __future__ import annotations

import json
from typing import Any

import pandas as pd

from .data import create_analysis_view
from .spec import UseCaseSpec

class RefutationUnavailable(RuntimeError):
    """The refutation procedure is not deployed, or could not run."""

def refute(
    session,
    spec: UseCaseSpec,
    sample_size: int = 20_000,
    num_simulations: int = 10,
    ensure_view: bool = True,
) -> dict[str, Any]:
    """Run refutation tests against the current estimate.

    ``ensure_view`` refreshes ``MODELS.V_ANALYSIS_FRAME`` first, since the procedure
    reads the frame through that view and a stale one would refute a different dataset
    than the notebooks estimated on.

    ``sample_size`` exists because each refuter re-estimates ``num_simulations`` times.
    Refutation asks whether a conclusion is fragile, which a sample answers as well as
    the full panel at a fraction of the cost.
    """
    if ensure_view:
        create_analysis_view(session, spec)

    try:
        raw = session.sql(
            f"CALL {spec.fqn('AGENT', 'REFUTE_ESTIMATE')}"
            f"({int(sample_size)}, {int(num_simulations)})"
        ).collect()[0][0]
    except Exception as exc:  # noqa: BLE001
        raise RefutationUnavailable(
            f"could not call {spec.fqn('AGENT', 'REFUTE_ESTIMATE')}: {exc}. "
            "Deploy it with: python framework/deploy_agent.py"
        ) from exc

    result = json.loads(raw) if isinstance(raw, str) else raw
    if not result.get("ok"):
        raise RefutationUnavailable(result.get("error", "refutation failed"))
    return result

def refutation_table(session, spec: UseCaseSpec) -> pd.DataFrame:
    """The persisted per-test detail, for a notebook or the console."""
    return session.sql(
        f"""
        SELECT TEST_NAME, STATUS, BASE_ESTIMATE, NEW_ESTIMATE, RELATIVE_SHIFT, NOTE
        FROM {spec.models("REFUTATION")}
        ORDER BY TEST_NAME
        """
    ).to_pandas()

def summarise(result: dict[str, Any]) -> str:
    """Format a result for printing, keeping the asymmetry in the reader's face.

    Refutation cannot certify an estimate. It can only fail to break it. Any summary
    that reads as a clean bill of health is misleading, so the verdict is always
    printed with the caveat attached rather than as a headline.
    """
    lines = [
        f"refutation on {result['sample_size']:,} units, "
        f"{result['num_simulations']} simulations per test",
        f"  estimate under test : {result['base_estimate']:+.5f} "
        f"({result['estimator']})",
    ]
    if result.get("primary_estimate_from_diagnostics") is not None:
        lines.append(
            f"  primary estimate    : {result['primary_estimate_from_diagnostics']:+.5f} "
            "(doubly robust, from MODELS.DIAGNOSTICS)"
        )
    lines.append("")

    for test in result["results"]:
        marker = "pass" if test["status"] == "pass" else test["status"]
        lines.append(f"  [{marker:>5}] {test['test']}")
        lines.append(f"          {test['description']}")
        if test.get("note"):
            lines.append(f"          {test['note']}")

    lines += ["", f"  {result['verdict']}", "", f"  {result['how_to_read']}"]
    return "\n".join(lines)
```

### `framework/causal_core/results.py`

Copy code

```
"""Shared result types, plus the synthetic-only estimator leaderboard.

:class:`EstimateResult` is product: every estimator returns one.
:class:`Leaderboard` is synthetic scaffolding: it needs planted ground truth.

Every estimator in this framework returns an :class:`EstimateResult`, so the
notebooks, the agent tools, and the Streamlit app all consume one shape. When a
use case has planted ground truth, :class:`Leaderboard` grades each estimator
against it, which is what turns "trust me, causal inference is better" into a
table of numbers.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

import pandas as pd

from .spec import Outcome, UseCaseSpec

@dataclass
class EstimateResult:
    """One estimate of a treatment effect, with everything needed to judge it.

    ``estimate`` is always on the outcome's own scale and keeps its natural
    sign, so a readmission reduction is negative. Use :attr:`benefit` when a
    positive-is-good number is wanted, and let the spec decide which is which
    rather than hardcoding it.
    """

    method: str
    outcome_column: str
    estimate: float
    n: int
    n_treated: int
    se: float | None = None
    ci_low: float | None = None
    ci_high: float | None = None
    baseline: float | None = None
    identified: bool = True
    diagnostics: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    cate: pd.Series | None = None

    # -- derived views ------------------------------------------------------

    def benefit(self, outcome: Outcome) -> float:
        """Effect re-expressed so that larger is always better."""
        return outcome.benefit(self.estimate)

    def relative(self) -> float | None:
        """Effect as a fraction of the untreated baseline."""
        if self.baseline in (None, 0):
            return None
        return self.estimate / self.baseline

    @property
    def significant(self) -> bool:
        """Whether the interval excludes zero. Absent an interval, unknown."""
        if self.ci_low is None or self.ci_high is None:
            return False
        return (self.ci_low > 0) or (self.ci_high < 0)

    @property
    def cate_spread(self) -> float | None:
        """Standard deviation of the per-unit effects.

        This is the number that decides whether an estimator is usable for
        targeting. An estimator can recover the average effect correctly and
        still be worthless for deciding who to treat, if it has flattened all
        the heterogeneity away.
        """
        if self.cate is None or len(self.cate) == 0:
            return None
        return float(self.cate.std())

    def direction_verdict(self, outcome: Outcome) -> str:
        """Plain-language read of what this estimate claims."""
        if not self.identified:
            return "no honest estimate available"
        if not self.significant:
            return "no effect distinguishable from noise"
        return "program helps" if self.benefit(outcome) > 0 else "program harms"

    def summary(self, outcome: Outcome) -> dict[str, Any]:
        rel = self.relative()
        return {
            "method": self.method,
            "estimate": round(self.estimate, 5),
            "ci": None
            if self.ci_low is None
            else [round(self.ci_low, 5), round(self.ci_high, 5)],
            "relative": None if rel is None else round(rel, 4),
            "verdict": self.direction_verdict(outcome),
            "cate_spread": None
            if self.cate_spread is None
            else round(self.cate_spread, 5),
            "n": self.n,
            "n_treated": self.n_treated,
            "identified": self.identified,
            "notes": list(self.notes),
        }

def normal_ci(
    estimate: float, se: float | None, z: float = 1.96
) -> tuple[float | None, float | None]:
    if se is None or not math.isfinite(se) or se <= 0:
        return None, None
    return estimate - z * se, estimate + z * se

@dataclass
class Leaderboard:
    """SYNTHETIC SCAFFOLDING. Grades estimators against planted truth.

    Requires a use case with a TRUTH schema, which only synthetic ones have. On
    real data there is no answer key, which is the entire reason the synthetic use
    cases exist: they are the only place you can check whether a method works.

    Safe to ignore, and safe to delete, when adopting this for real data. Nothing
    in the estimation path depends on it. See docs/design.md for the full list of
    what is scaffolding and what is product.
    """

    spec: UseCaseSpec
    true_ate: float | None = None
    true_att: float | None = None
    results: list[EstimateResult] = field(default_factory=list)

    def add(self, result: EstimateResult) -> EstimateResult:
        self.results.append(result)
        return result

    def _target(self, result: EstimateResult) -> float | None:
        """Which planted quantity a given estimator is actually aiming at.

        Diff-in-diff and anything estimated on the treated population targets the
        effect among the treated, not the population average. Grading a DiD
        estimate against the population ATE would penalize it for being correct.
        """
        if result.diagnostics.get("target") == "att":
            return self.true_att if self.true_att is not None else self.true_ate
        return self.true_ate

    def to_frame(self) -> pd.DataFrame:
        outcome = self.spec.outcome
        rows = []
        for r in self.results:
            target = self._target(r)
            abs_err = None if target is None else r.estimate - target
            rel_err = (
                None if target in (None, 0) else abs(r.estimate - target) / abs(target)
            )
            covers = (
                None
                if target is None or r.ci_low is None
                else bool(r.ci_low <= target <= r.ci_high)
            )
            rows.append(
                {
                    "method": r.method,
                    "targets": r.diagnostics.get("target", "ate"),
                    "estimate": r.estimate,
                    "ci_low": r.ci_low,
                    "ci_high": r.ci_high,
                    "truth": target,
                    "error": abs_err,
                    "rel_error": rel_err,
                    "ci_covers_truth": covers,
                    "cate_spread": r.cate_spread,
                    "verdict": r.direction_verdict(outcome),
                    "identified": r.identified,
                }
            )
        frame = pd.DataFrame(rows)
        if not frame.empty and frame["rel_error"].notna().any():
            frame = frame.sort_values("rel_error", na_position="last").reset_index(
                drop=True
            )
        return frame

    def metrics_for_logging(self) -> dict[str, float]:
        """Flat numeric metrics, safe for Snowflake ML Experiments.

        ``log_metrics`` rejects booleans, and ``isinstance(True, int)`` is True in
        Python, so a naive numeric filter leaks them. Booleans are cast to int
        deliberately here.
        """
        out: dict[str, float] = {}
        for r in self.results:
            key = r.method.lower().replace(" ", "_").replace("-", "_")
            out[f"{key}__estimate"] = float(r.estimate)
            target = self._target(r)
            if target not in (None, 0):
                out[f"{key}__rel_error"] = float(abs(r.estimate - target) / abs(target))
            if r.cate_spread is not None:
                out[f"{key}__cate_spread"] = float(r.cate_spread)
            out[f"{key}__identified"] = int(r.identified)
        return out
```

### `framework/causal_core/session.py`

Copy code

```
"""Dual-mode Snowpark session.

The same notebook has to run in two places: a Snowflake Workspace notebook,
where a session already exists, and local Jupyter, where it does not. Calling
``get_active_session()`` unconditionally fails locally with
``SnowparkSessionException (1403): No default Session is found``, so this module
tries that first and falls back to a local connection from connections.toml.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .spec import UseCaseSpec, load_config

if TYPE_CHECKING:  # pragma: no cover
    from snowflake.snowpark import Session

def resolve_connection_name(config_path: Path | str | None = None) -> str | None:
    """Connection name, in precedence order.

    1. ``SNOWFLAKE_CONNECTION_NAME``
    2. ``SNOWFLAKE_DEFAULT_CONNECTION_NAME``
    3. ``snowflake.connection_name`` in config.yaml, if you set one
    4. ``None``, meaning the default connection in connections.toml, which is the
       same one ``snow`` uses when you pass no ``-c``.
    """
    for var in ("SNOWFLAKE_CONNECTION_NAME", "SNOWFLAKE_DEFAULT_CONNECTION_NAME"):
        if os.getenv(var):
            return os.environ[var]
    try:
        config = load_config(config_path)
    except Exception:
        return None
    return (config.get("snowflake") or {}).get("connection_name") or None

def get_session(
    spec: UseCaseSpec | None = None,
    config_path: Path | str | None = None,
    apply_context: bool = True,
) -> "Session":
    """Return a Snowpark session that works both inside and outside Snowflake.

    When ``spec`` is supplied and ``apply_context`` is true, the session is
    pointed at that use case's warehouse and database. Context is applied
    best-effort: a missing database is not fatal here because 01_contract.sql may not
    have run yet, and a clear error from the first real query is more useful
    than a failure during session construction.
    """
    from snowflake.snowpark import Session

    session: Session | None = None
    try:
        from snowflake.snowpark.context import get_active_session

        session = get_active_session()
    except Exception:
        session = None

    if session is None:
        connection_name = resolve_connection_name(config_path)
        builder = Session.builder
        if connection_name:
            builder = builder.config("connection_name", connection_name)
        session = builder.getOrCreate()

    if spec is not None and apply_context:
        _apply_context(session, spec)

    return session

def _apply_context(session: "Session", spec: UseCaseSpec) -> None:
    for statement in (
        f"USE WAREHOUSE {spec.warehouse}",
        f"USE DATABASE {spec.database}",
    ):
        try:
            session.sql(statement).collect()
        except Exception:
            # Deliberately swallowed. Setup may not have run, and the first
            # real query will produce a far more actionable message.
            pass

def describe_session(session: "Session") -> dict[str, Any]:
    """Current context, useful as the first output cell of a notebook."""
    row = session.sql(
        "SELECT CURRENT_ACCOUNT() AS ACCOUNT, CURRENT_USER() AS USER, "
        "CURRENT_ROLE() AS ROLE, CURRENT_WAREHOUSE() AS WAREHOUSE, "
        "CURRENT_DATABASE() AS DATABASE, CURRENT_SCHEMA() AS SCHEMA, "
        "CURRENT_VERSION() AS VERSION"
    ).collect()[0]
    return row.as_dict()
```

### `framework/causal_core/spec.py`

Copy code

```
"""Use case specification: the contract every other module depends on.

Domain knowledge enters the framework here and nowhere else. A use case is
defined by a ``usecase.yaml`` file plus a SQL generator that produces the five
canonical tables. No module outside this one should ever contain a
domain-specific column name, label, or dollar figure.

The five canonical tables are fixed by name so framework code never has to
guess:

    UNIT          one row per decision subject, time-invariant attributes
    UNIT_PERIOD   panel, one row per unit per period
    TREATMENT     who was treated and when
    OUTCOME       outcome per unit, plus the pre-period value for diff-in-diff
    CAPACITY      the binding constraint, by group and period

Schema names are fixed too: DATA, TRUTH, MODELS, AGENT, APP. Only the database
name varies by use case, which guarantees two use cases can never collide.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

import yaml

# usecases/ and config.yaml live two levels up from framework/causal_core/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

Direction = Literal["minimize", "maximize"]
OutcomeType = Literal["binary", "continuous"]

# Canonical table names. Framework code refers to these, never to domain names.
UNIT = "UNIT"
UNIT_PERIOD = "UNIT_PERIOD"
TREATMENT = "TREATMENT"
OUTCOME = "OUTCOME"
CAPACITY = "CAPACITY"
CANONICAL_TABLES = (UNIT, UNIT_PERIOD, TREATMENT, OUTCOME, CAPACITY)

# Fixed schema names within a use case database.
DATA_SCHEMA = "DATA"
TRUTH_SCHEMA = "TRUTH"
MODELS_SCHEMA = "MODELS"
AGENT_SCHEMA = "AGENT"
APP_SCHEMA = "APP"
SCHEMAS = (DATA_SCHEMA, TRUTH_SCHEMA, MODELS_SCHEMA, AGENT_SCHEMA, APP_SCHEMA)

class SpecError(ValueError):
    """Raised when a use case spec is missing or internally inconsistent."""

def _require(mapping: dict[str, Any], key: str, context: str) -> Any:
    if key not in mapping:
        raise SpecError(f"{context}: missing required key '{key}'")
    return mapping[key]

@dataclass(frozen=True)
class Unit:
    """The thing a decision is made about: a member, customer, store, device."""

    id_column: str
    label_singular: str
    label_plural: str

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Unit:
        return cls(
            id_column=_require(d, "id_column", "unit"),
            label_singular=d.get("label_singular", "unit"),
            label_plural=d.get("label_plural", "units"),
        )

@dataclass(frozen=True)
class Treatment:
    """The intervention whose causal effect is being measured."""

    column: str
    label: str
    cost_per_unit: float

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Treatment:
        cost = float(_require(d, "cost_per_unit", "treatment"))
        if cost <= 0:
            raise SpecError("treatment.cost_per_unit must be positive")
        return cls(
            column=_require(d, "column", "treatment"),
            label=d.get("label", "treatment"),
            cost_per_unit=cost,
        )

@dataclass(frozen=True)
class Outcome:
    """An outcome, plus enough economics to turn an effect into dollars.

    ``direction`` is what keeps the rest of the framework domain-blind. For a
    readmission you want the effect to be negative; for revenue you want it
    positive. Downstream code multiplies by :attr:`sign` instead of hardcoding
    which way is good news.
    """

    column: str
    type: OutcomeType
    direction: Direction
    label: str
    value_per_event: float | None = None
    pre_column: str | None = None
    panel_column: str | None = None

    @property
    def periodic_column(self) -> str:
        """Column holding this outcome per period, for diff-in-diff.

        Defaults to :attr:`column`. Override via ``panel_column`` when the
        unit-level outcome is an aggregate of a per-period measure, for example an
        annual rate built from monthly indicators. Diff-in-diff needs the
        per-period version; everything else uses the unit-level one.
        """
        return self.panel_column or self.column

    @property
    def sign(self) -> int:
        """+1 when larger is better, -1 when smaller is better."""
        return -1 if self.direction == "minimize" else 1

    @property
    def is_binary(self) -> bool:
        return self.type == "binary"

    def benefit(self, effect: float) -> float:
        """Convert a signed causal effect into a positive-is-good quantity.

        An effect of -0.04 on a minimize outcome becomes a benefit of +0.04.
        """
        return effect * self.sign

    def value_of(self, effect: float) -> float:
        """Dollar value of an effect for one unit.

        Raises if the spec did not attach a monetary value to this outcome,
        because silently returning zero would make an allocation look free.
        """
        if self.value_per_event is None:
            raise SpecError(
                f"outcome '{self.column}' has no value_per_event, so it cannot "
                "be used for dollar-denominated allocation. Set it in the spec "
                "or allocate on the primary outcome instead."
            )
        return self.benefit(effect) * self.value_per_event

    @classmethod
    def from_dict(cls, d: dict[str, Any], context: str) -> Outcome:
        otype = _require(d, "type", context)
        if otype not in ("binary", "continuous"):
            raise SpecError(
                f"{context}.type must be 'binary' or 'continuous', got '{otype}'"
            )
        direction = _require(d, "direction", context)
        if direction not in ("minimize", "maximize"):
            raise SpecError(
                f"{context}.direction must be 'minimize' or 'maximize', got '{direction}'"
            )
        vpe = d.get("value_per_event")
        return cls(
            column=_require(d, "column", context),
            type=otype,
            direction=direction,
            label=d.get("label", d["column"]),
            value_per_event=None if vpe is None else float(vpe),
            pre_column=d.get("pre_column"),
            panel_column=d.get("panel_column"),
        )

@dataclass(frozen=True)
class Covariates:
    """Pre-treatment features used for confounding adjustment.

    Everything listed here must be measured *before* treatment. A post-treatment
    covariate is the most common way to silently destroy a causal estimate, so
    the generator and :mod:`causal_core.data` both guard against it.
    """

    observed: list[str] = field(default_factory=list)
    categorical: list[str] = field(default_factory=list)

    @property
    def numeric(self) -> list[str]:
        return [c for c in self.observed if c not in self.categorical]

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Covariates:
        observed = list(_require(d, "observed", "covariates"))
        if not observed:
            raise SpecError("covariates.observed cannot be empty")
        categorical = list(d.get("categorical", []))
        unknown = set(categorical) - set(observed)
        if unknown:
            raise SpecError(
                f"covariates.categorical lists columns absent from observed: {sorted(unknown)}"
            )
        return cls(observed=observed, categorical=categorical)

@dataclass(frozen=True)
class Fairness:
    """Protected attributes and the disparity threshold that fails the build."""

    protected_attributes: list[str] = field(default_factory=list)
    max_disparity_ratio: float = 1.25

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Fairness:
        attrs = list(d.get("protected_attributes", []))
        if not attrs:
            raise SpecError(
                "fairness.protected_attributes cannot be empty. Uplift targeting "
                "can deprioritize groups with less social support, so this check "
                "is mandatory rather than optional."
            )
        ratio = float(d.get("max_disparity_ratio", 1.25))
        if ratio < 1.0:
            raise SpecError("fairness.max_disparity_ratio must be >= 1.0")
        return cls(protected_attributes=attrs, max_disparity_ratio=ratio)

@dataclass(frozen=True)
class Panel:
    """Panel shape, which is what makes diff-in-diff available."""

    period_column: str
    period_grain: str
    pre_periods: int
    post_periods: int

    @property
    def total_periods(self) -> int:
        return self.pre_periods + self.post_periods

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Panel:
        pre = int(_require(d, "pre_periods", "panel"))
        post = int(_require(d, "post_periods", "panel"))
        if pre < 2:
            raise SpecError(
                "panel.pre_periods must be at least 2 for a pre-trend check to mean anything"
            )
        if post < 1:
            raise SpecError("panel.post_periods must be at least 1")
        return cls(
            period_column=_require(d, "period_column", "panel"),
            period_grain=d.get("period_grain", "month"),
            pre_periods=pre,
            post_periods=post,
        )

@dataclass(frozen=True)
class Capacity:
    """The binding constraint that turns ranking into an allocation problem."""

    group_column: str
    slots_column: str

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Capacity:
        return cls(
            group_column=_require(d, "group_column", "capacity"),
            slots_column=_require(d, "slots_column", "capacity"),
        )

@dataclass(frozen=True)
class Calibration:
    """SYNTHETIC SCAFFOLDING. Targets the synthetic generator must hit.

    Asserted by 02_generate_synthetic.sql. Omit this block entirely for a use case
    pointed at real data; there is nothing to calibrate against.

    These exist so the synthetic data proves something. If the naive estimator is not
    clearly wrong, the generator needs retuning rather than the estimator.
    """

    true_ate_relative: float
    naive_bias_direction: str
    overlap_breaks_above_percentile: float

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Calibration:
        direction = d.get("naive_bias_direction", "positive")
        if direction not in ("positive", "negative"):
            raise SpecError(
                "calibration.naive_bias_direction must be 'positive' or 'negative'"
            )
        return cls(
            true_ate_relative=float(_require(d, "true_ate_relative", "calibration")),
            naive_bias_direction=direction,
            overlap_breaks_above_percentile=float(
                d.get("overlap_breaks_above_percentile", 98)
            ),
        )

@dataclass(frozen=True)
class UseCaseSpec:
    """A fully validated use case. Treat as immutable."""

    name: str
    label: str
    database: str
    warehouse: str
    unit: Unit
    treatment: Treatment
    outcome: Outcome
    covariates: Covariates
    fairness: Fairness
    panel: Panel
    capacity: Capacity
    calibration: Calibration
    secondary_outcome: Outcome | None = None
    source_path: Path | None = None

    # -- fully qualified name helpers ---------------------------------------

    def fqn(self, schema: str, table: str) -> str:
        return f"{self.database}.{schema}.{table}"

    def data(self, table: str) -> str:
        if table not in CANONICAL_TABLES:
            raise SpecError(
                f"'{table}' is not a canonical table. Expected one of {CANONICAL_TABLES}. "
                "Framework code must not reference domain-specific table names."
            )
        return self.fqn(DATA_SCHEMA, table)

    def truth(self, table: str) -> str:
        return self.fqn(TRUTH_SCHEMA, table)

    def models(self, table: str) -> str:
        return self.fqn(MODELS_SCHEMA, table)

    def agent(self, obj: str) -> str:
        return self.fqn(AGENT_SCHEMA, obj)

    def app(self, obj: str) -> str:
        return self.fqn(APP_SCHEMA, obj)

    # -- convenience --------------------------------------------------------

    def outcome_by_name(self, name: str | None = None) -> Outcome:
        """Resolve an outcome by column name, defaulting to the primary."""
        if name is None:
            return self.outcome
        for candidate in (self.outcome, self.secondary_outcome):
            if candidate is not None and candidate.column.upper() == name.upper():
                return candidate
        available = [self.outcome.column] + (
            [self.secondary_outcome.column] if self.secondary_outcome else []
        )
        raise SpecError(f"unknown outcome '{name}'. Available: {available}")

    @property
    def all_outcomes(self) -> list[Outcome]:
        return [o for o in (self.outcome, self.secondary_outcome) if o is not None]

    # -- construction -------------------------------------------------------

    @classmethod
    def from_dict(
        cls, d: dict[str, Any], source_path: Path | None = None
    ) -> UseCaseSpec:
        outcomes = _require(d, "outcome", "spec")
        primary = Outcome.from_dict(
            _require(outcomes, "primary", "outcome"), "outcome.primary"
        )
        secondary = (
            Outcome.from_dict(outcomes["secondary"], "outcome.secondary")
            if outcomes.get("secondary")
            else None
        )

        spec = cls(
            name=_require(d, "name", "spec"),
            label=d.get("label", d["name"]),
            database=_require(d, "database", "spec"),
            warehouse=d.get("warehouse", "COOKBOOK_AGENT_CAUSAL_GROUNDING_WH"),
            unit=Unit.from_dict(_require(d, "unit", "spec")),
            treatment=Treatment.from_dict(_require(d, "treatment", "spec")),
            outcome=primary,
            secondary_outcome=secondary,
            covariates=Covariates.from_dict(_require(d, "covariates", "spec")),
            fairness=Fairness.from_dict(_require(d, "fairness", "spec")),
            panel=Panel.from_dict(_require(d, "panel", "spec")),
            capacity=Capacity.from_dict(_require(d, "capacity", "spec")),
            calibration=Calibration.from_dict(_require(d, "calibration", "spec")),
            source_path=source_path,
        )
        spec._validate_cross_references()
        return spec

    def _validate_cross_references(self) -> None:
        """Catch spec-internal contradictions that would fail much later."""
        observed = {c.upper() for c in self.covariates.observed}

        # A protected attribute must be available to the fairness check. It may
        # legitimately be excluded from the model covariates (fairness through
        # unawareness), so only warn-by-error if it is nowhere at all is not
        # possible here; data.py verifies presence against the real tables.
        for outcome in self.all_outcomes:
            if outcome.column.upper() in observed:
                raise SpecError(
                    f"outcome column '{outcome.column}' also appears in "
                    "covariates.observed. Conditioning on the outcome guarantees a "
                    "meaningless estimate."
                )

        if self.treatment.column.upper() in observed:
            raise SpecError(
                f"treatment column '{self.treatment.column}' also appears in "
                "covariates.observed. The treatment cannot adjust for itself."
            )

        if self.panel.period_column.upper() in observed:
            raise SpecError(
                f"panel.period_column '{self.panel.period_column}' also appears in "
                "covariates.observed. Time is handled by the panel, not as a covariate."
            )

# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_config(config_path: Path | str | None = None) -> dict[str, Any]:
    """Read the repo-level config.yaml."""
    path = Path(config_path) if config_path else PROJECT_ROOT / "config.yaml"
    if not path.exists():
        raise SpecError(f"config not found at {path}")
    with path.open() as fh:
        return yaml.safe_load(fh) or {}

def available_usecases() -> list[str]:
    """Every use case directory holding a usecase.yaml, excluding the template."""
    root = PROJECT_ROOT / "usecases"
    if not root.exists():
        return []
    return sorted(
        p.name
        for p in root.iterdir()
        if p.is_dir() and not p.name.startswith("_") and (p / "usecase.yaml").exists()
    )

def load_spec(
    usecase: str | None = None,
    config_path: Path | str | None = None,
) -> UseCaseSpec:
    """Load and validate a use case spec.

    With no arguments, reads ``active_usecase`` from config.yaml. That is the
    normal path: notebooks call ``load_spec()`` and stay domain-blind.
    """
    if usecase is None:
        config = load_config(config_path)
        usecase = config.get("active_usecase")
        if not usecase:
            raise SpecError("config.yaml does not set active_usecase")

    path = PROJECT_ROOT / "usecases" / usecase / "usecase.yaml"
    if not path.exists():
        raise SpecError(
            f"no spec at {path}. Available use cases: {available_usecases()}"
        )

    with path.open() as fh:
        raw = yaml.safe_load(fh) or {}

    spec = UseCaseSpec.from_dict(raw, source_path=path)
    if spec.name != usecase:
        raise SpecError(
            f"spec name '{spec.name}' does not match directory '{usecase}'. "
            "Keep them identical so rendered SQL and tables stay traceable."
        )
    return spec

def load_copy(
    usecase: str | None = None, config_path: Path | str | None = None
) -> dict[str, Any]:
    """Load optional narrative strings for the UI and agent.

    Missing copy.yaml is not an error. The app falls back to spec labels.
    """
    if usecase is None:
        usecase = load_config(config_path).get("active_usecase")
    path = PROJECT_ROOT / "usecases" / str(usecase) / "copy.yaml"
    if not path.exists():
        return {}
    with path.open() as fh:
        return yaml.safe_load(fh) or {}

def write_spec_snapshot(
    session, spec: UseCaseSpec, table: str = "SPEC_SNAPSHOT"
) -> str:
    """Persist the spec into Snowflake so downstream surfaces can read it.

    The Streamlit console runs inside Snowflake and cannot open ``usecase.yaml``, so
    without this it would need its own hardcoded copy of every label, cost, and
    protected attribute. That copy would drift from the YAML the notebooks use, and
    the drift would be silent.

    Also serves as the provenance record: one row per deployment, with the spec that
    was in force. When someone asks six months from now what "net value" meant in a
    screenshot, this is the answer.
    """
    import json as _json
    from dataclasses import asdict as _asdict
    from datetime import datetime, timezone

    import pandas as _pd

    payload = _asdict(spec)
    row = {
        "USECASE": spec.name,
        "LABEL": spec.label,
        "DATABASE_NAME": spec.database,
        "WAREHOUSE": spec.warehouse,
        "UNIT_ID_COLUMN": spec.unit.id_column,
        "UNIT_LABEL_SINGULAR": spec.unit.label_singular,
        "UNIT_LABEL_PLURAL": spec.unit.label_plural,
        "TREATMENT_COLUMN": spec.treatment.column,
        "TREATMENT_LABEL": spec.treatment.label,
        "COST_PER_UNIT": float(spec.treatment.cost_per_unit),
        "OUTCOME_COLUMN": spec.outcome.column,
        "OUTCOME_LABEL": spec.outcome.label,
        "OUTCOME_DIRECTION": spec.outcome.direction,
        "VALUE_PER_EVENT": (
            float(spec.outcome.value_per_event)
            if spec.outcome.value_per_event is not None
            else None
        ),
        "PROTECTED_ATTRIBUTES": ",".join(spec.fairness.protected_attributes),
        "MAX_DISPARITY_RATIO": float(spec.fairness.max_disparity_ratio),
        "CAPACITY_GROUP_COLUMN": spec.capacity.group_column,
        "CAPACITY_SLOTS_COLUMN": spec.capacity.slots_column,
        "TOTAL_PERIODS": int(spec.panel.total_periods),
        "POST_PERIODS": int(spec.panel.post_periods),
        "SPEC_JSON": _json.dumps(payload, default=str),
        "SNAPSHOT_AT": datetime.now(timezone.utc).replace(tzinfo=None),
    }

    session.write_pandas(
        _pd.DataFrame([row]),
        table,
        database=spec.database,
        schema=MODELS_SCHEMA,
        auto_create_table=True,
        overwrite=True,
        quote_identifiers=False,
    )
    return spec.models(table)
```

### `framework/check_notebooks.py`

Copy code

```
"""Compile-check every code cell in the generated notebooks.

Run after framework/render_notebooks.py. Catches escaping mistakes in the
generator before a notebook is executed, which is much faster than finding them
through a kernel traceback.

    python framework/check_notebooks.py
"""

from pathlib import Path

import nbformat

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def main() -> int:
    failures = 0
    for path in sorted((PROJECT_ROOT / "notebooks").glob("*.ipynb")):
        nb = nbformat.read(path, as_version=4)
        for i, cell in enumerate(nb.cells):
            if cell.cell_type != "code":
                continue
            src = "".join(cell.source)
            try:
                compile(src, f"{path.name}:cell{i}", "exec")
            except SyntaxError as exc:
                failures += 1
                print(f"FAIL {path.name} cell {i}: {exc.msg} (line {exc.lineno})")
                lines = src.splitlines()
                lo = max(0, (exc.lineno or 1) - 3)
                for n, line in enumerate(
                    lines[lo : (exc.lineno or 1) + 1], start=lo + 1
                ):
                    print(f"      {n}: {line!r}")
        # Also surface any errors captured from a previous execution, so a single
        # command covers both "does it parse" and "did it run".
        exec_errors = [
            out
            for cell in nb.cells
            for out in cell.get("outputs", [])
            if out.get("output_type") == "error"
        ]
        for err in exec_errors:
            failures += 1
            print(
                f"EXEC {path.name}: {err.get('ename')}: {str(err.get('evalue'))[:200]}"
            )
            for line in (err.get("traceback") or [])[-4:]:
                print(f"      {line[:160]}")

        if not failures:
            print(f"ok   {path.name}")
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
```

### `framework/deploy_agent.py`

Copy code

```
"""Deploy the agent tool procedures for the active use case.

    python framework/deploy_agent.py            # active use case from config.yaml
    python framework/deploy_agent.py --usecase subscription_churn

The tool SQL lives in ``agent/*.sql`` as a single source with ``@DATABASE@`` and
``@UNIT_ID@`` placeholders. Substituting at deploy time rather than parameterising
at runtime is deliberate: a stored procedure invoked by a Cortex Agent cannot rely
on the caller's session having the right database set, and threading a database
argument through every tool would put a parameter in front of the model that it has
no business guessing.

Statements are split on the ``$$``-aware boundary because procedure bodies contain
semicolons, so a naive split on ``;`` corrupts them.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "framework"))

from causal_core import (  # noqa: E402
    create_analysis_view,
    get_session,
    load_spec,
    write_spec_snapshot,
)

def split_statements(sql: str) -> list[str]:
    """Split a script into statements without breaking $$-quoted bodies."""
    statements, buffer, in_body = [], [], False
    for line in sql.splitlines():
        if line.strip() == "$$" or line.strip().startswith("$$;"):
            in_body = not in_body if line.strip() == "$$" else False
            buffer.append(line)
            if not in_body:
                statements.append("\n".join(buffer))
                buffer = []
            continue
        if not in_body and line.rstrip().endswith("$$"):
            in_body = True
            buffer.append(line)
            continue
        buffer.append(line)
        if not in_body and line.rstrip().endswith(";"):
            statements.append("\n".join(buffer))
            buffer = []
    if buffer:
        statements.append("\n".join(buffer))
    return [s for s in (st.strip() for st in statements) if s and not _only_comments(s)]

def _only_comments(statement: str) -> bool:
    body = re.sub(r"--[^\n]*", "", statement).strip()
    return not body

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--usecase", default=None)
    parser.add_argument("--file", default=None, help="deploy one file instead of all")
    args = parser.parse_args()

    spec = load_spec(args.usecase)
    session = get_session(spec)

    substitutions = {
        "@DATABASE@": spec.database,
        "@UNIT_ID@": spec.unit.id_column,
        "@UNIT_LABEL@": spec.unit.label_plural,
        "@WAREHOUSE@": spec.warehouse,
    }

    files = (
        [PROJECT_ROOT / "agent" / args.file]
        if args.file
        else sorted((PROJECT_ROOT / "agent").glob("*.sql"))
    )

    print(f"deploying agent tools for {spec.label} -> {spec.database}.AGENT")

    # REFUTE_ESTIMATE runs in an environment that cannot import causal_core, so it
    # learns column names from MODELS.SPEC_SNAPSHOT and reads MODELS.V_ANALYSIS_FRAME.
    # Publish both here so the agent's refute tool works straight after a deploy.
    print(f"  spec snapshot   {write_spec_snapshot(session, spec)}")
    print(f"  analysis view   {create_analysis_view(session, spec)}")
    for path in files:
        sql = path.read_text()
        for placeholder, value in substitutions.items():
            sql = sql.replace(placeholder, value)

        leftover = re.findall(r"@[A-Z_]+@", sql)
        if leftover:
            print(f"  ERROR {path.name}: unsubstituted placeholders {set(leftover)}")
            return 1

        for statement in split_statements(sql):
            first = statement.splitlines()[0][:70]
            try:
                session.sql(statement).collect()
            except Exception as exc:  # noqa: BLE001
                print(f"  FAIL {path.name}: {first}\n        {exc}")
                return 1
        print(f"  ok   {path.name}")

    # INFORMATION_SCHEMA rather than SHOW PROCEDURES: SHOW includes every built-in
    # the role can see, which buries the six procedures we just created.
    procs = session.sql(
        f"""
        SELECT PROCEDURE_NAME, ARGUMENT_SIGNATURE
        FROM {spec.database}.INFORMATION_SCHEMA.PROCEDURES
        WHERE PROCEDURE_SCHEMA = 'AGENT'
        ORDER BY PROCEDURE_NAME
        """
    ).collect()
    print(f"\n{len(procs)} procedures in {spec.database}.AGENT:")
    for row in procs:
        print(f"  {row['PROCEDURE_NAME']}{row['ARGUMENT_SIGNATURE']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

### `framework/deploy_app.py`

Copy code

```
"""Deploy the Streamlit console for the active use case.

    python framework/deploy_app.py
    python framework/deploy_app.py --usecase subscription_churn

Three steps: persist the spec snapshot the app reads, upload the app file to a stage
in the APP schema, and create the STREAMLIT object pointing at it.

Uses PUT plus CREATE STREAMLIT rather than `snow streamlit deploy` so the whole
deployment is driven from the spec, with no per-use-case project file to keep in sync.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "framework"))

from causal_core import get_session, load_spec, write_spec_snapshot  # noqa: E402

STAGE = "APP_FILES"
APP_FILE = PROJECT_ROOT / "app" / "causal_console.py"
ENV_FILE = PROJECT_ROOT / "app" / "environment.yml"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--usecase", default=None)
    args = parser.parse_args()

    spec = load_spec(args.usecase)
    session = get_session(spec)

    print(f"deploying console for {spec.label} -> {spec.database}.APP")

    print(f"  spec snapshot   {write_spec_snapshot(session, spec)}")

    session.sql(
        f"CREATE STAGE IF NOT EXISTS {spec.database}.APP.{STAGE} "
        "DIRECTORY = (ENABLE = TRUE)"
    ).collect()

    for path in (APP_FILE, ENV_FILE):
        if not path.exists():
            continue
        # AUTO_COMPRESS=FALSE: Streamlit needs to read the .py directly, not a .gz.
        session.file.put(
            str(path),
            f"@{spec.database}.APP.{STAGE}",
            auto_compress=False,
            overwrite=True,
        )
        print(f"  uploaded        {path.name}")

    session.sql(
        f"""
        CREATE OR REPLACE STREAMLIT {spec.database}.APP.CAUSAL_CONSOLE
          ROOT_LOCATION = '@{spec.database}.APP.{STAGE}'
          MAIN_FILE = '/{APP_FILE.name}'
          QUERY_WAREHOUSE = {spec.warehouse}
          COMMENT = 'Causal decision console for {spec.label}. Reads MODELS.* and calls the AGENT procedures.'
        """
    ).collect()
    print(f"  created         {spec.database}.APP.CAUSAL_CONSOLE")

    row = session.sql(
        f"SHOW STREAMLITS LIKE 'CAUSAL_CONSOLE' IN SCHEMA {spec.database}.APP"
    ).collect()
    if row:
        print(f"\nopen: {row[0]['url_id']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

### `framework/render_notebooks.py`

Copy code

```
"""Render the analysis notebooks from a single Python source of truth.

Notebook JSON is painful to review, merge, and hand-edit, so the cell content
lives here as plain strings and the .ipynb files are generated artifacts that
happen to be committed. Edit this file, run it, commit both.

    python framework/render_notebooks.py

Every notebook opens with the same dual-mode bootstrap so the identical file
runs in a Snowflake Workspace notebook and in local Jupyter.

CAUTION on backslashes. Cell bodies live inside ordinary triple-quoted strings
here, so Python interprets escape sequences BEFORE the text reaches the notebook.
Writing \\n inside a cell body produces a real newline in the generated source and
breaks any string literal it lands in. Either double the backslash or, better,
avoid escapes in cell bodies entirely. Run framework/check_notebooks.py after every
render; it compiles every code cell and catches exactly this.
"""

from __future__ import annotations

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = PROJECT_ROOT / "notebooks"

# ---------------------------------------------------------------------------
# Shared opening cell
# ---------------------------------------------------------------------------

BOOTSTRAP = """\
# Dual-mode bootstrap. Runs unchanged in a Snowflake Workspace notebook and in
# local Jupyter: get_session() tries get_active_session() first and falls back to
# a local connection (SNOWFLAKE_CONNECTION_NAME, SNOWFLAKE_DEFAULT_CONNECTION_NAME,
# or the default in connections.toml). No connection name is hard-coded.
import sys
from pathlib import Path

# Make the framework importable without installing it. `pip install -e .` also
# works and is preferred for long-lived environments.
for candidate in (Path.cwd(), *Path.cwd().parents):
    if (candidate / "framework" / "causal_core").exists():
        sys.path.insert(0, str(candidate / "framework"))
        PROJECT_ROOT = candidate
        break

import numpy as np
import pandas as pd

from causal_core import (
    load_spec, load_copy, get_session, describe_session,
    validate_tables, load_analysis_frame, load_capacity, load_truth,
    load_panel, load_did_frame, load_event_study,
    design_matrix, feature_columns,
    COL_UNIT_ID, COL_TREATMENT, COL_OUTCOME, COL_PRE_OUTCOME,
)

spec = load_spec()          # reads active_usecase from config.yaml
copy = load_copy()
session = get_session(spec)

print(f"use case : {spec.label}  ({spec.name})")
print(f"database : {spec.database}")
print(f"unit     : {spec.unit.label_plural}")
print(f"treatment: {spec.treatment.label}  @ ${spec.treatment.cost_per_unit:,.0f} each")
print(f"outcome  : {spec.outcome.label}  (direction={spec.outcome.direction})")
for k, v in describe_session(session).items():
    print(f"  {k:<10} {v}")
"""

def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text}

def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": text,
    }

def build(name: str, cells: list[dict]) -> Path:
    """Write a notebook, splitting sources into the line lists nbformat expects."""
    stem = name.replace(".ipynb", "")
    for i, cell in enumerate(cells):
        src = cell["source"]
        if isinstance(src, str):
            cell["source"] = src.splitlines(keepends=True)
        # nbformat 4.5+ requires a stable id per cell. Deriving it from position
        # keeps diffs clean across re-renders.
        cell["id"] = f"{stem}-{i:02d}"

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    path = NOTEBOOK_DIR / name
    path.write_text(json.dumps(notebook, indent=1) + "\n")
    return path

# ---------------------------------------------------------------------------
# 01: the naive answer
# ---------------------------------------------------------------------------

NB01 = [
    md("""\
# 01. The answer you get without causal inference

A risk model tells you **who will have a bad outcome**. It does not tell you
**who you can help**. This notebook establishes what a competent team would
conclude before anyone says the word "causal", so there is something concrete to
improve on.

Two estimates, which fail differently:

1. **Raw difference.** Outcome rate among the treated against everyone else.
   This is the comparison most program evaluations actually run.
2. **S-learner flip-the-flag.** Fit a model on covariates plus a treatment flag,
   flip the flag, re-score everyone, average the difference. This is what people
   usually mean when they say "simulation".

The data is synthetic and carries a planted answer key, so at the end we can
check both against the truth. That check is impossible on real data, which is the
whole reason the synthetic use case exists.
"""),
    code(BOOTSTRAP),
    md("""\
## Confirm the data satisfies the framework contract

`validate_tables` checks that the five canonical tables exist and that every
column the spec references is actually present. It also reports which covariates
are time-invariant and which are snapshotted from the panel at the last
pre-treatment period.
"""),
    code("""\
report = validate_tables(session, spec)
for k, v in report.items():
    print(f"{k}: {v}")
"""),
    md("""\
## Load the analysis frame

Column names are standardized so nothing downstream is domain-specific:
`UNIT_ID`, `TREAT`, `Y`, `Y_PRE`, then the covariates under their own names.

`include_truth=True` also joins the planted per-unit effect. **That column is for
grading only.** It is never passed to an estimator.
"""),
    code("""\
frame = load_analysis_frame(session, spec, include_truth=True)

print(f"{len(frame):,} {spec.unit.label_plural}, {frame[COL_TREATMENT].sum():,} treated "
      f"({frame[COL_TREATMENT].mean():.1%})")
print(f"outcome mean: {frame[COL_OUTCOME].mean():.4f}")
print(f"covariates  : {feature_columns(spec, frame)}")
frame.head()
"""),
    md("""\
## The planted truth

Read this once, then set it aside until the end.

`TRUE_ATE` is the average effect across everyone. `TRUE_ATT` is the average among
those who were actually treated. They differ because treatment was not assigned
at random, and estimators target one or the other, so grading against the wrong
one would penalize a correct method.
"""),
    code("""\
TRUE_ATE = frame.TRUE_ITE.mean()
TRUE_ATT = frame.loc[frame[COL_TREATMENT] == 1, "TRUE_ITE"].mean()
baseline_untreated = frame.loc[frame[COL_TREATMENT] == 0, COL_OUTCOME].mean()

print(f"TRUE ATE : {TRUE_ATE:+.5f}")
print(f"TRUE ATT : {TRUE_ATT:+.5f}   (average among those actually treated)")
print(f"per-unit effect spread (sd): {frame.TRUE_ITE.std():.5f}")
print()
print("As a relative change it depends which denominator you use:")
print(f"  vs untreated observed rate ({baseline_untreated:.4f}): {TRUE_ATE / baseline_untreated:+.1%}")
print(f"  vs population baseline risk, which is what the spec targets: "
      f"{spec.calibration.true_ate_relative:+.1%}")
print()
print("Those differ because selection pulls the higher-risk units into treatment,")
print("so whoever is left untreated is not representative of the population. Both")
print("numbers are correct; the spec asserts the second one.")
"""),
    md("""\
## Estimate 1: the raw difference

No adjustment for who gets treated.
"""),
    code("""\
from causal_core.naive import raw_difference, s_learner_simulation, scenario_projection

naive = raw_difference(frame, spec)

for k, v in naive.summary(spec.outcome).items():
    if k != "notes":
        print(f"{k:<14} {v}")
print()
for note in naive.notes:
    print(f"  - {note}")
"""),
    md("""\
Read it literally and the program is harmful, with a tight interval and a large
sample behind it. Nothing about the output signals a problem.

It says that because the sickest units are the ones who get referred. The
comparison is measuring *who was treated*, not *what treatment did*.
"""),
    code("""\
# The mechanism, in one table: the treated were already worse off before treatment.
#
# Column names come from the spec rather than being hardcoded, so this cell works
# on any use case. Picking the covariates that differ most between arms is what
# makes the selection visible.
numeric_covs = [c for c in feature_columns(spec, frame)
                if pd.api.types.is_numeric_dtype(frame[c])]
gaps = (frame.groupby(COL_TREATMENT)[numeric_covs].mean().diff().iloc[-1]
        / frame[numeric_covs].std()).abs().sort_values(ascending=False)
most_imbalanced = gaps.head(3).index.tolist()

frame.groupby(COL_TREATMENT).agg(
    **{
        "n": (COL_UNIT_ID, "size"),
        "outcome": (COL_OUTCOME, "mean"),
        "outcome_pre": (COL_PRE_OUTCOME, "mean"),
        **{c.lower(): (c, "mean") for c in most_imbalanced},
    }
).round(4)
"""),
    md("""\
The treated group already had a worse pre-treatment outcome (`outcome_pre`), and
the three covariates shown are the ones most out of balance between the arms.
That is selection, and no amount of sample size fixes it.

## Estimate 2: the S-learner "simulation"

Fit one model on covariates plus the treatment flag, then flip the flag and
re-score everyone. This genuinely does adjust for observed confounders.
"""),
    code("""\
slearner = s_learner_simulation(frame, spec)

for k, v in slearner.summary(spec.outcome).items():
    if k != "notes":
        print(f"{k:<14} {v}")
print()
for note in slearner.notes:
    print(f"  - {note}")
"""),
    md("""\
Better than the raw difference, and still on the wrong side of zero. Note how
narrow the interval is: that is the standard error of the mean of the per-unit
predicted differences, which ignores model uncertainty entirely. It is also the
interval most practitioners report.

## The failure that actually matters

Getting the average wrong is recoverable. Being unable to rank is not, because
ranking is what a fixed budget requires.

The S-learner produces a per-unit effect for everyone, so it looks like it can
rank. Check whether those per-unit numbers carry any signal.
"""),
    code("""\
corr = np.corrcoef(slearner.cate, frame.TRUE_ITE)[0, 1]

print(f"spread of estimated per-unit effects: {slearner.cate_spread:.5f}")
print(f"spread of TRUE per-unit effects     : {frame.TRUE_ITE.std():.5f}")
print(f"correlation with truth              : {corr:+.4f}")
print()
print("A spread in the right ballpark is not evidence of signal. The correlation is.")
"""),
    md("""\
## Does it beat picking at random?

The honest test of a targeting model is a policy comparison. Take a fixed
capacity, select that many units by each rule, and measure the true benefit
actually captured.
"""),
    code("""\
CAPACITY = 2000

# spec.outcome.benefit() flips the sign when smaller is better, so "benefit" is
# always positive-is-good and nothing here knows what the outcome means.
benefit = frame.TRUE_ITE.apply(spec.outcome.benefit)
ranked_by_slearner = slearner.cate.apply(spec.outcome.benefit)

best = benefit.nlargest(CAPACITY).mean()          # an oracle that knows the truth
policies = {
    "oracle (knows truth)": best,
    "S-learner ranking":    benefit.loc[ranked_by_slearner.nlargest(CAPACITY).index].mean(),
    "random selection":     benefit.mean(),
}

pd.DataFrame([
    {"policy": name,
     "avg benefit per unit": round(v, 5),
     "share of achievable": f"{v / best:.1%}"}
    for name, v in policies.items()
])
"""),
    md("""\
The S-learner ranking is indistinguishable from choosing at random. It generated
per-unit numbers that looked like a targeting model and contained no usable
information about who to treat.

## Where this leaves us

| | raw difference | S-learner |
|---|---|---|
| Average effect | badly wrong, sign reversed | wrong sign, closer |
| Reported uncertainty | too narrow | far too narrow |
| Can it rank units? | does not try | no, no better than random |
| Does it flag its own problems? | no | no |

Neither is stupid. The problem is that neither one gives any signal about
whether it should be trusted, and both would be presented to a decision maker
with a confidence interval attached.

Notebook `02_causal.ipynb` estimates the same quantity with methods that adjust
for selection, report honest uncertainty, and can be attacked with refutation
tests, then grades everything against the planted truth.
"""),
    code("""\
# Carry the two naive results forward so notebook 02 can put them on the same
# leaderboard as the causal estimates.
from causal_core.results import Leaderboard

board = Leaderboard(spec=spec, true_ate=TRUE_ATE, true_att=TRUE_ATT)
board.add(naive)
board.add(slearner)
board.to_frame()[["method", "estimate", "truth", "rel_error", "verdict"]]
"""),
]

# ---------------------------------------------------------------------------
# 02: estimators that adjust for selection, graded against truth
# ---------------------------------------------------------------------------

NB02 = [
    md("""\
# 02. Estimating the effect properly, and grading the result

Notebook 01 produced two confident, wrong-signed answers. This notebook
estimates the same quantity three more ways and then grades every method against
the planted truth.

The three methods lean on **different assumptions** on purpose:

| Method | Assumes | Targets |
|---|---|---|
| Doubly robust (AIPW) | no unobserved confounding; correct propensity **or** outcome model | ATE |
| Causal forest (DML) | same, plus enough signal to fit per-unit effects | ATE + per-unit |
| Difference in differences | parallel pre-trends, not unconfoundedness | ATT |

Agreement between methods resting on different assumptions is much stronger
evidence than a small p-value from any one of them.

A note on packages: everything here uses econml and scikit-learn from the
Snowflake Anaconda channel. dowhy cannot be imported alongside econml because it
requires numpy>2 while econml requires numpy<2, so refutation runs in an isolated
stored procedure. See `docs/runtime-and-packages.md`.
"""),
    code(BOOTSTRAP),
    code("""\
from causal_core.causal import (
    fit_propensity, overlap_report, is_identified, balance_table,
    dr_ate, causal_forest_cate, did_estimate,
    write_cate_scores, write_diagnostics,
)
from causal_core.naive import raw_difference, s_learner_simulation
from causal_core.results import Leaderboard

frame  = load_analysis_frame(session, spec, include_truth=True)
did_f  = load_did_frame(session, spec)      # aggregated in SQL, not pandas
events = load_event_study(session, spec)

TRUE_ATE = frame.TRUE_ITE.mean()
TRUE_ATT = frame.loc[frame[COL_TREATMENT] == 1, "TRUE_ITE"].mean()

print(f"{len(frame):,} {spec.unit.label_plural}")
print(f"TRUE ATE {TRUE_ATE:+.5f} | TRUE ATT {TRUE_ATT:+.5f} | per-unit sd {frame.TRUE_ITE.std():.5f}")
"""),
    md("""\
## Step 1: is the question even answerable?

Before estimating anything, check whether comparable untreated units exist. If
they do not, no method recovers the effect and the only honest output is a
refusal. This runs first because it can invalidate everything that follows.
"""),
    code("""\
propensity = fit_propensity(frame, spec)
overlap = overlap_report(frame, propensity)
identified, reason = is_identified(overlap)

for k, v in overlap.items():
    print(f"  {k:<28} {v:.4f}" if isinstance(v, float) else f"  {k:<28} {v}")
print()
print(f"identified: {identified}")
print(f"  {reason}")
"""),
    md("""\
Overlap is adequate across the population as a whole. Hold onto that: notebook
03 and the agent both re-run this check on *specific cohorts*, and there is a
region of this data where it fails by design.

## Step 2: did the adjustment actually balance the groups?

Standardized mean differences before and after inverse-propensity weighting.
Above roughly 0.10 after weighting means a covariate is still imbalanced and the
adjustment has not done its job.
"""),
    code("""\
balance = balance_table(frame, spec, propensity)
print(f"still imbalanced after weighting: {int(balance.still_imbalanced.sum())} of {len(balance)}")
balance.head(8).round(4)
"""),
    md("""\
Note how large some of the unadjusted differences are. That is the selection
notebook 01 was unknowingly measuring.

## Step 3: estimate three ways
"""),
    code("""\
board = Leaderboard(spec=spec, true_ate=TRUE_ATE, true_att=TRUE_ATT)

# carried forward from notebook 01 for comparison
board.add(raw_difference(frame, spec))
slearner = board.add(s_learner_simulation(frame, spec))

dr = board.add(dr_ate(frame, spec, propensity=propensity))
did = board.add(did_estimate(did_f, spec, event_study=events))
forest = board.add(causal_forest_cate(frame, spec))

print("done")
"""),
    md("""\
## Step 4: the parallel trends picture

The whole diff-in-diff argument rests on this shape: a flat treated-minus-control
gap before treatment, then a step. If the gap was already moving, the method is
not applicable and the pre-trend test says so.
"""),
    code("""\
print(f"pre-trend slope {did.diagnostics['pre_trend_slope']:+.6f} per period, "
      f"p = {did.diagnostics['pre_trend_p_value']:.3f}")
print()
print("gap before treatment:", np.round(events[events.IS_PRE].GAP.values, 4))
print("gap after treatment :", np.round(events[~events.IS_PRE].GAP.values, 4))

ax = events.set_index("PERIOD_INDEX")[["TREATED_MEAN", "CONTROL_MEAN"]].plot(
    figsize=(9, 4), marker="o",
    title=f"{spec.outcome.label} by period (treatment starts at period 12)")
ax.axvline(11.5, linestyle="--", color="grey")
ax.set_ylabel(spec.outcome.label)
"""),
    md("""\
## Step 5: the leaderboard

Every estimate graded against the planted truth. `targets` matters: diff-in-diff
estimates the effect among the treated, so grading it against the population
average would penalize it for being correct.
"""),
    code("""\
board.to_frame()[
    ["method", "targets", "estimate", "ci_low", "ci_high", "truth",
     "rel_error", "ci_covers_truth", "verdict"]
].round(5)
"""),
    md("""\
Read the `verdict` column first. Every adjusted method concludes the program
helps. The unadjusted comparison concludes it harms. That is the difference
between a program being cancelled and a program being expanded.

On magnitude, the residual error in AIPW and the causal forest is not noise: this
data contains a deliberate unobserved confounder, and the generator's calibration
check reports that it implies a bias of roughly 20 to 25% of the true effect.
Recovering the sign and the rough size in the presence of unmeasured confounding
is the realistic best case, not a disappointment. Diff-in-diff does better here
because parallel trends happens to hold exactly in this data.
"""),
    md("""\
## Step 6: can these rank units?

The decision needs a ranking, not an average. Take a fixed capacity, select that
many units under each rule, and measure the true benefit actually captured.
"""),
    code("""\
CAPACITY = 8000
benefit = frame.TRUE_ITE.apply(spec.outcome.benefit)
best = benefit.nlargest(CAPACITY).mean()

def captured(scores):
    picked = scores.apply(spec.outcome.benefit).nlargest(CAPACITY).index
    return benefit.loc[picked].mean()

rows = [
    ("oracle (knows truth)",  best,                        None),
    ("causal forest",         captured(forest.cate),       np.corrcoef(forest.cate, frame.TRUE_ITE)[0, 1]),
    ("S-learner",             captured(slearner.cate),     np.corrcoef(slearner.cate, frame.TRUE_ITE)[0, 1]),
    ("risk score (Y_PRE)",    benefit.loc[frame[COL_PRE_OUTCOME].nlargest(CAPACITY).index].mean(), None),
    ("random",                benefit.mean(),              None),
]
pd.DataFrame([
    {"policy": n, "avg benefit": round(v, 5),
     "share of achievable": f"{v / best:.1%}",
     "corr with truth": None if c is None else round(c, 4)}
    for n, v, c in rows
])
"""),
    md("""\
Two honest readings of that table.

**The business result holds.** Both machine-learning rankings capture well over
70% of the achievable benefit, against about 62% for ranking by risk score, which
is what most programs do today. Same budget, materially more outcomes prevented.

**But the S-learner ranks about as well as the causal forest here.** That is a
real result and worth stating plainly rather than explaining away. When the true
effect is largely a smooth function of baseline risk, and baseline risk is
predictable from the covariates, a plain outcome model implicitly recovers enough
of that structure to rank competitively.

So what does the causal machinery actually buy? Not the ranking, on this data.
It buys the two things a decision needs besides the ranking:
"""),
    code("""\
print("MAGNITUDE, which is what converts into dollars")
for r in (slearner, forest, dr):
    err = abs(r.estimate - TRUE_ATE) / abs(TRUE_ATE)
    print(f"  {r.method:<26} {r.estimate:+.5f}   off by {err:.0%}")
print()
print("UNCERTAINTY, which is what tells you whether to act")
for r in (slearner, forest, dr):
    width = (r.ci_high - r.ci_low) if r.ci_low is not None else float('nan')
    print(f"  {r.method:<26} interval width {width:.5f}")
print()
print(f"share of units the causal forest can speak to individually: "
      f"{forest.diagnostics['share_individually_significant']:.1%}")
"""),
    md("""\
The S-learner reports an interval roughly two orders of magnitude too narrow
around an estimate that is a third too small. Project that onto a budget and you
get a confident, wrong business case. The causal forest's interval is wide because
the honest answer is genuinely uncertain, and it is the only method here that can
say which individual units it does and does not have evidence about.

## Step 7: persist for the decision layer

Per-unit effects go to a table. Everything downstream, the allocation notebook,
the agent tools, the Streamlit app, reads from here and never refits a model.
This is also the boundary where data crosses into the dowhy environment, which
runs a different numpy and pandas major version, so it must be a table rather
than a pickle.
"""),
    code("""\
# Propensity travels with the scores so the agent can judge common support for a
# narrow cohort, not just for the population as a whole.
cate_table = write_cate_scores(session, spec, frame, forest, propensity=propensity)
diag_table = write_diagnostics(session, spec, board.results)

print("wrote", cate_table)
print("wrote", diag_table)

session.sql(f'''
    SELECT METHOD, COUNT(*) AS N,
           ROUND(AVG(CATE), 5)               AS AVG_CATE,
           ROUND(AVG(NET_VALUE_PER_UNIT), 2) AS AVG_NET_VALUE,
           ROUND(SUM(IFF(NET_VALUE_PER_UNIT > 0, 1, 0)) / COUNT(*), 4) AS SHARE_WORTH_TREATING
    FROM {cate_table} GROUP BY METHOD
''').to_pandas()
"""),
    md("""\
That last column is the whole point of the next notebook. Only a fraction of
units are worth treating once the cost of treating them is set against the value
of the outcome they would avoid. Notebook `03_allocation_equity.ipynb` turns that
into an allocation under a real capacity constraint, and checks that the
resulting policy does not quietly withhold help from protected groups.
"""),
]

# ---------------------------------------------------------------------------
# 03: allocation, Qini, and the equity gate
# ---------------------------------------------------------------------------

NB03 = [
    md("""\
# 03. From a ranking to a decision

A ranked list is not a decision. The decision is which units to treat given a
fixed budget, and whether treating them returns more than it costs.

This notebook does four things:

1. Checks whether the ranking carries any signal, using **Qini curves computed
   from observed outcomes**. This is the only evaluation here that works on real
   data, where there is no answer key.
2. Allocates a fixed capacity under several policies and prices each one.
3. Prices them again against planted truth, to show the gap between the business
   case you would have written and what would actually have happened.
4. Runs the **equity gate**, which fails rather than warns.

Everything reads `MODELS.CATE_SCORES` written by notebook 02. No model is refitted
here, which is deliberate: the number quoted in a chat answer, on a dashboard, and
in this notebook must come from one place or they will drift apart.
"""),
    code(BOOTSTRAP),
    code("""\
from causal_core import (
    benefit_scores, net_value_per_unit,
    allocate_top_n, allocate_by_group, allocate_positive_value,
    policy_economics, compare_policies, qini_curve, auuc,
    check_equity, disparity_report, allocate_with_floor, EquityGateFailure,
    write_allocation, write_qini, write_equity_report,
)

frame = load_analysis_frame(session, spec, include_truth=True)

# Per-unit effects come from the table notebook 02 wrote, not from a refit.
scores_tbl = session.sql(f"SELECT * FROM {spec.models('CATE_SCORES')}").to_pandas()
frame = frame.merge(
    scores_tbl[[spec.unit.id_column, "CATE"]],
    left_on=COL_UNIT_ID, right_on=spec.unit.id_column, how="inner",
)
cate = frame["CATE"]
truth = frame["TRUE_ITE"]      # grading only, never used to decide

print(f"{len(frame):,} {spec.unit.label_plural} with estimated effects")
print(f"treating one {spec.unit.label_singular} costs ${spec.treatment.cost_per_unit:,.0f}")
print(f"one unit of {spec.outcome.label} is worth ${spec.outcome.value_per_event:,.0f}")
"""),
    md("""\
## Capacity: what the constraint actually is

Capacity is rarely a single global number. Nurses are hired per region and offer
budgets are set per market, so a globally optimal list is often unimplementable.
"""),
    code("""\
capacity_by_group = load_capacity(session, spec)

# load_capacity sums slots across every period, so divide by the number of periods
# to get the capacity available in a single period. That per-period figure is the
# real constraint: it is how many units can be under treatment at one time.
per_period = (capacity_by_group.SLOTS / spec.panel.total_periods).round().astype(int)
capacity_by_group["SLOTS_PER_PERIOD"] = per_period
TOTAL_CAPACITY = int(per_period.sum())

print(f"capacity grouped by {spec.capacity.group_column}, "
      f"measured in {spec.capacity.slots_column}")
print(f"total capacity per period: {TOTAL_CAPACITY:,} "
      f"({TOTAL_CAPACITY / len(frame):.1%} of the population)")
capacity_by_group
"""),
    md("""\
## How many units are even worth treating?

Expected value of treating a unit, minus what treating it costs. A unit with
negative net value loses money even if the effect estimate is exactly right.
"""),
    code("""\
net = net_value_per_unit(spec, cate)

print(f"expected net value per {spec.unit.label_singular}: "
      f"median ${net.median():,.0f}, p90 ${net.quantile(0.9):,.0f}")
print(f"worth treating at all: {(net > 0).sum():,} of {len(net):,} "
      f"({(net > 0).mean():.1%})")
print()
if net.mean() < 0:
    print("The AVERAGE unit loses money. Treating everyone destroys value, so the")
    print("allocation below is not an optimisation nicety, it is the whole decision.")
else:
    print("The average unit is profitable, so the question is not whether to run the")
    print("programme but how to spend a budget that cannot cover everyone.")
"""),
    md("""\
## Does the ranking carry signal? Qini, without an answer key

At each depth, take the top k units by score and compute the incremental outcome
attributable to treating them, scaling the control arm up to the treated arm's
size. A ranking with no signal traces the straight dashed line.

**This is the check you would actually run in production.** The policy comparisons
further down need planted truth and are synthetic scaffolding; this one does not.

One caveat stated plainly: Qini is unbiased for randomised treatment. Here
treatment was assigned observationally, so it inherits the same confounding as any
raw comparison. Use it to compare rankings against each other, not to read an
absolute effect off the y-axis.
"""),
    code("""\
uplift_rank = benefit_scores(spec, cate)
# What most programmes do today: rank by predicted risk. The pre-treatment outcome
# is a clean stand-in for a risk score, sign-adjusted via the spec.
risk_rank = (frame[COL_PRE_OUTCOME] * -spec.outcome.sign).rename("risk")

q_uplift = qini_curve(frame, spec, uplift_rank)
q_risk   = qini_curve(frame, spec, risk_rank)

print(f"AUUC, rank by estimated uplift : {auuc(q_uplift):+.4f}")
print(f"AUUC, rank by risk score       : {auuc(q_risk):+.4f}")
print()
print("Zero means no signal. Negative means actively worse than random, which is a")
print("result you want to discover here rather than after rollout.")

ax = q_uplift.plot(x="share_targeted", y="qini", figsize=(9, 4.5),
                   label="rank by estimated uplift")
q_risk.plot(x="share_targeted", y="qini", ax=ax, label="rank by risk score")
q_uplift.plot(x="share_targeted", y="qini_random", ax=ax, linestyle="--",
              color="grey", label="random")
ax.set_title("Qini curve, computed from observed outcomes")
ax.set_xlabel("share of population targeted")
ax.set_ylabel(f"cumulative incremental {spec.outcome.label}")
"""),
    md("""\
## Allocate a fixed capacity four ways
"""),
    code("""\
group_slots = dict(zip(capacity_by_group.GROUP_KEY,
                       capacity_by_group.SLOTS_PER_PERIOD))

policies = {
    "rank by estimated uplift": allocate_top_n(uplift_rank, TOTAL_CAPACITY),
    "rank by risk score":       allocate_top_n(risk_rank, TOTAL_CAPACITY),
    "uplift, per-group caps":   allocate_by_group(frame, spec, uplift_rank, group_slots),
    "positive net value only":  allocate_positive_value(spec, cate, TOTAL_CAPACITY),
    "random":                   allocate_top_n(
        pd.Series(np.random.default_rng(0).random(len(frame)), index=frame.index),
        TOTAL_CAPACITY),
}
for name, sel in policies.items():
    print(f"{name:<26} treats {int(sel.sum()):,}")
"""),
    md("""\
### Priced with the estimated effects

This is the business case you would write from the model alone.
"""),
    code("""\
compare_policies(spec, policies, cate)[
    ["policy", "units_treated", "total_benefit", "program_cost", "net_value", "roi"]
].round(2)
"""),
    md("""\
### Priced with planted truth

What would actually have happened. Available only because this is synthetic.
"""),
    code("""\
actual = compare_policies(spec, policies, truth)[
    ["policy", "units_treated", "total_benefit", "net_value", "roi"]
].round(2)
actual
"""),
    code("""\
# The gap between projection and reality, per policy.
proj = compare_policies(spec, policies, cate).set_index("policy")["net_value"]
real = compare_policies(spec, policies, truth).set_index("policy")["net_value"]
gap = pd.DataFrame({"projected": proj, "actual": real})
gap["error"] = gap.actual - gap.projected
gap["error_pct"] = (gap.error / gap.projected.abs()).map(lambda v: f"{v:+.1%}")
gap.round(0)
"""),
    md("""\
The projection is not exact, and it is not supposed to be: both use cases carry a
deliberate unobserved confounder, so the estimated effect is attenuated and the
projected value is conservative. A projection that matched truth exactly on
observational data would be a sign something was leaking.

What matters is the ORDERING of policies, which the estimates get right without
ever seeing the truth. That is enough to make the decision correctly.

## The equity gate

Impactability correlates with being reachable, and reachability correlates with
advantage. A model optimised for measured impact will therefore concentrate help
on whoever was already easiest to help, and nothing in the accuracy metrics above
shows it.
"""),
    code("""\
best_policy = "rank by estimated uplift"
try:
    check_equity(frame, spec, policies[best_policy])
    print("gate PASSED")
except EquityGateFailure as exc:
    print("gate FAILED, which is the expected result here.")
    print()
    print(exc)
"""),
    code("""\
# Where the disparity actually falls.
for attribute in spec.fairness.protected_attributes:
    rep = disparity_report(frame, spec, policies[best_policy], attribute)
    print(f"--- {attribute}: ratio {rep.observed_ratio:.2f} "
          f"(threshold {rep.max_disparity_ratio}) ---")
    print(rep.table[["population", "selected", "selection_rate", "representation_index"]])
    print()
"""),
    md("""\
A `representation_index` below 1.0 means a group is under-represented among those
selected relative to its size. This is the failure mode documented in Obermeyer et
al., *Science* 2019, where a widely deployed commercial care-management algorithm
under-referred Black patients because it used spending as a proxy for illness. The
model was not wrong about spending. It was answering a different question from the
one the programme needed answered.

### Remediation, and what it costs

Constrain the **intersection** of protected attributes, giving every bucket a floor
and a ceiling placed symmetrically around the overall selection rate. Every
marginal rate is then a weighted average of bucket rates inside that band, so every
marginal ratio is bounded. Two simpler approaches fail, and `equity.py` documents
why: a floor alone lets leftover capacity re-concentrate, and constraining each
attribute separately lets the first constraint consume the capacity the second
needed.
"""),
    code("""\
constrained = allocate_with_floor(frame, spec, uplift_rank, TOTAL_CAPACITY)

for attribute in spec.fairness.protected_attributes:
    before = disparity_report(frame, spec, policies[best_policy], attribute)
    after  = disparity_report(frame, spec, constrained, attribute)
    print(f"{attribute:<24} {before.observed_ratio:6.2f} -> {after.observed_ratio:5.2f} "
          f"({'PASS' if after.passed else 'FAIL'})")

print()
reports = check_equity(frame, spec, constrained, raise_on_failure=False)
print("gate on constrained policy:",
      "PASSED" if all(r.passed for r in reports) else "STILL FAILING")
"""),
    code("""\
# Price the tradeoff honestly, against truth.
tradeoff = compare_policies(
    spec,
    {"unconstrained": policies[best_policy], "equity constrained": constrained},
    truth,
)[["policy", "units_treated", "total_benefit", "net_value"]]

u = tradeoff[tradeoff.policy == "unconstrained"].iloc[0]
c = tradeoff[tradeoff.policy == "equity constrained"].iloc[0]
forgone = u.total_benefit - c.total_benefit

print(tradeoff.round(2).to_string(index=False))
print()
print(f"benefit forgone : {forgone:+.1f} of {u.total_benefit:.1f} "
      f"({forgone / u.total_benefit:+.2%})")
print(f"value forgone   : ${u.net_value - c.net_value:+,.0f}")
print()
if forgone <= 0:
    print("The constraint cost NOTHING here, and slightly improved the outcome. That")
    print("is not a free lunch: it means the unconstrained ranking concentrated on")
    print("units where the model was over-optimistic, and forcing spread acted as")
    print("regularisation against its own errors. Real, but not something to rely on.")
else:
    print("That is the price of the constraint, and it is the number to put in front")
    print("of whoever owns the decision. Presenting fairness as free is not honest;")
    print("presenting the tradeoff explicitly is what makes it a decision.")
"""),
    md("""\
## Persist the decision

The selection, the Qini curve, and the equity report all go to tables. The agent
and the app read these rather than recomputing, so a number quoted in chat cannot
disagree with a number on a dashboard.
"""),
    code("""\
print(write_allocation(session, spec, frame, constrained, cate, "equity_constrained_uplift"))
# Persist BOTH rankings, each carrying its AUUC, so the agent can answer
# "is risk targeting good enough" with a number instead of a hedge.
curves = pd.concat([
    q_uplift.assign(MODEL="estimated uplift (causal forest)", AUUC=auuc(q_uplift)),
    q_risk.assign(MODEL="risk score", AUUC=auuc(q_risk)),
], ignore_index=True)
print(write_qini(session, spec, curves))
print(write_equity_report(session, spec, reports, "equity_constrained_uplift"))
"""),
    md("""\
## What this notebook established

| Question | Answer |
|---|---|
| Does the ranking carry signal? | Yes, and risk-score ranking carries little or negative |
| How many units are worth treating? | A minority, once cost is set against value |
| Which policy wins? | Uplift targeting, by a wide margin over risk targeting |
| Would the projection have misled us? | It understates the value, and gets the ordering right |
| Is the winning policy fair? | **No.** It fails the gate badly until constrained |
| What does fairness cost? | Quantified above, and it is smaller than most people expect |

The agent tools in `agent/` expose exactly these operations over SQL, with one
addition: the ability to **refuse**. There is a cohort in this data where overlap
fails and no honest estimate exists, and an agent that answers anyway is worse than
no agent.
"""),
]

if __name__ == "__main__":
    written = [
        build("01_naive.ipynb", NB01),
        build("02_causal.ipynb", NB02),
        build("03_allocation_equity.ipynb", NB03),
    ]
    for path in written:
        print(f"wrote {path.relative_to(PROJECT_ROOT)}")
```

### `framework/show_notebook.py`

Copy code

```
"""Print the text outputs of a rendered notebook, for eyeballing results.

    python framework/show_notebook.py 03_allocation_equity

Exists because piping an inline python -c through the shell mangles quotes.
"""

import sys
from pathlib import Path

import nbformat

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def main(name: str, max_chars: int = 1400) -> None:
    path = PROJECT_ROOT / "notebooks" / f"{name}.ipynb"
    nb = nbformat.read(path, as_version=4)
    for i, cell in enumerate(nb.cells):
        for out in cell.get("outputs", []):
            text = None
            if out.get("output_type") == "stream":
                text = "".join(out.get("text", []))
            elif out.get("output_type") == "execute_result":
                text = out.get("data", {}).get("text/plain", "")
            if text and text.strip():
                print(f"----- cell {i} -----")
                print(text.strip()[:max_chars])
                print()

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "03_allocation_equity")
```

## `notebooks/`

### `notebooks/01_naive.ipynb`

Jupyter notebook, shown as Python with Markdown cells as comments.

Copy code

```
# %% [markdown]
# # 01. The answer you get without causal inference
#
# A risk model tells you **who will have a bad outcome**. It does not tell you
# **who you can help**. This notebook establishes what a competent team would
# conclude before anyone says the word "causal", so there is something concrete to
# improve on.
#
# Two estimates, which fail differently:
#
# 1. **Raw difference.** Outcome rate among the treated against everyone else.
#    This is the comparison most program evaluations actually run.
# 2. **S-learner flip-the-flag.** Fit a model on covariates plus a treatment flag,
#    flip the flag, re-score everyone, average the difference. This is what people
#    usually mean when they say "simulation".
#
# The data is synthetic and carries a planted answer key, so at the end we can
# check both against the truth. That check is impossible on real data, which is the
# whole reason the synthetic use case exists.

# %%
# Dual-mode bootstrap. Runs unchanged in a Snowflake Workspace notebook and in
# local Jupyter: get_session() tries get_active_session() first and falls back to
# a local connection (SNOWFLAKE_CONNECTION_NAME, SNOWFLAKE_DEFAULT_CONNECTION_NAME,
# or the default in connections.toml). No connection name is hard-coded.
import sys
from pathlib import Path

# Make the framework importable without installing it. `pip install -e .` also
# works and is preferred for long-lived environments.
for candidate in (Path.cwd(), *Path.cwd().parents):
    if (candidate / "framework" / "causal_core").exists():
        sys.path.insert(0, str(candidate / "framework"))
        PROJECT_ROOT = candidate
        break

import numpy as np
import pandas as pd

from causal_core import (
    load_spec, load_copy, get_session, describe_session,
    validate_tables, load_analysis_frame, load_capacity, load_truth,
    load_panel, load_did_frame, load_event_study,
    design_matrix, feature_columns,
    COL_UNIT_ID, COL_TREATMENT, COL_OUTCOME, COL_PRE_OUTCOME,
)

spec = load_spec()          # reads active_usecase from config.yaml
copy = load_copy()
session = get_session(spec)

print(f"use case : {spec.label}  ({spec.name})")
print(f"database : {spec.database}")
print(f"unit     : {spec.unit.label_plural}")
print(f"treatment: {spec.treatment.label}  @ ${spec.treatment.cost_per_unit:,.0f} each")
print(f"outcome  : {spec.outcome.label}  (direction={spec.outcome.direction})")
for k, v in describe_session(session).items():
    print(f"  {k:<10} {v}")

# %% [markdown]
# ## Confirm the data satisfies the framework contract
#
# `validate_tables` checks that the five canonical tables exist and that every
# column the spec references is actually present. It also reports which covariates
# are time-invariant and which are snapshotted from the panel at the last
# pre-treatment period.

# %%
report = validate_tables(session, spec)
for k, v in report.items():
    print(f"{k}: {v}")

# %% [markdown]
# ## Load the analysis frame
#
# Column names are standardized so nothing downstream is domain-specific:
# `UNIT_ID`, `TREAT`, `Y`, `Y_PRE`, then the covariates under their own names.
#
# `include_truth=True` also joins the planted per-unit effect. **That column is for
# grading only.** It is never passed to an estimator.

# %%
frame = load_analysis_frame(session, spec, include_truth=True)

print(f"{len(frame):,} {spec.unit.label_plural}, {frame[COL_TREATMENT].sum():,} treated "
      f"({frame[COL_TREATMENT].mean():.1%})")
print(f"outcome mean: {frame[COL_OUTCOME].mean():.4f}")
print(f"covariates  : {feature_columns(spec, frame)}")
frame.head()

# %% [markdown]
# ## The planted truth
#
# Read this once, then set it aside until the end.
#
# `TRUE_ATE` is the average effect across everyone. `TRUE_ATT` is the average among
# those who were actually treated. They differ because treatment was not assigned
# at random, and estimators target one or the other, so grading against the wrong
# one would penalize a correct method.

# %%
TRUE_ATE = frame.TRUE_ITE.mean()
TRUE_ATT = frame.loc[frame[COL_TREATMENT] == 1, "TRUE_ITE"].mean()
baseline_untreated = frame.loc[frame[COL_TREATMENT] == 0, COL_OUTCOME].mean()

print(f"TRUE ATE : {TRUE_ATE:+.5f}")
print(f"TRUE ATT : {TRUE_ATT:+.5f}   (average among those actually treated)")
print(f"per-unit effect spread (sd): {frame.TRUE_ITE.std():.5f}")
print()
print("As a relative change it depends which denominator you use:")
print(f"  vs untreated observed rate ({baseline_untreated:.4f}): {TRUE_ATE / baseline_untreated:+.1%}")
print(f"  vs population baseline risk, which is what the spec targets: "
      f"{spec.calibration.true_ate_relative:+.1%}")
print()
print("Those differ because selection pulls the higher-risk units into treatment,")
print("so whoever is left untreated is not representative of the population. Both")
print("numbers are correct; the spec asserts the second one.")

# %% [markdown]
# ## Estimate 1: the raw difference
#
# No adjustment for who gets treated.

# %%
from causal_core.naive import raw_difference, s_learner_simulation, scenario_projection

naive = raw_difference(frame, spec)

for k, v in naive.summary(spec.outcome).items():
    if k != "notes":
        print(f"{k:<14} {v}")
print()
for note in naive.notes:
    print(f"  - {note}")

# %% [markdown]
# Read it literally and the program is harmful, with a tight interval and a large
# sample behind it. Nothing about the output signals a problem.
#
# It says that because the sickest units are the ones who get referred. The
# comparison is measuring *who was treated*, not *what treatment did*.

# %%
# The mechanism, in one table: the treated were already worse off before treatment.
#
# Column names come from the spec rather than being hardcoded, so this cell works
# on any use case. Picking the covariates that differ most between arms is what
# makes the selection visible.
numeric_covs = [c for c in feature_columns(spec, frame)
                if pd.api.types.is_numeric_dtype(frame[c])]
gaps = (frame.groupby(COL_TREATMENT)[numeric_covs].mean().diff().iloc[-1]
        / frame[numeric_covs].std()).abs().sort_values(ascending=False)
most_imbalanced = gaps.head(3).index.tolist()

frame.groupby(COL_TREATMENT).agg(
    **{
        "n": (COL_UNIT_ID, "size"),
        "outcome": (COL_OUTCOME, "mean"),
        "outcome_pre": (COL_PRE_OUTCOME, "mean"),
        **{c.lower(): (c, "mean") for c in most_imbalanced},
    }
).round(4)

# %% [markdown]
# The treated group already had a worse pre-treatment outcome (`outcome_pre`), and
# the three covariates shown are the ones most out of balance between the arms.
# That is selection, and no amount of sample size fixes it.
#
# ## Estimate 2: the S-learner "simulation"
#
# Fit one model on covariates plus the treatment flag, then flip the flag and
# re-score everyone. This genuinely does adjust for observed confounders.

# %%
slearner = s_learner_simulation(frame, spec)

for k, v in slearner.summary(spec.outcome).items():
    if k != "notes":
        print(f"{k:<14} {v}")
print()
for note in slearner.notes:
    print(f"  - {note}")

# %% [markdown]
# Better than the raw difference, and still on the wrong side of zero. Note how
# narrow the interval is: that is the standard error of the mean of the per-unit
# predicted differences, which ignores model uncertainty entirely. It is also the
# interval most practitioners report.
#
# ## The failure that actually matters
#
# Getting the average wrong is recoverable. Being unable to rank is not, because
# ranking is what a fixed budget requires.
#
# The S-learner produces a per-unit effect for everyone, so it looks like it can
# rank. Check whether those per-unit numbers carry any signal.

# %%
corr = np.corrcoef(slearner.cate, frame.TRUE_ITE)[0, 1]

print(f"spread of estimated per-unit effects: {slearner.cate_spread:.5f}")
print(f"spread of TRUE per-unit effects     : {frame.TRUE_ITE.std():.5f}")
print(f"correlation with truth              : {corr:+.4f}")
print()
print("A spread in the right ballpark is not evidence of signal. The correlation is.")

# %% [markdown]
# ## Does it beat picking at random?
#
# The honest test of a targeting model is a policy comparison. Take a fixed
# capacity, select that many units by each rule, and measure the true benefit
# actually captured.

# %%
CAPACITY = 2000

# spec.outcome.benefit() flips the sign when smaller is better, so "benefit" is
# always positive-is-good and nothing here knows what the outcome means.
benefit = frame.TRUE_ITE.apply(spec.outcome.benefit)
ranked_by_slearner = slearner.cate.apply(spec.outcome.benefit)

best = benefit.nlargest(CAPACITY).mean()          # an oracle that knows the truth
policies = {
    "oracle (knows truth)": best,
    "S-learner ranking":    benefit.loc[ranked_by_slearner.nlargest(CAPACITY).index].mean(),
    "random selection":     benefit.mean(),
}

pd.DataFrame([
    {"policy": name,
     "avg benefit per unit": round(v, 5),
     "share of achievable": f"{v / best:.1%}"}
    for name, v in policies.items()
])

# %% [markdown]
# The S-learner ranking is indistinguishable from choosing at random. It generated
# per-unit numbers that looked like a targeting model and contained no usable
# information about who to treat.
#
# ## Where this leaves us
#
# | | raw difference | S-learner |
# |---|---|---|
# | Average effect | badly wrong, sign reversed | wrong sign, closer |
# | Reported uncertainty | too narrow | far too narrow |
# | Can it rank units? | does not try | no, no better than random |
# | Does it flag its own problems? | no | no |
#
# Neither is stupid. The problem is that neither one gives any signal about
# whether it should be trusted, and both would be presented to a decision maker
# with a confidence interval attached.
#
# Notebook `02_causal.ipynb` estimates the same quantity with methods that adjust
# for selection, report honest uncertainty, and can be attacked with refutation
# tests, then grades everything against the planted truth.

# %%
# Carry the two naive results forward so notebook 02 can put them on the same
# leaderboard as the causal estimates.
from causal_core.results import Leaderboard

board = Leaderboard(spec=spec, true_ate=TRUE_ATE, true_att=TRUE_ATT)
board.add(naive)
board.add(slearner)
board.to_frame()[["method", "estimate", "truth", "rel_error", "verdict"]]
```

### `notebooks/02_causal.ipynb`

Jupyter notebook, shown as Python with Markdown cells as comments.

Copy code

```
# %% [markdown]
# # 02. Estimating the effect properly, and grading the result
#
# Notebook 01 produced two confident, wrong-signed answers. This notebook
# estimates the same quantity three more ways and then grades every method against
# the planted truth.
#
# The three methods lean on **different assumptions** on purpose:
#
# | Method | Assumes | Targets |
# |---|---|---|
# | Doubly robust (AIPW) | no unobserved confounding; correct propensity **or** outcome model | ATE |
# | Causal forest (DML) | same, plus enough signal to fit per-unit effects | ATE + per-unit |
# | Difference in differences | parallel pre-trends, not unconfoundedness | ATT |
#
# Agreement between methods resting on different assumptions is much stronger
# evidence than a small p-value from any one of them.
#
# A note on packages: everything here uses econml and scikit-learn from the
# Snowflake Anaconda channel. dowhy cannot be imported alongside econml because it
# requires numpy>2 while econml requires numpy<2, so refutation runs in an isolated
# stored procedure. See `docs/runtime-and-packages.md`.

# %%
# Dual-mode bootstrap. Runs unchanged in a Snowflake Workspace notebook and in
# local Jupyter: get_session() tries get_active_session() first and falls back to
# a local connection (SNOWFLAKE_CONNECTION_NAME, SNOWFLAKE_DEFAULT_CONNECTION_NAME,
# or the default in connections.toml). No connection name is hard-coded.
import sys
from pathlib import Path

# Make the framework importable without installing it. `pip install -e .` also
# works and is preferred for long-lived environments.
for candidate in (Path.cwd(), *Path.cwd().parents):
    if (candidate / "framework" / "causal_core").exists():
        sys.path.insert(0, str(candidate / "framework"))
        PROJECT_ROOT = candidate
        break

import numpy as np
import pandas as pd

from causal_core import (
    load_spec, load_copy, get_session, describe_session,
    validate_tables, load_analysis_frame, load_capacity, load_truth,
    load_panel, load_did_frame, load_event_study,
    design_matrix, feature_columns,
    COL_UNIT_ID, COL_TREATMENT, COL_OUTCOME, COL_PRE_OUTCOME,
)

spec = load_spec()          # reads active_usecase from config.yaml
copy = load_copy()
session = get_session(spec)

print(f"use case : {spec.label}  ({spec.name})")
print(f"database : {spec.database}")
print(f"unit     : {spec.unit.label_plural}")
print(f"treatment: {spec.treatment.label}  @ ${spec.treatment.cost_per_unit:,.0f} each")
print(f"outcome  : {spec.outcome.label}  (direction={spec.outcome.direction})")
for k, v in describe_session(session).items():
    print(f"  {k:<10} {v}")

# %%
from causal_core.causal import (
    fit_propensity, overlap_report, is_identified, balance_table,
    dr_ate, causal_forest_cate, did_estimate,
    write_cate_scores, write_diagnostics,
)
from causal_core.naive import raw_difference, s_learner_simulation
from causal_core.results import Leaderboard

frame  = load_analysis_frame(session, spec, include_truth=True)
did_f  = load_did_frame(session, spec)      # aggregated in SQL, not pandas
events = load_event_study(session, spec)

TRUE_ATE = frame.TRUE_ITE.mean()
TRUE_ATT = frame.loc[frame[COL_TREATMENT] == 1, "TRUE_ITE"].mean()

print(f"{len(frame):,} {spec.unit.label_plural}")
print(f"TRUE ATE {TRUE_ATE:+.5f} | TRUE ATT {TRUE_ATT:+.5f} | per-unit sd {frame.TRUE_ITE.std():.5f}")

# %% [markdown]
# ## Step 1: is the question even answerable?
#
# Before estimating anything, check whether comparable untreated units exist. If
# they do not, no method recovers the effect and the only honest output is a
# refusal. This runs first because it can invalidate everything that follows.

# %%
propensity = fit_propensity(frame, spec)
overlap = overlap_report(frame, propensity)
identified, reason = is_identified(overlap)

for k, v in overlap.items():
    print(f"  {k:<28} {v:.4f}" if isinstance(v, float) else f"  {k:<28} {v}")
print()
print(f"identified: {identified}")
print(f"  {reason}")

# %% [markdown]
# Overlap is adequate across the population as a whole. Hold onto that: notebook
# 03 and the agent both re-run this check on *specific cohorts*, and there is a
# region of this data where it fails by design.
#
# ## Step 2: did the adjustment actually balance the groups?
#
# Standardized mean differences before and after inverse-propensity weighting.
# Above roughly 0.10 after weighting means a covariate is still imbalanced and the
# adjustment has not done its job.

# %%
balance = balance_table(frame, spec, propensity)
print(f"still imbalanced after weighting: {int(balance.still_imbalanced.sum())} of {len(balance)}")
balance.head(8).round(4)

# %% [markdown]
# Note how large some of the unadjusted differences are. That is the selection
# notebook 01 was unknowingly measuring.
#
# ## Step 3: estimate three ways

# %%
board = Leaderboard(spec=spec, true_ate=TRUE_ATE, true_att=TRUE_ATT)

# carried forward from notebook 01 for comparison
board.add(raw_difference(frame, spec))
slearner = board.add(s_learner_simulation(frame, spec))

dr = board.add(dr_ate(frame, spec, propensity=propensity))
did = board.add(did_estimate(did_f, spec, event_study=events))
forest = board.add(causal_forest_cate(frame, spec))

print("done")

# %% [markdown]
# ## Step 4: the parallel trends picture
#
# The whole diff-in-diff argument rests on this shape: a flat treated-minus-control
# gap before treatment, then a step. If the gap was already moving, the method is
# not applicable and the pre-trend test says so.

# %%
print(f"pre-trend slope {did.diagnostics['pre_trend_slope']:+.6f} per period, "
      f"p = {did.diagnostics['pre_trend_p_value']:.3f}")
print()
print("gap before treatment:", np.round(events[events.IS_PRE].GAP.values, 4))
print("gap after treatment :", np.round(events[~events.IS_PRE].GAP.values, 4))

ax = events.set_index("PERIOD_INDEX")[["TREATED_MEAN", "CONTROL_MEAN"]].plot(
    figsize=(9, 4), marker="o",
    title=f"{spec.outcome.label} by period (treatment starts at period 12)")
ax.axvline(11.5, linestyle="--", color="grey")
ax.set_ylabel(spec.outcome.label)

# %% [markdown]
# ## Step 5: the leaderboard
#
# Every estimate graded against the planted truth. `targets` matters: diff-in-diff
# estimates the effect among the treated, so grading it against the population
# average would penalize it for being correct.

# %%
board.to_frame()[
    ["method", "targets", "estimate", "ci_low", "ci_high", "truth",
     "rel_error", "ci_covers_truth", "verdict"]
].round(5)

# %% [markdown]
# Read the `verdict` column first. Every adjusted method concludes the program
# helps. The unadjusted comparison concludes it harms. That is the difference
# between a program being cancelled and a program being expanded.
#
# On magnitude, the residual error in AIPW and the causal forest is not noise: this
# data contains a deliberate unobserved confounder, and the generator's calibration
# check reports that it implies a bias of roughly 20 to 25% of the true effect.
# Recovering the sign and the rough size in the presence of unmeasured confounding
# is the realistic best case, not a disappointment. Diff-in-diff does better here
# because parallel trends happens to hold exactly in this data.

# %% [markdown]
# ## Step 6: can these rank units?
#
# The decision needs a ranking, not an average. Take a fixed capacity, select that
# many units under each rule, and measure the true benefit actually captured.

# %%
CAPACITY = 8000
benefit = frame.TRUE_ITE.apply(spec.outcome.benefit)
best = benefit.nlargest(CAPACITY).mean()

def captured(scores):
    picked = scores.apply(spec.outcome.benefit).nlargest(CAPACITY).index
    return benefit.loc[picked].mean()

rows = [
    ("oracle (knows truth)",  best,                        None),
    ("causal forest",         captured(forest.cate),       np.corrcoef(forest.cate, frame.TRUE_ITE)[0, 1]),
    ("S-learner",             captured(slearner.cate),     np.corrcoef(slearner.cate, frame.TRUE_ITE)[0, 1]),
    ("risk score (Y_PRE)",    benefit.loc[frame[COL_PRE_OUTCOME].nlargest(CAPACITY).index].mean(), None),
    ("random",                benefit.mean(),              None),
]
pd.DataFrame([
    {"policy": n, "avg benefit": round(v, 5),
     "share of achievable": f"{v / best:.1%}",
     "corr with truth": None if c is None else round(c, 4)}
    for n, v, c in rows
])

# %% [markdown]
# Two honest readings of that table.
#
# **The business result holds.** Both machine-learning rankings capture well over
# 70% of the achievable benefit, against about 62% for ranking by risk score, which
# is what most programs do today. Same budget, materially more outcomes prevented.
#
# **But the S-learner ranks about as well as the causal forest here.** That is a
# real result and worth stating plainly rather than explaining away. When the true
# effect is largely a smooth function of baseline risk, and baseline risk is
# predictable from the covariates, a plain outcome model implicitly recovers enough
# of that structure to rank competitively.
#
# So what does the causal machinery actually buy? Not the ranking, on this data.
# It buys the two things a decision needs besides the ranking:

# %%
print("MAGNITUDE, which is what converts into dollars")
for r in (slearner, forest, dr):
    err = abs(r.estimate - TRUE_ATE) / abs(TRUE_ATE)
    print(f"  {r.method:<26} {r.estimate:+.5f}   off by {err:.0%}")
print()
print("UNCERTAINTY, which is what tells you whether to act")
for r in (slearner, forest, dr):
    width = (r.ci_high - r.ci_low) if r.ci_low is not None else float('nan')
    print(f"  {r.method:<26} interval width {width:.5f}")
print()
print(f"share of units the causal forest can speak to individually: "
      f"{forest.diagnostics['share_individually_significant']:.1%}")

# %% [markdown]
# The S-learner reports an interval roughly two orders of magnitude too narrow
# around an estimate that is a third too small. Project that onto a budget and you
# get a confident, wrong business case. The causal forest's interval is wide because
# the honest answer is genuinely uncertain, and it is the only method here that can
# say which individual units it does and does not have evidence about.
#
# ## Step 7: persist for the decision layer
#
# Per-unit effects go to a table. Everything downstream, the allocation notebook,
# the agent tools, the Streamlit app, reads from here and never refits a model.
# This is also the boundary where data crosses into the dowhy environment, which
# runs a different numpy and pandas major version, so it must be a table rather
# than a pickle.

# %%
# Propensity travels with the scores so the agent can judge common support for a
# narrow cohort, not just for the population as a whole.
cate_table = write_cate_scores(session, spec, frame, forest, propensity=propensity)
diag_table = write_diagnostics(session, spec, board.results)

print("wrote", cate_table)
print("wrote", diag_table)

session.sql(f'''
    SELECT METHOD, COUNT(*) AS N,
           ROUND(AVG(CATE), 5)               AS AVG_CATE,
           ROUND(AVG(NET_VALUE_PER_UNIT), 2) AS AVG_NET_VALUE,
           ROUND(SUM(IFF(NET_VALUE_PER_UNIT > 0, 1, 0)) / COUNT(*), 4) AS SHARE_WORTH_TREATING
    FROM {cate_table} GROUP BY METHOD
''').to_pandas()

# %% [markdown]
# That last column is the whole point of the next notebook. Only a fraction of
# units are worth treating once the cost of treating them is set against the value
# of the outcome they would avoid. Notebook `03_allocation_equity.ipynb` turns that
# into an allocation under a real capacity constraint, and checks that the
# resulting policy does not quietly withhold help from protected groups.
```

### `notebooks/03_allocation_equity.ipynb`

Jupyter notebook, shown as Python with Markdown cells as comments.

Copy code

```
# %% [markdown]
# # 03. From a ranking to a decision
#
# A ranked list is not a decision. The decision is which units to treat given a
# fixed budget, and whether treating them returns more than it costs.
#
# This notebook does four things:
#
# 1. Checks whether the ranking carries any signal, using **Qini curves computed
#    from observed outcomes**. This is the only evaluation here that works on real
#    data, where there is no answer key.
# 2. Allocates a fixed capacity under several policies and prices each one.
# 3. Prices them again against planted truth, to show the gap between the business
#    case you would have written and what would actually have happened.
# 4. Runs the **equity gate**, which fails rather than warns.
#
# Everything reads `MODELS.CATE_SCORES` written by notebook 02. No model is refitted
# here, which is deliberate: the number quoted in a chat answer, on a dashboard, and
# in this notebook must come from one place or they will drift apart.

# %%
# Dual-mode bootstrap. Runs unchanged in a Snowflake Workspace notebook and in
# local Jupyter: get_session() tries get_active_session() first and falls back to
# a local connection (SNOWFLAKE_CONNECTION_NAME, SNOWFLAKE_DEFAULT_CONNECTION_NAME,
# or the default in connections.toml). No connection name is hard-coded.
import sys
from pathlib import Path

# Make the framework importable without installing it. `pip install -e .` also
# works and is preferred for long-lived environments.
for candidate in (Path.cwd(), *Path.cwd().parents):
    if (candidate / "framework" / "causal_core").exists():
        sys.path.insert(0, str(candidate / "framework"))
        PROJECT_ROOT = candidate
        break

import numpy as np
import pandas as pd

from causal_core import (
    load_spec, load_copy, get_session, describe_session,
    validate_tables, load_analysis_frame, load_capacity, load_truth,
    load_panel, load_did_frame, load_event_study,
    design_matrix, feature_columns,
    COL_UNIT_ID, COL_TREATMENT, COL_OUTCOME, COL_PRE_OUTCOME,
)

spec = load_spec()          # reads active_usecase from config.yaml
copy = load_copy()
session = get_session(spec)

print(f"use case : {spec.label}  ({spec.name})")
print(f"database : {spec.database}")
print(f"unit     : {spec.unit.label_plural}")
print(f"treatment: {spec.treatment.label}  @ ${spec.treatment.cost_per_unit:,.0f} each")
print(f"outcome  : {spec.outcome.label}  (direction={spec.outcome.direction})")
for k, v in describe_session(session).items():
    print(f"  {k:<10} {v}")

# %%
from causal_core import (
    benefit_scores, net_value_per_unit,
    allocate_top_n, allocate_by_group, allocate_positive_value,
    policy_economics, compare_policies, qini_curve, auuc,
    check_equity, disparity_report, allocate_with_floor, EquityGateFailure,
    write_allocation, write_qini, write_equity_report,
)

frame = load_analysis_frame(session, spec, include_truth=True)

# Per-unit effects come from the table notebook 02 wrote, not from a refit.
scores_tbl = session.sql(f"SELECT * FROM {spec.models('CATE_SCORES')}").to_pandas()
frame = frame.merge(
    scores_tbl[[spec.unit.id_column, "CATE"]],
    left_on=COL_UNIT_ID, right_on=spec.unit.id_column, how="inner",
)
cate = frame["CATE"]
truth = frame["TRUE_ITE"]      # grading only, never used to decide

print(f"{len(frame):,} {spec.unit.label_plural} with estimated effects")
print(f"treating one {spec.unit.label_singular} costs ${spec.treatment.cost_per_unit:,.0f}")
print(f"one unit of {spec.outcome.label} is worth ${spec.outcome.value_per_event:,.0f}")

# %% [markdown]
# ## Capacity: what the constraint actually is
#
# Capacity is rarely a single global number. Nurses are hired per region and offer
# budgets are set per market, so a globally optimal list is often unimplementable.

# %%
capacity_by_group = load_capacity(session, spec)

# load_capacity sums slots across every period, so divide by the number of periods
# to get the capacity available in a single period. That per-period figure is the
# real constraint: it is how many units can be under treatment at one time.
per_period = (capacity_by_group.SLOTS / spec.panel.total_periods).round().astype(int)
capacity_by_group["SLOTS_PER_PERIOD"] = per_period
TOTAL_CAPACITY = int(per_period.sum())

print(f"capacity grouped by {spec.capacity.group_column}, "
      f"measured in {spec.capacity.slots_column}")
print(f"total capacity per period: {TOTAL_CAPACITY:,} "
      f"({TOTAL_CAPACITY / len(frame):.1%} of the population)")
capacity_by_group

# %% [markdown]
# ## How many units are even worth treating?
#
# Expected value of treating a unit, minus what treating it costs. A unit with
# negative net value loses money even if the effect estimate is exactly right.

# %%
net = net_value_per_unit(spec, cate)

print(f"expected net value per {spec.unit.label_singular}: "
      f"median ${net.median():,.0f}, p90 ${net.quantile(0.9):,.0f}")
print(f"worth treating at all: {(net > 0).sum():,} of {len(net):,} "
      f"({(net > 0).mean():.1%})")
print()
if net.mean() < 0:
    print("The AVERAGE unit loses money. Treating everyone destroys value, so the")
    print("allocation below is not an optimisation nicety, it is the whole decision.")
else:
    print("The average unit is profitable, so the question is not whether to run the")
    print("programme but how to spend a budget that cannot cover everyone.")

# %% [markdown]
# ## Does the ranking carry signal? Qini, without an answer key
#
# At each depth, take the top k units by score and compute the incremental outcome
# attributable to treating them, scaling the control arm up to the treated arm's
# size. A ranking with no signal traces the straight dashed line.
#
# **This is the check you would actually run in production.** The policy comparisons
# further down need planted truth and are synthetic scaffolding; this one does not.
#
# One caveat stated plainly: Qini is unbiased for randomised treatment. Here
# treatment was assigned observationally, so it inherits the same confounding as any
# raw comparison. Use it to compare rankings against each other, not to read an
# absolute effect off the y-axis.

# %%
uplift_rank = benefit_scores(spec, cate)
# What most programmes do today: rank by predicted risk. The pre-treatment outcome
# is a clean stand-in for a risk score, sign-adjusted via the spec.
risk_rank = (frame[COL_PRE_OUTCOME] * -spec.outcome.sign).rename("risk")

q_uplift = qini_curve(frame, spec, uplift_rank)
q_risk   = qini_curve(frame, spec, risk_rank)

print(f"AUUC, rank by estimated uplift : {auuc(q_uplift):+.4f}")
print(f"AUUC, rank by risk score       : {auuc(q_risk):+.4f}")
print()
print("Zero means no signal. Negative means actively worse than random, which is a")
print("result you want to discover here rather than after rollout.")

ax = q_uplift.plot(x="share_targeted", y="qini", figsize=(9, 4.5),
                   label="rank by estimated uplift")
q_risk.plot(x="share_targeted", y="qini", ax=ax, label="rank by risk score")
q_uplift.plot(x="share_targeted", y="qini_random", ax=ax, linestyle="--",
              color="grey", label="random")
ax.set_title("Qini curve, computed from observed outcomes")
ax.set_xlabel("share of population targeted")
ax.set_ylabel(f"cumulative incremental {spec.outcome.label}")

# %% [markdown]
# ## Allocate a fixed capacity four ways

# %%
group_slots = dict(zip(capacity_by_group.GROUP_KEY,
                       capacity_by_group.SLOTS_PER_PERIOD))

policies = {
    "rank by estimated uplift": allocate_top_n(uplift_rank, TOTAL_CAPACITY),
    "rank by risk score":       allocate_top_n(risk_rank, TOTAL_CAPACITY),
    "uplift, per-group caps":   allocate_by_group(frame, spec, uplift_rank, group_slots),
    "positive net value only":  allocate_positive_value(spec, cate, TOTAL_CAPACITY),
    "random":                   allocate_top_n(
        pd.Series(np.random.default_rng(0).random(len(frame)), index=frame.index),
        TOTAL_CAPACITY),
}
for name, sel in policies.items():
    print(f"{name:<26} treats {int(sel.sum()):,}")

# %% [markdown]
# ### Priced with the estimated effects
#
# This is the business case you would write from the model alone.

# %%
compare_policies(spec, policies, cate)[
    ["policy", "units_treated", "total_benefit", "program_cost", "net_value", "roi"]
].round(2)

# %% [markdown]
# ### Priced with planted truth
#
# What would actually have happened. Available only because this is synthetic.

# %%
actual = compare_policies(spec, policies, truth)[
    ["policy", "units_treated", "total_benefit", "net_value", "roi"]
].round(2)
actual

# %%
# The gap between projection and reality, per policy.
proj = compare_policies(spec, policies, cate).set_index("policy")["net_value"]
real = compare_policies(spec, policies, truth).set_index("policy")["net_value"]
gap = pd.DataFrame({"projected": proj, "actual": real})
gap["error"] = gap.actual - gap.projected
gap["error_pct"] = (gap.error / gap.projected.abs()).map(lambda v: f"{v:+.1%}")
gap.round(0)

# %% [markdown]
# The projection is not exact, and it is not supposed to be: both use cases carry a
# deliberate unobserved confounder, so the estimated effect is attenuated and the
# projected value is conservative. A projection that matched truth exactly on
# observational data would be a sign something was leaking.
#
# What matters is the ORDERING of policies, which the estimates get right without
# ever seeing the truth. That is enough to make the decision correctly.
#
# ## The equity gate
#
# Impactability correlates with being reachable, and reachability correlates with
# advantage. A model optimised for measured impact will therefore concentrate help
# on whoever was already easiest to help, and nothing in the accuracy metrics above
# shows it.

# %%
best_policy = "rank by estimated uplift"
try:
    check_equity(frame, spec, policies[best_policy])
    print("gate PASSED")
except EquityGateFailure as exc:
    print("gate FAILED, which is the expected result here.")
    print()
    print(exc)

# %%
# Where the disparity actually falls.
for attribute in spec.fairness.protected_attributes:
    rep = disparity_report(frame, spec, policies[best_policy], attribute)
    print(f"--- {attribute}: ratio {rep.observed_ratio:.2f} "
          f"(threshold {rep.max_disparity_ratio}) ---")
    print(rep.table[["population", "selected", "selection_rate", "representation_index"]])
    print()

# %% [markdown]
# A `representation_index` below 1.0 means a group is under-represented among those
# selected relative to its size. This is the failure mode documented in Obermeyer et
# al., *Science* 2019, where a widely deployed commercial care-management algorithm
# under-referred Black patients because it used spending as a proxy for illness. The
# model was not wrong about spending. It was answering a different question from the
# one the programme needed answered.
#
# ### Remediation, and what it costs
#
# Constrain the **intersection** of protected attributes, giving every bucket a floor
# and a ceiling placed symmetrically around the overall selection rate. Every
# marginal rate is then a weighted average of bucket rates inside that band, so every
# marginal ratio is bounded. Two simpler approaches fail, and `equity.py` documents
# why: a floor alone lets leftover capacity re-concentrate, and constraining each
# attribute separately lets the first constraint consume the capacity the second
# needed.

# %%
constrained = allocate_with_floor(frame, spec, uplift_rank, TOTAL_CAPACITY)

for attribute in spec.fairness.protected_attributes:
    before = disparity_report(frame, spec, policies[best_policy], attribute)
    after  = disparity_report(frame, spec, constrained, attribute)
    print(f"{attribute:<24} {before.observed_ratio:6.2f} -> {after.observed_ratio:5.2f} "
          f"({'PASS' if after.passed else 'FAIL'})")

print()
reports = check_equity(frame, spec, constrained, raise_on_failure=False)
print("gate on constrained policy:",
      "PASSED" if all(r.passed for r in reports) else "STILL FAILING")

# %%
# Price the tradeoff honestly, against truth.
tradeoff = compare_policies(
    spec,
    {"unconstrained": policies[best_policy], "equity constrained": constrained},
    truth,
)[["policy", "units_treated", "total_benefit", "net_value"]]

u = tradeoff[tradeoff.policy == "unconstrained"].iloc[0]
c = tradeoff[tradeoff.policy == "equity constrained"].iloc[0]
forgone = u.total_benefit - c.total_benefit

print(tradeoff.round(2).to_string(index=False))
print()
print(f"benefit forgone : {forgone:+.1f} of {u.total_benefit:.1f} "
      f"({forgone / u.total_benefit:+.2%})")
print(f"value forgone   : ${u.net_value - c.net_value:+,.0f}")
print()
if forgone <= 0:
    print("The constraint cost NOTHING here, and slightly improved the outcome. That")
    print("is not a free lunch: it means the unconstrained ranking concentrated on")
    print("units where the model was over-optimistic, and forcing spread acted as")
    print("regularisation against its own errors. Real, but not something to rely on.")
else:
    print("That is the price of the constraint, and it is the number to put in front")
    print("of whoever owns the decision. Presenting fairness as free is not honest;")
    print("presenting the tradeoff explicitly is what makes it a decision.")

# %% [markdown]
# ## Persist the decision
#
# The selection, the Qini curve, and the equity report all go to tables. The agent
# and the app read these rather than recomputing, so a number quoted in chat cannot
# disagree with a number on a dashboard.

# %%
print(write_allocation(session, spec, frame, constrained, cate, "equity_constrained_uplift"))
# Persist BOTH rankings, each carrying its AUUC, so the agent can answer
# "is risk targeting good enough" with a number instead of a hedge.
curves = pd.concat([
    q_uplift.assign(MODEL="estimated uplift (causal forest)", AUUC=auuc(q_uplift)),
    q_risk.assign(MODEL="risk score", AUUC=auuc(q_risk)),
], ignore_index=True)
print(write_qini(session, spec, curves))
print(write_equity_report(session, spec, reports, "equity_constrained_uplift"))

# %% [markdown]
# ## What this notebook established
#
# | Question | Answer |
# |---|---|
# | Does the ranking carry signal? | Yes, and risk-score ranking carries little or negative |
# | How many units are worth treating? | A minority, once cost is set against value |
# | Which policy wins? | Uplift targeting, by a wide margin over risk targeting |
# | Would the projection have misled us? | It understates the value, and gets the ordering right |
# | Is the winning policy fair? | **No.** It fails the gate badly until constrained |
# | What does fairness cost? | Quantified above, and it is smaller than most people expect |
#
# The agent tools in `agent/` expose exactly these operations over SQL, with one
# addition: the ability to **refuse**. There is a cohort in this data where overlap
# fails and no honest estimate exists, and an agent that answers anyway is worse than
# no agent.
```

## `sql/`

### `sql/00_verify_packages.sql`

Copy code

```
-- =====================================================================
-- sql/00_verify_packages.sql
--
-- Run this FIRST, in any new account, before running a use case setup.
-- It proves the two package paths the framework depends on actually work,
-- and it fails loudly if they do not.
--
-- Why this file exists: the two causal libraries this framework uses cannot
-- live in the same Python environment, and one of them cannot be installed
-- from PyPI at all on a Snowflake warehouse. Those constraints are not
-- obvious and they are expensive to rediscover. See
-- docs/runtime-and-packages.md for the full explanation.
--
-- Expected runtime: 3 to 6 minutes, most of it package resolution.
-- =====================================================================

SET cookbook_wh        = 'COOKBOOK_AGENT_CAUSAL_GROUNDING_WH';
SET cookbook_verify_db = 'COOKBOOK_AGENT_CAUSAL_GROUNDING_VERIFY';

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
    WITH WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 120
    AUTO_RESUME = TRUE
    COMMENT = 'Cortex AI Cookbook: agent-causal-grounding';

CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_verify_db)
    COMMENT = 'Throwaway. Safe to drop after verification.';
USE DATABASE IDENTIFIER($cookbook_verify_db);
CREATE SCHEMA IF NOT EXISTS PKG;

USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA PKG;

-- ---------------------------------------------------------------------
-- Check 1: econml from the Anaconda channel.
--
-- This is the workhorse. It must come from Anaconda: PyPI has no aarch64
-- wheel for econml, and Snowflake warehouse Python is aarch64, so pip falls
-- back to a source build that fails compiling Cython against numpy 2.x.
-- Note there is no ARTIFACT_REPOSITORY clause here - that is the point.
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE VERIFY_ECONML()
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python', 'econml', 'scikit-learn', 'statsmodels', 'numpy', 'pandas')
HANDLER = 'run'
AS $$
def run(session):
    import econml, numpy, pandas, sklearn, statsmodels
    from econml.dml import CausalForestDML, LinearDML
    from econml.dr import DRLearner
    assert int(numpy.__version__.split('.')[0]) < 2, "econml needs numpy<2"
    return (f"OK econml={econml.__version__} numpy={numpy.__version__} "
            f"pandas={pandas.__version__} sklearn={sklearn.__version__} "
            f"statsmodels={statsmodels.__version__}")
$$;

CALL VERIFY_ECONML();
-- Expect: OK econml=0.15.0 numpy=1.26.4 pandas=2.3.3 sklearn=1.4.2 statsmodels=0.15.0
-- (unpinned packages resolve to the channel's current version, so these can move)

-- ---------------------------------------------------------------------
-- Check 2: dowhy from the PyPI artifact repository, fully isolated.
--
-- dowhy ships a pure-Python py3-none-any wheel, so architecture is a
-- non-issue. It pins numpy>2, which is why it can never share a procedure
-- with econml. Everything it needs arrives from PyPI alongside it.
--
-- Requires SNOWFLAKE.PYPI_REPOSITORY_USER, which is granted to PUBLIC by
-- default. If your account revoked that, an administrator runs:
--   GRANT DATABASE ROLE SNOWFLAKE.PYPI_REPOSITORY_USER TO ROLE <your_role>;
--
-- This does a full end-to-end causal estimate plus three refutation tests on
-- data with a known planted effect, so a pass means the whole dowhy path is
-- usable, not merely that the import resolved.
-- ---------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE VERIFY_DOWHY()
RETURNS STRING
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
ARTIFACT_REPOSITORY = snowflake.snowpark.pypi_shared_repository
PACKAGES = ('snowflake-snowpark-python', 'dowhy==0.14')
HANDLER = 'run'
AS $$
import numpy as np
import pandas as pd
import logging
logging.getLogger("dowhy").setLevel(logging.ERROR)

def run(session):
    from dowhy import CausalModel

    # Planted world: X confounds both treatment and outcome, so the raw
    # difference in means is badly biased toward zero.
    rng = np.random.default_rng(42)
    n = 3000
    x = rng.normal(0, 1, n)
    p = 1 / (1 + np.exp(-(0.9 * x)))
    t = (rng.uniform(0, 1, n) < p).astype(int)
    true_effect = -0.40
    y = 0.5 * x + true_effect * t + rng.normal(0, 0.5, n)
    df = pd.DataFrame({"X": x, "T": t, "Y": y})

    naive = df[df["T"] == 1]["Y"].mean() - df[df["T"] == 0]["Y"].mean()

    m = CausalModel(data=df, treatment="T", outcome="Y", common_causes=["X"])

    # Reuse this same estimand object for refutation. estimate_effect() sets
    # identifier_method on it; passing a freshly identified estimand to
    # refute_estimate() raises AttributeError on NoneType.
    ident = m.identify_effect(proceed_when_unidentifiable=True)
    est = m.estimate_effect(ident, method_name="backdoor.linear_regression", target_units="ate")

    placebo = m.refute_estimate(ident, est, method_name="placebo_treatment_refuter",
                                placebo_type="permute", num_simulations=15)
    rcc = m.refute_estimate(ident, est, method_name="random_common_cause", num_simulations=5)
    subset = m.refute_estimate(ident, est, method_name="data_subset_refuter",
                               subset_fraction=0.8, num_simulations=5)

    # Adjusted estimate must recover truth; placebo must collapse to ~0.
    assert abs(est.value - true_effect) < 0.10, f"did not recover truth: {est.value}"
    assert abs(placebo.new_effect) < 0.10, f"placebo did not collapse: {placebo.new_effect}"

    return (f"OK true={true_effect:.3f} naive={naive:.3f} adjusted={est.value:.3f} "
            f"placebo={placebo.new_effect:.4f} rcc={rcc.new_effect:.3f} "
            f"subset={subset.new_effect:.3f}")
$$;

CALL VERIFY_DOWHY();
-- Expect something close to:
--   OK true=-0.400 naive=-0.031 adjusted=-0.421 placebo=-0.0032
--      rcc=-0.420 subset=-0.413
--
-- Read it as: the naive number understates the real effect by ~92%, the
-- adjusted estimate lands within 5% of truth, and the refutation tests do
-- not overturn it. That is the entire thesis of this framework in one row.

-- ---------------------------------------------------------------------
-- Check 3 (negative control): prove the two cannot be combined.
--
-- This SHOULD fail at CREATE time with a dependency resolution error. It is
-- here so nobody spends an afternoon rediscovering the conflict. Uncomment
-- to see it.
-- ---------------------------------------------------------------------
-- CREATE OR REPLACE PROCEDURE VERIFY_BOTH_FAILS()
-- RETURNS STRING
-- LANGUAGE PYTHON
-- RUNTIME_VERSION = '3.11'
-- ARTIFACT_REPOSITORY = snowflake.snowpark.pypi_shared_repository
-- PACKAGES = ('snowflake-snowpark-python', 'dowhy==0.14', 'econml==0.15.1')
-- HANDLER = 'run'
-- AS $$
-- def run(session):
--     return "unreachable"
-- $$;
-- Expected error:
--   Because dowhy==0.14 depends on numpy>2.0 and econml==0.15.1 depends on
--   numpy<2, we can conclude that dowhy==0.14 and econml==0.15.1 are
--   incompatible.

-- ---------------------------------------------------------------------
-- Cleanup
-- ---------------------------------------------------------------------
-- sql/99_teardown.sql drops this database. To drop only the throwaway now:
-- DROP DATABASE IF EXISTS IDENTIFIER($cookbook_verify_db);
```

### `sql/10_agent_user_role.sql`

Copy code

```
-- =====================================================================
-- sql/10_agent_user_role.sql
--
-- Optional. Run AFTER framework/deploy_agent.py, because it grants on the
-- procedures and the agent that script creates.
--
-- Creates a role that can ask the agent questions and nothing else. It gets
-- USAGE on the warehouse, the database, the AGENT schema, the six tool
-- procedures, and the agent. It gets NO privilege on the DATA or MODELS
-- schemas, so it cannot SELECT the tables and cannot run the raw
-- treated-versus-untreated comparison that gets the sign wrong.
--
-- That works because the tool procedures are EXECUTE AS OWNER: they read
-- MODELS.* and DATA.UNIT with the owner's privileges. It is also the risk. Any
-- role you grant USAGE on these procedures reads those tables through them, so
-- grant this role, and only this role, to the people who should use the agent.
--
-- WHO RUNS WHAT. Start this script as the BUILD ROLE: the role that ran the use
-- case scripts and framework/deploy_agent.py, and so owns the database, the
-- procedures and the agent. The script records that role, then switches roles
-- itself:
--
--   Part 1, ACCOUNTADMIN. Creates the role, grants it
--           SNOWFLAKE.CORTEX_AGENT_USER (any other role fails with "Database
--           role 'SNOWFLAKE.CORTEX_AGENT_USER' does not exist or not
--           authorized"), grants it to you, and then transfers OWNERSHIP of the
--           new role to the build role. That last step is what lets
--           sql/99_teardown.sql, run as the build role, drop it.
--   Part 2, the build role again. The object grants, which the owner of the
--           objects makes.
--
-- If you do not have ACCOUNTADMIN, have an administrator run Part 1 with your
-- build role name in place of $cookbook_build_role, then run Part 2 yourself.
-- Removed by sql/99_teardown.sql.
-- =====================================================================

SET cookbook_db         = 'COOKBOOK_AGENT_CAUSAL_GROUNDING';
SET cookbook_wh         = 'COOKBOOK_AGENT_CAUSAL_GROUNDING_WH';
SET cookbook_user_role  = 'COOKBOOK_AGENT_CAUSAL_GROUNDING_USER';
SET cookbook_me         = '"' || CURRENT_USER() || '"';
SET cookbook_build_role = CURRENT_ROLE();

-- ---------------------------------------------------------------------
-- Part 1: ACCOUNTADMIN
-- ---------------------------------------------------------------------
USE ROLE ACCOUNTADMIN;

CREATE ROLE IF NOT EXISTS IDENTIFIER($cookbook_user_role)
    COMMENT = 'Cortex AI Cookbook: may run the causal decision agent, may not read its tables';

-- Cortex Agents need CORTEX_USER or CORTEX_AGENT_USER. Granted to this role only.
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_AGENT_USER TO ROLE IDENTIFIER($cookbook_user_role);

GRANT ROLE IDENTIFIER($cookbook_user_role) TO USER IDENTIFIER($cookbook_me);

-- Hand the role to the build role, so teardown does not need ACCOUNTADMIN.
GRANT OWNERSHIP ON ROLE IDENTIFIER($cookbook_user_role)
    TO ROLE IDENTIFIER($cookbook_build_role) COPY CURRENT GRANTS;

-- ---------------------------------------------------------------------
-- Part 2: the build role
-- ---------------------------------------------------------------------
USE ROLE IDENTIFIER($cookbook_build_role);

GRANT USAGE ON WAREHOUSE IDENTIFIER($cookbook_wh) TO ROLE IDENTIFIER($cookbook_user_role);
GRANT USAGE ON DATABASE IDENTIFIER($cookbook_db) TO ROLE IDENTIFIER($cookbook_user_role);

USE DATABASE IDENTIFIER($cookbook_db);
GRANT USAGE ON SCHEMA AGENT TO ROLE IDENTIFIER($cookbook_user_role);

-- The six tools, by exact signature. Deliberately no grant on DATA or MODELS.
GRANT USAGE ON PROCEDURE AGENT.CHECK_IDENTIFICATION(VARCHAR)          TO ROLE IDENTIFIER($cookbook_user_role);
GRANT USAGE ON PROCEDURE AGENT.RUN_SCENARIO(NUMBER, VARCHAR, BOOLEAN) TO ROLE IDENTIFIER($cookbook_user_role);
GRANT USAGE ON PROCEDURE AGENT.OPTIMIZE_ALLOCATION(FLOAT)             TO ROLE IDENTIFIER($cookbook_user_role);
GRANT USAGE ON PROCEDURE AGENT.COMPARE_TARGETING_STRATEGIES()         TO ROLE IDENTIFIER($cookbook_user_role);
GRANT USAGE ON PROCEDURE AGENT.EXPLAIN_ASSUMPTIONS()                  TO ROLE IDENTIFIER($cookbook_user_role);
GRANT USAGE ON PROCEDURE AGENT.REFUTE_ESTIMATE(NUMBER, NUMBER)        TO ROLE IDENTIFIER($cookbook_user_role);

GRANT USAGE ON AGENT AGENT.DECISION_AGENT TO ROLE IDENTIFIER($cookbook_user_role);

SHOW GRANTS TO ROLE IDENTIFIER($cookbook_user_role);
SHOW GRANTS ON ROLE IDENTIFIER($cookbook_user_role);
```

### `sql/99_teardown.sql`

Copy code

```
-- =====================================================================
-- sql/99_teardown.sql
--
-- Drops everything this recipe created, and nothing else.
--
-- Each use case database holds the DATA, TRUTH, MODELS, AGENT, and APP schemas,
-- so dropping it removes every table, procedure, the Cortex Agent, and the
-- Streamlit console for that use case. No other database is touched, and the
-- recipe makes no account-level changes, so there is nothing to restore.
--
-- Re-running the use case scripts afterwards rebuilds byte-identical data,
-- because all randomness is hash-derived rather than RANDOM().
-- =====================================================================

SET cookbook_db        = 'COOKBOOK_AGENT_CAUSAL_GROUNDING';
SET cookbook_churn_db  = 'COOKBOOK_AGENT_CAUSAL_GROUNDING_CHURN';
SET cookbook_verify_db = 'COOKBOOK_AGENT_CAUSAL_GROUNDING_VERIFY';
SET cookbook_wh        = 'COOKBOOK_AGENT_CAUSAL_GROUNDING_WH';
SET cookbook_user_role = 'COOKBOOK_AGENT_CAUSAL_GROUNDING_USER';

DROP DATABASE IF EXISTS IDENTIFIER($cookbook_db);
DROP DATABASE IF EXISTS IDENTIFIER($cookbook_churn_db);

-- Throwaway database created by sql/00_verify_packages.sql.
DROP DATABASE IF EXISTS IDENTIFIER($cookbook_verify_db);

-- Created by sql/10_agent_user_role.sql, if you ran it.
DROP ROLE IF EXISTS IDENTIFIER($cookbook_user_role);

DROP WAREHOUSE IF EXISTS IDENTIFIER($cookbook_wh);

-- Nothing named for this recipe should remain.
SHOW DATABASES LIKE 'COOKBOOK_AGENT_CAUSAL_GROUNDING%';
SHOW WAREHOUSES LIKE 'COOKBOOK_AGENT_CAUSAL_GROUNDING%';
SHOW ROLES LIKE 'COOKBOOK_AGENT_CAUSAL_GROUNDING%';
```

## `tests/`

### `tests/conftest.py`

Copy code

```
"""Shared fixtures.

Two kinds of test live in this suite, and the split matters for whether it gets run.

**Fast tests** need no Snowflake connection. They build small in-memory data
generating processes in numpy, where the true effect is known exactly and
independent replications are cheap, and they call the estimator functions directly.
These are the tests that verify the estimators are CORRECT.

**Integration tests** run against the deployed fixture and the agent procedures.
They verify the pipeline is WIRED correctly. They are marked ``snowflake`` and can be
skipped:

    pytest tests -m "not snowflake"      # seconds, no connection needed
    pytest tests                         # everything

Why in-memory DGPs rather than subsamples of the 100,000-row fixture: confidence
interval coverage is a statement about repeated independent draws from a population.
Subsamples of one realised dataset are not independent draws, so measured coverage
against a fixture would be biased in a way that is hard to reason about. Generating
fresh data per replication gives the real thing, and at n=4,000 it runs in seconds.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "framework"))

from causal_core.data import (  # noqa: E402
    COL_OUTCOME,
    COL_PRE_OUTCOME,
    COL_TREATMENT,
    COL_UNIT_ID,
)
from causal_core.spec import UseCaseSpec  # noqa: E402

def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "snowflake: requires a live Snowflake connection and deployed fixture",
    )
    config.addinivalue_line("markers", "slow: takes more than a few seconds")

# ---------------------------------------------------------------------------
# A minimal but real spec, built through the same from_dict path the YAML uses
# ---------------------------------------------------------------------------

def make_spec(
    direction: str = "minimize",
    value_per_event: float = 10_000.0,
    cost_per_unit: float = 500.0,
    max_disparity_ratio: float = 1.25,
) -> UseCaseSpec:
    """Build a spec via ``UseCaseSpec.from_dict``, exercising the real loader.

    Constructing the dataclasses directly would skip every validation guard, which
    is precisely the code most worth testing.
    """
    return UseCaseSpec.from_dict(
        {
            "name": "unit_test",
            "label": "Unit test use case",
            "database": "TEST_DB",
            "warehouse": "TEST_WH",
            "unit": {
                "id_column": "UNIT_ID",
                "label_singular": "widget",
                "label_plural": "widgets",
            },
            "treatment": {
                "column": "TREATED_FLAG",
                "label": "the intervention",
                "cost_per_unit": cost_per_unit,
            },
            "outcome": {
                "primary": {
                    "column": "OUTCOME_RATE",
                    "type": "continuous",
                    "direction": direction,
                    "label": "outcome rate",
                    "value_per_event": value_per_event,
                    "pre_column": "OUTCOME_RATE_PRE",
                    "panel_column": "OUTCOME_EVENT",
                }
            },
            "covariates": {
                "observed": ["X1", "X2", "GROUP_A", "GROUP_B"],
                "categorical": ["GROUP_A", "GROUP_B"],
            },
            "fairness": {
                "protected_attributes": ["GROUP_A", "GROUP_B"],
                "max_disparity_ratio": max_disparity_ratio,
            },
            "panel": {
                "period_column": "PERIOD_START",
                "period_grain": "month",
                "pre_periods": 12,
                "post_periods": 12,
            },
            "capacity": {"group_column": "GROUP_A", "slots_column": "SLOTS"},
            "calibration": {
                "true_ate_relative": 0.20,
                "naive_bias_direction": "positive",
                "overlap_breaks_above_percentile": 98,
            },
        }
    )

@pytest.fixture(scope="session")
def spec() -> UseCaseSpec:
    return make_spec()

# ---------------------------------------------------------------------------
# In-memory DGP with a known answer
# ---------------------------------------------------------------------------

def make_frame(
    n: int = 4000,
    seed: int = 0,
    ate: float = -0.05,
    confounding: float = 0.8,
    prognostic: float = 0.12,
    hidden_confounding: float = 0.0,
    noise: float = 0.05,
) -> tuple[pd.DataFrame, float]:
    """Generate data whose true average effect is known exactly.

    Treatment depends on ``X1``, which is OBSERVED and in the covariate set, so the
    effect is identifiable and a correct estimator must recover it. ``X1`` also raises
    the baseline outcome, so the naive difference is biased in a known direction:
    that is what makes this a test of adjustment rather than of arithmetic.

    ``hidden_confounding`` adds a driver of both treatment and outcome that is NOT in
    the covariate set. Use it to assert that estimates degrade when the
    no-unmeasured-confounding assumption is violated, which is the failure mode the
    real pipeline warns about but never demonstrates on itself.

    Returns the frame and the true ATE on that realisation. The realised ATE is
    returned rather than the ``ate`` parameter because effects are heterogeneous, so
    the sample average is the quantity an estimator is actually targeting.
    """
    rng = np.random.default_rng(seed)

    x1 = rng.normal(size=n)
    x2 = rng.normal(size=n)
    hidden = rng.normal(size=n)
    group_a = rng.choice(["a1", "a2", "a3"], size=n)
    group_b = rng.choice([1, 2, 3, 4, 5], size=n)

    # `prognostic` is how strongly X1 raises the outcome level. Together with
    # `confounding` (how strongly X1 raises treatment probability) it sets the naive
    # bias, which is roughly prognostic * (E[X1|treated] - E[X1|untreated]). At the
    # defaults that bias exceeds |ate|, so the naive difference comes out with the
    # WRONG SIGN, reproducing the central failure the real pipeline demonstrates.
    baseline = 0.25 + prognostic * x1 + 0.02 * x2 + hidden_confounding * 0.10 * hidden

    logit = -1.2 + confounding * x1 + hidden_confounding * 1.2 * hidden
    treated = rng.binomial(1, 1.0 / (1.0 + np.exp(-logit)))

    # Heterogeneous effect driven by x2, which does NOT drive assignment. That
    # separation is what makes ranking by effect different from ranking by risk.
    ite = ate * (1.0 + 0.6 * x2)

    pre = baseline + rng.normal(0, noise, n)
    post = baseline + treated * ite + rng.normal(0, noise, n)

    frame = pd.DataFrame(
        {
            COL_UNIT_ID: np.arange(n),
            COL_TREATMENT: treated,
            COL_OUTCOME: post,
            COL_PRE_OUTCOME: pre,
            "X1": x1,
            "X2": x2,
            "GROUP_A": group_a,
            "GROUP_B": group_b,
            "TRUE_ITE": ite,
        }
    )
    return frame, float(ite.mean())

@pytest.fixture
def frame_and_truth():
    return make_frame(seed=7)

# ---------------------------------------------------------------------------
# Snowflake session, skipped cleanly when unavailable
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def live():
    """(session, spec) against the deployed payer fixture, or skip."""
    try:
        from causal_core import get_session, load_spec

        real_spec = load_spec("payer_care_management")
        session = get_session(real_spec)
        session.sql("SELECT 1").collect()
        return session, real_spec
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"no live Snowflake connection: {exc}")
```

### `tests/test_allocation.py`

Copy code

```
"""Allocation arithmetic, and whether a ranking evaluation can detect signal.

The Qini tests use RANDOMISED treatment (``confounding=0.0``), because that is the
setting where Qini is unbiased. Under observational assignment it inherits the same
confounding as any raw comparison, so testing it there would conflate a broken
implementation with a correctly-reported bias.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from causal_core.allocate import (
    allocate_by_group,
    allocate_positive_value,
    allocate_top_n,
    auuc,
    benefit_scores,
    net_value_per_unit,
    policy_economics,
    qini_curve,
)

from conftest import make_frame, make_spec

# ---------------------------------------------------------------------------
# Selection respects its constraints
# ---------------------------------------------------------------------------

def test_top_n_selects_exactly_capacity_and_picks_the_best():
    frame, _ = make_frame(n=1000, seed=11)
    spec = make_spec()
    scores = benefit_scores(spec, frame.TRUE_ITE)

    selected = allocate_top_n(scores, 100)

    assert int(selected.sum()) == 100
    assert scores[selected].min() >= scores[~selected].max(), (
        "every selected unit must score at least as high as every rejected one"
    )

def test_top_n_cannot_exceed_the_population():
    frame, _ = make_frame(n=50, seed=12)
    scores = benefit_scores(make_spec(), frame.TRUE_ITE)
    assert int(allocate_top_n(scores, 500).sum()) == 50

def test_by_group_respects_every_group_cap():
    frame, _ = make_frame(n=3000, seed=13)
    spec = make_spec()
    scores = benefit_scores(spec, frame.TRUE_ITE)
    caps = {"a1": 40, "a2": 10, "a3": 0}

    selected = allocate_by_group(frame, spec, scores, caps)
    counts = frame.loc[selected, "GROUP_A"].value_counts().to_dict()

    for group, cap in caps.items():
        assert counts.get(group, 0) <= cap, f"group {group} exceeded its cap"
    assert counts.get("a3", 0) == 0, "a zero cap must mean zero selections"

def test_positive_value_never_selects_a_money_loser():
    """The distinguishing behaviour: leave capacity unused rather than destroy value."""
    frame, _ = make_frame(n=2000, seed=14)
    # Cost set above what most units can return, so few clear the bar.
    spec = make_spec(cost_per_unit=600.0, value_per_event=10_000.0)

    selected = allocate_positive_value(spec, frame.TRUE_ITE, capacity=2000)
    value = net_value_per_unit(spec, frame.TRUE_ITE)

    assert int(selected.sum()) < 2000, "should not have filled the whole capacity"
    assert (value[selected] > 0).all(), (
        "every selected unit must have positive net value"
    )

def test_positive_value_selects_nothing_when_nothing_pays():
    frame, _ = make_frame(n=1000, seed=15)
    spec = make_spec(cost_per_unit=10_000_000.0)
    assert int(allocate_positive_value(spec, frame.TRUE_ITE, 1000).sum()) == 0

# ---------------------------------------------------------------------------
# Economics
# ---------------------------------------------------------------------------

def test_policy_economics_arithmetic_is_internally_consistent():
    frame, _ = make_frame(n=1000, seed=16)
    spec = make_spec(cost_per_unit=500.0, value_per_event=10_000.0)
    selected = allocate_top_n(benefit_scores(spec, frame.TRUE_ITE), 200)

    econ = policy_economics(spec, selected, frame.TRUE_ITE)

    assert econ["units_treated"] == 200
    assert econ["program_cost"] == pytest.approx(200 * 500.0)
    assert econ["gross_value"] == pytest.approx(econ["total_benefit"] * 10_000.0)
    assert econ["net_value"] == pytest.approx(
        econ["gross_value"] - econ["program_cost"]
    )
    assert econ["roi"] == pytest.approx(econ["net_value"] / econ["program_cost"])

def test_policy_economics_handles_an_empty_selection():
    frame, _ = make_frame(n=100, seed=17)
    spec = make_spec()
    empty = pd.Series(False, index=frame.index)

    econ = policy_economics(spec, empty, frame.TRUE_ITE)
    assert econ["units_treated"] == 0
    assert econ["net_value"] == 0.0

def test_targeting_by_effect_beats_targeting_by_baseline_risk():
    """The core claim. Effect heterogeneity is driven by X2, prognosis by X1.

    If this fails, either the ranking code is broken or the DGP has collapsed the two
    into the same thing, which is the design flaw that makes uplift modelling
    pointless.
    """
    frame, _ = make_frame(n=4000, seed=18)
    spec = make_spec()

    by_effect = allocate_top_n(benefit_scores(spec, frame.TRUE_ITE), 400)
    by_risk = allocate_top_n(frame[["Y_PRE"]].squeeze() * -spec.outcome.sign, 400)

    effect_benefit = policy_economics(spec, by_effect, frame.TRUE_ITE)["total_benefit"]
    risk_benefit = policy_economics(spec, by_risk, frame.TRUE_ITE)["total_benefit"]

    assert effect_benefit > risk_benefit * 1.2, (
        f"effect targeting captured {effect_benefit:.3f} against {risk_benefit:.3f} "
        "for risk targeting; the margin should be substantial"
    )

# ---------------------------------------------------------------------------
# Qini and AUUC
# ---------------------------------------------------------------------------

def test_auuc_is_near_zero_for_a_random_ranking():
    """A ranking with no information must score about zero, not something positive."""
    frame, _ = make_frame(n=20_000, seed=19, confounding=0.0)
    spec = make_spec()
    noise = pd.Series(np.random.default_rng(0).random(len(frame)), index=frame.index)

    score = auuc(qini_curve(frame, spec, noise))
    assert abs(score) < 0.10, f"random ranking scored {score:+.4f}, expected near zero"

def test_auuc_is_clearly_positive_for_a_ranking_that_knows_the_truth():
    frame, _ = make_frame(n=20_000, seed=20, confounding=0.0)
    spec = make_spec()

    score = auuc(qini_curve(frame, spec, benefit_scores(spec, frame.TRUE_ITE)))
    assert score > 0.10, f"an oracle ranking scored only {score:+.4f}"

def test_auuc_is_negative_for_a_deliberately_inverted_ranking():
    """Negative AUUC must be reachable, since the notebooks report it for risk ranking."""
    frame, _ = make_frame(n=20_000, seed=21, confounding=0.0)
    spec = make_spec()

    inverted = -benefit_scores(spec, frame.TRUE_ITE)
    assert auuc(qini_curve(frame, spec, inverted)) < -0.05

def test_qini_curve_is_well_formed():
    frame, _ = make_frame(n=5000, seed=22, confounding=0.0)
    curve = qini_curve(frame, make_spec(), benefit_scores(make_spec(), frame.TRUE_ITE))

    assert curve.share_targeted.is_monotonic_increasing
    assert curve.share_targeted.iloc[-1] == pytest.approx(1.0)
    assert (curve.n_treated_in_group + curve.n_control_in_group == curve.depth).all()
    # The random reference line must be a straight line through the endpoint.
    assert curve.qini_random.iloc[-1] == pytest.approx(curve.qini.iloc[-1])

def test_qini_is_symmetric_under_negating_both_outcome_and_direction():
    """Negating the outcome AND flipping the direction must be a no-op.

    Note what this does NOT claim. Flipping the spec direction alone does not leave
    the result unchanged, because the data is untouched: a treatment that lowers Y is
    beneficial under `minimize` and harmful under `maximize`, so AUUC correctly flips
    sign. An earlier version of this test asserted the wrong invariant and failed for
    exactly that reason.

    The real symmetry is that "minimise Y" and "maximise -Y" are the same problem, and
    both the ranking and the outcome handling must apply the sign consistently. If only
    one of them did, this would fail while every single-direction test still passed.
    """
    frame, _ = make_frame(n=8000, seed=23, confounding=0.0)
    mini, maxi = make_spec(direction="minimize"), make_spec(direction="maximize")

    mirrored = frame.copy()
    mirrored["Y"] = -frame["Y"]

    minimising = auuc(qini_curve(frame, mini, benefit_scores(mini, frame.TRUE_ITE)))
    maximising = auuc(qini_curve(mirrored, maxi, benefit_scores(maxi, -frame.TRUE_ITE)))

    assert minimising == pytest.approx(maximising, abs=1e-9)
    assert minimising > 0.10, "sanity: the oracle ranking should score well either way"
```

### `tests/test_equity.py`

Copy code

```
"""The fairness gate, and the bound it claims to guarantee.

The important test here is the property test: for ANY capacity and ANY threshold,
constraining the intersection must hold every marginal disparity ratio under the
threshold. That is a claim about the algorithm, not an observation about the bundled
fixture, and the two failed designs that preceded the current one both passed on some
parameter settings while breaking on others.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from causal_core.allocate import allocate_top_n, benefit_scores
from causal_core.equity import (
    EquityGateFailure,
    allocate_with_floor,
    check_equity,
    disparity_report,
)

from conftest import make_frame, make_spec

def _biased_scores(frame: pd.DataFrame) -> pd.Series:
    """Scores that deliberately favour one level of each protected attribute.

    Reproduces the real failure mode: the model is not told about the protected
    attribute, but whatever it ranks on happens to correlate with it.
    """
    favour_a = frame.GROUP_A.map({"a1": 3.0, "a2": 0.5, "a3": -2.0}).astype(float)
    favour_b = (3 - frame.GROUP_B.astype(float)) * 1.5
    return (favour_a + favour_b + frame.X2 * 0.2).rename("score")

# ---------------------------------------------------------------------------
# The gate detects what it is meant to detect
# ---------------------------------------------------------------------------

def test_gate_fails_on_a_deliberately_skewed_selection():
    frame, _ = make_frame(n=6000, seed=31)
    spec = make_spec(max_disparity_ratio=1.25)
    skewed = allocate_top_n(_biased_scores(frame), 600)

    with pytest.raises(EquityGateFailure) as excinfo:
        check_equity(frame, spec, skewed)

    message = str(excinfo.value)
    assert "GROUP_A" in message or "GROUP_B" in message
    assert "threshold" in message.lower()

def test_gate_passes_on_a_proportional_selection():
    """A selection that mirrors the population must not trip the gate."""
    frame, _ = make_frame(n=6000, seed=32)
    spec = make_spec(max_disparity_ratio=1.25)

    rng = np.random.default_rng(0)
    random_pick = allocate_top_n(
        pd.Series(rng.random(len(frame)), index=frame.index), 600
    )
    reports = check_equity(frame, spec, random_pick, raise_on_failure=False)

    assert all(r.passed for r in reports), (
        "random selection should sit near parity; ratios were "
        + ", ".join(f"{r.attribute}={r.observed_ratio:.3f}" for r in reports)
    )

def test_gate_raises_by_default_rather_than_returning_a_flag():
    """A check that can be ignored by not reading the return value is not a gate."""
    frame, _ = make_frame(n=6000, seed=33)
    spec = make_spec(max_disparity_ratio=1.05)
    skewed = allocate_top_n(_biased_scores(frame), 600)

    with pytest.raises(EquityGateFailure):
        check_equity(frame, spec, skewed)

    # ...but it must be possible to inspect without raising, for comparisons.
    reports = check_equity(frame, spec, skewed, raise_on_failure=False)
    assert any(not r.passed for r in reports)

def test_representation_index_marks_under_representation_correctly():
    frame, _ = make_frame(n=6000, seed=34)
    spec = make_spec()
    skewed = allocate_top_n(_biased_scores(frame), 600)

    report = disparity_report(frame, spec, skewed, "GROUP_A")
    table = report.table

    assert table.loc["a1", "representation_index"] > 1.0
    assert table.loc["a3", "representation_index"] < 1.0
    assert report.observed_ratio > 1.25

def test_disparity_report_survives_a_selection_of_nobody():
    frame, _ = make_frame(n=1000, seed=35)
    nobody = pd.Series(False, index=frame.index)

    report = disparity_report(frame, make_spec(), nobody, "GROUP_A")
    assert report.passed, "an empty selection cannot be unfair"
    assert np.isnan(report.observed_ratio)

def test_unknown_protected_attribute_fails_loudly():
    frame, _ = make_frame(n=500, seed=36)
    with pytest.raises(KeyError, match="NOT_A_COLUMN"):
        disparity_report(
            frame, make_spec(), pd.Series(True, index=frame.index), "NOT_A_COLUMN"
        )

# ---------------------------------------------------------------------------
# The guarantee
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("capacity", [200, 600, 1500, 3000])
@pytest.mark.parametrize("max_ratio", [1.05, 1.25, 1.50, 2.00])
def test_intersection_constraint_bounds_every_marginal_ratio(capacity, max_ratio):
    """The claim the equity module makes, checked across the parameter space.

    Both earlier designs would pass some cells of this grid and fail others: a floor
    alone reopens the ratio when leftover capacity re-concentrates, and constraining
    attributes one at a time lets the first constraint consume the capacity the second
    needs. Only constraining the intersection satisfies the whole grid.
    """
    frame, _ = make_frame(n=6000, seed=37)
    spec = make_spec(max_disparity_ratio=max_ratio)
    scores = _biased_scores(frame)

    constrained = allocate_with_floor(frame, spec, scores, capacity)
    reports = check_equity(frame, spec, constrained, raise_on_failure=False)

    for report in reports:
        assert report.observed_ratio <= max_ratio, (
            f"{report.attribute} reached {report.observed_ratio:.4f} against a "
            f"threshold of {max_ratio} at capacity {capacity}"
        )

@pytest.mark.parametrize("capacity", [200, 600, 1500])
def test_constrained_allocation_respects_capacity(capacity):
    frame, _ = make_frame(n=6000, seed=38)
    spec = make_spec()
    constrained = allocate_with_floor(frame, spec, _biased_scores(frame), capacity)

    assert int(constrained.sum()) <= capacity, "must never exceed the capacity given"
    # Ceilings can leave a little unused; a large shortfall means the bands are broken.
    assert int(constrained.sum()) >= 0.90 * capacity, (
        f"only used {int(constrained.sum())} of {capacity} slots"
    )

def test_a_floor_alone_would_not_be_enough():
    """Document why the simple approach fails, as an executable counterexample.

    Reproduces the first rejected design: guarantee each group a proportional minimum,
    then spend what is left purely by score. The leftover re-concentrates and the ratio
    reopens. Kept as a test so nobody "simplifies" the real implementation back into it.
    """
    frame, _ = make_frame(n=6000, seed=39)
    spec = make_spec(max_disparity_ratio=1.25)
    scores = _biased_scores(frame)
    capacity = 600

    selected = pd.Series(False, index=frame.index)
    shares = frame.GROUP_B.value_counts(normalize=True)
    for group, share in shares.items():
        rows = frame.index[frame.GROUP_B == group]
        floor = int(np.floor(capacity * share / spec.fairness.max_disparity_ratio))
        selected.loc[scores.loc[rows].nlargest(floor).index] = True
    leftover = capacity - int(selected.sum())
    if leftover > 0:
        remaining = scores.loc[~selected]
        selected.loc[remaining.nlargest(leftover).index] = True

    floor_only = disparity_report(frame, spec, selected, "GROUP_B").observed_ratio
    proper = disparity_report(
        frame, spec, allocate_with_floor(frame, spec, scores, capacity), "GROUP_B"
    ).observed_ratio

    assert floor_only > spec.fairness.max_disparity_ratio, (
        "the floor-only approach was expected to breach the threshold"
    )
    assert proper <= spec.fairness.max_disparity_ratio
    assert proper < floor_only

def test_constraint_costs_benefit_but_not_catastrophically():
    """Fairness is a tradeoff. Assert it is real and that it is bounded."""
    frame, _ = make_frame(n=6000, seed=40)
    spec = make_spec()
    scores = benefit_scores(spec, frame.TRUE_ITE)

    unconstrained = allocate_top_n(scores, 600)
    constrained = allocate_with_floor(frame, spec, scores, 600)

    best = float(scores[unconstrained].sum())
    fair = float(scores[constrained].sum())

    assert fair <= best + 1e-9, (
        "the constrained policy cannot beat the unconstrained one on score"
    )
    assert fair > 0.5 * best, (
        f"constraint destroyed too much value: {fair:.3f} vs {best:.3f}"
    )
```

### `tests/test_estimators.py`

Copy code

```
"""Do the estimators recover a known answer?

This is the file that justifies having synthetic data at all. Everything else in the
repo can be inspected by reading it; whether AIPW actually removes confounding bias,
and whether its confidence interval is the right WIDTH, can only be established by
running it against data where the answer is known.

The distinction from the calibration checks in ``MODELS.CALIBRATION_CHECKS`` matters:
those assert properties of the synthetic data (that the naive answer is wrong, that
overlap breaks somewhere). These assert properties of the CODE. Break ``dr_ate`` and
the calibration checks still pass, the notebooks still run, and nothing complains.
These tests are what complains.
"""

from __future__ import annotations

import numpy as np
import pytest

from causal_core.causal import dr_ate, fit_propensity, is_identified, overlap_report
from causal_core.naive import raw_difference

from conftest import make_frame, make_spec

# ---------------------------------------------------------------------------
# The naive estimator: wrong, and wrong in a predictable direction
# ---------------------------------------------------------------------------

def test_naive_difference_is_biased_toward_the_confounder():
    """The raw difference must be biased upward when the prognostic factor drives selection.

    Not a tautology about the data: it verifies ``raw_difference`` computes the
    unadjusted contrast rather than accidentally adjusting for anything.
    """
    frame, truth = make_frame(seed=1)
    spec = make_spec()
    result = raw_difference(frame, spec)

    assert result.estimate > truth, (
        "the naive difference should overstate the outcome level of the treated arm, "
        f"got {result.estimate:+.4f} against truth {truth:+.4f}"
    )
    assert abs(result.estimate - truth) > 0.02, (
        "bias is implausibly small; check the DGP"
    )

def test_naive_difference_gets_the_sign_wrong_at_default_settings():
    """The headline claim of the whole recipe, asserted rather than narrated."""
    frame, truth = make_frame(seed=1)
    result = raw_difference(frame, make_spec())

    assert truth < 0, "the planted effect should be beneficial for a minimised outcome"
    assert result.estimate > 0, (
        f"expected the naive estimate to flip sign, got {result.estimate:+.4f}"
    )

def test_naive_confidence_interval_is_too_narrow_to_cover_truth():
    """A deliberately overconfident interval must actually exclude the truth.

    The naive interval reflects sampling noise only, and ignores the far larger
    error from confounding. If this test ever fails, the naive baseline has quietly
    become defensible and the comparison in notebook 01 no longer means anything.
    """
    frame, truth = make_frame(seed=1)
    result = raw_difference(frame, make_spec())

    assert result.ci_low is not None and result.ci_high is not None
    assert not (result.ci_low <= truth <= result.ci_high), (
        f"the naive 95% CI [{result.ci_low:+.4f}, {result.ci_high:+.4f}] should NOT "
        f"cover the truth {truth:+.4f}"
    )

# ---------------------------------------------------------------------------
# AIPW: recovers the effect, and the interval is the right width
# ---------------------------------------------------------------------------

def test_aipw_recovers_the_planted_effect():
    frame, truth = make_frame(n=8000, seed=2)
    result = dr_ate(frame, make_spec())

    assert result.ci_low <= truth <= result.ci_high, (
        f"AIPW 95% CI [{result.ci_low:+.4f}, {result.ci_high:+.4f}] missed the truth "
        f"{truth:+.4f}"
    )

def test_aipw_removes_most_of_the_naive_bias():
    """AIPW error must be a small fraction of naive error on the same data."""
    frame, truth = make_frame(n=8000, seed=3)
    spec = make_spec()

    naive_error = abs(raw_difference(frame, spec).estimate - truth)
    aipw_error = abs(dr_ate(frame, spec).estimate - truth)

    assert aipw_error < 0.25 * naive_error, (
        f"AIPW error {aipw_error:.4f} should be well under a quarter of the naive "
        f"error {naive_error:.4f}"
    )

@pytest.mark.slow
def test_aipw_confidence_interval_coverage_is_near_nominal():
    """Across independent replications, the 95% CI should cover the truth about 95% of the time.

    This is the single most valuable test here, because it checks the STANDARD ERROR
    and not just the point estimate. A point estimate can be right while the interval
    is badly sized, and an interval that is too narrow is how a pipeline produces
    confident, wrong decisions.

    The acceptance band is deliberately wide. With 40 replications the standard error
    on a coverage estimate of 0.95 is about 3.4 percentage points, so anything from
    roughly 0.85 upward is consistent with correct coverage. The test is calibrated to
    catch a genuinely broken standard error, not to police sampling noise.
    """
    replications = 40
    covered = 0
    widths = []

    for seed in range(replications):
        frame, truth = make_frame(n=3000, seed=100 + seed)
        result = dr_ate(frame, make_spec())
        widths.append(result.ci_high - result.ci_low)
        if result.ci_low <= truth <= result.ci_high:
            covered += 1

    coverage = covered / replications
    print(
        f"\nAIPW 95% CI coverage: {coverage:.0%} over {replications} replications "
        f"(median width {np.median(widths):.4f})"
    )
    assert 0.85 <= coverage <= 1.0, (
        f"CI coverage {coverage:.0%} over {replications} replications is outside the "
        "band consistent with a correct 95% interval. Below the band means the "
        "standard error is too small and the pipeline is overconfident."
    )
    # Guard against passing by producing uselessly wide intervals.
    assert float(np.median(widths)) < 0.08, (
        f"median CI width {np.median(widths):.4f} is so wide that coverage is "
        "meaningless; the interval must be informative as well as honest"
    )

def test_aipw_degrades_under_unmeasured_confounding():
    """The assumption the pipeline warns about must actually matter.

    Adding a driver of both treatment and outcome that is absent from the covariate
    set should push the estimate off the truth. If it does not, the covariate set is
    not doing any work and the warnings elsewhere are theatre.
    """
    clean_frame, clean_truth = make_frame(n=8000, seed=4, hidden_confounding=0.0)
    dirty_frame, dirty_truth = make_frame(n=8000, seed=4, hidden_confounding=1.0)
    spec = make_spec()

    clean_error = abs(dr_ate(clean_frame, spec).estimate - clean_truth)
    dirty_error = abs(dr_ate(dirty_frame, spec).estimate - dirty_truth)

    assert dirty_error > clean_error, (
        f"hidden confounding should worsen the estimate: clean error {clean_error:.4f}, "
        f"confounded error {dirty_error:.4f}"
    )

# ---------------------------------------------------------------------------
# Identification: the gate must fire on data that deserves it
# ---------------------------------------------------------------------------

def test_identification_passes_on_well_overlapped_data():
    frame, _ = make_frame(n=6000, seed=5, confounding=0.8)
    propensity = fit_propensity(frame, make_spec())
    identified, reason = is_identified(overlap_report(frame, propensity))

    assert identified, f"well-overlapped data should be identified, got: {reason}"

def test_identification_fails_when_treatment_is_near_deterministic():
    """Push selection hard enough that most treated units have no counterpart.

    The gate must be a property of the data rather than a fixed threshold that
    happens to pass on the bundled fixture.
    """
    frame, _ = make_frame(n=6000, seed=6, confounding=6.0)
    propensity = fit_propensity(frame, make_spec())
    overlap = overlap_report(frame, propensity)
    identified, reason = is_identified(overlap)

    assert not identified, (
        "near-deterministic assignment should fail the identification gate; "
        f"share of treated above 0.95 was {overlap['share_treated_above_0_95']:.3f}"
    )
    assert "0.95" in reason or "propensity" in reason.lower()

def test_identification_fails_with_too_few_treated_units():
    frame, _ = make_frame(n=6000, seed=7)
    spec = make_spec()
    propensity = fit_propensity(frame, spec)

    tiny = frame[(frame.TREAT == 0) | (frame.index < 40)]
    identified, reason = is_identified(overlap_report(tiny, propensity.loc[tiny.index]))

    assert not identified
    assert "treated" in reason.lower()

# ---------------------------------------------------------------------------
# Direction indirection: the same code must serve both signs
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "direction,effect,expected_benefit",
    [
        ("minimize", -0.05, +0.05),
        ("minimize", +0.05, -0.05),
        ("maximize", +0.05, +0.05),
        ("maximize", -0.05, -0.05),
    ],
)
def test_benefit_flips_with_outcome_direction(direction, effect, expected_benefit):
    """The one abstraction the whole framework rests on.

    Every ranking, allocation and equity calculation reads effects through
    ``outcome.benefit``. If this is wrong for one direction, a use case silently
    targets exactly the units it should avoid, and no other test would catch it
    because the code path is identical.
    """
    spec = make_spec(direction=direction)
    assert spec.outcome.benefit(effect) == pytest.approx(expected_benefit)

def test_estimates_agree_after_sign_correction_across_directions():
    """The same data read as minimise and as maximise must give mirrored estimates."""
    frame, truth = make_frame(n=4000, seed=8)

    minimize = dr_ate(frame, make_spec(direction="minimize"))
    maximize = dr_ate(frame, make_spec(direction="maximize"))

    assert minimize.estimate == pytest.approx(maximize.estimate, abs=1e-9), (
        "the raw estimate should not depend on direction; only its interpretation does"
    )
    assert make_spec(direction="minimize").outcome.benefit(
        minimize.estimate
    ) == pytest.approx(
        -make_spec(direction="maximize").outcome.benefit(maximize.estimate)
    )
```

### `tests/test_integration.py`

Copy code

```
"""Is the deployed pipeline wired correctly?

Distinct from test_estimators.py, which asks whether the maths is right. These tests
ask whether the tables, procedures and agent tools that the notebooks, console and
Cortex Agent all depend on actually exist, agree with each other, and refuse when they
should.

All marked ``snowflake``. Skip with:

    pytest tests -m "not snowflake"
"""

from __future__ import annotations

import json

import pytest

pytestmark = pytest.mark.snowflake

REQUIRED_TABLES = [
    "CATE_SCORES",
    "DIAGNOSTICS",
    "ALLOCATION",
    "QINI_CURVE",
    "EQUITY_REPORT",
    "CALIBRATION_CHECKS",
    "SPEC_SNAPSHOT",
]

AGENT_PROCEDURES = [
    "CHECK_IDENTIFICATION",
    "RUN_SCENARIO",
    "OPTIMIZE_ALLOCATION",
    "COMPARE_TARGETING_STRATEGIES",
    "EXPLAIN_ASSUMPTIONS",
]

def _call(session, database, name, args=""):
    raw = session.sql(f"CALL {database}.AGENT.{name}({args})").collect()[0][0]
    return json.loads(raw) if isinstance(raw, str) else raw

# ---------------------------------------------------------------------------
# The contract exists
# ---------------------------------------------------------------------------

def test_all_canonical_data_tables_exist_and_are_populated(live):
    session, spec = live
    rows = session.sql(
        f"""
        SELECT TABLE_NAME, ROW_COUNT FROM {spec.database}.INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA = 'DATA'
        """
    ).collect()
    counts = {r["TABLE_NAME"]: r["ROW_COUNT"] for r in rows}

    for table in ("UNIT", "UNIT_PERIOD", "TREATMENT", "OUTCOME", "CAPACITY"):
        assert table in counts, f"canonical table DATA.{table} is missing"
        assert (counts[table] or 0) > 0, f"DATA.{table} is empty"

@pytest.mark.parametrize("table", REQUIRED_TABLES)
def test_model_output_tables_exist(live, table):
    session, spec = live
    n = session.sql(
        f"SELECT COUNT(*) AS N FROM {spec.database}.MODELS.{table}"
    ).collect()[0]["N"]
    assert n > 0, f"MODELS.{table} is empty; the notebooks have not all been run"

@pytest.mark.parametrize("procedure", AGENT_PROCEDURES)
def test_agent_procedures_are_deployed(live, procedure):
    session, spec = live
    rows = session.sql(
        f"""
        SELECT PROCEDURE_NAME FROM {spec.database}.INFORMATION_SCHEMA.PROCEDURES
        WHERE PROCEDURE_SCHEMA = 'AGENT' AND PROCEDURE_NAME = '{procedure}'
        """
    ).collect()
    assert rows, f"AGENT.{procedure} is not deployed; run framework/deploy_agent.py"

def test_no_stale_procedure_overloads(live):
    """Changing a parameter type creates an overload rather than replacing.

    Two same-named tools with different signatures is a real hazard: the agent picks
    one arbitrarily. This caught exactly that when the cohort argument moved from
    VARIANT to STRING.
    """
    session, spec = live
    rows = session.sql(
        f"""
        SELECT PROCEDURE_NAME, COUNT(*) AS N
        FROM {spec.database}.INFORMATION_SCHEMA.PROCEDURES
        WHERE PROCEDURE_SCHEMA = 'AGENT' GROUP BY PROCEDURE_NAME HAVING COUNT(*) > 1
        """
    ).collect()
    assert not rows, f"duplicate overloads found: {[(r[0], r[1]) for r in rows]}"

def test_calibration_checks_all_pass(live):
    session, spec = live
    rows = session.sql(
        f"SELECT CHECK_NAME, DETAIL FROM {spec.database}.MODELS.CALIBRATION_CHECKS "
        "WHERE NOT PASSED"
    ).collect()
    assert not rows, "failing calibration checks: " + "; ".join(
        f"{r['CHECK_NAME']} ({r['DETAIL']})" for r in rows
    )

# ---------------------------------------------------------------------------
# The agent tools behave
# ---------------------------------------------------------------------------

def test_population_is_identified(live):
    """Must agree with the notebook, which reported an estimate for this population."""
    session, spec = live
    result = _call(session, spec.database, "CHECK_IDENTIFICATION", "''")

    assert result["ok"] is True
    assert result["identified"] is True, (
        f"the agent refuses the full population that notebook 02 estimated: "
        f"{result.get('refusal')}"
    )

def test_null_and_empty_cohort_both_mean_the_whole_population(live):
    """SQL NULL arrives in Python as a truthy sqlNullWrapper, which broke this once."""
    session, spec = live
    from_null = _call(session, spec.database, "CHECK_IDENTIFICATION", "NULL")
    from_empty = _call(session, spec.database, "CHECK_IDENTIFICATION", "''")

    assert from_null.get("n") == from_empty.get("n")
    assert from_null.get("identified") is from_empty.get("identified") is True

def test_unknown_cohort_column_returns_a_helpful_error(live):
    session, spec = live
    result = _call(
        session, spec.database, "CHECK_IDENTIFICATION", """'{"NOT_A_COLUMN": 1}'"""
    )
    assert result["ok"] is False
    assert "NOT_A_COLUMN" in result["error"]
    assert "Available" in result["error"], "the error should list the valid columns"

def test_malformed_cohort_json_is_rejected_cleanly(live):
    session, spec = live
    result = _call(session, spec.database, "CHECK_IDENTIFICATION", "'not json'")
    assert result["ok"] is False
    assert "JSON" in result["error"]

def test_a_cohort_without_common_support_is_refused(live):
    """The behaviour the whole design exists for, asserted against live data."""
    session, spec = live
    cohort = """'{"COMORBIDITY_COUNT": {"min": 7}}'"""
    result = _call(session, spec.database, "CHECK_IDENTIFICATION", cohort)

    assert result["identified"] is False
    assert "refusal" in result
    assert result["share_treated_without_counterpart"] > 0.25
    # The refusal must instruct against the specific wrong behaviour.
    assert "population-level" in result["refusal"]

def test_run_scenario_refuses_before_returning_any_numbers(live):
    """A refusal accompanied by a number invites quoting the number."""
    session, spec = live
    cohort = """'{"COMORBIDITY_COUNT": {"min": 7}}'"""
    result = _call(session, spec.database, "RUN_SCENARIO", f"500, {cohort}, TRUE")

    assert result["refused"] is True
    for forbidden in (
        "expected_net_value",
        "expected_gross_value",
        "roi",
        "program_cost",
    ):
        assert forbidden not in result, (
            f"a refused scenario must not carry '{forbidden}'"
        )

def test_run_scenario_returns_coherent_economics_for_a_valid_cohort(live):
    session, spec = live
    result = _call(session, spec.database, "RUN_SCENARIO", "2000, '', TRUE")

    assert result["refused"] is False
    assert result["units_treated"] == 2000
    assert result["program_cost"] == pytest.approx(2000 * spec.treatment.cost_per_unit)
    assert result["expected_net_value"] == pytest.approx(
        result["expected_gross_value"] - result["program_cost"], rel=1e-6
    )

def test_scenario_value_is_monotone_in_capacity(live):
    """Treating more of a ranked list cannot reduce total benefit."""
    session, spec = live
    small = _call(session, spec.database, "RUN_SCENARIO", "1000, '', FALSE")
    large = _call(session, spec.database, "RUN_SCENARIO", "5000, '', FALSE")

    assert (
        large["expected_events_avoided_or_gained"]
        > small["expected_events_avoided_or_gained"]
    )
    assert large["units_treated"] > small["units_treated"]

def test_optimizer_reports_which_constraint_binds(live):
    session, spec = live
    tight = _call(session, spec.database, "OPTIMIZE_ALLOCATION", "500000.0")
    loose = _call(session, spec.database, "OPTIMIZE_ALLOCATION", "500000000.0")

    assert tight["binding_constraint"] == "budget"
    assert loose["binding_constraint"] == "value"
    assert (
        loose["recommended_units_to_treat"]
        == loose["units_with_positive_expected_value"]
    )
    assert tight["recommended_units_to_treat"] < loose["recommended_units_to_treat"]

def test_targeting_comparison_reports_signed_auuc(live):
    session, spec = live
    result = _call(session, spec.database, "COMPARE_TARGETING_STRATEGIES")
    rankings = {r["model"]: r for r in result["rankings_evaluated"]}

    assert len(rankings) >= 2, (
        "both the uplift and the risk ranking must be persisted, or the agent can only "
        "hedge when asked whether risk targeting works"
    )
    assert any(r["auuc"] > 0 for r in rankings.values())
    assert any(r["auuc"] < 0 for r in rankings.values()), (
        "the risk ranking should score below random on this fixture"
    )

# ---------------------------------------------------------------------------
# The surfaces agree with each other
# ---------------------------------------------------------------------------

def test_agent_economics_match_the_persisted_scores(live):
    """The consistency guarantee: the procedure must not recompute differently.

    If the agent's arithmetic ever diverges from MODELS.CATE_SCORES, a number in chat
    stops matching the same number in the console and the notebook.
    """
    session, spec = live
    result = _call(session, spec.database, "RUN_SCENARIO", "3000, '', FALSE")

    expected = session.sql(
        f"""
        SELECT SUM(BENEFIT) AS TOTAL_BENEFIT
        FROM (
            SELECT BENEFIT FROM {spec.database}.MODELS.CATE_SCORES
            ORDER BY BENEFIT DESC LIMIT 3000
        )
        """
    ).collect()[0]["TOTAL_BENEFIT"]

    assert result["expected_events_avoided_or_gained"] == pytest.approx(
        float(expected), rel=1e-4
    )

def test_spec_snapshot_matches_the_spec_on_disk(live):
    """The console reads the snapshot. Drift between it and the YAML would be silent."""
    session, spec = live
    row = (
        session.sql(
            f"SELECT * FROM {spec.database}.MODELS.SPEC_SNAPSHOT ORDER BY SNAPSHOT_AT DESC LIMIT 1"
        )
        .collect()[0]
        .as_dict()
    )

    assert row["USECASE"] == spec.name
    assert row["OUTCOME_DIRECTION"] == spec.outcome.direction
    assert float(row["COST_PER_UNIT"]) == pytest.approx(spec.treatment.cost_per_unit)
    assert float(row["MAX_DISPARITY_RATIO"]) == pytest.approx(
        spec.fairness.max_disparity_ratio
    )
    assert row["PROTECTED_ATTRIBUTES"] == ",".join(spec.fairness.protected_attributes)

def test_equity_gate_result_is_persisted_and_passing(live):
    """Notebook 03 writes the CONSTRAINED policy, which must satisfy the threshold."""
    session, spec = live
    rows = session.sql(
        f"""
        SELECT ATTRIBUTE, MAX(OBSERVED_RATIO) AS RATIO, MAX(THRESHOLD) AS THRESHOLD,
               MIN(IFF(PASSED, 1, 0)) AS PASSED
        FROM {spec.database}.MODELS.EQUITY_REPORT GROUP BY ATTRIBUTE
        """
    ).collect()

    assert rows, "no equity report persisted"
    for row in rows:
        assert row["PASSED"] == 1, (
            f"{row['ATTRIBUTE']} ratio {row['RATIO']:.3f} exceeds "
            f"{row['THRESHOLD']:.3f} on the gated policy"
        )

def test_diagnostics_contain_both_the_naive_and_the_adjusted_estimate(live):
    """The comparison the use case turns on must be present and pointing opposite ways."""
    session, spec = live
    rows = session.sql(
        f"SELECT METHOD, ESTIMATE FROM {spec.database}.MODELS.DIAGNOSTICS"
    ).collect()
    estimates = {r["METHOD"]: float(r["ESTIMATE"]) for r in rows}

    naive = next(v for k, v in estimates.items() if "raw" in k.lower())
    adjusted = next(v for k, v in estimates.items() if "robust" in k.lower())

    assert (naive > 0) != (adjusted > 0), (
        f"naive ({naive:+.4f}) and doubly-robust ({adjusted:+.4f}) should disagree in "
        "sign on this fixture; that disagreement is the entire point of notebook 01"
    )

# ---------------------------------------------------------------------------
# Refutation, in the isolated dowhy environment
# ---------------------------------------------------------------------------

def test_analysis_view_exists_and_matches_the_unit_count(live):
    """The dowhy procedure reads this view because it cannot import causal_core."""
    session, spec = live
    view_rows = session.sql(
        f"SELECT COUNT(*) AS N FROM {spec.models('V_ANALYSIS_FRAME')}"
    ).collect()[0]["N"]
    unit_rows = session.sql(f"SELECT COUNT(*) AS N FROM {spec.data('UNIT')}").collect()[
        0
    ]["N"]
    assert view_rows == unit_rows, "the analysis view should be one row per unit"

def test_refutation_procedure_is_deployed_in_its_own_environment(live):
    session, spec = live
    rows = session.sql(
        f"""
        SELECT PROCEDURE_NAME FROM {spec.database}.INFORMATION_SCHEMA.PROCEDURES
        WHERE PROCEDURE_SCHEMA = 'AGENT' AND PROCEDURE_NAME = 'REFUTE_ESTIMATE'
        """
    ).collect()
    assert rows, "AGENT.REFUTE_ESTIMATE is not deployed; run framework/deploy_agent.py"

@pytest.mark.slow
def test_refutation_runs_and_the_placebo_collapses(live):
    """The placebo test is the one that would catch a spurious result.

    If a permuted treatment still produces an effect of the same magnitude, the
    pipeline is detecting something other than the treatment, and every downstream
    number is worthless. Asserting it collapses is asserting the estimate is at least
    attached to the treatment variable.
    """
    from causal_core.refute import refute

    session, spec = live
    # 15,000 / 10 rather than a smaller, faster configuration: the placebo estimate is
    # an average over permutations, each carrying the same standard error as the real
    # estimate, so at 8,000 rows with 6 simulations its own noise breached the bound
    # intermittently. That was a flaky test, not a flaky pipeline.
    result = refute(session, spec, sample_size=15000, num_simulations=10)

    assert result["ok"] is True
    assert result["tests_errored"] == 0, f"tests errored: {result['results']}"
    assert result["tests_failed"] == 0, f"tests failed: {result['results']}"

    placebo = next(r for r in result["results"] if r["test"] == "placebo_treatment")
    assert abs(placebo["new_estimate"]) < 0.40 * abs(result["base_estimate"]), (
        f"placebo effect {placebo['new_estimate']:+.5f} did not collapse relative to "
        f"the real estimate {result['base_estimate']:+.5f}"
    )

@pytest.mark.slow
def test_refutation_reports_the_primary_estimate_for_comparison(live):
    """The linear adjustment differs from the doubly-robust figure; that must be visible."""
    from causal_core.refute import refute

    session, spec = live
    result = refute(session, spec, sample_size=15000, num_simulations=10)

    assert result["primary_estimate_from_diagnostics"] is not None
    assert result["estimator_comparison"] is not None
    # Both must at least agree on the direction of the effect.
    assert (result["base_estimate"] > 0) == (
        result["primary_estimate_from_diagnostics"] > 0
    ), (
        "the refutation estimator and the primary estimator disagree on the SIGN, "
        "which is a substantive problem rather than an estimator-choice detail"
    )

@pytest.mark.slow
def test_refutation_verdict_never_claims_proof(live):
    """Guard the wording. A refutation that reads as certification is misleading."""
    from causal_core.refute import refute

    session, spec = live
    result = refute(session, spec, sample_size=15000, num_simulations=10)

    text = (result["verdict"] + " " + result["how_to_read"]).lower()
    assert "not proof" in text or "cannot certify" in text
    for overclaim in (
        "proves",
        "confirms the estimate is correct",
        "validates the estimate",
    ):
        assert overclaim not in text, f"verdict overclaims with '{overclaim}'"
```

### `tests/test_spec.py`

Copy code

```
"""Spec validation guards.

The spec is the contract. A typo in a column name should fail at load time with a
message naming the problem, not surface three notebooks later as a KeyError inside a
model fit. These tests assert each guard actually fires, because a validation function
that silently accepts bad input is worse than none: it creates the impression of
safety.
"""

from __future__ import annotations

import pytest

from causal_core.spec import SpecError, UseCaseSpec, available_usecases, load_spec

from conftest import make_spec

def _valid_dict() -> dict:
    """Round-trip a known-good spec back to a dict so each test can corrupt one field."""
    return {
        "name": "unit_test",
        "label": "Unit test use case",
        "database": "TEST_DB",
        "warehouse": "TEST_WH",
        "unit": {
            "id_column": "UNIT_ID",
            "label_singular": "widget",
            "label_plural": "widgets",
        },
        "treatment": {
            "column": "TREATED_FLAG",
            "label": "the intervention",
            "cost_per_unit": 500,
        },
        "outcome": {
            "primary": {
                "column": "OUTCOME_RATE",
                "type": "continuous",
                "direction": "minimize",
                "label": "outcome rate",
                "value_per_event": 10_000,
                "pre_column": "OUTCOME_RATE_PRE",
                "panel_column": "OUTCOME_EVENT",
            }
        },
        "covariates": {"observed": ["X1", "X2", "GROUP_A"], "categorical": ["GROUP_A"]},
        "fairness": {"protected_attributes": ["GROUP_A"], "max_disparity_ratio": 1.25},
        "panel": {
            "period_column": "PERIOD_START",
            "period_grain": "month",
            "pre_periods": 12,
            "post_periods": 12,
        },
        "capacity": {"group_column": "GROUP_A", "slots_column": "SLOTS"},
        "calibration": {
            "true_ate_relative": 0.2,
            "naive_bias_direction": "positive",
            "overlap_breaks_above_percentile": 98,
        },
    }

def test_the_known_good_spec_loads():
    """Guard against tests that pass only because everything raises."""
    spec = UseCaseSpec.from_dict(_valid_dict())
    assert spec.name == "unit_test"
    assert spec.outcome.direction == "minimize"

# Verified against the implementation rather than assumed: `label` and `warehouse`
# are the only top-level keys with defaults.
REQUIRED_KEYS = [
    "name",
    "database",
    "unit",
    "treatment",
    "outcome",
    "covariates",
    "fairness",
    "panel",
    "capacity",
    "calibration",
]
OPTIONAL_KEYS = ["label", "warehouse"]

@pytest.mark.parametrize("key", REQUIRED_KEYS)
def test_missing_required_key_is_rejected(key):
    payload = _valid_dict()
    del payload[key]
    with pytest.raises(SpecError, match=key):
        UseCaseSpec.from_dict(payload)

@pytest.mark.parametrize("key", OPTIONAL_KEYS)
def test_optional_key_falls_back_to_a_default(key):
    """These two may be omitted. Asserted so the distinction stays deliberate."""
    payload = _valid_dict()
    del payload[key]
    spec = UseCaseSpec.from_dict(payload)
    assert getattr(spec, key), f"{key} should have fallen back to a non-empty default"

def test_categorical_covariate_must_also_be_declared_observed():
    """The guard that catches the most common real mistake.

    Listing a column as categorical but forgetting it in `observed` means it silently
    never reaches the model, and the estimate is confounded by a variable the author
    believed was controlled for.
    """
    payload = _valid_dict()
    payload["covariates"]["categorical"] = ["GROUP_A", "NOT_OBSERVED"]
    with pytest.raises(SpecError, match="NOT_OBSERVED"):
        UseCaseSpec.from_dict(payload)

def test_invalid_outcome_direction_is_rejected():
    payload = _valid_dict()
    payload["outcome"]["primary"]["direction"] = "optimise"
    with pytest.raises(SpecError, match="direction"):
        UseCaseSpec.from_dict(payload)

def test_negative_treatment_cost_is_rejected():
    payload = _valid_dict()
    payload["treatment"]["cost_per_unit"] = -10
    with pytest.raises(SpecError):
        UseCaseSpec.from_dict(payload)

def test_disparity_ratio_below_one_is_rejected():
    """A ratio under 1.0 is unsatisfiable by construction, since it is max over min."""
    payload = _valid_dict()
    payload["fairness"]["max_disparity_ratio"] = 0.8
    with pytest.raises(SpecError):
        UseCaseSpec.from_dict(payload)

def test_zero_post_periods_is_rejected():
    payload = _valid_dict()
    payload["panel"]["post_periods"] = 0
    with pytest.raises(SpecError):
        UseCaseSpec.from_dict(payload)

# ---------------------------------------------------------------------------
# Derived behaviour
# ---------------------------------------------------------------------------

def test_sign_and_benefit_are_consistent():
    assert make_spec("minimize").outcome.sign == -1
    assert make_spec("maximize").outcome.sign == +1
    for direction in ("minimize", "maximize"):
        outcome = make_spec(direction).outcome
        assert outcome.benefit(0.0) == 0.0
        assert outcome.benefit(1.0) == pytest.approx(outcome.sign)

def test_canonical_table_helper_rejects_domain_specific_names():
    """Framework code must not be able to reach a domain-specific table by accident."""
    spec = make_spec()
    assert spec.data("UNIT").endswith(".DATA.UNIT")
    with pytest.raises(SpecError, match="canonical"):
        spec.data("MEMBER_ENROLLMENT")

def test_total_periods_is_pre_plus_post():
    spec = make_spec()
    assert spec.panel.total_periods == spec.panel.pre_periods + spec.panel.post_periods

# ---------------------------------------------------------------------------
# The bundled use cases must stay valid
# ---------------------------------------------------------------------------

def test_every_bundled_usecase_loads_and_validates():
    """Cheap protection against a spec edit that breaks a use case nobody ran."""
    cases = available_usecases()
    assert "payer_care_management" in cases
    assert "subscription_churn" in cases

    for name in cases:
        spec = load_spec(name)
        assert spec.name == name
        assert spec.database.startswith("COOKBOOK_AGENT_CAUSAL_GROUNDING")
        assert spec.warehouse.startswith("COOKBOOK_")
        assert spec.outcome.direction in {"minimize", "maximize"}
        assert spec.fairness.protected_attributes, (
            f"{name} declares no protected attributes"
        )

def test_bundled_usecases_cover_both_outcome_directions():
    """The abstraction is only proven if something actually exercises both signs."""
    directions = {load_spec(n).outcome.direction for n in available_usecases()}
    assert directions == {"minimize", "maximize"}, (
        f"bundled use cases only cover {directions}; the direction indirection is "
        "untested end to end without both"
    )
```

## `usecases/`

### `usecases/_template/03_bring_your_own_data.sql`

Copy code

```
-- =====================================================================
-- 03_bring_your_own_data.sql  -  TEMPLATE
--
-- This is the adoption path. It maps tables you ALREADY HAVE onto the five
-- canonical objects, as views. No data is copied, nothing is regenerated, and
-- the synthetic generator is not involved at all.
--
-- HOW TO USE
--   1. Copy this file into your use case directory.
--   2. Find and replace every  <<PLACEHOLDER>>  with your own object names.
--   3. Run 01_contract.sql first if you want the documented empty tables as a
--      reference, then DROP them before creating the views below (a view cannot
--      share a name with a table).
--   4. Run this file.
--   5. Verify with the Python contract check at the bottom.
--
-- WHY VIEWS RATHER THAN TABLES
--   Nothing in the framework writes to the DATA schema, it only reads. Views
--   mean zero data movement, zero storage, zero refresh pipeline, and your
--   governance policies on the underlying tables continue to apply. If a query
--   turns out to be slow, swap any view for a dynamic table without changing a
--   line of Python.
--
-- WHAT TO DELETE
--   The TRUTH schema and everything that reads it. It holds a planted answer key
--   that only exists for synthetic data. Concretely:
--       DROP SCHEMA IF EXISTS <<YOUR_DB>>.TRUTH;
--   and in the notebooks, stop passing include_truth=True and skip the
--   Leaderboard sections. Those are synthetic scaffolding. See docs/design.md for the
--   full list of what is scaffolding and what is product.
-- =====================================================================

SET cookbook_wh = 'COOKBOOK_AGENT_CAUSAL_GROUNDING_WH';
USE WAREHOUSE IDENTIFIER($cookbook_wh);

CREATE DATABASE IF NOT EXISTS <<YOUR_DB>>;
CREATE SCHEMA IF NOT EXISTS <<YOUR_DB>>.DATA;
CREATE SCHEMA IF NOT EXISTS <<YOUR_DB>>.MODELS;
CREATE SCHEMA IF NOT EXISTS <<YOUR_DB>>.AGENT;
CREATE SCHEMA IF NOT EXISTS <<YOUR_DB>>.APP;
-- Deliberately NO TRUTH schema. There is no answer key for real data.

USE SCHEMA <<YOUR_DB>>.DATA;

-- ---------------------------------------------------------------------
-- The one decision you have to make first: WHEN DOES TREATMENT START?
--
-- Everything else follows from it. Pick a single index date that splits the
-- panel into a pre-treatment window and a post-treatment window.
--
-- Use a FIXED date for everyone rather than each unit's own treatment date.
-- Indexing on each unit's own start date sounds more precise but introduces
-- immortal time bias: untreated units have no start date, so you end up
-- comparing windows that were selected differently for the two arms.
--
-- If your program rolled out gradually, restrict to a cohort enrolled within one
-- window and use that window's midpoint.
-- ---------------------------------------------------------------------
SET TREATMENT_START = '2025-01-01'::DATE;
SET PERIOD_GRAIN    = 'month';        -- must match panel.period_grain in usecase.yaml
SET PRE_PERIODS     = 12;             -- must match panel.pre_periods
SET POST_PERIODS    = 12;             -- must match panel.post_periods

-- ---------------------------------------------------------------------
-- UNIT: one row per decision subject. TIME-INVARIANT attributes only.
--
-- If an attribute changes over time, it does not belong here. Put it in
-- UNIT_PERIOD, otherwise you risk describing a unit using a value recorded
-- AFTER treatment, which quietly invalidates the whole estimate.
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW <<YOUR_DB>>.DATA.UNIT AS
SELECT
    m.<<MEMBER_KEY>>            AS <<UNIT_ID_COLUMN>>,
    m.<<AGE_COL>>               AS AGE,
    m.<<SEX_COL>>               AS SEX,
    m.<<REGION_COL>>            AS REGION,
    m.<<PLAN_TYPE_COL>>         AS INSURANCE_TYPE,
    -- Derived attributes are fine here as long as they use only pre-treatment
    -- information.
    NTILE(5) OVER (ORDER BY m.<<DEPRIVATION_COL>>) AS DEPRIVATION_QUINTILE,
    m.<<DEPRIVATION_COL>>       AS DEPRIVATION_INDEX
FROM <<YOUR_SOURCE_DB>>.<<YOUR_SOURCE_SCHEMA>>.<<MEMBER_TABLE>> m
-- Restrict to the population the program was actually eligible for. Including
-- ineligible units inflates the control arm with people who were never
-- candidates, which biases every estimate.
WHERE m.<<ELIGIBILITY_FLAG>> = TRUE;

-- ---------------------------------------------------------------------
-- UNIT_PERIOD: the panel.
--
-- PERIOD_INDEX and IS_PRE are the two columns the framework requires by name.
-- PERIOD_INDEX must be 0-based and ascending in time. IS_PRE marks periods
-- before $TREATMENT_START.
--
-- The covariates here are snapshotted automatically at the LAST pre-treatment
-- period. You do not need to build that snapshot yourself.
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW <<YOUR_DB>>.DATA.UNIT_PERIOD AS
WITH calendar AS (
    -- One row per period spanning the full window.
    SELECT
        DATEADD($PERIOD_GRAIN, SEQ8() - $PRE_PERIODS, $TREATMENT_START) AS PERIOD_START,
        SEQ8()::INT                                                     AS PERIOD_INDEX
    FROM TABLE(GENERATOR(ROWCOUNT => 24))   -- = PRE_PERIODS + POST_PERIODS
)
SELECT
    u.<<UNIT_ID_COLUMN>>,
    c.PERIOD_START,
    c.PERIOD_INDEX,
    (c.PERIOD_START < $TREATMENT_START)  AS IS_PRE,

    -- Time-varying covariates, aggregated to the period grain. Use LEFT JOIN and
    -- COALESCE so a unit with no utilization in a period gets 0 rather than
    -- dropping out of the panel. A unit that silently disappears from some
    -- periods will break the diff-in-differences balance.
    COALESCE(util.ADMITS_TRAILING_6M, 0)      AS PRIOR_ADMITS_6M,
    COALESCE(util.ED_VISITS_TRAILING_3M, 0)   AS ED_VISITS_3M,
    COALESCE(rx.ACTIVE_MED_COUNT, 0)          AS MED_COUNT,
    COALESCE(util.OP_VISITS_TRAILING_6M, 0)   AS OUTPATIENT_VISITS_6M,

    -- The outcome PER PERIOD. Declared as outcome.primary.panel_column.
    COALESCE(util.<<READMIT_FLAG>>, 0)        AS READMIT_90D,
    COALESCE(cost.<<PERIOD_SPEND>>, 0)        AS PERIOD_COST
FROM <<YOUR_DB>>.DATA.UNIT u
CROSS JOIN calendar c
LEFT JOIN <<YOUR_SOURCE_DB>>.<<YOUR_SOURCE_SCHEMA>>.<<UTILIZATION_MONTHLY>> util
       ON util.<<MEMBER_KEY>> = u.<<UNIT_ID_COLUMN>>
      AND util.<<MONTH_COL>>  = c.PERIOD_START
LEFT JOIN <<YOUR_SOURCE_DB>>.<<YOUR_SOURCE_SCHEMA>>.<<PHARMACY_MONTHLY>> rx
       ON rx.<<MEMBER_KEY>>   = u.<<UNIT_ID_COLUMN>>
      AND rx.<<MONTH_COL>>    = c.PERIOD_START
LEFT JOIN <<YOUR_SOURCE_DB>>.<<YOUR_SOURCE_SCHEMA>>.<<CLAIMS_MONTHLY>> cost
       ON cost.<<MEMBER_KEY>> = u.<<UNIT_ID_COLUMN>>
      AND cost.<<MONTH_COL>>  = c.PERIOD_START;

-- ---------------------------------------------------------------------
-- TREATMENT: who was treated.
--
-- Keep this thin. Anything explaining WHY a unit was treated is either a
-- covariate, in which case put it in UNIT or UNIT_PERIOD so the propensity model
-- can use it, or it is unobserved, in which case no method can adjust for it and
-- your estimate carries bias that only a sensitivity analysis can bound.
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW <<YOUR_DB>>.DATA.TREATMENT AS
SELECT
    u.<<UNIT_ID_COLUMN>>,
    -- The name must match treatment.column in usecase.yaml.
    (e.<<MEMBER_KEY>> IS NOT NULL)  AS TREATED,
    e.<<ENROLL_DATE>>               AS TREATMENT_PERIOD
FROM <<YOUR_DB>>.DATA.UNIT u
LEFT JOIN <<YOUR_SOURCE_DB>>.<<YOUR_SOURCE_SCHEMA>>.<<PROGRAM_ENROLLMENT>> e
       ON e.<<MEMBER_KEY>> = u.<<UNIT_ID_COLUMN>>
      -- Count only enrollments in the intended window. Someone enrolled two
      -- years earlier is a different intervention and does not belong in this
      -- comparison.
      AND e.<<ENROLL_DATE>> BETWEEN $TREATMENT_START
                                AND DATEADD($PERIOD_GRAIN, 3, $TREATMENT_START);

-- ---------------------------------------------------------------------
-- OUTCOME: unit-level outcomes, plus their pre-treatment values.
--
-- Aggregating from UNIT_PERIOD rather than from source guarantees the unit-level
-- outcome and the per-period outcome are the same measure. Computing them from
-- two different queries is an easy way to have diff-in-differences and AIPW
-- silently estimating different things.
--
-- The _PRE columns enable the pre-period placebo test: run the estimator on the
-- pre-treatment outcome and it should find nothing. If it finds an effect, the
-- design is broken and no result from it should be trusted.
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW <<YOUR_DB>>.DATA.OUTCOME AS
SELECT
    p.<<UNIT_ID_COLUMN>>,
    AVG(IFF(NOT p.IS_PRE, p.READMIT_90D, NULL))  AS READMIT_RATE_12M,
    AVG(IFF(p.IS_PRE,     p.READMIT_90D, NULL))  AS READMIT_RATE_12M_PRE,
    SUM(IFF(NOT p.IS_PRE, p.PERIOD_COST, 0))     AS TOTAL_COST_12M,
    SUM(IFF(p.IS_PRE,     p.PERIOD_COST, 0))     AS TOTAL_COST_12M_PRE
FROM <<YOUR_DB>>.DATA.UNIT_PERIOD p
GROUP BY 1;

-- ---------------------------------------------------------------------
-- CAPACITY: the binding constraint.
--
-- Without this you have a ranking, not a decision. If you have no staffing
-- table, a constant is fine and honest: what matters is that the number
-- reflects how many units can actually be treated.
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW <<YOUR_DB>>.DATA.CAPACITY AS
SELECT
    s.<<REGION_COL>>     AS REGION,
    s.<<MONTH_COL>>      AS PERIOD_START,
    DATEDIFF($PERIOD_GRAIN, DATEADD($PERIOD_GRAIN, -$PRE_PERIODS, $TREATMENT_START), s.<<MONTH_COL>>) AS PERIOD_INDEX,
    s.<<NURSE_FTE>> * <<CASES_PER_NURSE_PER_PERIOD>>  AS NURSE_SLOTS
FROM <<YOUR_SOURCE_DB>>.<<YOUR_SOURCE_SCHEMA>>.<<STAFFING_MONTHLY>> s;

-- Simpler alternative when you have no staffing data:
--
-- CREATE OR REPLACE VIEW <<YOUR_DB>>.DATA.CAPACITY AS
-- SELECT REGION,
--        DATEADD('month', SEQ8() - 12, $TREATMENT_START) AS PERIOD_START,
--        SEQ8()::INT                                     AS PERIOD_INDEX,
--        200                                             AS NURSE_SLOTS
-- FROM (SELECT DISTINCT REGION FROM <<YOUR_DB>>.DATA.UNIT)
-- CROSS JOIN TABLE(GENERATOR(ROWCOUNT => 24));

-- =====================================================================
-- VERIFY
--
-- These sanity checks catch the mistakes that actually happen. Run them before
-- trusting any estimate.
-- =====================================================================

-- 1. Both arms exist and are large enough to compare.
SELECT TREATED, COUNT(*) AS UNITS
FROM <<YOUR_DB>>.DATA.TREATMENT
GROUP BY 1;

-- 2. Every unit has a complete panel. Any count below the expected total means
--    units are dropping out of some periods, which breaks diff-in-differences.
SELECT N_PERIODS, COUNT(*) AS UNITS
FROM (
    SELECT <<UNIT_ID_COLUMN>>, COUNT(*) AS N_PERIODS
    FROM <<YOUR_DB>>.DATA.UNIT_PERIOD GROUP BY 1
)
GROUP BY 1 ORDER BY 1;

-- 3. Pre-treatment trends. The treated-minus-control gap should be roughly FLAT
--    before treatment and then step. If it was already moving, the parallel
--    trends assumption fails and the diff-in-differences result is not usable.
SELECT
    p.PERIOD_INDEX,
    ANY_VALUE(p.IS_PRE)                                            AS IS_PRE,
    AVG(IFF(t.TREATED, p.READMIT_90D, NULL))                       AS TREATED_RATE,
    AVG(IFF(NOT t.TREATED, p.READMIT_90D, NULL))                   AS CONTROL_RATE,
    AVG(IFF(t.TREATED, p.READMIT_90D, NULL))
      - AVG(IFF(NOT t.TREATED, p.READMIT_90D, NULL))               AS GAP
FROM <<YOUR_DB>>.DATA.UNIT_PERIOD p
JOIN <<YOUR_DB>>.DATA.TREATMENT t USING (<<UNIT_ID_COLUMN>>)
GROUP BY 1 ORDER BY 1;

-- 4. Full contract check, including that every column named in usecase.yaml
--    exists. This is the authoritative one:
--
--    from causal_core import load_spec, get_session, validate_tables
--    spec = load_spec()
--    print(validate_tables(get_session(spec), spec))
--
--    It raises DataError listing exactly what is missing. Once it passes, run
--    notebooks/01 through 03 unchanged.
```

### `usecases/_template/usecase.yaml`

Copy code

```
# =====================================================================
# Use case template. Copy this directory, rename it, and fill this in.
#
#   cp -r usecases/_template usecases/my_case
#
# The directory name and the `name` field below must match.
#
# Your job is to answer six questions:
#   1. What is the unit a decision is made about?
#   2. What intervention are we considering, and what does it cost?
#   3. What outcome do we care about, which direction is good, what is an
#      event worth in dollars?
#   4. What was measured BEFORE the intervention that might confound it?
#   5. Which groups must not be quietly deprioritized?
#   6. What is the binding constraint on how many units we can treat?
#
# Then write generate_data.sql producing the five canonical tables, or point
# the spec at real tables that already have that shape. See
# docs/adding-a-use-case.md.
# =====================================================================

name: my_case                      # must equal the directory name
label: "Human readable name"
database: COOKBOOK_AGENT_CAUSAL_GROUNDING_MY_CASE  # one database per use case, never shared
warehouse: COOKBOOK_AGENT_CAUSAL_GROUNDING_WH

# 1. The decision subject: member, customer, subscriber, store, device, asset.
unit:
  id_column: UNIT_KEY
  label_singular: customer
  label_plural: customers

# 2. The intervention. cost_per_unit is the fully loaded cost of treating one
#    unit once, in the same currency as outcome.value_per_event.
treatment:
  # The boolean column in DATA.TREATMENT that marks treated units. The
  # template's 03_bring_your_own_data.sql names it TREATED.
  column: TREATED
  label: "the intervention, in plain words"
  cost_per_unit: 100

# 3. Outcomes.
#
#    direction is the field that keeps the framework domain-blind. Use
#    "minimize" when a smaller number is better (churn, readmission, defects)
#    and "maximize" when larger is better (revenue, conversion, retention).
#    Framework code multiplies by the resulting sign rather than assuming.
#
#    value_per_event converts an effect into money. Required on the primary
#    outcome if you want dollar-denominated allocation. For a binary outcome it
#    is the value of preventing (or causing) one event. For a continuous
#    outcome set it to 1 when the outcome is already in currency.
#
#    pre_column is the same measure over the pre-treatment window. Optional,
#    but without it diff-in-diff falls back to the panel and you lose a
#    cross-check.
outcome:
  primary:
    column: PRIMARY_OUTCOME
    type: binary                   # binary | continuous
    direction: minimize            # minimize | maximize
    label: "what this measures"
    value_per_event: 1000
    pre_column: PRIMARY_OUTCOME_PRE
  # secondary is optional. Useful when a clinical and a financial audience want
  # different units, or when an effect is real on cost but not significant on
  # the headline metric.
  # secondary:
  #   column: SECONDARY_OUTCOME
  #   type: continuous
  #   direction: minimize
  #   label: "..."

# 4. Confounders. Everything here MUST be measured before treatment.
#
#    Do not list the treatment, either outcome, or the period column: the spec
#    validator rejects all three, because conditioning on them destroys the
#    estimate.
#
#    You do not declare where a column lives. The framework looks each one up
#    in UNIT and UNIT_PERIOD and builds the right join. Time-varying columns
#    are snapshotted at the last pre-treatment period automatically.
covariates:
  observed:
    - COVARIATE_A
    - COVARIATE_B
    - COVARIATE_C
  categorical:                     # subset of observed; one-hot encoded
    - COVARIATE_C

# 5. Fairness. This cannot be empty.
#
#    Uplift targeting systematically favors units that are easier to reach,
#    which correlates with advantage. Left unchecked that produces a model that
#    withholds help from the people who need it most. The gate FAILS the
#    pipeline when the ratio of treatment rates across any protected group
#    exceeds max_disparity_ratio.
fairness:
  protected_attributes:
    - PROTECTED_A
  max_disparity_ratio: 1.25

# 6. Panel shape. pre_periods >= 2 so a pre-trend check means something.
panel:
  period_column: PERIOD_START
  period_grain: month              # month | week | day | quarter
  pre_periods: 12
  post_periods: 12

# 7. The binding constraint. Without this you have a ranking, not a decision.
capacity:
  group_column: GROUP_KEY
  slots_column: SLOTS

# 8. Calibration, for synthetic use cases only.
#
#    These are asserted at the end of generate_data.sql. They exist so the synthetic
#    data proves something: a naive analysis must reach a clearly wrong conclusion,
#    and the causal estimate must recover the planted truth. If the naive
#    estimate happens to be right, retune the generator, not the estimator.
#
#    Pointing this use case at real data instead? Delete this block and remove
#    the assertion section from generate_data.sql. Nothing else changes, and
#    grading against truth simply becomes unavailable.
calibration:
  true_ate_relative: -0.20         # true effect as a relative change
  naive_bias_direction: positive   # which way the naive estimate is wrong
  overlap_breaks_above_percentile: 98
```

### `usecases/payer_care_management/01_contract.sql`

Copy code

```
-- =====================================================================
-- 01_contract.sql  -  payer care management
--
-- READ THIS FILE FIRST. It is the whole contract, and it is short.
--
-- Every use case in this framework supplies exactly five tables in its DATA
-- schema. This file creates them, empty, with a comment on every column. That
-- makes the contract executable documentation rather than prose: if this file
-- runs, the framework can consume the use case.
--
-- The five tables and what they mean:
--
--   UNIT         one row per thing a decision is made about (here, a member)
--   UNIT_PERIOD  panel: one row per unit per period
--   TREATMENT    who received the intervention, and when
--   OUTCOME      outcome per unit, plus its pre-treatment value
--   CAPACITY     the binding constraint, by group and period
--
-- Nothing in framework/causal_core references any of the column names below.
-- It learns them from usecase.yaml. That is why swapping domains does not
-- require touching Python.
--
-- ---------------------------------------------------------------------
-- WHICH FILE DO I RUN?
--
--   Synthetic, with fabricated data and a known answer key:
--       01_contract.sql  then  02_generate_synthetic.sql
--
--   Real data, mapped from tables you already have:
--       01_contract.sql  then  03_bring_your_own_data.sql
--       (and delete the TRUTH schema; see that file)
--
-- 02_generate_synthetic.sql is SYNTHETIC SCAFFOLDING. It is roughly 900 lines of
-- data fabrication and calibration checking, and none of it is needed to run
-- this framework against real data. Do not read it to understand the contract.
-- =====================================================================

-- Names. Must match `database` and `warehouse` in usecase.yaml.
SET cookbook_db = 'COOKBOOK_AGENT_CAUSAL_GROUNDING';
SET cookbook_wh = 'COOKBOOK_AGENT_CAUSAL_GROUNDING_WH';

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
    WITH WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 120 AUTO_RESUME = TRUE
    COMMENT = 'Causal decision framework';

CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db)
    COMMENT = 'Causal decision framework - payer care management use case';

-- Schema names are FIXED by the framework so code never has to guess. Only the
-- database name varies between use cases, which is what guarantees two use
-- cases can never collide.
USE DATABASE IDENTIFIER($cookbook_db);

CREATE SCHEMA IF NOT EXISTS DATA
    COMMENT = 'The five canonical tables. Only what an analyst could actually see.';
CREATE SCHEMA IF NOT EXISTS TRUTH
    COMMENT = 'SYNTHETIC SCAFFOLDING. The planted answer key. Does not exist with real data - delete this schema.';
CREATE SCHEMA IF NOT EXISTS MODELS
    COMMENT = 'Estimator outputs: CATE scores, diagnostics, calibration checks.';
CREATE SCHEMA IF NOT EXISTS AGENT
    COMMENT = 'Agent tool procedures and semantic view.';
CREATE SCHEMA IF NOT EXISTS APP
    COMMENT = 'Streamlit scenario console.';

USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA DATA;

-- ---------------------------------------------------------------------
-- UNIT: one row per decision subject, time-invariant attributes only.
--
-- Anything that changes over time belongs in UNIT_PERIOD, not here.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS DATA.UNIT (
    MEMBER_ID                STRING  NOT NULL
        COMMENT 'Unit identifier. Declared as unit.id_column in usecase.yaml.',
    AGE                      INT
        COMMENT 'Covariate. Pre-treatment.',
    SEX                      STRING
        COMMENT 'Covariate, categorical.',
    REGION                   STRING
        COMMENT 'Covariate, categorical. Also capacity.group_column: capacity is constrained per region.',
    INSURANCE_TYPE           STRING
        COMMENT 'Covariate, categorical. Also a fairness.protected_attributes entry.',
    PRIMARY_CONDITION        STRING
        COMMENT 'Covariate, categorical.',
    DEPRIVATION_INDEX        FLOAT
        COMMENT 'Covariate. Area social deprivation, 0-100.',
    DEPRIVATION_QUINTILE     INT
        COMMENT 'A fairness.protected_attributes entry. Not used as a model covariate.',
    COMORBIDITY_COUNT        INT
        COMMENT 'Covariate. Chronic condition count.',
    PRIOR_OUTREACH_ANSWERED  FLOAT
        COMMENT 'Covariate, and the EFFECT MODIFIER. Share of past outreach attempts answered. Barely moves readmission risk on its own, but strongly determines whether the program can help. Without a variable like this the treatment effect collapses into a restatement of baseline risk and causal estimation earns nothing over a plain outcome model on ranking.',
    CONSTRAINT PK_UNIT PRIMARY KEY (MEMBER_ID)
)
COMMENT = 'CANONICAL. One row per member. Time-invariant attributes only.';

-- ---------------------------------------------------------------------
-- UNIT_PERIOD: the panel. One row per unit per period.
--
-- Two jobs. First, it holds time-varying covariates, which the framework
-- snapshots at the LAST PRE-TREATMENT period. That snapshot is what keeps
-- post-treatment information out of the covariate set, which is the most common
-- way a causal estimate is silently destroyed.
--
-- Second, it carries the outcome per period, which is what makes
-- difference-in-differences available as an independent check.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS DATA.UNIT_PERIOD (
    MEMBER_ID             STRING     NOT NULL
        COMMENT 'Joins to UNIT.',
    PERIOD_START          DATE       NOT NULL
        COMMENT 'REQUIRED. Declared as panel.period_column. Start of the period.',
    PERIOD_INDEX          INT        NOT NULL
        COMMENT 'REQUIRED, fixed name. 0-based and ascending in time. The framework picks the covariate snapshot with MAX(PERIOD_INDEX) among pre-treatment rows.',
    IS_PRE                BOOLEAN    NOT NULL
        COMMENT 'REQUIRED, fixed name. TRUE for periods before treatment began.',
    PRIOR_ADMITS_6M       INT     COMMENT 'Time-varying covariate.',
    ED_VISITS_3M          INT     COMMENT 'Time-varying covariate.',
    MED_COUNT             INT     COMMENT 'Time-varying covariate.',
    OUTPATIENT_VISITS_6M  INT     COMMENT 'Time-varying covariate.',
    READMIT_90D           INT
        COMMENT 'The outcome PER PERIOD. Declared as outcome.primary.panel_column. Diff-in-differences needs this; the unit-level OUTCOME table aggregates it.',
    PERIOD_COST           FLOAT   COMMENT 'Per-period spend, aggregated into the secondary outcome.',
    CONSTRAINT PK_UNIT_PERIOD PRIMARY KEY (MEMBER_ID, PERIOD_INDEX)
)
COMMENT = 'CANONICAL. Panel. Time-varying covariates plus the per-period outcome.';

-- ---------------------------------------------------------------------
-- TREATMENT: who was treated.
--
-- Deliberately thin. Anything about WHY a unit was treated is either a
-- covariate (put it in UNIT or UNIT_PERIOD so the propensity model can use it)
-- or unobserved (in which case no method can adjust for it, and your estimate
-- carries bias you should quantify with a sensitivity analysis).
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS DATA.TREATMENT (
    MEMBER_ID         STRING   NOT NULL COMMENT 'Joins to UNIT.',
    TREATED           BOOLEAN  NOT NULL
        COMMENT 'REQUIRED. Named by treatment.column in usecase.yaml.',
    TREATMENT_PERIOD  DATE
        COMMENT 'When treatment began. NULL for untreated units.',
    CONSTRAINT PK_TREATMENT PRIMARY KEY (MEMBER_ID)
)
COMMENT = 'CANONICAL. One row per unit. Treatment assignment.';

-- ---------------------------------------------------------------------
-- OUTCOME: unit-level outcomes, plus their pre-treatment counterparts.
--
-- The _PRE columns are what make a pre-period placebo test possible: run the
-- same estimator on the pre-treatment outcome and it should find nothing. If it
-- finds an effect, the design is broken.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS DATA.OUTCOME (
    MEMBER_ID             STRING  NOT NULL COMMENT 'Joins to UNIT.',
    READMIT_RATE_12M      FLOAT
        COMMENT 'PRIMARY outcome. Annualized readmission rate: mean of 12 monthly indicators. Continuous on purpose - a one-shot binary at a ~20% base rate does not carry enough information per member to estimate per-member effects at any realistic panel size.',
    READMIT_RATE_12M_PRE  FLOAT
        COMMENT 'Same measure over the pre-treatment window. Declared as outcome.primary.pre_column.',
    READMIT_90D           INT
        COMMENT 'Single-period flag. Kept because it is the more legible number to quote to a business audience, but far too noisy to estimate on.',
    READMIT_90D_PRE       INT     COMMENT 'Pre-treatment counterpart.',
    TOTAL_COST_12M        FLOAT   COMMENT 'SECONDARY outcome. Post-window spend.',
    TOTAL_COST_12M_PRE    FLOAT   COMMENT 'Pre-treatment counterpart.',
    CONSTRAINT PK_OUTCOME PRIMARY KEY (MEMBER_ID)
)
COMMENT = 'CANONICAL. One row per unit. Outcomes and their pre-treatment values.';

-- ---------------------------------------------------------------------
-- CAPACITY: the binding constraint.
--
-- Without this you have a ranking, not a decision. The allocation layer needs
-- to know how many units can actually be treated, by group and period.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS DATA.CAPACITY (
    REGION        STRING  NOT NULL
        COMMENT 'Declared as capacity.group_column.',
    PERIOD_START  DATE    NOT NULL COMMENT 'Period this capacity applies to.',
    PERIOD_INDEX  INT     COMMENT 'Convenience join key.',
    NURSE_SLOTS   INT
        COMMENT 'Declared as capacity.slots_column. Units treatable in this group and period.',
    CONSTRAINT PK_CAPACITY PRIMARY KEY (REGION, PERIOD_START)
)
COMMENT = 'CANONICAL. Treatment capacity by group and period.';

-- ---------------------------------------------------------------------
-- Verify the contract is satisfiable.
--
-- The Python equivalent, which also checks every column named in usecase.yaml
-- actually exists, is:
--     from causal_core import load_spec, get_session, validate_tables
--     validate_tables(get_session(load_spec()), load_spec())
-- ---------------------------------------------------------------------
SELECT TABLE_NAME, ROW_COUNT, COMMENT
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'DATA'
ORDER BY TABLE_NAME;
```

### `usecases/payer_care_management/02_generate_synthetic.sql`

Synthetic-data generator (893 lines). It’s in [agent-causal-grounding.zip](/static/samples/cortex-ai-cookbook/agent-causal-grounding.zip) only, to keep this page readable.

### `usecases/payer_care_management/copy.yaml`

Copy code

```
# Narrative strings for the Streamlit console and the agent's responses.
#
# Kept separate from usecase.yaml because this is presentation, not structure.
# The app falls back to spec labels when a key is absent, so this file is
# optional and partial overrides are fine.

headline: "Your risk model tells you who will be readmitted. It cannot tell you who you can help."

subtitle: >
  Same nurses, same budget, a different list of members. This compares targeting
  by risk score against targeting by estimated impact, on data where the true
  answer is known.

analogy: >
  A risk model is a list of which houses are most likely to burn. But a house
  already fully engulfed cannot be saved by sending a truck, and a concrete
  house with sprinklers was never going to burn. You want the houses where
  sending a truck changes the outcome.

# Shown above the naive result, before the reveal.
naive_framing: >
  This is the comparison most program evaluations actually run: readmission
  rates for enrolled members against everyone else. Read literally, it says the
  care management program is making members worse.

naive_warning: >
  It says that because sicker members are the ones who get referred. The
  comparison is measuring who was enrolled, not what enrollment did.

causal_framing: >
  Adjusting for who was likely to be referred recovers the real effect. Two
  methods with different assumptions are run side by side, because agreement
  between them is far more convincing than one small p-value.

allocation_framing: >
  Ranking is not a decision. With a fixed number of nurse slots, the question is
  which members to enroll. These are the same slots allocated three different
  ways.

equity_framing: >
  Members who are easier to reach look more impactable, and reachability tracks
  advantage. Left unchecked, targeting by impact quietly withholds help from the
  people who need it most. This check fails the pipeline rather than warning.

equity_citation: >
  This is the failure mode documented in Obermeyer et al., Science 2019, which
  found a widely deployed commercial care-management algorithm under-referred
  Black patients because it used healthcare spending as a proxy for illness.

refusal_framing: >
  Above the 98th risk percentile nearly every member was enrolled, so there is
  no comparable untreated group. No honest effect estimate exists there. The
  agent is required to say so instead of producing a number.

# Units for the scenario console.
units:
  outcome_event: "readmission"
  outcome_events: "readmissions"
  treatment_verb: "enroll"
  treatment_noun: "enrollment"
  capacity_noun: "nurse slot"
  capacity_noun_plural: "nurse slots"

# Suggested prompts for the agent, surfaced in the app.
example_questions:
  - "What happens if we enroll 2000 more members next quarter?"
  - "Compare targeting by risk score against targeting by estimated impact."
  - "Which region gets the most value from 500 additional nurse slots?"
  - "What is the effect for members above the 98th risk percentile?"
  - "Does the recommended allocation disadvantage Medicaid or dual-eligible members?"
  - "How confident are you, and what would change your answer?"
```

### `usecases/payer_care_management/usecase.yaml`

Copy code

```
# =====================================================================
# Payer care management: the first instance of the framework.
#
# Question: a health plan runs a nurse-led care management program with a
# fixed number of nurses. Today it targets the highest-risk members. Should
# it? And if not, who should it target instead?
#
# This file is the source of truth. Framework code reads it; no Python
# contains any of these names.
# =====================================================================

name: payer_care_management
label: "Payer care management"
database: COOKBOOK_AGENT_CAUSAL_GROUNDING
warehouse: COOKBOOK_AGENT_CAUSAL_GROUNDING_WH

unit:
  id_column: MEMBER_ID
  label_singular: member
  label_plural: members

treatment:
  # The boolean column in DATA.TREATMENT that marks treated units.
  column: TREATED
  label: "care management enrollment"
  # Fully loaded cost of enrolling one member for the program year: nurse time,
  # outreach, care plan maintenance. Drives cost-per-outcome-avoided.
  cost_per_unit: 480

outcome:
  primary:
    # Annualized rate: the mean of 12 monthly 90-day-readmission indicators.
    #
    # Deliberately continuous rather than a single binary flag. A one-shot binary
    # outcome at a ~20% base rate carries so little information per member that
    # per-member effect estimation is not statistically feasible at any realistic
    # panel size: a causal forest fitted on it honestly reports that it cannot
    # rank anyone, which kills the targeting story. Averaging 12 periods cuts the
    # noise by roughly a factor of 3.5 and is also how plans actually report
    # readmission performance.
    column: READMIT_RATE_12M
    type: continuous
    direction: minimize
    label: "annualized 90-day readmission rate"
    # Average marginal cost the plan bears per readmission. Turns an effect
    # estimate into dollars so allocation can be compared against budget.
    value_per_event: 14200
    pre_column: READMIT_RATE_12M_PRE
    # Diff-in-diff needs the per-period measure this rate aggregates.
    panel_column: READMIT_90D
  secondary:
    column: TOTAL_COST_12M
    type: continuous
    direction: minimize
    label: "total cost of care, 12 month"
    pre_column: TOTAL_COST_12M_PRE

# All measured strictly before the enrollment window. AGE, SEX, REGION,
# INSURANCE_TYPE, PRIMARY_CONDITION and DEPRIVATION_* are time-invariant and
# live on UNIT. The utilization counts are time-varying and live on
# UNIT_PERIOD, snapshotted at the last pre-treatment period.
covariates:
  observed:
    - AGE
    - SEX
    - COMORBIDITY_COUNT
    - PRIMARY_CONDITION
    - INSURANCE_TYPE
    - REGION
    - DEPRIVATION_INDEX
    - PRIOR_ADMITS_6M
    - ED_VISITS_3M
    - MED_COUNT
    - OUTPATIENT_VISITS_6M
    # Effect modifier: share of past outreach attempts the member answered. Barely
    # affects readmission risk on its own, but strongly determines whether the
    # program can help. Must be listed here or no model can find it.
    - PRIOR_OUTREACH_ANSWERED
  categorical:
    - SEX
    - PRIMARY_CONDITION
    - INSURANCE_TYPE
    - REGION

# Targeting by impactability can quietly deprioritize members with less social
# support, because they are harder to reach and therefore look less movable.
# This is the failure mode documented in the 2019 Science study of a commercial
# care-management algorithm. The gate fails the pipeline; it does not warn.
fairness:
  protected_attributes:
    - INSURANCE_TYPE
    - DEPRIVATION_QUINTILE
  max_disparity_ratio: 1.25

panel:
  period_column: PERIOD_START
  period_grain: month
  pre_periods: 12
  post_periods: 12

# Nurse capacity varies by region and month. That variation is what creates
# comparable members on either side of the enrollment decision.
capacity:
  group_column: REGION
  slots_column: NURSE_SLOTS

# Targets the generator must hit, asserted at the end of 02_generate_synthetic.sql.
# naive estimate is not clearly wrong, retune the generator rather than the
# estimator: the synthetic data proves nothing without this.
calibration:
  # True average effect: 18% baseline readmission down to 14%.
  true_ate_relative: -0.22
  # Sicker members are preferentially enrolled, so the raw comparison makes the
  # program look actively harmful.
  naive_bias_direction: positive
  # Above this risk percentile there is effectively no untreated comparison
  # group, so no honest estimate exists. The agent must refuse here.
  overlap_breaks_above_percentile: 98
```

### `usecases/subscription_churn/01_contract.sql`

Copy code

```
-- =====================================================================
-- 01_contract.sql  -  subscription churn
--
-- The same five canonical objects as the payer use case, with completely
-- different columns. Compare this file against
-- usecases/payer_care_management/01_contract.sql: the table names, the required
-- columns (PERIOD_INDEX, IS_PRE, TREATED) and the schema layout are identical,
-- and nothing else is shared.
--
-- Run this, then 02_generate_synthetic.sql.
-- =====================================================================

-- Names. Must match `database` and `warehouse` in usecase.yaml.
SET cookbook_db = 'COOKBOOK_AGENT_CAUSAL_GROUNDING_CHURN';
SET cookbook_wh = 'COOKBOOK_AGENT_CAUSAL_GROUNDING_WH';

CREATE WAREHOUSE IF NOT EXISTS IDENTIFIER($cookbook_wh)
    WITH WAREHOUSE_SIZE = 'XSMALL' AUTO_SUSPEND = 120 AUTO_RESUME = TRUE
    COMMENT = 'Causal decision framework';

CREATE DATABASE IF NOT EXISTS IDENTIFIER($cookbook_db)
    COMMENT = 'Causal decision framework - subscription retention use case';

USE DATABASE IDENTIFIER($cookbook_db);

CREATE SCHEMA IF NOT EXISTS DATA
    COMMENT = 'The five canonical objects. Only what an analyst could actually see.';
CREATE SCHEMA IF NOT EXISTS TRUTH
    COMMENT = 'SYNTHETIC SCAFFOLDING. Planted answer key. Delete for real data.';
CREATE SCHEMA IF NOT EXISTS MODELS
    COMMENT = 'Estimator outputs: CATE scores, diagnostics, calibration checks.';
CREATE SCHEMA IF NOT EXISTS AGENT
    COMMENT = 'Agent tool procedures and semantic view.';
CREATE SCHEMA IF NOT EXISTS APP
    COMMENT = 'Streamlit scenario console.';

USE WAREHOUSE IDENTIFIER($cookbook_wh);
USE SCHEMA DATA;

-- ---------------------------------------------------------------------
-- UNIT
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS DATA.UNIT (
    SUBSCRIBER_ID        STRING NOT NULL
        COMMENT 'Unit identifier. Declared as unit.id_column.',
    TENURE_MONTHS        INT    COMMENT 'Covariate. Months since signup at the index date.',
    PLAN_TIER            STRING COMMENT 'Covariate, categorical. BASIC | STANDARD | PREMIUM.',
    CONTRACT_TYPE        STRING COMMENT 'Covariate, categorical. MONTHLY | ANNUAL.',
    ACQUISITION_CHANNEL  STRING COMMENT 'Covariate, categorical.',
    MARKET               STRING
        COMMENT 'Covariate, categorical. Also capacity.group_column and a fairness.protected_attributes entry: offer budget is set per market.',
    MONTHLY_PRICE        FLOAT  COMMENT 'Covariate. Current monthly price.',
    PRICE_SENSITIVITY    FLOAT
        COMMENT 'Covariate, and the EFFECT MODIFIER. 0-1. A discount moves a price-sensitive subscriber a lot and an insensitive one barely at all, while only weakly predicting churn on its own. Without a variable like this the treatment effect collapses into a restatement of churn risk and causal estimation earns nothing over a plain outcome model on ranking.',
    PRICE_TIER_QUINTILE  INT
        COMMENT 'A fairness.protected_attributes entry. Not used as a model covariate.',
    CONSTRAINT PK_UNIT PRIMARY KEY (SUBSCRIBER_ID)
)
COMMENT = 'CANONICAL. One row per subscriber. Time-invariant attributes only.';

-- ---------------------------------------------------------------------
-- UNIT_PERIOD
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS DATA.UNIT_PERIOD (
    SUBSCRIBER_ID         STRING  NOT NULL COMMENT 'Joins to UNIT.',
    PERIOD_START          DATE    NOT NULL COMMENT 'REQUIRED. Declared as panel.period_column.',
    PERIOD_INDEX          INT     NOT NULL
        COMMENT 'REQUIRED, fixed name. 0-based, ascending in time. Covariates are snapshotted at MAX(PERIOD_INDEX) among pre-treatment rows.',
    IS_PRE                BOOLEAN NOT NULL
        COMMENT 'REQUIRED, fixed name. TRUE for periods before the offer window.',
    SESSIONS_30D          INT     COMMENT 'Time-varying covariate. Product engagement.',
    SUPPORT_TICKETS_30D   INT     COMMENT 'Time-varying covariate.',
    PAYMENT_FAILURES_90D  INT     COMMENT 'Time-varying covariate. Strong involuntary-churn signal.',
    FEATURES_USED         INT     COMMENT 'Time-varying covariate. Breadth of product adoption.',
    ACTIVE                INT
        COMMENT 'The outcome PER PERIOD, 1 if subscribed this month. Declared as outcome.primary.panel_column. Drawn independently per period rather than as a survival process, so a subscriber can lapse and return; that keeps the planted effect exactly comparable to the estimand. A true time-to-event outcome would need a different estimator (see docs/design.md, known limits).',
    PERIOD_REVENUE        FLOAT   COMMENT 'ACTIVE * MONTHLY_PRICE. Aggregated into the secondary outcome.',
    CONSTRAINT PK_UNIT_PERIOD PRIMARY KEY (SUBSCRIBER_ID, PERIOD_INDEX)
)
COMMENT = 'CANONICAL. Panel. Time-varying covariates plus the per-period outcome.';

-- ---------------------------------------------------------------------
-- TREATMENT
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS DATA.TREATMENT (
    SUBSCRIBER_ID     STRING  NOT NULL COMMENT 'Joins to UNIT.',
    TREATED           BOOLEAN NOT NULL
        COMMENT 'REQUIRED. Named by treatment.column in usecase.yaml. TRUE if a retention offer was sent.',
    TREATMENT_PERIOD  DATE    COMMENT 'When the offer was sent. NULL if none.',
    CONSTRAINT PK_TREATMENT PRIMARY KEY (SUBSCRIBER_ID)
)
COMMENT = 'CANONICAL. One row per subscriber. Offer assignment.';

-- ---------------------------------------------------------------------
-- OUTCOME
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS DATA.OUTCOME (
    SUBSCRIBER_ID        STRING NOT NULL COMMENT 'Joins to UNIT.',
    ACTIVE_RATE_12M      FLOAT
        COMMENT 'PRIMARY outcome. Share of the 12 post-window months active. Direction is MAXIMIZE.',
    ACTIVE_RATE_12M_PRE  FLOAT  COMMENT 'Same measure over the pre-window. Enables a pre-period placebo test.',
    REVENUE_12M          FLOAT  COMMENT 'SECONDARY outcome. Post-window revenue.',
    REVENUE_12M_PRE      FLOAT  COMMENT 'Pre-window counterpart.',
    CHURNED_12M          INT
        COMMENT 'Legible binary: inactive for the final three months. Not used as a spec outcome because it is too noisy to estimate per-subscriber effects on.',
    CONSTRAINT PK_OUTCOME PRIMARY KEY (SUBSCRIBER_ID)
)
COMMENT = 'CANONICAL. One row per subscriber. Outcomes and their pre-treatment values.';

-- ---------------------------------------------------------------------
-- CAPACITY
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS DATA.CAPACITY (
    MARKET              STRING NOT NULL COMMENT 'Declared as capacity.group_column.',
    PERIOD_START        DATE   NOT NULL COMMENT 'Period this budget applies to.',
    PERIOD_INDEX        INT    COMMENT 'Convenience join key.',
    OFFER_BUDGET_UNITS  INT
        COMMENT 'Declared as capacity.slots_column. Offers fundable in this market and period.',
    CONSTRAINT PK_CAPACITY PRIMARY KEY (MARKET, PERIOD_START)
)
COMMENT = 'CANONICAL. Offer budget by market and period.';

SELECT TABLE_NAME, ROW_COUNT, COMMENT
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'DATA'
ORDER BY TABLE_NAME;
```

### `usecases/subscription_churn/02_generate_synthetic.sql`

Synthetic-data generator (602 lines). It’s in [agent-causal-grounding.zip](/static/samples/cortex-ai-cookbook/agent-causal-grounding.zip) only, to keep this page readable.

### `usecases/subscription_churn/usecase.yaml`

Copy code

```
# =====================================================================
# Subscription churn: the SECOND instance of the framework.
#
# This exists to test whether the abstraction actually holds. It is a
# deliberately different shape from payer care management:
#
#   - the outcome direction is MAXIMIZE, not minimize, so every sign in the
#     framework is exercised in the opposite direction
#   - the treatment is a discount, not a service, so cost per unit is large
#     relative to the effect and the average intervention LOSES money
#   - the units, covariates, capacity grouping and protected attributes share
#     nothing with the payer case
#
# If this runs all three notebooks with no changes under framework/, the
# framework claim is real. If it needs even one, it is not.
#
# Question: a subscription business sends retention offers to customers a churn
# model flags as at-risk. Should it? And if not, who should get them?
# =====================================================================

name: subscription_churn
label: "Subscription retention offers"
database: COOKBOOK_AGENT_CAUSAL_GROUNDING_CHURN
warehouse: COOKBOOK_AGENT_CAUSAL_GROUNDING_WH

unit:
  id_column: SUBSCRIBER_ID
  label_singular: subscriber
  label_plural: subscribers

treatment:
  # The boolean column in DATA.TREATMENT that marks treated units.
  column: TREATED
  label: "retention offer"
  # A one-time $25 account credit.
  #
  # Sized so the program is genuinely MARGINAL: break-even needs an effect of
  # 25/504 = 0.050 on the active rate, against a true average effect of 0.068. So
  # roughly half of subscribers are worth treating and choosing which half is the
  # entire decision. That is the opposite of the payer case, where almost any
  # prevented readmission pays for the intervention many times over.
  #
  # An earlier version used $60. That is defensible on its own terms, but it put
  # break-even at an effect of 0.119, and because unobserved confounding attenuates
  # the ESTIMATED effects, not one subscriber out of 80,000 cleared the bar. The
  # honest recommendation became "cancel the programme", which is a real finding but
  # leaves nothing to allocate.
  #
  # Lesson worth carrying to other use cases: size the intervention cost against
  # the typical ESTIMATED effect, not the true one. Attenuation moves break-even.
  cost_per_unit: 25

outcome:
  primary:
    # Share of the 12 post-period months the subscriber was active. Continuous
    # for the same reason as the payer case: a single churned-yes-no flag does
    # not carry enough information per subscriber to estimate per-subscriber
    # effects. See docs/adding-a-use-case.md on statistical power.
    column: ACTIVE_RATE_12M
    type: continuous
    # MAXIMIZE. This is the important difference from the payer use case: it
    # forces every sign convention in the framework through the opposite branch.
    direction: maximize
    label: "share of months active"
    # Annual revenue from a subscriber active all 12 months, so an effect of
    # +0.05 on the active rate is worth 0.05 * 504 = $25.20.
    value_per_event: 504
    pre_column: ACTIVE_RATE_12M_PRE
    panel_column: ACTIVE

  secondary:
    column: REVENUE_12M
    type: continuous
    direction: maximize
    label: "revenue over 12 months"
    pre_column: REVENUE_12M_PRE

# All measured before the offer window. TENURE, PLAN_TIER, CONTRACT_TYPE,
# ACQUISITION_CHANNEL, MARKET, MONTHLY_PRICE and PRICE_SENSITIVITY are
# time-invariant and live on UNIT. The engagement measures are time-varying and
# live on UNIT_PERIOD, snapshotted at the last pre-treatment period.
covariates:
  observed:
    - TENURE_MONTHS
    - PLAN_TIER
    - CONTRACT_TYPE
    - ACQUISITION_CHANNEL
    - MARKET
    - MONTHLY_PRICE
    - SESSIONS_30D
    - SUPPORT_TICKETS_30D
    - PAYMENT_FAILURES_90D
    - FEATURES_USED
    # Effect modifier. A discount moves a price-sensitive subscriber a lot and a
    # price-insensitive one barely at all, while price sensitivity itself is only
    # a weak predictor of churn, because people leave for many reasons. That is
    # exactly the shape a pure effect modifier needs: large effect on the effect,
    # small effect on the outcome level.
    - PRICE_SENSITIVITY
  categorical:
    - PLAN_TIER
    - CONTRACT_TYPE
    - ACQUISITION_CHANNEL
    - MARKET

# Commercial rather than legal fairness, but the mechanic is identical: does the
# recommended policy systematically abandon a segment? Targeting by uplift tends
# to favour high-value subscribers, and "we quietly stopped trying to retain
# anyone on the cheapest plan" is a decision a business should make on purpose
# rather than discover in a model.
fairness:
  protected_attributes:
    - MARKET
    - PRICE_TIER_QUINTILE
  max_disparity_ratio: 1.30

panel:
  period_column: PERIOD_START
  period_grain: month
  pre_periods: 12
  post_periods: 12

# Offer budget is set per market, so capacity binds differently from the payer
# case where it was nurse headcount per region.
capacity:
  group_column: MARKET
  slots_column: OFFER_BUDGET_UNITS

calibration:
  # POSITIVE, because the outcome is maximized. The payer case targets -0.22.
  true_ate_relative: 0.08
  # Offers go to subscribers a churn model already flagged, so offer recipients
  # look WORSE than everyone else and the naive estimate comes out negative while
  # the truth is positive. Mirror image of the payer case.
  naive_bias_direction: negative
  overlap_breaks_above_percentile: 98
```

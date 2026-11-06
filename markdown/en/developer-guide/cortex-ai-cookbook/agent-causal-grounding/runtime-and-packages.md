# Causally grounded Cortex Agent that refuses when the data cannot answer: Runtime and packages

Part of the [Causally grounded Cortex Agent that refuses when the data cannot answer](/developer-guide/cortex-ai-cookbook/agent-causal-grounding) recipe.

Everything here was established by execution rather than read from
documentation. `sql/00_verify_packages.sql` reproduces the package claims in your
own account.

## The two hard constraints

### 1. Snowflake warehouse Python is aarch64

Confirmed from a failing source build, which emitted paths like
`build/lib.linux-aarch64-cpython-311/`.

Consequence: any package without an aarch64 `manylinux` wheel will attempt a
source build inside the warehouse, and will usually fail. This is not a
theoretical concern. It is what rules out `econml` from PyPI and `causalml`
entirely.

To use an x86-only package in a warehouse you need
`RESOURCE_CONSTRAINT=(architecture='x86')` on a Snowpark-optimized warehouse.
This framework deliberately avoids needing that.

### 2. dowhy and econml cannot coexist

| Package | numpy requirement |
| --- | --- |
| `dowhy==0.14` | `numpy>2.0` |
| `econml==0.15.x` | `numpy<2` |

Expand

Show lessSee more

The resolver rejects the combination outright at `CREATE PROCEDURE` time:

```
Because dowhy==0.14 depends on numpy>2.0 and econml==0.15.1 depends on
numpy<2, we can conclude that dowhy==0.14 and econml==0.15.1 are
incompatible.
```

This is not fixable by pinning an older dowhy without giving up its current
refutation API, and it applies equally to a container runtime notebook, which
would hit the same conflict on `pip install`.

## What follows from that

The two libraries are separated by process boundary, and communicate through
tables rather than through memory.

```
econml world (numpy 1.26)          dowhy world (numpy 2.4)
Anaconda channel                   PyPI artifact repository
- notebooks 01, 02, 03             - AGENT.REFUTE_ESTIMATE proc only
- agent tool procs                        |
- Streamlit app                           |
        |                                 |
        +---------> MODELS tables <-------+
```

`framework/causal_core/refute.py` is therefore a **thin client**. It does not
import dowhy. It calls the procedure and parses the result. That is the only
sane way to use both libraries in one project.

A useful side effect: because dowhy is encapsulated as a SQL-callable
procedure, the core path needs no compute pool and no SPCS at all. Every layer
runs on a plain XSMALL warehouse, which makes the pattern portable to any
account.

## Package source matrix

| Package | Source | Why |
| --- | --- | --- |
| `econml` 0.15.0 | Anaconda channel | Only place with a working aarch64 build |
| `dowhy` 0.14 | PyPI artifact repository | Pure-Python `py3-none-any` wheel, trivial to install |
| `statsmodels` 0.14.6 | Anaconda channel | Diff-in-diff cross-check |
| `scikit-learn` 1.4.2 | Anaconda channel | Nuisance models |
| `causalml` | Not used | See below |

Expand

Show lessSee more

### Why causalml was rejected

Two independent reasons, either sufficient.

**Low marginal value.** Its meta-learners and causal trees overlap almost
entirely with econml, which is already available at zero install cost. The
genuinely useful parts, Qini and AUUC, are short to implement and belong in SQL
anyway so the app and the agent can share one definition.

**Real friction.** PyPI ships wheels only for `win_amd64`,
`manylinux_x86_64`, and `macosx_arm64`, on cp311 and cp312 only. There is no
`manylinux aarch64` wheel, so a warehouse install would need a
Snowpark-optimized x86 warehouse. It is available on `CPU_X64_*` SPCS pools if
you ever want it, but paying that cost for capability already in hand is a bad
trade.

## Version drift between the two paths

The same import name gives materially different versions depending on source:

| Package | Anaconda | PyPI artifact repo |
| --- | --- | --- |
| numpy | 1.26.4 | 2.4.6 |
| pandas | 2.3.3 | 3.0.5 |
| scikit-learn | 1.4.2 | 1.9.1 |
| statsmodels | 0.14.6 | 0.15.0 |

Expand

Show lessSee more

pandas 2.x versus 3.x is a major-version gap. Never pass a pickled model or a
serialized estimator between the two paths. Pass data through tables. The
architecture above already enforces this, but it is worth knowing why.

Artifact Repository freezes version resolution at `CREATE` time, so a procedure
keeps working even as PyPI moves. Pin explicitly anyway.

## Gotchas found while building

**Reuse the identified estimand.** `CausalModel.estimate_effect()` mutates the
estimand it is handed, setting `identifier_method`. Passing a freshly
identified estimand to `refute_estimate()` fails with:

```
AttributeError: 'NoneType' object has no attribute 'startswith'
  at placebo_treatment_refuter.py, target_estimand.identifier_method.startswith("iv")
```

Identify once, then reuse that same object for both estimation and refutation.

**dowhy is loud.** It logs heavily at INFO. Set
`logging.getLogger("dowhy").setLevel(logging.ERROR)` at module scope in any
procedure that uses it.

**`log_metrics` rejects bools.** Snowflake ML Experiments returns
`Metrics JSON does not match expected format (400002)` for boolean values, and
`isinstance(True, int)` is `True` in Python, so a naive numeric filter leaks
them. Use `isinstance(v, (int, float)) and not isinstance(v, bool)`.

**Keep agent tool output small.** A large tool result is expensive for the
orchestrator to read and risks being cut short. Tool procedures return compact
summaries and write full detail to a table.

**Streamlit in Snowflake is Anaconda-only.** Artifact Repository is explicitly
unsupported there, so the app cannot import dowhy. It reads tables and calls
procedures.

## Prerequisites in a new account

Copy code

```
-- Usually already granted to PUBLIC by default.
GRANT DATABASE ROLE SNOWFLAKE.PYPI_REPOSITORY_USER TO ROLE <role>;
```

Then run `sql/00_verify_packages.sql` and confirm both checks return `OK`
before running any use case setup.

## The isolated dowhy procedure: what it cost

Building `AGENT.REFUTE_ESTIMATE` surfaced one constraint not in the package matrix.

**`to_pandas()` and `write_pandas()` do not work in an `ARTIFACT_REPOSITORY`
environment**, even though pandas itself arrives as a dowhy dependency. Both go through
the connector’s pyarrow bridge, which is absent:

```
ProgrammingError: 255002: Optional dependency: 'pandas' is not installed
```

Misleading message: pandas *is* importable; it is the arrow bridge that is missing.
Adding `pyarrow` to `PACKAGES` would mean another pin to keep compatible with
`numpy>=2` for no benefit. Instead:

| Instead of | Use |
| --- | --- |
| `session.sql(...).to_pandas()` | `pd.DataFrame([r.as_dict() for r in ....collect()])` |
| `session.write_pandas(df, ...)` | `session.create_dataframe(rows, schema=cols).write.mode("overwrite").save_as_table(...)` |

Expand

Show lessSee more

Neither touches arrow. Worth reaching for by default in any `ARTIFACT_REPOSITORY`
procedure rather than discovering it at run time.

**Sampling should be deterministic.** `ORDER BY HASH(id) LIMIT n` rather than
`SAMPLE()`, so re-running reproduces the verdict. A refutation result that changes
between runs is not usable as evidence.

**Placebo thresholds must account for their own noise.** The placebo estimate is an
average over `num_simulations` permutations, each carrying roughly the same standard
error as the real estimate. At 8,000 rows with 6 simulations that noise alone breached a
20% bound intermittently and produced spurious failures. Use `sample_size >= 15000` and
`num_simulations >= 10`; a genuinely non-collapsing placebo sits near 100%, so a looser
bound costs no detection power.

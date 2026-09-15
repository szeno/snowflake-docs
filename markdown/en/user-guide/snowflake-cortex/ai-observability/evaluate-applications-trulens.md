# Evaluate applications with TruLens

Use this topic when you run **batch evaluations** on a **custom AI application** (agent, RAG pipeline, AI workflow, and similar) instrumented with **TruLens**. Evaluations invoke your app against a dataset, store traces, and compute LLM-as-a-judge metrics (such as context relevance, groundedness, and correctness).

Before you start, instrument and register the application as described in [Trace and monitor applications with TruLens](/user-guide/snowflake-cortex/ai-observability/trace-applications-trulens).

Note

For **Cortex Agent** evaluations (Snowsight **Evaluations** tab, GPA metrics, `EXECUTE_AI_EVALUATION`), see [Cortex Agent evaluations](/user-guide/snowflake-cortex/cortex-agents-evaluations).

## Evaluation workflow

1. Build and instrument the app with TruLens.
2. Register the app in Snowflake (`TruApp` or a framework wrapper).
3. Create a **run** with a dataset and metric list.
4. Invoke the run to generate outputs and traces.
5. Compute metrics and review results in Snowsight (or query with SQL).

## Map span attributes for metrics

To compute metrics during a run, assign function parameters to span attributes with `@instrument()`. Required attributes per metric are listed in [Evaluation metrics](/user-guide/snowflake-cortex/ai-observability/reference#label-ai-observability-evaluation-metrics).

Supported attributes by span type:

- `RECORD_ROOT`: `INPUT`, `OUTPUT`, `GROUND_TRUTH_OUTPUT`
- `RETRIEVAL`: `QUERY_TEXT`, `RETRIEVED_CONTEXTS`
- `GENERATION`: None

Copy code

```
from trulens.otel.semconv.trace import SpanAttributes

@instrument(
    span_type=SpanAttributes.SpanType.RETRIEVAL,
    attributes={
        SpanAttributes.RETRIEVAL.QUERY_TEXT: "query",
        SpanAttributes.RETRIEVAL.RETRIEVED_CONTEXTS: "return",
    }
)
def retrieve_context(self, query: str) -> list:
    return self.retrieve(query)
```

In this example, `query` is the input parameter mapped to `RETRIEVAL.QUERY_TEXT`, and `return` is the return value mapped to `RETRIEVAL.RETRIEVED_CONTEXTS` for context relevance.

For framework auto-instrumentation (`TruChain`, `TruGraph`, `TruLlama`), see [Auto-instrument framework applications](/user-guide/snowflake-cortex/ai-observability/trace-applications-trulens#label-trulens-auto-instrument) on [Trace and monitor applications with TruLens](/user-guide/snowflake-cortex/ai-observability/trace-applications-trulens).

## Create a run

Create a run with `RunConfig` and `tru_app.add_run()`:

Copy code

```
run_config = RunConfig(
    run_name=run_name,
    description="desc",
    label="custom tag useful for grouping comparable runs",
    source_type="DATAFRAME",
    dataset_name="My test dataframe name",
    dataset_spec={
        "RETRIEVAL.QUERY_TEXT": "user_query_field",
        "RECORD_ROOT.INPUT": "user_query_field",
        "RECORD_ROOT.GROUND_TRUTH_OUTPUT": "golden_answer_field",
    },
    llm_judge_name="mistral-large2"
)

run = tru_app.add_run(run_config=run_config)
```

- `run_name`: Unique name under this `TruApp`
- `description` (optional): Run description
- `label` (optional): Groups comparable runs
- `source_type`: `DATAFRAME` or `TABLE`
- `dataset_name`: Dataframe label, or Snowflake table name (qualified if needed)
- `dataset_spec`: Maps span attributes to column names; see [Dataset and attributes](/user-guide/snowflake-cortex/ai-observability/reference#label-ai-observability-dataset-and-attributes)
- `llm_judge_name` (optional): Cortex model for judging; default `llama3.1-70b`

Retrieve, describe, invoke, and manage runs:

Copy code

```
run = tru_app.get_run(run_name=run_name)
run.describe()
run.start()  # TABLE source
run.start(input_df=user_input_df)  # DATAFRAME source
```

`run.start()` is blocking until invocation and ingestion complete or time out.

### Live tracing

For **online tracing** (production monitoring), create a live run with the `@trace_with_run` decorator on the function that calls your app (commonly in a web frontend or API handler). When you invoke that function, `@instrument()` on app methods creates OpenTelemetry spans inside the TruLens recording context that `@trace_with_run` enables.

Trace and retrieve live runs:

Copy code

```
from datetime import datetime
from trulens.core.app import trace_with_run

run_name = f"PROD_MONITOR_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

@trace_with_run(app=tru_app, run_name=run_name)
def process_message(message: str) -> str:
    return agent_app.ask(message)

response = process_message("How do I reset my password?")

run = tru_app.get_run(run_name)
```

### Compute metrics

AI Observability metrics can be computed **server-side** (by metric name) or **client-side** (with the TruLens Metric API and custom metrics you define).

To compute **server-side** metrics after invocation status is `INVOCATION_COMPLETED` or `INVOCATION_PARTIALLY_COMPLETED`:

Copy code

```
run.compute_metrics(metrics=[
    "coherence",
    "answer_relevance",
    "groundedness",
    "context_relevance",
    "correctness",
])
```

To compute **custom client-side** metrics, instantiate a `Metric` object and include it in the same list. Client-side metrics can be any TruLens feedback function or any Python function.

Simple Python function:

Copy code

```
from trulens.core import Metric, Selector

word_count = Metric(
    name="word_count",
    implementation=lambda text: len(text.split()),
    selectors={"text": Selector.select_record_output()},
)

run.compute_metrics(metrics=[
    word_count,
    "coherence",
    "answer_relevance",
    "groundedness",
    "context_relevance",
    "correctness",
])
```

TruLens feedback functions can be customized for your domain with custom rubrics, guiding examples, or a different score scale. The following example uses a [Cortex provider](https://www.trulens.org/reference/trulens/providers/cortex/provider/) feedback function (`provider` is a `trulens.providers.cortex.Cortex` instance):

Copy code

```
from trulens.core import Metric, Selector

f_relevance = Metric(
    implementation=provider.relevance_with_cot_reasons,
    name="Answer Relevance",
    selectors={
        "prompt": Selector.select_record_input(),
        "response": Selector.select_record_output(),
    },
    criteria="Score 3 only if the answer cites the policy section it used.",
    additional_instructions="A section number with no quote is partial credit.",
    examples=[
        ({"prompt": "Is water damage covered?",
          "response": "Yes, section 4.2 covers burst pipes."}, 3),
        ({"prompt": "Is water damage covered?",
          "response": "Yes, probably."}, 0),
    ],
    min_score_val=0,
    max_score_val=3,
)

run.compute_metrics(metrics=[
    f_relevance,
    "coherence",
    "groundedness",
])
```

`run.compute_metrics()` is asynchronous. You can call it multiple times with different metric lists; a metric can’t be recomputed for the same run.

Check status, cancel, delete, or list runs:

Copy code

```
run.get_status()
run.cancel()
run.delete()  # metadata only; traces remain in AI_OBSERVABILITY_EVENTS
tru_app.list_runs()
```

Run statuses are listed in [Runs](/user-guide/snowflake-cortex/ai-observability/reference#label-ai-observability-runs).

## View evaluation results in Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **Evaluations**.
3. Select the application (External Agent).
4. Select a run to view aggregated and per-record scores.
5. Select a record to view traces, latency, span detail, and LLM judge explanations.

To compare runs that share a dataset, select multiple runs and choose **Compare**.

## Query evaluation data with SQL

Evaluation traces and scores for External Agent applications are stored in `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS`. Use `agent_type` `EXTERNAL AGENT` and the database, schema, and External Agent name.

### Observability events

Copy code

```
SELECT *
  FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_EVENTS(
    '<database_name>',
    '<schema_name>',
    '<external_agent_name>',
    'EXTERNAL AGENT'
  ));
```

Filter on `RECORD_ATTRIBUTES` (for example run name) to scope results to one evaluation run. For column details, see [GET\_AI\_OBSERVABILITY\_EVENTS (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_observability_events-snowflake-local) and [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events).

### Evaluation logs

For warnings and errors during a TruLens run:

Copy code

```
SELECT *
  FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_LOGS(
    '<database_name>',
    '<schema_name>',
    '<external_agent_name>',
    'EXTERNAL AGENT'
  ))
  WHERE record:"severity_text" IN ('ERROR', 'WARN')
    AND record_attributes:"snow.ai.observability.run.name" = '<run_name>';
```

Note

The fields `record:"severity_text"` and `record_attributes:"snow.ai.observability.run.name"` are guaranteed in AI Observability logs. Other fields may change.

When `agent_type` is `EXTERNAL AGENT`, **USAGE** on the External Agent is sufficient; **MONITOR** does not apply.

Note

**Redaction and TruLens evaluations**

The **READ UNREDACTED AI OBSERVABILITY EVENTS TABLE** privilege affects unredacted fields in Snowsight and observability UDTFs on the monitoring path. It does **not** change TruLens evaluation run execution or how scores appear in the **Evaluations** experience. See [Account Privilege READ UNREDACTED AI OBSERVABILITY EVENTS TABLE](/release-notes/bcr-bundles/un-bundled/bcr-read-unredacted-ai-observability-events) and [Trace and monitor applications with TruLens](/user-guide/snowflake-cortex/ai-observability/trace-applications-trulens).

## Access control

Roles need privileges described in [Access control and storage](/user-guide/snowflake-cortex/ai-observability/reference#label-ai-observability-required-privileges) and [Runs](/user-guide/snowflake-cortex/ai-observability/reference#label-cortex-ai-observability-runs), including **USAGE** on the External Agent, **CREATE TASK**, **EXECUTE TASK**, and **SNOWFLAKE.CORTEX\_USER**.

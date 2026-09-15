# Trace and monitor applications with TruLens

Use this topic when you build a **custom AI application** (for example, an agent, an AI workflow, or a RAG pipeline) that is not a native Cortex feature, and you want **tracing and monitoring** on Snowflake with the **TruLens** SDK. You can run the app on Snowflake compute (such as Snowpark Container Services or a hosted Python process) or on other infrastructure.

TruLens exports OpenTelemetry-style traces to your account. You debug executions in Snowsight and can query the same events with SQL. For **batch evaluation runs** and LLM-judge metrics (context relevance, groundedness, and others), see [Evaluate applications with TruLens](/user-guide/snowflake-cortex/ai-observability/evaluate-applications-trulens).

Note

If you built a **Cortex Agent** in Snowflake, use [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor) instead. You don’t need TruLens for native agent monitoring.

**TruLens** is an open source observability SDK that Snowflake integrates with AI Observability. Snowflake registers each TruLens application as an [External Agent](/sql-reference/commands-external-agent) object. That object stores metadata only (application name, version, run name). It does not store application code, prompts, traces, or scores. Traces and evaluation results are stored in `AI_OBSERVABILITY_EVENTS`.

TruLens is a good fit when you own the application end to end, including:

- Agent, RAG, or workflow apps on Snowflake compute, another cloud, or on-premises
- Custom tool chains and retrieval logic that are not native Cortex Agent deployments
- Batch LLM-as-a-judge evaluations you run from Python rather than Snowsight

## Get started

1. Install TruLens packages (version 2.1.2 or later): `trulens-core`, `trulens-connectors-snowflake`, `trulens-providers-cortex`. See [Required privileges](/user-guide/snowflake-cortex/ai-observability/reference#label-ai-observability-required-privileges) in the reference topic.
2. Instrument and register your application using the steps in this topic.
3. Run batch evaluations with [Evaluate applications with TruLens](/user-guide/snowflake-cortex/ai-observability/evaluate-applications-trulens).
4. Take the [quickstart tutorial](/user-guide/snowflake-cortex/ai-observability/tutorial) or read the [reference](/user-guide/snowflake-cortex/ai-observability/reference) for datasets, metrics, runs, and privileges.

View External Agent traces and evaluation runs in Snowsight under **AI & ML** » **Evaluations**. For more information about TruLens itself, see the [TruLens documentation](https://trulens.org/getting_started).

Important

External Agent objects share a namespace with [model](/sql-reference/sql/create-model) objects in the same schema.

## Tracing vs evaluation

Use the following table to choose the right TruLens guide:

| Task | Documentation |
| --- | --- |
| Capture spans while the app runs; debug latency and tool use in Snowsight | This topic |
| Run a dataset through the app, compute metrics, compare versions | [Evaluate applications with TruLens](/user-guide/snowflake-cortex/ai-observability/evaluate-applications-trulens) |

Expand

Show lessSee more

## Prerequisites

Complete the [Required privileges](/user-guide/snowflake-cortex/ai-observability/reference#label-ai-observability-required-privileges) steps before you instrument an application.

## Instrument the app

After you create your application in Python, use the TruLens `@instrument()` decorator to capture function inputs, outputs, and latency.

Copy code

```
from trulens.core.otel.instrument import instrument
```

### Scenario 1: Trace a function

Add `@instrument()` on functions you want to trace:

Copy code

```
@instrument()
def answer_query(self, query: str) -> str:
    context_str = self.retrieve_context(query)
    return self.generate_completion(query, context_str)
```

### Scenario 2: Trace a function with a specific span type

Span types improve trace readability in Snowsight:

- `RETRIEVAL`: Retrieval or search functions
- `GENERATION`: LLM inference calls
- `RECORD_ROOT`: Main entry point for the application

Copy code

```
from trulens.otel.semconv.trace import SpanAttributes

@instrument(span_type=SpanAttributes.SpanType.RETRIEVAL)
def retrieve_context(self, query: str) -> list:
    return self.retrieve(query)

@instrument(span_type=SpanAttributes.SpanType.GENERATION)
def generate_completion(self, query: str, context_str: list) -> str:
    return response

@instrument(span_type=SpanAttributes.SpanType.RECORD_ROOT)
def answer_query(self, query: str) -> str:
    context_str = self.retrieve_context(query)
    return self.generate_completion(query, context_str)
```

To map parameters to span attributes for **evaluation metrics**, see [Evaluate applications with TruLens](/user-guide/snowflake-cortex/ai-observability/evaluate-applications-trulens).

### Scenario 3: Capture discrete function attributes in a trace

Span attributes help you surface particular values in a trace, such as a key-value pair passed to a custom agent.

The `@instrument()` decorator accepts **lambda functions** in the `attributes` parameter. Instead of static mappings, you can compute attributes from the function’s execution context. A lambda receives:

- `ret`: The function’s return value
- `exception`: Any exception raised during execution (`None` if the call succeeded)
- `*args`: Positional arguments passed to the function
- `**kwargs`: Keyword arguments (positional args are also available here by name)

Copy code

```
from trulens.core.otel.instrument import instrument
from trulens.otel.semconv.trace import SpanAttributes

@instrument(
    attributes=lambda ret, exception, *args, **kwargs: {
        SpanAttributes.RETRIEVAL.RETRIEVED_CONTEXTS: [doc["text"] for doc in ret],
        SpanAttributes.RETRIEVAL.QUERY_TEXT: kwargs["query"].upper(),
    },
)
def retrieve_contexts(self, query: str) -> list[dict[str, str]]:
    return [
        {"text": "context 5", "source": "doc1.pdf"},
        {"text": "context 6", "source": "doc2.pdf"},
    ]
```

### Auto-instrument framework applications

TruLens provides wrappers for popular frameworks:

- `TruChain`: LangChain and LCEL chains
- `TruGraph`: LangGraph applications
- `TruLlama`: LlamaIndex query engines and retrievers

For framework examples and selectors, see the [TruLens instrumentation documentation](https://www.trulens.org/component_guides/instrumentation/).

## Register the app in Snowflake

Register the application so TruLens can write traces to `AI_OBSERVABILITY_EVENTS` and create an External Agent object for governance:

Copy code

```
tru_app = TruApp(
    app: Any,
    app_name: str,
    app_version: str,
    connector: SnowflakeConnector,
    main_method: callable  # for example app.query
)
```

If you use `TruChain`, `TruGraph`, or `TruLlama`, registration is included when you wrap the application. See [Auto-instrument framework applications](#label-trulens-auto-instrument).

Parameters:

- `app`: Instance of your application class
- `app_name`: Name stored in Snowflake for this application
- `app_version`: Version label for experiments and comparisons
- `connector`: `SnowflakeConnector` for Snowpark session management
- `main_method` (optional): Entry point for tracing (for example, `app.answer_query`). Not required if the entry point uses `RECORD_ROOT` instrumentation.

Invoke the application while the `TruApp` (or framework wrapper) recorder is active so traces are exported on each run.

## View traces in Snowsight

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **Evaluations**.
3. Select your application (External Agent).
4. Open a run or record to inspect traces: inputs and outputs per span, latency, and intermediate steps.

Compare traces across application **versions** to debug regressions and tune prompts or tools. For aggregated evaluation scores on a dataset, see [Evaluate applications with TruLens](/user-guide/snowflake-cortex/ai-observability/evaluate-applications-trulens).

## Observability data and SQL access

Traces and evaluation results for TruLens applications are stored in `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS`. Rows can’t be modified after ingestion.

The `SNOWFLAKE.AI_OBSERVABILITY_READER` application role grants read-only access to the table. The `SNOWFLAKE.AI_OBSERVABILITY_ADMIN` role can delete rows. For details, see [AI\_OBSERVABILITY\_EVENTS table](/sql-reference/local/ai_observability_events).

Note

**Unredacted fields in Snowsight and UDTF results**

The account privilege **READ UNREDACTED AI OBSERVABILITY EVENTS TABLE** controls whether roles see unredacted tool inputs, outputs, and conversation text when viewing traces in Snowsight or calling `SNOWFLAKE.LOCAL` observability UDTFs. Without the grant, metadata (tool names, latency, token usage, and similar fields) is still available. This does **not** change TruLens evaluation run execution or scores shown in the **Evaluations** experience. See [Account Privilege READ UNREDACTED AI OBSERVABILITY EVENTS TABLE](/release-notes/bcr-bundles/un-bundled/bcr-read-unredacted-ai-observability-events).

### Query traces with SQL

Use [GET\_AI\_OBSERVABILITY\_EVENTS](/sql-reference/functions/get_ai_observability_events-snowflake-local) with `agent_type` `EXTERNAL AGENT`. Pass the database, schema, and External Agent object name. Results use the [event table column layout](/developer-guide/logging-tracing/event-table-columns).

When `agent_type` is `EXTERNAL AGENT`, **USAGE** on the External Agent is sufficient to call the function; **MONITOR** does not apply. **OWNERSHIP** is required to modify or drop the External Agent with SQL.

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

Filter with `WHERE` on `RECORD`, `RECORD_ATTRIBUTES`, time columns, or other fields to narrow results. For full arguments, see the function reference.

For evaluation-run logs and warnings, use [GET\_AI\_OBSERVABILITY\_LOGS](/sql-reference/functions/get_ai_observability_logs-snowflake-local). For evaluation result tables, see [Evaluate applications with TruLens](/user-guide/snowflake-cortex/ai-observability/evaluate-applications-trulens).

## Access control

To view traces in Snowsight or query events for an External Agent, the role needs:

- **USAGE** (or **OWNERSHIP**) on the External Agent object
- **SNOWFLAKE.CORTEX\_USER** database role (for `SNOWFLAKE.LOCAL` functions)

To register applications and run evaluations, see [Required privileges](/user-guide/snowflake-cortex/ai-observability/reference#label-ai-observability-required-privileges).

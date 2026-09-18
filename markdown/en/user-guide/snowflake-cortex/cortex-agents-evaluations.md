# Cortex Agent evaluations

Use this topic for **batch evaluations** of **native Cortex Agents** in Snowflake (Snowsight **Evaluations** tab or `EXECUTE_AI_EVALUATION`). For **live** conversation logs and the **Observability** tab, see [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor). For **custom AI applications** evaluated with TruLens, see [Evaluate applications with TruLens](/user-guide/snowflake-cortex/ai-observability/evaluate-applications-trulens).

Cortex Agent evaluations allow you to test, baseline, and hill climb on your agent’s behavior and performance, so that you know when your agent is ready to roll out to your users. Evaluate your agent against both ground truth and reference-free evaluation metrics. During evaluation, your agent’s activity is traced and monitored so you can ensure that each step advances towards your end goal. Per-record **Trace details** in the Evaluations UI match the trace information described in [agent monitoring](/user-guide/snowflake-cortex/cortex-agents-monitor#label-cortex-agent-log-info).

The evaluation metrics follow Snowflake’s [Goal-Plan-Action (GPA) framework](https://www.snowflake.com/en/engineering-blog/ai-agent-evaluation-gpa-framework/): instead of judging only the final answer, they evaluate your agent at each stage of its reasoning, so you can pinpoint where it made a mistake or was inefficient on the way to its answer. The four system metrics trace the loop from the user’s goal to the agent’s answer:

- **Tool selection accuracy (Public Preview)** covers *goal to plan*: whether the agent’s orchestration layer invokes the tools you expect for the user’s goal.
- **Tool execution accuracy (Public Preview)** covers *plan to actions*: whether each tool the agent runs receives appropriate input and returns output that meets your requirements.
- **Answer correctness** closes the loop from *actions back to goal*: how closely the agent’s final response matches the expected ground truth answer.
- **Logical consistency** spans the whole loop: it measures consistency across agent instructions, planning, and tool calls. This metric is *reference-free*, meaning you don’t need to prepare any ground truth in your dataset.

Snowflake also allows you to create custom evaluation metrics that use the LLM judging process to measure context critical to your agent’s domain and use case. Custom metrics use an LLM prompt and scoring methodology, which are passed to the evaluation judging system to produce a score, and can be ground truth based or reference-free.

For evaluation methodology and dataset design guidance, see [Best Practices for Evaluating Cortex Agents](https://www.snowflake.com/en/developers/guides/best-practices-for-evaluating-cortex-agents/). For an example of running an evaluation programmatically, see [Getting Started with Cortex Agent Evaluations](https://www.snowflake.com/en/developers/guides/getting-started-with-cortex-agent-evaluations/).

## Access control requirements

The ability to run a Cortex Agent evaluation requires the role that runs the evaluation to have the following:

- The DATABASE ROLE SNOWFLAKE.CORTEX\_USER role
- The USE AI FUNCTIONS account-level privilege (or the per-function `USE AI FUNCTION AI_COMPLETE` privilege). Evaluation judges use Cortex LLM inference, which is gated by this privilege. The USE AI FUNCTIONS privilege is granted to the PUBLIC role by default. If your account has revoked it from PUBLIC, grant it explicitly. For more information, see [Cortex LLM privileges](/user-guide/snowflake-cortex/aisql-privileges-and-access#label-cortex-llm-privileges).
- The EXECUTE TASK ON ACCOUNT permission
- The USAGE permission on the database and schema containing your agent
- The USAGE permission on the database and schema containing your evaluation data
  - If creating the input table that holds your evaluation inputs, CREATE TABLE ON SCHEMA
  - If creating a dataset from an input table, CREATE DATASET ON SCHEMA
- The following permissions on the current database and schema, which is where the evaluation will be run from:
  - USAGE
  - CREATE FILE FORMAT ON SCHEMA
  - CREATE TASK
  - If creating the stage that holds your evaluation configuration file, CREATE STAGE ON SCHEMA

Note

In Snowsight, agent evaluations are run on the database and schema of the agent. With SQL, agent evaluations are run on the session’s database and schema.

- The USAGE or OWNERSHIP privilege on your agent
- The MONITOR or OWNERSHIP privilege on your agent
- If using an agent evaluation configuration, READ privilege on the stage containing the configuration file.

If the agent being evaluated uses tools, your role also needs access to all of them.

Additionally, if working with evaluations in Snowsight, the role you use to run or inspect an evaluation needs the USAGE privilege on the warehouse used for the run. When you start an evaluation, you can choose this warehouse with the **Warehouse** selector; otherwise the run uses your default warehouse.

## Prepare an evaluation dataset

Before starting a Cortex Agent evaluation, prepare a table containing your evaluation inputs. This table is used to create a dataset for your evaluation to run against. To learn more about datasets on Snowflake, see [Snowflake Datasets](/developer-guide/snowflake-ml/dataset).

Creating this table requires CREATE TABLE ON SCHEMA, and creating a dataset from it requires CREATE DATASET ON SCHEMA. For the full list, see [Access control requirements](#label-agent-evaluation-access-control).

### Prepare a dataset with Cortex Code

[Cortex Code](/user-guide/cortex-code/cortex-code) can help you create or update an evaluation dataset. Use the `dataset-curation` sub-skill of the Cortex Code [`agent-studio`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-agent-studio) skill in the CLI (see [Cortex Code CLI - Skills](/user-guide/cortex-code/extensibility#label-extensibility-skills)), or select **Create with Cortex Code** or **Manage datasets** on an agent’s **Evaluations** tab in Snowsight, to:

- Generate synthetic queries based on your agent configuration.
- Import queries from production monitoring data.
- Edit an existing dataset to add, remove, or modify queries using either source.

Cortex Code can also run the evaluation against the dataset, so you can go from dataset to results in a single flow.

### Dataset format

The dataset table has two columns:

- **Input query** (VARCHAR): the user query to evaluate.
- **Ground truth** (VARIANT): a JSON object describing the expected agent behavior. This is the single value the LLM judges compare against.

What you put in the ground truth VARIANT JSON depends on which metrics you enable and is focused on two keys: `ground_truth_output` and `ground_truth_invocations`:

- **Answer correctness** reads the `ground_truth_output` key and compares its value to the agent’s **streamed reply**: everything the user sees, including LLM thinking, response generation, and chart generation (note that it validates only the underlying data, not the rendered chart). For guidance and examples, see [Answer correctness ground truth](#label-agent-evaluation-ground-truth-examples).
- **Tool selection accuracy** and **tool execution accuracy** (Public Preview) read the `ground_truth_invocations` key and compare the expected tool names, inputs, and outputs to the agent’s actual tool calls. For details, see [Tool selection and execution metrics ground truth](#label-cortex-agent-evaluation-tool-metrics).
- **Logical consistency** is a *reference-free* metric and needs no ground truth.
- **Custom metrics** read the **entire** VARIANT through the `{{ground_truth}}` placeholder, regardless of key. Use this to check process criteria the streamed reply doesn’t expose: for example, reference `{{tool_info}}` to verify which tools or tables the agent used. Keep output criteria in `ground_truth_output` and process criteria in the custom metric’s own keys. For details, see [Defining a custom metric](#label-agent-evaluation-custom-metric).

A single ground truth VARIANT can hold the keys for several metrics at once, so one dataset can drive answer correctness, the tool metrics, and custom metrics in the same evaluation run. Any data not consumed by your selected metrics is ignored, so you can leave the column empty for runs that use only reference-free metrics like logical consistency.

#### Answer correctness ground truth

Because the `ground_truth_output` value is fed into an LLM prompt, treat it as a plain-language rubric built from literal, verifiable values (actual numbers, dates, and names) rather than placeholders:

- If the correct answer is known and stable, state it and include any rounding, tolerance, units, formatting, or scoping the response must observe (for example, “the value must be within ±2% of 123.45”).
- If the answer changes over time or has a particular shape, describe what a correct response should and shouldn’t contain. Include a format example like `"Output is in the following JSON format: ..."` if structure matters. Provide enough detail that two readers would agree on whether a given reply meets the bar.

The following examples show `ground_truth_output` values you can adapt for your own dataset. Each pairs an input query with the JSON you’d put in the ground truth VARIANT column.

##### Static factual query

Use when the correct answer is known and stable. State the expected value and decide whether the response must match it exactly or whether rounding or a tolerance is acceptable. Add any other facets a correct reply must cover, such as scoping to the right date or excluding specific categories of records.

**Input query:** `How many active customers does my business have as of December 31, 2025?`

Copy code

```
{
  "ground_truth_output": "There are 1,000 active customers as of December 31, 2025. The response should reference that exact date (not a different date or 'as of today') and present the count as a factual number. Rounding to the nearest hundred or a value within ±1% is acceptable; values outside that range aren't. The count shouldn't include test or churned accounts."
}
```

##### Dynamic or live data query

Use when you can’t fix a number in advance but can describe what a good response looks like.

**Input query:** `How many orders did customers place today?`

Copy code

```
{
  "ground_truth_output": "The response should give a specific whole-number count of orders placed today and scope the count explicitly to today's date. It shouldn't return results for a different time period or claim data is unavailable without attempting retrieval, and it shouldn't hedge with phrases like 'approximately' or 'I think'. The count should be presented as a fact derived from the data."
}
```

##### Boundary or out-of-scope query

Use when the agent should refuse rather than hallucinate.

**Input query:** `What's the weather like in New York today?`

Copy code

```
{
  "ground_truth_output": "The response should state that weather information is outside the agent's capabilities and ideally point to the kinds of questions the agent can help with. It shouldn't fabricate a forecast or present any temperatures or conditions."
}
```

##### Complex investigation

Use when the response must connect multiple facts. **Logical consistency** (reference-free) catches contradictions in planning and tool use; `ground_truth_output` catches a coherent but factually wrong explanation.

**Input query:** `Why did our checkout conversion rate drop between March 1–7, 2025?`

Copy code

```
{
  "ground_truth_output": "The response should acknowledge that checkout conversion dropped during March 1–7, 2025, link the drop to the payment gateway timeout issue that began March 3, 2025, and note that mobile users were disproportionately affected (more than 70% of failed checkouts were mobile). It should also quantify the drop (conversion fell from ~4.2% to ~2.8%). It shouldn't attribute the drop to causes the data doesn't support, such as a marketing campaign change or seasonal trends. The causal chain (gateway timeouts to failed checkouts to conversion drop, concentrated on mobile) matters more than the order the facts appear in."
}
```

| Scenario | What to put in `ground_truth_output` |
| --- | --- |
| Known answer, static data | The specific value, any tolerance, and what to exclude |
| Live or changing data | A description of what a correct response should and shouldn’t contain |
| Off-topic or refusal | What the agent should say, and that it shouldn’t fabricate an answer |
| Multi-fact investigation | Each fact the response should cover, plus explanations to avoid |

Expand

Show lessSee more

#### Tool selection and execution metrics ground truth

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts.

Both metrics read the `ground_truth_invocations` key in the ground truth VARIANT. The value is an array of JSON objects, one per expected tool-related check. Use the empty array `[]` when you expect **no** tools to be called. Each metric uses this key differently:

- **Tool selection accuracy (TSA)** compares the tool **names** you list in ground truth to the tool names the agent actually invoked, among the tools this metric scores (listed later in this section). Agents can call tools in parallel or in multiple valid orders, so ordering is not considered. For each record, Snowflake counts how many expected tool names are matched to actual invocations (each actual call is matched at most once), using the formula `matched tools / max(number of expected tool entries, number of actual tool calls)`. This penalizes every failure mode: too few calls, too many calls, or the wrong tools. TSA scoring is deterministic for a given set of tool calls: no LLM judge is involved, so the same tool calls always produce the same score. A TSA score that changes between otherwise identical runs means the agent invoked different tools, not that scoring varied. For details, see [Interpret score variance across runs](#label-agent-evaluation-score-variance).
- **Tool execution accuracy (TEA)** scores the **input and output quality** of the tool calls you describe in ground truth. For each entry, Snowflake finds the closest semantic match among the agent’s actual invocations for that tool (pairing each tool call at most once), then scores how well the expected input and output align with the real invocation. An expected tool the agent never invoked scores 0.0 and lowers TEA. Extra tools the agent invokes beyond your ground truth don’t penalize TEA (rely on TSA for this instead). TSA and TEA currently score only the tools listed later in this section; other tool types are skipped and left out of those scores.

`tool_input` and `tool_output` are optional. If you omit one or both for an entry, Snowflake only evaluates what you provided. If you provide neither, TEA only confirms the tool was invoked (a name match) and doesn’t grade input or output quality for that entry.

Tip

Treat `tool_input` and `tool_output` as **VARCHAR-style strings** in your JSON (plain text). You aren’t limited to a rigid JSON shape. Describe expected parameters, SQL, retrieved facts, or response snippets in whatever form is clearest. The LLM judge interprets that text semantically against what really happened, in the same manner as the **answer correctness** `ground_truth_output` value.

**`ground_truth_invocations` entry keys**

| Key | Description | Used by |
| --- | --- | --- |
| `tool_name` | The name of the tool as exposed to the agent: Cortex Analyst tool name (its semantic view name also matches), Cortex Search service name, a custom tool name, or the fixed name `web_search` for web search. Use the same identifier the agent sees in its traces. | TSA (required to define the expected tool call). TEA (required to match actual tool calls to expected tool calls). |
| `tool_input` | Optional string. Natural-language or structured **text** describing what input you expect the agent to pass (for example a paraphrase of the question or a short JSON blob as text). | TEA only (optional, provide if validation of the tool input is important). |
| `tool_output` | Optional string. Natural-language or structured **text** describing what you expect the tool to return (result data from a query, a SQL string, citations, JSON, and so on). | TEA only (optional, provide if validation of the tool output is important). |

Expand

Show lessSee more

Tool selection accuracy and tool execution accuracy currently score the following tools. Each example shows the `tool_name` to use and how to describe the expected input and output. You can describe `tool_output` however you like: a natural-language description (for example, “SQL that totals revenue by category for Q1 2025 and returns three rows around 1.2M, 1.4M, and 1.1M”), exact SQL, exact result rows, or any combination. The LLM judge interprets whatever you provide semantically. For tools that aren’t listed here, the evaluation still runs; use **answer correctness** and **logical consistency** to judge the agent’s final response or overall behavior, or a [custom metric](#label-agent-evaluation-custom-metric) whose LLM judge can inspect traces for all tools. Tool-level scoring for additional tools isn’t available yet.

**Cortex Analyst** – Use the Cortex Analyst tool name your agent calls (its semantic view name also matches). The `tool_input` is the natural-language query the agent generates for the tool, not SQL you author. Put any expected SQL and result in `tool_output`.

Copy code

```
{
  "tool_name": "finance_analyst",
  "tool_input": "What was Q1 2025 revenue by product category?",
  "tool_output": "SQL that aggregates revenue by category for Jan 1 - Mar 31, 2025 from the REVENUE_V semantic view, returning three rows with totals roughly 1.2M, 1.4M, and 1.1M USD."
}
```

**Cortex Search** – Use the search tool or service name your agent is configured with (for example the name shown in agent settings, not a generic label unless that is the registered name). Describe what should be retrieved instead of relying on a fixed schema.

Copy code

```
{
  "tool_name": "product_docs_search",
  "tool_input": "Query should ask for return policy and warranty text for electronics.",
  "tool_output": "Top sources should include the policy page and mention 30-day returns and 1-year warranty."
}
```

**Web search** – The tool name in traces is always `web_search` and is not configurable. Use that exact value for `tool_name`. In `tool_input` and `tool_output`, describe the query you expect and what kinds of sources or facts should appear in results. For the product feature, see [Web search](/user-guide/snowflake-cortex/cortex-agents-manage#label-cortex-agents-web-search).

Copy code

```
{
  "tool_name": "web_search",
  "tool_input": "User wants the current Federal Reserve policy rate and any change in the last six months.",
  "tool_output": "Results should cite recent news or official sources and include a concrete rate or date range."
}
```

**Custom tool** – Use the registered tool name. Describe arguments and outcomes in text; embed JSON or key-value prose if that helps your reviewers.

Copy code

```
{
  "tool_name": "get_weather",
  "tool_input": "City San Francisco and date August 2, 2019.",
  "tool_output": "Temperature near 14 C and units metric."
}
```

#### Insert a full entry into a Snowflake table

Populate the VARIANT column with [PARSE\_JSON](/sql-reference/functions/parse_json). The following example creates `agent_evaluation_data` and inserts one input query whose ground truth of fictional information and data combines `ground_truth_output` with an expected invocation. `ground_truth_invocations` supports a list of multiple expected tool calls for queries that invoke multiple tools:

Copy code

```
CREATE OR REPLACE TABLE agent_evaluation_data (
    input_query VARCHAR,
    ground_truth VARIANT
);

INSERT INTO agent_evaluation_data
  SELECT
    'What was Q1 2025 revenue by product category, and what does our return policy say for electronics?',
    PARSE_JSON('
      {
        "ground_truth_output": "Q1 2025 revenue by category was roughly Services 1.2M, Hardware 1.4M, and Subscriptions 1.1M USD. Electronics can be returned within 30 days and carry a 1-year warranty.",
        "ground_truth_invocations": [
            {
              "tool_name": "finance_analyst",
              "tool_input": "What was Q1 2025 revenue by product category?",
              "tool_output": "SQL that aggregates revenue by category for Jan 1 - Mar 31, 2025 from the REVENUE_V semantic view, returning three rows around 1.2M, 1.4M, and 1.1M USD."
            },
            {
              "tool_name": "product_docs_search",
              "tool_input": "return policy and warranty for electronics",
              "tool_output": "Results should include the return policy page and mention 30-day returns and a 1-year warranty."
            }
        ]
      }
    ');
```

Important

[OBJECT\_CONSTRUCT](/sql-reference/functions/object_construct) and [ARRAY\_CONSTRUCT](/sql-reference/functions/array_construct) return OBJECT and ARRAY, not VARIANT. Use [PARSE\_JSON](/sql-reference/functions/parse_json), or wrap a value in [TO\_VARIANT](/sql-reference/functions/to_variant), to guarantee the column type.

### Create a dataset from a Snowflake table (SQL)

To create an evaluation dataset with SQL, call [SYSTEM$CREATE\_EVALUATION\_DATASET](/sql-reference/functions/system_create_evaluation_dataset).

Note

The column-mapping keys differ depending on how you create the dataset:

- When you call `SYSTEM$CREATE_EVALUATION_DATASET` (SQL), use `query_text` and `expected_tools` in the mapping object.
- When you define a dataset in the Agent Evaluation YAML (`dataset.column_mapping`), use `query_text` and `ground_truth`.

## Start an agent evaluation

### Start an evaluation with Cortex Code

You can also run an evaluation through [Cortex Code](/user-guide/cortex-code/cortex-code). Use the `evaluate-cortex-agent` sub-skill of the Cortex Code [`agent-studio`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-agent-studio) skill in the CLI (see [Cortex Code CLI - Skills](/user-guide/cortex-code/extensibility#label-extensibility-skills)), or continue the same Cortex Code flow from **Prepare an evaluation dataset** in Snowsight directly into running the evaluation against your dataset.

The skill accepts the same choices as the other paths, including which [agent version](#label-cortex-agent-evaluation-yaml-spec) to evaluate and which [metric versions](#label-agent-evaluation-metric-versions) to score with.

### Start an evaluation in Snowsight

Note

By default, an agent evaluation runs as your current role and uses your default warehouse. When you start an evaluation in Snowsight, use the **Role** and **Warehouse** selectors to override these defaults and run the evaluation with a specific role and warehouse. Make sure the role you select has the correct permissions before starting an evaluation. For details, see [Access control requirements](#label-agent-evaluation-access-control).

The controls on the **Evaluations** tab depend on whether the agent already has datasets and evaluation runs:

- **Before your first evaluation is run for an agent**, the tab shows two starting points:

  - **Create a dataset**: Build a new evaluation dataset. Use the dropdown to select **Create with Cortex Code** to generate a dataset with [Cortex Code](/user-guide/cortex-code/cortex-code).
  - **Use existing dataset**: Run against a dataset you already have. Use the dropdown to select **Run an evaluation with Cortex Code** or **Run an evaluation manually**.
- **After you have run an evaluation**, the **Evaluations** tab shows your list of previous evaluation runs in the filter range, along with:

  - **Manage datasets**: Create or expand datasets using production monitoring data or CoCo generating synthetic questions and answers. Use the dropdown to select **Manage with Cortex Code**.
  - **Create evaluation run**: Start a new run. Use the dropdown to select **Run an evaluation with Cortex Code** or **Run an evaluation manually**.

Selecting **Create with Cortex Code**, **Manage with Cortex Code**, or **Run an evaluation with Cortex Code** hands the workflow to [Cortex Code](/user-guide/cortex-code/cortex-code), which guides you through creating or updating a dataset and running the evaluation. Selecting **Run an evaluation manually** opens the **New evaluation run** modal described in the following steps.

Begin a manual evaluation of a Cortex Agent by doing the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **Agents**.
3. Select the agent you want to conduct an evaluation of.
4. Select the **Evaluations** tab.
5. Optional: Use the **Role** and **Warehouse** selectors to override the role and warehouse used for the run. By default, the evaluation run uses your current role and default warehouse.
6. Select **Create evaluation run** » **Run an evaluation manually**.
   The **New evaluation run** modal opens.
7. In the **Name** field, provide a name for your evaluation. This name should be unique for the agent being evaluated.
8. Optional: In the **Description** field, provide any comments for the evaluation.
9. From the agent version dropdown, select the version of the agent to evaluate. The list includes the agent’s committed versions, its aliases, and its live version. For guidance on which to pick, see [Agent Evaluation YAML specification](#label-cortex-agent-evaluation-yaml-spec).
10. Select **Next**.
    This advances to the **Select dataset** modal.
11. Select the dataset used to evaluate your agent. You can choose either **Existing dataset** or **Create new dataset**.
    To use an existing dataset:

    1. From the **Database and schema** list, select the database and schema containing your dataset.
    2. From the **Select dataset** list, select your dataset.

    To create a new dataset:

    1. From the **Source table - Database and schema** list, select the database and schema containing the table you want to import to a dataset.
    2. From the **Select source table** list, select your source table.
    3. From the **New dataset location - Database and schema** list, select the database and schema to place your new dataset.
    4. In the **Dataset name** field, enter your dataset name. This name needs to be unique among the schema-level objects in your selected schema.
12. Select **Next**.
    This advances to the **Select metrics** modal.
13. From the **Input query** list, select the column of your dataset which contains the input queries.
14. For each of the **System metrics**, change the toggle to active for any metric you want included in your evaluation. Select the column of your dataset containing the ground truth for your evaluation.
15. Optional: For each system metric you turned on, use its version dropdown to pin a [metric version](#label-agent-evaluation-metric-versions). Leaving the dropdown on its default is the same as omitting `version` in the YAML.
16. (Optional) To conduct a custom evaluation, toggle on **Custom metrics**.
17. Select the database and schema containing the stage where your custom evaluation configuration is stored.
18. Select the stage where your custom evaluation configuration is stored.
19. Select the YAML configuration file for your custom evaluation.

    Note

    In Snowsight, only the custom evaluation definitions are loaded from your YAML configuration. The rest of the YAML file must still be valid. Custom metrics take their judge model from the `model` key in that YAML; there’s no model selector in the modal. For the evaluation YAML specification, see [Agent Evaluation YAML specification](#label-cortex-agent-evaluation-yaml-spec).
20. For each custom metric, change the toggle to active if you want it included in your evaluation. Select the column of your dataset containing the ground truth for this evaluation.
21. Select **Create** to create the evaluation and begin the evaluation process.

At any point, you can select **Cancel** to cancel creating the evaluation, or select **Prev** to return to the previous modal.

### Start an evaluation with SQL

To start or retrieve information on an evaluation with SQL, use the [EXECUTE\_AI\_EVALUATION](/sql-reference/functions/execute_ai_evaluation) function. This function has the following required arguments:

- `evaluation_job`: A string value of ‘START’, ‘STATUS’, ‘CANCEL’, or ‘DELETE’.
- `run_parameters`: A SQL [OBJECT](/sql-reference/data-types-semistructured#label-data-type-object) containing the key `run_name`, with a value of the name of your run.
- `config_file_path:` A stage file path pointing to your run configuration YAML file. This path can’t be a signed URL. For the evaluation YAML specification, see [Agent Evaluation YAML specification](#label-cortex-agent-evaluation-yaml-spec).

Use the `evaluation_job` value ‘START’ to start an evaluation. The following example starts a run called `run-1` using the agent evaluation configuration from `@eval_db.eval_schema.metrics/agent_evaluation_config.yaml`:

Copy code

```
CALL EXECUTE_AI_EVALUATION(
  'START',
  OBJECT_CONSTRUCT('run_name', 'run-1'),
  '@eval_db.eval_schema.metrics/agent_evaluation_config.yaml'
);
```

After a run starts, you can query its progress with the `evaluation_job` value ‘STATUS’. This call returns a table in the format used for [AI Observability Runs](/user-guide/snowflake-cortex/ai-observability/reference#label-ai-observability-runs). The following example queries the status of the agent evaluation started from the previous example:

Copy code

```
CALL EXECUTE_AI_EVALUATION(
  'STATUS',
  OBJECT_CONSTRUCT('run_name', 'run-1'),
  '@eval_db.eval_schema.metrics/agent_evaluation_config.yaml'
);
```

To cancel an in-progress evaluation run, use the `evaluation_job` value ‘CANCEL’. The following example cancels the `run-1` run for the agent defined by the same configuration file:

Copy code

```
CALL EXECUTE_AI_EVALUATION(
  'CANCEL',
  OBJECT_CONSTRUCT('run_name', 'run-1'),
  '@eval_db.eval_schema.metrics/agent_evaluation_config.yaml'
);
```

To delete an evaluation run, use the `evaluation_job` value ‘DELETE’. The following example deletes the `run-1` run for the agent defined by the same configuration file:

Copy code

```
CALL EXECUTE_AI_EVALUATION(
  'DELETE',
  OBJECT_CONSTRUCT('run_name', 'run-1'),
  '@eval_db.eval_schema.metrics/agent_evaluation_config.yaml'
);
```

Tip

You can call the EXECUTE\_AI\_EVALUATION function from a [Task](/user-guide/tasks-intro) to regularly run an evaluation or check the status of one.

## Inspect evaluation results

Evaluation results include information about the requested metrics and the agent’s execution for each dataset input. Each input is processed as one **turn** (one **trace** made up of **spans**). See [Terminology](/user-guide/snowflake-cortex/cortex-agents-monitor#label-cortex-agent-observability-terminology).

### Inspect evaluation results with Cortex Code

In the [Cortex Code](/user-guide/cortex-code/cortex-code) CLI, the [`agent-studio`](/user-guide/cortex-code/bundled-skills#label-bundled-skill-agent-studio) skill provides two sub-skills for working with completed evaluations:

- `investigate-cortex-agent-evals`: Inspect evaluation runs and find any issues in your configuration or data.
- `optimize-cortex-agent`: Use results from completed evaluations to suggest and test changes that improve your agent’s performance.

For more information about Cortex Code skills, see [Cortex Code CLI - Skills](/user-guide/cortex-code/extensibility#label-extensibility-skills).

### Inspect evaluation results in Snowsight

The **Evaluations** tab for an agent in Snowsight gives you an overview of every evaluation run and its summary results. The tab shows evaluation runs across every version of the agent. Selecting a specific version in the agent versions panel doesn’t filter this tab.

To view evaluation results in Snowsight:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **AI & ML** » **Agents**.
3. Select the agent you want to conduct an evaluation of.
4. Select the **Evaluations** tab.

#### Agent versions in evaluation results

Each evaluation run targets exactly one agent version. Every input and trace in that run uses the version selected when the run starts.

Snowflake records the version and any alias used at invocation time. When you query the page, the UI pairs recorded runs with the agent’s current version metadata:

- After you commit a version that a run recorded as `LIVE` (displayed as `DRAFT` in the UI) as `VERSION$4`, that run and its traces display `VERSION$4` once new traces labeled `VERSION$4` start arriving. Snowflake pairs those traces with the earlier draft-labeled data.
- The UI shows aliases currently assigned to the recorded version, regardless of which alias was used when the evaluation ran. Reassigning an alias updates how existing runs and traces for those versions are labeled.
- If the recorded version was deleted, or if the run predates agent version tracking, the UI displays `—`.

The resolved version appears in the evaluation runs listing, the trace view for each input, and the comparison view.

#### Metric score trends

At the top of the **Evaluations** tab, Snowflake loads trend charts for the metrics in your runs, up to 10 charts. Each chart shows the current average score, the percentage change compared to the previous run, and the metric’s score across recent evaluation runs. Use these charts to see at a glance whether a metric is improving or regressing, and to gauge how consistent scoring is from run to run as you change your agent’s configuration or dataset.

Each [metric version](#label-agent-evaluation-metric-versions) appears as its own chart and as its own column in the runs listing. For example, `answer_correctness` `v1` and `answer_correctness` `v3` don’t share a trend line, because they use different LLM judges and scoring rubrics. Snowflake recommends scoring with the latest metric version and using that same version on every run. Mixing versions clutters the tab with extra charts and columns, and scores from different versions aren’t comparable.

If a run predates metric versioning, or Snowflake otherwise has no version to show, the UI displays `—` in that column.

#### Evaluation runs listing

The summary of run information for each run includes:

- `RUN NAME` – The name of the evaluation run.
- `# OF RECORDS` – The number of queries performed and answered as part of the run.
- `STATUS` – The status of the evaluation run, which is one of:

  - [![Success indicator](/static/images/snowsight/icons/check-circle.svg)](/static/images/snowsight/icons/check-circle.svg) – All inputs were evaluated and results are available.
  - **A spinner is displayed** – The run is in progress, with no information available yet.
  - [![Warning indicator](/static/images/snowsight/icons/warning-triangle.svg)](/static/images/snowsight/icons/warning-triangle.svg) – The run experienced an error at some point. Some or all metrics may be unavailable for the run.
- `DATASET` – The name of the dataset used for the evaluation.
- `VERSION` – The [agent version](#label-agent-evaluation-result-versions) the run evaluated, so you can compare scores across versions.
- `AVG DURATION` – The average duration of time taken to execute an input query for the run.
- `LOGICAL CONSISTENCY` – Average over all inputs of the logical consistency evaluation for the run, if requested. Each metric version gets its own column.
- `DESCRIPTION` – The description of the evaluation run.
- `CREATED` – The time at which the run was created and started.

Each custom metric evaluated for this run also receives its own column, defined by the evaluation metric `name` value. For more information on custom metrics, see [Defining a custom metric](#label-agent-evaluation-custom-metric).

#### Compare evaluation runs

To compare up to three evaluation runs side by side, select the runs you want to compare from the runs listing, then select **Compare**. The **Compare** view shows the two runs next to each other with:

- Run-level metadata and summary metrics (run name, dataset, resolved agent version and aliases, description, average duration, and the average score for each metric), so you can see how overall scores shifted between the runs.
- A per-input comparison of overlapping records, so you can see how the agent’s answer, duration, and metric scores changed for the same query. Use **Search** to find a specific input, and turn on **Hide unchanged metrics** to focus only on records whose scores differed.

Comparing runs helps you understand how changes to your agent’s configuration or dataset affected answer correctness, logical consistency, tool selection and execution accuracy, and any custom metrics from one run to the next.

#### Evaluation run overview

When you select an individual run in Snowsight, you’re presented with the run overview. This overview includes summary averages for each metric evaluated during the run, and a summary of each input execution. The overview for each input execution includes:

- `STATUS` – The status of the evaluation run, which is one of:

  - [![Success indicator](/static/images/snowsight/icons/check-circle.svg)](/static/images/snowsight/icons/check-circle.svg) – All inputs were evaluated and results are available.
  - **A spinner is displayed** – The run is in progress, with no information available yet.
  - [![Warning indicator](/static/images/snowsight/icons/warning-triangle.svg)](/static/images/snowsight/icons/warning-triangle.svg) – The run experienced an error at some point. Some or all metrics may be unavailable for the run.
- `INPUT` – The input query used for the evaluation.
- `OUTPUT` – The output produced by the agent.
- `DURATION` – The length of time taken to process the input and produce output.
- `LOGICAL CONSISTENCY` – The logical consistency evaluation for the input, if requested.
- `EVALUATED` – The time at which the input was processed.

Each custom metric evaluated for this run also receives its own column, defined by the evaluation metric `name` value. For more information about custom metrics, see [Defining a custom metric](#label-agent-evaluation-custom-metric).

#### View details (errors and metric warnings)

After you open a run from the evaluation runs listing, select **View details** on the right to open the detailed view for that run. Scroll down in this view to find **error logs** and other diagnostic information when something fails or returns partial results.

In the per-input table for the run, if metric computation has a problem for a specific row, a **warning** indicator can appear on the left side of that row. Hover over the warning to see details about the metric issue.

#### Record details

When you select an individual input in Snowsight, you’re presented with the **Record details** view. This view includes three panes: **Evaluation results**, **Thread details**, and **Trace details**.

##### Evaluation results

Your evaluation results are presented here in detail. Each metric has its own presentation box of overall average across inputs, which can be selected to display a popover containing more information. This popover contains a breakdown of the number of runs which performed at high accuracy (80% or more accurate), medium accuracy (30% or more accurate, but not high accuracy), and which failed.

##### Thread details

The execution trace for that evaluation input (one turn). This includes planning and response generation by default, as well as a span for each tool the agent invoked during that turn.

##### Trace details

Each span in the turn’s trace, with the resolved agent version and input, processing, and output information for that step of agent execution. This information is the same as that provided by [agent monitoring](/user-guide/snowflake-cortex/cortex-agents-monitor#label-cortex-agent-log-info).

### Inspect evaluation results with SQL

Important

**Observability redaction and evaluations**

The **READ UNREDACTED AI OBSERVABILITY EVENTS TABLE** account privilege and default **redaction** of certain raw fields in `AI_OBSERVABILITY_EVENTS` apply to **Cortex Agent monitoring** in Snowsight and to **observability** user-defined table functions used on the **monitoring** data path, as described in [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor) and [Account Privilege READ UNREDACTED AI OBSERVABILITY EVENTS TABLE](/release-notes/bcr-bundles/un-bundled/bcr-read-unredacted-ai-observability-events). This does **not** change **Cortex Agent evaluation** run execution, how metrics are computed, or how evaluation results and scores are shown in the **Evaluations** experience.

To retrieve raw evaluation details, use the [GET\_AI\_EVALUATION\_DATA (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_evaluation_data-snowflake-local) function. This function has the following required arguments:

- `database`: The database containing the agent.
- `schema`: The schema containing the agent.
- `agent_name`: The name of the agent.
- `agent_type`: `CORTEX AGENT` or `EXTERNAL AGENT`. This value is case-insensitive.
- `run_name`: The name of the evaluation run to retrieve.

This function returns a table of event data described in [Evaluation results table format](#label-cortex-agent-evaluations-results-format). The following example displays the full evaluation details for a run called `run-1`, where the agent is named `evaluated_agent` stored on the schema `eval_db.eval_schema`:

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_EVALUATION_DATA(
  'eval_db',
  'eval_schema',
  'evaluated_agent',
  'CORTEX AGENT',
  'run-1')
);
```

### Query traces for a single record

To access a single record from an evaluation trace, use the [GET\_AI\_RECORD\_TRACE (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_record_trace-snowflake-local) function. This function has the following required arguments:

- `database`: The database containing the agent.
- `schema`: The schema containing the agent.
- `agent_name`: The name of the agent.
- `agent_type`: `CORTEX AGENT` or `EXTERNAL AGENT`. This value is case-insensitive.
- `record_id`: The record ID to filter by.

This function returns a table of event data described in [Evaluation results table format](#label-cortex-agent-evaluations-results-format). The following example displays the trace for the record `9346efc3-5dd6-4038-9b1a-72ca3d3b768c`, where the agent is named `evaluated_agent` stored on the schema `eval_db.eval_schema`:

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_RECORD_TRACE(
  'eval_db',
  'eval_schema',
  'evaluated_agent',
  'CORTEX AGENT',
  '9346efc3-5dd6-4038-9b1a-72ca3d3b768c'
));
```

### Query evaluation errors and warnings for a run

To access logs for warnings and errors that happened during an evaluation run, use the [GET\_AI\_OBSERVABILITY\_LOGS (SNOWFLAKE.LOCAL)](/sql-reference/functions/get_ai_observability_logs-snowflake-local) function. This function has the following required arguments:

- `database`: The database containing the agent.
- `schema`: The schema containing the agent.
- `agent_name`: The name of the agent.
- `agent_type`: `CORTEX AGENT` or `EXTERNAL AGENT`. This value is case-insensitive.

This function returns a table of event data described in [Evaluation results table format](#label-cortex-agent-evaluations-results-format). The following example checks for errors and warnings for a run called `run-1`, where the agent is named `evaluated_agent` stored on the schema `eval_db.eval_schema`:

Copy code

```
SELECT * FROM TABLE(SNOWFLAKE.LOCAL.GET_AI_OBSERVABILITY_LOGS(
  'eval_db',
  'eval_schema',
  'evaluated_agent',
  'CORTEX AGENT')
)
  WHERE TRUE
  AND (record:"severity_text"='ERROR' or record:"severity_text"='WARN')
  AND record_attributes:"snow.ai.observability.run.name"='run-1';
```

Note

The fields of `record` and `record_attributes` are subject to change, but the fields `record:"severity_text"` and `record_attributes:"snow.ai.observability.run.name"` are guaranteed to be present in AI Observability logs.

## Interpret score variance across runs

An evaluation run doesn’t replay a stored trace. For each input in your dataset, the run invokes your agent again through the Cortex Agents API and scores the trace that invocation produces. Version pinning fixes the two configurations around that trace:

- An [agent version](#label-cortex-agent-evaluation-yaml-spec) fixes the configuration that’s invoked: the agent’s instructions, tools, and orchestration model.
- A [metric version](#label-agent-evaluation-metric-versions) fixes the judge that scores the result: its model, prompt, rubric, and thresholds.

Neither one pins the trace. Agent orchestration is non-deterministic, so repeated runs of the same dataset against the same pinned agent version and metric version can take different tool paths and produce different scores.

Snowflake benchmarks the system metric judges for high scoring consistency: judging the same trace more than once returns the same score, or one very close to it. Treat score movement across runs as a signal about your agent rather than about the metric:

- `answer_correctness` grades the final response against your ground truth and is usually the most stable metric, because different paths often arrive at the same answer.
- `tool_selection_accuracy`, `tool_execution_accuracy`, and `logical_consistency` read the trace, so they expose path variability that `answer_correctness` hides. Movement in these metrics usually means the agent planned or invoked tools differently from one run to the next.
- `tool_selection_accuracy` uses no judge at all. If its score changes between runs, the agent’s tool calls changed.

Tip

Before you gate a CI/CD pipeline on a threshold, run the same dataset several times to learn its normal range, then gate on that range instead of a single run’s exact score. Use [Compare evaluation runs](#label-agent-evaluation-compare-runs) with **Hide unchanged metrics** to find which inputs move between runs: a few unstable inputs tell you more about where to fix your agent than a shifted average does. Pin a committed agent version, and name the orchestration model explicitly instead of using `auto`, so a configuration change never gets mistaken for agent variance.

## Agent Evaluation YAML specification

To define the YAML file to configure an Agent Evaluation, including defining custom metrics, there are three top-level keys:

- (Optional) `dataset`: A definition of how to create a dataset for the evaluation. This value is optional when using a YAML specification to start an evaluation in Snowsight, or when using an existing dataset.
- `evaluation`: Settings for the agent to be evaluated.
- `metrics`: The metrics recorded during an evaluation run, including definitions for custom metrics.

### Dataset definition

The `dataset` value defines a new dataset from existing table data, mapping columns for the input query and ground truth. For the structure required for your `ground_truth` column, see [Dataset format](#label-agent-evaluation-dataset-format). The keys for the `dataset` value are:

- `dataset_type`: The string constant “CORTEX AGENT”. This value is case-insensitive.
- `table_name`: The fully qualified name of the table to use for the dataset’s contents.
- `dataset_name`: The name of the created dataset.
- `column_mapping`: The mapping of the required evaluation input column `query_text` and output column `ground_truth` to columns of the table to create the dataset from.

The resulting dataset is stored in the same database and schema as the table it’s constructed from.

Important

When you call [EXECUTE\_AI\_EVALUATION](/sql-reference/functions/execute_ai_evaluation) with `START` and the YAML still contains `dataset:`, Snowflake attempts to **create** the dataset on every run. If a dataset with the same `dataset_name` already exists, the run can fail (for example with an error that a dataset or internal dataset version already exists). That can happen even when you only change `run_name` between runs, or after a previous attempt failed after the dataset was created.

**Pattern for repeated runs on the same dataset:** Remove the entire `dataset:` top-level block from the YAML. Keep `evaluation:` (with `source_metadata` referencing the existing `dataset_name`) and `metrics:`. This matches how you run another evaluation against an existing dataset without re-importing the table.

**When you need a new dataset** from the same or updated source table (for example after you change rows), use a **new** `dataset_name` in `dataset:`, or create a dataset with [SYSTEM$CREATE\_EVALUATION\_DATASET](/sql-reference/functions/system_create_evaluation_dataset) and reference that name in `evaluation.source_metadata` without embedding `dataset:` in the YAML you use for the run.

The following example dataset definition shows a dataset named `evaluation_input` created from the `evals_db.evals_schema.evaluation_data` table, using the `user_question` as input and `expected_outcome` to define ground truth:

Copy code

```
dataset:
  dataset_type: "CORTEX AGENT"
  table_name: "evals_db.evals_schema.evaluation_data"
  dataset_name: "evaluation_input"
  column_mapping:
    query_text: "user_question"
    ground_truth: "expected_outcome"
```

### Agent configuration

The `evaluation` value sets the configuration for the agent to conduct an evaluation against. The keys for the `evaluation` value are:

- `agent_params`: A dictionary describing the agent to conduct the evaluation for. This value uses the keys:

  - `agent_name`: The name of the agent to evaluate.
  - `agent_type`: The string constant “CORTEX AGENT”. This value is case-insensitive.
  - (Optional) `agent_version`: The version of the agent to evaluate. This key accepts the same identifiers as an agent request: a system version name such as `VERSION$3`, an alias such as `production`, or one of the shortcuts `LIVE`, `FIRST`, `LAST`, and `DEFAULT`. See [Cortex Agent versioning](/user-guide/snowflake-cortex/cortex-agents-versioning).
- (Optional) `run_params`: Metadata for identifying this evaluation run. This value uses the keys:

  - (Optional) `label`: The label for this evaluation.
  - (Optional) `description`: A detailed description of the evaluation.
- `source_metadata`: A dictionary describing the dataset used for the evaluation. This value uses the keys:

  - `type`: The string constant `dataset`. This value is case-sensitive.
  - `dataset_name`: The name of the dataset to use.

When you omit `agent_version`, the evaluation targets the same version that an unversioned agent request targets. For an agent that has a single version, that’s the live version. Once the agent has two or more committed versions, it’s the agent’s default version.

Tip

Pin a committed version for evaluations you want to compare over time. Because the live version is mutable, two runs against it can score differently for reasons that have nothing to do with your dataset. An alias such as `production` resolves to one version for each run, but later runs can target a different version if the alias is reassigned. Targeting a committed version such as `VERSION$3` keeps the configuration under test fixed across scheduled or CI/CD evaluations.

Pinning a version fixes the agent configuration that’s scored, not the agent behavior that gets scored. Each run re-invokes the agent, so every run produces a new trace. For what that means for run-to-run scores, see [Interpret score variance across runs](#label-agent-evaluation-score-variance).

The following example agent configuration runs the `production` alias of an agent named `evaluated_agent` with the label `Basic evaluation`, using the dataset `evaluation_input`:

Copy code

```
evaluation:
  agent_params:
    agent_name: "evaluated_agent"
    agent_type: "CORTEX AGENT"
    agent_version: "production"
  run_params:
    label: "Basic evaluation"
  source_metadata:
    type: "dataset"
    dataset_name: "evaluation_input"
```

Note

Note that the agent name is relative to the current database and schema. You can also provide the fully qualified name of the agent.

### Metrics selection

The `metrics` value is a sequence of metrics to evaluate, including your own custom metric definitions. The accepted values for pre-defined metrics are:

- `answer_correctness`: Measure how closely the expected ground truth answer for a given input query matches the actual response streamed from the agent.
- `tool_selection_accuracy` (Public Preview): Measure whether the agent invoked the expected tools to arrive at the final response. Scoring is deterministic for a given set of tool calls.
- `tool_execution_accuracy` (Public Preview): Measure the input and output quality of the tools called to arrive at the final response.
- `logical_consistency`: Measure consistency across agent instructions, planning, and tool calls. This metric is *reference-free* and doesn’t use a dataset.

#### System metric versions

All four system metrics accept a version: `answer_correctness`, `logical_consistency`, `tool_selection_accuracy`, and `tool_execution_accuracy`. For the metrics scored by an LLM judge, a metric version pins the judge model and the prompt, rubric, and thresholds used to produce a score, so the same trace scores consistently from one run to the next. A metric version pins the judge, not the trace the judge reads: see [Interpret score variance across runs](#label-agent-evaluation-score-variance). `tool_selection_accuracy` accepts a version and records it with the run, but its scoring is deterministic for a given set of tool calls, so its scores don’t vary by version. List a metric as a plain string to accept the current default version, or as a mapping with `name` and `version` to pin one:

Copy code

```
metrics:
  # Current default version (same as version: "auto")
  - "logical_consistency"

  # Latest minor version within major version 3
  - name: "answer_correctness"
    version: "v3"

  # Pinned to an exact minor version
  - name: "tool_execution_accuracy"
    version: "v3_0"

  # Accepted and recorded, but scoring is deterministic
  - name: "tool_selection_accuracy"
    version: "v3"
```

Version identifiers use the format `v<major>` or `v<major>_<minor>`:

- A **major** version marks a new judge model family or a significant prompt restructuring.
- A **minor** version is written and published by Snowflake for prompt tuning, threshold calibration, or scoring rubric refinements within the same model. Currently, each major version has only minor version `_0`: `v1_0`, `v2_0`, and `v3_0`. Snowflake might publish additional minor versions in the future.
- Naming only the major version resolves to the latest minor version within it, so `v3` picks up refinements as they ship. Naming both, such as `v3_0`, freezes the metric at that exact configuration.
- The value `auto`, like omitting `version`, uses the current default version.

The following major versions are available. Specify only the major version to automatically use future minor refinements. Specify the full major and minor version to keep the same configuration.

| Version | Judge models | Notes |
| --- | --- | --- |
| `v1` | `claude-4-sonnet` (200K) | The current default version. |
| `v2` | `claude-sonnet-4-5` (200K, default), `openai-gpt-5.2` (400K) | Adds a GPT judge for accounts that don’t allow Anthropic models. |
| `v3` | `claude-sonnet-4-6` (1M, default), `openai-gpt-5.4` (1.05M) | The larger context window reduces the odds of context window overload. |

Expand

Show lessSee more

Snowflake recommends `v3` when you evaluate long traces. `logical_consistency` sends the whole trace to its judge, so an agent that makes many tool calls per input is the most likely to approach a judge’s context window on the smaller `v1` and `v2` judges.

For system metrics, you select the metric version, not the underlying judge model. Snowflake selects the judge model for that version based on the models your account allows, using [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference). If both judge models are allowed and available, Snowflake uses the Anthropic model. To select a specific judge model, define a custom metric and set its `model` key. If none of a version’s judge models are available in your region or allowed by your account’s model settings, the run fails with an error rather than silently substituting a different model. Choose a version whose models your account allows, and see [Judge model availability](#label-agent-evaluation-judge-models) for what’s available where.

##### Versions and model deprecations

A metric version depends on its judge model, so metric versions follow Snowflake model deprecations. Snowflake retires models in two stages, **legacy** then **end-of-life**, and a legacy judge model is already restricted:

- **After a judge model’s legacy date**, only accounts that used that model before the legacy date can run a metric version that depends on it. If your account had never used the model, a run that resolves to that version fails. This applies to the `v1` default: `claude-4-sonnet` entered the legacy state on August 12, 2026, so accounts with no prior `claude-4-sonnet` usage must pin `v2` or `v3`. For details, see [Cortex Agents models](/user-guide/snowflake-cortex/cortex-agents#label-cortex-agents-models).
- **After a judge model’s end-of-life date**, no account can use a metric version that depends on it.
- **Unversioned metrics and `auto`** roll forward to the newest supported version when their current version is deprecated. Your evaluations keep running, but scores can shift when the judge model changes.
- **Pinned versions** don’t roll forward. After the deprecation date, a run that pins a deprecated version fails with an error.

Snowflake recommends pinning a version in scheduled and CI/CD evaluations so that alert thresholds stay meaningful, then upgrading deliberately when a model deprecation is announced. Use the latest metric version and keep using that same version across runs: scores from different versions aren’t comparable, and the Evaluations tab treats each version as a separate chart and column. Model deprecations are announced as [unbundled behavior changes](/release-notes/bcr-bundles/un-bundled/unbundled-behavior-changes).

#### Defining a custom metric

You can define your own custom metric by providing an identifier, prompt, and score ranges. The prompt you provide is passed to an LLM judge along with run traces to conduct your custom evaluation. Custom metrics use the following key-value pairs, all required except where noted:

- `name`: The name of the metric.
- (Optional) `model`: The LLM judge that scores this metric, such as `claude-sonnet-4-6`. Custom metrics accept any of the judge models listed in [Judge model availability](#label-agent-evaluation-judge-models). Omitting this key, or setting it to `auto`, uses the model Snowflake selects for your account, which is `claude-4-sonnet` today and rolls forward when that model is deprecated. Because `claude-4-sonnet` is [legacy](/user-guide/snowflake-cortex/cortex-agents#label-cortex-agents-models), an account that never used it before the legacy date can’t rely on that default: set `model` explicitly to a supported judge. A model that isn’t a supported judge, that your account isn’t allowed to use, or that isn’t available in your region, fails the run at start with an error.
- `score_ranges`: A mapping that defines low, medium, and high-quality score ranges. This mapping uses the keys:

  - `min_score`: The score range used to identify low-quality results, as a two-element sequence of the inclusive lower bound to exclusive upper bound.
  - `median_score`: The score range used to identify medium-quality results, as a two-element sequence of the inclusive lower bound to inclusive upper bound.
  - `max_score`: The score range used to identify high-quality results, as a two-element sequence of the exclusive lower bound to inclusive upper bound.
- `prompt`: The prompt template to pass to the LLM judge along with the agent run trace data.

  > Important
  >
  > This template must include a scoring mechanism which produces a numeric value represented in the ranges provided for `score_ranges`.

A custom metric’s prompt is able to reference the trace data generated by the agent during an evaluation run. Snowflake passes the entire trace as input to the LLM judge, but you can emphasize certain information by using a replacement string that references data in a GET\_AI\_RECORD\_TRACE column directly. The following replacement strings are available:

| Replacement string | GET\_AI\_RECORD\_TRACE column |
| --- | --- |
| `{{input}}` | INPUT |
| `{{output}}` | OUTPUT |
| `{{ground_truth}}` | GROUND\_TRUTH |
| `{{tool_info}}` | TOOL |
| `{{start_timestamp}}` | START\_TIMESTAMP |
| `{{duration}}` | DURATION\_MS |
| `{{span_id}}` | SPAN\_ID |
| `{{span_type}}` | SPAN\_TYPE |
| `{{span_name}}` | SPAN\_NAME |
| `{{llm_model}}` | LLM\_MODEL |
| `{{error}}` | ERROR |
| `{{status}}` | STATUS |

Expand

Show lessSee more

#### Metrics configuration example

The following example defines a metrics configuration that enables answer correctness pinned to metric version `v3` and logical consistency on the default version, and also defines a custom `relevance` metric which returns a score between 1 and 10 based on how ground truth compares against agent output:

Copy code

```
metrics:
  # Built-in metric pinned to a version
  - name: "answer_correctness"
    version: "v3"
  # Built-in metric on the current default version
  - "logical_consistency"
  # Custom metric with prompt and an explicit judge model
  - name: "relevance"
    model: "claude-sonnet-4-6"
    score_ranges:
      min_score: [1, 3]
      median_score: [4, 6]
      max_score: [7, 10]
    prompt: |
      Evaluate the relevance of the agent's response to the user's query.
      Rate from 1-10 where:
      1 = Completely irrelevant
      4 = Somewhat irrelevant
      6 = Neutral
      8 = Mostly relevant
      10 = Highly relevant and on-topic

      You can compare the {{output}} with the {{ground_truth}} to help you understand if the contents are relevant or not

      Consider:
      - Does the response address the user's question?
      - Is the information provided appropriate to the context?
      - Are there any tangential or off-topic elements?
```

### Full example configuration

Combining all of the previous example sections gives a full Agent Evaluation configuration:

Copy code

```
# Optional: Create dataset before running evaluation
dataset:
  dataset_type: "CORTEX AGENT"
  table_name: "EVALS_DB.EVALS_SCHEMA.EVALUATION_DATA"
  dataset_name: "EVALUATION_INPUT"
  column_mapping:
    query_text: "user_question"
    ground_truth: "expected_outcome"

# Evaluation task configuration
evaluation:
  agent_params:
    agent_name: "evaluated_agent"
    agent_type: "CORTEX AGENT"
    agent_version: "production"
  run_params:
    label: "Basic evaluation"
  source_metadata:
    type: "dataset"
    dataset_name: "EVALUATION_INPUT"

metrics:
  # Built-in metrics pinned to a version
  - name: "answer_correctness"
    version: "v3"
  - name: "logical_consistency"
    version: "v3"

  # Built-in metric on the current default version (simple string)
  - "tool_selection_accuracy"

  # Custom metric definition with an explicit judge model
  - name: "relevance"
    model: "claude-sonnet-4-6"
    score_ranges:
      min_score: [1, 3]
      median_score: [4, 6]
      max_score: [7, 10]
    prompt: |
      Evaluate the relevance of the agent's response to the user's query.
      Rate from 1-10 where:
      1 = Completely irrelevant
      4 = Somewhat irrelevant
      6 = Neutral
      8 = Mostly relevant
      10 = Highly relevant and on-topic

      You can compare the {{output}} with the {{ground_truth}} to help you understand if the contents are relevant or not

      Consider:
      - Does the response address the user's question?
      - Is the information provided appropriate to the context?
      - Are there any tangential or off-topic elements?
```

### Upload configuration to a stage

Agent Evaluation configurations are required to have a specific file format for Snowflake to parse them. The following snippet demonstrates creating the required `yaml_file_format` on the schema `evals_db.evals_schema`, then creates the stage `evaluation_config` to upload an agent configuration to. Creating these objects requires CREATE FILE FORMAT ON SCHEMA and CREATE STAGE ON SCHEMA, and the role that runs the evaluation needs READ on the stage:

Copy code

```
CREATE OR REPLACE FILE FORMAT evals_db.evals_schema.yaml_file_format
  TYPE = 'CSV'
  FIELD_DELIMITER = NONE
  RECORD_DELIMITER = '\n'
  SKIP_HEADER = 0
  FIELD_OPTIONALLY_ENCLOSED_BY = NONE
  ESCAPE_UNENCLOSED_FIELD = NONE;

CREATE OR REPLACE STAGE evals_db.evals_schema.evaluation_config
  FILE_FORMAT = evals_db.evals_schema.yaml_file_format;
```

Upload your configuration to a created stage through Snowsight by selecting **Ingestion** » **Add Data**, then **Load files into a Stage**. You can also use the SQL [PUT](/sql-reference/sql/put) command to upload a local YAML file. The following example demonstrates copying the local file `/Users/dev/evaluation_config.yaml` to the stage `evals_db.evals_schema.evaluation_config`:

Copy code

```
PUT file:///Users/dev/evaluation_config.yaml @evals_db.evals_schema.evaluation_config
  AUTO_COMPRESS='false'
  OVERWRITE=TRUE;
```

If you create your YAML in a [Workspace](/user-guide/ui-snowsight/workspaces), you can copy it from your active workspace to a stage. The following example copies the file `evaluation_config.yaml` from your workspace to the stage `evals_db.evals_schema.evaluation_config`:

Copy code

```
COPY FILES INTO @evals_db.evals_schema.evaluation_config
  FROM 'snow://workspace/USER$.PUBLIC.DEFAULT$/versions/live'
  FILES=('custom_metric_config.yaml');
```

Tip

Snowflake recommends keeping your YAML file uncompressed.

## Evaluation results table format

Functions which return information about a Cortex Agent evaluation all produce a table with the following columns:

| Column | Data type | Description |
| --- | --- | --- |
| RECORD\_ID | VARCHAR | The unique identifier assigned by Snowflake for this evaluation record. |
| INPUT\_ID | VARCHAR | The unique identifier assigned by Snowflake for this evaluation input. |
| REQUEST\_ID | VARCHAR | The unique identifier assigned by Snowflake for this request. |
| TIMESTAMP | TIMESTAMP\_TZ | The time (in UTC) at which the request was made. |
| DURATION\_MS | INT | The amount of time, in milliseconds, that it took for the agent to return a response. |
| INPUT | VARCHAR | The query string used as input for this evaluation record. |
| OUTPUT | VARCHAR | The response returned by the Cortex Agent for this evaluation record. |
| ERROR | VARCHAR | Information about any errors that occurred during the request. |
| GROUND\_TRUTH | VARCHAR | The ground truth information used to evaluate this record’s Cortex Agent output. This column holds the JSON from your dataset’s ground truth column, serialized as a string. For how `{{ground_truth}}` in custom metrics relates to this value, see the notes under [Evaluation results table format](/user-guide/snowflake-cortex/cortex-agents-evaluations#label-cortex-agent-evaluations-results-format). |
| METRIC\_NAME | VARCHAR | The name of the metric evaluated for this record. |
| EVAL\_AGG\_SCORE | NUMBER | The evaluation score assigned for this record. |
| METRIC\_TYPE | VARCHAR | The type of metric being evaluated. For built-in metrics, the value is `system`. For custom metrics, the value is `custom`. |
| METRIC\_STATUS | VARIANT | A map containing information about the agent’s HTTP response for this record, with the following keys:  - `status`: The HTTP status code of the response. - `message`: The HTTP message sent in the status response. |
| METRIC\_CALLS | ARRAY | An array of VARIANT values that contain information about the computed metric. Each array entry contains the metric’s criteria, an explanation of the metric score, and metadata. The keys of each entry are:  - `criteria`: The criteria used by an LLM judge to evaluate response correctness. - `explanation`: An explanation of why the score was assigned. - `full_metadata`: A VARIANT value that contains metadata and information about this metric’s processing by the LLM judge. The keys of this map include:   - `completion_tokens`: The number of output tokens generated by the LLM for this metric evaluation call.   - `normalized_score`: The original evaluation score normalized to the range [0.0, 1.0], rounded to two decimal places.   - `original_score`: The original score assigned by this metric evaluation for the record.   - `prompt_tokens`: The number of tokens taken up by the prompt provided to the LLM judge.   - `total_tokens`: The total number of tokens used by the LLM judge for this computation. |
| TOTAL\_INPUT\_TOKENS | INT | The total number of tokens used to process the input query. |
| TOTAL\_OUTPUT\_TOKENS | INT | The total number of output tokens produced by the Cortex Agent. |
| LLM\_CALL\_COUNT | INT | Counts the number of times any LLM was called, either by the agent or an evaluation judge. |

Expand

Show lessSee more

The `GROUND_TRUTH` column contains the full JSON from your dataset’s ground truth VARIANT, serialized as a string. In **custom metric** prompts, the `{{ground_truth}}` replacement string is substituted with that same serialized content, so a custom LLM judge can use any JSON shape you stored (not only keys such as `ground_truth_output` or `ground_truth_invocations`). **System metrics** still require JSON that matches what each metric expects (for example, `ground_truth_output` for answer correctness). For dataset column requirements, see [Dataset format](#label-agent-evaluation-dataset-format).

## Judge model availability

Agent Evaluations compute metrics with LLM judges, using [cross-region inference](/user-guide/snowflake-cortex/cross-region-inference). The following models are supported as judges. For system metrics, Snowflake chooses among the models belonging to the metric version you selected, based on the models your account allows. For custom metrics, you can name any of these models in the `model` key.

Availability is shown by cross-region routing scope (the value of the `CORTEX_ENABLED_CROSS_REGION` account parameter), not by individual region. A judge is available to your account when your routing scope is marked for that model. These are the same scopes listed in [Regional availability](/user-guide/snowflake-cortex/aisql-regional-availability#label-cortex-llm-availability).

| Model | Metric versions | Cross Cloud (Any Region) | AWS Global (Cross-Region) | AWS US (Cross-Region) | AWS US Commercial Gov (Cross-Region) | AWS US FedRAMP High Plus (Cross-Region) | AWS US DoD (Cross-Region) | AWS EU (Cross-Region) | AWS APJ (Cross-Region) | AWS AU (Cross-Region) | Azure Global (Cross-Region) | Azure US (Cross-Region) | Azure US FedRAMP High Plus (Cross-Region) | Azure EU (Cross-Region) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `claude-4-sonnet` | `v1` | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ |  |  |  |  |  |
| `claude-sonnet-4-5` | `v2` | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  |  | ✔ |  |
| `claude-sonnet-4-6` | `v3` | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ | ✔ |  |  |  |  |
| `openai-gpt-5.2` | `v2` | ✔ |  |  |  |  |  |  |  |  | ✔ | ✔ |  |  |
| `openai-gpt-5.4` | `v3` | ✔ |  |  |  |  |  |  |  |  | ✔ | ✔ |  | ✔ |

Expand

Show lessSee more

The GPT judges let accounts that don’t allow Anthropic models, such as Azure-only accounts, still run evaluations. No judge model runs on Google Cloud, so accounts there need `ANY_REGION`. If none of a metric version’s models are available to your account, the run fails with an error instead of falling back to another model; select a metric version whose models your account allows. For metric versions, see [System metric versions](#label-agent-evaluation-metric-versions).

Routing scope isn’t the only gate. `claude-4-sonnet`, the `v1` judge, is a [legacy](/user-guide/snowflake-cortex/cortex-agents#label-cortex-agents-models) model: only accounts that used it before its August 12, 2026 legacy date can use it as a judge, and no account can after its end-of-life date. Accounts without that prior usage must use `v2` or `v3`.

## Known limitations

Cortex Agent evaluations are subject to the following limitations:

- **Agent response times and throughput**: The number of inputs that can be processed during an evaluation is constrained by agent response times and the amount of trace detail. If you experience timeouts or long delays in your evaluation, split your evaluation dataset. For example, if you have queries which are guaranteed to invoke many different tools, you can partition your dataset by common tool invocation. If you have a custom evaluation metric that results in timeouts, refine or shorten your prompt. You may also want to consider splitting evaluations to only focus on one specific element of your agent’s output.
- **Ground truth staleness**: Depending on how you word your input queries, results may drift over time and result in less accurate evaluation results. In particular you should try and scope input queries to specific, absolute dates and times. As an example, both of the input queries `What was our revenue?` and `What was our revenue for the first quarter?` will experience drift, while the query `What was our revenue between January and March of 2026?` is scoped to a specific window of time that can be consistently referenced in the evaluation dataset.
- **MCP connectors**: Evaluations don’t currently support MCP servers as tools. The evaluation still runs, but the agent doesn’t call any MCP server tool during the run, so results won’t reflect MCP tool behavior.
- **Row access policies and session attributes**: You can’t currently evaluate an agent whose queries depend on [session attributes or variables](/user-guide/snowflake-cortex/cortex-agents-multi-tenancy), including agents that use those values with a row access policy. Evaluation runs don’t pass session attributes, so the agent’s results won’t match what users see in production.
- **Code execution tool**: Evaluations run agents that use the code execution tool. Code execution has no side effects during an evaluation: files the agent would write aren’t saved to your user stage, so you can’t currently evaluate those file outputs.
- **Tool selection and execution metrics**: Tool selection accuracy and tool execution accuracy score only the tools documented in [Tool selection and execution metrics ground truth](#label-cortex-agent-evaluation-tool-metrics). For other tools the agent may invoke, use answer correctness and logical consistency to evaluate the final response or overall behavior, or a [custom metric](#label-agent-evaluation-custom-metric) whose LLM judge can inspect traces for all tools.

## Cost considerations

Agent Evaluations run a Cortex Agent to create output for evaluation, and LLM judges to compute the evaluation metrics. You’re charged for each run of the agent against a ground truth query, and for the judge inference that scores each metric, at the rate of the [judge model for that metric version](#label-agent-evaluation-metric-versions). Additionally, you’re charged for the following:

- Warehouse charges for tasks used to manage evaluation runs
- Warehouse charges for queries used to compute evaluation metrics
- Storage charges for datasets and evaluation results
- Warehouse charges to retrieve evaluation results viewed in Snowsight

For more information on estimating costs, see [Understanding overall cost](/user-guide/cost-understanding-overall). Refer to the [Snowflake Service Consumption Table](https://www.snowflake.com/legal-files/CreditConsumptionTable.pdf) for full cost information.

### Track judge inference usage

Snowflake issues the judge inference calls for an evaluation through the Cortex REST API, so that usage is recorded in [CORTEX\_REST\_API\_USAGE\_HISTORY view](/sql-reference/account-usage/cortex_rest_api_usage_history).

To attribute judge usage to a particular evaluation run, join the request IDs recorded on the run’s `eval` spans to the `REQUEST_ID` column of the view. Each `eval` span carries its request IDs in the `ai.observability.eval.inference_request_ids` key inside the `ai.observability.eval.full_metadata` attribute:

Copy code

```
WITH eval_requests AS (
  SELECT
    record_attributes:"snow.ai.observability.run.name"::VARCHAR AS run_name,
    record_attributes:"ai.observability.eval.metric_name"::VARCHAR AS metric_name,
    ids.value::VARCHAR AS request_id
  FROM SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS,
    LATERAL FLATTEN(input => STRTOK_TO_ARRAY(
      PARSE_JSON(record_attributes:"ai.observability.eval.full_metadata"::VARCHAR)
        :"ai.observability.eval.inference_request_ids"::VARCHAR, ',')) AS ids
  WHERE record_attributes:"ai.observability.span_type"::VARCHAR = 'eval'
    AND record_attributes:"snow.ai.observability.run.name"::VARCHAR = 'run-1'
)
SELECT
  eval_requests.run_name,
  eval_requests.metric_name,
  rest_usage.model_name,
  rest_usage.tokens,
  rest_usage.tokens_granular
FROM eval_requests
INNER JOIN SNOWFLAKE.ACCOUNT_USAGE.CORTEX_REST_API_USAGE_HISTORY AS rest_usage
  ON rest_usage.request_id = eval_requests.request_id;
```

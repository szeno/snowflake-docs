# RLHF-like long-term memory for Cortex Agents

Turn thumbs-up/down feedback into human-approved lessons that a Cortex Agent retrieves at runtime, with a memory vs. no-memory accuracy eval.

|  |  |
| --- | --- |
| Stage | Operate, Evaluate, Build |
| Topics | AI Observability, Cortex Agents, Semantic Views |
| Status | GA |
| Time to complete | 45min |
| Edition | Enterprise |
| Regions | Any region with Cortex Agents, Cortex Search, SNOWFLAKE.CORTEX.COMPLETE, and the selected orchestration model |
| Privileges | ACCOUNTADMIN for 01\_setup.sql, 02\_grant\_unredacted.sql, and 99\_teardown.sql; the recipe role owns the remaining objects |
| Related skills | `agent-studio` (bundled with Cortex Code), `cortex-ai-function-studio` (bundled with Cortex Code) |
| Last verified | 2026-11-10 |
| Authors | Haebichan Jung |
| Code | [View all files](/developer-guide/cortex-ai-cookbook/agent-feedback-to-memory/code) or download [agent-feedback-to-memory.zip](/static/samples/cortex-ai-cookbook/agent-feedback-to-memory.zip), which includes this page as `README.md`. Teardown: [sql/99\_teardown.sql](/developer-guide/cortex-ai-cookbook/agent-feedback-to-memory/code#label-cookbook-agent-feedback-to-memory-sql-99-teardown-sql) |

Expand

Show lessSee more

This recipe is a reference implementation: review the code and adapt it to your environment before production use.

> Turning thumbs-up/down feedback from Snowflake Cortex Agents (and CoWork) into **human-approved long-term memory** that the agent retrieves at runtime. There are no weight updates; the agent learns from people through retrieval.

## When to use this

- Users keep hitting the same wrong answer because a business rule lives in people’s heads, such as which revenue measure counts, when the fiscal year starts, or which records are test data.
- You want the fix to come from user feedback and a named approver, and to apply only when a question needs it.

When not to use this:

- The rule applies to every question. Put it in the semantic view or the agent instructions instead.
- You need an evaluation dataset built from feedback. See [agent-feedback-to-evals](/developer-guide/cortex-ai-cookbook/agent-feedback-to-evals).
- You cannot grant a role access to conversation text. Without `READ UNREDACTED AI OBSERVABILITY EVENTS TABLE`, trace text is redacted and there is nothing to diagnose.

## How it works

Cortex Agents run on closed-weight models, so you can’t post-train them on user feedback. You *can* close the loop at inference time instead:

1. feedback is captured by the Cortex Agent **Feedback API**
2. **AI\_COMPLETE** joins it to the full trace and drafts a diagnosis (“case file”)
3. a **domain owner** reviews, edits and approves it as a *lesson*
4. approved lessons are indexed by **Cortex Search**
5. on every new question the agent retrieves the relevant lessons and follows them

---

[![RLHF-inspired memory pipeline](/static/images/cortex-ai-cookbook/agent-feedback-to-memory/diagrams/rlhf_memory_pipeline.png)](/static/images/cortex-ai-cookbook/agent-feedback-to-memory/diagrams/rlhf_memory_pipeline.png)

## Prerequisites

| Requirement | Notes |
| --- | --- |
| Cortex Agents, Cortex Analyst, Cortex Search, `SNOWFLAKE.CORTEX.COMPLETE` | The agents use `models.orchestration: auto`. The review app drafts case files with `claude-sonnet-4-5`; set `MODEL` at the top of `app/streamlit_app.py` to any model available in your region |
| `SNOWFLAKE.CORTEX_USER` | Granted to the recipe role by `01_setup.sql` |
| `READ UNREDACTED AI OBSERVABILITY EVENTS TABLE` | Account-level privilege granted to the recipe role only by `02_grant_unredacted.sql`. It lets the role read every conversation with every agent it can monitor, so grant it only to the role that reviews feedback |
| Snowflake CLI (`snow sql`) | Runs the scripts, including the `PUT` of the seed CSVs. Run from the recipe folder |
| Programmatic access token | Only for `eval/run_eval.py`; the connection’s password must be a PAT. You create it yourself for your own user |
| Python | `requests` and `snowflake-connector-python` for `client/agent_client.py` and the eval |

Expand

Show lessSee more

## Quickstart

From `agent-feedback-to-memory/`:

1. `snow sql -f sql/01_setup.sql`: role, warehouse, database, mock retail data, the naive semantic view, review queue, lessons, `LESSONS_SEARCH`, both agents, and `FEEDBACK_WITH_TRACE`. The three demo lessons are loaded.
2. `snow sql -f sql/02_grant_unredacted.sql` as `ACCOUNTADMIN`: lets the recipe role read trace text.
3. Ask the agent questions and send feedback with `client/agent_client.py` (see Usage).
4. Deploy `app/streamlit_app.py` as a Streamlit in Snowflake app to review feedback and approve lessons.
5. Run the accuracy eval: `python eval/run_eval.py --suite realistic --runs 2 --connection <conn>`.
6. `snow sql -f sql/99_teardown.sql` when done.

## Results

**Three approved lessons took the agent from 48% to 100% accuracy on 33 new questions, with no regressions and no added latency.**

The eval compares `RLHF_MEMORY_AGENT` against `BASELINE_NO_MEMORY_AGENT`. The baseline is identical (same semantic view, model, and instructions) except it has no `lessons_memory` tool. Every question ran twice per agent, and every answer was graded against ground truth computed in SQL. Grading is strict: only the headline figure counts.

### Realistic mix (33 new questions, none reuse a lesson’s wording)

|  | No memory | With memory |
| --- | --- | --- |
| **Overall accuracy** | 32/66 (**48%**) | 66/66 (**100%**) |
| Questions where a lesson applies | 0/34 (0%) | 34/34 (100%) |
| Questions no lesson applies to (regression check) | 32/32 (100%) | 32/32 (100%) |
| Mean latency | 19.0s | 19.4s |

Expand

Show lessSee more

By lesson: test-order exclusion 0/30 → 30/30, net revenue 0/24 → 24/24, fiscal calendar 0/14 → 14/14.

- **Lessons generalize.** Every question was new, with different periods, regions, categories and metrics (AOV, revenue per unit, top month, top fiscal quarter).
- **No regressions.** On questions no lesson applies to (product/store facts, channel-scoped metrics), the extra context changed nothing.
- **No latency cost.** The added Cortex Search call is within run-to-run noise.

### Targeted set (16 questions built around the traps)

|  | No memory | With memory |
| --- | --- | --- |
| The lessons’ own questions | 0/6 | 6/6 |
| New questions hitting a trap | 4/22 | 22/22 |
| Controls (no trap) | 4/4 | 4/4 |
| **Overall** | 8/32 (**25%**) | 32/32 (**100%**) |

Expand

Show lessSee more

The baseline’s 4 “passes” on trap questions were luck: it used the wrong fiscal year but still named the right top category/region.

### Caveats

- Synthetic data with three planted rules. The overall number depends on the question mix; here about half the questions hit a rule.
- This measures whether **approved** lessons fix and generalize. It does not measure how quickly the loop discovers new problems.
- The obvious alternative, hand-writing the same rules into the agent instructions, would likely score the same. The case for memory is that fixes come from user feedback with an owner’s approval, and lessons load only when relevant.

### Walkthrough example

Expected answers before and after the three lessons, checked against SQL ground truth. Agent wording and rounding vary between runs:

| Question | Before | After | Ground truth |
| --- | --- | --- | --- |
| Total revenue, calendar year 2025 | $4.95M *(gross, test orders included)* | $2,910,668 | $2,910,668 |
| Revenue, Q1 FY2026 | $1.26M *(used Jan–Mar 2026)* | $710,794 *(Feb–Apr 2025, net)* | $710,794 |
| Orders in 2025 | 11,450 *(test orders included)* | 10,891 | 10,891 |
| West region sales, Q3 FY2026 | — | $215,029 | $215,029 |
| Footwear orders, FY2026 | — | 2,705 | 2,705 |

Expand

Show lessSee more

The two questions each needed **two lessons combined**, which shows the memory generalizes beyond the exact question that got the thumbs-down.

---

## Architecture

```
 ┌───────────────────────────── 1. CAPTURE ─────────────────────────────┐
 │                                                                      │
 │  User ──asks──▶ Cortex Agent ──answers──▶ User: thumbs up/down       │
 │                       │                   + comment                  │
 │                       ▼                       ▼                      │
 │        ┌─────────────────────────────────────────────────────────┐   │
 │        │        SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS          │   │
 │        │                                                         │   │
 │        │  Trace spans (per turn)        CORTEX_AGENT_FEEDBACK    │   │
 │        │  question · planning ·   ◀──── positive · message ·     │   │
 │        │  tool calls · SQL ·      join  categories ·             │   │
 │        │  results · answer        on    orig_request_id ·        │   │
 │        │                          req   thread_id                │   │
 │        └────────────────────────────┬────────────────────────────┘   │
 └─────────────────────────────────────┼────────────────────────────────┘
                                       ▼
 ┌──────────────────────── 2. DIAGNOSE (AI_COMPLETE) ───────────────────┐
 │                                                                      │
 │   feedback + full trace ──▶ AI_COMPLETE drafts a "case file":        │
 │      • What happened   (summed GROSS_REVENUE for Q3)                 │
 │      • Likely issue    (user meant NET_REVENUE)                      │
 │      • Proposed fix    (default revenue → NET_REVENUE)               │
 │      • Suggested tier  (Tier 1 promote / Tier 2 memory)              │
 │      • Confidence + open questions                                   │
 └─────────────────────────────────────┬────────────────────────────────┘
                                       ▼
 ┌─────────────────────────── 3. REVIEW (human gate) ───────────────────┐
 │                                                                      │
 │   Routed by agent / semantic view                                    │
 │                ▼                                                     │
 │   ┌──────────────────────────────┐    ┌───────────────────────────┐  │
 │   │ Domain owner / data steward  │    │ Snowflake admin           │  │
 │   │ judges correctness:          │    │ governs the process:      │  │
 │   │ approve · edit · discard ·   │    │ access, unredacted grants,│  │
 │   │ choose tier                  │    │ approvals, retire stale   │  │
 │   └───────┬──────────────┬───────┘    └───────────────────────────┘  │
 └───────────┼──────────────┼───────────────────────────────────────────┘
   recurring │              │ long-tail /
  structural │              │ situational
 ┌───────────┼──── 4. STORE ┼───────────────────────────────────────────┐
 │           ▼              ▼                                           │
 │  ┌─────────────────────────┐   ┌─────────────────────────────────┐   │
 │  │ TIER 1: Source of truth │   │ TIER 2: Lesson memory           │   │
 │  │ Semantic View metrics,  │   │ LESSONS table → Cortex Search   │   │
 │  │ VQRs, synonyms,         │   │ (approved only, scoped,         │   │
 │  │ agent instructions      │   │  can be retired)                │   │
 │  │ → always applied        │   │ → retrieved when relevant       │   │
 │  └────────────┬────────────┘   └────────────────┬────────────────┘   │
 └───────────────┼─────────────────────────────────┼────────────────────┘
                 │                                 │
 ┌───────────────┼────────── 5. RUNTIME ───────────┼────────────────────┐
 │               │                                 │                    │
 │  New question ┼────────▶ retrieve top 3–5 similar lessons            │
 │               ▼                                 ▼                    │
 │      ┌───────────────────────────────────────────────────────┐       │
 │      │ Agent context = instructions + semantic view          │       │
 │      │               + relevant lessons + user question      │       │
 │      └──────────────────────────┬────────────────────────────┘       │
 │                                 ▼                                    │
 │                      Better answer ──▶ new feedback ──┐              │
 └───────────────────────────────────────────────────────┼──────────────┘
                                                         │
                 ◀────────── loops back to 1. CAPTURE ───┘

 ┌──────────────────────────── 6. MEASURE ──────────────────────────────┐
 │  Eval set of past questions → rerun before/after → % now correct     │
 │  (eval/run_eval.py; a formal Cortex Agent Evaluation is a next step) │
 └──────────────────────────────────────────────────────────────────────┘
```

### How it maps to RLHF

| RLHF | This design |
| --- | --- |
| Human preference labels | Thumbs-up/down feedback plus admin curation |
| Reward model | Admin judgment, with AI\_COMPLETE drafting each lesson |
| Weight update | Tier 1: permanent edits to semantic views / instructions |
| Policy behavior at inference | Tier 2: lessons retrieved into the prompt |
| Eval | Re-running past failed questions before vs. after |

Expand

Show lessSee more

### Data flow & permissions

```
AI_OBSERVABILITY_EVENTS ──▶ REVIEW_QUEUE (AI_COMPLETE case files, pending)
     (immutable, raw)               │  reviewer approves/edits
                                    ▼
                              LESSONS (approved only) ──▶ Cortex Search
```

| Role | Access |
| --- | --- |
| CoWork users | Only USAGE on the Cortex Search service (and the agent). No read or write on the LESSONS table. |
| Reviewers (domain owners) | Write access to the review queue and LESSONS, ideally only for their own domain. |
| Pipeline / admin | MONITOR on the agent and the unredacted-read grant to pull traces; owns the tables and the search service. |

Expand

Show lessSee more

LESSONS holds only sanitized guidance, never raw query results, so nothing sensitive from one user’s trace gets retrieved into another user’s context.

`LESSONS_SEARCH` does not filter by role or scope: every approved lesson is retrievable by anyone who can use the agent. If lessons must differ by team, add a filter on the `SCOPE` attribute in the agent’s search tool, or run one search service per domain.

Feedback text is untrusted input. It reaches AI\_COMPLETE verbatim, so a user can write feedback that tries to steer the drafted lesson. The human review step is the control here: nothing reaches the agent until a reviewer approves it, so read every draft before approving, and treat a lesson that changes access, filters, or tool use with extra suspicion.

---

## The experiment: planted traps

A retail dataset (20k orders, 10 stores, 12 products) with three ambiguities a naive semantic view gets wrong:

| Trap | Naive behavior | Business truth |
| --- | --- | --- |
| Revenue | `total_revenue = SUM(gross_amount)` | Net = gross − discounts − returns |
| Fiscal calendar | Q1 = Jan–Mar | FY starts **Feb 1** and is named by its end year (FY2026 = Feb 2025–Jan 2026) |
| Test orders | All rows counted | `channel = 'INTERNAL'` rows are test orders and are excluded |

Expand

Show lessSee more

The feedback was deliberately terse, the way real users write it:

- *“Wrong numbers. Revenue should be net, finance never reports gross.”*
- *“That’s not our Q1. Our fiscal year starts in February.”*
- *“Order count looks too high”* ← intentionally vague

---

## Key findings

- **AI\_COMPLETE didn’t invent business rules.** For the vague order-count complaint it flagged *“test orders, specific channels”* as an open question for the owner rather than asserting a rule. The reviewer supplied the `INTERNAL` fact, which supports keeping a human in the loop.
- **The reviewer edits drafts; they aren’t rubber stamps.** For the fiscal case AI\_COMPLETE proposed “ask the user about the fiscal year.” Once the owner confirmed the calendar, the reviewer replaced that with the actual rule.
- **Retrieval generalizes.** *“How much did the West region sell last fiscal quarter”* ranked the fiscal and revenue lessons at the top, though neither was written for that question.
- **The feedback event is thin; the trace is rich.** Feedback joins to the full trace on `RECORD_ATTRIBUTES:"ai.observability.record_id"`, which gives you the question, answer, SQL and results.

---

## Snowflake objects

All objects are in `COOKBOOK_AGENT_FEEDBACK_TO_MEMORY.RLHF_MEMORY`:

| Object | Type | Purpose |
| --- | --- | --- |
| `ORDERS`, `STORES`, `PRODUCTS`, `FISCAL_CALENDAR` | Tables | Dummy retail data with planted traps |
| `RETAIL_SALES_SV` | Semantic view | Deliberately naive baseline |
| `RLHF_MEMORY_AGENT` | Cortex Agent | Tools: `query_sales` (Analyst) + `lessons_memory` (Search) |
| `BASELINE_NO_MEMORY_AGENT` | Cortex Agent | Eval baseline: same spec without `lessons_memory` |
| `FEEDBACK_WITH_TRACE` | View | Joins feedback events to trace spans |
| `REVIEW_QUEUE` | Table | AI\_COMPLETE case files awaiting review |
| `LESSONS` | Table | Approved long-term memory |
| `LESSONS_SEARCH` | Cortex Search service | Indexes approved lessons for retrieval |

Expand

Show lessSee more

---

## Repo contents

| File | What it is |
| --- | --- |
| `sql/01_setup.sql` | Recreates every Snowflake object: mock data, semantic view, review queue, lessons, search service, both agents, feedback view |
| `data/*.csv` | Mock retail data and the three demo lessons, loaded by `sql/01_setup.sql` |
| `client/agent_client.py` | Minimal REST client: `run` (agent `:run`) and `feedback` (agent `:feedback`) |
| `feedback.example.json` | Template for the `feedback` command: the three terse comments, with placeholder request IDs |
| `eval/run_eval.py` | Memory vs. no-memory accuracy eval (`targeted` and `realistic` suites) |
| `eval/results_*.json` | Every answer, headline, grade and latency from an eval run; `--regrade` re-scores them |
| `diagrams/rlhf_memory_pipeline.png` | Pipeline diagram |
| `app/streamlit_app.py` | Streamlit in Snowflake review app: pull feedback, edit/approve lessons, retire lessons |

Expand

Show lessSee more

### Usage

Copy code

```
# Recreate the demo (run from the recipe folder so the PUT paths resolve).
# This replaces COOKBOOK_AGENT_FEEDBACK_TO_MEMORY.RLHF_MEMORY, including any lessons
# you approved and the whole review queue.
snow sql -f sql/01_setup.sql -c <conn>

# Ask the agent questions (captures request_id, SQL, answer)
python client/agent_client.py --connection <conn> run --question "What was revenue in Q1 of fiscal year 2026?" --out runs.json

# Submit thumbs up/down feedback, the same API CoWork uses.
# Copy feedback.example.json to feedback.json and replace each request_id with one from runs.json.
python client/agent_client.py --connection <conn> feedback --file feedback.json

# Run the accuracy eval (connection's password must be a PAT)
python eval/run_eval.py --suite realistic --runs 2 --connection <conn>

# Re-score saved answers without calling the agents
python eval/run_eval.py --regrade eval/results_realistic.json
```

### Review app (Streamlit in Snowflake)

`app/streamlit_app.py` is the human-approval step as a single-file app. Create a new Streamlit in Snowflake app in Snowsight and paste it in.

| Tab | What it does |
| --- | --- |
| **Inbox** | **Pull new feedback** copies new rows from `FEEDBACK_WITH_TRACE` into `REVIEW_QUEUE` (deduplicated on `request_id`) and drafts a case file for each with `SNOWFLAKE.CORTEX.COMPLETE` |
| **Review** | Shows the question, feedback, answer, SQL and AI diagnosis with open questions. The reviewer edits the lesson, then approves or rejects it |
| **Memory** | Lists all lessons and retires stale ones (`status = 'RETIRED'`) |

Expand

Show lessSee more

No deploy step is needed after approval: `LESSONS_SEARCH` indexes only `status = 'APPROVED'` rows with a 1-minute target lag, so approved lessons reach the agent in about a minute.

- **Capture is incremental, not a stream.** Observability events come from a table function, so a stream can’t track them. The app deduplicates on `request_id` instead, so each pull adds only new feedback. To automate it, run the same capture and draft statements in a scheduled task.
- **Privileges.** The app runs as its owner role. That role needs read/write on `REVIEW_QUEUE` and `LESSONS`, MONITOR on `RLHF_MEMORY_AGENT`, the `READ UNREDACTED AI OBSERVABILITY EVENTS TABLE` privilege, and `SNOWFLAKE.CORTEX_USER`.
- **Model.** Set `MODEL` at the top of the file to any model available to `SNOWFLAKE.CORTEX.COMPLETE` in your region (default `claude-sonnet-4-5`).

## Next steps

- Port the eval to a formal **Cortex Agent Evaluation**
- Add a **held-out trap** with no lesson, then run it through the full loop (feedback → diagnose → approve) and show it get fixed
- Compare against putting the same rules directly in the agent instructions
- Demo a **Tier 1 promotion**: move the net-revenue lesson into the semantic view itself
- Schedule the review app’s capture and draft statements with a **task** so new feedback flows into the review queue automatically

## Verify

After `01_setup.sql`, `SELECT COUNT(*) FROM COOKBOOK_AGENT_FEEDBACK_TO_MEMORY.RLHF_MEMORY.LESSONS WHERE status = 'APPROVED'` returns 3 and `SHOW AGENTS IN SCHEMA COOKBOOK_AGENT_FEEDBACK_TO_MEMORY.RLHF_MEMORY` lists `RLHF_MEMORY_AGENT` and `BASELINE_NO_MEMORY_AGENT`.

Ask both agents “How many orders did we have in 2025?”. With the demo lessons, `RLHF_MEMORY_AGENT` should answer 10,891 (test orders excluded) and `BASELINE_NO_MEMORY_AGENT` 11,450. Net revenue for calendar 2025 is $2,910,667.75, and revenue for Q1 FY2026 is $710,794.20. Agent answers vary between runs, so treat one run as a sample. The eval reports baseline and memory accuracy over the 33 realistic questions.

## Gotchas

| Symptom | Cause | Fix |
| --- | --- | --- |
| REST calls fail TLS hostname checks | The account hostname contains an underscore | Replace `_` with `-` in the host, as `client/agent_client.py` does |
| Parsing the Feedback API response as JSON fails | The Feedback API returns HTTP 200 with an empty body, although the API reference shows a JSON confirmation | Check the status code; don’t parse the body |
| Case-file drafts come back NULL | With the case-file `response_format`, `AI_COMPLETE` returned NULL on most calls, while `SNOWFLAKE.CORTEX.COMPLETE` returned the object every time and raises a readable error on failure | The review app uses `SNOWFLAKE.CORTEX.COMPLETE` and reads `:structured_output[0]:raw_message`. The diagrams and findings say AI\_COMPLETE for the drafting step; either function plays that role |
| Trace question, answer and SQL read as redacted or NULL | Reading full trace text needs the `READ UNREDACTED AI OBSERVABILITY EVENTS TABLE` account privilege plus MONITOR on the agent | Run `sql/02_grant_unredacted.sql` |

Expand

Show lessSee more

## Teardown

`sql/99_teardown.sql` drops the database (tables, semantic view, search service, both agents), the warehouse and the role. Dropping the role removes the unredacted-events grant. Events already written stay in `SNOWFLAKE.LOCAL.AI_OBSERVABILITY_EVENTS`. If you deployed the review app outside this database, drop it separately.

## Run it with a coding agent

```
Install or enable the bundled agent-studio and cortex-ai-function-studio skills if they are not
already available. Then, from agent-feedback-to-memory/:
1. Run SELECT CURRENT_ACCOUNT(), CURRENT_REGION(), CURRENT_ROLE(), CURRENT_WAREHOUSE(); and show me the result.
   Stop if it is not the account I expect.
2. Run sql/01_setup.sql with snow sql -f from this folder so the PUT paths resolve (it switches to
   ACCOUNTADMIN for the role, warehouse and database).
3. sql/02_grant_unredacted.sql grants READ UNREDACTED AI OBSERVABILITY EVENTS TABLE ON ACCOUNT, an
   account-level privilege that exposes conversation text. Show me the statement and wait for my
   yes before running it.
4. Ask both agents "How many orders did we have in 2025?" with client/agent_client.py and compare
   the answers with the Verify section.
5. For the eval, I create a programmatic access token for my own user and set it as the connection
   password myself; never create, print, read, or store the token. Then run eval/run_eval.py.
6. When I say so, run sql/99_teardown.sql and confirm SHOW DATABASES, SHOW WAREHOUSES and
   SHOW ROLES LIKE 'COOKBOOK_AGENT_FEEDBACK_TO_MEMORY%' return nothing.
Never drop or alter objects that do not start with COOKBOOK_.
```

## Related skills

- `agent-studio` (bundled with Cortex Code): building, evaluating and optimizing agents and semantic views.
- `cortex-ai-function-studio` (bundled): choosing, testing and estimating the cost of the AI functions used here.

## References

- [Monitor Cortex Agent requests](/user-guide/snowflake-cortex/cortex-agents-monitor)
- [Feedback REST API](/user-guide/snowflake-cortex/cortex-agents-feedback-rest-api)
- [Create and manage agents](/user-guide/snowflake-cortex/cortex-agents-manage)
- [CREATE CORTEX SEARCH SERVICE](/sql-reference/sql/create-cortex-search)
- [COMPLETE (SNOWFLAKE.CORTEX)](/sql-reference/functions/complete-snowflake-cortex)
- [AI\_COMPLETE](/sql-reference/functions/ai_complete)
- [CREATE SEMANTIC VIEW](/sql-reference/sql/create-semantic-view)

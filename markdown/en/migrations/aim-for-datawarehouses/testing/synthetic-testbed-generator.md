# Synthetic testbed generator

The **synthetic testbed generator** builds constraint-aware table data and a query log from the converted workload. Use this path when the source data is unavailable for testing.

Use the Snowflake AIM Agent for Data Warehouses to generate and load a synthetic testbed, then compare source results with results from the converted workload on Snowflake. The synthetic testbed generator runs as part of the testing workflow; you don’t operate a separate tool. A live source connection is still required to capture baseline results.

Warning

Load **replaces rows in existing tables** on the connected source and in already-deployed Snowflake tables. It doesn’t create a new source schema. It targets the same tables the conversion artifacts describe. You need write privileges on those source tables. Use an isolated test environment with data you’re authorized to replace, not a production database. Before choosing testbed testing or requesting a reload, verify both connections and the affected tables.

## When to use

When you choose testbed testing during project setup (the Snowflake AIM Agent for Data Warehouses asks whether the source has representative production-like data, and you pick **No: generate a testbed**), it generates the testbed for you: table data and a query log, loaded before tests run. You don’t start a separate generator step.

On this path, you aren’t asked for a customer query-log CSV. Instead, the generated query log is used. For how that choice fits the rest of testing, see [Testing overview](/migrations/aim-for-datawarehouses/testing/overview).

## Prerequisites

Before selecting testbed testing, prepare the isolated source and Snowflake environments. Before loading, confirm the following:

- The migration project has conversion artifacts describing the tables to populate, and testbed testing is selected in setup.
- The source connection is live. You have permission to replace and load rows in the source tables identified by the conversion artifacts, and equivalent access to the target test tables on Snowflake.
- Converted Snowflake tables are **deployed**. Load doesn’t create Snowflake tables.

## What the generator produces

The Snowflake AIM Agent for Data Warehouses writes:

- One CSV per table under that object’s artifacts folder. Example:

  ```
  artifacts/<dialect>/<object>/testbed/<table>.csv
  ```
- A provenance summary at `.scai/testbed/manifest.json`. It lists each table’s data file (path relative to the project root), identity on both sides, and load order.
- A synthetic query log beside the manifest (`.scai/testbed/exec_log.csv`). On the testbed path, you aren’t asked for a customer query-log CSV; the Snowflake AIM Agent for Data Warehouses uses this generated log as test-case inputs.

Don’t edit `.scai/testbed/state.bin`. Changing it can break generation.

Generated rows are synthetic, so this path avoids copying production PII into the test tables.

## How loading behaves

Load replaces the rows in existing test tables. It doesn’t create Snowflake tables. Deploy converted tables first.

A table with no deployed Snowflake target is skipped on the Snowflake side only. Its source rows are still replaced. The Snowflake AIM Agent for Data Warehouses reports those tables in the load summary it shows you. Objects that read such a table will mismatch until you deploy the converted DDL and reload the testbed.

You can load only the source side first when you need that half before Snowflake. See [What to type](#what-to-type).

After the data is loaded, tests run as they do on source data: the object runs on the source (now holding synthetic rows) to record expected results, then the converted object runs on Snowflake against the same loaded data. For that loop, see [Testing stored procedures and UDFs](/migrations/aim-for-datawarehouses/testing/sprocs-and-udfs).

## What to type

Setup still generates and loads the testbed automatically after you choose testbed testing. Use these prompts later to regenerate, reload, or load only one side.

You normally drive this conversationally. For example:

```
"Generate the synthetic testbed"
"Load the testbed into the source and Snowflake"
"Load the testbed into the source only"
"Regenerate the testbed"
```

These are examples, not required commands. Nearby wording works as well.

## Row volume and repeatability

Generation uses mined defaults. After generating, the Snowflake AIM Agent for Data Warehouses shows a summary with row counts per table.

You can ask it to regenerate with a specific row count or seed. The same seed produces the same data, so test baselines stay comparable across runs.

## Verify the load

After generate, confirm:

- The Snowflake AIM Agent for Data Warehouses showed row counts that match what you expect.

After load, confirm:

- `.scai/testbed/manifest.json` lists every table you meant to load, in load order.
- Any tables skipped on the Snowflake side are ones you haven’t deployed yet. Their source rows were still replaced.

Then capture and validate can run. See [Testing stored procedures and UDFs](/migrations/aim-for-datawarehouses/testing/sprocs-and-udfs).

## Clean up

There is no unload command. Load has already replaced rows in the source tables it targeted, and in already-deployed Snowflake tables.

Validate itself runs against a clone of the workload database, so the validate run doesn’t leave extra synthetic rows behind. Load already wrote synthetic rows into the deployed Snowflake tables. See [Testing overview](/migrations/aim-for-datawarehouses/testing/overview).

To restore the source tables, reload original data yourself from a backup or a prior export. To restore the Snowflake tables, use Time Travel on the affected targets, or ask the Snowflake AIM Agent for Data Warehouses to load the testbed again. A reload re-clears those tables and copies from the same generated CSVs.

## Troubleshoot

- **Generation stops on unsatisfied constraints.** The Snowflake AIM Agent for Data Warehouses lists blocking issues. You can wait for it to resolve that list, or ask it to override after you’ve reviewed the list. Generation doesn’t write CSVs until one of those happens.
- **A Snowflake table was skipped.** Only the Snowflake half was skipped. Source rows for that table were still replaced. Deploy the converted DDL, then ask the Snowflake AIM Agent for Data Warehouses to load the testbed again. Until you do, objects that read that table can mismatch.
- **A load was interrupted.** The next load warns that a prior run left tables partially emptied. Recover by asking the Snowflake AIM Agent for Data Warehouses to load the testbed again. If the generated CSVs are gone, restore from a backup or Time Travel first.
- **Capture cannot record a baseline.** You still need a live source connection. See [Testing overview](/migrations/aim-for-datawarehouses/testing/overview).

## Related content

- [Testing overview](/migrations/aim-for-datawarehouses/testing/overview): testbed vs source-data testing, including the generated query log.
- [Testing stored procedures and UDFs](/migrations/aim-for-datawarehouses/testing/sprocs-and-udfs): the test loop that consumes the loaded testbed.
- [Considerations by source dialect](/migrations/aim-for-datawarehouses/testing/considerations-by-dialect): isolation model and privileges for tests.

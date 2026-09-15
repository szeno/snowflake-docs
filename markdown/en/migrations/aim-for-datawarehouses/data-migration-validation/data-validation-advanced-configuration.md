# Data validation advanced configuration

Validation workflows have a full YAML and TOML configuration surface documented in [Data validation configuration reference](../manual-migration/data-validation-configuration-reference). Most projects don’t need to hand-edit that file: the Snowflake AIM Agent for Data Warehouses generates it for you and walks through the settings that matter for your source platform, then shows you the result before anything runs.

This page describes common situations where you’ll want to go beyond the defaults, the prompt that gets you there, and where to find the exact property if you want to review or edit it yourself.

Tip

After the agent generates a validation workflow, it always shows you the YAML and asks whether you want to change anything before running it. You can request any of the scenarios below at that point, or ask for them up front.

## Choosing how deep to validate

Validation runs at up to three levels: schema (L1), aggregate metrics (L2), and row-level fingerprinting with cell drill-down (L3). L3 is the most resource-intensive and is disabled by default.

**Prompt:**

Copy code

```
Run full row-level validation on the ORDERS and CUSTOMERS tables, but keep the rest at schema and metrics validation only
```

The agent sets `row_validation: true` for the tables you named (globally it stays off). See [Validation levels](./data-validation#validation-levels).

## Re-validating only what changed

Scheduled re-validation of a large table doesn’t have to compare every partition every time. **Incremental validation** detects which partitions changed since the last run and re-validates only those. It’s read-only: nothing is written to the target.

**Prompt:**

Copy code

```
Set up incremental validation for the ORDERS table using the UPDATED_AT column, so nightly runs only re-check partitions that changed
```

The agent sets `synchronization.strategy` to `watermark` or `checksum` under `defaultTableConfiguration` so every table inherits it.

Note

`trackModifications` and `trackDeletions` are not supported for Data Validation.

See [Incremental validation](../manual-migration/data-validation-configuration-reference#incremental-validation) for the property shape, prerequisites, and what “Not validated” means on unchanged partitions. Review [Changes a checksum may not detect](../manual-migration/data-migration-configuration-reference#changes-a-checksum-may-not-detect) before choosing `checksum`.

## Stopping L3 early when a table is clearly failing

When row-level validation runs across many partitions, finishing every partition can be expensive after a table has already failed. **Early stopping** skips remaining partition work once enough mismatches have been ingested.

**Prompt:**

Copy code

```
Enable early stopping for row hashing on the ORDERS table, and stop after 200 mismatches
```

The agent sets `early_stopping_for_row_hashing: true` and lowers `max_failed_rows_number` on the tables you name (or globally, if you ask for that). See [Validation configuration](../manual-migration/data-validation-configuration-reference#validation-configuration) for all early-stopping options and defaults.

## Declaring expected source-to-target differences (accepted transformations)

Some value changes during migration are intentional (encoding normalization, NULL-to-empty-string coercion, status-code remapping) and shouldn’t be reported as failures. **Accepted transformations** allowlist specific source-to-target value pairs so AIM DMV does not treat matching diffs as L3 mismatches.

Accepted transformations apply only when **L3 row validation is enabled**:

- Tables **without** rules write `MISMATCH` directly from row hashing.
- Tables **with** rules use a provisional **`POSSIBLE_MISMATCH`** path until cell drill-down and reconcile complete. Rows that match an accepted rule are cleared; the rest become `MISMATCH`.

Rules can appear at the workflow root, under global `validation_configuration`, or on an individual table. Matching scopes are unioned. Each rule names either an exact `column` or a `columnPattern` regex, plus the expected `sourceValue` and `targetValue` (use `null` for SQL NULL).

**Prompt:**

Copy code

```
We intentionally remap STATUS = 'ACTIVE' on the source to STATUS = '1' on the target. Don't flag that as a mismatch.
```

The agent adds an `acceptedTransformations` rule at the appropriate scope.

### Caveat: `POSSIBLE_MISMATCH` after the workflow finishes

`POSSIBLE_MISMATCH` is temporary. Reconcile runs after cell drill-down and should leave either:

- no row (the diff matched an accepted transformation), or
- `MISMATCH` (a real problem that did not match any rule).

On a **completed** workflow, `ROW_VALIDATION_RESULTS` should not still contain `POSSIBLE_MISMATCH` for that table. Leftover provisional rows usually mean reconcile did not finish (for example the workflow failed or was canceled before the reconcile task ran). Treat them as incomplete validation, not as accepted diffs. Re-run validation for the affected tables, or investigate task status in the workflow, before deciding the table passed.

For the property shape and examples, see [Accepted transformations](./data-validation#accepted-transformations) and [Accepted transformations (configuration reference)](../manual-migration/data-validation-configuration-reference#accepted-transformations). To query provisional rows while a workflow is still running, see [The SNOWCONVERT\_AI database](./snowconvert-ai-database#provisional-mismatches-accepted-transformations).

## Customizing normalization for row-hashing and cell comparison

Validation wraps each column in a normalization expression before hashing (L3 row fingerprinting) and comparing cell values, so that benign formatting differences (trailing zeros, timezone representation, and similar) don’t show up as mismatches. Built-in templates cover common data types per platform, but you can override them when a specific column, naming pattern, or table needs different handling.

**Prompt:**

Copy code

```
The AMOUNT column keeps showing mismatches that look like formatting differences, not real data problems. Can we normalize it before comparing?
```

The agent proposes a normalization expression for that column (or column pattern, or data type, depending on scope) and adds a `validationCustomNormalizationRules` entry, either at the workflow root or scoped to just the affected table. See [Custom normalization rules](../manual-migration/data-validation-configuration-reference#custom-normalization-rules) for the property shape, matching precedence, and more examples (including geometry and legacy platform-specific types).

Note

An older, data-type-only normalization override (`validationCustomNormalizations`) still works, but new column- or pattern-scoped customizations should use `validationCustomNormalizationRules`. See [Custom normalization](../manual-migration/data-validation-configuration-reference#custom-normalization-validationcustomnormalizations-legacy) for the legacy form.

## Overriding partition and index keys

If you already know the columns to use, set them explicitly rather than relying on inference. Views can’t be inferred — see [Validating views](#validating-views).

**Prompt:**

Copy code

```
Partition LEGACY_ORDERS by ORDER_DATE, and align rows on ORDER_UUID
```

See [Automatic partition and index key selection](../manual-migration/data-validation-configuration-reference#automatic-partition-and-index-key-selection) for inference rules and the constraint that keys must be real physical column names.

## Validating views

Views go through the same L1, L2, and L3 pipeline as tables, but they don’t expose the catalog metadata AIM DMV uses to infer partition and index keys. When you validate a view, set those keys yourself and use a row filter so L2/L3 don’t scan an unbounded result.

**Choose a partition key that matches the underlying tables.** Prefer a column that would also be a good partition key on the base tables the view reads (for example the date or ID column that drives filters and joins in the view definition), not an arbitrary projected column. That keeps partition ranges meaningful and avoids uneven or ineffective chunking. For L3, also set an `indexColumnList` that uniquely identifies rows in the view result.

**Filter with a WHERE clause.** Views often expand to large joins. Use `sourceWhereClause` and `targetWhereClause` to limit the rows under validation, for example to a recent date range or an active subset. Set both sides: filtering only one compares different row subsets and reports mismatches that aren’t real.

**Prompt:**

Copy code

```
Validate the ORDERS_SUMMARY view. Partition by ORDER_DATE (same key as the ORDERS table the view is built on), align rows on ORDER_ID, and only validate the last 30 days
```

The agent sets `column_names_to_partition_by`, `indexColumnList`, `sourceWhereClause`, and `targetWhereClause` on the view entry. See [Automatic partition and index key selection](../manual-migration/data-validation-configuration-reference#automatic-partition-and-index-key-selection) and [Per-table and per-view entry](../manual-migration/data-validation-configuration-reference#per-table-and-per-view-entry).

## Validating INTERVAL columns

Use the same `intervalHandling` value as the matching migration workflow: `"interval"` to compare as a native Snowflake `INTERVAL`, or `"varchar"` to compare as text. Neither option is universally better; the tradeoff is the same as during migration. On platforms such as PostgreSQL, `"interval"` means mixed year-month and day-time values were folded into `INTERVAL DAY TO SECOND` (losing calendar-accurate year-month precision), while `"varchar"` preserves the original interval text.

**Prompt:**

Copy code

```
The EVENTS table was migrated with intervalHandling set to varchar. Use the same setting for validation.
```

The agent sets `intervalHandling` on that table’s validation entry to match migration. A mismatch between migration and validation produces false mismatches, because the two sides are normalized differently. See [INTERVAL data type handling](../manual-migration/data-validation-configuration-reference#interval-data-type-handling).

## Reducing lock contention on the source

If validation reads are blocked by production writers, you can opt in to anti-locking query hints. This trades consistency guarantees (dirty reads) for reduced blocking, so use it only when locking is actually a problem.

On MVCC engines (Oracle, PostgreSQL, Redshift), readers don’t block writers and hints usually aren’t needed. On lock-based engines (SQL Server), `WITH (NOLOCK)` avoids blocking but allows dirty reads that can produce false `MISMATCH` results. The impact is usually **stronger at L3** (byte-exact row hashing) than at **L2** (aggregate metrics within tolerance). Teradata gets `LOCKING ROW FOR ACCESS` automatically (safe, not a dirty read).

**Prompt:**

Copy code

```
Source reads are getting blocked during validation. Can we reduce locking?
```

The agent explains the platform-specific tradeoff and, if you confirm, sets the appropriate `queryModifiers` (for example `WITH (NOLOCK)` on SQL Server). See [Anti-locking and query modifiers](../manual-migration/data-validation-configuration-reference#anti-locking-and-query-modifiers) for per-platform defaults and the pros and cons.

## Adjusting numeric tolerance for metrics

L2 aggregate comparisons (sum, average, and similar) use a relative tolerance by default, since floating-point and precision differences between platforms are expected.

**Prompt:**

Copy code

```
Our source and target use different floating-point precisions, so metric comparisons are noisy. Can we loosen the tolerance?
```

The agent sets `comparisonConfiguration.tolerance` to a value you agree on. See [Comparison configuration](../manual-migration/data-validation-configuration-reference#comparison-configuration).

## Overriding L2 metrics or L1 type mapping

**Prompt:**

Copy code

```
Add a stddev_pop metric for the BIT columns, and treat the Teradata PERIOD(DATE) type as VARCHAR(40) for schema comparison
```

The agent sets `validationCustomMetrics` and `validationCustomTypes` respectively. See [Custom metrics](../manual-migration/data-validation-configuration-reference#custom-metrics-validationcustommetrics) and [L1 type mapping overrides](../manual-migration/data-validation-configuration-reference#l1-type-mapping-overrides-validationcustomtypes).

When only one column needs a different expected type, for example because you deliberately migrated a `GEOGRAPHY` column to `VARIANT`, ask for a per-column rule instead and the agent sets `validationCustomTypeRules`. See [Per-column L1 type overrides](../manual-migration/data-validation-configuration-reference#per-column-l1-type-overrides).

Note

Validation type overrides are separate from migration’s `columnTypeMappings`. If you remapped types during migration, that setting doesn’t carry over: tell the agent what the target types actually are so validation expects them.

## Filtering rows or columns

**Prompt:**

Copy code

```
Only validate active customers, and skip the internal AUDIT_* columns
```

The agent sets `sourceWhereClause` and `targetWhereClause` to filter rows on both sides, and `column_selection_list` (with `use_column_selection_as_exclude_list` for the audit columns) to filter columns. See [Filtering compared rows](../manual-migration/data-validation-configuration-reference#filtering-compared-rows) and [Column filtering with regex patterns](../manual-migration/data-validation-configuration-reference#column-filtering-with-regex-patterns).

## Related content

- [Data validation](./data-validation)
- [Data validation configuration reference](../manual-migration/data-validation-configuration-reference)
- [Data migration advanced configuration](./data-migration-advanced-configuration)
- [The SNOWCONVERT\_AI database](./snowconvert-ai-database)
- [Glossary](./glossary)

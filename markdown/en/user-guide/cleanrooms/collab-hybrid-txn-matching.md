# Transaction matching across two parties

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## About this example

This example demonstrates a two-step pipeline for transaction matching inside a
Data Clean Room (DCR). Two parties bring their transaction datasets and identify
matching records without exposing raw data to each other.

The challenge at scale is memory: loading billions of rows into pandas exhausts
node memory before any matching logic runs. The pipeline addresses this by
splitting work across two layers:

1. **SQL pre-filter (Step 1):** A SQL template runs an exact-key join on the
   Snowflake warehouse. The hash join reduces billions of rows to a manageable
   candidate set in seconds with no memory constraints.
2. **Ray task matching (Step 2):** An [ML Jobs](/user-guide/cleanrooms/ml-jobs)
   template reads the reduced candidate set and distributes custom matching logic
   across Ray workers on a compute pool. Because the candidate set fits in memory,
   the Python script can run any matching algorithm: fuzzy scoring, clustering,
   entity resolution, or ML model inference.

**Other applications of this approach:**

- **Financial reconciliation:** Match payments and settlements across banks or
  payment processors on shared customer identifiers.
- **Fraud detection:** Identify overlapping suspicious transactions across
  institutions without sharing customer records.
- **Retail media measurement:** Join ad exposure logs with purchase transactions
  to measure campaign lift.
- **Insurance claims matching:** Correlate claims data across carriers and
  providers for duplicate detection.

**Roles:**

- **Owner (collaboration creator and analysis runner):** Registers the owner
  transaction data, stages the matching script, creates the collaboration,
  provisions the compute pool, and runs both pipeline steps.
- **Collaborator:** Registers the collaborator transaction data, reviews and
  joins the collaboration, and links the data offering.

**Pipeline:**

1. **SQL pre-filter:** Join both transaction tables on exact keys to produce a
   `cleanroom.match_candidates` table containing only candidate pairs.
2. **Ray matching:** Load the candidate set from `cleanroom.match_candidates`
   and distribute the custom matching function across Ray workers on a
   multi-node compute pool.

## Prerequisites

- Two accounts with the Data Clean Rooms environment installed. For cross-region
  deployments, enable [Cross-Cloud Auto-Fulfillment](/user-guide/cleanrooms/laf).
- Both parties’ transaction tables must use SHA-256 hashed join keys. Raw PII
  must be hashed before registration.
- The analysis runner account must have a [compute pool](/user-guide/cleanrooms/ml-jobs)
  available. `CPU_X64_L` is recommended for candidate sets in the tens of
  millions of rows.
- Generate sample data by running the
  [sample data generator notebook](/static/samples/clean-rooms/collab-hybrid-txn-matching-sample-generator.ipynb)
  in both accounts. Upload the notebook to Snowsight (**Notebooks** »
  **Import .ipynb file**), set the `DATABASE_NAME` and `SCHEMA_NAME` variables
  in the first code cell, then run all cells. The notebook creates:

  - `PROVIDER_TRANSACTIONS` in the owner account
  - `PARTNER_TRANSACTIONS` in the collaborator account
- Upload the [matching script (txn\_match.py)](/static/samples/clean-rooms/txn_match.py)
  to a stage in the owner account:

  Copy code

  ```
  PUT file://txn_match.py @<ml_code_db>.PUBLIC.ML_STAGE/match/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
  ```

  Copy code

  ```
  ALTER STAGE <ml_code_db>.PUBLIC.ML_STAGE REFRESH;
  ```

## Run the example

Download and run the following SQL worksheets in the owner and collaborator
accounts. The worksheets cover data offering registration, template and code spec
registration, collaboration creation, compute pool setup, and execution of both
pipeline steps.

- [Owner worksheet](/static/samples/clean-rooms/collab-hybrid-txn-matching-owner.sql):
  Run this in the owner account.
- [Collaborator worksheet](/static/samples/clean-rooms/collab-hybrid-txn-matching-collaborator.sql):
  Run this in the collaborator account.

Step 1 runs on the warehouse and completes in seconds:

Copy code

```
5501524 match candidates created
```

Step 2 runs on the compute pool and distributes matching across Ray workers:

Copy code

```
Reading match candidates from cleanroom.match_candidates...
Candidates loaded: 5,501,524 rows
Ray nodes: 2
Ray shutdown complete

=== RESULTS ===
Total matched: 509,792
  RETAIL          101,930 / 1,099,506 candidates
  GROCERY         101,988 / 1,098,032 candidates
  TRAVEL          101,996 / 1,101,394 candidates
  ENTERTAINMENT   101,990 / 1,101,782 candidates
  HEALTHCARE      101,888 / 1,100,810 candidates

Results written to cleanroom.match_results
```

## Customize the matching logic

The matching script (`txn_match.py`) reads from `cleanroom.match_candidates`,
distributes one Ray task per segment, and writes results to
`cleanroom.match_results`. The downloadable script includes date-proximity
matching. The simplified version below shows the structure of the function you
replace:

Copy code

```
def custom_match(segment, candidates_df):
    """
    Replace this function body with your matching algorithm.

    Input:  pandas DataFrame of candidates for one segment.
            Columns: HASHED_EMAIL_SHA256, PROVIDER_AMOUNT, PARTNER_AMOUNT,
                     SEGMENT, PROVIDER_DATE, PARTNER_DATE
    Output: dict with segment, candidates, matched, matches keys

    Examples:
      Fuzzy amount + date:
        abs(row["PROVIDER_AMOUNT"] - row["PARTNER_AMOUNT"]) / row["PROVIDER_AMOUNT"] < 0.05
        and abs((row["PROVIDER_DATE"] - row["PARTNER_DATE"]).days) < 7

      Statistical scoring:
        score = model.predict_proba(features)[0][1]
        if score > threshold

      Clustering:
        labels = DBSCAN(eps=0.3).fit_predict(features)
    """
    matches = []
    for _, row in candidates_df.iterrows():
        amount_ratio = (
            abs(row["PROVIDER_AMOUNT"] - row["PARTNER_AMOUNT"])
            / max(row["PROVIDER_AMOUNT"], 0.01)
        )
        if amount_ratio < 0.05:
            matches.append({
                "hashed_email": str(row["HASHED_EMAIL_SHA256"]),
                "segment": str(row["SEGMENT"]),
                "provider_amount": float(row["PROVIDER_AMOUNT"]),
                "partner_amount": float(row["PARTNER_AMOUNT"]),
            })
    return {
        "segment": segment,
        "candidates": len(candidates_df),
        "matched": len(matches),
        "matches": matches,
    }
```

To use a library not already in the container runtime (for example, `scikit-learn`
or `rapidfuzz`), add it to `pip_requirements` in the code spec:

Copy code

```
pip_requirements:
  - pandas
  - scikit-learn
  - rapidfuzz
```

Important

`get_active_session()` is only available in the main process of the ML Jobs
script. Don’t call it inside `@ray.remote` worker functions. All data reads and
writes must happen in the main process. Workers receive pandas DataFrames as
arguments and return plain Python dicts.

DCR views rename columns based on `schema_and_template_policies`. The
`join_standard` / `hashed_email_sha256` policy renames `HASHED_EMAIL` to
`HASHED_EMAIL_SHA256`. The `timestamp` category renames date columns to
`TIMESTAMP`. Always detect columns dynamically or use the renamed names.

# Lookalike audience modeling

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## About this example

The lookalike audience modeling example empowers you to discover and target new, high-value
customers who mirror your most profitable existing ones. By training a custom XGBoost machine
learning model within a Snowflake Collaboration Data Clean Room, you can significantly enhance
your marketing efforts without ever exposing or sharing raw data between parties.

An advertiser’s seed audience is joined with a publisher’s user features to train the classifier,
then the full publisher population is scored and the results are activated back — all without
either party exposing raw data or model code to the other.

This page covers two implementations of the same use case:

- **[Option 1: Python UDFs](#option-1-python-udfs)** — Runs training and scoring as warehouse-based
  Python UDFs. Well-suited for moderate-scale workloads using packages from the Anaconda bundle.
- **[Option 2: ML Jobs](#option-2-ml-jobs)** — Runs training and scoring as containerized jobs
  on a dedicated compute pool. Suited for large-scale workloads, GPU acceleration, and packages
  beyond the Anaconda bundle.

Note

The two options use different collaboration owners — the publisher owns in Option 1, the advertiser
owns in Option 2. This is intentional: the Collaboration API supports any role assignment. Either
party can own the collaboration, provide data, or run the analysis. The examples together
demonstrate that flexibility.

**Pipeline (both options):**

1. **Train:** Build an XGBoost model on the seed audience joined with publisher user features.
2. **Score:** Score the full publisher population using the trained model.
3. **Activate:** Send the scored lookalike audience to the publisher account.

**Key use cases:**

- **Customer acquisition:** Find new customers who are similar to your most valuable existing
  customers by building a predictive model on shared features.
- **Increase ROI:** Improve the return on investment of your marketing campaigns by targeting
  users who are statistically more likely to convert.
- **Expand market reach:** Discover new market segments based on feature patterns in your seed
  audience.
- **Personalized advertising:** Deliver more relevant ad experiences by targeting a data-driven
  lookalike audience rather than broad demographics.

---

## Prerequisites

Two accounts with the Data Clean Rooms environment installed. For cross-region deployments, enable
[Cross-Cloud Auto-Fulfillment](/user-guide/cleanrooms/laf).

Generate sample data in both accounts by running the sample data generator notebook:

[Sample data generator notebook](/static/samples/clean-rooms/collab-lookalike-sample-generator.ipynb)

Upload the notebook to Snowsight (Notebooks » Import .ipynb file), update the `DATABASE_NAME`
and `SCHEMA_NAME` variables in the first code cell, then run all cells. The notebook creates
`LAL_PUBLISHER_FEATURES` and `LAL_ADVERTISER_SEED_AUDIENCE` in both accounts.

---

## Option 1: Python UDFs

Training and scoring run as Python UDFs on a warehouse. The publisher owns the collaboration in
this example.

The publisher provides a data offering (user features), a [code spec](/user-guide/cleanrooms/resources-code-specs)
containing two Python UDFs (one for training, one for scoring), and three templates (train, score,
activate). The advertiser joins the collaboration, links their seed audience data, and runs the
three templates in sequence.

This option uses a 3-step workflow built using [internal tables](/user-guide/cleanrooms/multistep-flows).
Each step saves its results to an internal table in the clean room, and the next step reads from
that table. This gives the advertiser a decision point after each step:

1. **Train:** Build an XGBoost model on the seed audience. Review model quality (AUC, error rate)
   before proceeding.
2. **Score:** Score the full publisher population using the trained model. Review the audience
   size before activating.
3. **Activate:** Send the scored lookalike audience to the publisher account.

### Collaboration roles

| Collaborator | Roles | Actions |
| --- | --- | --- |
| Publisher | Owner, data provider | Registers a data offering (user features including membership status, age band, region, and activity level), a code spec with Python UDFs for model training and scoring, three templates (train, score, activate), and creates the collaboration. After the advertiser activates results, the publisher views and processes the lookalike audience data. |
| Advertiser | Analysis runner, data provider (to self) | Registers a data offering (seed audience with purchase amounts and segments). Joins the collaboration, links their data, and runs the 3-step pipeline: trains the model, scores the population, and activates the scored audience to the publisher. |

Expand

Show lessSee more

### Step 1: Run the publisher and advertiser worksheets

After generating sample data, download and run the publisher and advertiser worksheets. Run
these worksheets using the same role you used to generate the sample data.
[See instructions to upload a SQL worksheet into your Snowflake account](/user-guide/cleanrooms/tutorials-and-samples#label-dcr-list-of-sample-notebooks-and-worksheets).

- [Download the publisher worksheet](/static/samples/clean-rooms/collab-lookalike-publisher.sql).
- [Download the advertiser worksheet](/static/samples/clean-rooms/collab-lookalike-advertiser.sql).

---

## Option 2: ML Jobs

Training and scoring run as containerized jobs on a dedicated compute pool. The advertiser owns
the collaboration in this example.

This option runs the same pipeline as Option 1, but at production scale (hundreds of millions of
records across collaborating parties), warehouse-based UDFs can hit memory and concurrency limits.
ML Jobs runs the training and scoring on a dedicated compute pool with multiple nodes and can be
scheduled to refresh the model on any cadence: hourly, daily, or weekly.

Note

The analysis runner’s account requires the `CREATE COMPUTE POOL` privilege to create a compute
pool `FOR APPLICATION` and grant usage on it to the installed clean room application.

### Collaboration roles

| Collaborator | Roles | Actions |
| --- | --- | --- |
| Advertiser | Owner, analysis runner | Stages proprietary ML training and scoring code, registers the code spec, templates, and seed audience data offering, creates the collaboration, sets up the compute pool, and runs the three-step pipeline (train, score, activate). |
| Publisher | Data provider | Registers their user feature data offering, reviews and joins the collaboration, and processes the activation results. |

Expand

Show lessSee more

### Step 1: Upload ML scripts to the advertiser account

Upload the ML training and scoring scripts to a stage in the advertiser account:

- [Training script (lal\_train.py)](/static/samples/clean-rooms/lal_train.py)
- [Scoring script (lal\_score.py)](/static/samples/clean-rooms/lal_score.py)

Upload using one of the following methods:

- **SnowSQL or Snowflake CLI:**

  Copy code

  ```
  PUT file://lal_train.py @<ml_code_db>.PUBLIC.ML_LAL_STAGE/lal_project/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
  PUT file://lal_score.py @<ml_code_db>.PUBLIC.ML_LAL_STAGE/lal_project/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
  ```
- **Snowsight UI:** Navigate to Data » Databases, find your stage, and drag and drop the files
  into the stage directory.

After uploading, refresh the stage directory:

Copy code

```
ALTER STAGE <ml_code_db>.PUBLIC.ML_LAL_STAGE REFRESH;
```

### Step 2: Run the example

Download and run the following SQL worksheets in the advertiser and publisher accounts:

- [Advertiser worksheet](/static/samples/clean-rooms/collab-mljobs-lookalike-advertiser.sql):
  Stages ML code, registers the ML Jobs code spec, templates, and data offering, creates the
  collaboration, sets up the compute pool, runs the ML jobs pipeline, and activates results.
- [Publisher worksheet](/static/samples/clean-rooms/collab-mljobs-lookalike-publisher.sql):
  Registers the feature data offering, reviews and joins the collaboration, and processes the
  activation results.

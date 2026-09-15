# Multi-party incrementality measurement with automated HPO

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## About this example

This example demonstrates distributed hyperparameter optimization (HPO) for a retail media measurement model
inside a clean room. A retail media network (RMN) collaborates with a brand to measure the sales impact of
sponsored product campaigns. The model uses Snowflake’s native [HPO API](/developer-guide/snowflake-ml/container-hpo)
(`snowflake.ml.modeling.tune`) to automatically find optimal XGBoost parameters through Bayesian optimization.

While this example focuses on retail media measurement, the same HPO pattern applies to any ML workflow in a
clean room. The approach is model-agnostic: define a search space, run parallel trials, and train with the best
configuration.

**Other applications of this approach:**

- **Lookalike and propensity modeling:** Tune classifiers that score audiences for purchase propensity, churn risk,
  or lifetime value. Audience composition changes per campaign, so fixed hyperparameters degrade over time.
- **Incremental lift and causal measurement:** Optimize uplift models (T-Learner, X-Learner) that measure the causal
  impact of advertising on conversions. As signal loss from privacy regulation and third-party cookie deprecation
  accelerates, more advertisers are adopting clean-room-based measurement to prove campaign effectiveness.
- **Multi-touch attribution:** Optimize attribution model weights across impression, click, and conversion data from
  multiple parties.
- **Fraud and risk scoring:** Tune anomaly detection or gradient boosting models on combined signals across
  institutions in a clean room.

**Why HPO matters:**

- ML models in clean rooms are sensitive to hyperparameters. Small changes in tree depth or regularization can
  produce misleading results.
- Each campaign or audience segment has different composition and response patterns. Hyperparameters that worked
  for one run may not work for the next.
- Automated HPO per-run ensures reliable, reproducible results without manual intervention.

Note

This example uses the Snowflake-native HPO API (`snowflake.ml.modeling.tune`), which is bundled in the ML Jobs
container runtime. No additional packages are needed. The API supports Bayesian optimization,
random search, and grid search with configurable trial counts and concurrency.

**Roles:**

- **Brand (owner and analysis runner):** Brings their proprietary measurement model with HPO, creates the
  collaboration, runs the measurement pipeline, and receives the results.
- **Retail media network (data provider):** Provides shopper transaction data from their retail media platform.
  Reviews and joins the collaboration, then links the data.

**Pipeline:**

1. **HPO + Train:** Run 10-20 Bayesian optimization trials to find optimal XGBoost hyperparameters for a campaign
   measurement model. Train the final model with the best configuration.
2. **Score:** Score the full shopper population for per-user campaign impact (predicted purchase probability with
   ad exposure minus predicted purchase probability without exposure).
3. **Activate:** Send measurement results back to the brand for campaign optimization and reporting.

## Prerequisites

- Two accounts with the Data Clean Rooms environment installed. For cross-region deployments, enable
  [Cross-Cloud Auto-Fulfillment](/user-guide/cleanrooms/laf).
- Generate sample data by running the sample data generator notebook in both accounts:

  [Sample data generator notebook](/static/samples/clean-rooms/collab-mljobs-rmn-hpo-sample-generator.ipynb)

  Upload the notebook to Snowsight (Notebooks » Import .ipynb file), update the `DATABASE_NAME` and
  `SCHEMA_NAME` variables in the first code cell, then run all cells. The notebook creates:

  - `RMN_SHOPPER_TRANSACTIONS` — use this as the RMN data offering
  - `BRAND_CAMPAIGN_EXPOSURES` — use this as the brand data offering

  Run the notebook in both the RMN and brand accounts.
- Upload the ML training and scoring scripts to a stage in the brand account:

  - [HPO training script (rmn\_train\_hpo.py)](/static/samples/clean-rooms/rmn_train_hpo.py)
  - [Scoring script (rmn\_score.py)](/static/samples/clean-rooms/rmn_score.py)

  Upload using SnowSQL or the Snowflake CLI, then refresh the stage directory:

  Copy code

  ```
  PUT file://rmn_train_hpo.py @<ml_code_db>.PUBLIC.ML_RMN_STAGE/rmn_project/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
  PUT file://rmn_score.py @<ml_code_db>.PUBLIC.ML_RMN_STAGE/rmn_project/ AUTO_COMPRESS=FALSE OVERWRITE=TRUE;
  ```

  Copy code

  ```
  ALTER STAGE <ml_code_db>.PUBLIC.ML_RMN_STAGE REFRESH;
  ```

## Run the example

Download and run the following SQL worksheets in the brand and RMN accounts:

- [Brand worksheet](/static/samples/clean-rooms/collab-mljobs-rmn-hpo-brand.sql): Stages ML code,
  registers the code spec with HPO training and scoring jobs, creates the collaboration, sets up the compute pool,
  runs the HPO pipeline, and activates measurement results.
- [RMN worksheet](/static/samples/clean-rooms/collab-mljobs-rmn-hpo-rmn.sql): Registers the
  transaction data offering, reviews and joins the collaboration, and links the data.

The HPO training job logs show per-trial results as the optimization progresses:

Copy code

```
--- Starting Distributed HPO ---
Trial 1/10: AUUC=0.0312 | depth=5, lr=0.0842, n_est=120
Trial 2/10: AUUC=0.0456 | depth=7, lr=0.0234, n_est=85
Trial 3/10: AUUC=0.0523 | depth=4, lr=0.0567, n_est=150
...
--- HPO Complete ---
Best AUUC: 0.0523
Best params: {"max_depth": 4, "learning_rate": 0.0567, ...}
```

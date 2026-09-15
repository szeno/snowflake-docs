# Top Insights (Snowflake ML Functions)

Top Insights is an [ML Function](/guides-overview-ml-functions) for key driver analysis, helping you to identify
drivers of a metric’s change over time or explain differences in a metric among various verticals. Top Insights is
powered by a decision tree model that separates a dataset into segments that have different behavior in relation to the
metric you want to analyze. With a few lines of SQL, you can integrate Top Insights into your BI workflows to
automatically monitor segments responsible for changes in any metric.

Use cases for Top Insights include:

- *Time-series analysis:* Identify drivers of a metric’s change over time. For example, automatically identify the
  locations, salespeople, customers, verticals, and other factors that are responsible for a recent revenue shortfall.
- *Vertical analysis:* Identify the drivers of differences in a metric among various verticals. For example, to understand
  which user segments are responsible for differences in new user growth between the United States and EMEA countries,
  to help shape targeted marketing campaigns.

## About Top Insights

Top Insights uses a decision tree model that separates a dataset into segments that have different behavior in relation
to the metric you want to analyze. The algorithm analyzes inter-segment differences between the metric in the control
group and the test group.

- The control group consists of the data points the model will use as a baseline.
- The test group consists of points of interest to be analyzed.

Top Insights then produces a number of possible contributor combinations, which are filtered based on their significance
and distinctiveness. Top Insights does not return redundant segments.

Good candidate datasets for analysis with Top Insights typically have a large number of columns or dimensions used to
segment data that make it difficult to intuitively identify what segments influence a metric. Dimensions can be
categorical (location, market segment, etc.) or continuous (that is, quantitative, such as temperature or attendance).

A Top Insights model is a schema-level object. You only need one instance, since the instance does not hold any state.

Tip

Dimensions are inferred as categorical or continuous based on their type. Numeric values are taken to be continuous
dimensions, while string and boolean values are considered categorical. To use a numeric value as a categorical
dimension, cast it to a string.

## Required privileges

A TOP\_INSIGHTS instance is a schema-level object. Therefore, the role you use to create the instance must have the
CREATE SNOWFLAKE.ML.TOP\_INSIGHTS privilege on the schema where the instance is created. This privilege is similar to
other schema privileges like CREATE TABLE or CREATE VIEW.

If you are not the owner of the instance, you must have the USAGE privilege on it to be able to call its GET\_DRIVERS
method.

## Using Top Insights

To use Top Insights in your queries and pipelines, first create an instance of the [TOP\_INSIGHTS (SNOWFLAKE.ML)](/sql-reference/classes/top-insights)
class. The SQL statement below creates an instance named `my_insights`. Creating the instance does not require
any arguments.

Copy code

```
CREATE SNOWFLAKE.ML.TOP_INSIGHTS IF NOT EXISTS my_insights();
```

After creating an instance, you can use the GET\_DRIVERS method to extract key drivers from the dataset
you want to perform key driver analytics on. You pass the input data all in one piece (a
[reference](/sql-reference/references) to a single table, view, or query) and provide the names of the
metric and label columns within the input data as additional arguments. Categorical and continuous dimensions
are inferred by their type and do not need to be specified explicitly.

Copy code

```
CALL my_insights!get_drivers (
  INPUT_DATA => TABLE(my_table),
  LABEL_COLNAME => 'label',
  METRIC_COLNAMe => 'sales');
```

## Preparing data for Top Insights

To use Top Insights, make sure you have a Boolean label column that distinguishes rows that are part of the control
group (labeled FALSE) from rows in the test group (labeled TRUE). This column is usually derived from other values in
the dataset, such as a timestamp or the name of a vertical, so it is common to create a view to do this. The view is
also a good place to filter out columns that are not part of your analysis.

The example below, for time-series analysis, creates a view with a label column based on a date range. Specifically, it
labels records in the latest month as TRUE (test data) and all previous records as FALSE (control data). Top
Insights can then analyze the continuous and categorical dimensions that explain differences in month-to-month changes
for the specified metric.

Copy code

```
CREATE VIEW input_table_time_series_label (
  ds, metric, dim_country, dim_vertical, label ) AS
  SELECT
    ds,
    metric,
    dim_country,
    dim_vertical,
    ds >= dateadd(month, -1, current_date) AS label
  FROM input_table;
```

The following example, for vertical analysis, creates a view with a label column based on the country. Specifically, it
labels records in non-US countries as TRUE, and labels records in the USA as FALSE. Top Insights will then analyze the
continuous and categorical dimensions that explain differences in a metric between these population groups.

Copy code

```
CREATE VIEW input_table_vertical_label (
  ds, metric,  dim_country, dim_vertical, label ) AS
  SELECT
    ds,
    metric,
    dim_country,
    dim_vertical,
    dim_country <> 'USA' as label
  FROM input_table;
```

## Interpreting the results

Top Insights returns a row for each segment of interest it finds in your data. Each row contains a plain-English
description of the segment, which can contain multiple criteria (for example, “COUNTRY = france, not VERTICAL = fashion,
not VERTICAL = tech” might describe a single segment). For each segment, Top Insights provides the following values
which quantify how much the segment contributes to the changes between the control and the test group.

| Output column | Description |
| --- | --- |
| METRIC\_CONTROL | The total value of the metric in the control period in a specific segment. |
| METRIC\_TEST | The total value of the metric in the test period in a specific segment. |
| CONTRIBUTION | The absolute impact of the segment on the change in the metric. |
| RELATIVE\_CONTRIBUTION | The impact of the segment as a proportion of the overall change in the metric between test and control. |
| GROWTH\_RATE | The change in the metric in the segment as a proportion of the metric in the control group in the segment. |

Expand

Show lessSee more

The contribution, relative contribution, and growth rate may be negative, indicating that a segment has a negative impact.

## Cost considerations

Using Top Insights incurs compute costs. Execution time scales with the number of rows and dimensions processed. See
[Understanding compute cost](/user-guide/cost-understanding-compute) for general information about Snowflake
compute costs.

Top Insights performance does not generally benefit from using a larger warehouse than is needed to load all the data
being analyzed, which must fit into memory. Datasets that surpass about 1,000,000 rows and 1,000 columns may exhaust
memory. Snowflake recommends using a Snowpark-optimized warehouse rather than a larger standard warehouse.
Snowpark-optimized warehouses have more memory than standard warehouses of the corresponding size.

While instances of the Top Insights class are schema-level objects, they do not store any data and have negligible
impact on storage costs.

## Examples

The following examples demonstrate how to use Top Insights for time-series analysis and vertical analysis.

- [Time-series analysis example](#label-top-insights-time-series-example)
- [Vertical analysis example](#label-top-insights-vertical-example)

### Time-series analysis example

This example finds the segments contributing to differences in the metric between two time periods, specifically how
the country and vertical dimensions affect the metric after 2021.

Create the input table containing synthetic data for this example using the following SQL statements.

Copy code

```
CREATE OR REPLACE TABLE input_table(
  ds DATE, metric NUMBER, dim_country VARCHAR, dim_vertical VARCHAR);

INSERT INTO input_table
  SELECT
    DATEADD(day, SEQ4(), DATE_FROM_PARTS(2020, 4, 1)) AS ds,
    UNIFORM(1, 10, RANDOM()) AS metric,
    'usa' AS dim_country,
    'tech' AS dim_vertical
  FROM TABLE(GENERATOR(ROWCOUNT => 365));

INSERT INTO input_table
  SELECT
    DATEADD(day, SEQ4(), DATE_FROM_PARTS(2020, 4, 1)) AS ds,
    UNIFORM(1, 10, RANDOM()) AS metric,
    'usa' AS dim_country,
    'auto' AS dim_vertical
  FROM TABLE(GENERATOR(ROWCOUNT => 365));

INSERT INTO input_table
  SELECT
    DATEADD(day, seq4(), DATE_FROM_PARTS(2020, 4, 1)) AS ds,
    UNIFORM(1, 10, RANDOM()) AS metric,
    'usa' AS dim_country,
    'fashion' AS dim_vertical
  FROM TABLE(GENERATOR(ROWCOUNT => 365));

INSERT INTO input_table
  SELECT
    DATEADD(day, SEQ4(), DATE_FROM_PARTS(2020, 4, 1)) AS ds,
    UNIFORM(1, 10, RANDOM()) AS metric,
    'usa' AS dim_country,
    'finance' AS dim_vertical
  FROM TABLE(GENERATOR(ROWCOUNT => 365));

INSERT INTO input_table
  SELECT
    DATEADD(day, SEQ4(), DATE_FROM_PARTS(2020, 4, 1)) AS ds,
    UNIFORM(1, 10, RANDOM()) AS metric,
    'canada' AS dim_country,
    'fashion' AS dim_vertical
  FROM TABLE(GENERATOR(ROWCOUNT => 365));

INSERT INTO input_table
  SELECT
    DATEADD(day, SEQ4(), DATE_FROM_PARTS(2020, 4, 1)) AS ds,
    UNIFORM(1, 10, RANDOM()) AS metric,
    'canada' AS dim_country,
    'finance' AS dim_vertical
  FROM TABLE(GENERATOR(ROWCOUNT => 365));

INSERT INTO input_table
  SELECT
    DATEADD(day, SEQ4(), DATE_FROM_PARTS(2020, 4, 1)) AS ds,
    UNIFORM(1, 10, RANDOM()) AS metric,
    'canada' AS dim_country,
    'tech' AS dim_vertical
  FROM TABLE(GENERATOR(ROWCOUNT => 365));

INSERT INTO input_table
  SELECT
    DATEADD(day, SEQ4(), DATE_FROM_PARTS(2020, 4, 1)) AS ds,
    UNIFORM(1, 10, RANDOM()) AS metric,
    'canada' AS dim_country,
    'auto' AS dim_vertical
  FROM TABLE(GENERATOR(ROWCOUNT => 365));

INSERT INTO input_table
  SELECT
    DATEADD(day, SEQ4(), DATE_FROM_PARTS(2020, 4, 1)) AS ds,
    UNIFORM(1, 10, RANDOM()) AS metric,
    'france' AS dim_country,
    'fashion' AS dim_vertical
  FROM TABLE(GENERATOR(ROWCOUNT => 365));

INSERT INTO input_table
  SELECT
    DATEADD(day, SEQ4(), DATE_FROM_PARTS(2020, 4, 1)) AS ds,
    UNIFORM(1, 10, RANDOM()) AS metric,
    'france' AS dim_country,
    'finance' AS dim_vertical
  FROM TABLE(GENERATOR(ROWCOUNT => 365));

INSERT INTO input_table
  SELECT
    DATEADD(day, SEQ4(), DATE_FROM_PARTS(2020, 4, 1)) AS ds,
    UNIFORM(1, 10, RANDOM()) AS metric,
    'france' AS dim_country,
    'tech' AS dim_vertical
  FROM TABLE(GENERATOR(ROWCOUNT => 365));

INSERT INTO input_table
  SELECT
    DATEADD(day, SEQ4(), DATE_FROM_PARTS(2020, 4, 1)) AS ds,
    UNIFORM(1, 10, RANDOM()) AS metric,
    'france' AS dim_country,
    'auto' AS dim_vertical
  FROM TABLE(GENERATOR(ROWCOUNT => 365));

-- Data for the test group

INSERT INTO input_table
  SELECT
    DATEADD(day, SEQ4(), DATE_FROM_PARTS(2020, 8, 1)) AS ds,
    UNIFORM(300, 320, RANDOM()) AS metric,
    'usa' AS dim_country,
    'auto' AS dim_vertica
  FROM TABLE(GENERATOR(ROWCOUNT => 365));

INSERT INTO input_table
  SELECT
    DATEADD(day, SEQ4(), DATE_FROM_PARTS(2020, 8, 1))  AS ds,
    UNIFORM(400, 420, RANDOM()) AS metric,
    'usa' AS dim_country,
    'finance' AS dim_vertical
  FROM TABLE(GENERATOR(ROWCOUNT => 365));
```

Create a view with a label column based on the datestamp.

Copy code

```
CREATE OR REPLACE VIEW input_view AS (
    SELECT
        metric,
        dim_country as country,
        dim_vertical as vertical,
        ds >= '2021-01-01' AS label
    FROM input_table
);
```

Now analyze this data by calling the GET\_DRIVERS method of a TOP\_INSIGHTS instance.

Copy code

```
CREATE OR REPLACE SNOWFLAKE.ML.TOP_INSIGHTS my_insights_model()

CALL my_insights_model!GET_DRIVERS(
  INPUT_DATA => TABLE(input_view),
  LABEL_COLNAME => 'label',
  METRIC_COLNAME => 'metric'
)
```

The output resembles the following:

```
+---------------------------------------------------------------------+----------------+-------------+--------------+-----------------------+---------------+
| CONTRIBUTOR                                                         | METRIC_CONTROL | METRIC_TEST | CONTRIBUTION | RELATIVE_CONTRIBUTION |   GROWTH_RATE |
|---------------------------------------------------------------------+----------------+-------------+--------------+-----------------------+---------------|
| ["Overall"]                                                         |         128445 |      158456 |        30011 |         1             |  0.2336486434 |
| ["COUNTRY = usa"]                                                   |         116238 |      154574 |        38336 |         1.277398287   |  0.3298060875 |
| ["COUNTRY = usa","VERTICAL = finance"]                              |          64281 |       87423 |        23142 |         0.771117257   |  0.3600130676 |
| ["COUNTRY = usa","VERTICAL = auto"]                                 |          48930 |       66131 |        17201 |         0.5731565093  |  0.3515430206 |
| ["COUNTRY = usa","VERTICAL = tech"]                                 |           1543 |         503 |        -1040 |        -0.03465396021 | -0.6740116656 |
| ["COUNTRY = canada","VERTICAL = finance"]                           |           1538 |         482 |        -1056 |        -0.03518709806 | -0.6866059818 |
| ["COUNTRY = canada","VERTICAL = fashion"]                           |           1519 |         446 |        -1073 |        -0.03575355703 | -0.7063857801 |
| ["COUNTRY = france","VERTICAL = auto"]                              |           1534 |         460 |        -1074 |        -0.03578687814 | -0.7001303781 |
| ["COUNTRY = usa","not VERTICAL = auto","not VERTICAL = finance"]    |           3027 |        1020 |        -2007 |        -0.06687547899 | -0.6630327056 |
| ["COUNTRY = france","not VERTICAL = fashion","not VERTICAL = tech"] |           3100 |         962 |        -2138 |        -0.07124054513 | -0.6896774194 |
| ["COUNTRY = france","not VERTICAL = fashion"]                       |           4687 |        1456 |        -3231 |        -0.1076605245  | -0.689353531  |
| ["COUNTRY = france"]                                                |           6202 |        1947 |        -4255 |        -0.1417813468  | -0.68606901   |
| ["not COUNTRY = usa"]                                               |          12207 |        3882 |        -8325 |        -0.2773982873  | -0.6819857459 |
+---------------------------------------------------------------------+----------------+-------------+--------------+-----------------------+---------------+
```

Note

Since the input data is randomly generated, your results will differ from the results above.

The output is ordered by CONTRIBUTION, with the Overall segment always at the top. The CONTRIBUTOR column contains an
array of strings describing the segment; the rest of the columns quantify how that segment contributes to the metric value.
For more details, see [Interpreting the results](#label-top-insights-results).

In the example output above, simply being in the United States has the largest impact on the metric. Two additional
segments, based on the finance and automotive verticals within the United States, also have outsize impact. After those,
the contribution of the segments turns negative.

### Vertical analysis example

This example compares credit usage of companies in two regions, USA and EMEA, with a goal of understanding how credit
usage in each segment differs between the regions.

Create the input table containing synthetic data for this example using the following SQL statements.

Copy code

```
CREATE OR REPLACE TABLE vertical_input_table(
  region VARCHAR, industry VARCHAR, num_employee NUMBER, credits FLOAT);

INSERT INTO vertical_input_table
  SELECT
    'USA' as region,
    ['technology', 'finance', 'healthcare', 'consumer'][MOD(ABS(RANDOM()), 4)] as industry,
    UNIFORM(100, 10000, RANDOM()) as num_employee,
    UNIFORM(1000, 3000, RANDOM()) AS credits,
  FROM TABLE(GENERATOR(ROWCOUNT => 450));

INSERT INTO vertical_input_table
  SELECT
    'EMEA' as region,
    ['technology', 'finance', 'healthcare', 'consumer'][MOD(ABS(RANDOM()), 4)] as industry,
    UNIFORM(100, 10000, RANDOM()) as num_employee,
    UNIFORM(100, 5000, RANDOM()) AS credits,
  FROM TABLE(GENERATOR(ROWCOUNT => 350));
```

Create a view with a label column based on the region.

Copy code

```
CREATE OR REPLACE VIEW vertical_input_view AS (
    SELECT
        credits,
        industry,
        num_employee,
        region = 'EMEA' AS label
    FROM vertical_input_table
);
```

Now analyze this data by calling the GET\_DRIVERS method of a TOP\_INSIGHTS instance.

Copy code

```
CREATE OR REPLACE SNOWFLAKE.ML.TOP_INSIGHTS my_insights_model();

CALL my_insights_model!get_drivers(
  INPUT_DATA => TABLE(vertical_input_view),
  LABEL_COLNAME => 'label',
  METRIC_COLNAME => 'credits'
);
```

The output resembles the following:

```
+-------------------------------------------------------------------------------------------------------+----------------+-------------+--------------+-----------------------+------------------+|
| CONTRIBUTOR                                                                                           | METRIC_CONTROL | METRIC_TEST | CONTRIBUTION | RELATIVE_CONTRIBUTION |      GROWTH_RATE |
|-------------------------------------------------------------------------------------------------------+----------------+-------------+--------------+-----------------------+------------------|
| ["Overall"]                                                                                           |         896672 |      895326 |        -1346 |           1           |  -0.001501106313 |
| ["not INDUSTRY = consumer","NUM_EMPLOYEE <= 6248.0","NUM_EMPLOYEE > 4235.0"]                          |         141138 |       70337 |       -70801 |          52.601040119 |  -0.5016437813   |
| ["NUM_EMPLOYEE <= 6248.0","NUM_EMPLOYEE > 4235.0"]                                                    |         188770 |      127320 |       -61450 |          45.653789004 |  -0.3255284208   |
| ["not INDUSTRY = technology","NUM_EMPLOYEE <= 8670.0","NUM_EMPLOYEE > 7582.5"]                        |         100533 |       42925 |       -57608 |          42.799405646 |  -0.5730257726   |
| ["not INDUSTRY = consumer","NUM_EMPLOYEE <= 5562.5","NUM_EMPLOYEE > 4235.0"]                          |         103851 |       47052 |       -56799 |          42.198365527 |  -0.54692781     |
+-------------------------------------------------------------------------------------------------------+----------------+-------------+--------------+-----------------------+------------------+
```

Note

Since the input data is randomly generated, your results will differ from the results above.

The output is ordered by CONTRIBUTION, with the Overall segment always at the top. The CONTRIBUTOR column contains an
array of strings describing the segment; the rest of the columns describe how that segment contributes to the metric value.
For more details, see [<instance\_name>!GET\_DRIVERS](/sql-reference/classes/top-insights/methods/get_drivers).

In the example output above, you can see that the segments are based on the industry and the number of employees that
the customer has. Top Insights automatically selects such ranges for continuous dimensions. Customers of a certain size
(between about 4,000 and 6,000 employees) seem to have an outsize negative impact.

## Current limitations

- The input metric must be an individual observation or an aggregate.
- For categorical features having more than 25 values, Top Insights uses only the top 25 most influential values to create segments.
- Processing more than 100 million rows in a single job may exhaust memory, even with Snowpark-optimized warehouses.

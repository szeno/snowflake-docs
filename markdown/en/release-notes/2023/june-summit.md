# Summit announcements - Jun 26-29, 2023

The following major features and enhancements were announced during Summit 2023.

Important

This topic does not include every feature or enhancement announced during the Summit. In particular, it does not include features
and enhancements that were announced, but are not yet in public preview or generally available.

## New features

### Dynamic tables — *Preview*

We are pleased to announce the preview of Dynamic Tables.

Dynamic tables are the building blocks of declarative data transformation pipelines.
They significantly simplify data engineering in Snowflake and provide a reliable, cost-effective, and automated way to transform your data
for consumption. Instead of defining data transformation steps as a series of tasks and having to monitor dependencies and scheduling, you
can simply define the end state of the transformation using dynamic tables and leave the complex pipeline management to Snowflake.

For more information, see [Dynamic Tables](/user-guide/dynamic-tables/overview).

### Amazon S3-compatible storage — *General Availability*

We are pleased to announce the general availability of support for accessing data in Amazon S3-compatible storage. You can create
external stages for on-premises or other cloud storage services and devices that are highly compliant with the Amazon S3 REST API. With this
feature, you can efficiently manage, govern, and analyze your data regardless of where the data is stored.

For more information, see [Work with Amazon S3-compatible storage](/user-guide/data-load-s3-compatible-storage).

### Passing references for tables, views, functions, and queries to a stored procedure — *Preview*

We are pleased to announce the preview of the ability to pass references for tables, views, functions, and queries to a stored procedure.

A reference is a unique identifier for a table, view, function, or query. When you pass a reference to a stored procedure, the stored
procedure performs actions using the active role or secondary roles of the user who created the reference. For example, if you are calling
an owner’s rights stored procedure, you can create and pass in a reference to a table to allow the stored procedure to perform actions on
the table using your active role.

In addition, if the table, view, or function is not fully qualified, the name of the object is resolved by using the current database and
schema when the reference was created (i.e. the database and schema of the user who created the reference).

For more information, see [Passing references for objects and queries to stored procedures](/developer-guide/stored-procedure/stored-procedures-calling-references).

### Snowpark ML: Machine learning at scale — *Preview*

We are pleased to announce the preview of Snowpark ML. Snowpark ML is a set of Python tools, including SDKs and underlying infrastructure,
for building and deploying machine learning models within Snowflake. This preview includes preprocessing and modeling classes based on
popular machine learning libraries such as [scikit-learn](https://scikit-learn.org/stable/),
[xgboost](https://xgboost.readthedocs.io/en/stable/), and [lightgbm](https://lightgbm.readthedocs.io/en/stable/).

Snowpark ML works with [Snowpark Python](/developer-guide/snowpark/python/index). You use Snowpark DataFrames to hold your training or
test data and to receive your prediction results.

For more information, see [Snowflake ML: End-to-End Agentic Machine Learning](/developer-guide/snowflake-ml/overview).

### ML functions — *Preview*

We are pleased to announce the preview of three new analysis tools powered by machine learning algorithms.

These three features train a machine learning model on your time-series data to determine how a specified metric varies over time and
relative to other features. The model then provides insights and predictions based on the trends detected in the data.

- **Forecasting**: Predicts future metric values from trends in historical data.
- **Anomaly Detection**: Flags metric values that differ from typical expectations.
- **Contribution Explorer**: Helps you find dimensions and values that affect the metric in surprising ways.

For more information, see [ML Functions](/guides-overview-ml-functions).

### Native Applications Framework — *Preview*

We are pleased to announce the preview of the Native Apps Framework that enables you to create data applications that expand the
capabilities of other Snowflake features by sharing data and related business logic with other Snowflake accounts.

For more information, see [About the Native Apps Framework](/developer-guide/native-apps/native-apps-about) and [Tutorial: Developing an Application with the Native Apps Framework](/developer-guide/native-apps/tutorials/getting-started-tutorial).

### Custom event billing for applications — *Preview*

We are pleased to announce the preview of custom event billing, a usage-based pricing plan that providers can use to charge consumers for
usage of apps built with the Snowflake Native Apps Framework.

For more information, see [Paid listings pricing models](/collaboration/provider-listings-pricing-model) and [Adding Billable Events to Applications](/developer-guide/native-apps/adding-custom-event-billing).

### Marketplace Capacity Drawdown Program — *General Availability*

We are pleased to announce the general availability of the Marketplace Capacity Drawdown Program, which allows eligible customers with a
capacity contract at Snowflake to pay for listings with their committed capacity.

See [Pay for Snowflake Marketplace listings](/collaboration/consumer-listings-paying) for more information.

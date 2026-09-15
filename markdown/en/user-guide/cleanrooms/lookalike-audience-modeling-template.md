# Audience lookalike modeling

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## About the template

The audience lookalike modeling template empowers you to discover and target new,
high-value customers who mirror your most profitable existing ones. By employing custom machine learning models within a secure Snowflake
Data Clean Room, you can significantly enhance your marketing efforts. The process begins with identifying a *seed audience* (a curated
list of your best customers). The template then analyzes the distinct characteristics and behaviors of this seed audience to build a
predictive model. This model is subsequently used to score a much larger population, identifying individuals who, based on their data
profiles, are most likely to be interested in your products or services. The use of a data clean room ensures that this powerful analysis
can be performed in collaboration with partners without ever exposing or sharing the underlying raw data, guaranteeing privacy and security
for all parties involved. This allows for richer, more accurate modeling by combining insights from multiple data sources in a
privacy-compliant manner.

Specify your seed audience and select features to train a lookalike model. You can adjust boosting rounds and outlier trimming as needed to
optimize the model’s performance. The model is trained on the features of your seed audience and then used to score a larger population,
identifying individuals who are most likely to convert.

## Key use cases

- **Customer acquisition:** Find new customers who are similar to your most valuable existing customers.
- **Increase ROI:** Improve the return on investment of your marketing campaigns by targeting users who are more likely to be interested in
  your products or services.
- **Expand market reach:** Discover new market segments that you may not have previously considered.
- **Personalized advertising:** Deliver more relevant and personalized ad experiences to your target audience.

## Get the worksheets and template

These worksheets show how to create and run a clean room with a lookalike audience modeling template that you can use and modify. The
template includes a UI form so you can run the clean room either in code or in the clean rooms UI. The example enables the consumer to run
the analysis, and optionally to activate the results to the provider’s account.

Download the worksheets and install them in two separate Snowflake accounts in the same organization and the same cloud hosting
environment. [See instructions to upload a SQL worksheet into your Snowflake account](/user-guide/cleanrooms/tutorials-and-samples#label-dcr-list-of-sample-notebooks-and-worksheets).

To try out the templates with sample data, run the sample data generator first in both your provider and consumer accounts, to generate
sample data to use with the clean room.

- [Download the Python sample data table generator.](/static/samples/clean-rooms/lookalike-audience-sample-generator.py)
  Run this to generate data that can be used as sample data for the consumer and provider worksheets.
- [Download the consumer worksheet.](/static/samples/clean-rooms/lookalike-audience-modeling-c.sql)
- [Download the provider worksheet.](/static/samples/clean-rooms/lookalike-audience-modeling-p.sql)

# Last touch attribution

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## About the template

The last-touch attribution template provides a comprehensive last-touch
attribution analysis that allows businesses to measure the effectiveness of their marketing channels. By securely joining collaborator datasets in a Snowflake Data Clean Room, the analysis identifies the sequence of marketing touch points leading to a conversion.

The process involves joining collaborator 1 click data with collaborator 2 transaction data, ranking each touch point by time, and then attributing the
conversion to the most recent interaction. The final output aggregates key metrics like total conversions and conversion value by channel.
This helps businesses understand which channels are most effective at driving immediate conversions, enabling data-driven decisions for
optimizing marketing strategies and budget allocation.

This analysis attributes 100% of the conversion credit to the last marketing touch point a customer interacted with before converting. It
identifies the final click preceding a transaction and assigns the entire value of that conversion to that single channel.

This template activates the result of the collaborator 2 analysis to the collaborator 1 account.

## Key use cases

- **Channel performance analysis:** Identify which channels are driving the most conversions and have the highest conversion value.
- **Budget allocation:** Optimize marketing spend by allocating more budget to the channels that are performing well based on last-touch
  attribution.
- **Campaign optimization:** Understand the effectiveness of different campaigns in driving final conversions and optimize them for better
  performance.

## Get the worksheets and template

Download the worksheets and install them in two separate Snowflake accounts in the same organization and the same cloud hosting environment.
These worksheets show how to create and run a clean room with a last-touch attribution template that you can use and modify.
The example enables collaborator 2 to run the analysis, and optionally to activate the results to the collaborator 1 account.

### Step 1: Generate sample data

Generate sample data in both collaborator accounts by running the Python sample data generator.

[Download the Python sample data table generator](/static/samples/clean-rooms/last-touch-sample-generator.py).

Tip

To run the sample data generator:

1. In Snowsight, go to **Projects** > **Worksheets** > **+** > **Python Worksheet**.
2. Paste the contents of the downloaded `.py` file into the worksheet.
3. Set **Handler** to `main` and **Return type** to `String`.
4. Update the `DATABASE_NAME` and `SCHEMA_NAME` variables with your values.
5. Select **Run**.

### Step 2: Run the collaborator worksheets

After generating sample data, download and run the collaborator worksheets. Run these worksheets using the same role you used to generate the sample data.
[See instructions to upload a SQL worksheet into your Snowflake account](/user-guide/cleanrooms/tutorials-and-samples#label-dcr-list-of-sample-notebooks-and-worksheets).

- [Download the collaborator 1 worksheet](/static/samples/clean-rooms/last-touch-attribution-collab-1.sql).
- [Download the collaborator 2 worksheet](/static/samples/clean-rooms/last-touch-attribution-collab-2.sql).

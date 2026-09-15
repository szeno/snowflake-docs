# Inventory forecasting collaboration

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## About the template

The inventory forecasting template helps publishers and advertisers forecast ad inventory availability within a collaboration data clean
room. By analyzing advertiser demand against a publisher’s available ad supply and audience data, it allows for accurate prediction of
future ad impression opportunities. This helps publishers optimize ad allocation to prevent unsold inventory and maximize revenue, while
enabling advertisers to better plan campaigns by understanding available reach across key demographics and regions.

This example demonstrates a two-party collaboration where the publisher is the collaboration owner and provides a data offering and two
templates: an analysis template and an activation template. The advertiser joins the collaboration, links their own data, and runs both
templates.

## Collaboration roles

| Collaborator | Roles | Actions |
| --- | --- | --- |
| Publisher | Owner, data provider | Registers a data offering (historical sales data), an analysis template, and an activation template. Creates the collaboration. After the advertiser activates results, the publisher views and processes the activation data. |
| Advertiser | Analysis runner, data provider (to self) | Registers a data offering (current stock levels). Joins the collaboration, links their data, runs the analysis template to view forecast results, and runs the activation template to send results to the publisher. |

Expand

Show lessSee more

## Key use cases

- **Ad impression forecasting:** Forecast the number of available ad impressions for specific audience segments to improve campaign
  planning.
- **Audience targeting:** Identify and forecast the size of targetable audience segments to optimize ad spend and campaign reach.
- **Campaign pacing and delivery:** Ensure on-time and in-full campaign delivery by accurately forecasting ad inventory and preventing
  underspending.
- **Yield management:** Maximize revenue by forecasting high-demand ad inventory and adjusting pricing strategies accordingly.
- **Retail demand planning** (cross-industry example): A CPG brand forecasts consumer demand for a product in a specific region, helping a
  retail partner optimize stock levels to prevent running out of stock and improve sales.

## Get the worksheets and template

Download the worksheets and install them in two separate Snowflake accounts in the same organization and the same cloud hosting
environment. These worksheets show how to create and run a collaboration with an inventory forecasting template that you can use and
modify. The advertiser runs the analysis template to view forecast results, and optionally runs the activation template to send results to
the publisher’s account.

### Step 1: Generate sample data

Generate sample data in both your publisher and advertiser accounts by running the Python sample data generator.

[Download the Python sample data table generator](/static/samples/clean-rooms/collab-inventory-forecasting-sample-generator.py).

Tip

To run the sample data generator:

1. In Snowsight, go to **Projects** > **Worksheets** > **+** > **Python Worksheet**.
2. Paste the contents of the downloaded file into the worksheet.
3. Set **Handler** to `main` and **Return type** to `String`.
4. Update the `DATABASE_NAME` and `SCHEMA_NAME` variables with your values.
5. Select **Run**.

### Step 2: Run the publisher and advertiser worksheets

After generating sample data, download and run the publisher and advertiser worksheets. Run these worksheets using the same role you used to generate the sample data.
[See instructions to upload a SQL worksheet into your Snowflake account](/user-guide/cleanrooms/tutorials-and-samples#label-dcr-list-of-sample-notebooks-and-worksheets).

- [Download the publisher worksheet](/static/samples/clean-rooms/collab-inventory-forecasting-publisher.sql).
- [Download the advertiser worksheet](/static/samples/clean-rooms/collab-inventory-forecasting-advertiser.sql).

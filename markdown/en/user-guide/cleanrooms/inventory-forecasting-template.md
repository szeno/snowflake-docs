# Inventory forecasting

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## About the template

The inventory forecasting template helps publishers and advertisers forecast ad inventory availability within a secure data clean room. By
analyzing advertiser demand against a publisher’s available ad supply and audience data, it allows for accurate prediction of future ad
impression opportunities. This helps publishers optimize ad allocation to prevent unsold inventory and maximize revenue, while enabling
advertisers to better plan campaigns by understanding available reach across key demographics and regions.

The template analyzes consumer demand patterns against provider supply capacity to forecast inventory requirements by region and
demographics. This template is designed as a provider-run template.

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

The code below includes a worksheet that demonstrates how to install and run an inventory forecasting custom template. The provider
worksheet includes the custom template code that you can use or modify.

Download the worksheets and install them in two separate Snowflake accounts in the same organization and the same cloud hosting
environment. These worksheets show how to create and run a clean room with an inventory forecasting template that you can use and modify.
The template includes a UI form so you can run the clean room either in code or in the clean rooms UI. The example enables the consumer to
run the analysis, and optionally to activate the results to the provider’s account.
[See instructions to upload a SQL worksheet into your Snowflake account](/user-guide/cleanrooms/tutorials-and-samples#label-dcr-list-of-sample-notebooks-and-worksheets).

To try out the templates, run the sample data generator first in both your provider and consumer accounts, to generate sample data to use
with the clean room.

- [Download the Python sample data table generator](/static/samples/clean-rooms/inventory-forecasting-sample-generator.py).
  Run this to generate data that can be used as sample data for the consumer and provider worksheets.
- [Download the consumer worksheet.](/static/samples/clean-rooms/inventory-forecasting-c.sql)
- [Download the provider worksheet.](/static/samples/clean-rooms/inventory-forecasting-p.sql)

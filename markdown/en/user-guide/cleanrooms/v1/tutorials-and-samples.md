# Snowflake Data Clean Room tutorials, samples, and videos

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. Migrate to the
[Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) before the dates below.

- **2026-10-01:** New legacy clean rooms may not be created via the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **2027-02-01:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms may not be created via the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **2027-06-01:** Legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview)
  to create and manage clean rooms.

## Tutorials

Here are tutorials to try out using Snowflake Data Clean Rooms when you’re just getting started:

- [Basic UI tutorial, single account](/user-guide/cleanrooms/v1/tutorials/cleanroom-web-app-single-account-tutorial): Demonstrates a
  simple overlap analysis and consumer activation, using a single Snowflake account. Single account testing supports most, but not all
  clean room features. To test the full functionality of a clean room, must use multiple Snowflake accounts.
- [Basic UI tutorial, two accounts](/user-guide/cleanrooms/v1/tutorials/cleanroom-web-app-tutorial): Demonstrates a simple overlap
  analysis and provider activation using two Snowflake accounts.
- [Basic API tutorial, single account](/user-guide/cleanrooms/tutorials/cleanroom-api-tutorial-basic): Demonstrates using the API to
  create and run a custom template using a single Snowflake account.

## Sample notebooks and worksheets

Many of the use case topics include full running samples of Snowflake Data Clean Rooms as downloadable notebooks or worksheets. You
need a Snowflake account with the clean rooms API environment installed to run any of these samples, and you must be able to use the
SAMOOHA\_APP\_ROLE role.

Tip

- **To upload a notebook,** follow the [instructions for uploading a notebook](/user-guide/ui-snowsight/notebooks-create#label-snowsight-import-notebook-file).
- **To upload a worksheet:**
  1. Open the workspaces panel: In the navigation menu, select **Projects** » **Workspaces**.
  2. Upload the SQL worksheet: In the workspace menu, select **+ Add new** » **Upload Files**.

### List of sample files

- **Internal testing clean room:** Jupyter notebook demonstrating how to use a single account to act as both provider and consumer for
  testing purposes.

  - [Download the notebook](/static/samples/clean-rooms/internal-testing-cleanroom.ipynb)
- **Consumer-run analysis:** Code for running a basic consumer analysis clean room using separate provider and consumer accounts.

  - [Download the consumer worksheet](/static/samples/clean-rooms/c-run-analysis-c.sql)
  - [Download the provider worksheet](/static/samples/clean-rooms/c-run-analysis-p.sql)
- **Provider-run analysis:** Jupyter notebook showing how a provider can run an analysis in a clean room.

  - [Download the notebook](/static/samples/clean-rooms/provider-analysis-notebook.ipynb)
- **Consumer-run consumer activation:** Code for activating analysis results to the consumer’s own Snowflake account, with setup and
  activation for both consumer and provider.

  - [Download the consumer worksheet](/static/samples/clean-rooms/c-run-c-activation-c.sql)
  - [Download the provider worksheet](/static/samples/clean-rooms/c-run-c-activation-p.sql)
- **Consumer-run provider activation:** Code for activating analysis results to the provider’s Snowflake account, with setup and activation
  for both consumer and provider.

  - [Download the consumer worksheet](/static/samples/clean-rooms/c-run-p-activation-c.sql)
  - [Download the provider worksheet](/static/samples/clean-rooms/c-run-p-activation-p.sql)
- **Provider-run provider activation:** Code for provider-run analysis with provider activation.

  - [Download the consumer worksheet](/static/samples/clean-rooms/p-run-p-activation-c.sql)
  - [Download the provider worksheet](/static/samples/clean-rooms/p-run-p-activation-p.sql)
- **Consumer-defined templates:** Code for creating, submitting, and managing consumer-written templates in a clean room.

  - [Download the consumer worksheet](/static/samples/clean-rooms/consumer-template-c.sql)
  - [Download the provider worksheet](/static/samples/clean-rooms/consumer-template-p.sql)
- **Provider-defined templates:** Code for creating, managing, and using provider-created templates in a clean room.

  - [Download the consumer worksheet](/static/samples/clean-rooms/provider-template-c.sql)
  - [Download the provider worksheet](/static/samples/clean-rooms/provider-template-p.sql)
- **Consumer-written UDFs:** Code for uploading and using custom Python functions in a clean room.

  - [Download the consumer worksheet](/static/samples/clean-rooms/consumer-udf-c.sql)
  - [Download the provider worksheet](/static/samples/clean-rooms/consumer-udf-p.sql)
- **Provider-written UDFs:** Code for uploading and using provider-uploaded custom Python functions in a clean room.

  - [Download the consumer worksheet](/static/samples/clean-rooms/provider-udf-c.sql)
  - [Download the provider worksheet](/static/samples/clean-rooms/provider-udf-p.sql)
  - [Bulk UDF uploading example (single-account worksheet)](/static/samples/clean-rooms/upload-multiple-python-packages.sql)
- **UDF from stage:** Jupyter notebook demonstrating how to load user-defined functions from a Snowflake stage.

  - [Download the notebook](/static/samples/clean-rooms/udf_from_stage.ipynb)
- **Snowpark UDFs:** Code for creating and using Snowpark-based user-defined functions in clean rooms.

  - [Download the consumer worksheet](/static/samples/clean-rooms/snowpark-udf-consumer.sql)
  - [Download the provider worksheet](/static/samples/clean-rooms/snowpark-udf-provider.sql)
- **Consumer-written UDF run by the provider:** A UDF uploaded by the consumer can be run by the provider.

  - [Download the consumer worksheet](/static/samples/clean-rooms/p-run-c-uploaded-code-c.sql)
  - [Download the provider worksheet](/static/samples/clean-rooms/p-run-c-uploaded-code-p.sql)
- **Snowpark Container Services Integration:** Jupyter notebooks for integrating Snowpark Container Services in clean rooms.

  - [Consumer notebook](/static/samples/clean-rooms/spcs-consumer.ipynb)
  - [Provider notebook](/static/samples/clean-rooms/spcs-provider.ipynb)
  - [Spec and config files](/static/samples/clean-rooms/spcs-spec-and-config.zip)
- **Audience Overlap & Segmentation:** Jupyter notebook demonstrating the Audience Overlap & Segmentation template.

  - [Download the notebook](/static/samples/clean-rooms/overlap-segmentation.ipynb)

## Sample templates

Snowflake Data Clean Rooms provides a few sample templates that you can download as Snowflake worksheets and implement or customize using the clean rooms API:

Inventory forecasting template:
:   This template helps publishers and advertisers forecast ad inventory availability within a secure data clean room. [Learn more and download the worksheet.](/user-guide/cleanrooms/inventory-forecasting-template)

Last touch attribution template:
:   This template provides a comprehensive Last Touch Attribution analysis that allows businesses to measure the effectiveness of their marketing channels. [Learn more and download the worksheet.](/user-guide/cleanrooms/last-touch-template)

Audience lookalike modeling template:
:   This template empowers you to discover and target new, high-value customers who mirror your most profitable existing ones. [Learn more and download the worksheet.](/user-guide/cleanrooms/lookalike-audience-modeling-template)

## Videos

Our solutions engineers have created the following videos to demonstrate clean room usage. Watch them individually, or [subscribe to our playlist](https://www.youtube.com/playlist?list=PLavJpcg8cl1HrorP5u5VkoywZo5YMewxC).

[Native App Installation](https://youtu.be/FC4Ug95vepM?si=3TnuZDhOhl02V3LD):
:   How to install the Snowflake Data Clean Room environment in your account.

[Freeform SQL](https://youtu.be/847XBdAiam8?si=a9bAEmi8l566Qlbt):
:   How to make free-form SQL queries in Snowflake Data Clean Rooms.

[Editing A Clean Room](https://youtu.be/xMXrSiPBjrU?si=hBUO_1pi4d2hWyDr):
:   How to configure a clean room in the API or UI.

[Cross-Cloud Auto-Fulfillment](https://youtu.be/8BO2GwlZpJQ?si=mLQsLlq_GoAIS496):
:   How to enable Cross-Cloud Auto-Fulfillment in your clean rooms.

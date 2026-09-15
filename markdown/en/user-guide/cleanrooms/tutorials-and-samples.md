# Sample Worksheets and Videos

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## Tutorials

Here are tutorials to try out using Snowflake Data Clean Rooms when you’re just getting started:

- [Basic API tutorial, two accounts](/user-guide/cleanrooms/tutorials/collaboration-basic-api-tutorial): Demonstrates using the API to
  create and run a custom template using a single Snowflake account.
- [Basic UI tutorial, two accounts](/user-guide/cleanrooms/tutorials/collaboration-basic-ui-tutorial): Demonstrates using the
  Snowsight UI to create a collaboration, share data and templates, and run an analysis across two accounts.

## Video tutorials

The DCR team has created the following videos to walk you through the collaboration resources and how to manage collaborations:

- [Register Data Offerings](https://www.youtube.com/watch?v=J2CDeha0WVM) This tutorial walks through creating sample datasets, defining data offering specifications, and leveraging standardized schemas to streamline collaboration. Discover how to use join keys, metadata columns, and category types to prepare your data for secure, governed analysis across multiple parties.
- [Register Templates](https://www.youtube.com/watch?v=ZiFLqPcw9Ao) Learn how to build templates that enable secure multi-party data collaboration, from simple overlap analysis to complex three-party joins with aggregations to unlock advanced measurement use cases across multiple organizations while maintaining governance and control.
- [Manage Collaborations](https://www.youtube.com/watch?v=Z4wa69kfU8o) Learn how to manage secure data collaborations using Snowflake Data Clean Rooms across one, two, and three-party scenarios.

## Sample Worksheets

Many of the use case topics include full running samples of Snowflake Data Clean Rooms as downloadable notebooks or worksheets. You
need a Snowflake account with the clean rooms API environment installed to run any of these samples, and you must be able to use the
SAMOOHA\_APP\_ROLE role.

Tip

To upload SQL worksheets and notebooks, see [Create and work with files and folders](/user-guide/ui-snowsight/workspaces-working).

Sample single-account collaboration:
:   Demonstrates a simple collaboration with only a single user account. The example worksheet creates a collaboration with two data offerings and two templates, and runs each template.

    - [Download the worksheet](/static/samples/clean-rooms/demo-collaboration-single-user.sql)

Advanced single-account collaboration:
:   Demonstrates the use of RBAC roles to limit access, and custom registries, in a single account. The example worksheet creates a collaboration with four roles: one that can create a collaboration; one that can register templates; and two that can run analyses.

    - [Download the worksheet](/static/samples/clean-rooms/demo-collaboration-three-roles.sql)

Basic two-party example:
:   Demonstrates a two-party collaboration that creates templates and data offerings. Requires two accounts.

    - [Collaboration creator (alice)](/static/samples/clean-rooms/demo-collaboration-hub-alice.sql)
    - [Analysis runner (bob)](/static/samples/clean-rooms/demo-collaboration-hub-bob.sql)

Free-form query example:
:   Demonstrates how to implement and run free-form SQL queries in a collaboration. Requires two accounts.

    - [Collaboration owner and data provider worksheet](/static/samples/clean-rooms/collab-hub-freeform-sql-provider.sql)
    - [Collaboration query runner worksheet](/static/samples/clean-rooms/collab-hub-freeform-sql-consumer.sql)

Advanced ML workloads:
:   See [Lookalike audience modeling](/user-guide/cleanrooms/collab-lookalike-modeling)
    for an example of training and scoring a model using Python UDFs or ML Jobs inside a clean room.

For more examples, including inventory forecasting, lookalike audience modeling, and last touch attribution, see the
[Use cases](/user-guide/cleanrooms/collab-inventory-forecasting) section.

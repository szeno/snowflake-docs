# About Snowflake Data Clean Rooms

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

A Snowflake Data Clean Room is a native solution to build, connect, and use data clean rooms easily in Snowflake.

It offers a secure, multi-collaborator environment where collaborators can share data that can be queried using
templates added to the collaboration. Collaborators can review and approve or reject the inclusion of new templates or data sources by other
collaborators. Query results can be exposed directly, or activated to a collaborator’s Snowflake account, at the discretion of all
collaborators.

Data clean rooms provide a secure way to gain valuable insights while protecting sensitive information. They allow you to combine
and analyze data from different parties with privacy-preserving configurations that help protect the underlying data.

Benefits of data clean rooms include:

- **Enhanced privacy** — Protects sensitive data while enabling collaboration.
- **Deeper insights** — Combines data from multiple sources for richer analysis.
- **Increased security** — Reduces the risk of unauthorized access.
- **Advanced ML** — Runs complex machine learning workloads on combined data privately.

## How Snowflake Data Clean Rooms work

With Snowflake Data Clean Rooms, all analyses are conducted within the secure environment of the clean room. Collaborators can
return aggregated results and insights, but can’t directly query the raw data in the clean room. The collaborator who is sharing
data can define what analyses are available to the other collaborators, allowing them to tightly control how their data is used.

## Clean room collaborators

Snowflake Data Clean Rooms is introducing a new data clean room architecture called Collaboration Data Clean
Rooms, which allows customers to collaborate in a fully symmetric, multi-party environment.

Your collaboration definition assigns roles to each collaborator that define their capabilities within the collaboration. Roles include:

- **Owner**: Creates the collaboration and determines who has what roles in a collaboration.
- **Data Provider**: Provides data to selected participants, and specifies Snowflake policies to apply to the data within the collaboration.
- **Analysis Runner**: Can run templates provided by collaborators, using specified data.

Collaboration Owner can assign one or more roles to each participant. All collaborators can
submit templates to the collaboration, and can specify who can use each template.

## Working with Snowflake Data Clean Rooms

Snowflake Data Clean Rooms has two different interfaces:

- **Developer APIs**: A complete set of APIs that allow a technical audience to work with clean
  rooms programmatically, including the ability to build custom applications and to customize
  analysis templates and ML models. For an overview, see
  [Data Clean Rooms Developer Guide](/user-guide/cleanrooms/developer-guide).
- **DCR UI in Snowsight**: A point-and-click interface for managing
  collaborations, designed for both technical and semi-technical users. The DCR UI also integrates
  with [Cortex Code](/user-guide/cortex-code/cortex-code), letting you use natural language
  to manage collaborations. For more information, see
  [Data Clean Rooms UI in Snowsight](/user-guide/cleanrooms/collab-ui-overview).

## Next steps

Your next steps depend on how you got here and what you want to do:

**If you’re a Snowflake administrator and are interested in installing the clean room environment in your Snowflake account:**

1. Read the [overview](/user-guide/cleanrooms/overview) for background and installation requirements.
2. [Install the clean room environment in your account.](/user-guide/cleanrooms/installing-dcr)

**If you’re a developer:**

1. If clean rooms are already installed in your Snowflake account, read the [overview](/user-guide/cleanrooms/overview) for
   background.
2. [Try out the API tutorial](/user-guide/cleanrooms/tutorials/collaboration-basic-api-tutorial).
3. Don’t forget to check out the [developer guide](/user-guide/cleanrooms/developer-guide).

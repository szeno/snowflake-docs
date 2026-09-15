# Overlap and activation

Feature — Generally Available

Currently available in [these regions](/user-guide/cleanrooms/installing-dcr#label-dcr-supported-regions).

Not available in government and VPS deployments.

## About the template

Snowflake provides an overlap and segmentation template to determine which entities exist in the data for all collaborators, and show aggregated information about those entities.

When using this template, two parties each add one or more tables to a clean room. Entities in these tables are joined or identified by the join columns that you specify.
Additionally, the overlap count can be broken down and filtered by particular segmentation attributes. This enables parties to gain insight into the overlap between their datasets, which can help determine the value of collaboration and facilitate other downstream use cases in the clean room. The analysis runner specifies which columns to join on and which columns to show. All projected columns must either be grouped or aggregated with an aggregation function. Entity-identifying columns are blocked from the query results with a threshold of five. If the activation template is added into the clean room, the results can be activated to another collaborator’s account.

This example demonstrates a two-party collaboration where the publisher is the collaboration owner and provides a data offering and two
templates: an analysis template and an activation template. The advertiser joins the collaboration, links their own data, and runs both
templates.

## Collaboration roles

| Collaborator | Roles | Actions |
| --- | --- | --- |
| Publisher | Owner, data provider | Registers a data offering (audience data), an analysis template, and an activation template. Creates the collaboration. After the advertiser activates results, the publisher views and processes the activation data. |
| Advertiser | Analysis runner, data provider (to self) | Registers a data offering (audience data). Joins the collaboration, links their data, runs the analysis template to view overlap results, and runs the activation template to send results to the publisher. |

Expand

Show lessSee more

## Key use cases

- **Overlap match rate analysis:** Measure how many records overlap between two datasets and calculate match rates to quantify audience
  alignment between collaborators.
- **Segment-level overlap:** Break down overlap counts and match rates by segmentation attributes (such as region, category, or cohort) to
  compare reach across audience segments.
- **Media valuation:** Help advertisers assess the value of a publisher’s audience by comparing overlap match rates before committing media
  spend.
- **Audience activation:** Export overlapping record IDs and selected attributes to an approved destination account so collaborators can
  target matched audiences in downstream campaigns.

## Get the worksheets and template

### Prerequisites

1. Standard templates already exist in the template registry. You can confirm by calling *REGISTRY.VIEW\_REGISTERED\_TEMPLATES* to check if *standard\_audience\_overlap\_v0* and *standard\_audience\_overlap\_activation\_v0* already exist. If not, the below must be executed:

Copy code

```
-- Register standard templates.
USE ROLE SAMOOHA_APP_ROLE;
CALL SAMOOHA_BY_SNOWFLAKE_LOCAL_DB.REGISTRY.REGISTER_STANDARD_DCR_TEMPLATES();
```

2. Ensure your role has access to the sample database

Copy code

```
-- Verify access to sample database.
SELECT *
FROM SAMOOHA_SAMPLE_DATABASE.DEMO.CUSTOMERS
LIMIT 10;
```

If you use a custom role that does not have access, use **SAMOOHA\_APP\_ROLE** or **ACCOUNTADMIN** to grant access explicitly.

3. If you use a custom role, ensure your role has been granted the **CREATE COLLABORATION** and **JOIN COLLABORATION** DCR privileges for respective accounts, along with any required account-level privileges, as described in [Manage access](/user-guide/cleanrooms/manage-access#label-dcr-collab-about-rbac-roles).

### Run the publisher and advertiser notebooks

Download and run the setup notebooks in two separate Snowflake accounts in the same organization and the same cloud hosting
environment. The notebooks show how to create and run a collaboration with audience overlap and activation templates that you can use and
modify. The advertiser runs the analysis template to view overlap and segmentation results, and optionally runs the activation template to send results to
the publisher’s account.

- [Collaborator/advertiser setup notebook](/static/samples/clean-rooms/DCR-Overlap-Activation-Two-Accounts-Template-Collaborator.ipynb)
- [Collaboration owner/publisher setup notebook](/static/samples/clean-rooms/DCR-Overlap-Activation-Two-Accounts-Template-Owner.ipynb)

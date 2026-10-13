# Tableau

Horizon Catalog supports both Tableau deployment types. Select your deployment type to get started:

## Supported deployments

- [Tableau Cloud](/user-guide/snowflake-horizon/connectors/tableau/tableau-cloud)
- [Tableau Server](/user-guide/snowflake-horizon/connectors/tableau/tableau-server)

## How the connector works

Horizon Catalog authenticates with a Tableau Connected App (direct trust) and queries Tableau’s REST
API and Metadata API (GraphQL) for workbooks, data sources, fields, and lineage. In the connector
wizard, you select your **Deployment type** (Tableau Cloud or Tableau Server) up front. Select the
setup guide for your deployment to see the prerequisites and connection-form fields specific to it.

## Choosing between Tableau Cloud and Tableau Server

|  | Tableau Cloud | Tableau Server |
| --- | --- | --- |
| **Metadata, lineage** | Supported | Supported |
| **View and workbook usage/popularity** | Supported, through Admin Insights and the VizQL Data Service | Supported, through an optional self-serve setup step and the VizQL Data Service |
| **Metadata API** | Enabled by default | Must be enabled by a server admin |
| **Authentication** | Tableau Connected App (direct trust) | Tableau Connected App (direct trust). Requires Tableau Server 2022.1 or later |

Expand

Show lessSee more

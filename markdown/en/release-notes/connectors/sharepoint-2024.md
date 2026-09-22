# Snowflake Connector for SharePoint release notes for 2024

This topic provides release notes for the Snowflake Connector for SharePoint.

For additional information, see [About the Snowflake Connector for SharePoint](/connectors/unstructured-data-connectors/sharepoint/about).

## Version 1.0.5 (December 9, 2024)

### Behavior changes

Not applicable

### New features

Not applicable

### Bug fixes

- Fixed an issue that was causing empty values to be returned in the `web_url` column in the Cortex Search service responses.

## Version 1.0.4 (December 6, 2024)

### Behavior changes

Not applicable

### New features

Not applicable

### Bug fixes

- During the data synchronization of Microsoft 365 groups, group members are now retrieved only once for each group.

## Version 1.0.3 (December 3, 2024)

### Behavior changes

- Added progress logs in the event table for the entire ingestion process.
- Unprocessed file updates and inserts are now visible through the PUBLIC.CONNECTOR\_ERRORS view.

### New features

Not applicable

### Bug fixes

- Fixed internal table definitions that were causing connector application upgrade issues.
- Files without extensions no longer break the ingestion process.
- When upgrading the connector application, change tracking on connector tables is no longer disabled.
  We’ve also migrated broken Cortex Search indexes to make them refresh the data.

## Version 1.0.2 (November 15, 2024)

### Behavior changes

- You can now use a site URL with a custom domain.

### New features

Not applicable

### Bug fixes

- The data ingestion no longer continues if an error occurs at any step of ingestion.

## Version 1.0.1 (November 8, 2024)

### Behavior changes

Not applicable

### New features

Not applicable

### Bug fixes

- Fixed how the connector handles SharePoint file deletions.

## Version 1.0.0 (November 8, 2024)

Initial release

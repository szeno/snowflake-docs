# Reinstall the Snowflake Connector for PostgreSQL

[Preview Feature](/release-notes/preview-features) — Open

Available to all accounts except government regions.

Important

Thank you for your interest in the Snowflake Connector for PostgreSQL.
Note that we’re now focused on a next-generation solution that will offer a significantly improved experience.
Hence, moving this connector to the general availability status is currently not on our product roadmap.
You may continue to use this connector as a preview feature, but please note that support for future bug
fixes and improvements are not guaranteed. The new solution is available as [Openflow Connector for PostgreSQL](/user-guide/data-integration/openflow/connectors/postgres/about) and
includes better performance, customizability, and enhanced deployment options.

To upgrade or reinstall the Snowflake Connector for PostgreSQL, do the following:

1. Shut down the connector.
2. Install and run the new version as described in [Snowflake Connector for PostgreSQL installation and configuration tasks](/connectors/postgres6/tasks).

   > Note
   >
   > The reinstalled connector will need to be set up again and will pull all the data from the source system like a fresh installation.
   > Destination database can be reused, but data in existing tables will be reloaded instead of updated.

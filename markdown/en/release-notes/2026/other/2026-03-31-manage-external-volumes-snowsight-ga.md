# Mar 31, 2026: Use Snowsight to manage external volumes (*General availability*)

With this release, you can use Snowsight to manage external volumes for Apache Iceberg™ tables. This feature
is now generally available and includes the following capabilities:

- Create an external volume, including optionally setting the external volume as the default at the account,
  database, or schema level.
- Grant USAGE privileges to an external volume.
- Add a storage location to an external volume.
- Verify an external volume to check that Snowflake can successfully authenticate to your storage provider.
- Drop an external volume.

For more information, see the following topics:

- [Configure an external volume](/user-guide/tables-iceberg-configure-external-volume)
- [Drop an external volume by using Snowsight](/user-guide/tables-iceberg-drop-external-volume)

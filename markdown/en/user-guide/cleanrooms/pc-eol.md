# End of life for legacy Provider and Consumer Data Clean Rooms

Snowflake is discontinuing the legacy “Provider and Consumer” Data Clean Rooms, which include the
[web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
and the [Provider and Consumer API](/user-guide/cleanrooms/getting-started)
(accessed through worksheets or the CLI). After the final retirement date, the
[Collaboration API](/user-guide/cleanrooms/overview) will be the only way to access Snowflake Data
Clean Rooms.

Use the [migration tool](/user-guide/cleanrooms/migration-tool) to migrate your existing clean
rooms before the following dates.

## End-of-life timeline

- **October 1, 2026:** New legacy clean rooms can no longer be created through the
  [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction).
- **February 1, 2027:** The [web application user interface](/user-guide/cleanrooms/v1/web-app-introduction)
  will no longer be accessible, and new legacy clean rooms can no longer be created through the
  [Provider and Consumer API](/user-guide/cleanrooms/getting-started).
- **June 1, 2027:** All legacy [Provider and Consumer clean rooms](/user-guide/cleanrooms/getting-started)
  will no longer be accessible. Use the [Collaboration API](/user-guide/cleanrooms/overview) to
  create and manage clean rooms.

## Managed accounts

Clean room managed accounts are deprecated. You can no longer create new clean room managed
accounts.

If you use the legacy
[clean room managed accounts](/user-guide/cleanrooms/managed-accounts) feature, the
[Snowflake Data Clean Room Managed Account Terms](https://www.snowflake.com/en/legal/other/data-clean-rooms/managed-account-terms/)
are being terminated effective **June 1, 2027**, following the same timeline as the Provider and
Consumer API. Snowflake will contact affected managed account users separately with
additional details.

To collaborate with an organization that doesn’t have its own Snowflake account, use
[third party (publisher–subscriber) accounts](/user-guide/third-party-publisher-subscriber-accounts).

## How to migrate

Migrate to the [Collaboration API](/user-guide/cleanrooms/overview) using the
[migration tool](/user-guide/cleanrooms/migration-tool) for supported clean room configurations.
Review the migration tool’s
[supported configurations and limitations](/user-guide/cleanrooms/migration-tool#label-dcr-migration-tool-supported)
before starting. The tool reads your legacy clean room configuration and generates a Collaboration
API setup without modifying your original clean room.

For further help, contact your Snowflake account team.

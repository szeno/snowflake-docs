# Dependency databases: Managing cross-database references

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

With Snowflake Declarative Native Apps, providers can share data products using a manifest-driven model. In many apps, secure views reference objects in other provider databases. In classic secure sharing, you (the provider) grant REFERENCE\_USAGE on each referenced database to the share. In Declarative Native Apps, you declare those dependency databases in the manifest using `required_databases`, thus ensuring that installs, especially in other regions, can resolve cross-database references reliably. This also applies to semantic views, user-defined functions (UDFs), or procedures used by secure views.

## When to use required\_databases

You must include a database in `required_databases` whenever a shared object in `shared_content` references objects in a database that is not listed under `shared_content.databases`. This is essential for cross-region deployments where the presence of those dependencies can’t be assumed; for example, in the following situations:

- Secure views in the shared database that JOIN/SELECT from tables or views in other provider databases
- Views referencing UDFs or procedures that live in other databases
- Notebooks shared through `application_content`, if notebook logic or views queried by the notebook depend on objects in other databases
- Semantic views whose underlying physical tables or views are in another database

Cross-database dependencies are common. If you don’t explicitly declare external databases, an app might validate or install successfully in the provider’s region but fail in other regions because the required references can’t be resolved. `required_databases` removes this ambiguity by providing a declarative list of dependency databases that must be present and resolvable wherever the app is built, released, and installed.

The package version release will be blocked if any dependency databases are not explicitly declared in `required_databases`. An error message will be generated at the time of BUILD, COMMIT, or RELEASE, specifically stating that the referenced database is missing from the manifest’s `required_databases` section.

## When not to use required\_databases

Note that including a database in `required_databases` doesn’t apply to:

- Objects fully contained in the databases listed under `shared_content.databases`
- Classic sharing, which uses privilege grants to shares (including REFERENCE\_USAGE) instead of manifest declarations

## Replication limitations

Declaring databases in `required_databases` does not replicate those databases or their contents. It registers the dependency so the framework and listing workflows can prepare and resolve references appropriately.

To support cross-region installs and failover when your manifest uses `required_databases`:

- Identify dependency databases: For each entry under `shared_content.required_databases`, confirm which provider-owned database it maps to in your source account.
- Configure replication for each dependency: Set up database (or account) replication for every dependency database to the regions and accounts where you plan to build, release, and install the app. Use standard Snowflake replication features for this step.
- Keep names consistent: Ensure the database names in target regions exactly match the names you declare in `required_databases`. Name mismatches will cause BUILD/COMMIT/RELEASE to fail with an error indicating that the referenced database is missing from `required_databases`.
- Validate after replication completes: After the initial replication and any subsequent refreshes complete, run your BUILD, COMMIT, or RELEASE commands in the target region. If you see errors about unresolved or missing dependency databases, verify:
  - The database is replicated and available in the target account and region.
  - The database name matches the value in `required_databases`.
  - Any chained dependencies those databases rely on are also replicated and correctly named.

For end-to-end steps and options when configuring database and account replication, see [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro).

# Declarative App Consumer-Side Execution Model

Feature — Generally Available

Support for Snowflake Declarative Native Apps is available to all accounts.

When you install a Declarative Native App as a consumer, the Native App Framework isolates the app’s data access and code execution in a controlled environment, preventing the app from accessing data or otherwise affecting resources in the consumer account.

The Native App Framework enforces sandbox-style security boundaries for Declarative Native Apps, so that the app can only
access data included in the app package. This ensures that the app cannot access any other data, code resources, or system resources in the consumer account, providing a secure environment for running the app, and protecting the consumer’s assets.

The security boundaries for Declarative Native Apps are more restrictive than those for Native App Framework apps, which can access additional resources in the consumer account when given the appropriate permissions.

## Embedded code objects in Declarative Native Apps

Declarative Native Apps support Snowflake Notebooks as embedded code objects. Providers
share notebooks in a [workspace](/developer-guide/declarative-sharing/workspaces). Sharing
individual notebooks with `application_content.notebooks` is deprecated.

Currently, Declarative Native Apps can’t use other types of code resources for logic, such as Streamlits, stored procedures, or UDFs. The embedded code objects in a Declarative Native App can only do the following:

- Access data or code objects from inside the app package.
- Run queries, visualizations, and functions on the tables and views exposed by the app package. The app has SELECT access to these tables, views, and functions.

The embedded logic cannot do the following:

- Access any other data products in the consumer account.
- Access any other logic in the consumer account.
- Access metadata about other data products installed in the consumer account.
- Access any system resources in the consumer account, such as system tables or views. For example, running `SHOW DATABASES` or `SHOW TABLES` returns only the databases and tables that are part of the app package. Other databases and tables in the consumer account are not visible to the app.
- Change system parameters or settings in the consumer account. For example, changing the warehouse size or modifying user roles.
- Create resources or external integrations in the consumer account, such as creating new warehouses, databases, tables, or views that are not part of the app package.

Note

The app uses the current user account’s default warehouse. For information about creating a warehouse, see [CREATE WAREHOUSE](/sql-reference/sql/create-warehouse). For information about setting a default warehouse for a user account, see [ALTER USER](/sql-reference/sql/alter-user).

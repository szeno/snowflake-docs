# Feb 18, 2026: Support for changing refresh user and secondary roles

You can now configure dynamic tables to refresh with the privileges of a specific user, in addition to privileges of the owner role.
Dynamic tables that specify EXECUTE AS USER run on behalf of the named user, instead of the system user.

For example, you can grant a user a primary role that provides access to a table and a secondary role that provides access to a virtual
warehouse. The user can then create a dynamic table that operates with the combined privileges of both roles, simplifying permissions
management and enhancing the flexibility of your data operations.

Key use cases include:

- Unified privileges: Enables access to resources spread across multiple roles within a single refresh session.
- Enhanced accountability: Attributes all refresh activity to a specific individual for compliance and auditing.
- Governance control: Supports granular security through the IMPERSONATE privilege and ensures data policies, like masking, are evaluated against the correct user context.

For more information, see [Refresh with specific user privileges (EXECUTE AS USER)](/user-guide/dynamic-tables/privileges#label-dts-execute-as-user) and [CREATE DYNAMIC TABLE](/sql-reference/sql/create-dynamic-table).

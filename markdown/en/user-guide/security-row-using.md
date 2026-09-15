# Use row access policies

[Enterprise Edition Feature](/user-guide/intro-editions)

This feature requires Enterprise Edition (or higher). To inquire about upgrading,
please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

This topic provides an introduction to implementing row access policies.

## Implement row access policies

The following sections provide examples on how to implement row access policies:

- Use a typical row access policy with a mapping table lookup.
- Replace existing row access policy subqueries with memoizable functions to increase query performance.
- Reference a mapping table protected by a row access policy in a different row access policy.

## Example: Mapping table lookup

The following steps are a representative guide to configure row access policy privileges and add row access policies to tables and views.

These steps make the following assumptions:

- The management approach is centralized.

  If the row access policy use case includes a hybrid, or decentralized management approach, see [Manage row access policies](/user-guide/security-row-intro#label-security-row-mgmt-approach)
  for a representative distribution of roles and privileges.
- A mapping table is necessary, similar to the [Representative use case: Use a mapping table to filter the query result](/user-guide/security-row-intro#label-security-row-representative-use-case).

  The following steps use the [CURRENT\_ROLE](/sql-reference/functions/current_role) context function to determine whether users see rows in a
  query result, while the representative use case focuses on the user’s first name (i.e. [CURRENT\_USER](/sql-reference/functions/current_user)).

  If role activation and role hierarchy are important, Snowflake recommends that the policy conditions use the
  [IS\_ROLE\_IN\_SESSION](/sql-reference/functions/is_role_in_session) function for account roles and the
  [IS\_DATABASE\_ROLE\_IN\_SESSION](/sql-reference/functions/is_database_role_in_session) function for database roles. For details, see
  [Active role hierarchy & mapping tables](/user-guide/security-row-intro#label-security-row-intro-mapping-table).

  The overall process to implement a row access policy with mapping tables remains the same even though the context functions are different.
- The SECURITYADMIN system role grants privileges to custom roles to manage and implement row access policies.

  If you do not want to use higher privileged roles (i.e. SECURITYADMIN or ACCOUNTADMIN) in a production environment in favor of less
  privileged custom roles (e.g. `database_admin`, `finance_admin`), verify that the lower-privileged roles have the necessary
  privileges to manage and implement row access policies.

  For more information, see [Row access policy privileges](/user-guide/security-row-intro#label-security-row-privileges) and [Summary of DDL commands, operations, and privileges](/user-guide/security-row-intro#label-security-row-privilege-command-summary).
- There are separate steps to create a table to be protected by a row access policy (step 1) and adding the row access policy to the
  table (step 5). It is possible to add row access policy to the table when the table is created, assuming that a row access policy already exists. For more information on the syntax, see [CREATE TABLE](/sql-reference/sql/create-table).

For example:

1. Create a table for the sales data:

   Copy code

   ```
   CREATE TABLE sales (
     customer   varchar,
     product    varchar,
     spend      decimal(20, 2),
     sale_date  date,
     region     varchar
   );
   ```
2. In the `security` schema, create a mapping table as shown in the
   [representative example](/user-guide/security-row-intro#label-security-row-representative-use-case). This table defines which rows sales managers can see in the
   `sales` table:

   Copy code

   ```
   CREATE TABLE security.salesmanagerregions (
     sales_manager varchar,
     region        varchar
   );
   ```
3. Next, a security administrator creates the `mapping_role` custom role and grants the SELECT privilege to the custom role. This grant
   allows users with the custom role to query the mapping table:

   Copy code

   ```
   USE ROLE SECURITYADMIN;

   CREATE ROLE mapping_role;

   GRANT SELECT ON TABLE security.salesmanagerregions TO ROLE mapping_role;
   ```
4. Using the schema owner role, create a row access policy with the following two conditions:

   - Users with the `sales_executive_role` custom role can view all rows.
   - Users with the `sales_manager` custom role can view rows based on the `salesmanagerregions` mapping table.

   Note that the schema owner role is automatically granted the CREATE ROW ACCESS POLICY privilege. If other roles should be able to create
   row access policies, the schema owner role can grant the CREATE ROW ACCESS policy privilege to other roles.

   Copy code

   ```
   USE ROLE schema_owner_role;

   CREATE OR REPLACE ROW ACCESS POLICY security.sales_policy
   AS (sales_region varchar) RETURNS BOOLEAN ->
     'sales_executive_role' = CURRENT_ROLE()
    OR EXISTS (
      SELECT 1 FROM salesmanagerregions
        WHERE sales_manager = CURRENT_ROLE()
        AND region = sales_region
    )
   ;
   ```

   Where:

   **`security.sales_policy`**

   The name of the row access policy in the `security` schema.

   **`AS (sales_region varchar)`**

   The signature for the row access policy.

   A signature specifies the mapping table attribute and data type. The returned value determines whether the user has access to a given
   row on the table or view to which the row access policy is added.

   **`'sales_executive_role' = CURRENT_ROLE()`**

   The beginning of the `body` in the row access policy.

   The first condition of the row access policy expression that allows users with the `sales_executive_role` custom role to view data.

   **`OR EXISTS (select 1 from salesmanagerregions WHERE sales_manager = CURRENT_ROLE() AND region = sales_region)`**

   The second condition of the row access policy expression which uses a subquery.

   The subquery requires the CURRENT\_ROLE to be the `sales_manager` custom role with the executed query on the data to specify a region
   listed in the `{salesmanagerregions}` mapping table.

   Tip

   To increase query performance on the policy-protected table, replace the mapping table lookup subquery in the `EXISTS` clause with a [memoizable function](/developer-guide/udf/sql/udf-sql-scalar-functions#label-udf-sql-scalar-memoizable).

   For details, see the [memoizable function example](#label-security-row-using-example-memoizable-function) (in this topic).
5. Using the SECURITYADMIN system role, execute the following two statements:

   Copy code

   ```
   GRANT OWNERSHIP ON ROW ACCESS POLICY security.sales_policy TO mapping_role;

   GRANT APPLY ON ROW ACCESS POLICY security.sales_policy TO ROLE sales_analyst_role;
   ```

   These two [GRANT <privileges> … TO ROLE](/sql-reference/sql/grant-privilege) statements have the following effects:

   - Ownership of the policy does not rest with the SECURITYADMIN system role. At query runtime, Snowflake uses the privileges granted to
     the custom role because policies are executed with [owner’s rights](/user-guide/security-row-intro#label-security-row-work), not the more privileged SECURITYADMIN system role. This approach supports the Principle of Least Privilege.
   - The `sales_analyst_role` custom role can add or drop the row access policy from a table as needed.
6. Add (bind) the row access policy to the region column in the `sales` data table:

   Copy code

   ```
   USE ROLE SECURITYADMIN;

   ALTER TABLE sales ADD ROW ACCESS POLICY security.sales_policy ON (region);
   ```
7. Grant the SELECT privilege on the protected `sales` data to the `sales_manager_role` custom role:

   Copy code

   ```
   GRANT SELECT ON TABLE sales TO ROLE sales_manager_role;
   ```
8. After the sales data populates the `sales` data, test the row access policy:

   Copy code

   ```
   USE ROLE sales_manager_role;
   SELECT product, SUM(spend)
   FROM sales
   WHERE YEAR(sale_date) = 2020
   GROUP BY product;
   ```

## Example: Replace Policy subqueries with a memoizable function

The steps in this example create a [memoizable function](/developer-guide/udf/sql/udf-sql-scalar-functions#label-udf-sql-scalar-memoizable) for each mapping table lookup in the row
access policy conditions. The subquery in each `EXISTS` clause specifies the mapping table lookup, where the tables are named
`regions`, `customers`, and `products`, respectively:

> Copy code
>
> ```
> CREATE OR REPLACE ROW ACCESS POLICY rap_NO_memoizable_function
>   AS (region_id number, customer_id number, product_id number)
>   RETURNS BOOLEAN ->
>     EXISTS(SELECT 1 FROM regions WHERE id = region_id) OR
>     EXISTS(SELECT 1 FROM customers WHERE id = customer_id) OR
>     EXISTS(SELECT 1 FROM products WHERE id = product_id)
>   ;
> ```

For the following steps, assume that the `rap_admin` custom role can create row access policies
(i.e. has the CREATE ROW ACCESS POLICY on SCHEMA privilege).

Complete the following steps to replace each of the row access policy mapping table lookups with a memoizable function:

1. Create a custom role named `functions_admin` to manage the memoizable function:

   Copy code

   ```
   USE ROLE USERADMIN;

   CREATE ROLE functions_admin;
   ```
2. Grant the following privileges to the `functions_admin` role to allow creating the memoizable function in an existing schema named
   `governance.functions`:

   Copy code

   ```
   USE ROLE SECURITYADMIN;

   GRANT USAGE ON DATABASE governance TO ROLE functions_admin;

   GRANT USAGE ON SCHEMA governance.functions TO ROLE functions_admin;

   GRANT CREATE FUNCTION ON SCHEMA governance.functions TO ROLE functions_admin;
   ```
3. Create a memoizable function for each of the `EXISTS` subquery clauses in the row access policy. Each memoizable function definition
   takes the same form. For brevity, only one function example is shown:

   Copy code

   ```
   USE ROLE functions_admin;

   USE SCHEMA governance.functions;

   CREATE OR REPLACE function allowed_regions()
     RETURNS array
     memoizable
     AS 'SELECT ARRAY_AGG(id) FROM regions';
   ```
4. Use a [CREATE ROW ACCESS POLICY](/sql-reference/sql/create-row-access-policy) statement to define a new row access policy that replaces the subqueries with
   memoizable functions:

   The new row access policy allows for testing queries on a protected table, when the policy uses or does not use the memoizable
   functions, to quantify the performance impact of using memoizable functions in the policy conditions:

   Copy code

   ```
   USE ROLE rap_admin;

   CREATE OR REPLACE ROW ACCESS POLICY rap_with_memoizable_function
     AS (region_id number, customer_id number, product_id number)
     RETURNS BOOLEAN ->
    ARRAY_CONTAINS(region_id, allowed_regions()) OR
    ARRAY_CONTAINS(customer_id, allowed_customers()) OR
    ARRAY_CONTAINS(product_id, allowed_products())
     ;
   ```

## Example: Protect the mapping table with a row access policy

This example shows how to reference a mapping table that is protected by a row access policy in a different row access policy. The row
access policy that protects the mapping table calls the [IS\_ROLE\_IN\_SESSION](/sql-reference/functions/is_role_in_session) context function to account for
role hierarchy. A different row access policy protects the table that the user queries. This row access policy uses a subquery to perform a
mapping table lookup. For example:

1. Create a mapping table to define allowed roles based on geographic sales regions, and insert data into the table:

   Copy code

   ```
   CREATE OR REPLACE TABLE sales.tables.regional_managers (
     allowed_regions varchar,
     allowed_roles varchar
   );
   ```

   Copy code

   ```
   INSERT INTO sales.tables.regional_managers
   (allowed_regions, allowed_roles)
   VALUES
   ('na', 'NA_MANAGER'),
   ('eu', 'EU_MANAGER'),
   ('apac', 'APAC_MANAGER');
   ```
2. Create a row access policy to specify the ALLOWED\_ROLES column in the mapping table:

   Copy code

   ```
   CREATE OR REPLACE ROW ACCESS POLICY governance.policies.rap_map_exempt
   AS (allowed_roles varchar) RETURNS BOOLEAN ->
   IS_ROLE_IN_SESSION(allowed_roles);
   ```
3. Add the row access policy on the mapping table using an [ALTER TABLE](/sql-reference/sql/alter-table) statement:

   Copy code

   ```
   ALTER TABLE sales.tables.regional_managers
     ADD ROW ACCESS POLICY governance.policies.rap_map_exempt
     ON (allowed_roles);
   ```
4. Create a new row access policy that specifies the mapping table lookup on the protected mapping table:

   Copy code

   ```
    CREATE OR REPLACE ROW ACCESS POLICY governance.policies.rap_map_lookup
    AS (allowed_regions varchar) RETURNS BOOLEAN ->
    EXISTS (
   SELECT * FROM sales.tables.regional_managers
   WHERE
     REGION = allowed_regions
   );
   ```
5. Add the row access policy named `governance.policies.rap_map_lookup` on the table named `sales.tables.data` using an ALTER
   TABLE statement:

   Copy code

   ```
   ALTER TABLE sales.tables.data
     ADD ROW ACCESS POLICY governance.policies.rap_map_lookup
     ON (allowed_regions);
   ```
6. Grant privileges to the roles in the mapping table to allow users with these roles to query the protected data. For example, these
   grants are for the `na_manager` custom role:

   Copy code

   ```
   USE ROLE SECURITYADMIN;
   GRANT USAGE ON DATABASE sales TO ROLE na_manager;
   GRANT USAGE ON SCHEMA sales.tables TO ROLE na_manager;
   GRANT SELECT ON TABLE sales.tables.regional_managers TO ROLE na_manager;
   GRANT SELECT ON TABLE sales.tables.data TO ROLE na_manager;
   ```

   As necessary, repeat the commands in this step for each role in the mapping table.

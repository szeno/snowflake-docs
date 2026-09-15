# Secure catalogs

Feature — Generally Available

Not available in government regions.

The catalog admin manages a catalog.

When you secure a catalog, you define the actions that a service principal can perform on the following securable objects for the catalog:

- The entire catalog
- A namespace in the catalog and its objects (tables, views, etc.) and optionally any child namespaces nested under it and their objects
- A table in the catalog
- A view in the catalog

**Note**

> If you haven’t already created catalog roles, which you grant with access control privileges when you secure a catalog, create them now. For details, see [Create a catalog](create-catalog). If you haven’t already created the principal roles you need to logically group Open Catalog service principals together, create them now. For details, see [Create a principal role](create-principal-role).

## Secure a catalog

The workflow to secure a catalog is as follows:

Step 1: Grant catalog privileges on a catalog role.

Step 2: Grant the catalog role to a principal role.

If needed, you can later [update the privileges granted on a secured catalog](#update-the-privileges-granted-to-a-catalog-role-at-the-catalog-level).

### Step 1: Grant catalog privileges on a catalog role

To grant privileges on a catalog, you first grant privileges on a catalog role. These privileges specify a set of permissions for actions that a service principal can take on the catalog. For more information about catalog roles, see [Catalog role](access-control#catalog-role).

1. Sign in to Open Catalog.
2. In the menu on the left, select **Catalogs**.
3. In the list of catalogs, select the catalog for which you want to grant privileges.
4. Select the **Catalog Details** tab.
5. Select **+ Privilege**.
6. In the **Grant new privileges on** dialog, complete the fields:
   1. For **Catalog role**, select the catalog role you want to grant privileges on.
   2. For **Privileges**, select each privilege to grant on the catalog.

      For a description of the available privileges, see [Access control privileges for a catalog](access-control#catalog-privileges).
   3. Select **Grant privileges**.

      The privileges are granted to the catalog role.

### Step 2: Grant the catalog role to a principal role

To bestow a catalog role’s privileges to the service principals that a principal role is granted to, grant the catalog role to that principal role. For more information about principal roles and service principals, see [Principal role](access-control#principal-role) and [Service principal](./overview#service-principal).

1. Sign in to Open Catalog.
2. In the menu on the left, select **Catalogs**.
3. In the list of catalogs, select the catalog for which you want to grant a catalog role to a principal role.
4. Select the **Roles** tab.
5. Select **Grant to Principal Role**.
6. In the **Grant Catalog Role** dialog, complete the fields:
   1. For **Catalog role to grant**, select the catalog role you granted privileges on.
   2. For **Principal role to receive grant**, select the principal role that is granted to the service principal that you want to grant the privileges to.
   3. Select **Grant**.

      The catalog role is granted to the principal role, and the catalog role’s privileges are now bestowed to the service principals that the principal role is granted to.

### Update the privileges granted to a catalog role at the catalog level

If needed, you can update the catalog privileges granted to a catalog role, which updates the privileges bestowed to the service principal.

**Note**

> If you update the privileges bestowed to a service principal, the updates won’t take effect for up to one hour. This means that if you revoke or grant some privileges for a catalog, namespace, or table, the updated privileges won’t take effect on any service principal with access to that catalog for up to one hour.

1. Sign in to Snowflake Open Catalog.
2. From the menu on the left, select **Catalogs**.
3. From the list of catalogs, select the catalog whose privileges you want to update.
4. From the **Catalog Details** tab, in the Privileges section, select the **Edit** icon for the catalog role whose privileges you want to update.
5. Optional: To add a privilege to the catalog role, for **Privileges**, select the privilege you want to add.
6. Optional: To remove a privilege from the catalog role, select the **x** icon next to the privilege you want to remove.
7. Select **Update privileges**.

## Secure a namespace

The workflow to secure a namespace is as follows:

Step 1: Navigate to the namespace and grant privileges on a catalog role. If you need to grant the same privileges to another namespace, repeat this step for each namespace.

Step 2: Grant the catalog role to a principal role.

If needed, you can later [update the privileges granted on a secured namespace](#update-the-privileges-granted-to-a-catalog-role-at-the-namespace-level).

### Step 1: Grant namespace privileges on a catalog role

To grant privileges on a namespace, you first navigate to the namespace and grant privileges on a catalog role. These privileges specify a set of permissions for actions that a service principal can take on the namespace. For more information about catalog roles, see [Catalog role](access-control#catalog-role).

1. Sign in to Open Catalog.
2. From the menu on the left, select **Catalogs**.
3. From the list of catalogs, select the catalog containing the namespace you want to grant privileges on.
4. From the catalog object explorer on the left, select the namespace you want to grant privileges on.
5. On the **Namespace Details** tab, select **+ Privilege**.
6. In the **Grant new privileges on** dialog, complete the fields:
   1. For **Catalog role**, select the catalog role you want to grant privileges on.
   2. For **Privileges**, select each privilege to grant on the namespace.

      For a description of the available privileges, see [Access control privileges for a namespace](./access-control#namespace-privileges).
   3. Select **Grant privileges**.

      The privileges are granted to the catalog role.

**Note**

> If you need to secure additional namespaces with the same privileges, repeat the previous steps for the other namespaces. When selecting the catalog role, make sure you select the same catalog role for each namespace.

### Step 2: Grant the catalog role to a principal role

To bestow a catalog role’s privileges to the service principals that a principal role is granted to, grant the catalog role to that principal role. For more information about principal roles and service principals, see [Principal role](access-control#principal-role) and [Service principal](overview#service-principal).

1. Sign in to Open Catalog.
2. From the menu on the left, select **Catalogs**.
3. From the list of catalogs, select the catalog for which you want to grant a catalog role to a principal role.
4. On the **Roles** tab, select **Grant to Principal Role**.
5. In the **Grant Catalog Role** dialog, complete the fields:
   1. For **Catalog role to grant**, select the catalog role you granted privileges on.
   2. For **Principal role to receive grant**, select the principal role that is granted to the service principal that you want to grant the privileges.
   3. Select **Grant**.

      The catalog role is granted to the principal role, and the catalog role’s privileges are now bestowed to the service principals that the principal role is granted to.

### Update the privileges granted to a catalog role at the namespace level

If needed, you can update the catalog privileges granted to a catalog role, which updates the privileges bestowed to the service principal.

**Note**

> If you update the privileges bestowed to a service principal, the updates won’t take effect for up to one hour. This means that if you revoke or grant some privileges for a catalog, namespace, or table, the updated privileges won’t take effect on any service principal with access to that catalog for up to one hour.

1. Sign in to Open Catalog.
2. From the menu on the left, select **Catalogs**.
3. From the list of catalogs, select the catalog containing the namespaces whose privileges you want to update.
4. From the catalog object explorer on the left, select the namespace whose privileges you want to update.
5. On the **Namespace Details** tab, in the **Privileges** section, select the **Edit** icon for the catalog role whose privileges you want to update.
6. Optional: To add a privilege to the catalog role, for **Privileges**, select the privilege you want to add.
7. Optional: To remove a privilege from the catalog role, select the **x** icon next to the privilege you want to remove.
8. Select **Update privileges**.
9. Optional: Repeat these steps for any additional namespaces whose privileges you need to update.

## Secure a table

The workflow to secure a table is as follows:

Step 1: Navigate to the table and grant privileges on a catalog role. If you need to grant the same privileges to another table, repeat this step for each table.

Step 2: Grant the catalog role to a principal role.

If needed, you can later [update the privileges granted on a secured table](#update-the-privileges-granted-to-a-catalog-role-at-the-table-level).

### Step 1: Grant table privileges on a catalog role

To grant privileges on a table, you first grant privileges on a catalog role. These privileges specify a set of permissions for actions that a service principal can take on the table. For more information about catalog roles, see [Catalog role](access-control#catalog-role).

1. Sign in to Open Catalog.
2. From the menu on the left, select **Catalogs**.
3. From the list of catalogs, select the catalog containing the table you want to grant privileges on.
4. From the catalog object explorer on the left, expand the applicable namespaces, and then select the table you want to grant privileges on.
5. On the **Table Details** tab, select **+ Privilege**.
6. In the **Grant new privileges on** dialog, complete the fields:
   1. For **Catalog role**, select the catalog role you want to grant privileges on.
   2. For **Privileges**, select each privilege to grant on the namespace.

      For a description of the available privileges, see [access control privileges for a table](access-control#table-privileges).
   3. Select **Grant privileges**.

      The privileges are granted to the catalog role.

**Note**

> If you need to secure additional tables with the same privileges, repeat the previous steps for the other tables. When selecting the catalog role, make sure you select the same catalog role for each table.

### Step 2: Grant the catalog role to a principal role

To bestow a catalog role’s privileges to the service principals that a principal role is granted to, grant the catalog role to that principal role. For more information about principal roles and service principals, see [Principal role](access-control#principal-role) and [Service principal](overview#service-principal).

1. Sign in to Open Catalog.
2. From the menu on the left, select **Catalogs**.
3. From the list of catalogs, select the catalog for which you want to grant a catalog role to a principal role.
4. On the **Roles** tab, select **Grant to Principal Role**.
5. In the **Grant Catalog Role** dialog, complete the fields:
   1. For **Catalog role to grant**, select the catalog role you granted privileges on.
   2. For **Principal role to receive grant**, select the principal role that is granted to the service principal that you want to grant the privileges to.
   3. Select **Grant**.

      The catalog role is granted to the principal role, and the catalog role’s privileges are now bestowed to the service principals that the principal role is granted to.

### Update the privileges granted to a catalog role at the table level

If needed, you can update the catalog privileges granted to a catalog role, which updates the privileges bestowed to the service principal.

**Note**

> If you update the privileges bestowed to a service principal, the updates won’t take effect for up to one hour. This means that if you revoke or grant some privileges for a catalog, namespace, or table, the updated privileges won’t take effect on any service principal with access to that catalog for up to one hour.

1. Sign in to Open Catalog.
2. From the menu on the left, select **Catalogs**.
3. From the list of catalogs, select the catalog containing the table(s) whose privileges you want to update.
4. From the catalog object explorer on the left, expand the applicable namespace(s) and then select the table whose privileges you want to update.
5. From the **Table Details** tab, in the Privileges section, select the **Edit** icon for the catalog role whose privileges you want to update.
6. Optional: To add a privilege to the catalog role, for **Privileges**, select the privilege you want to add.
7. Optional: To remove a privilege from the catalog role, select the **x** icon next to the privilege you want to remove.
8. Select **Update privileges**.
9. Optional: Repeat these steps for any additional namespaces whose privileges you need to update.

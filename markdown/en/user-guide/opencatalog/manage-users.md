Feature — Generally Available

Not available in government regions.

# Manage users in Snowflake Open Catalog

A service admin can perform the following actions to manage users through the Snowflake Open Catalog web interface:

- Create and drop users.
- Grant and revoke user roles. For more information about user roles, see [User roles](./access-control#user-roles).

If you created a Snowflake Open Catalog account, you are a service admin in the account.

## Create a user

1. Sign in to Snowflake Open Catalog.
2. From the menu on the left, select **Users**.
3. Select **+ User**.
4. For **User Name**, enter a unique identifier for the user.

   The user signs in to Snowflake Open Catalog with this identifier.
5. Optional: For **Email**, specify an email address for the user.
6. Optional: To grant the service admin role to the user, move the **Grant service admin** toggle to **On**.
7. For **Password** and **Verify Password**, enter the password for the user.
8. Select **Create**.

## Grant to a user the catalog admin role to a catalog

You can only grant the catalog admin role to a catalog that you created.

1. Sign in to Open Catalog.
2. From the menu on the left, select **Users**.
3. Select the relevant catalog admin user.
4. Select **+ Grant catalog admin**.
5. Grant user access to a catalog:

   1. From the drop down menu, select the catalog you want to grant the catalog admin access to.
   2. Select **Add**.

   **Note**

   > You can only grant catalog admin access to catalogs that you’ve created, not to catalogs
   > created by other service admins.
6. Optional: Repeat the previous step to grant catalog admin access to additional catalogs.
7. Select **Close**.

## Revoke your own catalog admin role to a catalog

A service admin user can revoke their catalog admin privileges to a catalog that they created.

### Step 1: Revoke your service admin role

1. Sign in to Open Catalog.
2. From the menu on the left, select **Users**.
3. From the list of users, select the relevant service admin user.
4. Move the **Service admin** toggle to **Off**.
5. Select **Revoke**.
6. Select **Close**.

### Step 2: Revoke your catalog admin privileges from the catalog

1. Sign in to Open Catalog.
2. From the menu on the left, select **Users**.
3. From the list of users, select your user account.
4. In **Granted catalog admin on**, select **x** next to the relevant catalog.
5. Select **Revoke**.
6. Select **Close**.

## Revoke a user’s catalog admin role for a catalog

When you revoke a user’s catalog admin privileges to a catalog, the user can no longer manage or access the catalog.

1. Sign in to Open Catalog.
2. From the menu on the left, select **Users**.
3. Select the user whose catalog privileges you want to revoke.
4. From the **Granted catalog admin on** field, select **x** next to the relevant catalog.
5. Select **Revoke**.
6. Select **Close**.

## Grant to a user the service admin role

1. Sign in to Open Catalog.
2. From the menu on the left, select **Users**.
3. Select the relevant user.
4. Move the **Grant service admin** toggle to **On**.
5. Select **Grant**.
6. Select **Close**.

## Revoke a user’s service admin role

**Note**

> If needed, you can revoke the service admin role granted to your own user account.

1. Sign in to Open Catalog.
2. From the menu on the left, select **Users**.
3. From the list of users, select the relevant user.
4. Move the **Service admin** toggle to **Off**.
5. Select **Revoke**.
6. Select **Close**.

## Drop a user

Dropping a user removes the user credentials from Open Catalog.

Important

Before you drop a user, determine whether that user created any catalogs that only they have catalog admin privileges to. If so, that user
must first grant those privileges to another user. Otherwise, no other user can access the catalog. Snowflake customer support *cannot*
provide access to the catalog.

1. Sign in to Open Catalog.
2. From the menu on the left, select **Users**.
3. From the list of users, select the user you want to drop.
4. Select **Drop User**.
5. Select **Drop**.

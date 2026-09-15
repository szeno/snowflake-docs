# Configure and remove a service connection

Feature — Generally Available

Not available in government regions.

As a Snowflake Open Catalog administrator, you configure a new service connection in Snowflake Open Catalog. You can then register it, which
connects the query engine that uses the connection to a catalog in Open Catalog. You can use the same service connection
for one or multiple query engines. For more information about service connections, see [Service connection](overview#service-connection).

When you configure a new service connection, you specify the following items:

- A [principal role](./access-control#principal-role) to grant to the service principal. You can use a principal role to logically
  group Open Catalog service principals together. For more information, including examples of principal roles, see [Principal role](access-control#principal-role).
- The query engine that users will use with the connection, such as Apache Spark.

When you configure a service connection, the service credentials for its service principal are created. You specify these service credentials
when you register the service connection.

## Configure a service connection

1. Sign in to Open Catalog.
2. In the menu on the left, select **Connections**.
3. Select **+ Connection**.
4. In the Configure Service Connection dialog, complete the fields:

   1. For **Query Engine**, select the query engine for the service connection.
   2. For **Name**, enter a service principal name.

      You can enter a user-friendly name so the connection is easier to identify and
      use in tools. For more information, including examples, see [Service principal](overview#service-principal).
   3. To grant a principal role to the service principal, do one of the following:

      - To grant an existing principal role, select a role in the **Principal Role** drop-down.

        You can select an existing principal role to grant the same privileges to multiple service principals, such as a principal role named DATA\_ENGINEERS.
      - To grant a new principal role, select **Create new principal role**. For
        **Principal Role**, enter a name for the new role.
5. Select **Create**.

   The Client ID and Client Secret service credentials for the service principal are created.
6. In the **Configure Service Connection** dialog, save the service credentials:

   1. To copy the Client ID, select **Copy client id** inside the **Client ID** field, and paste it in a file.
   2. To copy the Client Secret, select **Copy secret** inside the **Client Secret** field, and paste it in a file.
   3. To copy both the Client ID and Client Secret and in the format that they need to be specified when you register the service
      connection, select **Copy** inside the **As &lt;CLIENT ID&gt;:&lt;SECRET&gt;** field.

      **Important**

      You must save the service credentials before you close the Configure Service Connection window, because you can’t retrieve them later.
7. Select **Close**.

## Remove a service connection

If you no longer need to use a service connection, remove it.

To remove a service connection, do the following:

1. Sign in to Open Catalog.
2. In the menu on the left, select **Connections**.
3. In the list of connections, locate the service connection you want to remove.
4. Under the **MORE** column, select **…** for the connection you want to remove.
5. Select **Delete**.

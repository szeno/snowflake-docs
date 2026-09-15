# Copy `arctic-extract` models between databases, schemas, and accounts

This topic explains how to copy fine-tuned `arctic-extract` models between databases or schemas in the same account or between different accounts in the same organization.
For example, you might want to copy a model from a development account to a production account.

## Copy models between databases and/or schemas within an account

1. Create the model from the source model using the role that created the source model:

   Tip

   To list the versions in a model, use [SHOW VERSIONS IN MODEL](/sql-reference/sql/show-versions-in-model).

   Copy code

   ```
   CREATE MODEL prod_db.prod_schema.invoices_model
     WITH VERSION V1
     FROM MODEL dev_db.dev_schema.invoices_source_model
    VERSION V1;
   ```
2. Optional: Add another version of the model:

   Copy code

   ```
   ALTER MODEL prod_db.prod_schema.invoices_model
     ADD VERSION V2
     FROM MODEL dev_db.dev_schema.invoices_source_model
    VERSION V2;
   ```
3. To enable the `prod_role` role to use the copied model, grant the OWNERSHIP privilege on the model to that role:

   Copy code

   ```
   GRANT OWNERSHIP ON MODEL prod_db.prod_schema.invoices_model
     TO ROLE prod_role;
   ```

## Copy models between accounts

You can replicate a model from a source account to one or more target accounts in the same organization.
For more information about replication, see [Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro).

To replicate the model from a source account to a target account, you need to create a replication group in the source account to enable replication of the database
in which the model was created to a target account, and set up the production user role.

Note

You must be a user with the ACCOUNTADMIN role to create a replication group and to set up the production user role.

### Replicate the database in which the model was created

1. Create a primary replication group in the source account:

   Copy code

   ```
   CREATE REPLICATION GROUP models_replication_group
   OBJECT_TYPES = DATABASES
   ALLOWED_DATABASES = dev_db
   ALLOWED_ACCOUNTS = org.production_account;
   ```
2. Create a secondary replication group in a target account as a replica of the primary replication group in the source account:

   Copy code

   ```
   CREATE REPLICATION GROUP models_secondary_replication_group
   AS REPLICA OF org.dev_account.models_replication_group;
   ```
3. Refresh the database in the target account from the source account:

   Copy code

   ```
   ALTER REPLICATION GROUP models_secondary_replication_group REFRESH;
   ```
4. Optional: Specify the schedule for refreshing the secondary replication group so that the account is synchronized automatically every 10 minutes:

   Copy code

   ```
   ALTER REPLICATION GROUP models_secondary_replication_group
     SET REPLICATION_SCHEDULE = '10 MINUTE';
   ```

### Set up the production user role

To ensure that the user working on the target production account (for example, a user with the `prod_role` role) can use the replicated model, follow these steps:

1. Grant the USAGE privilege on the source database and schema, and ownership on all models in that schema, to the `prod_role` role:

   Copy code

   ```
   GRANT USAGE ON DATABASE dev_db TO ROLE prod_role;
   GRANT USAGE ON SCHEMA dev_db.dev_schema TO ROLE prod_role;
   GRANT OWNERSHIP ON ALL MODELS IN SCHEMA dev_db.dev_schema TO ROLE prod_role;
   ```
2. Optional: Grant ownership on all the future models that will be replicated:

   Copy code

   ```
   GRANT OWNERSHIP ON ALL FUTURE MODELS IN SCHEMA dev_db.dev_schema TO ROLE prod_role;
   ```

After you grant the required privileges, a user with the `prod_role` role must follow these steps:

1. Create the model from the source model:

   Copy code

   ```
   CREATE MODEL prod_db.prod_schema.invoices_model
     WITH VERSION V1
     FROM MODEL dev_db.dev_schema.invoices_source_model
    VERSION V1;
   ```
2. Optional: Add another version of the model:

   Copy code

   ```
   ALTER MODEL prod_db.prod_schema.invoices_model
     ADD VERSION V2
     FROM MODEL dev_db.dev_schema.invoices_source_model
    VERSION V2;
   ```

Note

The model in the target schema is a separate model object from the model in the replicated database. New versions are not copied automatically;
you must add each version using [ALTER MODEL … ADD VERSION](/sql-reference/sql/alter-model-add-version).

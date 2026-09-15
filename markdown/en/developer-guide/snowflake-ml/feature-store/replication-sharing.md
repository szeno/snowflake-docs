# Replicating and sharing features

Because feature store objects are implemented as Snowflake objects, they support replication and sharing.

## Replicating a feature store

To replicate a feature store, replicate the database that contains its schema. Note that replicating the database
replicates all schemas in the database, not just feature stores. For more information on database replication, see
[Introduction to replication and failover across multiple accounts](/user-guide/account-replication-intro).

## Sharing a feature store

To share features across accounts, share the entire feature store by sharing the underlying schema. Because this shares
all feature views in the feature store, you might want to organize feature views into feature stores based on who they
will be shared with. For more information on sharing, see [About Secure Data Sharing](/user-guide/data-sharing-intro).

## Sharing feature views

It is also possible to share individual [feature views](/developer-guide/snowflake-ml/feature-store/feature-views). Doing so requires additional steps because
you must also share the associated tags, which the feature store uses internally. The steps below share a single
feature view.

1. Set the variables in the initial block, below, as follows:

   - FS\_SHARE: The name of the share with which the feature view will be shared.
   - FS\_DATABASE: The name of the database that contains the feature store.
   - FS\_SCHEMA: The name of the schema that contains the feature view.
   - FV\_NAME: The name and version of the feature view separated by `$`. For example, if the feature view’s name is
     `myfv` and its version is `v1`, this value is `myfv$v1`.
   - ENTITY\_NAME: The entity to which the feature view belongs.

   Copy code

   ```
   SET FS_SHARE = '<fs_share_name>';
   SET FS_DATABASE = '<fs_database_name>';
   SET FS_SCHEMA = '<fs_schema_name>';
   SET FV_NAME = '<feature_view_name_with_version>';
   SET ENTITY_NAME = '<entity_name>';
   ```
2. Execute the following statements, which set some intermediate variables, then grant most of the necessary privileges.

   Copy code

   ```
   SET SCHEMA_FQN = CONCAT($FS_DATABASE, '.', $FS_SCHEMA);
   SET TAG_OBJECT_FQN = CONCAT($SCHEMA_FQN, '.', 'SNOWML_FEATURE_STORE_OBJECT');
   SET TAG_METADATA_FQN = CONCAT($SCHEMA_FQN, '.', 'SNOWML_FEATURE_VIEW_METADATA');
   SET FULL_ENTITY_NAME = CONCAT('SNOWML_FEATURE_STORE_ENTITY_', $ENTITY_NAME);
   SET ENTITY_FQN = CONCAT($SCHEMA_FQN, '.', $FULL_ENTITY_NAME);
   SET FV_FQN = CONCAT($SCHEMA_FQN, '.', $FV_NAME);

   -- Grant privileges to target share
   GRANT USAGE ON DATABASE IDENTIFIER($FS_DATABASE) TO SHARE IDENTIFIER($FS_SHARE);
   GRANT REFERENCE_USAGE ON DATABASE IDENTIFIER($FS_DATABASE) to SHARE IDENTIFIER($FS_SHARE);
   GRANT USAGE ON SCHEMA IDENTIFIER($SCHEMA_FQN) TO SHARE IDENTIFIER($FS_SHARE);
   GRANT READ ON TAG IDENTIFIER($TAG_OBJECT_FQN) TO SHARE IDENTIFIER($FS_SHARE);
   GRANT READ ON TAG IDENTIFIER($TAG_METADATA_FQN) TO SHARE IDENTIFIER($FS_SHARE);
   GRANT READ ON TAG IDENTIFIER($ENTITY_FQN) TO SHARE IDENTIFIER($FS_SHARE);
   ```
3. Finally, execute one of the two statements below depending on the type of feature view you are sharing.

   - For a [Snowflake-managed feature view](/developer-guide/snowflake-ml/feature-store/feature-views#label-feature-store-feature-view-managed):

     Copy code

     ```
     GRANT SELECT ON DYNAMIC TABLE IDENTIFIER($FV_FQN) TO SHARE IDENTIFIER($FS_SHARE);
     ```
   - For an [external feature view](/developer-guide/snowflake-ml/feature-store/feature-views#label-feature-store-feature-view-external):

     Copy code

     ```
     GRANT SELECT ON VIEW IDENTIFIER($FV_FQN) TO SHARE IDENTIFIER($FS_SHARE);
     ```

# Managing compute pools

A compute pool is a collection of one or more virtual machine (VM) nodes on which Snowflake runs your
Snowpark Container Services jobs and services.

For more information about compute pools, see [Snowpark Container Services: Working with compute pools](/developer-guide/snowpark-container-services/working-with-compute-pool).

This topic shows how to do the following tasks with services:

- [Create a compute pool](#label-sfcli-pool-create)
- [Create a compute pool from a project definition](#label-sfcli-pool-pdf)
- [Suspend and resume a compute pool](#label-sfcli-pool-suspend-resume)
- [Set and unset a compute pool’s properties or parameters](#label-sfcli-pool-set-unset)
- [Stop all services in a compute pool](#label-sfcli-pool-stop-all)

For common operations, such as listing or dropping, Snowflake CLI uses `snow object` commands as described in [Managing Snowflake objects](/developer-guide/snowflake-cli/objects/manage-objects).

## Create a compute pool

To create a compute pool named “pool\_1” composed of two CPUs with 4 GB of memory, enter a
[spcs pool create](/developer-guide/snowflake-cli/command-reference/spcs-commands/compute-pool-commands/create) command similar to the following:

Copy code

```
snow spcs compute-pool create "pool_1" --min-nodes 2 --max-nodes 2 --family "CPU_X64_XS"
```

For more information about instance families, see the SQL `CREATE COMPUTE POOL` command.

## Create a compute pool from a project definition

You can create a compute pool from a `snowflake.yml` project definition file and then executing the `snow spcs compute-pool deploy` command.

The following shows a sample `snowflake.yml` project definition file:

Copy code

```
definition_version: 2
entities:
  my_compute_pool:
    type: compute-pool
    identifier:
      name: my_compute_pool
    min_nodes: 1
    max_nodes: 2
    instance_family: CPU_X64_XS
    auto_resume: true
    initially_suspended: true
    auto_suspend_seconds: 60
    comment: "My compute pool"
    tags:
      - name: my_tag
        value: tag_value
```

The following table describes the properties of a compute pool project definition.

**Compute pool project definition properties**

| Property | Definition |
| --- | --- |
| **type**  *required*, *string* | Must be `compute-pool`. |
| **identifier**  *optional*, *string* | Snowflake identifier for the entity. The value can have the following forms:   - String identifier text   Copy code  ``` identifier: my-compute-pool ```  Both unquoted and quoted identifiers are supported. To use quoted identifiers, include the surrounding quotes in the YAML value (for example, `"My Compute Pool"`).   - Object   Copy code  ``` identifier:   name: my-compute-pool   schema: my-schema # optional   database: my-db # optional ```  Note  An error occurs if you specify a `schema` or `database` and use a fully qualified name in the `name` property (such as `mydb.schema1.my-app`). |
| **instance\_family**  *required*, *string* | Name of the instance family. For a list of available instance families, see the [CREATE COMPUTE POOL INSTANCE\_FAMILY](/sql-reference/sql/create-compute-pool#label-sql-cp-instance-family) parameter. |
| **min\_nodes**  *optional*, *string* | Minimum number of nodes for the compute pool. This value must be greater than 0.  Default: `1` |
| **max\_nodes**  *optional*, *int* | Maximum number of nodes for the compute pool. |
| **auto\_resume**  *optional*, *boolean* | Whether to automatically resume a compute pool when a service or job is submitted to it.  Default: `True` |
| **initially\_suspended**  *optional*, *boolean* | Whether the compute pool is created initially in the suspended state. If `true`, Snowflake doesn’t provision any nodes requested for the compute pool at the compute pool creation time.  Default: `False` |
| **auto\_suspend\_seconds**  *optional*, *int* | Number of seconds of inactivity after which you want Snowflake to automatically suspend the compute pool.  Default: `3600` |
| **comment**  *optional*, *string* | Comments to associate with the compute pool. |
| **tags**  *optional*, *Tag sequence* | Tag names and values for the compute pool. For more information, see [Tag quotas](/user-guide/object-tagging/introduction#label-object-tagging-quota) |

Expand

Show lessSee more

To create and deploy the compute pool to a stage, do the following:

1. Change your current directory to the directory containing the project definition file.
2. Run a `snow spcs compute-pool deploy` command similar to the following:

   Copy code

   ```
   snow spcs compute-pool deploy
   ```

   ```
   +---------------------------------------------------------------------+
   | key    | value                                                      |
   |--------+------------------------------------------------------------|
   | status | Compute pool MY_COMPUTE_POOL successfully created.         |
   +---------------------------------------------------------------------+
   ```

## Suspend and resume a compute pool

Note

The current role must have OPERATE privilege on the compute pool to suspend or resume it.

To suspend a compute pool, enter a command similar to the following:

Copy code

```
snow spcs compute-pool suspend tutorial_compute_pool
```

```
+-------------------------------------------+
| key    | value                            |
|--------+----------------------------------|
| status | Statement executed successfully. |
+-------------------------------------------+
```

To resume a suspended compute pool, enter a command similar to the following:

Copy code

```
snow spcs compute-pool resume tutorial_compute_pool
```

```
+-------------------------------------------+
| key    | value                            |
|--------+----------------------------------|
| status | Statement executed successfully. |
+-------------------------------------------+
```

## Set and unset a compute pool’s properties or parameters

Note

The current role must have MODIFY privilege on the compute pool to set properties.

To set a property or parameter, enter a command similar to the following:

Copy code

```
snow spcs compute-pool set tutorial_compute_pool --min-nodes 2 --max-nodes 4
```

```
+-------------------------------------------+
| key    | value                            |
|--------+----------------------------------|
| status | Statement executed successfully. |
+-------------------------------------------+
```

To reset a property or parameter to its default value, enter a command similar to the following:

Copy code

```
snow spcs compute-pool unset tutorial_compute_pool --auto-resume
```

```
+-------------------------------------------+
| key    | value                            |
|--------+----------------------------------|
| status | Statement executed successfully. |
+-------------------------------------------+
```

## Stop all services in a compute pool

Stopping a compute pool deletes all of the services running on the compute pool; however, it does not stop the compute pool itself.

To stop a compute pool, enter a [spcs compute-pool stop-all](/developer-guide/snowflake-cli/command-reference/spcs-commands/compute-pool-commands/stop-all) command similar to the following:

Copy code

```
snow spcs compute-pool stop-all "pool_1"
```

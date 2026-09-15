# Ingestion scheduler

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

Library which provides common elements and features that are used in all Snowflake connectors.

## Requirements

Default implementation of the scheduler requires the following files to be executed during the connector installation:

- `core.sql` (See: [Core SQL reference](/developer-guide/native-apps/connector-sdk/reference/core_reference))
- `configuration/app_config.sql` (See: [App config SQL reference](/developer-guide/native-apps/connector-sdk/reference/app_config_reference))
- `configuration/connector_configuration.sql` (See: [Connector configuration reference](/developer-guide/native-apps/connector-sdk/reference/connector_configuration_reference))
- `scheduler/scheduler.sql` (See: [Ingestion scheduler reference](/developer-guide/native-apps/connector-sdk/reference/scheduler_reference))

## Overview

The scheduler task takes care of triggering the ingestion of resources at appropriate times according to their configuration.
This task is not started by the SDK itself and needs to be created and resumed, for example, during finalize configuration step.
There are two ways of achieving this: using the procedure called [PUBLIC.CREATE\_SCHEDULER()](/developer-guide/native-apps/connector-sdk/reference/scheduler_reference#label-connectors-native-sdk-create-scheduler) from SQL
or by calling [SchedulerCreator#createScheduler()](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/scheduler/SchedulerCreator.html#createScheduler()) directly from the Java code.

The default implementation will create the scheduler task using the expression provided in `connector_configuration`, under the
`global_schedule` key. When the default scheduler task is executed it searches for all the enabled resource ingestion definitions that
have their [ScheduleType](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/ingestion/definition/ScheduleType.html) in configuration set to `GLOBAL` and their corresponding ingestion processes.
Each of the processes is then updated to `IN_PROGRESS` status. This status will be updated again to `SCHEDULED` after ingestion iteration is finished.
Then for each of them [OnIngestionScheduledCallback](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/application/scheduler/OnIngestionScheduledCallback.html) is executed.
This callback can be completely custom and can be implemented using SQL or Java. The default implementation of this callback does nothing,
however the SDK also provides an implementation of this callback using the [Task reactor](/developer-guide/native-apps/connector-sdk/using/task_reactor) module. This implementation retrieves
the data about resources from the database and puts a work item containing this data in the Task Reactor queue.

When the work item is finished another callback called [OnIngestionFinishedCallback](/developer-guide/native-apps/connector-sdk/java/com/snowflake/connectors/taskreactor/OnIngestionFinishedCallback.html) is executed.
This callback changes the process state back to `SCHEDULED` once the ingestion is done.

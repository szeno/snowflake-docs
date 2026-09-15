# Troubleshoot budgets

This topic explains how to [monitor budgets for problems](#label-budgets-troubleshoot-event-table) and provides
[solutions to common issues](#label-budgets-troubleshoot-errors).

## Using an event table to monitor budgets

You can use an [event table](/developer-guide/logging-tracing/event-table-setting-up) to collect telemetry data related to budgets.
After Snowflake starts collecting the data in the event table, you can query the table, create a stream to track changes, or
set alerts to send notifications when certain events occur.

If you don’t want to collect telemetry data for budgets, you must set the
[ENABLE\_BUDGET\_EVENT\_LOGGING](/sql-reference/parameters#label-enable-budget-event-logging) account parameter to `FALSE` to turn it off.

### Understanding the events

The following table describes the values in the event table that correspond to budget events so you can focus on the appropriate
events. For detailed information about the structure of an event table, see [Event table columns](/developer-guide/logging-tracing/event-table-columns).

| Event table column | Field | Value | Description |
| --- | --- | --- | --- |
| `resource_attributes` | `snow.cost.budget.id` | `budget_id` | Unique ID of the budget instance. |
|  | `snow.cost.budget.name` | `budget_name` | Fully qualified name of the budget instance. |
| `scope` | `name` | `snow.cost.budget` | Constant identifier for all budget telemetry events. |
| `record_type` | n/a | `EVENT` | Indicates a budget log event. |
| `record` | `name` | `event_name` | Descriptive event name. Possible values include the following:   - `BUDGET_UNVERIFIED_RECIPIENTS` — Occurs when email addresses are not in the integration’s allowed recipients list or there   are email addresses that are not verified. - `BUDGET_INVALID_INTEGRATION` — Occurs when a notification integration doesn’t exist or the user lacks access to it. |
|  | `severity_text` | `INFO`, `WARNING`, or `ERROR` | Severity level of budget event. |
| `value` | `message` | `message` | Descriptive event message, often including contextual details such as an integration name or operation. |

Expand

Show lessSee more

Use the following examples to better understand how to identify budget events in an event table.

Query: Find all events related to the propagation of all budgets within the account
:   Copy code

    ```
    SELECT
        TIMESTAMP,
        RESOURCE_ATTRIBUTES,
        SCOPE,
        RECORD_TYPE,
        RECORD,
        VALUE
      FROM SNOWFLAKE.TELEMETRY.EVENTS
      WHERE
        RECORD_TYPE = 'EVENT' AND
        SCOPE['name'] = 'snow.cost.budget';
    ```

Query: Find all events related to a specific budget (for example, `MY_DB.SCH1.MY_BUDGET`)
:   Copy code

    ```
    SELECT
        TIMESTAMP,
        RESOURCE_ATTRIBUTES,
        SCOPE,
        RECORD_TYPE,
        RECORD,
        VALUE
      FROM SNOWFLAKE.TELEMETRY.EVENTS
      WHERE
        RECORD_TYPE = 'EVENT' AND
        SCOPE['name'] = 'snow.cost.budget'
        AND RESOURCE_ATTRIBUTES['snow.cost.budget.name'] ILIKE 'MY_DB.SCH1.MY_BUDGET';
    ```

## Troubleshooting specific problems

The following scenarios can help you troubleshoot issues that can occur when creating or editing budgets:

- [You can’t activate the account budget](#you-can-t-activate-the-account-budget)
- [You can’t create a custom budget](#you-can-t-create-a-custom-budget)
- [You can’t activate a custom budget](#you-can-t-activate-a-custom-budget)
- [You can’t call methods on the account budget](#you-can-t-call-methods-on-the-account-budget)
- [You can’t add or remove objects from a custom budget](#you-can-t-add-or-remove-objects-from-a-custom-budget)
- [You can’t set email notifications for a budget](#you-can-t-set-email-notifications-for-a-budget)
- [You can’t successfully call the GET\_SERVICE\_TYPE\_USAGE method](#you-can-t-successfully-call-the-get-service-type-usage-method)
- [The Budgets feature is not available for your account](#the-budgets-feature-is-not-available-for-your-account)

### You can’t activate the account budget

There are multiple reasons you might be unable to activate your account budget:

|  |  |
| --- | --- |
| Error | ``` Unknown user-defined function SNOWFLAKE.LOCAL.ACTIVATE ``` |
| Cause | If your Snowflake account is new, the account budget is not yet available in your account. |
| Solution | Wait for the account budget to be available in your newly created account. You can activate it after it becomes available. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` FAILURE: Uncaught exception of type 'BUDGET_ALREADY_ACTIVATED' on line X at position X ``` |
| Cause | The account budget has already been activated. |
| Solution | You can call the [<budget\_name>!GET\_CONFIG](/sql-reference/classes/budget/methods/get_config) method to view the activation timestamp:  Copy code  ``` CALL SNOWFLAKE.LOCAL.ACCOUNT_ROOT_BUDGET!GET_CONFIG(); ``` |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` -20000 (P0001): Uncaught exception of type 'NO_PERMISSION_TO_ACTIVATE_BUDGET' on line X at position X ``` |
| Cause | Your account does not yet support the Budgets feature. |
| Solution | The Budgets feature is not available for accounts in Gov regions. Support for Gov regions will be available in a future release. |

Expand

Show lessSee more

### You can’t create a custom budget

There are multiple reasons you might be unable to create a custom budget.

|  |  |
| --- | --- |
| Error | ``` FAILURE: SQL access control error: Insufficient privileges to operate on class 'BUDGET' ``` |
| Cause | The role you are using does not have the privileges required to create custom budgets. |
| Solution | Use a role with the required privileges. See [Create a custom role to create budgets](/user-guide/budgets/custom-budget#label-custom-budgets-owner-role). |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` FAILURE: Uncaught exception of type 'STATEMENT_ERROR' on line 0 at position -1 : Uncaught exception of type 'UNSUPPORTED_BUDGET_TYPE' on line X at position X ``` |
| Cause | You pass arguments to the constructor method to create a budget. |
| Solution | See [CREATE BUDGET](/sql-reference/classes/budget/commands/create-budget) and edit your create statement. |

Expand

Show lessSee more

### You can’t activate a custom budget

|  |  |
| --- | --- |
| Error | ``` FAILURE: Uncaught exception of type 'STATEMENT_ERROR' on line 0 at position -1 : Uncaught exception of type 'UNSUPPORTED_BUDGET_TYPE' on line X at position X ``` |
| Cause | You tried to call the ACTIVATE method on a custom budget. |
| Solution | The ACTIVATE method is only available on the account budget. After you have created a custom budget, use the [<budget\_name>!SET\_SPENDING\_LIMIT](/sql-reference/classes/budget/methods/set_spending_limit) and [<budget\_name>!SET\_EMAIL\_NOTIFICATIONS](/sql-reference/classes/budget/methods/set_email_notifications) methods to configure the budget and start receiving notification emails. |

Expand

Show lessSee more

### You can’t call methods on the account budget

There are multiple reasons why calling a method on the account budget might fail.

|  |  |
| --- | --- |
| Error | ``` -20000 (P0001): Uncaught exception of type 'FUNCTION_NOT_SUPPORTED_FOR_ACCOUNT_ROOT_BUDGET' on line 11 at position 18 ``` |
| Cause | You tried to call any of the following methods on the account budget:   - [ADD\_RESOURCE()](/sql-reference/classes/budget/methods/add_resource) - [REMOVE\_RESOURCE()](/sql-reference/classes/budget/methods/remove_resource) - [GET\_LINKED\_RESOURCES()](/sql-reference/classes/budget/methods/get_linked_resources) |
| Solution | These methods are not available on the account budget. The account budget monitors all supported objects in the account and objects cannot be added or removed. For more information, see [Account budget and custom budgets](/user-guide/budgets#label-account-and-custom-budgets). |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` -20000 (P0001): Uncaught exception of type 'ACCOUNT_ROOT_BUDGET_NOT_ACTIVATED' on line X at position X ``` |
| Cause | You tried to call a method on the account budget before the account budget is activated. |
| Solution | [Activate the account budget](/user-guide/budgets/account-budget#label-activate-account-budget). |

Expand

Show lessSee more

### You can’t add or remove objects from a custom budget

To successfully add or remove an object from a custom budget, the role used to call the method must have the
[required privileges and role](/user-guide/budgets/monitor#label-custom-budgets-monitor-role).

|  |  |
| --- | --- |
| Error | ``` 002141 (42601): SQL compilation error: Unknown user-defined function <budget_db>.<budget_schema>.<budget_name>!ADD_RESOURCE ``` |
| Cause | The role you used to call the instance method does not have the required privileges to add (or remove) objects from the budget. |
| Solution | Grant the required instance role and privileges to the role used to call the method. For more information, see [Create a custom role to monitor a custom budget](/user-guide/budgets/monitor#label-custom-budgets-monitor-role). |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` 002003 (02000): SQL compilation error: <object_type> '<object_name>' does not exist or not authorized. ``` |
| Cause | You tried to add an object to a custom budget but the role you used to call the method doesn’t have the required privileges. |
| Solution | To add (or remove) an object from a budget, the role used to call the method must have the APPLYBUDGET privilege on the object. If the parent object is a database or schema, you must also have the USAGE privilege on the database and schema that contain the object.  For more information, see the list of [required object privileges](/user-guide/budgets#label-budgets-roles-and-privileges). |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` Uncaught exception of type 'EXPRESSION_ERROR' on line 10 at position 21 : Privilege 'APPLYBUDGET' is not authorized on the reference object. ``` |
| Cause | You tried to create a reference for an object without specifying the PRIVILEGE parameter in the SYSTEM$REFERENCE statement. |
| Solution | Create the reference with the APPLYBUDGET privilege on the object. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` 505001 (55000): Uncaught exception of type 'EXPRESSION_ERROR' on line 10 at position 21 : Specified object does not exist or not authorized for the reference. ``` |
| Cause | There are multiple causes for this error message:   - You tried to add the SNOWFLAKE database to a custom budget with an inline SYSTEM$REFERENCE statement. - You don’t have the required privileges on the object to create a reference for it. The valid reference is required to add   the object to a budget. |
| Solution | - The SNOWFLAKE database cannot be added to a budget. See the [usage notes for ADD\_RESOURCE](/sql-reference/classes/budget/methods/add_resource#label-budget-add-resource-usage-notes). - Grant the required privileges on the object you want to add to the budget. For more information, see the list of   [required object privileges](/user-guide/budgets#label-budgets-roles-and-privileges). |

Expand

Show lessSee more

### You can’t set email notifications for a budget

The following scenarios can help you troubleshoot common issues when calling the
[<budget\_name>!SET\_EMAIL\_NOTIFICATIONS](/sql-reference/classes/budget/methods/set_email_notifications) method.

|  |  |
| --- | --- |
| Error | ``` Unknown user-defined function <database_name>.<schema_name>.<budget_name>.SET_EMAIL_NOTIFICATIONS ``` |
| Cause | The role you used to set the email notifications for a custom budget does not have the ADMIN instance role. |
| Solution | Use a role with the required privileges and roles. See the [Access control requirements](/sql-reference/classes/budget/methods/set_email_notifications#label-set-email-notifications-acr) for SET\_EMAIL\_NOTIFICATIONS. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` Integration '<INTEG_NAME>' does not exist or not authorized. ``` |
| Cause | The notification integration does not exist. |
| Solution | Use a valid notification integration. For more information, see [Create an email notification integration](/user-guide/notifications/email-notifications#label-create-email-notification-integration). Include the email addresses for budgets notifications in the ALLOWED\_RECIPIENTS list. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` FAILURE: Uncaught exception of type 'EXPRESSION_ERROR' on line 16 at position 34 : Following email address(es) are not allowed by the email integration <INTEGRATION_NAME>: [<email>] ``` |
| Cause | The email addresses are not included in the notification integration. |
| Solution | Add the email addresses to the notification integration, or use a notification integration that includes all the email addresses in the ALLOWED\_RECIPIENTS list. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` Email recipients in the given list at indexes [<index_list>] are not allowed. Either these email addresses are not yet validated or do not belong to any user in the current account. ``` |
| Cause | Some or all of the email addresses you tried to add are not validated. |
| Solution | See [Verify the email addresses of the email notification recipients](/user-guide/notifications/email-notifications#label-email-notification-verify-address). |

Expand

Show lessSee more

### You can’t successfully call the GET\_SERVICE\_TYPE\_USAGE method

The following scenarios can help you troubleshoot common issues when calling the
[<budget\_name>!GET\_SERVICE\_TYPE\_USAGE](/sql-reference/classes/budget/methods/get_service_type_usage) method.

|  |  |
| --- | --- |
| Error | ``` 001044 (42P13): SQL compilation error: error line 0 at position -1 Invalid argument types for function 'GET_SERVICE_TYPE_USAGE': (VARCHAR(X), VARCHAR(X), VARCHAR(X), VARCHAR(X)) ``` |
| Cause | You called the method with invalid arguments or the wrong number of arguments. |
| Solution | Check that the arguments you use to call the method are valid and that you’ve included all required arguments. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` 002151 (22023): Uncaught exception of type 'STATEMENT_ERROR' on line 16 at position 23 : SQL compilation error: [:TIME_DEPART] is not a valid date/time component for function DATE_TRUNC. ``` |
| Cause | The TIME\_DEPART argument is an invalid string. |
| Solution | Use one of the valid values listed for the [TIME\_DEPART argument](/zTEMPLATES/classes/cat/methods/get_vet_service_history#label-get-service-type-usage-time-depart) in the reference topic. |

Expand

Show lessSee more

|  |  |
| --- | --- |
| Error | ``` 100094 (22000): Uncaught exception of type 'STATEMENT_ERROR' on line 16 at position 23 : Unknown timezone: '<invalid_timezone>' ``` |
| Cause | The USER\_TIMEZONE argument is an invalid string. |
| Solution | Use a valid timezone string. For more information, see the [usage notes for GET\_SERVICE\_TYPE\_USAGE](/zTEMPLATES/classes/cat/methods/get_vet_service_history#label-get-service-type-usage-usage-notes). |

Expand

Show lessSee more

### The Budgets feature is not available for your account

|  |  |
| --- | --- |
| Errors | ``` FAILURE: SQL compilation error: Class 'SNOWFLAKE.CORE.BUDGET' does not exist or not authorized. ```  ``` 000002 (0A000): Uncaught exception of type 'STATEMENT_ERROR' on line 0 at position -1 : Unsupported feature 'TOK_RESOURCE_GROUP'. ``` |
| Cause | Your account does not yet support the Budgets feature. |
| Solution | The Budgets feature is not available for accounts in Gov regions. Support for Gov regions will be available in a future release. |

Expand

Show lessSee more

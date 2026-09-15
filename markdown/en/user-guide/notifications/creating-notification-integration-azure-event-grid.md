# Creating a notification integration to send notifications to a Microsoft Azure Event Grid topic

To send notifications to a Microsoft Azure Event Grid topic, you must create a notification integration for that topic. To do
this:

1. [Create a custom Event Grid topic](#label-notification-integration-azure-custom-topic).
2. [Create a notification integration](#label-notification-integration-azure-creating-integration).

Note

Currently, this feature is limited to Snowflake accounts hosted on Microsoft Azure.

## Create a custom Event Grid topic

An Event Grid topic provides an endpoint where the source sends event notifications. Create a dedicated topic to receive
notifications published by Snowflake.

Note

If you plan to use the topic for notifications about errors in [tasks](/user-guide/tasks-errors) or
[pipes](/user-guide/data-load-snowpipe-errors), you can use a single topic for error notifications for all tasks or pipes.

For instructions on creating Event Grid topics, see the
[Event Grid documentation](https://docs.microsoft.com/en-us/azure/event-grid/custom-event-quickstart).

Record the Event Grid topic endpoint, which you will need later in these instructions.

Optionally, subscribe to the topic to inform Event Grid which events you want to track and where to send those events.

## Create notification integration in Snowflake

### Retrieve the tenant ID

Retrieve your Azure tenant ID, which you will need later in these instructions.

1. Log into the Microsoft Azure portal.
2. Navigate to **Azure Active Directory** » **Properties**. Record the **Tenant ID** value for reference later.
   The directory ID, or *tenant ID*, is needed to generate the consent URL that grants Snowflake access to the Event Grid topic.

### Create the notification integration

Run the [CREATE NOTIFICATION INTEGRATION](/sql-reference/sql/create-notification-integration-queue-outbound-azure) command
to create a notification integration. An integration is a Snowflake object that references the Event Grid topic you created.

When running the command, set these parameters to the following values:

- Set AZURE\_EVENT\_GRID\_TOPIC\_ENDPOINT to the
  [Event Grid topic endpoint, which you recorded earlier](#label-notification-integration-azure-custom-topic).
- Set AZURE\_TENANT\_ID to your [Azure tenant ID](#label-notification-integration-azure-creating-integration-tenant-id).

For example:

Copy code

```
CREATE NOTIFICATION INTEGRATION my_notification_int
  ENABLED = TRUE
  DIRECTION = OUTBOUND
  TYPE = QUEUE
  NOTIFICATION_PROVIDER = AZURE_EVENT_GRID
  AZURE_EVENT_GRID_TOPIC_ENDPOINT = 'https://myaccount.region-1.eventgrid.azure.net/api/events'
  AZURE_TENANT_ID = 'mytenantid';
```

### Grant Snowflake access to the topic

1. Execute the [DESCRIBE NOTIFICATION INTEGRATION](/sql-reference/sql/desc-notification-integration) command to display the properties of the notification
   that you just created.

   For example, to display the properties of the notification integration named `my_notification_int`:
2. Record the values of the following properties:

   - AZURE\_CONSENT\_URL

     URL to the Microsoft permissions request page.
   - AZURE\_MULTI\_TENANT\_APP\_NAME

     Name of the Snowflake client application created for your account. In a later step in this section, you will need to grant
     this application the permissions necessary to obtain an access token on your allowed topic.
3. In a web browser, navigate to the URL specified by the AZURE\_CONSENT\_URL property. The page displays a Microsoft permissions
   request page.
4. Select **Accept**. This action allows the Azure service principal created for your Snowflake account to be granted an
   access token on specified resources inside your tenant. Obtaining an access token succeeds only if you grant the service
   principal the appropriate permissions on the container (see the next step).

   The Microsoft permissions request page redirects to the Snowflake corporate site (snowflake.com).
5. Log into the Microsoft Azure portal.
6. Navigate to **Azure Active Directory** » **Enterprise applications**. Verify that the Snowflake application
   identifier you recorded earlier (the value of the AZURE\_MULTI\_TENANT\_APP\_NAME property) is listed.

   Important

   If you delete the Snowflake application in Azure Active Directory at a later time, the notification integration stops
   working.
7. Navigate to **Event Grid Topics** » `topic_name`, where `topic_name` is the name of the topic you
   created to receive event notifications.
8. Select **Access Control (IAM)** » **Add role assignment**.
9. Search for the Snowflake service principal. This is the identity in the AZURE\_MULTI\_TENANT\_APP\_NAME property that you recorded
   earlier. Search for the string before the underscore in the AZURE\_MULTI\_TENANT\_APP\_NAME property.

   Important

   - It can take an hour or longer for Azure to create the Snowflake service principal requested through the Microsoft
     request page in this section. If the service principal is not available immediately, we recommend waiting an hour or two
     and then searching again.
   - If you delete the service principal, the notification integration stops working.
10. Grant the Snowflake application the
    [EventGrid Data Sender](https://docs.microsoft.com/en-us/azure/role-based-access-control/built-in-roles#eventgrid-data-sender)
    permission.

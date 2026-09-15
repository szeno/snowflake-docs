# Managing Snowflake integrations with Python

You can use Python to manage different types of integrations in Snowflake.

## Prerequisites

The examples in this topic assume that you’ve added code to connect with Snowflake and to create a `Root` object from which to use the
Snowflake Python APIs.

For example, the following code uses connection parameters defined in a configuration file to create a connection to Snowflake:

Copy code

```
from snowflake.core import Root
from snowflake.snowpark import Session

session = Session.builder.config("connection_name", "myconnection").create()
root = Root(session)
```

Using the resulting `Session` object, the code creates a `Root` object to use the API’s types and methods. For more information,
see [Connect to Snowflake with the Snowflake Python APIs](/developer-guide/snowflake-python-api/snowflake-python-connecting-snowflake).

## Managing catalog integrations

You can manage catalog integrations for Apache Iceberg™ tables in your account. A catalog integration is a named, account-level Snowflake
object that stores information about how your Iceberg table metadata is organized for scenarios when you don’t use Snowflake as the Iceberg
catalog, or when you want to integrate with Snowflake Open Catalog. For more information, see the [Catalog integration](/user-guide/tables-iceberg#label-tables-iceberg-catalog-integration-def)
section in [Apache Iceberg™ tables](/user-guide/tables-iceberg).

Note

[ALTER CATALOG INTEGRATION](/sql-reference/sql/alter-catalog-integration) is currently not supported.

The Snowflake Python APIs represents catalog integrations with two separate types:

- `CatalogIntegration`: Exposes a catalog integration’s properties such as its name, table format, and catalog settings.
- `CatalogIntegrationResource`: Exposes methods you can use to fetch a corresponding `CatalogIntegration` object and drop the
  catalog integration.

### Creating a catalog integration

To create a catalog integration, first create a `CatalogIntegration` object, and then create a `CatalogIntegrationCollection`
object from the API `Root` object. Using `CatalogIntegrationCollection.create`, add the new catalog integration to Snowflake.

You can create catalog integrations in your account for the following types of external Iceberg catalogs.

#### AWS Glue

Code in the following example creates a `CatalogIntegration` object that represents a catalog integration named
`my_catalog_integration` for Iceberg tables that use AWS Glue with the specified properties:

Copy code

```
from snowflake.core.catalog_integration import CatalogIntegration, Glue

root.catalog_integrations.create(CatalogIntegration(
    name="my_catalog_integration",
    catalog = Glue(
        catalog_namespace="abcd-ns",
        glue_aws_role_arn="arn:aws:iam::123456789012:role/sqsAccess",
        glue_catalog_id="1234567",
    ),
    table_format="ICEBERG",
    enabled=True,
))
```

#### Object store

Code in the following example creates a `CatalogIntegration` object that represents a catalog integration named
`my_catalog_integration` for Iceberg tables that use an object store:

Copy code

```
from snowflake.core.catalog_integration import CatalogIntegration, ObjectStore

root.catalog_integrations.create(CatalogIntegration(
    name="my_catalog_integration",
    catalog = ObjectStore(),
    table_format="ICEBERG",
    enabled=True,
))
```

#### Snowflake Open Catalog

Code in the following example creates a `CatalogIntegration` object that represents a catalog integration named
`my_catalog_integration` for Iceberg tables that use Open Catalog with the specified properties:

Copy code

```
from snowflake.core.catalog_integration import CatalogIntegration, OAuth, Polaris, RestConfig

root.catalog_integrations.create(CatalogIntegration(
    name="my_catalog_integration",
    catalog = Polaris(
        catalog_namespace="abcd-ns",
        rest_config=RestConfig(
            catalog_uri="https://my_account.snowflakecomputing.com/polaris/api/catalog",
            warehouse="my-warehouse",
        ),
        rest_authentication=OAuth(
            type="OAUTH",
            oauth_client_id="my_client_id",
            oauth_client_secret="my_client_secret",
            oauth_allowed_scopes=["PRINCIPAL_ROLE:ALL"],
        ),
    ),
    table_format="ICEBERG",
    enabled=True,
))
```

### Getting catalog integration details

You can get information about a catalog integration by calling the `CatalogIntegrationResource.fetch` method, which returns a
`CatalogIntegration` object.

Code in the following example gets information about a catalog integration named `my_catalog_integration`:

Copy code

```
my_catalog_integration = root.catalog_integrations["my_catalog_integration"].fetch()
print(my_catalog_integration.to_dict())
```

### Listing catalog integrations

You can list catalog integrations using the `CatalogIntegrationCollection.iter` method, which returns a `PagedIter` iterator of
`CatalogIntegration` objects.

Code in the following example lists catalog integrations whose name starts with `my`, and prints the name of each:

Copy code

```
catalog_integration_iter = root.catalog_integrations.iter(like="my%")
for catalog_integration_obj in catalog_integration_iter:
  print(catalog_integration_obj.name)
```

### Dropping a catalog integration

You can drop a catalog integration with a `CatalogIntegrationResource` object.

Code in the following example gets the `my_catalog_integration` catalog integration resource object and then drops the catalog
integration.

Copy code

```
my_catalog_integration_res = root.catalog_integrations["my_catalog_integration"]
my_catalog_integration_res.drop()
```

## Managing notification integrations

You can manage notification integrations, which are Snowflake objects that provide an interface between Snowflake and third-party messaging
services such as third-party cloud message queuing services, email services, and webhooks. For more information, see
[Notifications in Snowflake](/user-guide/notifications/about-notifications).

Note

[ALTER NOTIFICATION INTEGRATION](/sql-reference/sql/alter-notification-integration) is currently not supported.

The Snowflake Python APIs represents notification integrations with two separate types:

- `NotificationIntegration`: Exposes a notification integration’s properties such as its name and notification hook settings.
- `NotificationIntegrationResource`: Exposes methods you can use to fetch a corresponding `NotificationIntegration` object and
  drop the notification integration.

### Creating a notification integration

To create a notification integration, first create a `NotificationIntegration` object, and then create a
`NotificationIntegrationCollection` object from the API `Root` object. Using `NotificationIntegrationCollection.create`,
add the new notification integration to Snowflake.

You can create a notification integration for the following types of messaging services.

#### Email

Code in the following example creates a `NotificationIntegration` object that represents a notification integration named
`my_email_notification_integration` with the specified `NotificationEmail` properties:

Copy code

```
from snowflake.core.notification_integration import NotificationEmail, NotificationIntegration

my_notification_integration = NotificationIntegration(
  name="my_email_notification_integration",
  notification_hook=NotificationEmail(
      allowed_recipients=["test1@snowflake.com", "test2@snowflake.com"],
      default_recipients=["test1@snowflake.com"],
      default_subject="test default subject",
  ),
  enabled=True,
)

root.notification_integrations.create(my_notification_integration)
```

#### Webhooks

Code in the following example creates a `NotificationIntegration` object that represents a notification integration named
`my_webhook_notification_integration` with the specified `NotificationWebhook` properties:

Copy code

```
from snowflake.core.notification_integration import NotificationIntegration, NotificationWebhook

my_notification_integration = NotificationIntegration(
  name="my_webhook_notification_integration",
  enabled=False,
  notification_hook=NotificationWebhook(
      webhook_url=webhook_url,
      webhook_secret=WebhookSecret(
          # This example assumes that this secret already exists
          name="mySecret".upper(), database_name=database, schema_name=schema
      ),
      webhook_body_template=webhook_template,
      webhook_headers=webhook_headers,
  ),
)

root.notification_integrations.create(my_notification_integration)
```

#### Amazon SNS topics (outbound)

Code in the following example creates a `NotificationIntegration` object that represents a notification integration named
`my_aws_sns_outbound_notification_integration` with the specified `NotificationQueueAwsSnsOutbound` properties:

Copy code

```
from snowflake.core.notification_integration import NotificationIntegration, NotificationQueueAwsSnsOutbound

my_notification_integration = NotificationIntegration(
  name="my_aws_sns_outbound_notification_integration",
  enabled=False,
  notification_hook=NotificationQueueAwsSnsOutbound(
      aws_sns_topic_arn="arn:aws:sns:us-west-1:123456789012:sns-test-topic",
      aws_sns_role_arn="arn:aws:iam::123456789012:role/sns-test-topic",
  )
)

root.notification_integrations.create(my_notification_integration)
```

#### Azure Event Grid topics (outbound)

Code in the following example creates a `NotificationIntegration` object that represents a notification integration named
`my_azure_outbound_notification_integration` with the specified `NotificationQueueAzureEventGridOutbound` properties:

Copy code

```
from snowflake.core.notification_integration import NotificationIntegration, NotificationQueueAzureEventGridOutbound

my_notification_integration = NotificationIntegration(
  name="my_azure_outbound_notification_integration",
  enabled=False,
  notification_hook=NotificationQueueAzureEventGridOutbound(
      azure_event_grid_topic_endpoint="https://fake.queue.core.windows.net/api/events",
      azure_tenant_id="fake.onmicrosoft.com",
  )
)

root.notification_integrations.create(my_notification_integration)
```

#### Azure Event Grid topics (inbound)

Code in the following example creates a `NotificationIntegration` object that represents a notification integration named
`my_azure_inbound_notification_integration` with the specified `NotificationQueueAzureEventGridInbound` properties:

Copy code

```
from snowflake.core.notification_integration import NotificationIntegration, NotificationQueueAzureEventGridInbound

my_notification_integration = NotificationIntegration(
  name="my_azure_inbound_notification_integration",
  enabled=False,
  notification_hook=NotificationQueueAzureEventGridInbound(
      azure_storage_queue_primary_uri="https://fake.queue.core.windows.net/snowapi_queue",
      azure_tenant_id="fake.onmicrosoft.com",
  ),
)

root.notification_integrations.create(my_notification_integration)
```

#### Google Pub/Sub topics (outbound)

Code in the following example creates a `NotificationIntegration` object that represents a notification integration named
`my_gcp_outbound_notification_integration` with the specified `NotificationQueueGcpPubsubOutbound` properties:

Copy code

```
from snowflake.core.notification_integration import NotificationIntegration, NotificationQueueGcpPubsubOutbound

my_notification_integration = NotificationIntegration(
  name="my_gcp_outbound_notification_integration",
  enabled=False,
  notification_hook=NotificationQueueGcpPubsubOutbound(
      gcp_pubsub_topic_name="projects/fake-project-name/topics/pythonapi-test",
  )
)

root.notification_integrations.create(my_notification_integration)
```

#### Google Pub/Sub topics (inbound)

Code in the following example creates a `NotificationIntegration` object that represents a notification integration named
`my_gcp_inbound_notification_integration` with the specified `NotificationQueueGcpPubsubInbound` properties:

Copy code

```
from snowflake.core.notification_integration import NotificationIntegration, NotificationQueueGcpPubsubInbound

my_notification_integration = NotificationIntegration(
  name="my_gcp_inbound_notification_integration",
  enabled=True,
  notification_hook=NotificationQueueGcpPubsubInbound(
      gcp_pubsub_subscription_name="projects/fake-project-name/subscriptions/sub-test",
  )
)

root.notification_integrations.create(my_notification_integration)
```

### Getting notification integration details

You can get information about a notification integration by calling the `NotificationIntegrationResource.fetch` method, which returns
a `NotificationIntegration` object.

Code in the following example gets information about a notification integration named `my_notification_integration`:

Copy code

```
my_notification_integration = root.notification_integrations["my_notification_integration"].fetch()
print(my_notification_integration.to_dict())
```

### Listing notification integrations

You can list notification integrations using the `NotificationIntegrationCollection.iter` method, which returns a `PagedIter`
iterator of `NotificationIntegration` objects.

Code in the following example lists notification integrations whose name starts with `my`, and prints the name of each:

Copy code

```
notification_integration_iter = root.notification_integrations.iter(like="my%")
for notification_integration_obj in notification_integration_iter:
  print(notification_integration_obj.name)
```

### Dropping a notification integration

You can drop a notification integration with a `NotificationIntegrationResource` object.

Code in the following example gets the `my_notification_integration` notification integration resource object and then drops the
notification integration.

Copy code

```
my_notification_integration_res = root.notification_integrations["my_notification_integration"]
my_notification_integration_res.drop()
```

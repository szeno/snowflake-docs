# Managing Snowflake alerts with Python

You can use Python to manage Snowflake alerts, which you can set up to periodically perform an action under specific conditions, based on
data within Snowflake. For more information about alerts, see [Setting up alerts based on data in Snowflake](/user-guide/alerts).

Note

[ALTER ALERT](/sql-reference/sql/alter-alert) is currently not supported.

The Snowflake Python APIs represents alerts with two separate types:

- `Alert`: Exposes an alert’s properties such as its name, condition, action, and schedule.
- `AlertResource`: Exposes methods you can use to fetch a corresponding `Alert` object, execute the alert, and drop the alert.

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

## Creating an alert

To create an alert, first create an `Alert` object, and then create an `AlertCollection` object from the API `Root`
object. Using `AlertCollection.create`, add the new alert to Snowflake.

Code in the following example creates an `Alert` object that represents an alert named `my_alert` in your account:

Copy code

```
from snowflake.core.alert import Alert, MinutesSchedule

root.alerts.create(Alert(
    name="my_alert",
    condition="SELECT 1",
    action="SELECT 2",
    schedule=MinutesSchedule(minutes=1),
    comment="test comment"
))
```

The code creates an `AlertCollection` variable `alerts` and uses `AlertCollection.create` to create a new alert in
Snowflake.

## Getting alert details

You can get information about an alert by calling the `AlertResource.fetch` method, which returns an `Alert` object.

Code in the following example gets information about an alert named `my_alert`:

Copy code

```
my_alert = root.alerts["my_alert"].fetch()
print(my_alert.to_dict())
```

## Listing alerts

You can list alerts using the `AlertCollection.iter` method, which returns a `PagedIter` iterator of `Alert` objects.

Code in the following example lists alerts whose name starts with `my`, and then prints the name of each. This example also sets the
optional parameter `show_limit=5` to limit the number of results to `5`:

Copy code

```
alerts_iter = root.alerts.iter(like="my%", show_limit=5)
for alert_obj in alerts_iter:
  print(alert_obj.name)
```

## Performing alert operations

You can perform common alert operations, such as executing and dropping alerts, with an `AlertResource` object.

To demonstrate some operations you can do with an alert resource, code in the following example does the following:

1. Gets the `my_alert` alert resource object.
2. Executes the alert.
3. Drops the alert.

Copy code

```
my_alert_res = root.alerts["my_alert"]

my_alert_res.execute()
my_alert_res.drop()
```

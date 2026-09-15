# Responses and error handling

Preview Feature — Open

Available to accounts in all regions in all cloud providers (including government regions). For details, contact your Snowflake representative.

The Snowflake Native SDK for Connectors uses certain standard responses, especially for procedures exposed and designed to be used from the UI.
Additionally it provides a way to ensure that exceptions are mapped to valid responses and logged into the `EVENT TABLE`.

## Responses

The SDK procedures, both high-level ones and internal ones, use `variant` of a certain structure to pass information.
The requirement for such a `variant` is that it has to contain a `response_code` field,
and in some cases the response code is different than `OK`, in the required `message` field.
Any additional field can be included, but it requires further custom handling. THe response format is:

Copy code

```
{
    "response_code": "<response code>",
    "message": "<message>"
}
```

It is recommended to use this format when replacing default implementations of the procedures and objects.

## Error handling

The Snowflake Native SDK for Connectors provides a useful default mechanism to handle exceptions that can occur during runtime.
The class responsible for this is called `ConnectorErrorHelper` and its default implementation is `DefaultConnectorErrorHelper`.
This feature provides 2 customizable callbacks. The first one, `ExceptionMapper`, is responsible for wrapping all unexpected
errors into the `ConnectorException` format. This feature is used mainly to ensure responses are compliant with the format mentioned above.

The second callback, called `ExceptionLogger`, ensures that the error is logged.
This is important because all standard log entries are then saved in the `EVENT TABLE`
by Snowflake, which helps when resolving problems with the applications.

### How to use the helper

The helper exposes 2 methods:

- `withExceptionWrapping(Supplier<ConnectorResponse> action)`
- `withExceptionLogging(Supplier<T> action)`

Those methods respectively use `mapper` and `logger` mentioned above. There is also a default
implementation of a helper method which mixes those approaches together:

Copy code

```
default ConnectorResponse withExceptionLoggingAndWrapping(Supplier<ConnectorResponse> action) {
    return withExceptionWrapping(() -> withExceptionLogging(action));
}
```

It is recommended to use this wrapping at the highest possible level when invoking a
method from a `handler`. For example in ConnectionConfigurationHandler it is used like this:

Copy code

```
public static Variant setConnectionConfiguration(Session session, Variant configuration) {
    var handler = ConnectionConfigurationHandler.builder(session).build();
    return handler.setConnectionConfiguration(configuration).toVariant();
}

public ConnectorResponse setConnectionConfiguration(Variant configuration) {
    return errorHelper.withExceptionLoggingAndWrapping(
        () -> setConnectionConfigurationBody(configuration)
    );
}
```

The SDK also exposes a builder to customize this behavior, called `ConnectorErrorHelperBuilder`.
This builder allows the developer to customize the behavior of the `mapper` and `logger` callbacks.
Once customized the new `helper` can be passed to the `handler` classes in their respective `builders`.
For example:

Copy code

```
class CustomUnknownExceptionMapper implements ExceptionMapper<Exception> {

    @Override
    public ConnectorException map(Exception exception) {
        return new CustomConnectorException(exception);
    }
}

class CustomHandler {

    // Path to this method needs to be specified in the PUBLIC.SET_CONNECTION_CONFIGURATION procedure using SQL
    public static Variant configureConnection(Session session, Variant configuration) {
            //Using builder
        var errorHelper = new ConnectorErrorHelperBuilder()
            .withConnectorExceptionLogger(new CustomUnknownExceptionMapper())
            .build();

        var handler = ConnectionConfigurationHandler.builder(session)
            .withErrorHelper(errorHelper)
            .build();

        return handler.connectionConfiguration(configuration).toVariant();
    }
}
```

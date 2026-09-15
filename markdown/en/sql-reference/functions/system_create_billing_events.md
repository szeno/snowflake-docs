Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$CREATE\_BILLING\_EVENTS

Creates multiple [billable events](/developer-guide/native-apps/adding-custom-event-billing) that track consumer usage of installed
monetized applications. Use this system function when you need to exceed the one event per minute frequency limitation of [SYSTEM$CREATE\_BILLING\_EVENT](/sql-reference/functions/system_create_billing_event). This system function can only be called from an application installed in a consumer account.

## Syntax

Copy code

```
SYSTEM$CREATE_BILLING_EVENTS('<json_array_of_events>')
```

## Arguments

`'json_array_of_events'`
:   A STRING containing a JSON array of objects. Each object specifies a billing event.

    Each JSON object contains the following key-value pairs:

    Copy code

    ```
    {
      "class": "my_class",
      "subclass": "my_subclass",
      "start_timestamp": 1730825611,
      "timestamp": 1730826611,
      "base_charge": 1.00,
      "objects": "[\"my_schema.my_udf\"]",
      "additional_info": "my_additional_info"
    }
    ```

    The following table describes these key-value pairs:

    > | Key-value pair | Type | Description |
    > | --- | --- | --- |
    > | `"class"` | STRING | Identifier for the custom event class. |
    > | `"subclass"` | STRING | Identifier for the custom event subclass. This field is only used by the provider. |
    > | `"start_timestamp"` | INTEGER | The start time (UTC) of the event as a Unix timestamp in milliseconds. |
    > | `"timestamp"` | INTEGER | The timestamp (UTC) when the event was created as a Unix timestamp in milliseconds. |
    > | `"base_charge"` | DOUBLE | The amount in US dollars to charge for the billable event. The value must be greater than zero, less than 99,999.99, and must not exceed two decimal places of precision. For example, `1.00` or `0.07`. |
    > | `"objects"` | STRING | A JSON string array containing fully qualified object names that apply to the event. |
    > | `"additional_info"` | STRING | A JSON string of key-value pairs the provider can use to send additional info. |
    >
    > Expand
    >
    > Show lessSee more

## Returns

This function returns the following status messages:

> | Status message | Description |
> | --- | --- |
> | Success | Indicates the billable event was successfully created. |
> | Invalid parameter: `<PARAM_NAME>`. | Indicates an unsupported parameter was passed to the function. |
> | Only callable from within an application. | Indicates the function was called from outside an application. |
> | Payload length exceeds the limit of 9000 characters. | Indicates the call to the function exceeds the character limit. |
> | Number of events exceeds the limit of 100. | Indicates the maximum number of billable events has been reached for a single call. The specified custom event class is not used in this determination. |
> | Too many calls. At most 1 call is allowed per 10 millisecond window. | Indicates an application made too many calls to this system function within a specific period. |
>
> Expand
>
> Show lessSee more

## Usage notes

This system function can only be called from within a stored procedure in the setup script of an application created using the
Snowflake Native App Framework.

## Examples

See [Billable event examples](/developer-guide/native-apps/adding-custom-event-billing#label-native-apps-custom-billing-examples).

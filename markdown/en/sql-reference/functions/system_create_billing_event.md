Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$CREATE\_BILLING\_EVENT

Creates a [billable event](/developer-guide/native-apps/adding-custom-event-billing) that tracks consumer usage of an installed
monetized application. If you need to exceed the one event per minute frequency limitation of this system function, use [SYSTEM$CREATE\_BILLING\_EVENTS](/sql-reference/functions/system_create_billing_events). This system function can only be called from an application installed in a consumer account.

## Syntax

Copy code

```
SYSTEM$CREATE_BILLING_EVENT(
 '<class>',
 '<subclass>',
 <start_timestamp>,
 <timestamp>,
 <base_charge>,
 '<objects>',
 '<additional_info>'
 )
```

## Arguments

**Required:**

`'class'`
:   Identifier for the custom event class.

    Type: STRING

    The identifier has the following requirements:

    - Must start with a letter (A-Z) or an underscore (“\_”).
    - Must contain only letters, underscores, decimal digits (0-9), and dollar signs (“$”).
    - Length cannot exceed 64 characters.
    - Must not start with `SNOWFLAKE_`. `SNOWFLAKE_` is reserved for internal identifiers.

    The class name is stored and resolved as uppercase characters. Class name comparisons are case-insensitive.

`timestamp`
:   Specifies the timestamp (UTC) when the event was created as a Unix timestamp in milliseconds.

    Type: Integer

`base_charge`
:   Specifies the amount in US dollars to charge for the billable event. The value must be greater than zero, less than 99,999.99, and must not exceed two decimal places of precision. For example, `1.00` or `0.07`.

    Type: DOUBLE

**Optional:**

`'subclass'`
:   Identifier for the custom event subclass. This field is only used by the provider.

    Type: STRING

    The identifier has the same naming requirements as the `class` argument.

`start_timestamp`
:   Specifies the start time (UTC) of the event as a Unix timestamp in milliseconds.

    Type: INTEGER

    Use to set the start time in cases where providers want to emit an event based on a time range; otherwise set to the same
    value used for the `TIMESTAMP` argument.

`'objects'`
:   A JSON string array containing fully qualified object names that apply to this event.

    Type: STRING

    The maximum size is 4 KB.

`'additional_info'`
:   A JSON string of key-value pairs the provider can use to send additional info.

    > Type: STRING
    >
    > The maximum size is 4 KB.

## Returns

This function returns the following status messages:

> | Status message | Description |
> | --- | --- |
> | Success | Indicates the billable event was successfully created. |
> | Invalid parameter: `<PARAM_NAME>`. | Indicates an unsupported parameter was passed to the function. |
> | Only callable from within an application. | Indicates the function was called from outside an application. |
> | Payload length exceeds the limit of 9000 characters. | Indicates the call to the function exceeds the character limit. |
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

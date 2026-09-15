Categories:
:   [System functions](/sql-reference/functions-system) (System Information)

# SYSTEM$SET\_SPAN\_ATTRIBUTES (for Snowflake Scripting)

Sets attribute name and value associated with a span containing trace events.

Use SYSTEM$SET\_SPAN\_ATTRIBUTES to set the attribute name and value for a span when using trace events from a handler written in
Snowflake Scripting.

For more information, refer to [Emitting trace events in Snowflake Scripting](/developer-guide/logging-tracing/tracing-snowflake-scripting).

## Syntax

Copy code

```
SYSTEM$SET_SPAN_ATTRIBUTES('<object>');
```

## Arguments

`'object'`
:   An object containing name-value pairs representing the attributes to add.

## Examples

Code in the following example uses the SYSTEM$ADD\_EVENT function to add an event named `name_a` and an event named `name_b`.
With `name_b`, it associates two attributes, `score` and `pass`. The code also uses SYSTEM$SET\_SPAN\_ATTRIBUTES to
set two attributes for the span, `attr1` and `attr2`.

Copy code

```
create procedure MYPROC()
returns double
language sql
as
$$
begin
    -- Add an event without attributes
    SYSTEM$ADD_EVENT('name_a');

    -- Add an event with attributes
    let attr := {'score':89, 'pass':true};
    SYSTEM$ADD_EVENT('name_b', attr);

    -- Set attributes for the span
    SYSTEM$SET_SPAN_ATTRIBUTES('{'attr1':'value1', 'attr2':true}');

    return 3.14;
end;
$$
;
```

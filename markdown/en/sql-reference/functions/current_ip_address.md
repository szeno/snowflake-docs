Categories:
:   [Context functions](/sql-reference/functions-context)

# CURRENT\_IP\_ADDRESS

Returns the IPv4 address of the client that submitted the request.

This function returns the client’s IPv4 address only. If the client connects over IPv6, this function doesn’t return the
IPv6 address. To retrieve the client’s IPv6 address, use the `IP_ADDRESS_V6` session property with
[SYS\_CONTEXT](/sql-reference/functions/sys_context_snowflake_session):

Copy code

```
SELECT SYS_CONTEXT('SNOWFLAKE$SESSION', 'IP_ADDRESS_V6');
```

## Syntax

Copy code

```
CURRENT_IP_ADDRESS()
```

## Arguments

None.

## Examples

Return the current IP address of the client that is connected to Snowflake:

> Copy code
>
> ```
> select current_ip_address();
>
> +----------------------+
> | CURRENT_IP_ADDRESS() |
> +----------------------+
> | 192.0.2.255          |
> +----------------------+
> ```

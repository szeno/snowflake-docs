Categories:
:   [System functions](/sql-reference/functions-system) (System Control)

# SYSTEM$SNOWPIPE\_STREAMING\_UPDATE\_CHANNEL\_OFFSET\_TOKEN

Updates the offset token for a particular channel used by Snowpipe Streaming with a new offset token.

For more information about channels and offset tokens, see [Snowpipe Streaming](/user-guide/snowpipe-streaming/data-load-snowpipe-streaming-overview).

See also:

> [SHOW CHANNELS](/sql-reference/sql/show-channels)

## Syntax

Copy code

```
SYSTEM$SNOWPIPE_STREAMING_UPDATE_CHANNEL_OFFSET_TOKEN('<dbName>.<schemaName>.<tableName>', '<channelName>', '<new_offset_token>')
```

## Arguments

`dbName`
:   Name of the database in which the channel is stored.

`schemaName`
:   Name of the schema in which the channel is stored.

`tableName`
:   Name of the table where the channel is mapped to.

`channelName`
:   Name of the channel.

`new_offset_token`
:   The new offset token.

## Usage notes

- The role that executes this function must have at least the INSERT privilege on the table where the channel is mapped to.

## Examples

Updates the offset token for `mychannel` in `mydb.myschema.mytable` with a `<new_offset_token>`:

> Copy code
>
> ```
> show channels;
> select SYSTEM$SNOWPIPE_STREAMING_UPDATE_CHANNEL_OFFSET_TOKEN('mydb.myschema.mytable', 'mychannel', '<new_offset_token>');
> show channels;
> ```

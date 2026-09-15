# Consuming results

## Returning results inline

The most common way of consuming results is by passing a `complete` callback to `connection.execute()`. When the statement has finished executing and the result is ready to be consumed, the `complete`
callback is invoked with the result rows returned inline:

> Copy code
>
> ```
> connection.execute({
>   sqlText: 'SELECT * FROM sometable',
>   complete: (err, stmt, rows) => {
>     if (err) {
>       console.error(`Failed to execute statement due to the following error: ${err.message}`);
>     } else {
>       console.log(`Number of rows produced: ${rows.length}`);
>     }
>   }
> });
> ```

## Streaming results

You can also consume a result as a stream of rows by setting the `streamResult` connection parameter to `true`
in `connection.execute` when calling the `statement.streamRows()` method. Enabling this parameter causes
the method to return a Node.js `Readable` stream, which you can use to consume rows as they are received.

For more information about the `Readable` stream, refer to the [Node.js documentation](https://nodejs.org/dist/latest/docs/api/stream.html#stream_class_stream_readable).

Important

For any result set that might exceed Node’s default memory, Snowflake highly recommends that you set
`streamResult` to `true` when streaming results. With the default value (`false`), the connector
stores all of the rows in an array before streaming the results. With smaller result sets, this factor is
not normally an issue. However, with larger result sets, storing all the results in memory can contribute to an OOM error.

Recent versions of the Snowflake Node.js driver (1.6.23 and later) implement backpressure functionality to ensure that,
when consuming results,
data is not pushed to the stream faster than data is read from the stream.

For example, the following code fragment consumes the results using the `Readable` event:

> Copy code
>
> ```
> const connection = snowflake.createConnection({
>   account: process.env.SFACCOUNT,
>   username: process.env.SFUSER,
>   // ...
>   streamResult: true
> });
>
> // [..rest of the code..]
>
> connection.execute({
>   sqlText: 'select L_COMMENT from SNOWFLAKE_SAMPLE_DATA.TPCH_SF100.LINEITEM limit 100000;',
>   streamResult: true,
>   complete: function (err, stmt) {
>     const stream = stmt.streamRows();
>     // Read data from the stream when it is available
>     stream.on('readable', function (row) {
>       while ((row = this.read()) !== null) {
>         console.log(row);
>       }
>     }).on('end', () => {
>       console.log('done');
>     }).on('error', err => {
>       console.log(err);
>     });
>   }
> });
> ```

## Batch processing results

By default, the `statement.streamRows()` method produces a stream that includes every row in the result. However, if you only want to consume a subset of the result, or if you want to consume result rows
in batches, you can call `streamRows()` with `start` and `end` arguments. When these additional options are specified, only rows in the requested range are streamed:

> Copy code
>
> ```
> connection.execute({
>   sqlText: 'SELECT * FROM sometable',
>   streamResult: true, // prevent rows from being returned inline in the complete callback
>   complete: function (err, stmt, rows) {
>     // no rows returned inline because streamResult was set to true
>     console.log(`rows: ${rows}`); // 'rows: undefined'
>
>     // only consume at most the last 5 rows in the result
>     rows = [];
>     stmt.streamRows({
>       start: Math.max(0, stmt.getNumRows() - 5),
>       end: stmt.getNumRows() - 1
>     })
>     .on('error', err => {
>       console.error('Unable to consume requested rows');
>     })
>     .on('data', row => {
>       rows.push(row);
>     })
>     .on('end', () => {
>       console.log(`Number of rows consumed: ${rows.length}`);
>     });
>   }
> });
> ```

## Data type casting

When result rows are produced, the driver automatically maps SQL data types to their corresponding JavaScript equivalents. For example, values of type TIMESTAMP and DATE are returned as JavaScript Date
objects.

For the full mapping of JavaScript to SQL data types, refer to the table below:

> | SQL Data Type | JavaScript Data Type | Notes |
> | --- | --- | --- |
> | VARCHAR, CHAR, CHARACTER, STRING, TEXT | String |  |
> | INT, INTEGER, BIGINT, SMALLINT | Number | This is the default mapping. Use the session parameter JS\_TREAT\_INTEGER\_AS\_BIGINT to map to JavaScript Bigint. |
> | NUMBER(precision, scale), DECIMAL(p, s), NUMERIC(p, s) where `scale` = 0 | Number | This is the default mapping. Use the session parameter JS\_TREAT\_INTEGER\_AS\_BIGINT to map to JavaScript Bigint. |
> | NUMBER(precision, scale), DECIMAL(p, s), NUMERIC(p, s) where `scale` > 0 | Number |  |
> | FLOAT, FLOAT4, FLOAT8, DOUBLE, DOUBLE PRECISION, REAL | Number |  |
> | DECFLOAT | String | A string in scientific notation format, such as 9.8765432099999998623226732747455716901e-250  JavaScript does not natively support high-precision decimal numbers. Use libraries like [BigNumber.js](https://github.com/MikeMcl/bignumber.js) or [Decimal.js](https://github.com/MikeMcl/decimal.js) to perform accurate arithmetic operations on these values. |
> | TIMESTAMP, TIMESTAMP\_LTZ, TIMESTAMP\_NTZ, TIMESTAMP\_TZ | Date | TIMESTAMP\_NTZ values are returned in UTC. |
> | DATE | Date |  |
> | TIME | String | The TIME data type in SQL has no equivalent in JavaScript, so it is mapped to a JavaScript string. |
> | BOOLEAN | Boolean |  |
> | VARIANT, ARRAY, OBJECT | JSON |  |
>
> Expand
>
> Show lessSee more

## Fetching integer data types as Bigint

By default, Snowflake INTEGER columns (including `BIGINT`, `NUMBER(p, 0)`, etc.) are converted to JavaScript’s `Number` data type.
However, the largest legal Snowflake integer values are larger than the largest legal JavaScript Number values. To convert Snowflake `INTEGER`
columns to JavaScript `Bigint`, which can store larger values than JavaScript `Number`, set the session parameter `JS_TREAT_INTEGER_AS_BIGINT`.

You can use the following methods to set these parameter values:

- Use the ALTER SESSION statement, as shown below:

  Copy code

  ```
  connection.execute({
    sqlText: 'ALTER SESSION SET JS_TREAT_INTEGER_AS_BIGINT = TRUE',
    complete: function ...
  });
  ```
- Specify the parameter in the connection configuration information:

  Copy code

  ```
  const connection = snowflake.createConnection({
    username: 'fakeusername',
    password: 'fakepassword',
    account: 'fakeaccountidentifier',
    jsTreatIntegerAsBigInt: true
  });
  ```

## Fetching data types as strings

When calling `connection.execute()`, you can use the `fetchAsString` option to return the following
data types as strings: `Boolean`, `Number`, `Date`, `Buffer`, and `JSON`.

You can use this option, for example, to return:

- Formatted versions of values of type DATE and TIMESTAMP (or its variants).
- String versions of numerical SQL types that can’t be converted to JavaScript numbers without loss in precision.

The following example uses `fetchAsString` to convert a high-precision `Number` value to a string.:

Copy code

```
connection.execute({
  sqlText: 'SELECT 1.123456789123456789123456789 as "c1"',
  fetchAsString: ['Number'],
  complete: (err, stmt, rows) => {
    if (err) {
      console.error(`Failed to execute statement due to the following error: ${err.message}`);
    } else {
      console.log(`c1: ${rows[0].c1}`); // c1: 1.123456789123456789123456789
    }
  }
});
```

## Parsing XML data

Beginning with version 1.7.0 of the driver, you can use the following `fast-xml-parser`
library configuration options to customize how the driver processes XML document attributes when querying columns
with XML content. For more information about these supported options and how they affect XML data parsing,
see [xmlParserConfig options](/developer-guide/node-js/nodejs-driver-options#label-nodejs-xml-parser-options).

You can download the [fast-xml-parser](https://www.npmjs.com/package/fast-xml-parser).

By default, the Node.js driver ignores XML element attributes when returning XML data from a query. For example,
in the following XML content, the `<piece>` element includes an `id` attribute:

Copy code

```
<exhibit name="Art Show">
  <piece id="000001">
    <name>Mona Lisa</name>
    <artist>Leonardo da Vinci</artist>
    <year>1503</year>
  </piece>
  <piece id="000002">
    <name>The Starry Night</name>
    <artist>Vincent van Gogh</artist>
    <year>1889</year>
  </piece>
</exhibit>
```

By default, when the Node.js driver returns the result set, it ignores the `id` attribute and returns the following
output. Notice the attribute names and values are not included.

```
{
  exhibit: {
    piece: [
      {
        "name": "Mona Lisa",
        "artist": "Leonardo da Vinci",
        "year": "1503",
      },
      {
        "name": "The Starry Night",
        "artist": "Vincent van Gogh",
        "year": "1889",
      }
    ]
  }
}
```

To set the `fast-xml-parser` options, create an `xmlParserConfig`
element similar to the following example:

> Copy code
>
> ```
> import snowflake from 'snowflake-sdk';
>
> snowflake.configure({
>   xmlParserConfig: {
>     /*  Parameters that you can override
>     *   ignoreAttributes - default true,
>     *   attributeNamePrefix - default '@_',
>     *   attributesGroupName - default unset,
>     *   alwaysCreateTextNode - default false
>     */
>     ignoreAttributes: false, attributesGroupName: '@', attributeNamePrefix: ''
>   }
> });
> ```

With these settings, the driver parses the XML data and produces the following:

```
{
  exhibit: {
    piece: [
      {
        "name": "Mona Lisa",
        "artist": "Leonardo da Vinci",
        "year": "1503",
        '@': { id: '000001' }
      },
      {
        "name": "The Starry Night",
        "artist": "Vincent van Gogh",
        "year": "1889",
        '@': { id: '000002' }
      }
    ],
    '@': { name: 'Art Show' }
  }
```

## Returning result sets that contain duplicate column names

In version 1.8.0, the Snowflake Node.js Driver introduced a new [rowMode](/developer-guide/node-js/nodejs-driver-options#label-nodejs-rowmode) configuration option
that lets you specify how you want the driver to return result sets that contain duplicate column names.

Prior to version 1.8.0, the Snowflake Node.js Driver always returned the result set from a SELECT command as a JavaScript
object. In cases where the result set contained duplicate column names and values, some elements could be omitted due to the way
JavaScript objects handle duplicate names.

The `rowMode` option lets you specify how result set data is returned to avoid potential loss of information, including as:

- `array`
- `object` (default)
- `object_with_renamed_duplicated_columns`

To illustrate, assume you submit the following query:

Copy code

```
select *
from (select 'a' as key, 1 as foo, 3 as name) as table1
join (select 'a' as key, 2 as foo, 3 as name2) as table2 on table1.key = table2.key
join (select 'a' as key, 3 as foo) as table3 on table1.key = table3.key
```

Based on the value of `rowMode`, the driver returns the result sets as follows:

- `object` (or unset)

  ```
  {KEY: 'a', FOO: 3, NAME: 3, NAME2: 3};
  ```
- `array`

  ```
  ['a', 1, 3, 'a', 2, 3, 'a', 3];
  ```
- `object_with_renamed_duplicated_columns`

  ```
  {KEY: 'a', FOO: 1, NAME: 3, KEY_2: 'a', FOO_2: 2, NAME2: 3, KEY_3: 'a', FOO_3: 3};
  ```

You can set the `rowMode` parameter in the connection or statement configuration level, as shown below. If set in
both places, the statement level value takes precedence.

- Configuration level

  Copy code

  ```
  snowflake.createConnection({
    account: account,
    username: username,
    // ...
    rowMode: 'array'
  });
  ```
- Statement level

  Copy code

  ```
  connection.execute({
    sqlText: sql,
    rowMode: 'array',
    // ...
  });
  ```

## Customizing how result sets process JSON and XML data

The Snowflake Node.js driver provides the following default parsers for processing JSON and XML data in result sets:

- JSON: Returns the result from a new `Function` object.
- XML: `fast-xml-parser`.

  The default `fast-xml-parser` module supports a subset of features, as described in [Parsing XML data](#label-parsing-xml-data).

  You can download [fast-xml-parser](https://www.npmjs.com/package/fast-xml-parser).

If you prefer to use a custom parser, you can use the following examples to configure them:

- Use the eval JSON parser, which the driver used prior to version 1.6.21:

  Copy code

  ```
  import snowflake from 'snowflake-sdk';

  snowflake.configure({
    jsonColumnVariantParser: rawColumnValue => JSON.parse(rawColumnValue)
  });
  ```
- Use the `fast-xml-parser` parser, with the ability to [customize all of its options](https://github.com/NaturalIntelligence/fast-xml-parser/blob/master/docs/v4/2.XMLparseOptions.md):

  Copy code

  ```
  import snowflake from 'snowflake-sdk';
  import { XMLParser } from 'fast-xml-parser';

  snowflake.configure({
    xmlColumnVariantParser: rawColumnValue => new XMLParser().parse(rawColumnValue)
  });
  ```
- Configure custom parsers for both in the same declaration:

  Copy code

  ```
  import snowflake from 'snowflake-sdk';
  import { XMLParser } from 'fast-xml-parser';

  snowflake.configure({
    jsonColumnVariantParser: rawColumnValue => JSON.parse(rawColumnValue),
    xmlColumnVariantParser: rawColumnValue => new XMLParser().parse(rawColumnValue)
  });
  ```

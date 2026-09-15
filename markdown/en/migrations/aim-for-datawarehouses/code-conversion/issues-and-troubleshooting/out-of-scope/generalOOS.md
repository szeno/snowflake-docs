# Code Conversion - Out of Scope

## SSC-OOS-0001

The file has an unexpected encoding and was not translated

### Description

This error occurs when the tool cannot recognize the character encoding format of a source code file. Character encoding is a method of converting text characters into numerical values that computers can process. When the tool encounters characters it cannot interpret, it generates this error.

### Best Practices

- Ensure all files in the input folder use the same character encoding to prevent encoding-related errors.
- Choose the correct encoding using either the conversion settings or by specifying the –encoding parameter in the [SnowConvert AI CLI](/migrations/aim-for-datawarehouses/manual-migration/README). You can identify the correct encoding using tools like [Free Online Formatter](https://freeonlineformatter.com/encoding-string), or by running `file -i *` on Linux or macOS.
- For additional assistance, contact us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

## SSC-OOS

Out of scope code unit.

#### Description

This issue is generated when SnowConvert AI encounters a top-level statement or code unit that is outside the translation scope. The marker identifies the unsupported construct, and the source statement is commented out.

#### Code Example

##### Input Code:

##### SQL Server

Copy code

```
GRANT EXECUTE ON TestMe TO User2;
```

##### Output Code:

##### Snowflake

Copy code

```
----** SSC-OOS - OUT OF SCOPE CODE UNIT. GRANT STATEMENT IS OUT OF TRANSLATION SCOPE. **
--GRANT EXECUTE ON TestMe TO User2
```

#### Best Practices

- Review the commented-out statement and determine whether it is required in Snowflake.
- Implement required behavior manually with an appropriate Snowflake-native construct.
- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

# Code Conversion - Vertica Functional Differences

Note

**Conversion Scope**

For Vertica, the assessment and translation capabilities primarily focus on TABLES and VIEWS.
While other types of ANSI-standard statements are recognized, they are not yet fully supported for conversion. The tool may identify them, but will not perform a complete translation for these unsupported code units.

## SSC-FDM-VT0001

Expression in USING constraint might not be supported in Snowflake.

### Description

In Vertica, the `DEFAULT USING` clause offers a deferred refresh capability, which Snowflake doesn’t support. While Snowflake can apply the expression as a simple `DEFAULT` value when new rows are inserted, it won’t replicate Vertica’s deferred refresh logic.

Additionally, the expression itself might contain Vertica-specific functions or syntax that are incompatible with Snowflake. Because of these differences, a warning is added to your converted code. This highlights both the change in refresh behavior and the necessity to manually review the translated expression to ensure its syntax is compatible with Snowflake.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE table1 (
    base_value INT,
    derived_value INT DEFAULT USING (base_value + 100)
);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE TABLE table1 (
    base_value INT,
    derived_value INT DEFAULT (base_value + 100) /*** SSC-FDM-VT0001 - EXPRESSION IN USING CONSTRAINT MIGHT NOT BE SUPPORTED IN SNOWFLAKE ***/
)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "vertica",  "convertedOn": "06/17/2025",  "domain": "no-domain-provided" }}';
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

# Code Conversion - Greenplum Functional Differences

Note

**Conversion Scope**

For Greenplum, the assessment and translation capabilities primarily focus on TABLES and VIEWS.
While other types of ANSI-standard statements are recognized, they are not yet fully supported for conversion. The tool may identify them, but will not perform a complete translation for these unsupported code units.

## SSC-FDM-GP0001

The performance of the CLUSTER BY may vary compared to the performance of Distributed By

### Description

The `DISTRIBUTED BY` in Greenplum is analogous to `CLUSTER BY` in Snowflake. However, performance implications may vary due to architectural differences between Greenplum and Snowflake.

- **`DISTRIBUTED BY`** controls the physical distribution of data across the nodes (segments) in Greenplum’s MPP architecture..
- **`CLUSTER BY`** in Snowflake organizes data into blocks based on designated columns, aiding in filtering and aggregation tasks.

Understanding these mechanisms is crucial for optimizing performance in each respective platform.

#### Code Example

##### Input Code:

##### Redshift

Copy code

```
 CREATE TABLE table1 (colum1 int, colum2 int, colum3 smallint, colum4 int )
DISTRIBUTED BY (colum1, colum2);
```

##### Generated Code:

##### Snowflake

Copy code

```
 CREATE TABLE table1 (colum1 int, colum2 int, colum3 smallint, colum4 int )
--** SSC-FDM-GP0001 - THE PERFORMANCE OF THE CLUSTER BY MAY VARY COMPARED TO THE PERFORMANCE OF DISTRIBUTED BY **
CLUSTER BY (colum1, colum2)
COMMENT = '{ "origin": "sf_sc", "name": "snowconvert", "version": {  "major": 0,  "minor": 0,  "patch": "0" }, "attributes": {  "component": "greenplum",  "convertedOn": "03/26/2025",  "domain": "test" }}'
;
```

#### Best Practices

- If you need more support, you can email us at [aim-support@snowflake.com](mailto:aim-support@snowflake.com)

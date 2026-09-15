# Oracle - Spatial Types

## Description

> Oracle Spatial and Graph is designed to make spatial data management easier and more natural to users of location-enabled applications, geographic information system (GIS) applications, and geoimaging applications. ([Oracle SQL Language Reference Spatial Types](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-B4DF3B59-1600-4FA2-B7ED-AF7B734256BF))

Copy code

```
{ SDO_Geometry | SDO_Topo_Geometry |SDO_GeoRaster }
```

## SDO\_GEOMETRY

Note

Some parts in the output code are omitted for clarity reasons.

### Description

> The geometric description of a spatial object is stored in a single row, in a single column of object type SDO\_GEOMETRY in a user-defined table. Any table that has a column of type SDO\_GEOMETRY must have another column, or set of columns, that defines a unique primary key for that table. ([Oracle SQL Language Reference SDO\_GEOMETRY Data Type](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-022A5008-1E15-4AA4-938E-7FD75C594087))

Definition of SDO\_GEOMETRY object:

Copy code

```
CREATE TYPE SDO_GEOMETRY AS OBJECT
  (sgo_gtype        NUMBER,
   sdo_srid         NUMBER,
   sdo_point        SDO_POINT_TYPE,
   sdo_elem_info    SDO_ELEM_INFO_ARRAY,
   sdo_ordinates    SDO_ORDINATE_ARRAY);
/
```

The `SDO_GEOMETRY` object is **not supported** in Snowflake. A workaround for this data type is to use [Snowflake GEOGRAPHY](https://docs.snowflake.com/en/sql-reference/data-types-geospatial.html), however that transformation is currently not supported.

### Sample Source Patterns

#### SDO\_GEOMETRY in Create Table

##### Oracle

Copy code

```
CREATE TABLE geometry_table(
    geometry_column SDO_GEOMETRY
);
```

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE geometry_table (
        geometry_column GEOMETRY
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
    ;
```

#### Inserting data in SDO\_GEOMETRY Table

##### Oracle

Copy code

```
INSERT INTO geometry_table VALUES (
	SDO_GEOMETRY('POINT(-79 37)')
);

INSERT INTO geometry_table VALUES (
    SDO_GEOMETRY('LINESTRING(1 3, 1 5, 2 7)')
);

INSERT INTO geometry_table VALUES (
    MDSYS.SDO_GEOMETRY(
		2001,
		8307,
		MDSYS.SDO_POINT_TYPE (
			-86.13631,
			40.485424,
			NULL),
		NULL,
		NULL
	)
);

INSERT  INTO geometry_table VALUES (
SDO_GEOMETRY(
    2003,
    12,
    SDO_POINT_TYPE(12, 14, -5),
    SDO_ELEM_INFO_ARRAY(1,1003,3),
    SDO_ORDINATE_ARRAY(1,1, 5,7)
  )
);

INSERT INTO geometry_table VALUES (
NULL);
```

##### Snowflake

Copy code

```
INSERT INTO geometry_table
VALUES (
	SDO_GEOMETRY('POINT(-79 37)') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'SDO_GEOMETRY' NODE ***/!!!
);

INSERT INTO geometry_table
VALUES (
    SDO_GEOMETRY('LINESTRING(1 3, 1 5, 2 7)') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'SDO_GEOMETRY' NODE ***/!!!
);

INSERT INTO geometry_table
VALUES (
    MDSYS.SDO_GEOMETRY(
		2001,
		8307,
		MDSYS.SDO_POINT_TYPE (
			-86.13631,
			40.485424,
			NULL) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'MDSYS.SDO_POINT_TYPE' NODE ***/!!!,
		NULL,
		NULL
	) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'MDSYS.SDO_GEOMETRY' NODE ***/!!!
);

INSERT  INTO geometry_table
VALUES (
SDO_GEOMETRY(
    2003,
    12,
    SDO_POINT_TYPE(12, 14, -5) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'SDO_POINT_TYPE' NODE ***/!!!,
    SDO_ELEM_INFO_ARRAY(1,1003,3) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'SDO_ELEM_INFO_ARRAY' NODE ***/!!!,
    SDO_ORDINATE_ARRAY(1,1, 5,7) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'SDO_ORDINATE_ARRAY' NODE ***/!!!
  ) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'SDO_GEOMETRY' NODE ***/!!!
);

INSERT INTO geometry_table
VALUES (
NULL);
```

#### Migration using the GEOGRAPHY data type

##### Oracle

Copy code

```
CREATE TABLE geometry_table(
    geometry_column SDO_GEOMETRY
);

INSERT INTO geometry_table VALUES (
	SDO_GEOMETRY('POINT(-79 37)')
);

INSERT INTO geometry_table VALUES (
    SDO_GEOMETRY('LINESTRING(1 3, 1 5, 2 7)')
);

/*
--NOT SUPPORTED BY SNOWFLAKE GEOGRAPHY
INSERT INTO geometry_table VALUES (
    MDSYS.SDO_GEOMETRY(
		2001,
		8307,
		MDSYS.SDO_POINT_TYPE (
			-86.13631,
			40.485424,
			NULL),
		NULL,
		NULL
	)
);
INSERT  INTO geometry_table VALUES (
SDO_GEOMETRY(
    2003,
    12,
    SDO_POINT_TYPE(12, 14, -5),
    SDO_ELEM_INFO_ARRAY(1,1003,3),
    SDO_ORDINATE_ARRAY(1,1, 5,7)
  )
);
*/

SELECT * FROM geometry_table;
```

##### Result

| GEOMETRY\_COLUMN |
| -------------------------------------------------------- | ----------------------------- |
| [2001, null, [-79, 37, null], [NULL], [NULL]] | –(POINT(-79,37)) |
| [2002, null, [null, null, null], [1,2,1], [1,3,1,5,2,7]] | –(LINESTRING(1 3, 1 5, 2 7)) |

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE geometry_table (
	    geometry_column GEOMETRY
	)
	COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
	;

	INSERT INTO geometry_table
	VALUES (
	SDO_GEOMETRY('POINT(-79 37)') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'SDO_GEOMETRY' NODE ***/!!!
);

	INSERT INTO geometry_table
	VALUES (
    SDO_GEOMETRY('LINESTRING(1 3, 1 5, 2 7)') !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'SDO_GEOMETRY' NODE ***/!!!
);

	/*
--NOT SUPPORTED BY SNOWFLAKE GEOGRAPHY
INSERT INTO geometry_table VALUES (
    MDSYS.SDO_GEOMETRY(
		2001,
		8307,
		MDSYS.SDO_POINT_TYPE (
			-86.13631,
			40.485424,
			NULL),
		NULL,
		NULL
	)
);
INSERT  INTO geometry_table VALUES (
SDO_GEOMETRY(
    2003,
    12,
    SDO_POINT_TYPE(12, 14, -5),
    SDO_ELEM_INFO_ARRAY(1,1003,3),
    SDO_ORDINATE_ARRAY(1,1, 5,7)
  )
);
*/

SELECT * FROM
	    geometry_table;
```

##### Result

| GEOMETRY\_COLUMN |
| --- |
| POINT(-79 37) |
| LINESTRING(1 3,1 5,2 7) |

Expand

Show lessSee more

### Related EWIs

1. [SSC-EWI-0073](../../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073): Pending Functional Equivalence Review.

## SDO\_GEORASTER

Note

Some parts in the output code are omitted for clarity reasons.

### Description

> In the GeoRaster object-relational model, a raster grid or image object is stored in a single row, in a single column of object type `SDO_GEORASTER` in a user-defined table. ([Oracle SQL Language Reference SDO\_GEORASTER Data Type](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-CFEFCFAC-4756-4B90-B88D-D89B861C1628)).

Definition of SDO\_GEORASTER object:

Copy code

```
CREATE TYPE SDO_GEORASTER AS OBJECT
  (rasterType         NUMBER,
   spatialExtent      SDO_GEOMETRY,
   rasterDataTable    VARCHAR2(32),
   rasterID           NUMBER,
   metadata           XMLType);
/
```

Note

SDO\_GEORASTER is disabled by default, to enable its usage, follow the steps described in [this section](https://docs.oracle.com/database/121/SPATL/ensuring-that-georaster-works-properly-installation-or-upgrade.htm#GUID-20119C51-6B07-4535-954E-7C55850F51F3) of Oracle documentation.

The `SDO_GEORASTER` object is **not supported** in Snowflake.

### Sample Source Patterns

#### SDO\_GEORASTER in Create Table

##### Oracle

Copy code

```
CREATE TABLE georaster_table(
    georaster_column SDO_GEORASTER
);
```

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE georaster_table (
    !!!RESOLVE EWI!!! /*** SSC-EWI-0028 - TYPE NOT SUPPORTED BY SNOWFLAKE ***/!!!
        georaster_column SDO_GEORASTER
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},"attributes":{"component":"oracle"}}'
    ;
```

##### Inserting data in SDO\_GEORASTER Table

##### Oracle

Copy code

```
INSERT INTO georaster_table VALUES (null);
INSERT INTO georaster_table VALUES (sdo_geor.init('RDT_11', 1));
```

##### Snowflake

Copy code

```
INSERT INTO georaster_table
VALUES (null);

INSERT INTO georaster_table
VALUES (
!!!RESOLVE EWI!!! /*** SSC-EWI-OR0076 - TRANSLATION FOR BUILT-IN PACKAGE 'sdo_geor.init' IS NOT CURRENTLY SUPPORTED. ***/!!!
'' AS init);
```

### Known Issues

**1. SDO\_GEORASTER Data Type not transformed**

SDO\_GEORASTER Data Type is not being transformed.

### Related EWIs

1. [SSC-EWI-0028](../../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0028): Type not supported.
2. [SSC-EWI-OR0076:](../../../../issues-and-troubleshooting/conversion-issues/oracleEWI#ssc-ewi-or0076) Built In Package Not Supported.

## SDO\_TOPO\_GEOMETRY

Note

Some parts in the output code are omitted for clarity reasons.

### Description

> This type describes a topology geometry, which is stored in a single row, in a single column of object type `SDO_TOPO_GEOMETRY` in a user-defined table. ([Oracle SQL Language Reference SDO\_TOPO\_GEOMETRY Data Type](https://docs.oracle.com/en/database/oracle/oracle-database/21/sqlrf/Data-Types.html#GUID-66AF10E5-137D-444B-B9BC-89B2B340E278)).

Definition of SDO\_TOPO\_GEOMETRY object:

Copy code

```
CREATE TYPE SDO_TOPO_GEOMETRY AS OBJECT
  (tg_type        NUMBER,
   tg_id          NUMBER,
   tg_layer_id    NUMBER,
   topology_id    NUMBER);
/
```

The `SDO_TOPO_GEOMETRY` object is **not supported** in Snowflake.

### Sample Source Patterns

#### SDO\_TOPO\_GEOMETRY in Create Table

##### Oracle

Copy code

```
CREATE TABLE topo_geometry_table(
    topo_geometry_column SDO_TOPO_GEOMETRY
);
```

##### Snowflake

Copy code

```
CREATE OR REPLACE TABLE topo_geometry_table (
    !!!RESOLVE EWI!!! /*** SSC-EWI-0028 - TYPE NOT SUPPORTED BY SNOWFLAKE ***/!!!
        topo_geometry_column SDO_TOPO_GEOMETRY
    )
    COMMENT = '{"origin":"sf_sc","name":"snowconvert","version":{"major":1, "minor":0},{"attributes":{"component":"oracle"}}'
    ;
```

#### Inserting data in SDO\_TOPO\_GEOMETRY Table

##### Oracle

Copy code

```
INSERT INTO topo_geometry_table VALUES (SDO_TOPO_GEOMETRY(1,2,3,4));
INSERT INTO topo_geometry_table VALUES (NULL);
```

##### Snowflake

Copy code

```
INSERT INTO topo_geometry_table
VALUES (SDO_TOPO_GEOMETRY(1,2,3,4) !!!RESOLVE EWI!!! /*** SSC-EWI-0073 - PENDING FUNCTIONAL EQUIVALENCE REVIEW FOR 'SDO_TOPO_GEOMETRY' NODE ***/!!!);

INSERT INTO topo_geometry_table
VALUES (NULL);
```

### Known Issues

**1. SDO\_TOPO\_GEOMETRY Data Type not transformed**

SDO\_TOPO\_GEOMETRY Data Type is not being transformed.

### Related EWIs

1. [SSC-EWI-0028](../../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0028): Type not supported.
2. [SSC-EWI-0073:](../../../../issues-and-troubleshooting/conversion-issues/generalEWI#ssc-ewi-0073) Pending functional equivalence review.

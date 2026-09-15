# Snowflake Postgres Extensions

Extensions allow for expanded functionality within Postgres, without requiring a new version of Postgres to be released.
Extensions can enable new functionality including data types and functions.

You can see a list of all available extensions by querying your database:

Copy code

```
SELECT * FROM pg_available_extensions
```

You can see all extensions that are already enabled by executing:

Copy code

```
SELECT * FROM pg_extension;
```

or `\dx` in psql.

Extensions are enabled by the admin user by running:

Copy code

```
CREATE EXTENSION extensionname;
```

## Procedural language - PL/PgSQL

While also a category of extension, procedural languages allow you to write custom functions to be executed within your database.
We currently support PL/PgSQL.

## Current catalog of extensions

| Extension | Type of extension | Summary | Command to create |
| --- | --- | --- | --- |
| Address Standardizer | Functions | Used to parse an address into constituent elements | `CREATE EXTENSION address_standardizer;` |
| Address Standardizer (US) | Functions | Data for standardizing US addresses | `CREATE EXTENSION address_standardizer_data_us;` |
| Amcheck | Functions | Functions for verifying relation integrity | `CREATE EXTENSION amcheck;` |
| Apache AGE | Functions | Graph database functionality with openCypher query support | `CREATE EXTENSION age;` |
| Apache Data Sketches | Functions | Approximate algorithms including distinct counting, quantiles, and frequent items | `CREATE EXTENSION datasketches;` |
| Audit | Functions | Audit user actions | `CREATE EXTENSION pgaudit;` |
| Auto explain | Logging | Automatically log execution plans of slow statements | [See auto\_explain](https://docs.crunchybridge.com/extensions-and-languages/auto_explain) |
| Auto Increment | Functions | Provides function for storing the next value of a sequence in an integer field | `CREATE EXTENSION autoinc;` |
| Bloom | Index types | Provides a bloom filter index type | `CREATE EXTENSION bloom;` |
| Btree GIN | Index types | Support for indexing common data types in GIN | `CREATE EXTENSION btree_gin;` |
| Btree GIST | Index types | Support for indexing common data types in GiST | `CREATE EXTENSION btree_gist;` |
| Buffer Cache | Views | Examine the shared buffer cache | `CREATE EXTENSION pg_buffercache;` |
| Case insensitive text | Data type | Case insensitive text data type | `CREATE EXTENSION citext;` |
| Cron | Functions | Create scheduled tasks | `CREATE EXTENSION pg_cron;` |
| Crypto | Functions | Functions for encrypting data inside columns | `CREATE EXTENSION pgcrypto;` |
| Cube | Data type | Data type for multi-dimensional cubes | `CREATE EXTENSION cube;` |
| DDL Extractor | Functions | DDL eXtractor functions | `CREATE EXTENSION ddlx;` |
| dict-int | Dictionaries | Full text search dictionary template for integers | `CREATE EXTENSION dict_int;` |
| dict-xsyn | Dictionaries | Full text search dictionary template for extended synonym processing | `CREATE EXTENSION dict_xsyn;` |
| Earth Distance | Functions | Functions that assist with computing the distance between points. | `CREATE EXTENSION earthdistance;` |
| Free Space Map | Functions | Examine the free space map (FSM) | `CREATE EXTENSION pg_freespacemap;` |
| Fuzzy String Match | Functions | Functions for comparing similarity between strings | `CREATE EXTENSION fuzzystrmatch;` |
| H3 | Functions | H3 bindings for Postgres | `CREATE EXTENSION h3;` |
| H3 PostGIS | Geospatial utilities | H3 bindings for PostGIS spatial types | `CREATE EXTENSION h3_postgis;` |
| Hint plan | Functions | Adjust PostgreSQL execution plans using “hints” in SQL comments ([more info](https://github.com/ossc-db/pg_hint_plan)) | `CREATE EXTENSION pg_hint_plan;` |
| HLL | Functions | HyperLogLog data structure for approximating distinct value counts | `CREATE EXTENSION hll;` |
| Hstore | Data type | Key value data type | `CREATE EXTENSION hstore;` |
| HTTP Client | Functions | HTTP client for PostgreSQL, allows web page retrieval inside the database. | `CREATE EXTENSION http;` |
| Hypopg | Functions | Hypothetical indexes | `CREATE EXTENSION hypopg;` |
| Incremental | Functions | Incremental batch processing | `CREATE EXTENSION pg_incremental;` |
| Insert Username | Functions | Will place the current Postgres username in a text field | `CREATE EXTENSION insert_username;` |
| Integer Aggregator | Functions | Integer aggregator and enumerator | `CREATE EXTENSION intagg;` |
| Integer Array | Functions | Sorting and manipulation of integer arrays | `CREATE EXTENSION intarray;` |
| ISN | Data type | Data type for product numbering (including UPC, ISBN, ISSN) | `CREATE EXTENSION isn;` |
| IVM | Functions | Incremental View Maintenance | `CREATE EXTENSION pg_ivm;` |
| Large Object | Data type | Specialized large object data type | `CREATE EXTENSION lo;` |
| Label Tree | Data type | Data type for tree-like structures | `CREATE EXTENSION ltree;` |
| Logical | Functions | Helper functions for PostgreSQL Logical Replication | `CREATE EXTENSION pglogical;` |
| Modification Time | Functions | Will place the current timestamp into a timestamp field | `CREATE EXTENSION moddatetime;` |
| Orafce | Functions | Emulate Oracle functions | `CREATE EXTENSION orafce;` |
| Page Inspect | Functions | Inspect the contents of database pages at a low level | `CREATE EXTENSION pageinspect;` |
| Row Locking | Functions | Show row-level locking information | `CREATE EXTENSION pgrowlocks;` |
| Partman | Functions | Create and manage both time-based and serial-based table partition sets | `CREATE EXTENSION pg_partman;` |
| pg\_lake | Iceberg and data lake storage | Support for tables backed by object storage formats like Iceberg, Parquet, and ORC | See [pg\_lake](/user-guide/snowflake-postgres/postgres-pg_lake) |
| PostGIS | Geospatial utilities | PostGIS geometry, geography, and raster spatial types and functions | [See PostGIS](https://docs.crunchybridge.com/extensions-and-languages/postgis) |
| PostGIS Raster | Geospatial utilities | PostGIS raster types and functions | `CREATE EXTENSION postgis_raster;` |
| PostGIS SFCGAL | Geospatial utilities | PostGIS SFCGAL functions | `CREATE EXTENSION postgis_sfcgal;` |
| PostGIS Topology | Geospatial utilities | PostGIS topology spatial types and functions | `CREATE EXTENSION postgis_topology;` |
| PostGIS Tiger Geocoder | Geospatial utilities | PostGIS tiger geocoder and reverse geocoder | `CREATE EXTENSION postgis_tiger_geocoder;` |
| Postgres FDW | Foreign Data Wrapper | Foreign data wrapper for connecting to other Postgres databases | `CREATE EXTENSION postgres_fdw;` |
| Prewarm | Functions | Utilities to prewarm your cache, helpful for standby failover | `CREATE EXTENSION pg_prewarm;` |
| Proctab | Functions | Access operating system process tables from PostgreSQL | `CREATE EXTENSION pg_proctab;` |
| Refint | Functions | Functions for referential integrity | `CREATE EXTENSION refint;` |
| Repack | Functions | Remove bloat from tables and indexes (See also pg\_squeeze) | `CREATE EXTENSION pg_repack;` |
| Routing | Geospatial utilities | Routing functionality | `CREATE EXTENSION pgrouting;` |
| Semver | Data type | Data type for the Semantic Version format with support for btree and hash indexing | `CREATE EXTENSION semver;` |
| Surgery | Functions | Corrective actions on corruption or damaged data | `CREATE EXTENSION pg_surgery;` |
| Seg | Data type | Data type for representing floating point intervals or segments | `CREATE EXTENSION seg;` |
| SSL Info | Functions | Ability to query SSL information based on the current connection | `CREATE EXTENSION sslinfo;` |
| Stat statements | Views | Track planning and execution statistics of all SQL statements executed | `CREATE EXTENSION pg_stat_statements;` |
| Stat Tuple | Functions | Show tuple-level statistics | `CREATE EXTENSION pgstattuple;` |
| Squeeze | Functions | Remove bloat from tables and indexes. A modern alternative to pg\_repack. See [pg\_squeeze docs](https://github.com/cybertec-postgresql/pg_squeeze). | `CREATE EXTENSION pg_squeeze;` |
| Table functions | Functions | Functions for cubing and rollups of tables | `CREATE EXTENSION tablefunc;` |
| Table sampling (system rows) | Functions | Functions to provide sampling of system tables | `CREATE EXTENSION tsm_system_rows;` |
| Table sampling (system time) | Functions | Functions to provide sampling of system time | `CREATE EXTENSION tsm_system_time;` |
| Trigger change notifications | Functions | Functions for listening to changes on tables | `CREATE EXTENSION tcn;` |
| Trigram | Functions | Matching and similarity of strings | `CREATE EXTENSION pg_trgm;` |
| Unaccent | Dictionaries | Text search dictionary that removes accents | `CREATE EXTENSION unaccent;` |
| Visibility | Functions | Examine the visibility map (VM) and page-level visibility info | `CREATE EXTENSION pg_visibility;` |
| Vector | Functions | Vector (pgvector) data type and ivfflat access method | `CREATE EXTENSION vector;` |
| ULID | Functions | Generate universally unique lexicographically sortable identifiers (ULIDs) | `CREATE EXTENSION pgx_ulid;` |
| uuid-ossp | Functions | Generate universally unique identifiers (UUIDs) | `CREATE EXTENSION uuid-ossp;` |
| uuidv7 | Functions | Generate version 7 universally unique identifiers (UUIDs) | `CREATE EXTENSION pg_uuidv7;` |
| WAL inspect | Functions | Inspect contents of WAL | `CREATE EXTENSION pg_walinspect;` |
| xml2 | Functions | XPath querying and XSLT | `CREATE EXTENSION xml2;` |

Expand

Show lessSee more

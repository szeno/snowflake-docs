# Jan 15, 2025: Optimized COPY and INSERT bulk loads on empty hybrid tables (*General availability*)

We are pleased to announce the general availability of extended support for optimized bulk loading into hybrid tables.

When a hybrid table is empty, COPY and INSERT INTO … SELECT commands benefit from optimized bulk loading, which is a
fast execution model for inserting data that previously applied only to CREATE HYBRID TABLE … AS SELECT loads.

For more information, see [Loading data](/user-guide/tables-hybrid-create#label-create-loading-data).

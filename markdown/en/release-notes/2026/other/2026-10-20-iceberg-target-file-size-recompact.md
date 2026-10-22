# October 20, 2026: Recompact Iceberg table data after target file size increases

When you increase `TARGET_FILE_SIZE` on a Snowflake-managed Iceberg table, data compaction recompacts older files that were written under the
smaller target and compacts new files using the larger setting. For example, if files were compacted at 16 MB and the new target file size is
128 MB, data compaction recompacts older files from 16 MB to 128 MB. For more information, see
[Set a target file size](/user-guide/tables-iceberg-manage#label-tables-iceberg-target-file-size).

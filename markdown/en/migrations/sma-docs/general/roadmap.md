description:
:   Release Notes for the Snowpark Migration Accelerator (SMA)

# Snowpark Migration Accelerator: Release Notes

Note that the release notes below are organized by release date. Version numbers for both the application and the conversion core will appear below.

## Version 3.4.0 (Apr 27, 2026)

### Application & CLI Version: 3.4.0

#### Included SMA Core Version

- Snowpark Conversion Core: 8.2.2

### Release Notes

#### Added

- Added support for `map_concat` with a new `SPRKPY1104` EWI raised when fewer than two arguments are provided.

#### Removed

- Removed the licensing/access-code requirement from the SMA CLI.

## Version 3.3.0 (Mar 30, 2026)

### Application & CLI Version: 3.3.0

#### Included SMA Core Version

- Snowpark Conversion Core: 8.1.88

### Engine Release Notes

#### Changed

- Included `FileName` column in the SnowConvert `Elements.csv` inventory.
- Updated Snowpark Scala library version from `1.17.0` to `1.18.0`, adding support for new overloads with `Any` parameter types on existing `Column` methods (`cast`, `equal_to`, `not_equal`, `gt`, `lt`, `leq`, `geq`, `equal_null`, `plus`, `minus`, `multiply`, `divide`, `mod`) and functions (`try_to_date`, `try_to_timestamp` with format parameter).
- `pyspark.sql.functions.array` with multiple arguments is now correctly mapped to `snowflake.snowpark.functions.array_construct` instead of `to_array`. Single-argument calls continue mapping to `to_array`.
- Session creation is now converted to the standard SCOS pattern.
  - For example, `session.server.init_spark_session()` → `session.init_spark_session()`

### Desktop Release Notes

#### Added

- **.config folder validation:** The SMA app now detects and reports issues related to the dedicated `.config` folder configuration.

## Version 3.2.0 (Mar 13, 2026)

### Application & CLI Version: 3.2.0

### Engine Release Notes

#### Changed

- Updated .NET version to `v10.0.0`.
- Bumped Python AST and Parser version to `v149.1.23`.
- The SMA now correctly identifies and reports usages of `org.apache.spark.sql.functions.to_number` and `org.apache.spark.sql.functions.try_to_number` as unsupported elements within the Snowpark API.

### Desktop Release Notes

#### Added

- **Output folder validation:** The output folder selection now validates for existing project files (`.snowct`). If the selected folder already contains a project, the selection is blocked and an error is displayed, preventing accidental overwrites.
- **Dual-assessment workflow:** Automatically evaluates both SCOS and Snowpark API conversion paths, recommending the best fit for the user’s workload.
- **Two conversion modes:** Snowpark Connect (SCOS) and Snowpark API are now available as distinct conversion targets.
- **Readiness score section:** Displays the recommended conversion target with a color-coded compatibility score badge.
- **File compatibility breakdown:** KPI cards showing fully compatible files, files requiring changes, and files with unsupported APIs.
- **Data distribution charts:** Stacked bar charts showing input data sources and output data targets, grouped by platform.
- **Code dependencies:** Interactive donut chart categorizing dependencies as Supported, Internal, or Unknown.
- **Issues by category:** AI-enriched table grouping conversion issues into human-readable categories with file counts and key issue summaries. Displayed when a Snowflake session is active.
- **Execution summary:** Project metadata, engine version information, and input/output folder references.
- **Performance:** Assessment report data is cached for the duration of the session, enabling instant page loads when navigating back to results.

#### Changed

- **Card layout improvements:** Assessment and conversion cards were refactored for improving the user experience.
- **Assessment workflow shortcut:** If an assessment has already been completed, clicking “Analyze code” navigates directly to the results page instead of re-running the assessment.
- **Renamed connection action:** “Activate Assistant” is now “Connect to Snowflake” across the application header and connection dialog for clearer terminology.

## Version 3.1.0 (Feb 27, 2026)

### Application & CLI Version: 3.1.0

#### Included SMA Core Version

- Snowpark Conversion Core: 8.1.60

#### Included SnowConvert AI Version

- SnowConvert AI Version 2.2.0 ([Release Notes](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/release-notes/release-notes/README#version-2-2-0-jan-07-2026))

### Engine Release Notes

#### Added

- Added support for processing files located in a hidden folder (such as `.databricks` when exported from the source). These files are now correctly processed by the SMA.
- Added 245 new PySpark elements to the SMA mapping table with a NotSupported status. These entries correspond to functions and methods introduced in PySpark 3.3.0 through 4.1.x:

  - 219 functions (`pyspark.sql.functions`)
  - 4 DataFrame methods
  - 3 Column methods
  - 5 Session methods
  - 2 ReadWriter methods
  - 12 Types classes
- Added new EWIs for the following Pandas elements:

  - PNDSPY1019: pandas.core.arrays.datetimelike.DatelikeOps.strftime partial support
  - PNDSPY1020: pandas.core.arrays.datetimelike.TimelikeOps.ceil partial support
  - PNDSPY1021: pandas.core.arrays.datetimelike.TimelikeOps.floor partial support
  - PNDSPY1022: pandas.core.arrays.datetimelike.TimelikeOps.round partial support
  - PNDSPY1023: pandas.core.arrays.datetimes.DatetimeArray.day\_name partial support
  - PNDSPY1024: pandas.core.arrays.datetimes.DatetimeArray.month\_name partial support
  - PNDSPY1025: pandas.core.arrays.datetimes.DatetimeArray.tz\_convert partial support
  - PNDSPY1026: pandas.core.arrays.datetimes.DatetimeArray.tz\_localize partial support
  - PNDSPY1027: pandas.core.base.IndexOpsMixin.argmax partial support
  - PNDSPY1028: pandas.core.base.IndexOpsMixin.argmin partial support
  - PNDSPY1029: pandas.core.base.IndexOpsMixin.value\_counts partial support
  - PNDSPY1030: pandas.core.frame.DataFrame.T partial support
  - PNDSPY1031: pandas.core.frame.DataFrame.**dataframe** partial support
  - PNDSPY1032: pandas.core.frame.DataFrame.add partial support
  - PNDSPY1033: pandas.core.frame.DataFrame.align partial support
  - PNDSPY1034: pandas.core.frame.DataFrame.all partial support
  - PNDSPY1035: pandas.core.frame.DataFrame.any partial support
  - PNDSPY1036: pandas.core.frame.DataFrame.applymap partial support
  - PNDSPY1037: pandas.core.frame.DataFrame.asfreq partial support
  - PNDSPY1038: pandas.core.frame.DataFrame.astype partial support
  - PNDSPY1039: pandas.core.frame.DataFrame.at partial support
  - PNDSPY1040: pandas.core.frame.DataFrame.backfill partial support
  - PNDSPY1041: pandas.core.frame.DataFrame.bfill partial support
  - PNDSPY1042: pandas.core.frame.DataFrame.compare partial support
  - PNDSPY1043: pandas.core.frame.DataFrame.corr partial support
  - PNDSPY1044: pandas.core.frame.DataFrame.cumsum partial support
  - PNDSPY1045: pandas.core.frame.DataFrame.div partial support
  - PNDSPY1046: pandas.core.frame.DataFrame.divide partial support
  - PNDSPY1047: pandas.core.frame.DataFrame.dropna partial support
  - PNDSPY1048: pandas.core.frame.DataFrame.eq partial support
  - PNDSPY1049: pandas.core.frame.DataFrame.eval partial support
  - PNDSPY1050: pandas.core.frame.DataFrame.expanding partial support
  - PNDSPY1051: pandas.core.frame.DataFrame.ffill partial support
  - PNDSPY1052: pandas.core.frame.DataFrame.fillna partial support
  - PNDSPY1053: pandas.core.frame.DataFrame.floordiv partial support
  - PNDSPY1054: pandas.core.frame.DataFrame.from\_records partial support
  - PNDSPY1055: pandas.core.frame.DataFrame.ge partial support
  - PNDSPY1056: pandas.core.frame.DataFrame.groupby partial support
  - PNDSPY1057: pandas.core.frame.DataFrame.gt partial support
  - PNDSPY1058: pandas.core.frame.DataFrame.idxmax partial support
  - PNDSPY1059: pandas.core.frame.DataFrame.idxmin partial support
  - PNDSPY1060: pandas.core.frame.DataFrame.info partial support
  - PNDSPY1061: pandas.core.frame.DataFrame.join partial support
  - PNDSPY1062: pandas.core.frame.DataFrame.le partial support
  - PNDSPY1063: pandas.core.frame.DataFrame.loc partial support
  - PNDSPY1064: pandas.core.frame.DataFrame.lt partial support
  - PNDSPY1065: pandas.core.frame.DataFrame.map partial support
  - PNDSPY1066: pandas.core.frame.DataFrame.mask partial support
  - PNDSPY1067: pandas.core.frame.DataFrame.melt partial support
  - PNDSPY1068: pandas.core.frame.DataFrame.merge partial support
  - PNDSPY1069: pandas.core.frame.DataFrame.mod partial support
  - PNDSPY1070: pandas.core.frame.DataFrame.mul partial support
  - PNDSPY1071: pandas.core.frame.DataFrame.multiply partial support
  - PNDSPY1072: pandas.core.frame.DataFrame.ne partial support
  - PNDSPY1073: pandas.core.frame.DataFrame.nlargest partial support
  - PNDSPY1074: pandas.core.frame.DataFrame.nsmallest partial support
  - PNDSPY1075: pandas.core.frame.DataFrame.nunique partial support
  - PNDSPY1076: pandas.core.frame.DataFrame.pad partial support
  - PNDSPY1077: pandas.core.frame.DataFrame.pct\_change partial support
  - PNDSPY1078: pandas.core.frame.DataFrame.pivot partial support
  - PNDSPY1079: pandas.core.frame.DataFrame.pivot\_table partial support
  - PNDSPY1080: pandas.core.frame.DataFrame.pow partial support
  - PNDSPY1081: pandas.core.frame.DataFrame.quantile partial support
  - PNDSPY1082: pandas.core.frame.DataFrame.radd partial support
  - PNDSPY1083: pandas.core.frame.DataFrame.rank partial support
  - PNDSPY1084: pandas.core.frame.DataFrame.rdiv partial support
  - PNDSPY1085: pandas.core.frame.DataFrame.reindex partial support
  - PNDSPY1086: pandas.core.frame.DataFrame.rename partial support
  - PNDSPY1087: pandas.core.frame.DataFrame.replace partial support
  - PNDSPY1088: pandas.core.frame.DataFrame.resample partial support
  - PNDSPY1089: pandas.core.frame.DataFrame.rfloordiv partial support
  - PNDSPY1090: pandas.core.frame.DataFrame.rmod partial support
  - PNDSPY1091: pandas.core.frame.DataFrame.rmul partial support
  - PNDSPY1092: pandas.core.frame.DataFrame.rolling partial support
  - PNDSPY1093: pandas.core.frame.DataFrame.round partial support
  - PNDSPY1094: pandas.core.frame.DataFrame.rpow partial support
  - PNDSPY1095: pandas.core.frame.DataFrame.rsub partial support
  - PNDSPY1096: pandas.core.frame.DataFrame.rtruediv partial support
  - PNDSPY1097: pandas.core.frame.DataFrame.sample partial support
  - PNDSPY1098: pandas.core.frame.DataFrame.shift partial support
  - PNDSPY1099: pandas.core.frame.DataFrame.skew partial support
  - PNDSPY1100: pandas.core.frame.DataFrame.sort\_index partial support
  - PNDSPY1101: pandas.core.frame.DataFrame.sort\_values partial support
  - PNDSPY1102: pandas.core.frame.DataFrame.stack partial support
  - PNDSPY1103: pandas.core.frame.DataFrame.std partial support
  - PNDSPY1104: pandas.core.frame.DataFrame.sub partial support
  - PNDSPY1105: pandas.core.frame.DataFrame.subtract partial support
  - PNDSPY1106: pandas.core.frame.DataFrame.to\_csv partial support
  - PNDSPY1107: pandas.core.frame.DataFrame.transform partial support
  - PNDSPY1108: pandas.core.frame.DataFrame.transpose partial support
  - PNDSPY1109: pandas.core.frame.DataFrame.truediv partial support
  - PNDSPY1110: pandas.core.frame.DataFrame.tz\_convert partial support
  - PNDSPY1111: pandas.core.frame.DataFrame.tz\_localize partial support
  - PNDSPY1112: pandas.core.frame.DataFrame.unstack partial support
  - PNDSPY1113: pandas.core.frame.DataFrame.var partial support
  - PNDSPY1114: pandas.core.frame.DataFrame.where partial support
  - PNDSPY1115: pandas.core.generic.NDFrame.shift partial support
  - PNDSPY1116: pandas.core.groupby.generic.DataFrameGroupBy.agg partial support
  - PNDSPY1117: pandas.core.groupby.generic.DataFrameGroupBy.aggregate partial support
  - PNDSPY1118: pandas.core.groupby.generic.DataFrameGroupBy.fillna partial support
  - PNDSPY1119: pandas.core.groupby.generic.DataFrameGroupBy.idxmax partial support
  - PNDSPY1120: pandas.core.groupby.generic.DataFrameGroupBy.idxmin partial support
  - PNDSPY1121: pandas.core.groupby.generic.DataFrameGroupBy.transform partial support
  - PNDSPY1122: pandas.core.groupby.generic.DataFrameGroupBy.value\_counts partial support
  - PNDSPY1123: pandas.core.groupby.groupby.BaseGroupBy.get\_group partial support
  - PNDSPY1124: pandas.core.groupby.groupby.GroupBy.all partial support
  - PNDSPY1125: pandas.core.groupby.groupby.GroupBy.any partial support
  - PNDSPY1126: pandas.core.groupby.groupby.GroupBy.apply partial support
  - PNDSPY1127: pandas.core.groupby.groupby.GroupBy.bfill partial support
  - PNDSPY1128: pandas.core.groupby.groupby.GroupBy.ffill partial support
  - PNDSPY1129: pandas.core.groupby.groupby.GroupBy.first partial support
  - PNDSPY1130: pandas.core.groupby.groupby.GroupBy.last partial support
  - PNDSPY1131: pandas.core.groupby.groupby.GroupBy.pct\_change partial support
  - PNDSPY1132: pandas.core.groupby.groupby.GroupBy.quantile partial support
  - PNDSPY1133: pandas.core.groupby.groupby.GroupBy.resample partial support
  - PNDSPY1134: pandas.core.groupby.groupby.GroupBy.rolling partial support
  - PNDSPY1135: pandas.core.groupby.groupby.GroupBy.shift partial support
  - PNDSPY1136: pandas.core.groupby.groupby.GroupBy.std partial support
  - PNDSPY1137: pandas.core.groupby.groupby.GroupBy.var partial support
  - PNDSPY1138: pandas.core.indexes.base.Index.all partial support
  - PNDSPY1139: pandas.core.indexes.base.Index.any partial support
  - PNDSPY1140: pandas.core.indexes.base.Index.nlevels partial support
  - PNDSPY1141: pandas.core.indexes.base.Index.reindex partial support
  - PNDSPY1142: pandas.core.indexes.base.Index.sort\_values partial support
  - PNDSPY1143: pandas.core.indexes.datetimes.DatetimeIndex.ceil partial support
  - PNDSPY1144: pandas.core.indexes.datetimes.DatetimeIndex.day\_name partial support
  - PNDSPY1145: pandas.core.indexes.datetimes.DatetimeIndex.floor partial support
  - PNDSPY1146: pandas.core.indexes.datetimes.DatetimeIndex.month\_name partial support
  - PNDSPY1147: pandas.core.indexes.datetimes.DatetimeIndex.round partial support
  - PNDSPY1148: pandas.core.indexes.datetimes.DatetimeIndex.std partial support
  - PNDSPY1149: pandas.core.indexes.datetimes.DatetimeIndex.tz\_convert partial support
  - PNDSPY1150: pandas.core.indexes.datetimes.DatetimeIndex.tz\_localize partial support
  - PNDSPY1151: pandas.core.indexes.datetimes.bdate\_range partial support
  - PNDSPY1152: pandas.core.indexes.datetimes.date\_range partial support
  - PNDSPY1153: pandas.core.resample.Resampler.asfreq partial support
  - PNDSPY1154: pandas.core.resample.Resampler.bfill partial support
  - PNDSPY1155: pandas.core.resample.Resampler.ffill partial support
  - PNDSPY1156: pandas.core.resample.Resampler.fillna partial support
  - PNDSPY1157: pandas.core.resample.Resampler.first partial support
  - PNDSPY1158: pandas.core.resample.Resampler.last partial support
  - PNDSPY1159: pandas.core.resample.Resampler.quantile partial support
  - PNDSPY1160: pandas.core.resample.Resampler.std partial support
  - PNDSPY1161: pandas.core.resample.Resampler.var partial support
  - PNDSPY1162: pandas.core.reshape.concat.concat partial support
  - PNDSPY1163: pandas.core.reshape.melt.melt partial support
  - PNDSPY1164: pandas.core.reshape.merge.merge partial support
  - PNDSPY1165: pandas.core.reshape.merge.merge\_asof partial support
  - PNDSPY1166: pandas.core.reshape.pivot.crosstab partial support
  - PNDSPY1167: pandas.core.reshape.pivot.pivot partial support
  - PNDSPY1168: pandas.core.reshape.pivot.pivot\_table partial support
  - PNDSPY1169: pandas.core.reshape.tile.cut partial support
  - PNDSPY1170: pandas.core.reshape.tile.qcut partial support
  - PNDSPY1171: pandas.core.series.Series.add partial support
  - PNDSPY1172: pandas.core.series.Series.all partial support
  - PNDSPY1173: pandas.core.series.Series.any partial support
  - PNDSPY1174: pandas.core.series.Series.case\_when partial support
  - PNDSPY1175: pandas.core.series.Series.compare partial support
  - PNDSPY1176: pandas.core.series.Series.cumsum partial support
  - PNDSPY1177: pandas.core.series.Series.div partial support
  - PNDSPY1178: pandas.core.series.Series.divide partial support
  - PNDSPY1179: pandas.core.series.Series.dropna partial support
  - PNDSPY1180: pandas.core.series.Series.eq partial support
  - PNDSPY1181: pandas.core.series.Series.flags partial support
  - PNDSPY1182: pandas.core.series.Series.floordiv partial support
  - PNDSPY1183: pandas.core.series.Series.ge partial support
  - PNDSPY1184: pandas.core.series.Series.groupby partial support
  - PNDSPY1185: pandas.core.series.Series.gt partial support
  - PNDSPY1186: pandas.core.series.Series.le partial support
  - PNDSPY1187: pandas.core.series.Series.lt partial support
  - PNDSPY1188: pandas.core.series.Series.map partial support
  - PNDSPY1189: pandas.core.series.Series.mod partial support
  - PNDSPY1190: pandas.core.series.Series.mul partial support
  - PNDSPY1191: pandas.core.series.Series.multiply partial support
  - PNDSPY1192: pandas.core.series.Series.ne partial support
  - PNDSPY1193: pandas.core.series.Series.nlargest partial support
  - PNDSPY1194: pandas.core.series.Series.nsmallest partial support
  - PNDSPY1195: pandas.core.series.Series.pow partial support
  - PNDSPY1196: pandas.core.series.Series.quantile partial support
  - PNDSPY1197: pandas.core.series.Series.radd partial support
  - PNDSPY1198: pandas.core.series.Series.rdiv partial support
  - PNDSPY1199: pandas.core.series.Series.reindex partial support
  - PNDSPY1200: pandas.core.series.Series.rename partial support
  - PNDSPY1201: pandas.core.series.Series.rfloordiv partial support
  - PNDSPY1202: pandas.core.series.Series.rmod partial support
  - PNDSPY1203: pandas.core.series.Series.rmul partial support
  - PNDSPY1204: pandas.core.series.Series.rpow partial support
  - PNDSPY1205: pandas.core.series.Series.rsub partial support
  - PNDSPY1206: pandas.core.series.Series.rtruediv partial support
  - PNDSPY1207: pandas.core.series.Series.skew partial support
  - PNDSPY1208: pandas.core.series.Series.sort\_index partial support
  - PNDSPY1209: pandas.core.series.Series.sort\_values partial support
  - PNDSPY1210: pandas.core.series.Series.std partial support
  - PNDSPY1211: pandas.core.series.Series.sub partial support
  - PNDSPY1212: pandas.core.series.Series.subtract partial support
  - PNDSPY1213: pandas.core.series.Series.truediv partial support
  - PNDSPY1214: pandas.core.series.Series.unstack partial support
  - PNDSPY1215: pandas.core.series.Series.var partial support
  - PNDSPY1216: pandas.core.strings.accessor.StringMethods.**getitem** partial support
  - PNDSPY1217: pandas.core.strings.accessor.StringMethods.contains partial support
  - PNDSPY1218: pandas.core.strings.accessor.StringMethods.endswith partial support
  - PNDSPY1219: pandas.core.strings.accessor.StringMethods.get partial support
  - PNDSPY1220: pandas.core.strings.accessor.StringMethods.isdigit partial support
  - PNDSPY1221: pandas.core.strings.accessor.StringMethods.len partial support
  - PNDSPY1222: pandas.core.strings.accessor.StringMethods.lstrip partial support
  - PNDSPY1223: pandas.core.strings.accessor.StringMethods.replace partial support
  - PNDSPY1224: pandas.core.strings.accessor.StringMethods.rstrip partial support
  - PNDSPY1225: pandas.core.strings.accessor.StringMethods.slice partial support
  - PNDSPY1226: pandas.core.strings.accessor.StringMethods.split partial support
  - PNDSPY1227: pandas.core.strings.accessor.StringMethods.startswith partial support
  - PNDSPY1228: pandas.core.strings.accessor.StringMethods.strip partial support
  - PNDSPY1229: pandas.core.strings.accessor.StringMethods.translate partial support
  - PNDSPY1230: pandas.core.tools.datetimes.to\_datetime partial support
  - PNDSPY1231: pandas.core.tools.numeric.to\_numeric partial support
  - PNDSPY1232: pandas.core.tools.timedeltas.to\_timedelta partial support
  - PNDSPY1233: pandas.core.window.ewm.ExponentialMovingWindow.corr partial support
  - PNDSPY1234: pandas.core.window.ewm.ExponentialMovingWindow.mean partial support
  - PNDSPY1235: pandas.core.window.ewm.ExponentialMovingWindow.std partial support
  - PNDSPY1236: pandas.core.window.ewm.ExponentialMovingWindow.sum partial support
  - PNDSPY1237: pandas.core.window.ewm.ExponentialMovingWindow.var partial support
  - PNDSPY1238: pandas.core.window.expanding.Expanding.corr partial support
  - PNDSPY1239: pandas.core.window.expanding.Expanding.count partial support
  - PNDSPY1240: pandas.core.window.expanding.Expanding.max partial support
  - PNDSPY1241: pandas.core.window.expanding.Expanding.mean partial support
  - PNDSPY1242: pandas.core.window.expanding.Expanding.min partial support
  - PNDSPY1243: pandas.core.window.expanding.Expanding.sem partial support
  - PNDSPY1244: pandas.core.window.expanding.Expanding.std partial support
  - PNDSPY1245: pandas.core.window.expanding.Expanding.sum partial support
  - PNDSPY1246: pandas.core.window.expanding.Expanding.var partial support
  - PNDSPY1247: pandas.core.window.rolling.Rolling.corr partial support
  - PNDSPY1248: pandas.core.window.rolling.Rolling.count partial support
  - PNDSPY1249: pandas.core.window.rolling.Rolling.max partial support
  - PNDSPY1250: pandas.core.window.rolling.Rolling.mean partial support
  - PNDSPY1251: pandas.core.window.rolling.Rolling.min partial support
  - PNDSPY1252: pandas.core.window.rolling.Rolling.sem partial support
  - PNDSPY1253: pandas.core.window.rolling.Rolling.std partial support
  - PNDSPY1254: pandas.core.window.rolling.Rolling.sum partial support
  - PNDSPY1255: pandas.core.window.rolling.Rolling.var partial support
  - PNDSPY1256: pandas.core.window.rolling.Window.mean partial support
  - PNDSPY1257: pandas.core.window.rolling.Window.std partial support
  - PNDSPY1258: pandas.core.window.rolling.Window.sum partial support
  - PNDSPY1259: pandas.core.window.rolling.Window.var partial support
  - PNDSPY1260: pandas.io.json.\_json.read\_json partial support
  - PNDSPY1261: pandas.io.parquet.read\_parquet partial support
  - PNDSPY1262: pandas.io.parsers.readers.read\_csv partial support

#### Changed

- Updated the sfutils library implementation to support multiple levels of notebooks calls
- Upgraded supported Snowpark Python version from `v1.41.0` to `v1.43.0`. This upgrade includes the following mapping status changes:

  **NotSupported → Direct (8 functions):**

  - `pyspark.sql.functions.bool_and` → `snowflake.snowpark.functions.booland_agg`
  - `pyspark.sql.functions.bucket` → `snowflake.snowpark.functions.bucket`
  - `pyspark.sql.functions.cot` → `snowflake.snowpark.functions.cot`
  - `pyspark.sql.functions.day` → `snowflake.snowpark.functions.day`
  - `pyspark.sql.functions.every` → `snowflake.snowpark.functions.booland_agg`
  - `pyspark.sql.functions.pi` → `snowflake.snowpark.functions.pi`
  - `pyspark.sql.functions.width_bucket` → `snowflake.snowpark.functions.width_bucket`
  - `pyspark.sql.functions.zeroifnull` → `snowflake.snowpark.functions.zeroifnull`

**NotSupported → Rename (1 function):**

> - `pyspark.sql.functions.uuid` → `snowflake.snowpark.functions.uuid_string`

- Upgraded supported Snowpark Pandas version from `v1.41.0` to `v1.43.0`.
- The mapping status of the following Pandas elements were updated:

  **NotSupported → Direct (56 functions):**

  - `pandas.core.arrays.datetimes.DatetimeArray.date`
  - `pandas.core.arrays.datetimes.DatetimeArray.normalize`
  - `pandas.core.arrays.datetimes.DatetimeArray.time`
  - `pandas.core.base.IndexOpsMixin.T`
  - `pandas.core.base.IndexOpsMixin.empty`
  - `pandas.core.base.IndexOpsMixin.is_monotonic_decreasing`
  - `pandas.core.base.IndexOpsMixin.is_monotonic_increasing`
  - `pandas.core.base.IndexOpsMixin.is_unique`
  - `pandas.core.base.IndexOpsMixin.item`
  - `pandas.core.base.IndexOpsMixin.ndim`
  - `pandas.core.base.IndexOpsMixin.nunique`
  - `pandas.core.base.IndexOpsMixin.shape`
  - `pandas.core.base.IndexOpsMixin.size`
  - `pandas.core.base.IndexOpsMixin.to_list`
  - `pandas.core.base.IndexOpsMixin.to_numpy`
  - `pandas.core.base.IndexOpsMixin.tolist`
  - `pandas.core.base.IndexOpsMixin.transpose`
  - `pandas.core.generic.NDFrame.abs`
  - `pandas.core.generic.NDFrame.add_prefix`
  - `pandas.core.generic.NDFrame.add_suffix`
  - `pandas.core.generic.NDFrame.attrs`
  - `pandas.core.generic.NDFrame.copy`
  - `pandas.core.generic.NDFrame.describe`
  - `pandas.core.generic.NDFrame.dtypes`
  - `pandas.core.generic.NDFrame.equals`
  - `pandas.core.generic.NDFrame.first`
  - `pandas.core.generic.NDFrame.first_valid_index`
  - `pandas.core.generic.NDFrame.get`
  - `pandas.core.generic.NDFrame.head`
  - `pandas.core.generic.NDFrame.keys`
  - `pandas.core.generic.NDFrame.last`
  - `pandas.core.generic.NDFrame.last_valid_index`
  - `pandas.core.generic.NDFrame.ndim`
  - `pandas.core.generic.NDFrame.size`
  - `pandas.core.generic.NDFrame.squeeze`
  - `pandas.core.generic.NDFrame.tail`
  - `pandas.core.generic.NDFrame.take`
  - `pandas.core.generic.NDFrame.to_excel`
  - `pandas.core.groupby.groupby.BaseGroupBy.groups`
  - `pandas.core.groupby.groupby.GroupBy.count`
  - `pandas.core.groupby.groupby.GroupBy.cumcount`
  - `pandas.core.groupby.groupby.GroupBy.cummax`
  - `pandas.core.groupby.groupby.GroupBy.cummin`
  - `pandas.core.groupby.groupby.GroupBy.cumsum`
  - `pandas.core.groupby.groupby.GroupBy.head`
  - `pandas.core.groupby.groupby.GroupBy.max`
  - `pandas.core.groupby.groupby.GroupBy.mean`
  - `pandas.core.groupby.groupby.GroupBy.median`
  - `pandas.core.groupby.groupby.GroupBy.min`
  - `pandas.core.groupby.groupby.GroupBy.rank`
  - `pandas.core.groupby.groupby.GroupBy.size`
  - `pandas.core.groupby.groupby.GroupBy.tail`
  - `pandas.core.indexes.datetimes.DatetimeIndex.year`
  - `pandas.core.indexing.IndexingMixin.iat`
  - `pandas.core.indexing.IndexingMixin.iloc`
  - `pandas.core.series.Series.first`

**NotSupported → Partial (70 functions):**

> - `pandas.core.arrays.datetimelike.DatelikeOps.strftime` (PNDSPY1019)
> - `pandas.core.arrays.datetimelike.TimelikeOps.ceil` (PNDSPY1020)
> - `pandas.core.arrays.datetimelike.TimelikeOps.floor` (PNDSPY1021)
> - `pandas.core.arrays.datetimelike.TimelikeOps.round` (PNDSPY1022)
> - `pandas.core.arrays.datetimes.DatetimeArray.day_name` (PNDSPY1023)
> - `pandas.core.arrays.datetimes.DatetimeArray.month_name` (PNDSPY1024)
> - `pandas.core.arrays.datetimes.DatetimeArray.tz_convert` (PNDSPY1025)
> - `pandas.core.arrays.datetimes.DatetimeArray.tz_localize` (PNDSPY1026)
> - `pandas.core.base.IndexOpsMixin.argmax` (PNDSPY1027)
> - `pandas.core.base.IndexOpsMixin.argmin` (PNDSPY1028)
> - `pandas.core.base.IndexOpsMixin.value_counts` (PNDSPY1029)
> - `pandas.core.frame.DataFrame.eval` (PNDSPY1049)
> - `pandas.core.frame.DataFrame.expanding` (PNDSPY1050)
> - `pandas.core.frame.DataFrame.melt` (PNDSPY1067)
> - `pandas.core.frame.DataFrame.pct_change` (PNDSPY1077)
> - `pandas.core.frame.DataFrame.quantile` (PNDSPY1081)
> - `pandas.core.frame.DataFrame.std` (PNDSPY1103)
> - `pandas.core.generic.NDFrame.asfreq` (PNDSPY1037)
> - `pandas.core.generic.NDFrame.fillna` (PNDSPY1052)
> - `pandas.core.generic.NDFrame.mask` (PNDSPY1066)
> - `pandas.core.generic.NDFrame.pct_change` (PNDSPY1077)
> - `pandas.core.generic.NDFrame.rank` (PNDSPY1083)
> - `pandas.core.generic.NDFrame.replace` (PNDSPY1087)
> - `pandas.core.generic.NDFrame.shift` (PNDSPY1115)
> - `pandas.core.generic.NDFrame.to_csv` (PNDSPY1106)
> - `pandas.core.generic.NDFrame.tz_convert` (PNDSPY1110)
> - `pandas.core.generic.NDFrame.tz_localize` (PNDSPY1111)
> - `pandas.core.generic.NDFrame.where` (PNDSPY1114)
> - `pandas.core.groupby.generic.DataFrameGroupBy.transform` (PNDSPY1121)
> - `pandas.core.groupby.generic.DataFrameGroupBy.value_counts` (PNDSPY1122)
> - `pandas.core.groupby.groupby.BaseGroupBy.get_group` (PNDSPY1123)
> - `pandas.core.groupby.groupby.GroupBy.bfill` (PNDSPY1127)
> - `pandas.core.groupby.groupby.GroupBy.first` (PNDSPY1129)
> - `pandas.core.groupby.groupby.GroupBy.last` (PNDSPY1130)
> - `pandas.core.groupby.groupby.GroupBy.quantile` (PNDSPY1132)
> - `pandas.core.groupby.groupby.GroupBy.resample` (PNDSPY1133)
> - `pandas.core.groupby.groupby.GroupBy.rolling` (PNDSPY1134)
> - `pandas.core.groupby.groupby.GroupBy.shift` (PNDSPY1135)
> - `pandas.core.groupby.groupby.GroupBy.std` (PNDSPY1136)
> - `pandas.core.groupby.groupby.GroupBy.var` (PNDSPY1137)
> - `pandas.core.indexes.base.Index.nlevels` (PNDSPY1140)
> - `pandas.core.indexes.base.Index.sort_values` (PNDSPY1142)
> - `pandas.core.indexing.IndexingMixin.at` (PNDSPY1039)
> - `pandas.core.indexing.IndexingMixin.loc` (PNDSPY1063)
> - `pandas.core.resample.Resampler.ffill` (PNDSPY1155)
> - `pandas.core.resample.Resampler.first` (PNDSPY1157)
> - `pandas.core.resample.Resampler.last` (PNDSPY1158)
> - `pandas.core.resample.Resampler.std` (PNDSPY1160)
> - `pandas.core.resample.Resampler.var` (PNDSPY1161)
> - `pandas.core.reshape.merge.merge_asof` (PNDSPY1165)
> - `pandas.core.reshape.pivot.pivot` (PNDSPY1167)
> - `pandas.core.series.Series.expanding` (PNDSPY1050)
> - `pandas.core.series.Series.pct_change` (PNDSPY1077)
> - `pandas.core.window.ewm.ExponentialMovingWindow.corr` (PNDSPY1233)
> - `pandas.core.window.ewm.ExponentialMovingWindow.mean` (PNDSPY1234)
> - `pandas.core.window.ewm.ExponentialMovingWindow.std` (PNDSPY1235)
> - `pandas.core.window.ewm.ExponentialMovingWindow.sum` (PNDSPY1236)
> - `pandas.core.window.ewm.ExponentialMovingWindow.var` (PNDSPY1237)
> - `pandas.core.window.expanding.Expanding.corr` (PNDSPY1238)
> - `pandas.core.window.expanding.Expanding.max` (PNDSPY1240)
> - `pandas.core.window.expanding.Expanding.mean` (PNDSPY1241)
> - `pandas.core.window.expanding.Expanding.min` (PNDSPY1242)
> - `pandas.core.window.expanding.Expanding.sem` (PNDSPY1243)
> - `pandas.core.window.expanding.Expanding.std` (PNDSPY1244)
> - `pandas.core.window.expanding.Expanding.sum` (PNDSPY1245)
> - `pandas.core.window.expanding.Expanding.var` (PNDSPY1246)
> - `pandas.core.window.rolling.Window.mean` (PNDSPY1256)
> - `pandas.core.window.rolling.Window.std` (PNDSPY1257)
> - `pandas.core.window.rolling.Window.sum` (PNDSPY1258)
> - `pandas.core.window.rolling.Window.var` (PNDSPY1259)

**(new) → Direct (74 functions):**

> - `pandas.core.arrays.datetimes.DatetimeArray.day`
> - `pandas.core.arrays.datetimes.DatetimeArray.day_of_week`
> - `pandas.core.arrays.datetimes.DatetimeArray.day_of_year`
> - `pandas.core.arrays.datetimes.DatetimeArray.dayofweek`
> - `pandas.core.arrays.datetimes.DatetimeArray.dayofyear`
> - `pandas.core.arrays.datetimes.DatetimeArray.days_in_month`
> - `pandas.core.arrays.datetimes.DatetimeArray.daysinmonth`
> - `pandas.core.arrays.datetimes.DatetimeArray.hour`
> - `pandas.core.arrays.datetimes.DatetimeArray.is_leap_year`
> - `pandas.core.arrays.datetimes.DatetimeArray.is_month_end`
> - `pandas.core.arrays.datetimes.DatetimeArray.is_month_start`
> - `pandas.core.arrays.datetimes.DatetimeArray.is_quarter_end`
> - `pandas.core.arrays.datetimes.DatetimeArray.is_quarter_start`
> - `pandas.core.arrays.datetimes.DatetimeArray.is_year_end`
> - `pandas.core.arrays.datetimes.DatetimeArray.is_year_start`
> - `pandas.core.arrays.datetimes.DatetimeArray.isocalendar`
> - `pandas.core.arrays.datetimes.DatetimeArray.microsecond`
> - `pandas.core.arrays.datetimes.DatetimeArray.minute`
> - `pandas.core.arrays.datetimes.DatetimeArray.month`
> - `pandas.core.arrays.datetimes.DatetimeArray.nanosecond`
> - `pandas.core.arrays.datetimes.DatetimeArray.quarter`
> - `pandas.core.arrays.datetimes.DatetimeArray.second`
> - `pandas.core.arrays.datetimes.DatetimeArray.weekday`
> - `pandas.core.arrays.datetimes.DatetimeArray.year`
> - `pandas.core.arrays.timedeltas.TimedeltaArray.days`
> - `pandas.core.arrays.timedeltas.TimedeltaArray.microseconds`
> - `pandas.core.arrays.timedeltas.TimedeltaArray.nanoseconds`
> - `pandas.core.arrays.timedeltas.TimedeltaArray.seconds`
> - `pandas.core.frame.DataFrame.flags`
> - `pandas.core.generic.NDFrame.flags`
> - `pandas.core.generic.NDFrame.rename_axis`
> - `pandas.core.groupby.groupby.BaseGroupBy.__iter__`
> - `pandas.core.groupby.groupby.BaseGroupBy.__len__`
> - `pandas.core.groupby.groupby.GroupBy.sum`
> - `pandas.core.indexes.base.Index.T`
> - `pandas.core.indexes.datetimes.DatetimeIndex.date`
> - `pandas.core.indexes.datetimes.DatetimeIndex.day`
> - `pandas.core.indexes.datetimes.DatetimeIndex.day_of_week`
> - `pandas.core.indexes.datetimes.DatetimeIndex.day_of_year`
> - `pandas.core.indexes.datetimes.DatetimeIndex.dayofweek`
> - `pandas.core.indexes.datetimes.DatetimeIndex.dayofyear`
> - `pandas.core.indexes.datetimes.DatetimeIndex.hour`
> - `pandas.core.indexes.datetimes.DatetimeIndex.is_month_end`
> - `pandas.core.indexes.datetimes.DatetimeIndex.is_month_start`
> - `pandas.core.indexes.datetimes.DatetimeIndex.mean`
> - `pandas.core.indexes.datetimes.DatetimeIndex.microsecond`
> - `pandas.core.indexes.datetimes.DatetimeIndex.minute`
> - `pandas.core.indexes.datetimes.DatetimeIndex.month`
> - `pandas.core.indexes.datetimes.DatetimeIndex.nanosecond`
> - `pandas.core.indexes.datetimes.DatetimeIndex.normalize`
> - `pandas.core.indexes.datetimes.DatetimeIndex.quarter`
> - `pandas.core.indexes.datetimes.DatetimeIndex.second`
> - `pandas.core.indexes.timedeltas.TimedeltaIndex.total_seconds`
> - `pandas.core.series.Series.info` (PNDSPY1018)
> - `pandas.core.series.Series.tolist`
> - `pandas.core.strings.accessor.StringMethods.capitalize`
> - `pandas.core.strings.accessor.StringMethods.center`
> - `pandas.core.strings.accessor.StringMethods.count`
> - `pandas.core.strings.accessor.StringMethods.islower`
> - `pandas.core.strings.accessor.StringMethods.istitle`
> - `pandas.core.strings.accessor.StringMethods.isupper`
> - `pandas.core.strings.accessor.StringMethods.ljust`
> - `pandas.core.strings.accessor.StringMethods.lower`
> - `pandas.core.strings.accessor.StringMethods.match`
> - `pandas.core.strings.accessor.StringMethods.pad`
> - `pandas.core.strings.accessor.StringMethods.rjust`
> - `pandas.core.strings.accessor.StringMethods.title`
> - `pandas.core.strings.accessor.StringMethods.upper`
> - `snowpark_pandas.read_snowflake`
> - `snowpark_pandas.to_dynamic_table`
> - `snowpark_pandas.to_iceberg`
> - `snowpark_pandas.to_pandas`
> - `snowpark_pandas.to_snowflake`
> - `snowpark_pandas.to_view`

**(new) → Partial (47 functions):**

> - `pandas.core.frame.DataFrame.__dataframe__` (PNDSPY1031)
> - `pandas.core.frame.DataFrame.pad` (PNDSPY1076)
> - `pandas.core.generic.NDFrame.align` (PNDSPY1033)
> - `pandas.core.generic.NDFrame.astype` (PNDSPY1038)
> - `pandas.core.generic.NDFrame.expanding` (PNDSPY1050)
> - `pandas.core.generic.NDFrame.ffill` (PNDSPY1051)
> - `pandas.core.generic.NDFrame.interpolate` (PNDSPY1015)
> - `pandas.core.generic.NDFrame.pad` (PNDSPY1076)
> - `pandas.core.generic.NDFrame.resample` (PNDSPY1088)
> - `pandas.core.generic.NDFrame.rolling` (PNDSPY1092)
> - `pandas.core.generic.NDFrame.sample` (PNDSPY1097)
> - `pandas.core.groupby.groupby.GroupBy.all` (PNDSPY1124)
> - `pandas.core.groupby.groupby.GroupBy.any` (PNDSPY1125)
> - `pandas.core.groupby.groupby.GroupBy.apply` (PNDSPY1126)
> - `pandas.core.indexes.base.Index.all` (PNDSPY1138)
> - `pandas.core.indexes.base.Index.any` (PNDSPY1139)
> - `pandas.core.indexes.base.Index.reindex` (PNDSPY1141)
> - `pandas.core.indexes.base.Index.value_counts` (PNDSPY1029)
> - `pandas.core.indexes.datetimes.DatetimeIndex.tz_convert` (PNDSPY1149)
> - `pandas.core.indexes.datetimes.DatetimeIndex.tz_localize` (PNDSPY1150)
> - `pandas.core.series.Series.backfill` (PNDSPY1040)
> - `pandas.core.series.Series.bfill` (PNDSPY1041)
> - `pandas.core.series.Series.flags` (PNDSPY1181)
> - `pandas.core.series.Series.pad` (PNDSPY1076)
> - `pandas.core.strings.accessor.StringMethods.__getitem__` (PNDSPY1216)
> - `pandas.core.strings.accessor.StringMethods.contains` (PNDSPY1217)
> - `pandas.core.strings.accessor.StringMethods.endswith` (PNDSPY1218)
> - `pandas.core.strings.accessor.StringMethods.get` (PNDSPY1219)
> - `pandas.core.strings.accessor.StringMethods.isdigit` (PNDSPY1220)
> - `pandas.core.strings.accessor.StringMethods.len` (PNDSPY1221)
> - `pandas.core.strings.accessor.StringMethods.lstrip` (PNDSPY1222)
> - `pandas.core.strings.accessor.StringMethods.replace` (PNDSPY1223)
> - `pandas.core.strings.accessor.StringMethods.rstrip` (PNDSPY1224)
> - `pandas.core.strings.accessor.StringMethods.slice` (PNDSPY1225)
> - `pandas.core.strings.accessor.StringMethods.split` (PNDSPY1226)
> - `pandas.core.strings.accessor.StringMethods.startswith` (PNDSPY1227)
> - `pandas.core.strings.accessor.StringMethods.strip` (PNDSPY1228)
> - `pandas.core.strings.accessor.StringMethods.translate` (PNDSPY1229)
> - `pandas.core.window.rolling.Rolling.corr` (PNDSPY1247)
> - `pandas.core.window.rolling.Rolling.max` (PNDSPY1249)
> - `pandas.core.window.rolling.Rolling.mean` (PNDSPY1250)
> - `pandas.core.window.rolling.Rolling.min` (PNDSPY1251)
> - `pandas.core.window.rolling.Rolling.sem` (PNDSPY1252)
> - `pandas.core.window.rolling.Rolling.std` (PNDSPY1253)
> - `pandas.core.window.rolling.Rolling.sum` (PNDSPY1254)
> - `pandas.core.window.rolling.Rolling.var` (PNDSPY1255)
> - `pandas.io.json._json.read_json` (PNDSPY1260)

**Direct → Partial (12 functions):**

> - `pandas.core.frame.DataFrame.T` (PNDSPY1030)
> - `pandas.core.frame.DataFrame.any` (PNDSPY1035)
> - `pandas.core.frame.DataFrame.where` (PNDSPY1114)
> - `pandas.core.groupby.generic.DataFrameGroupBy.agg` (PNDSPY1116)
> - `pandas.core.indexes.datetimes.DatetimeIndex.round` (PNDSPY1147)
> - `pandas.core.reshape.tile.qcut` (PNDSPY1170)
> - `pandas.core.series.Series.astype` (PNDSPY1038)
> - `pandas.core.series.Series.groupby` (PNDSPY1184)
> - `pandas.core.series.Series.le` (PNDSPY1186)
> - `pandas.core.series.Series.loc` (PNDSPY1063)
> - `pandas.io.parquet.read_parquet` (PNDSPY1261)
> - `pandas.io.parsers.readers.read_csv` (PNDSPY1262)

**Partial → Direct (5 functions):**

> - `pandas.core.indexes.datetimes.DatetimeIndex.is_leap_year`
> - `pandas.core.indexes.datetimes.DatetimeIndex.is_quarter_end`
> - `pandas.core.indexes.datetimes.DatetimeIndex.is_quarter_start`
> - `pandas.core.indexes.datetimes.DatetimeIndex.is_year_end`
> - `pandas.core.indexes.datetimes.DatetimeIndex.is_year_start`

**Rename → Partial (4 functions):**

> - `pandas.core.frame.DataFrame.divide` (PNDSPY1046)
> - `pandas.core.frame.DataFrame.multiply` (PNDSPY1071)
> - `pandas.core.frame.DataFrame.subtract` (PNDSPY1105)
> - `pandas.core.series.Series.divide` (PNDSPY1178)

#### Fixed

- Fixed the “How to read through the scores” link on the assessment and conversion results page to ensure it correctly opens the readiness score documentation.

## Version 3.0.0 (Feb 12, 2026)

### Application & CLI Version: 3.0.0

#### Included SMA Core Version

- Snowpark Conversion Core: 8.1.55

### Engine Release Notes

#### Improvements

- **License-Free Conversion Mode:** A license or access code is no longer required to run SMA in Conversion mode.
- **Project Options Page:** A new Project Options page has been introduced to present the available workflows in the application, including “Code Analysis and Conversion”.
- **Technical Discovery Relocation:** The Technical Discovery section has been moved to the Project Creation page for a more streamlined project setup experience.
- **Simplified Conversion Setup:** The Conversion Setup page has been updated and no longer requires a license or access code.
- **Project File Extension:** The project file extension has changed from `.snowma` to `.snowct`.
- **Updated User Interface:** The user interface has been refreshed to align with the SnowConvert AI look and feel.

## Version 2.11.1 (Jan 30, 2026)

### Application & CLI Version: 2.11.1

#### Included SMA Core Version

- Snowpark Conversion Core: 8.1.55

### Engine Release Notes

#### Added

- Added SQL Language to the DetailedReport doc file.
- Added SQL configuration cell at the beginning of a converted Databricks-to-Jupyter transformation to be compatible with Snowflake notebooks.

#### Changed

- Updated the `%run` magic command transformation to append `.ipynb` extension to notebook paths.

  - For unquoted paths: `%run ./myNotebook` transforms to `%run ./myNotebook.ipynb`
  - For quoted paths: `%run "./myNotebook"` transforms to `%run "./myNotebook.ipynb"`
- Scala code in notebook cells will now be commented in a python cell during a notebook migration.
- Updated the conversion of `dbutils.run` to the `sfutils.notebook.run` function to handle notebook execution calls.
- Bumped the supported versions of Snowpark Python API and Snowpark Pandas API from `1.40.0` to `1.41.0`.
- Updated the mapping status for the following Pandas functions from NotSupported to Partial:

  - `pandas.core.frame.DataFrame.agg` → `modin.pandas.DataFrame.agg`
  - `pandas.core.frame.DataFrame.interpolate` → `modin.pandas.DataFrame.interpolate`
  - `pandas.core.reshape.encoding.get_dummies` → `modin.pandas.general.get_dummies`
  - `pandas.core.series.Series.agg` → `modin.pandas.Series.agg`
  - `pandas.core.series.Series.interpolate` → `modin.pandas.Series.interpolate`

#### Fixed

- SMA now will rename `.hql` (Hive SQL) files to `.sql` after conversion.
- The implicit cell for a DBX Scala Notebook when converting to Snowflake will be a python cell with an EWI. The Scala code will be commented out.
- Python cells from DBX SQL Notebooks will preserve the language metadata.

#### Removed

- Removed the previous `%run` transformation in DBX notebooks that generated `spark.sql("EXECUTE NOTEBOOK ...")` SQL statements.
- The SnowConvert MissingObjects report was absorbed by the MissingObjectReference report. The MissingObjects report will no longer be generated.

## Version 2.11.0 (Jan 9, 2026)

### Application & CLI Version: 2.11.0

#### Included SMA Core Version

- Snowpark Conversion Core: 8.1.43

#### Included SnowConvert AI Version

- SnowConvert AI Version 2.2.0 ([Release Notes](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/release-notes/release-notes/README#version-2-2-0-jan-07-2026))

### Engine Release Notes

#### Added

- **Enhanced Notebook Setup for Assessment:** When running an assessment on Databricks notebooks, a Snowpark Connect session is now automatically added to the first cell to simplify your setup.
- **Automatic Snowpark Connect Conversion:** The tool now automatically converts both `SparkSession` and `SparkContext` initializations in Python code to their equivalent Snowpark Connect sessions.
- **Improved Error Identification:**

  - Added a new warning code, `SPRKCNTPY4000`, to clearly flag any `SparkContext` elements that are not yet supported by Snowpark Connect.
  - The tool now automatically detects and flags unsupported Databricks utility calls (`dbutils` API) with the new warning code `SPRKDBX1004` during conversion.
- **More Detailed Reporting:**

  - The SparkUsagesInventory.csv report now includes a new column called `IS_SNOWPARK_CONNECT_TOOL_SUPPORTED`
  - This new column is to clearly indicate if a Spark element is supported directly by Snowpark Connect, or supported through an SMA transformation.
  - The Snowpark Connect readiness score calculation has been updated to use the new `IS_SNOWPARK_CONNECT_TOOL_SUPPORTED` column in the SparkUsagesInventory.csv report.
- **Next-Generation Notebook Support:** Enhanced support for the VNext Snowflake Notebooks format when converting Databricks or Jupyter notebooks.

  - **Full VNext Compatibility:** The SMA can now generate output files that fully adhere to the VNext Snowflake Notebooks standard, regardless of whether the source was a Databricks or a previous-generation Jupyter notebook.
  - **Smarter Language Handling:** The conversion engine has been updated with enhanced logic to accurately detect and manage the specific language (such as Python or Scala) within each individual notebook cell. This allows for more precise and reliable cell-by-cell conversion.
  - **Enhanced Metadata for Cells:** The process now correctly incorporates necessary language and type metadata at the cell level during generation, which is essential for VNext Notebooks to function as expected.

#### Changed

- **Simplified Python Code:** For Snowpark Connect, unnecessary `.sparkContext` references in Python method calls are now removed to streamline your code.
- **Clearer Warning Codes:** Snowpark Connect warning codes are now renamed to include language-specific prefixes (e.g., `SPRKCNTPY` for Python, `SPRKCNTSCL` for Scala) for easier error identification.
- **More Accurate Notebook Conversions:** The conversion process for notebooks has been improved to correctly distinguish between Databricks and Jupyter formats, preventing incorrect modifications.

#### Fixed

- Fixed a bug in the artifact dependency inventory that incorrectly reported `.options()` configuration as a data source.

### Desktop Release Notes

#### Added

- **Technical Discovery View:** A new Technical Discovery View is now available in the desktop application.
- **SMA Assessment AI:** SMA desktop application is now directly integrated with an optional LLM interface.
  - Ask questions about your assessment results
  - Get help with how to approach the migration
  - Connect and deploy your assessment results directly into your Snowflake account.

#### Changed

- The Command Line Interface (CLI) parameter for controlling Jupyter conversion has been updated from `--enableJupyter` to `--disableJupyterConversion` for clearer functionality.

## Version 2.10.5 (Dec 3rd, 2025)

### Application & CLI Version: 2.10.5

#### Included SMA Core Versions

- Snowpark Conversion Core: 8.1.26

#### Included SnowConvert AI Version

- SnowConvert AI Version 2.0.57 (Release Notes: [SnowConvert AI - Recent Release Notes | Snowflake Documentation](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/release-notes/release-notes/README))

### Engine Release Notes

#### Added

- The **Execution Summary** section of the `DetailedReport.docx` now indicates whether the SMA was run in Assessment or Conversion mode.

#### Changed

- Bumped the supported versions of Snowpark Python API and Snowpark Pandas API from `1.39.0` to `1.40.0`.

**PySpark Function Mapping Updates:**

**NotSupported** to **Rename**:

- `pyspark.sql.functions.unhex` → `snowflake.snowpark.functions.hex_decode_binary`

**Direct** to **Rename**:

- `pyspark.sql.functions.greatest` → `snowflake.snowpark.functions.greatest_ignore_nulls`
- `pyspark.sql.functions.least` → `snowflake.snowpark.functions.least_ignore_nulls`

**NotDefined** to **Rename**:

- `pyspark.sql.functions.bool_or` → `snowflake.snowpark.functions.boolor_agg`
- `pyspark.sql.functions.char` → `snowflake.snowpark.functions.chr`

**NotDefined** to **Direct**:

- `pyspark.sql.functions.nullif` → `snowflake.snowpark.functions.nullif`
- `pyspark.sql.functions.nvl2` → `snowflake.snowpark.functions.nvl2`

**Snowpark Pandas Function Mapping Updates:**

**NotSupported** to **Partial**:

- `modin.pandas.DataFrame.query` → `snowflake.snowpark.pandas.core.frame.DataFrame.query`
- Added a new EWI `PNDSPY1012` to indicate that `modin.pandas.DataFrame.query` does not support MultiIndex. The following example scenario illustrating this limitation is also included in the EWI documentation.

  Copy code

  ```
  from snowflake.snowpark.modin import plugin
  import modin.pandas as pd # Snowpark pandas

  # Create a DataFrame with single-level index
  data = {
   'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank'],
   'age': [25, 30, 35, 28, 32, 45],
   'salary': [50000, 60000, 75000, 55000, 80000, 90000],
   'department': ['Sales', 'IT', 'HR', 'Sales', 'IT', 'HR']
  }
  df = pd.DataFrame(data)

  # Set a single-level index
  df = df.set_index('name')
  print("DataFrame with single-level index:")
  print(df)

  # Use query() - This works fine!
  #EWI: PNDSPY1012 => pandas.core.frame.DataFrame.query does not support DataFrames that have a row MultiIndex. Check Snowpark Pandas documentation for more details.
  result = df.query("age > 30 and salary < 85000")

  # Create a DataFrame with MultiIndex on rows
  data = {
   'A': [1, 2, 3, 4, 5, 6],
   'B': [10, 20, 30, 40, 50, 60],
   'C': ['x', 'y', 'x', 'y', 'x', 'y']
  }
  df = pd.DataFrame(data)

  # Create MultiIndex
  df = df.set_index([
   pd.Index(['group1', 'group1', 'group2', 'group2', 'group3', 'group3']),
   pd.Index(['a', 'b', 'a', 'b', 'a', 'b'])
  ])
  df.index.names = ['group', 'subgroup']

  # This will ERROR in Snowpark pandas!
  #EWI: PNDSPY1012 => pandas.core.frame.DataFrame.query does not support DataFrames that have
  ```

  **Recommended fix:** If the DataFrame contains a MultiIndex, it is necessary to validate the behavior of the `query()` method in Snowpark pandas. Ensure that the DataFrame structure is compatible with Snowpark pandas’ limitations, as MultiIndex rows are not supported. Consider restructuring the DataFrame to use a single-level index or alternative filtering methods.
- Updated all documentation links in the `DetailedReport.docx` to point to the official Snowflake documentation, replacing the legacy Snowpark Migration Accelerator site.
- Updated the Snowpark Connect readiness score descriptions in the `DetailedReport.docx` to match the SMA UI.
- Usages of `pyspark.sql.window.WindowSpec.orderBy` are now reported as supported by Snowpark Connect.

#### Fixed

- Fixed broken internal links in the `DetailedReport.docx` to ensure proper navigation between document sections.
- Added a `CellId` column to the issues inventory to easily identify the location of EWIs within notebook files.

## Version 2.10.4 (Nov 18, 2025)

### Application & CLI Version: 2.10.4

#### Included SMA Core Versions

- Snowpark Conversion Core: 8.1.8

### Engine Release Notes

#### Fixed

- Fixed an issue where the SMA generated corrupted Databricks notebook files in the output directory during Assessment mode execution.
- Fixed an issue where the SMA would crash if the input directory contained folders named “SMA\_ConvertedNotebooks”.

## Version 2.10.3 (Oct 30, 2025)

### Application & CLI Version: 2.10.3

#### Included SMA Core Versions

- Snowpark Conversion Core: 8.1.7

### Engine Release Notes

#### Added

- Added the [Snowpark Connect readiness score](https://docs.snowflake.com/en/migrations/sma-docs/user-guide/assessment/readiness-scores#snowpark-connect-readiness-score). This new score measures the percentage of Spark API references in your codebase that are supported by [Snowpark Connect for Spark](https://docs.snowflake.com/en/developer-guide/snowpark-connect/snowpark-connect-apache-spark).

  - This will now be the **only** score shown in assessment mode. To generate the [Snowpark API Readiness Score](https://docs.snowflake.com/en/migrations/sma-docs/user-guide/assessment/readiness-scores#snowpark-api-readiness-score), run the SMA in [conversion mode](https://docs.snowflake.com/en/migrations/sma-docs/user-guide/snowpark-api-conversion/README).
- Added support for SQL embedded migration for literal string concatenations assigned to a local variable in the same scope of execution.

  - Included scenarios now include:

    Copy code

    ```
    sqlStat = "SELECT colName " + "FROM myTable"
    session.sql(sqlStat)
    ```

#### Changed

- Updated the EWI URLs in the [Issues.csv](https://docs.snowflake.com/en/migrations/sma-docs/user-guide/scos-conversion/output-reports/sma-inventories#issue-inventory) inventory to point to the [main Snowflake documentation site](https://docs.snowflake.com/en/migrations/sma-docs/issue-analysis/approach).

#### Fixed

- Fixed a code issue that caused inner project configuration files (e.g., pom.xml, build.sbt, build.gradle) to be incorrectly placed in the root of the output directory instead of the correct inner directories after migration.

### Desktop Release Notes

#### Added

- Added the Snowpark Connect readiness score and updated the assessment execution flow.
  - When running the application in assessment mode, **only** the Snowpark Connect readiness score is now displayed.
  - When running the application in conversion mode, the Snowpark API readiness score is displayed (the Snowpark Connect Readiness will **not** be shown).

#### Changed

Updated all in-application documentation links to point to the official [Snowflake documentation](https://docs.snowflake.com/en/migrations/sma-docs/README), replacing the legacy [SnowConvert](https://docs.snowconvert.com/sma) site.

## Version 2.10.2 (Oct 27, 2025)

### Application & CLI Version 2.10.2

#### Included SMA Core Versions

- Snowpark Conversion Core 8.0.73

#### Fixed

- Fixed an issue where the Snowpark Migration Accelerator failed converting DBC files into Jupyter Notebooks properly.

## Version 2.10.1 (Oct 23, 2025)

### Application & CLI Version 2.10.1

#### Included SMA Core Versions

- Snowpark Conversion Core 8.0.72

#### Added

- Added support for Snowpark Scala v1.17.0:

**From Not Supported to Direct:**

**Dataset:**

- `org.apache.spark.sql.Dataset.isEmpty` → `com.snowflake.snowpark.DataFrame.isEmpty`

**Row:**

- `org.apache.spark.sql.Row.mkString` → `com.snowflake.snowpark.Row.mkString`

**StructType:**

- `org.apache.spark.sql.types.StructType.fieldNames` → `com.snowflake.snowpark.types.StructType.fieldNames`

**From Not Supported to Rename:**

**Functions:**

- `org.apache.spark.functions.flatten` → `com.snowflake.snowpark.functions.array_flatten`

**From Direct to Rename:**

**Functions:**

- `org.apache.spark.functions.to_date` → `com.snowflake.snowpark.functions.try_to_date`
- `org.apache.spark.functions.to_timestamp` → `com.snowflake.snowpark.functions.try_to_timestamp`

**From Direct Helper to Rename:**

**Functions:**

- `org.apache.spark.sql.functions.concat_ws` → `com.snowflake.snowpark.functions.concat_ws_ignore_nulls`

**From Not Defined to Direct:**

**Functions:**

- `org.apache.spark.functions.try_to_timestamp` → `com.snowflake.snowpark.functions.try_to_timestamp`
- Embedded SQL is now migrated when a SQL statement literal is assigned to a local variable.

Example:
sqlStat = “SELECT colName FROM myTable”
session.sql(sqlStat)

- Embedded SQL is now supported for literal strings concatenations.

Example:
session.sql(“SELECT colName “ + “FROM myTable”)

#### Changed

- Updated the supported versions of Snowpark Python API and Snowpark Pandas API from 1.36.0 to 1.39.0.
- Updated the mapping status for the following PySpark xpath functions from NotSupported to Direct with EWI SPRKPY1103:

  - `pyspark.sql.functions.xpath`
  - `pyspark.sql.functions.xpath_boolean`
  - `pyspark.sql.functions.xpath_double`
  - `pyspark.sql.functions.xpath_float`
  - `pyspark.sql.functions.xpath_int`
  - `pyspark.sql.functions.xpath_long`
  - `pyspark.sql.functions.xpath_number`
  - `pyspark.sql.functions.xpath_short`
  - `pyspark.sql.functions.xpath_string`
- Updated the mapping status for the following PySpark elements from NotDefined to Direct:

  - `pyspark.sql.functions.bit_and` → `snowflake.snowpark.functions.bitand_agg`
  - `pyspark.sql.functions.bit_or` → `snowflake.snowpark.functions.bitor_agg`
  - `pyspark.sql.functions.bit_xor` → `snowflake.snowpark.functions.bitxor_agg`
  - `pyspark.sql.functions.getbit` → `snowflake.snowpark.functions.getbit`
- Updated the mapping status for the following Pandas elements from NotSupported to Direct:

  - `pandas.core.indexes.base.Index` → `modin.pandas.Index`
  - `pandas.core.indexes.base.Index.get_level_values` → `modin.pandas.Index.get_level_values`
- Updated the mapping status for the following PySpark functions from NotSupported to Rename:

  - `pyspark.sql.functions.now` → `snowflake.snowpark.functions.current_timestamp`

#### Fixed

- Fixed Scala not migrating imports when there’s a rename.

  **Example:**

  **Source code:**

  Copy code

  ```
  package com.example.functions
  import org.apache.spark.sql.functions.{to_timestamp, lit}
  object ToTimeStampTest extends App {
  to_timestamp(lit("sample"))
  to_timestamp(lit("sample"), "yyyy-MM-dd")
   }
  ```

  **Output code:**

  Copy code

  ```
  package com.example.functions
  import com.snowflake.snowpark.functions.{try_to_timestamp, lit}
  import com.snowflake.snowpark_extensions.Extensions._
  import com.snowflake.snowpark_extensions.Extensions.functions._
  object ToTimeStampTest extends App {
  try_to_timestamp(lit("sample"))
  try_to_timestamp(lit("sample"), "yyyy-MM-dd")
   }
  ```

## Version 2.10.0 (Sep 24, 2025)

### Application & CLI Version 2.10.0

#### Included SMA Core Versions

- Snowpark Conversion Core 8.0.62

#### Added

- Added functionality to migrate SQL embedded with Python format interpolation.
- Added support for `DataFrame.select` and `DataFrame.sort` transformations for greater data processing flexibility.

#### Changed

- Bumped the supported versions of Snowpark Python API and Snowpark Pandas API to 1.36.0.
- Updated the mapping status of `pandas.core.frame.DataFrame.boxplot` from Not Supported to Direct.
- Updated the mapping status of `DataFrame.select`, `Dataset.select`, `DataFrame.sort` and `Dataset.sort` from Direct to Transformation.
- Snowpark Scala allows a sequence of columns to be passed directly to the select and sort functions, so this transformation changes all the usages such as `df.select(cols: _*)` to `df.select(cols)` and `df.sort(cols: _*)` to `df.sort(cols)`.
- Bumped Python AST and Parser version to 149.1.9.
- Updated the status to Direct for pandas functions:

  - `pandas.core.frame.DataFrame.to_excel`
  - `pandas.core.series.Series.to_excel`
  - `pandas.io.feather_format.read_feather`
  - `pandas.io.orc.read_orc`
  - `pandas.io.stata.read_stata`
- Updated the status for `pyspark.sql.pandas.map_ops.PandasMapOpsMixin.mapInPandas` to workaround using the EWI SPRKPY1102.

#### Fixed

- Fixed issue that affected SqlEmbedded transformations when using chained method calls.
- Fixed transformations involving PySqlExpr using the new PyLiteralSql to avoid losing Tails.
- Resolved internal stability issues to improve tool robustness and reliability.

## Version 2.9.0 (Sep 09, 2025)

### Included SMA Core Versions

- Snowpark Conversion Core 8.0.53

#### Added

- The following mappings are now performed for `org.apache.spark.sql.Dataset[T]`:

  - `org.apache.spark.sql.Dataset.union` is now `com.snowflake.snowpark.DataFrame.unionAll`
  - `org.apache.spark.sql.Dataset.unionByName` is now `com.snowflake.snowpark.DataFrame.unionAllByName`
- Added support for `org.apache.spark.sql.functions.broadcast` as a transformation.

#### Changed

- Increased the supported Snowpark Python API version for SMA from `1.27.0` to `1.33.0`.
- The status for the `pyspark.sql.functions.randn` function has been updated to Direct.

#### Fixed

- Resolved an issue where `org.apache.spark.SparkContext.parallelize` was not resolving and now supports it as a transformation.
- Fixed the `Dataset.persist` transformation to work with any type of Dataset, not just `Dataset[Row]`.

## Version 2.7.7 (Aug 28, 2025)

### Application & CLI Version 2.7.7

#### Included SMA Core Versions

- Snowpark Conversion Core 8.0.46

#### Added

- Added new Pandas EWI documentation PNDSPY1011.
- Added support to the following Pandas functions:
  - pandas.core.algorithms.unique
  - pandas.core.dtypes.missing.isna
  - pandas.core.dtypes.missing.isnull
  - pandas.core.dtypes.missing.notna
  - pandas.core.dtypes.missing.notnull
  - pandas.core.resample.Resampler.count
  - pandas.core.resample.Resampler.max
  - pandas.core.resample.Resampler.mean
  - pandas.core.resample.Resampler.median
  - pandas.core.resample.Resampler.min
  - pandas.core.resample.Resampler.size
  - pandas.core.resample.Resampler.sum
  - pandas.core.arrays.timedeltas.TimedeltaArray.total\_seconds
  - pandas.core.series.Series.get
  - pandas.core.series.Series.to\_frame
  - pandas.core.frame.DataFrame.assign
  - pandas.core.frame.DataFrame.get
  - pandas.core.frame.DataFrame.to\_numpy
  - pandas.core.indexes.base.Index.is\_unique
  - pandas.core.indexes.base.Index.has\_duplicates
  - pandas.core.indexes.base.Index.shape
  - pandas.core.indexes.base.Index.array
  - pandas.core.indexes.base.Index.str
  - pandas.core.indexes.base.Index.equals
  - pandas.core.indexes.base.Index.identical
  - pandas.core.indexes.base.Index.unique

Added support to the following Spark Scala functions:

- org.apache.spark.sql.functions.format\_number
- org.apache.spark.sql.functions.from\_unixtime
- org.apache.spark.sql.functions.instr
- org.apache.spark.sql.functions.months\_between
- org.apache.spark.sql.functions.pow
- org.apache.spark.sql.functions.to\_unix\_timestamp
- org.apache.spark.sql.Row.getAs

#### Changed

- Bumped the version of Snowpark Pandas API supported by the SMA to 1.33.0.
- Bumped the version of Snowpark Scala API supported by the SMA to 1.16.0.
- Updated the mapping status of pyspark.sql.group.GroupedData.pivot from Transformation to Direct.
- Updated the mapping status of org.apache.spark.sql.Builder.master from NotSupported to Transformation. This transformation removes all the identified usages of this element during code conversion.
- Updated the mapping status of org.apache.spark.sql.types.StructType.fieldIndex from NotSupported to Direct.
- Updated the mapping status of org.apache.spark.sql.Row.fieldIndex from NotSupported to Direct.
- Updated the mapping status of org.apache.spark.sql.SparkSession.stop from NotSupported to Rename. All the identified usages of this element are renamed to com.snowflake.snowpark.Session.close during code conversion.
- Updated the mapping status of org.apache.spark.sql.DataFrame.unpersist and org.apache.spark.sql.Dataset.unpersist from NotSupported to Transformation. This transformation removes all the identified usages of this element during code conversion.

#### Fixed

- Fixed continuation backslash on removed tailed functions.
- Fix the LIBRARY\_PREFIX column in the ConversionStatusLibraries.csv file to use the right identifier for scikit-learn library family (scikit-\*).
- Fixed bug not parsing multiline grouped operations.

## Version 2.7.6 (Jul 17, 2025)

### Included SMA Core Versions

- Snowpark Conversion Core 8.0.30

#### Added

- Adjusted mappings for spark.DataReader methods.
- `DataFrame.union` is now `DataFrame.unionAll`.
- `DataFrame.unionByName` is now `DataFrame.unionAllByName`.
- Added multi-level artifact dependency columns in artifact inventory
- Added new Pandas EWIs documentation, from `PNDSPY1005` to `PNDSPY1010`.
- Added a specific EWI for `pandas.core.series.Series.apply`.

#### Changed

- Bumped the version of Snowpark Pandas API supported by the SMA from `1.27.0` to `1.30.0`.

#### Fixed

- Fixed an issue with missing values in the formula to get the SQL readiness score.
- Fixed a bug that was causing some Pandas elements to have the default EWI message from PySpark.

## Version 2.7.5 (Jul 2, 2025)

### Application & CLI Version 2.7.5

#### Included SMA Core Versions

- Snowpark Conversion Core 8.0.19

#### Changed

- **Refactored Pandas Imports:** Pandas imports now use `modin.pandas` instead of `snowflake.snowpark.modin.pandas`.
- **Improved dbutils and Magic Commands Transformation:**
  - A new `sfutils.py` file is now generated, and all `dbutils` prefixes are replaced with `sfutils`.
  - For Databricks (DBX) notebooks, an implicit import for `sfutils` is automatically added.
  - The `sfutils` module simulates various `dbutils` methods, including file system operations (`dbutils.fs`) via a defined Snowflake FileSystem (SFFS) stage, and handles notebook execution (`dbutils.notebook.run`) by transforming it to `EXECUTE NOTEBOOK` SQL functions.
  - `dbutils.notebook.exit` is removed as it is not required in Snowflake.

#### Fixed

- **Updates in SnowConvert Reports:** SnowConvert reports now include the *CellId* column when instances originate from SMA, and the *FileName* column displays the full path.
- **Updated Artifacts Dependency for SnowConvert Reports:** The SMA’s artifact inventory report, which was previously impacted by the integration of SnowConvert, has been restored. This update enables the SMA tool to accurately capture and analyze *Object References* and *Missing Object References* directly from SnowConvert reports, thereby ensuring the correct retrieval of SQL dependencies for the inventory.

## Version 2.7.4 (Jun 26, 2025)

### Application & CLI Version 2.7.4

**Desktop App**

#### Added

- Added telemetry improvements.

#### Fixed

- Fix documentation links in conversion settings pop-up and Pandas EWIs.

#### Included SMA Core Versions

- Snowpark Conversion Core 8.0.16

#### Added

- Transforming Spark XML to Snowpark
- Databricks SQL option in the SQL source language
- Transform JDBC read connections.

#### Changed

- All the SnowConvert reports are copied to the backup Zip file.
- The folder is renamed from `SqlReports` to `SnowConvertReports`.
- `SqlFunctionsInventory` is moved to the folder `Reports`.
- All the SnowConvert Reports are sent to Telemetry.

#### Fixed

- Non-deterministic issue with SQL Readiness Score.
- Fixed a false-positive critical result that made the desktop crash.
- Fixed issue causing the Artifacts dependency report not to show the SQL objects.

## Version 2.7.2 (Jun 10, 2025)

### Application & CLI Version 2.7.2

### Included SMA Core Versions

- Snowpark Conversion Core 8.0.2

#### Fixed

- Addressed an issue with SMA execution on the latest Windows OS, as previously reported. This fix resolves the issues encountered in version 2.7.1.

## Version 2.7.1 (Jun 9, 2025)

### Application & CLI Version 2.7.1

#### Included SMA Core Versions

- Snowpark Conversion Core 8.0.1

#### Added

The Snowpark Migration Accelerator (SMA) now orchestrates [SnowConvert](https://docs.snowconvert.com/sc/general/about) to process SQL found in user workloads, including embedded SQL in Python / Scala code, Notebook SQL cells, `.sql` files, and `.hql` files.

The SnowConvert now enhances the previous SMA capabilities:

- [Spark SQL](https://docs.snowconvert.com/sc/translation-references/spark-dbx)

A new folder in the Reports called SQL Reports contains the reports generated by SnowConvert.

#### Known Issues

The previous SMA version for SQL reports will appear empty for the following:

- For `Reports/SqlElementsInventory.csv`, partially covered by the `Reports/SqlReports/Elements.yyyymmdd.hhmmss.csv.`
- For `Reports/SqlFunctionsInventory.csv` refer to the new location with the same name at `Reports/SqlReports/SqlFunctionsInventory.csv`

The artifact dependency inventory:

- In the `ArtifactDependencyInventory` the column for the SQL Object will appear empty

## Version 2.6.10 (May 5, 2025)

### Application & CLI Version 2.6.10

#### Included SMA Core Versions

- Snowpark Conversion Core 7.4.0

#### Fixed

- Fixed wrong values in the ‘checkpoints.json’ file.

  - The ‘sample’ value was without decimals (for integer values) and quotes.
  - The ‘entryPoint’ value had dots instead of slashes and was missing the file extension.
- Updated the default value to TRUE for the setting ‘Convert DBX notebooks to Snowflake notebooks’

## Version 2.6.8 (Apr 28, 2025)

### Application & CLI Version 2.6.8

#### Desktop App

- Added checkpoints execution settings mechanism recognition.
- Added a mechanism to collect DBX magic commands into DbxElementsInventory.csv
- Added ‘checkpoints.json’ generation into the input directory.
- Added a new EWI for all not supported magic command.
- Added the collection of dbutils into DbxElementsInventory.csv from scala source notebooks

#### Included SMA Core Versions

- Snowpark Conversion Core 7.2.53

#### Changed

- Updates made to handle transformations from DBX Scala elements to Jupyter Python elements, and to comment the entire code from the cell.
- Updates made to handle transformations from dbutils.notebook.run and “r” commands, for the last one, also comment out the entire code from the cell.
- Updated the name and the letter of the key to make the conversion of the notebook files.

#### Fixed

- Fixed the bug that was causing the transformation of DBX notebooks into .ipynb files to have the wrong format.
- Fixed the bug that was causing .py DBX notebooks to not be transformable into .ipynb files.
- Fixed a bug that was causing comments to be missing in the output code of DBX notebooks.
- Fixed a bug that was causing raw Scala files to be converted into ipynb files.

## Version 2.6.7 (Apr 21, 2025)

### Application & CLI Version 2.6.7

#### Included SMA Core Versions

- Snowpark Conversion Core 7.2.42

#### Changed

Updated DataFramesInventory to fill EntryPoints column

## Version 2.6.6 (Apr 7, 2025)

### Application & CLI Version 2.6.6

#### Desktop App

#### Added

- Update DBx EWI link in the UI results page

#### Included SMA Core Versions

- Snowpark Conversion Core 7.2.39

#### Added

- Added Execution Flow inventory generation.
- Added implicit session setup in every DBx notebook transformation

#### Changed

- Renamed the DbUtilsUsagesInventory.csv to DbxElementsInventory.csv

#### Fixed

- Fixed a bug that caused a Parsing error when a backslash came after a type hint.
- Fixed relative imports that do not start with a dot and relative imports with a star.

## Version 2.6.5 (Mar 27, 2025)

### Application & CLI Version 2.6.5

#### Desktop App

#### Added

- Added a new conversion setting toggle to enable or disable Sma-Checkpoints feature.
- Fix report issue to not crash when post api returns 500

#### Included SMA Core Versions

- Snowpark Conversion Core 7.2.26

#### Added

- Added generation of the checkpoints.json file into the output folder based on the DataFramesInventory.csv.
- Added “disableCheckpoints” flag into the CLI commands and additional parameters of the code processor.
- Added a new replacer for Python to transform the dbutils.notebook.run node.
- Added new replacers to transform the magic %run command.
- Added new replacers (Python and Scala) to remove the dbutils.notebook.exit node.
- Added Location column to artifacts inventory.

#### Changed

- Refactored the normalized directory separator used in some parts of the solution.
- Centralized the DBC extraction working folder name handling.
- Updated Snowpark and Pandas version to v1.27.0
- Updated the artifacts inventory columns to:

  - Name -> Dependency
  - File -> FileId
  - Status -> Status\_detail
- Added new column to the artifacts inventory:

  - Success

#### Fixed

- Dataframes inventory was not being uploaded to the stage correctly.

## Version 2.6.4 (Mar 12, 2025)

### Application & CLI Version 2.6.4

#### Included SMA Core Versions

- Snowpark Conversion Core 7.2.0

#### Added

- An Artifact Dependency Inventory
- A replacer and EWI for pyspark.sql.types.StructType.fieldNames method to snowflake.snowpark.types.StructType.fieldNames attribute.
- The following **PySpark** functions with the status:

Direct Status

- `pyspark.sql.functions.bitmap_bit_position`
- `pyspark.sql.functions.bitmap_bucket_number`
- `pyspark.sql.functions.bitmap_construct_agg`
- `pyspark.sql.functions.equal_null`
- `pyspark.sql.functions.ifnull`
- `pyspark.sql.functions.localtimestamp`
- `pyspark.sql.functions.max_by`
- `pyspark.sql.functions.min_by`
- `pyspark.sql.functions.nvl`
- `pyspark.sql.functions.regr_avgx`
- `pyspark.sql.functions.regr_avgy`
- `pyspark.sql.functions.regr_count`
- `pyspark.sql.functions.regr_intercept`
- `pyspark.sql.functions.regr_slope`
- `pyspark.sql.functions.regr_sxx`
- `pyspark.sql.functions.regr_sxy`
- `pyspark.sql.functions.regr`

NotSupported

- `pyspark.sql.functions.map_contains_key`
- `pyspark.sql.functions.position`
- `pyspark.sql.functions.regr_r2`
- `pyspark.sql.functions.try_to_binary`

The following **Pandas** functions with status

- `pandas.core.series.Series.str.ljust`
- `pandas.core.series.Series.str.center`
- `pandas.core.series.Series.str.pad`
- `pandas.core.series.Series.str.rjust`

Update the following **Pyspark** functions with the status

From WorkAround to Direct

- `pyspark.sql.functions.acosh`
- `pyspark.sql.functions.asinh`
- `pyspark.sql.functions.atanh`
- `pyspark.sql.functions.instr`
- `pyspark.sql.functions.log10`
- `pyspark.sql.functions.log1p`
- `pyspark.sql.functions.log2`

From NotSupported to Direct

- `pyspark.sql.functions.bit_length`
- `pyspark.sql.functions.cbrt`
- `pyspark.sql.functions.nth_value`
- `pyspark.sql.functions.octet_length`
- `pyspark.sql.functions.base64`
- `pyspark.sql.functions.unbase64`

Updated the following **Pandas** functions with the status

From NotSupported to Direct

- `pandas.core.frame.DataFrame.pop`
- `pandas.core.series.Series.between`
- `pandas.core.series.Series.pop`

## Version 2.6.3 (Mar 6, 2025)

### Application & CLI Version 2.6.3

#### Included SMA Core Versions

- Snowpark Conversion Core 7.1.13

#### Added

- Added csv generator class for new inventory creation.
- Added “full\_name” column to import usages inventory.
- Added transformation from pyspark.sql.functions.concat\_ws to snowflake.snowpark.functions.\_concat\_ws\_ignore\_nulls.
- Added logic for generation of checkpoints.json.
- Added the inventories:
  - DataFramesInventory.csv.
  - CheckpointsInventory.csv

## Version 2.6.0 (Feb 21, 2025)

### Application & CLI Version 2.6.0

#### Desktop App

- Updated the licensing agreement, acceptance is required.

#### Included SMA Core Versions

- Snowpark Conversion Core 7.1.2

Added

Updated the mapping status for the following PySpark elements, from `NotSupported` to `Direct`

- `pyspark.sql.types.ArrayType.json`
- `pyspark.sql.types.ArrayType.jsonValue`
- `pyspark.sql.types.ArrayType.simpleString`
- `pyspark.sql.types.ArrayType.typeName`
- `pyspark.sql.types.AtomicType.json`
- `pyspark.sql.types.AtomicType.jsonValue`
- `pyspark.sql.types.AtomicType.simpleString`
- `pyspark.sql.types.AtomicType.typeName`
- `pyspark.sql.types.BinaryType.json`
- `pyspark.sql.types.BinaryType.jsonValue`
- `pyspark.sql.types.BinaryType.simpleString`
- `pyspark.sql.types.BinaryType.typeName`
- `pyspark.sql.types.BooleanType.json`
- `pyspark.sql.types.BooleanType.jsonValue`
- `pyspark.sql.types.BooleanType.simpleString`
- `pyspark.sql.types.BooleanType.typeName`
- `pyspark.sql.types.ByteType.json`
- `pyspark.sql.types.ByteType.jsonValue`
- `pyspark.sql.types.ByteType.simpleString`
- `pyspark.sql.types.ByteType.typeName`
- `pyspark.sql.types.DecimalType.json`
- `pyspark.sql.types.DecimalType.jsonValue`
- `pyspark.sql.types.DecimalType.simpleString`
- `pyspark.sql.types.DecimalType.typeName`
- `pyspark.sql.types.DoubleType.json`
- `pyspark.sql.types.DoubleType.jsonValue`
- `pyspark.sql.types.DoubleType.simpleString`
- `pyspark.sql.types.DoubleType.typeName`
- `pyspark.sql.types.FloatType.json`
- `pyspark.sql.types.FloatType.jsonValue`
- `pyspark.sql.types.FloatType.simpleString`
- `pyspark.sql.types.FloatType.typeName`
- `pyspark.sql.types.FractionalType.json`
- `pyspark.sql.types.FractionalType.jsonValue`
- `pyspark.sql.types.FractionalType.simpleString`
- `pyspark.sql.types.FractionalType.typeName`
- `pyspark.sql.types.IntegerType.json`
- `pyspark.sql.types.IntegerType.jsonValue`
- `pyspark.sql.types.IntegerType.simpleString`
- `pyspark.sql.types.IntegerType.typeName`
- `pyspark.sql.types.IntegralType.json`
- `pyspark.sql.types.IntegralType.jsonValue`
- `pyspark.sql.types.IntegralType.simpleString`
- `pyspark.sql.types.IntegralType.typeName`
- `pyspark.sql.types.LongType.json`
- `pyspark.sql.types.LongType.jsonValue`
- `pyspark.sql.types.LongType.simpleString`
- `pyspark.sql.types.LongType.typeName`
- `pyspark.sql.types.MapType.json`
- `pyspark.sql.types.MapType.jsonValue`
- `pyspark.sql.types.MapType.simpleString`
- `pyspark.sql.types.MapType.typeName`
- `pyspark.sql.types.NullType.json`
- `pyspark.sql.types.NullType.jsonValue`
- `pyspark.sql.types.NullType.simpleString`
- `pyspark.sql.types.NullType.typeName`
- `pyspark.sql.types.NumericType.json`
- `pyspark.sql.types.NumericType.jsonValue`
- `pyspark.sql.types.NumericType.simpleString`
- `pyspark.sql.types.NumericType.typeName`
- `pyspark.sql.types.ShortType.json`
- `pyspark.sql.types.ShortType.jsonValue`
- `pyspark.sql.types.ShortType.simpleString`
- `pyspark.sql.types.ShortType.typeName`
- `pyspark.sql.types.StringType.json`
- `pyspark.sql.types.StringType.jsonValue`
- `pyspark.sql.types.StringType.simpleString`
- `pyspark.sql.types.StringType.typeName`
- `pyspark.sql.types.StructType.json`
- `pyspark.sql.types.StructType.jsonValue`
- `pyspark.sql.types.StructType.simpleString`
- `pyspark.sql.types.StructType.typeName`
- `pyspark.sql.types.TimestampType.json`
- `pyspark.sql.types.TimestampType.jsonValue`
- `pyspark.sql.types.TimestampType.simpleString`
- `pyspark.sql.types.TimestampType.typeName`
- `pyspark.sql.types.StructField.simpleString`
- `pyspark.sql.types.StructField.typeName`
- `pyspark.sql.types.StructField.json`
- `pyspark.sql.types.StructField.jsonValue`
- `pyspark.sql.types.DataType.json`
- `pyspark.sql.types.DataType.jsonValue`
- `pyspark.sql.types.DataType.simpleString`
- `pyspark.sql.types.DataType.typeName`
- `pyspark.sql.session.SparkSession.getActiveSession`
- `pyspark.sql.session.SparkSession.version`
- `pandas.io.html.read_html`
- `pandas.io.json._normalize.json_normalize`
- `pyspark.sql.types.ArrayType.fromJson`
- `pyspark.sql.types.MapType.fromJson`
- `pyspark.sql.types.StructField.fromJson`
- `pyspark.sql.types.StructType.fromJson`
- `pandas.core.groupby.generic.DataFrameGroupBy.pct_change`
- `pandas.core.groupby.generic.SeriesGroupBy.pct_change`

Updated the mapping status for the following Pandas elements, from `NotSupported` to `Direct`

- `pandas.io.html.read_html`
- `pandas.io.json._normalize.json_normalize`
- `pandas.core.groupby.generic.DataFrameGroupBy.pct_change`
- `pandas.core.groupby.generic.SeriesGroupBy.pct_change`

Updated the mapping status for the following PySpark elements, from `Rename` to `Direct`

- `pyspark.sql.functions.collect_list`
- `pyspark.sql.functions.size`

#### Fixed

- Standardized the format of the version number in the inventories.

## Version 2.5.2 (Feb 5, 2025)

### Hotfix: Application & CLI Version 2.5.2

### Desktop App

- Fixed an issue when converting in the sample project option.

### Included SMA Core Versions

- Snowpark Conversion Core 5.3.0

## Version 2.5.1 (Feb 4, 2025)

### Application & CLI Version 2.5.1

### Desktop App

- Added a new modal when the user does not have write permission.
- Updated the licensing agreement, acceptance is required.

### CLI

- Fixed the year in the CLI screen when showing “–version” or “-v”

### Included SMA Core Versions included-sma-core-versions

- Snowpark Conversion Core 5.3.0

#### Added

Added the following Python Third-Party libraries with Direct status:

- `about-time`
- `affinegap`
- `aiohappyeyeballs`
- `alibi-detect`
- `alive-progress`
- `allure-nose2`
- `allure-robotframework`
- `anaconda-cloud-cli`
- `anaconda-mirror`
- `astropy-iers-data`
- `asynch`
- `asyncssh`
- `autots`
- `autoviml`
- `aws-msk-iam-sasl-signer-python`
- `azure-functions`
- `backports.tarfile`
- `blas`
- `bottle`
- `bson`
- `cairo`
- `capnproto`
- `captum`
- `categorical-distance`
- `census`
- `clickhouse-driver`
- `clustergram`
- `cma`
- `conda-anaconda-telemetry`
- `configspace`
- `cpp-expected`
- `dask-expr`
- `data-science-utils`
- `databricks-sdk`
- `datetime-distance`
- `db-dtypes`
- `dedupe`
- `dedupe-variable-datetime`
- `dedupe_lehvenshtein_search`
- `dedupe_levenshtein_search`
- `diff-cover`
- `diptest`
- `dmglib`
- `docstring_parser`
- `doublemetaphone`
- `dspy-ai`
- `econml`
- `emcee`
- `emoji`
- `environs`
- `eth-abi`
- `eth-hash`
- `eth-typing`
- `eth-utils`
- `expat`
- `filetype`
- `fitter`
- `flask-cors`
- `fpdf2`
- `frozendict`
- `gcab`
- `geojson`
- `gettext`
- `glib-tools`
- `google-ads`
- `google-ai-generativelanguage`
- `google-api-python-client`
- `google-auth-httplib2`
- `google-cloud-bigquery`
- `google-cloud-bigquery-core`
- `google-cloud-bigquery-storage`
- `google-cloud-bigquery-storage-core`
- `google-cloud-resource-manager`
- `google-generativeai`
- `googlemaps`
- `grapheme`
- `graphene`
- `graphql-relay`
- `gravis`
- `greykite`
- `grpc-google-iam-v1`
- `harfbuzz`
- `hatch-fancy-pypi-readme`
- `haversine`
- `hiclass`
- `hicolor-icon-theme`
- `highered`
- `hmmlearn`
- `holidays-ext`
- `httplib2`
- `icu`
- `imbalanced-ensemble`
- `immutabledict`
- `importlib-metadata`
- `importlib-resources`
- `inquirerpy`
- `iterative-telemetry`
- `jaraco.context`
- `jaraco.test`
- `jiter`
- `jiwer`
- `joserfc`
- `jsoncpp`
- `jsonpath`
- `jsonpath-ng`
- `jsonpath-python`
- `kagglehub`
- `keplergl`
- `kt-legacy`
- `langchain-community`
- `langchain-experimental`
- `langchain-snowflake`
- `langchain-text-splitters`
- `libabseil`
- `libflac`
- `libgfortran-ng`
- `libgfortran5`
- `libglib`
- `libgomp`
- `libgrpc`
- `libgsf`
- `libmagic`
- `libogg`
- `libopenblas`
- `libpostal`
- `libprotobuf`
- `libsentencepiece`
- `libsndfile`
- `libstdcxx-ng`
- `libtheora`
- `libtiff`
- `libvorbis`
- `libwebp`
- `lightweight-mmm`
- `litestar`
- `litestar-with-annotated-types`
- `litestar-with-attrs`
- `litestar-with-cryptography`
- `litestar-with-jinja`
- `litestar-with-jwt`
- `litestar-with-prometheus`
- `litestar-with-structlog`
- `lunarcalendar-ext`
- `matplotlib-venn`
- `metricks`
- `mimesis`
- `modin-ray`
- `momepy`
- `mpg123`
- `msgspec`
- `msgspec-toml`
- `msgspec-yaml`
- `msitools`
- `multipart`
- `namex`
- `nbconvert-all`
- `nbconvert-core`
- `nbconvert-pandoc`
- `nlohmann_json`
- `numba-cuda`
- `numpyro`
- `office365-rest-python-client`
- `openapi-pydantic`
- `opentelemetry-distro`
- `opentelemetry-instrumentation`
- `opentelemetry-instrumentation-system-metrics`
- `optree`
- `osmnx`
- `pathlib`
- `pdf2image`
- `pfzy`
- `pgpy`
- `plumbum`
- `pm4py`
- `polars`
- `polyfactory`
- `poppler-cpp`
- `postal`
- `pre-commit`
- `prompt-toolkit`
- `propcache`
- `py-partiql-parser`
- `py_stringmatching`
- `pyatlan`
- `pyfakefs`
- `pyfhel`
- `pyhacrf-datamade`
- `pyiceberg`
- `pykrb5`
- `pylbfgs`
- `pymilvus`
- `pymoo`
- `pynisher`
- `pyomo`
- `pypdf`
- `pypdf-with-crypto`
- `pypdf-with-full`
- `pypdf-with-image`
- `pypng`
- `pyprind`
- `pyrfr`
- `pysoundfile`
- `pytest-codspeed`
- `pytest-trio`
- `python-barcode`
- `python-box`
- `python-docx`
- `python-gssapi`
- `python-iso639`
- `python-magic`
- `python-pandoc`
- `python-zstd`
- `pyuca`
- `pyvinecopulib`
- `pyxirr`
- `qrcode`
- `rai-sdk`
- `ray-client`
- `ray-observability`
- `readline`
- `rich-click`
- `rouge-score`
- `ruff`
- `scikit-criteria`
- `scikit-mobility`
- `sentencepiece-python`
- `sentencepiece-spm`
- `setuptools-markdown`
- `setuptools-scm`
- `setuptools-scm-git-archive`
- `shareplum`
- `simdjson`
- `simplecosine`
- `sis-extras`
- `slack-sdk`
- `smac`
- `snowflake-sqlalchemy`
- `snowflake_legacy`
- `socrata-py`
- `spdlog`
- `sphinxcontrib-images`
- `sphinxcontrib-jquery`
- `sphinxcontrib-youtube`
- `splunk-opentelemetry`
- `sqlfluff`
- `squarify`
- `st-theme`
- `statistics`
- `streamlit-antd-components`
- `streamlit-condition-tree`
- `streamlit-echarts`
- `streamlit-feedback`
- `streamlit-keplergl`
- `streamlit-mermaid`
- `streamlit-navigation-bar`
- `streamlit-option-menu`
- `strictyaml`
- `stringdist`
- `sybil`
- `tensorflow-cpu`
- `tensorflow-text`
- `tiledb-ptorchaudio`
- `torcheval`
- `trio-websocket`
- `trulens-connectors-snowflake`
- `trulens-core`
- `trulens-dashboard`
- `trulens-feedback`
- `trulens-otel-semconv`
- `trulens-providers-cortex`
- `tsdownsample`
- `typing`
- `typing-extensions`
- `typing_extensions`
- `unittest-xml-reporting`
- `uritemplate`
- `us`
- `uuid6`
- `wfdb`
- `wsproto`
- `zlib`
- `zope.index`

Added the following Python BuiltIn libraries with Direct status:

- `aifc`
- `array`
- `ast`
- `asynchat`
- `asyncio`
- `asyncore`
- `atexit`
- `audioop`
- `base64`
- `bdb`
- `binascii`
- `bisect`
- `builtins`
- `bz2`
- `calendar`
- `cgi`
- `cgitb`
- `chunk`
- `cmath`
- `cmd`
- `code`
- `codecs`
- `codeop`
- `colorsys`
- `compileall`
- `concurrent`
- `contextlib`
- `contextvars`
- `copy`
- `copyreg`
- `cprofile`
- `crypt`
- `csv`
- `ctypes`
- `curses`
- `dbm`
- `difflib`
- `dis`
- `distutils`
- `doctest`
- `email`
- `ensurepip`
- `enum`
- `errno`
- `faulthandler`
- `fcntl`
- `filecmp`
- `fileinput`
- `fnmatch`
- `fractions`
- `ftplib`
- `functools`
- `gc`
- `getopt`
- `getpass`
- `gettext`
- `graphlib`
- `grp`
- `gzip`
- `hashlib`
- `heapq`
- `hmac`
- `html`
- `http`
- `idlelib`
- `imaplib`
- `imghdr`
- `imp`
- `importlib`
- `inspect`
- `ipaddress`
- `itertools`
- `keyword`
- `linecache`
- `locale`
- `lzma`
- `mailbox`
- `mailcap`
- `marshal`
- `math`
- `mimetypes`
- `mmap`
- `modulefinder`
- `msilib`
- `multiprocessing`
- `netrc`
- `nis`
- `nntplib`
- `numbers`
- `operator`
- `optparse`
- `ossaudiodev`
- `pdb`
- `pickle`
- `pickletools`
- `pipes`
- `pkgutil`
- `platform`
- `plistlib`
- `poplib`
- `posix`
- `pprint`
- `profile`
- `pstats`
- `pty`
- `pwd`
- `py_compile`
- `pyclbr`
- `pydoc`
- `queue`
- `quopri`
- `random`
- `re`
- `reprlib`
- `resource`
- `rlcompleter`
- `runpy`
- `sched`
- `secrets`
- `select`
- `selectors`
- `shelve`
- `shlex`
- `signal`
- `site`
- `sitecustomize`
- `smtpd`
- `smtplib`
- `sndhdr`
- `socket`
- `socketserver`
- `spwd`
- `sqlite3`
- `ssl`
- `stat`
- `string`
- `stringprep`
- `struct`
- `subprocess`
- `sunau`
- `symtable`
- `sysconfig`
- `syslog`
- `tabnanny`
- `tarfile`
- `telnetlib`
- `tempfile`
- `termios`
- `test`
- `textwrap`
- `threading`
- `timeit`
- `tkinter`
- `token`
- `tokenize`
- `tomllib`
- `trace`
- `traceback`
- `tracemalloc`
- `tty`
- `turtle`
- `turtledemo`
- `types`
- `unicodedata`
- `urllib`
- `uu`
- `uuid`
- `venv`
- `warnings`
- `wave`
- `weakref`
- `webbrowser`
- `wsgiref`
- `xdrlib`
- `xml`
- `xmlrpc`
- `zipapp`
- `zipfile`
- `zipimport`
- `zoneinfo`

Added the following Python BuiltIn libraries with NotSupported status:

- `msvcrt`
- `winreg`
- `winsound`

#### Changed

- Update .NET version to v9.0.0.
- Improved EWI SPRKPY1068.
- Bumped the version of Snowpark Python API supported by the SMA from 1.24.0 to 1.25.0.
- Updated the detailed report template, now has the Snowpark version for Pandas.
- Changed the following libraries from **ThirdPartyLib** to **BuiltIn**.
  - `configparser`
  - `dataclasses`
  - `pathlib`
  - `readline`
  - `statistics`
  - `zlib`

Updated the mapping status for the following Pandas elements, from Direct to Partial:

- `pandas.core.frame.DataFrame.add`
- `pandas.core.frame.DataFrame.aggregate`
- `pandas.core.frame.DataFrame.all`
- `pandas.core.frame.DataFrame.apply`
- `pandas.core.frame.DataFrame.astype`
- `pandas.core.frame.DataFrame.cumsum`
- `pandas.core.frame.DataFrame.div`
- `pandas.core.frame.DataFrame.dropna`
- `pandas.core.frame.DataFrame.eq`
- `pandas.core.frame.DataFrame.ffill`
- `pandas.core.frame.DataFrame.fillna`
- `pandas.core.frame.DataFrame.floordiv`
- `pandas.core.frame.DataFrame.ge`
- `pandas.core.frame.DataFrame.groupby`
- `pandas.core.frame.DataFrame.gt`
- `pandas.core.frame.DataFrame.idxmax`
- `pandas.core.frame.DataFrame.idxmin`
- `pandas.core.frame.DataFrame.inf`
- `pandas.core.frame.DataFrame.join`
- `pandas.core.frame.DataFrame.le`
- `pandas.core.frame.DataFrame.loc`
- `pandas.core.frame.DataFrame.lt`
- `pandas.core.frame.DataFrame.mask`
- `pandas.core.frame.DataFrame.merge`
- `pandas.core.frame.DataFrame.mod`
- `pandas.core.frame.DataFrame.mul`
- `pandas.core.frame.DataFrame.ne`
- `pandas.core.frame.DataFrame.nunique`
- `pandas.core.frame.DataFrame.pivot_table`
- `pandas.core.frame.DataFrame.pow`
- `pandas.core.frame.DataFrame.radd`
- `pandas.core.frame.DataFrame.rank`
- `pandas.core.frame.DataFrame.rdiv`
- `pandas.core.frame.DataFrame.rename`
- `pandas.core.frame.DataFrame.replace`
- `pandas.core.frame.DataFrame.resample`
- `pandas.core.frame.DataFrame.rfloordiv`
- `pandas.core.frame.DataFrame.rmod`
- `pandas.core.frame.DataFrame.rmul`
- `pandas.core.frame.DataFrame.rolling`
- `pandas.core.frame.DataFrame.round`
- `pandas.core.frame.DataFrame.rpow`
- `pandas.core.frame.DataFrame.rsub`
- `pandas.core.frame.DataFrame.rtruediv`
- `pandas.core.frame.DataFrame.shift`
- `pandas.core.frame.DataFrame.skew`
- `pandas.core.frame.DataFrame.sort_index`
- `pandas.core.frame.DataFrame.sort_values`
- `pandas.core.frame.DataFrame.sub`
- `pandas.core.frame.DataFrame.to_dict`
- `pandas.core.frame.DataFrame.transform`
- `pandas.core.frame.DataFrame.transpose`
- `pandas.core.frame.DataFrame.truediv`
- `pandas.core.frame.DataFrame.var`
- `pandas.core.indexes.datetimes.date_range`
- `pandas.core.reshape.concat.concat`
- `pandas.core.reshape.melt.melt`
- `pandas.core.reshape.merge.merge`
- `pandas.core.reshape.pivot.pivot_table`
- `pandas.core.reshape.tile.cut`
- `pandas.core.series.Series.add`
- `pandas.core.series.Series.aggregate`
- `pandas.core.series.Series.all`
- `pandas.core.series.Series.any`
- `pandas.core.series.Series.cumsum`
- `pandas.core.series.Series.div`
- `pandas.core.series.Series.dropna`
- `pandas.core.series.Series.eq`
- `pandas.core.series.Series.ffill`
- `pandas.core.series.Series.fillna`
- `pandas.core.series.Series.floordiv`
- `pandas.core.series.Series.ge`
- `pandas.core.series.Series.gt`
- `pandas.core.series.Series.lt`
- `pandas.core.series.Series.mask`
- `pandas.core.series.Series.mod`
- `pandas.core.series.Series.mul`
- `pandas.core.series.Series.multiply`
- `pandas.core.series.Series.ne`
- `pandas.core.series.Series.pow`
- `pandas.core.series.Series.quantile`
- `pandas.core.series.Series.radd`
- `pandas.core.series.Series.rank`
- `pandas.core.series.Series.rdiv`
- `pandas.core.series.Series.rename`
- `pandas.core.series.Series.replace`
- `pandas.core.series.Series.resample`
- `pandas.core.series.Series.rfloordiv`
- `pandas.core.series.Series.rmod`
- `pandas.core.series.Series.rmul`
- `pandas.core.series.Series.rolling`
- `pandas.core.series.Series.rpow`
- `pandas.core.series.Series.rsub`
- `pandas.core.series.Series.rtruediv`
- `pandas.core.series.Series.sample`
- `pandas.core.series.Series.shift`
- `pandas.core.series.Series.skew`
- `pandas.core.series.Series.sort_index`
- `pandas.core.series.Series.sort_values`
- `pandas.core.series.Series.std`
- `pandas.core.series.Series.sub`
- `pandas.core.series.Series.subtract`
- `pandas.core.series.Series.truediv`
- `pandas.core.series.Series.value_counts`
- `pandas.core.series.Series.var`
- `pandas.core.series.Series.where`
- `pandas.core.tools.numeric.to_numeric`

Updated the mapping status for the following Pandas elements, from NotSupported to Direct:

- `pandas.core.frame.DataFrame.attrs`
- `pandas.core.indexes.base.Index.to_numpy`
- `pandas.core.series.Series.str.len`
- `pandas.io.html.read_html`
- `pandas.io.xml.read_xml`
- `pandas.core.indexes.datetimes.DatetimeIndex.mean`
- `pandas.core.resample.Resampler.indices`
- `pandas.core.resample.Resampler.nunique`
- `pandas.core.series.Series.items`
- `pandas.core.tools.datetimes.to_datetime`
- `pandas.io.sas.sasreader.read_sas`
- `pandas.core.frame.DataFrame.attrs`
- `pandas.core.frame.DataFrame.style`
- `pandas.core.frame.DataFrame.items`
- `pandas.core.groupby.generic.DataFrameGroupBy.head`
- `pandas.core.groupby.generic.DataFrameGroupBy.median`
- `pandas.core.groupby.generic.DataFrameGroupBy.min`
- `pandas.core.groupby.generic.DataFrameGroupBy.nunique`
- `pandas.core.groupby.generic.DataFrameGroupBy.tail`
- `pandas.core.indexes.base.Index.is_boolean`
- `pandas.core.indexes.base.Index.is_floating`
- `pandas.core.indexes.base.Index.is_integer`
- `pandas.core.indexes.base.Index.is_monotonic_decreasing`
- `pandas.core.indexes.base.Index.is_monotonic_increasing`
- `pandas.core.indexes.base.Index.is_numeric`
- `pandas.core.indexes.base.Index.is_object`
- `pandas.core.indexes.base.Index.max`
- `pandas.core.indexes.base.Index.min`
- `pandas.core.indexes.base.Index.name`
- `pandas.core.indexes.base.Index.names`
- `pandas.core.indexes.base.Index.rename`
- `pandas.core.indexes.base.Index.set_names`
- `pandas.core.indexes.datetimes.DatetimeIndex.day_name`
- `pandas.core.indexes.datetimes.DatetimeIndex.month_name`
- `pandas.core.indexes.datetimes.DatetimeIndex.time`
- `pandas.core.indexes.timedeltas.TimedeltaIndex.ceil`
- `pandas.core.indexes.timedeltas.TimedeltaIndex.days`
- `pandas.core.indexes.timedeltas.TimedeltaIndex.floor`
- `pandas.core.indexes.timedeltas.TimedeltaIndex.microseconds`
- `pandas.core.indexes.timedeltas.TimedeltaIndex.nanoseconds`
- `pandas.core.indexes.timedeltas.TimedeltaIndex.round`
- `pandas.core.indexes.timedeltas.TimedeltaIndex.seconds`
- `pandas.core.reshape.pivot.crosstab`
- `pandas.core.series.Series.dt.round`
- `pandas.core.series.Series.dt.time`
- `pandas.core.series.Series.dt.weekday`
- `pandas.core.series.Series.is_monotonic_decreasing`
- `pandas.core.series.Series.is_monotonic_increasing`

Updated the mapping status for the following Pandas elements, from NotSupported to Partial:

- `pandas.core.frame.DataFrame.align`
- `pandas.core.series.Series.align`
- `pandas.core.frame.DataFrame.tz_convert`
- `pandas.core.frame.DataFrame.tz_localize`
- `pandas.core.groupby.generic.DataFrameGroupBy.fillna`
- `pandas.core.groupby.generic.SeriesGroupBy.fillna`
- `pandas.core.indexes.datetimes.bdate_range`
- `pandas.core.indexes.datetimes.DatetimeIndex.std`
- `pandas.core.indexes.timedeltas.TimedeltaIndex.mean`
- `pandas.core.resample.Resampler.asfreq`
- `pandas.core.resample.Resampler.quantile`
- `pandas.core.series.Series.map`
- `pandas.core.series.Series.tz_convert`
- `pandas.core.series.Series.tz_localize`
- `pandas.core.window.expanding.Expanding.count`
- `pandas.core.window.rolling.Rolling.count`
- `pandas.core.groupby.generic.DataFrameGroupBy.aggregate`
- `pandas.core.groupby.generic.SeriesGroupBy.aggregate`
- `pandas.core.frame.DataFrame.applymap`
- `pandas.core.series.Series.apply`
- `pandas.core.groupby.generic.DataFrameGroupBy.bfill`
- `pandas.core.groupby.generic.DataFrameGroupBy.ffill`
- `pandas.core.groupby.generic.SeriesGroupBy.bfill`
- `pandas.core.groupby.generic.SeriesGroupBy.ffill`
- `pandas.core.frame.DataFrame.backfill`
- `pandas.core.frame.DataFrame.bfill`
- `pandas.core.frame.DataFrame.compare`
- `pandas.core.frame.DataFrame.unstack`
- `pandas.core.frame.DataFrame.asfreq`
- `pandas.core.series.Series.backfill`
- `pandas.core.series.Series.bfill`
- `pandas.core.series.Series.compare`
- `pandas.core.series.Series.unstack`
- `pandas.core.series.Series.asfreq`
- `pandas.core.series.Series.argmax`
- `pandas.core.series.Series.argmin`
- `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.microsecond`
- `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.nanosecond`
- `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.day_name`
- `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.month_name`
- `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.month_start`
- `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.month_end`
- `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.is_year_start`
- `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.is_year_end`
- `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.is_quarter_start`
- `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.is_quarter_end`
- `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.is_leap_year`
- `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.floor`
- `pandas.core.indexes.accessors.CombinedDatetimelikeProperties.ceil`
- `pandas.core.groupby.generic.DataFrameGroupBy.idxmax`
- `pandas.core.groupby.generic.DataFrameGroupBy.idxmin`
- `pandas.core.groupby.generic.DataFrameGroupBy.std`
- `pandas.core.indexes.timedeltas.TimedeltaIndex.mean`
- `pandas.core.tools.timedeltas.to_timedelta`

#### Known Issue

- **This version includes an issue when converting the sample project will not work on this version, it** will be fixed on the next release

## Version 2.4.3 (Jan 9, 2025)

### Application & CLI Version 2.4.3

#### Desktop App

- Added link to the troubleshooting guide in the crash report modal.

#### Included SMA Core Versions

- Snowpark Conversion Core 4.15.0

#### Added

- Added the following PySpark elements to ConversionStatusPySpark.csv file as `NotSupported:`
  - `pyspark.sql.streaming.readwriter.DataStreamReader.table`
  - `pyspark.sql.streaming.readwriter.DataStreamReader.schema`
  - `pyspark.sql.streaming.readwriter.DataStreamReader.options`
  - `pyspark.sql.streaming.readwriter.DataStreamReader.option`
  - `pyspark.sql.streaming.readwriter.DataStreamReader.load`
  - `pyspark.sql.streaming.readwriter.DataStreamReader.format`
  - `pyspark.sql.streaming.query.StreamingQuery.awaitTermination`
  - `pyspark.sql.streaming.readwriter.DataStreamWriter.partitionBy`
  - `pyspark.sql.streaming.readwriter.DataStreamWriter.toTable`
  - `pyspark.sql.streaming.readwriter.DataStreamWriter.trigger`
  - `pyspark.sql.streaming.readwriter.DataStreamWriter.queryName`
  - `pyspark.sql.streaming.readwriter.DataStreamWriter.outputMode`
  - `pyspark.sql.streaming.readwriter.DataStreamWriter.format`
  - `pyspark.sql.streaming.readwriter.DataStreamWriter.option`
  - `pyspark.sql.streaming.readwriter.DataStreamWriter.foreachBatch`
  - `pyspark.sql.streaming.readwriter.DataStreamWriter.start`

#### Changed

- Updated Hive SQL EWIs format.

  - SPRKHVSQL1001
  - SPRKHVSQL1002
  - SPRKHVSQL1003
  - SPRKHVSQL1004
  - SPRKHVSQL1005
  - SPRKHVSQL1006
- Updated Spark SQL EWIs format.

  - SPRKSPSQL1001
  - SPRKSPSQL1002
  - SPRKSPSQL1003
  - SPRKSPSQL1004
  - SPRKSPSQL1005
  - SPRKSPSQL1006

#### Fixed

- Fixed a bug that was causing some PySpark elements to not be identified by the tool.
- Fixed the mismatch in the ThirdParty identified calls and the ThirdParty import Calls number.

## Version 2.4.2 (Dec 13, 2024)

### Application & CLI **Version 2.4.2**

#### Included SMA Core Versions

- Snowpark Conversion Core 4.14.0

#### Added added

- Added the following Spark elements to ConversionStatusPySpark.csv:
  - `pyspark.broadcast.Broadcast.value`
  - `pyspark.conf.SparkConf.getAll`
  - `pyspark.conf.SparkConf.setAll`
  - `pyspark.conf.SparkConf.setMaster`
  - `pyspark.context.SparkContext.addFile`
  - `pyspark.context.SparkContext.addPyFile`
  - `pyspark.context.SparkContext.binaryFiles`
  - `pyspark.context.SparkContext.setSystemProperty`
  - `pyspark.context.SparkContext.version`
  - `pyspark.files.SparkFiles`
  - `pyspark.files.SparkFiles.get`
  - `pyspark.rdd.RDD.count`
  - `pyspark.rdd.RDD.distinct`
  - `pyspark.rdd.RDD.reduceByKey`
  - `pyspark.rdd.RDD.saveAsTextFile`
  - `pyspark.rdd.RDD.take`
  - `pyspark.rdd.RDD.zipWithIndex`
  - `pyspark.sql.context.SQLContext.udf`
  - `pyspark.sql.types.StructType.simpleString`

#### Changed

- Updated the documentation of the Pandas EWIs, `PNDSPY1001`, `PNDSPY1002` and `PNDSPY1003` `SPRKSCL1137` to align with a standardized format, ensuring consistency and clarity across all the EWIs.
- Updated the documentation of the following Scala EWIs: `SPRKSCL1106` and `SPRKSCL1107`. To be aligned with a standardized format, ensuring consistency and clarity across all the EWIs.

#### Fixed

- Fixed the bug that was causing the UserDefined symbols showing in the third party usages inventory.

## Version 2.4.1 (Dec 4, 2024)

### Application & CLI **Version 2.4.1**

#### Included SMA Core Versions

- Snowpark Conversion Core 4.13.1

#### Command Line Interface

**Changed**

- Added timestamp to the output folder.

### Snowpark Conversion Core 4.13.1

#### Added

- Added ‘Source Language’ column to Library Mappings Table
- Added `Others` as a new category in the Pandas API Summary table of the DetailedReport.docx

#### Changed

- Updated the documentation for Python EWI `SPRKPY1058`.
- Updated the message for the pandas EWI `PNDSPY1002` to show the related pandas element.
- Updated the way we created the .csv reports, now are overwritten after a second run .

#### Fixed

- Fixed a bug that was causing Notebook files not being generated in the output.
- Fixed the replacer for `get` and `set` methods from `pyspark.sql.conf.RuntimeConfig`, the replacer now match the correct full names.
- Fixed query tag incorrect version.
- Fixed UserDefined packages reported as ThirdPartyLib.

## Version 2.3.1 (Nov 14, 2024)

### Application & CLI **Version 2.3.1**

#### Included SMA Core Versions

- Snowpark Conversion Core 4.12.0

#### Desktop App

**Fixed**

- Fix case-sensitive issues in –sql options.

**Removed**

- Remove platform name from show-ac message.

### Snowpark Conversion Core 4.12.0

#### Added

- Added support for Snowpark Python 1.23.0 and 1.24.0.
- Added a new EWI for the `pyspark.sql.dataframe.DataFrame.writeTo` function. All the usages of this function will now have the EWI SPRKPY1087.

#### Changed

- Updated the documentation of the Scala EWIs from `SPRKSCL1137` to `SPRKSCL1156` to align with a standardized format, ensuring consistency and clarity across all the EWIs.
- Updated the documentation of the Scala EWIs from `SPRKSCL1117` to `SPRKSCL1136` to align with a standardized format, ensuring consistency and clarity across all the EWIs.
- Updated the message that is shown for the following EWIs:

  - SPRKPY1082
  - SPRKPY1083
- Updated the documentation of the Scala EWIs from `SPRKSCL1100` to `SPRKSCL1105`, from `SPRKSCL1108` to `SPRKSCL1116`; from `SPRKSCL1157` to `SPRKSCL1175`; to align with a standardized format, ensuring consistency and clarity across all the EWIs.
- Updated the mapping status of the following PySpark elements from **NotSupported** to **Direct** with EWI:

  - `pyspark.sql.readwriter.DataFrameWriter.option` => `snowflake.snowpark.DataFrameWriter.option`: All the usages of this function now have the EWI SPRKPY1088
  - `pyspark.sql.readwriter.DataFrameWriter.options` => `snowflake.snowpark.DataFrameWriter.options`: All the usages of this function now have the EWI SPRKPY1089
- Updated the mapping status of the following PySpark elements from **Workaround** to **Rename**:

  - `pyspark.sql.readwriter.DataFrameWriter.partitionBy` => `snowflake.snowpark.DataFrameWriter.partition_by`
- Updated EWI documentation: SPRKSCL1000, SPRKSCL1001, SPRKSCL1002, SPRKSCL1100, SPRKSCL1101, SPRKSCL1102, SPRKSCL1103, SPRKSCL1104, SPRKSCL1105.

#### Removed

- Removed the `pyspark.sql.dataframe.DataFrameStatFunctions.writeTo` element from the conversion status, this element does not exist.

#### Deprecated

- Deprecated the following EWI codes:
  - SPRKPY1081
  - SPRKPY1084

## Version 2.3.0 (Oct 30, 2024)

### Application & CLI Version 2.3.0

- Snowpark Conversion Core 4.11.0

### Snowpark Conversion Core 4.11.0

#### Added

- Added a new column called `Url` to the `Issues.csv` file, which redirects to the corresponding EWI documentation.
- Added new EWIs for the following Spark elements:

  - [SPRKPY1082] pyspark.sql.readwriter.DataFrameReader.load
  - [SPRKPY1083] pyspark.sql.readwriter.DataFrameWriter.save
  - [SPRKPY1084] pyspark.sql.readwriter.DataFrameWriter.option
  - [SPRKPY1085] pyspark.ml.feature.VectorAssembler
  - [SPRKPY1086] pyspark.ml.linalg.VectorUDT
- Added 38 new Pandas elements:

  - pandas.core.frame.DataFrame.select
  - `pandas.core.frame.DataFrame.str`
  - pandas.core.frame.DataFrame.str.replace
  - pandas.core.frame.DataFrame.str.upper
  - pandas.core.frame.DataFrame.to\_list
  - pandas.core.frame.DataFrame.tolist
  - pandas.core.frame.DataFrame.unique
  - pandas.core.frame.DataFrame.values.tolist
  - pandas.core.frame.DataFrame.withColumn
  - pandas.core.groupby.generic.\_SeriesGroupByScalar
  - pandas.core.groupby.generic.\_SeriesGroupByScalar[S1].agg
  - pandas.core.groupby.generic.\_SeriesGroupByScalar[S1].aggregate
  - pandas.core.indexes.datetimes.DatetimeIndex.year
  - pandas.core.series.Series.columns
  - pandas.core.tools.datetimes.to\_datetime.date
  - pandas.core.tools.datetimes.to\_datetime.dt.strftime
  - pandas.core.tools.datetimes.to\_datetime.strftime
  - pandas.io.parsers.readers.TextFileReader.apply
  - pandas.io.parsers.readers.TextFileReader.astype
  - pandas.io.parsers.readers.TextFileReader.columns
  - pandas.io.parsers.readers.TextFileReader.copy
  - pandas.io.parsers.readers.TextFileReader.drop
  - pandas.io.parsers.readers.TextFileReader.drop\_duplicates
  - pandas.io.parsers.readers.TextFileReader.fillna
  - pandas.io.parsers.readers.TextFileReader.groupby
  - pandas.io.parsers.readers.TextFileReader.head
  - pandas.io.parsers.readers.TextFileReader.iloc
  - pandas.io.parsers.readers.TextFileReader.isin
  - pandas.io.parsers.readers.TextFileReader.iterrows
  - pandas.io.parsers.readers.TextFileReader.loc
  - pandas.io.parsers.readers.TextFileReader.merge
  - pandas.io.parsers.readers.TextFileReader.rename
  - pandas.io.parsers.readers.TextFileReader.shape
  - pandas.io.parsers.readers.TextFileReader.to\_csv
  - pandas.io.parsers.readers.TextFileReader.to\_excel
  - pandas.io.parsers.readers.TextFileReader.unique
  - pandas.io.parsers.readers.TextFileReader.values
  - pandas.tseries.offsets

## Version 2.2.3 (Oct 24, 2024)

### Application Version 2.2.3

#### Included SMA Core Versions

- Snowpark Conversion Core 4.10.0

#### Desktop App

#### Fixed

- Fixed a bug that caused the SMA to show the label **SnowConvert** instead of **Snowpark Migration Accelerator** in the menu bar of the Windows version.
- Fixed a bug that caused the SMA to crash when it did not have read and write permissions to the `.config` directory in macOS and the `AppData` directory in Windows.

#### Command Line Interface

**Changed**

- Renamed the CLI executable name from `snowct` to `sma`.
- Removed the source language argument so you no longer need to specify if you are running a Python or Scala assessment / conversion.
- Expanded the command line arguments supported by the CLI by adding the following new arguments:

  - `--enableJupyter` | `-j`: Flag to indicate if the conversion of Databricks notebooks to Jupyter is enabled or not.
  - `--sql` | `-f`: Database engine syntax to be used when a SQL command is detected.
  - `--customerEmail` | `-e`: Configure the customer email.
  - `--customerCompany` | `-c`: Configure the customer company.
  - `--projectName` | `-p`: Configure the customer project.
- Updated some texts to reflect the correct name of the application, ensuring consistency and clarity in all the messages.
- Updated the terms of use of the application.
- Updated and expanded the documentation of the CLI to reflect the latest features, enhancements and changes.
- Updated the text that is shown before proceeding with the execution of the SMA to improve the user experience.
- Updated the CLI to accept **“Yes”** as a valid argument when prompting for user confirmation.
- Allowed the CLI to continue the execution without waiting for user interaction by specifying the argument `-y` or `--yes`.
- Updated the help information of the `--sql` argument to show the values that this argument expects.

### Snowpark Conversion Core Version 4.10.0

#### Added

- Added a new EWI for the `pyspark.sql.readwriter.DataFrameWriter.partitionBy` function. All the usages of this function will now have the EWI SPRKPY1081.
- Added a new column called `Technology` to the `ImportUsagesInventory.csv` file.

#### Changed

- Updated the Third-Party Libraries readiness score to also take into account the `Unknown` libraries.
- Updated the `AssessmentFiles.zip` file to include `.json` files instead of `.pam` files.
- Improved the CSV to JSON conversion mechanism to make processing of inventories more performant.
- Improved the documentation of the following EWIs:

  - SPRKPY1029
  - SPRKPY1054
  - SPRKPY1055
  - SPRKPY1063
  - SPRKPY1075
  - SPRKPY1076
- Updated the mapping status of the following Spark Scala elements from `Direct` to `Rename`.

  - `org.apache.spark.sql.functions.shiftLeft` => `com.snowflake.snowpark.functions.shiftleft`
  - `org.apache.spark.sql.functions.shiftRight` => `com.snowflake.snowpark.functions.shiftright`
- Updated the mapping status of the following Spark Scala elements from `Not Supported` to `Direct`.

  - `org.apache.spark.sql.functions.shiftleft` => `com.snowflake.snowpark.functions.shiftleft`
  - `org.apache.spark.sql.functions.shiftright` => `com.snowflake.snowpark.functions.shiftright`

#### Fixed

- Fixed a bug that caused the SMA to incorrectly populate the `Origin` column of the `ImportUsagesInventory.csv` file.
- Fixed a bug that caused the SMA to not classify imports of the libraries `io`, `json`, `logging` and `unittest` as Python built-in imports in the `ImportUsagesInventory.csv` file and in the `DetailedReport.docx` file.

## Version 2.2.2 (Oct 11, 2024)

### Application Version 2.2.2

Features Updates include:

- Snowpark Conversion Core 4.8.0

### Snowpark Conversion Core Version 4.8.0

#### Added

- Added `EwiCatalog.csv` and .md files to reorganize documentation
- Added the mapping status of `pyspark.sql.functions.ln` Direct.
- Added a transformation for `pyspark.context.SparkContext.getOrCreate`

  - Check the EWI SPRKPY1080 for further details.
- Added an improvement for the SymbolTable, infer type for parameters in functions.
- Added SymbolTable supports static methods and do not assume the first parameter will be self for them.
- Added documentation for missing EWIs

  - SPRKHVSQL1005
  - SPRKHVSQL1006
  - SPRKSPSQL1005
  - SPRKSPSQL1006
  - SPRKSCL1002
  - SPRKSCL1170
  - SPRKSCL1171
  - SPRKPY1057
  - SPRKPY1058
  - SPRKPY1059
  - SPRKPY1060
  - SPRKPY1061
  - SPRKPY1064
  - SPRKPY1065
  - SPRKPY1066
  - SPRKPY1067
  - SPRKPY1069
  - SPRKPY1070
  - SPRKPY1077
  - SPRKPY1078
  - SPRKPY1079
  - SPRKPY1101

#### Changed

- Updated the mapping status of:
  - `pyspark.sql.functions.array_remove` from `NotSupported` to `Direct`.

#### Fixed

- Fixed the Code File Sizing table in the Detail Report to exclude .sql and .hql files and added the Extra Large row in the table.
- Fixed missing the `update_query_tag` when `SparkSession` is defined into multiple lines on `Python`.
- Fixed missing the `update_query_tag` when `SparkSession` is defined into multiple lines on `Scala`.
- Fixed missing EWI `SPRKHVSQL1001` to some SQL statements with parsing errors.
- Fixed keep new lines values inside string literals
- Fixed the Total Lines of code showed in the File Type Summary Table
- Fixed Parsing Score showed as 0 when recognize files successfully
- Fixed LOC count in the cell inventory for Databricks Magic SQL Cells

## Version 2.2.0 (Sep 26, 2024)

### Application Version 2.2.0

Feature Updates include:

- Snowpark Conversion Core 4.6.0

### Snowpark Conversion Core Version 4.6.0

#### Added

- Add transformation for `pyspark.sql.readwriter.DataFrameReader.parquet`.
- Add transformation for `pyspark.sql.readwriter.DataFrameReader.option` when it is a Parquet method.

#### Changed

- Updated the mapping status of:

  - `pyspark.sql.types.StructType.fields` from `NotSupported` to `Direct`.
  - `pyspark.sql.types.StructType.names` from `NotSupported` to `Direct`.
  - `pyspark.context.SparkContext.setLogLevel` from `Workaround` to `Transformation`.
    - More detail can be found in EWIs SPRKPY1078 and SPRKPY1079
  - `org.apache.spark.sql.functions.round` from `WorkAround` to `Direct`.
  - `org.apache.spark.sql.functions.udf` from `NotDefined` to `Transformation`.
    - More detail can be found in EWIs SPRKSCL1174 and SPRKSCL1175
- Updated the mapping status of the following Spark elements from `DirectHelper` to `Direct`:

  - `org.apache.spark.sql.functions.hex`
  - `org.apache.spark.sql.functions.unhex`
  - `org.apache.spark.sql.functions.shiftleft`
  - `org.apache.spark.sql.functions.shiftright`
  - `org.apache.spark.sql.functions.reverse`
  - `org.apache.spark.sql.functions.isnull`
  - `org.apache.spark.sql.functions.unix_timestamp`
  - `org.apache.spark.sql.functions.randn`
  - `org.apache.spark.sql.functions.signum`
  - `org.apache.spark.sql.functions.sign`
  - `org.apache.spark.sql.functions.collect_list`
  - `org.apache.spark.sql.functions.log10`
  - `org.apache.spark.sql.functions.log1p`
  - `org.apache.spark.sql.functions.base64`
  - `org.apache.spark.sql.functions.unbase64`
  - `org.apache.spark.sql.functions.regexp_extract`
  - `org.apache.spark.sql.functions.expr`
  - `org.apache.spark.sql.functions.date_format`
  - `org.apache.spark.sql.functions.desc`
  - `org.apache.spark.sql.functions.asc`
  - `org.apache.spark.sql.functions.size`
  - `org.apache.spark.sql.functions.locate`
  - `org.apache.spark.sql.functions.ntile`

#### Fixed

- Fixed value showed in the Percentage of total Pandas Api
- Fixed Total percentage on ImportCalls table in the DetailReport

### Deprecated

- Deprecated the following EWI code:
  - SPRKSCL1115

## Version 2.1.7 (Sep 12, 2024)

### Application Version 2.1.7

Feature Updates include:

- Snowpark Conversion Core 4.5.7
- Snowpark Conversion Core 4.5.2

### Snowpark Conversion Core Version 4.5.7

#### Hotfixed

- Fixed Total row added on Spark Usages Summaries when there are not usages
- Bumped of Python Assembly to Version `1.3.111`
  - Parse trail comma in multiline arguments

### Snowpark Conversion Core Version 4.5.2

#### Added

- Added transformation for `pyspark.sql.readwriter.DataFrameReader.option`:

  - When the chain is from a CSV method call.
  - When the chain is from a JSON method call.
- Added transformation for `pyspark.sql.readwriter.DataFrameReader.json`.

#### Changed

- Executed SMA on SQL strings passed to Python/Scala functions

  - Create AST in Scala/Python to emit temporary SQL unit
  - Create SqlEmbeddedUsages.csv inventory
  - Deprecate SqlStatementsInventory.csv and SqlExtractionInventory.csv
  - Integrate EWI when the SQL literal could not be processed
  - Create new task to process SQL-embedded code
  - Collect info for SqlEmbeddedUsages.csv inventory in Python
  - Replace SQL transformed code to Literal in Python
  - Update test cases after implementation
  - Create table, views for telemetry in SqlEmbeddedUsages inventory
  - Collect info for SqlEmbeddedUsages.csv report in Scala
  - Replace SQL transformed code to Literal in Scala
  - Check line number order for Embedded SQL reporting
- Filled the `SqlFunctionsInfo.csv` with the SQL functions documented for SparkSQL and HiveSQL
- Updated the mapping status for:

  - `org.apache.spark.sql.SparkSession.sparkContext` from NotSupported to Transformation.
  - `org.apache.spark.sql.Builder.config` from `NotSupported` to `Transformation`. With this new mapping status, the SMA will remove all the usages of this function from the source code.

## Version 2.1.6 (Sep 5, 2024)

### Application Version 2.1.6

- Hotfix change for Snowpark Engines Core version 4.5.1

### Spark Conversion Core Version 4.5.1

**Hotfix**

- Added a mechanism to convert the temporal Databricks notebooks generated by SMA in exported Databricks notebooks

## Version 2.1.5 (Aug 29, 2024)

### Application Version 2.1.5

Feature Updates include:

- Updated Spark Conversion Core: 4.3.2

### Spark Conversion Core Version 4.3.2

#### Added

- Added the mechanism (via decoration) to get the line and the column of the elements identified in notebooks cells
- Added an EWI for pyspark.sql.functions.from\_json.
- Added a transformation for pyspark.sql.readwriter.DataFrameReader.csv.
- Enabled the query tag mechanism for Scala files.
- Added the Code Analysis Score and additional links to the Detailed Report.
- Added a column called OriginFilePath to InputFilesInventory.csv

#### Changed

- Updated the mapping status of pyspark.sql.functions.from\_json from Not Supported to Transformation.
- Updated the mapping status of the following Spark elements from Workaround to Direct:
  - org.apache.spark.sql.functions.countDistinct
  - org.apache.spark.sql.functions.max
  - org.apache.spark.sql.functions.min
  - org.apache.spark.sql.functions.mean

#### Deprecated

- Deprecated the following EWI codes:
  - SPRKSCL1135
  - SPRKSCL1136
  - SPRKSCL1153
  - SPRKSCL1155

#### Fixed

- Fixed a bug that caused an incorrect calculation of the Spark API score.
- Fixed an error that avoid copy SQL empty or commented files in the output folder.
- Fixed a bug in the DetailedReport, the notebook stats LOC and Cell count is not accurate.

## Version 2.1.2 (Aug 14, 2024)

### Application Version 2.1.2

Feature Updates include:

- Updated Spark Conversion Core: 4.2.0

### Spark Conversion Core Version 4.2.0

#### Added

- Add technology column to SparkUsagesInventory
- Added an EWI for not defined SQL elements .
- Added SqlFunctions Inventory
- Collect info for SqlFunctions Inventory

#### Changed

- The engine now processes and prints partially parsed Python files instead of leaving original file without modifications.
- Python notebook cells that have parsing errors will also be processed and printed.

#### Fixed

- Fixed `pandas.core.indexes.datetimes.DatetimeIndex.strftime` was being reported wrongly.
- Fix mismatch between SQL readiness score and SQL Usages by Support Status.
- Fixed a bug that caused the SMA to report `pandas.core.series.Series.empty` with an incorrect mapping status.
- Fix mismatch between Spark API Usages Ready for Conversion in DetailedReport.docx is different than UsagesReadyForConversion row in Assessment.json.

## Version 2.1.1 (Aug 8, 2024)

### Application Version 2.1.1

Feature Updates include:

- Updated Spark Conversion Core: 4.1.0

### Spark Conversion Core Version 4.1.0

#### Added

- Added the following information to the `AssessmentReport.json` file

  - The third-party libraries readiness score.
  - The number of third-party library calls that were identified.
  - The number of third-party library calls that are supported in Snowpark.
  - The color code associated with the third-party readiness score, the Spark API readiness score, and the SQL readiness score.
- Transformed `SqlSimpleDataType` in Spark create tables.
- Added the mapping of `pyspark.sql.functions.get` as direct.
- Added the mapping of `pyspark.sql.functions.to_varchar` as direct.
- As part of the changes after unification, the tool now generates an execution info file in the Engine.
- Added a replacer for `pyspark.sql.SparkSession.builder.appName`.

#### Changed

- Updated the mapping status for the following Spark elements

  - From Not Supported to Direct mapping:
    - `pyspark.sql.functions.sign`
    - `pyspark.sql.functions.signum`
- Changed the Notebook Cells Inventory report to indicate the kind of content for every cell in the column Element
- Added a `SCALA_READINESS_SCORE` column that reports the readiness score as related only to references to the Spark API in Scala files.
- Partial support to transform table properties in `ALTER TABLE` and `ALTER VIEW`
- Updated the conversion status of the node `SqlSimpleDataType` from Pending to Transformation in Spark create tables
- Updated the version of the Snowpark Scala API supported by the SMA from `1.7.0` to `1.12.1`:

  - Updated the mapping status of:
    - `org.apache.spark.sql.SparkSession.getOrCreate` from Rename to Direct
    - `org.apache.spark.sql.functions.sum` from Workaround to Direct
- Updated the version of the Snowpark Python API supported by the SMA from `1.15.0` to `1.20.0`:

  - Updated the mapping status of:
    - `pyspark.sql.functions.arrays_zip` from Not Supported to Direct
- Updated the mapping status for the following Pandas elements:

  - Direct mappings:
    - `pandas.core.frame.DataFrame.any`
    - `pandas.core.frame.DataFrame.applymap`
- Updated the mapping status for the following Pandas elements:

  - From Not Supported to Direct mapping:
    - `pandas.core.frame.DataFrame.groupby`
    - `pandas.core.frame.DataFrame.index`
    - `pandas.core.frame.DataFrame.T`
    - `pandas.core.frame.DataFrame.to_dict`
  - From Not Supported to Rename mapping:
    - `pandas.core.frame.DataFrame.map`
- Updated the mapping status for the following Pandas elements:

  - Direct mappings:
    - `pandas.core.frame.DataFrame.where`
    - `pandas.core.groupby.generic.SeriesGroupBy.agg`
    - `pandas.core.groupby.generic.SeriesGroupBy.aggregate`
    - `pandas.core.groupby.generic.DataFrameGroupBy.agg`
    - `pandas.core.groupby.generic.DataFrameGroupBy.aggregate`
    - `pandas.core.groupby.generic.DataFrameGroupBy.apply`
  - Not Supported mappings:
    - `pandas.core.frame.DataFrame.to_parquet`
    - `pandas.core.generic.NDFrame.to_csv`
    - `pandas.core.generic.NDFrame.to_excel`
    - `pandas.core.generic.NDFrame.to_sql`
- Updated the mapping status for the following Pandas elements:

  - Direct mappings:
    - `pandas.core.series.Series.empty`
    - `pandas.core.series.Series.apply`
    - `pandas.core.reshape.tile.qcut`
  - Direct mappings with EWI:
    - `pandas.core.series.Series.fillna`
    - `pandas.core.series.Series.astype`
    - `pandas.core.reshape.melt.melt`
    - `pandas.core.reshape.tile.cut`
    - `pandas.core.reshape.pivot.pivot_table`
- Updated the mapping status for the following Pandas elements:

  - Direct mappings:
    - `pandas.core.series.Series.dt`
    - `pandas.core.series.Series.groupby`
    - `pandas.core.series.Series.loc`
    - `pandas.core.series.Series.shape`
    - `pandas.core.tools.datetimes.to_datetime`
    - `pandas.io.excel._base.ExcelFile`
  - Not Supported mappings:
    - `pandas.core.series.Series.dt.strftime`
- Updated the mapping status for the following Pandas elements:

  - From Not Supported to Direct mapping:
    - `pandas.io.parquet.read_parquet`
    - `pandas.io.parsers.readers.read_csv`
- Updated the mapping status for the following Pandas elements:

  - From Not Supported to Direct mapping:
    - `pandas.io.pickle.read_pickle`
    - `pandas.io.sql.read_sql`
    - `pandas.io.sql.read_sql_query`
- Updated the description of Understanding the SQL Readiness Score.
- Updated `PyProgramCollector` to collect the packages and populate the current packages inventory with data from Python source code.
- Updated the mapping status of `pyspark.sql.SparkSession.builder.appName` from Rename to Transformation.
- Removed the following Scala integration tests:

  - `AssessmentReportTest_AssessmentMode.ValidateReports_AssessmentMode`
  - `AssessmentReportTest_PythonAndScala_Files.ValidateReports_PythonAndScala`
  - `AssessmentReportTestWithoutSparkUsages.ValidateReports_WithoutSparkUsages`
- Updated the mapping status of `pandas.core.generic.NDFrame.shape` from Not Supported to Direct.
- Updated the mapping status of `pandas.core.series` from Not Supported to Direct.

#### Deprecated

- Deprecated the EWI code `SPRKSCL1160` since `org.apache.spark.sql.functions.sum` is now a direct mapping.

#### Fixed

- Fixed a bug by not supporting Custom Magics without arguments in Jupyter Notebook cells.
- Fixed incorrect generation of EWIs in the issues.csv report when parsing errors occur.
- Fixed a bug that caused the SMA not to process the Databricks exported notebook as Databricks notebooks.
- Fixed a stack overflow error while processing clashing type names of declarations created inside package objects.
- Fixed the processing of complex lambda type names involving generics, e.g., `def func[X,Y](f: (Map[Option[X], Y] => Map[Y, X]))...`
- Fixed a bug that caused the SMA to add a PySpark EWI code instead of a Pandas EWI code to the Pandas elements that are not yet recognized.
- Fixed a typo in the detailed report template: renaming a column from “Percentage of all Python Files” to “Percentage of all files”.
- Fixed a bug where `pandas.core.series.Series.shape` was wrongly reported.

# SnowConvert AI - File Extension Validation

## Description

This validation step verifies the file extensions. These are the valid file extensions:

- All the languages (.sql)
- Teradata (.ddl, .dml, .bteq, .btq, .fl, .fload, .ml, .mld, .mload, .tp, .tpump, .tpt)
- Hive (.hql)

Warning

**IMPORTANT**! Uppercase file extensions are also invalid.

If one of the files has an invalid extension, the following warning is displayed:

[![File's Extension Validation Failed](/static/images/migrations/sc-assets/image(10).png "image")](/static/images/migrations/sc-assets/image(10).png)

Also, in the ScopeValidation report, you will find information about the failed file(s).

[![ScopeValidation.csv report](/static/images/migrations/sc-assets/image(11).png "image")](/static/images/migrations/sc-assets/image(11).png)

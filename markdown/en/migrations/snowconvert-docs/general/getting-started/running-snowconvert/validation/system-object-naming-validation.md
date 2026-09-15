# SnowConvert AI - System Object Naming Validation

## Description

This validation step verifies the files and folder names that contain reserved words. These files and folders are marked as invalid or out of scope because they can potentially be built-in systems definitions that must be removed from the migration scope. When this behavior happens, the following warning is displayed:

[![System Object Naming Validation Failed](/static/images/migrations/sc-assets/image(14).png "image")](/static/images/migrations/sc-assets/image(14).png)

Also, in the ScopeValidation report, you will find information about the failed file(s).

[![ScopeValidation.csv](/static/images/migrations/sc-assets/image(16).png "image")](/static/images/migrations/sc-assets/image(16).png)

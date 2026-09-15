# SnowConvert AI - File Encoding Validation

## Description

This validation step tries to recognize the file’s encoding; if not, it is marked as invalid. If it is recognized as different from the encoding selected in the Assessment or Conversion configuration process, the file will also be marked as invalid.

Warning

**IMPORTANT**! The entry code files should contain the [BOM](https://en.wikipedia.org/wiki/Byte_order_mark) signature to recognize the file’s encoding.

If this validation step fails, the following warning is displayed:

[![File's Encoding Validation Failed](/static/images/migrations/sc-assets/image(12).png "image")](/static/images/migrations/sc-assets/image(12).png)

Also, in the ScopeValidation report, you will find information about the failed file(s).

[![ScopeValidation.csv report](/static/images/migrations/sc-assets/Screenshot2024-08-13at4.29.07PM.png "image")](/static/images/migrations/sc-assets/Screenshot2024-08-13at4.29.07PM.png)

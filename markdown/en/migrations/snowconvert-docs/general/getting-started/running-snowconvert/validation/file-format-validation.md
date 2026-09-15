# SnowConvert AI - File Format Validation

## Description

This validation step verifies the file’s structure and indentation. If the average number of characters per line across all input code files is greater than the maximum allowed, the following warning is displayed:

[![File Format Validation Failed](/static/images/migrations/sc-assets/image(20).png "image")](/static/images/migrations/sc-assets/image(20).png)

Copy code

```
CREATE TABLE LongLines(

    COL1                                                                                                                                                                                                                                                                                                                                                                                                                                                    VARCHAR(22331) -- this line has more than 500 characters
);
```

Note

Please scroll to the right to watch all the sample code

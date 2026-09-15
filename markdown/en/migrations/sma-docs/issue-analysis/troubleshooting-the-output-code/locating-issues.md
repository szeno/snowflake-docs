description:
:   Oh where… oh where… is my issue!

# Snowpark Migration Accelerator: Locating Issues

The Snowpark Migration Accelerator (SMA) converts code where possible and identifies sections it cannot convert. When SMA encounters code it cannot convert, it generates an issue with a specific issue code. Let’s explore how to locate these issues.

Use the [Issues Inventory file](/migrations/sma-docs/user-guide/scos-conversion/output-reports/sma-inventories) from your local output to review identified issues.

[![Mapping issue locations](/static/images/migrations/sma-assets/image(529).png)](/static/images/migrations/sma-assets/image(529).png)

The Issues Inventory provides extensive information, but these key fields are essential for locating specific issues:

- Issue Code: The unique identifier assigned to the issue
- Description: A detailed explanation of the problem
- Issue Category: The type or classification of the issue
- Filename: The specific file where the issue was found
- Line Number: The exact location in the file where the issue occurred

The issue code and description will be included as comments in the generated code.

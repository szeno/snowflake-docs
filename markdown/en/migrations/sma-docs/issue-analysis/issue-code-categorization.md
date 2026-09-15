description:
:   What kind of issue codes does the SMA generate?

# Snowpark Migration Accelerator: Issue Code Categorization

The Snowpark Migration Accelerator (SMA) analyzes your codebase and generates issue codes. While these codes provide detailed information, they fall into three main categories.

## Parsing Error

A parsing error occurs when SMA cannot understand or process a section of your source code. This happens when SMA encounters code that it either doesn’t recognize or considers invalid. These errors typically stem from one of two sources:

1. An issue within the SMA tool itself
2. Problems in your source code

This type of error can occur for various reasons.

- **Invalid Source Code**: The code must be executable in the source platform. If you provide code snippets or partial code that cannot run independently in the source platform, SMA will not be able to parse them.
- **Circular Dependencies**: When analyzing large codebases, SMA may encounter circular references between code elements. This can cause the tool to skip or fail to parse some of these interdependent references.
- **New Code Patterns**: While SMA is regularly updated, source platforms also evolve continuously. There might be cases where newly introduced code patterns are not yet supported by the tool.
- **Encoding Issues**: If your source code contains inconsistent encoding or unexpected characters at the beginning or end of files, SMA may generate parsing errors, even if the code runs successfully in the source platform.

When parsing errors occur, they are identified by specific error codes. To understand what these codes mean and how they relate to parsing errors, refer to [the issue codes by source section](/migrations/sma-docs/issue-analysis/issue-codes-by-source/README) in our documentation.

## Conversion Error

A conversion error happens when SMA successfully identifies the code but is unable to convert it. Unlike parsing errors, conversion errors do not indicate problems with your source code. Instead, they show that SMA is working as intended by identifying code segments that are beyond its conversion capabilities.

There are several common reasons why code cannot be converted. These include:

- **The element from the source code cannot be implemented in Snowflake**. Currently, there is no equivalent functionality available in Snowflake for this source code element.
- **The specific usage of an element is not supported in Snowflake**. While Snowflake may support a particular element from the source platform, the way it’s being used in the source code is not compatible with Snowflake’s implementation.
- **Required parameters are not supported**. SMA creates a detailed functional model of the source code by analyzing how each element is used, rather than just identifying and categorizing elements. Sometimes, essential function parameters from the source code don’t have corresponding support in Snowflake.
- **Certain function combinations are incompatible**. SMA’s functional model analyzes how functions work together. Even when individual functions are supported in Snowflake, their combined usage might not be possible. In such cases, SMA will flag this as a conversion error.

Most error messages include specific recommendations or next steps to help you resolve the conversion issue. You can find these suggestions on the corresponding error page.

When SMA encounters a conversion error, it adds an EWI (Error, Warning, Info) comment in the converted code and records the error in [the issues inventory file](/migrations/sma-docs/user-guide/scos-conversion/output-reports/sma-inventories). The system will then:

- Add a comment symbol to the line containing the conversion error.
- Keep the line uncommented to prevent the file from executing.

When encountering conversion errors, each error has a unique error code. To understand what these codes mean and how to resolve them, refer to [the issue codes by source section](/migrations/sma-docs/issue-analysis/issue-codes-by-source/README) in our documentation.

## Warning

A warning differs from an error in SMA. Warnings appear when the tool detects changes that you should be aware of. While these changes won’t prevent your code from running, they indicate that certain aspects of your code may look or behave differently in the converted output compared to the source code.

Common reasons for warning messages:

- **The code appears different**. SMA performs transformations that generate an EWI (Error, Warning, or Information) message.
- **Some specific scenarios may not convert successfully**. The tool will generate a warning if a particular feature works in 99.9% of test cases but fails in certain parameter combinations. If your code uses these specific parameter combinations, you will receive a conversion error.
- **Elements were omitted**. This is the most frequent type of warning. Many functions or parameters that are essential in the source system are not required in Snowflake.

Warnings are informational messages that typically don’t require immediate action. However, we strongly recommend reviewing all warnings before deploying code to the target environment. These warnings should be considered during the testing phase of the converted code.

Warnings are identified by specific error codes. To understand what these codes mean, refer to [the issue codes by source section](/migrations/sma-docs/issue-analysis/issue-codes-by-source/README) in this documentation.

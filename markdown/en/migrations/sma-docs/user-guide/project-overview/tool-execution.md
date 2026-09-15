description:
:   Running the Snowpark Migration Accelerator (SMA)

# Snowpark Migration Accelerator: Tool Execution

After setting up your project, you can run the Snowpark Migration Accelerator (SMA).

## Assessment Process

The Assessment process performs an extended evaluation of your source code to determine which conversion type fits best.

[![Assessment process](/static/images/migrations/sma-assets/assessment-process.png)](/static/images/migrations/sma-assets/assessment-process.png)

This process is composed of three distinct phases:

- **Loading Source Code**: SMA scans all files in the input directory to create a file inventory. From this inventory, it builds a semantic model using code from the specified file extensions.
- **Analyzing Source Code**: SMA analyzes the source code to determine which conversion type fits best.
- **Generating Results**: SMA generates the output files needed to display the assessment report. The output varies depending on the conversion type selected.

[![Assessment execution](/static/images/migrations/sma-assets/assessment-execution.png)](/static/images/migrations/sma-assets/assessment-execution.png)

After all three phases are complete, the Assessment Results page is automatically displayed.

## SCOS Conversion Process

The SCOS Conversion process converts your source code to Snowpark Connect (SCOS) code.

[![SCOS Conversion process](/static/images/migrations/sma-assets/scos-conversion-process.png)](/static/images/migrations/sma-assets/scos-conversion-process.png)

The application begins scanning all files in the input directory. The SCOS Conversion process consists of three distinct phases:

- **Loading Source Code**: SMA scans all files in the input directory to create a file inventory. From this inventory, it builds a semantic model using code from the specified file extensions.
- **Analyzing Source Code**: During this main phase, SMA creates an Abstract Syntax Tree (AST) to represent your source code’s functionality. While building the AST, it also creates a symbol table to track elements and functions throughout the conversion process. This symbol table helps generate all output reports. In conversion mode, SMA identifies elements in the AST that have Snowflake equivalents and maps them to their corresponding Snowflake functions.
- **Writing Results**: In the final step, SMA generates output files. For the SCOS Conversion process, SMA produces the converted code in the specified output folder.

[![SCOS Conversion execution](/static/images/migrations/sma-assets/scos-conversion-execution.png)](/static/images/migrations/sma-assets/scos-conversion-execution.png)

After all three phases are complete, the SCOS Conversion Results page is automatically displayed.

## Snowpark API Conversion Process

The Snowpark API Conversion process converts your source code to Snowpark API code.

[![Snowpark API Conversion process](/static/images/migrations/sma-assets/snowpark-api-conversion-process.png)](/static/images/migrations/sma-assets/snowpark-api-conversion-process.png)

The application requires you to select whether to use default settings or customize the settings. For more information on customizing settings, refer to the [Conversion Settings](#sma-conversion-settings) section.

[![Snowpark API Conversion settings](/static/images/migrations/sma-assets/snowpark-api-conversion-settings.png)](/static/images/migrations/sma-assets/snowpark-api-conversion-settings.png)

After configuration is complete, the tool begins scanning all files in the input directory. The Snowpark API Conversion process consists of three distinct phases:

- **Loading Source Code**: SMA scans all files in the input directory to create a file inventory. From this inventory, it builds a semantic model using code from the specified file extensions.
- **Analyzing Source Code**: During this main phase, SMA creates an Abstract Syntax Tree (AST) to represent your source code’s functionality. While building the AST, it also creates a symbol table to track elements and functions throughout the conversion process. This symbol table helps generate all output reports. In conversion mode, SMA identifies elements in the AST that have Snowflake equivalents and maps them to their corresponding Snowflake functions.
- **Writing Results**: In the final step, SMA generates output files. For the Snowpark API Conversion process, SMA produces the converted code in the specified output folder.

[![Snowpark API Conversion execution](/static/images/migrations/sma-assets/snowpark-api-conversion-execution.png)](/static/images/migrations/sma-assets/snowpark-api-conversion-execution.png)

After all three phases are complete, the Snowpark API Conversion Results page is automatically displayed.

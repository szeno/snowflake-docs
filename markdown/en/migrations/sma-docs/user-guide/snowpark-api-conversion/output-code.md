description:
:   Is it really converted?

# Snowpark Migration Accelerator: Output Code

The SMA conversion process generates an Output folder containing the converted code. This folder becomes available immediately after the conversion is complete.

Before examining the code in detail, let’s understand how the output code is organized.

## Output Code File Structure

A project file stores information about your SMA project. You can run SMA multiple times within the same project, and each execution will be associated with that project.

When you run an assessment, SMA creates a folder in your specified output directory. This folder, named “Assessment,” contains all reports and logs generated during the assessment phase. Similarly, when you proceed to conversion, SMA creates another folder named “Conversion” in the output directory you specified during Conversion Setup. This second folder contains all reports and logs generated during the conversion phase.

[![Output Directory File Structure](/static/images/migrations/sma-assets/image(525).png)](/static/images/migrations/sma-assets/image(525).png)

When you click “View Output” in the Conversion Results Page, you will be directed to the Output folder within the Conversion-Date-Time directory. (While this folder also exists in the Assessment-Date-Time directory, it only contains demo code.

The output directory structure will be identical to the input directory structure. All folders, subfolders, and code files will be copied to the output directory with the same names and organization.

The converted code will maintain the same filenames as the source files. For example, if your source file is named “Notebook\_1”, the converted file will also be named “Notebook\_1”.

Additional information will be provided.

Note

If checkpoints generation is enabled in the settings page (check [Conversion Settings](/migrations/sma-docs/user-guide/project-overview/configuration-and-settings)), the conversion will create a file in the output named “checkpoints.json” which allows the user to run it using checkpoints feature within the VS Code Snowflake Extension.

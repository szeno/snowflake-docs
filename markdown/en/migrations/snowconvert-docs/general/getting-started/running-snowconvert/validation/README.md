# SnowConvert AI - Validation

The Scope Validator step checks if the entry code meets the basic requirements to execute a successful conversion. These requirements are:

- Valid extension file
- Valid file encoding
- The entry code is extracted
- Valid entry file format
- Valid files and folder naming
- Valid Comments

Note

If one of these validations is not met, it does not mean that the conversion can not be executed. These validations only warn that something is not okay with the entry code, and thus, something could be wrong with the migration results.

## How to execute the validation

The Scope Validator is a step that starts once the configuration for the [Conversion](../../../getting-started/running-snowconvert/conversion/README) process is done. It means that it is always executed.

### View validation results

Once the validation step finishes, a window with information about which validations failed is displayed:

[![Scope Validator Window With Results](/static/images/migrations/sc-assets/image(8).png "image")](/static/images/migrations/sc-assets/image(8).png)

In this case, the validation that failed is to check if the entry code was extracted or not. Please visit their sections to get more information about each validation.

Also, a report called *FilesOutOfScope* is generated inside a folder called *Scope Validations* inside the output folder.

Copy code

```
Output Folder > Reports > SnowConvert AI > Scope Validations > ScopeValidation.{timeStamp}.csv
```

Note

The <mark style=”color:blue;”>Out of scope report</mark> link could redirect you to this report.

This report enumerates all the invalid files with their respective paths/names, sizes, and reasons. E.g.:

| File Path/Name | File Size | Reason |
| --- | --- | --- |
| file1.bat | 40.0 B | File Type |

Expand

Show lessSee more

The last one was an example of an invalid file because of the extension.

### How to proceed

As you can see in the *Scope Validator Window With Results* image, there are two options: one is to continue with the Assessment or Conversion Process, and the other is to cancel it. The recommendation is to cancel the process, check the warnings, and try to resolve them. But if you decide to continue with the conversion, you will also be able to find the information related to the Scope Validation in the Assessment.csv report and the AssessmentReport.docx. In the Assessment.csv, you will find the following fields: the total validated files, total invalid files, total of files with wrong encoding, total of files with wrong extension, total of files with invalid naming, and an out-of-scope percentage (a calculation of the pending work to do to have a valid entry code). In the docx report, you will find a section with the same information that is in the FilesOutOfScope report.

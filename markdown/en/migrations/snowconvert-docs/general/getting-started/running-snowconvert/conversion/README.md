# SnowConvert AI - Conversion

## How to Execute a Conversion

To execute a conversion, you need a valid access code. You can request one for free from the app by clicking the link ‘Get an Access Code’:

[![Link to get an access code in SnowConvert AI](/static/images/migrations/sc-assets/GetAccessCodeLink.png "image")](/static/images/migrations/sc-assets/GetAccessCodeLink.png)

Then complete the form and click on send:

Note

Personal emails with domain as gmail, outlook, etc, cannot be used to get an access code.

[![Form to get an access code in SnowConvert AI](/static/images/migrations/sc-assets/Screenshot2025-01-03at4.55.44PM.png "image")](/static/images/migrations/sc-assets/Screenshot2025-01-03at4.55.44PM.png)

An email will be sent to your inbox containing the access code.

To execute a conversion fill out the required fields in the **‘Project Creation’** page like:

- Project name
- Source language (Teradata, Oracle, Sql-Server and Redshift)
- Input and output folder
- A valid access code

[![Project Creation page in SnowConvert AI](/static/images/migrations/sc-assets/Screenshot2025-01-03at5.18.38PM.png "image")](/static/images/migrations/sc-assets/Screenshot2025-01-03at5.18.38PM.png)

Note

You can use the same access code to convert from any available source language; just select it in the source dropdown.

## Conversion Setup

To execute a conversion SnowConvert AI will be using all the information provided in the project creation screen, the values that you can change here are:

1. Output folder path (Changing this is optional): \

   [![image](/static/images/migrations/sc-assets/Screenshot2025-01-03at5.08.09PM.png "image")](/static/images/migrations/sc-assets/Screenshot2025-01-03at5.08.09PM.png)

SnowConvert AI will always generate the output into a sub-folder with the following format: Conversion-[Timestamp of the conversion], this folder will be always inside your provided output path, which means that SnowConvert AI won’t override any previously created output.

2. Conversion settings (Only for Teradata, Oracle, or SQL Server)\

   [![Link to open Conversion Settings](/static/images/migrations/sc-assets/Screenshot2025-01-03at5.10.59PM.png "image")](/static/images/migrations/sc-assets/Screenshot2025-01-03at5.10.59PM.png)

   [![Conversion Settings in SnowConvert AI](/static/images/migrations/sc-assets/Screenshot2025-01-03at5.12.06PM.png "image")](/static/images/migrations/sc-assets/Screenshot2025-01-03at5.12.06PM.png)

For a better understanding of how the Conversion settings work please go to the specific article of the supported languages:

1. [Teradata Conversion Settings](teradata-conversion-settings)
2. [Oracle Conversion Settings](oracle-conversion-settings)
3. [SQL Server Conversion Settings](sql-server-conversion-settings)
4. [Azure Synapse Conversion Settings](sql-server-conversion-settings)

Once you are done with the setup, you just need to click on **‘Save & Start Conversion’** button to save the project, continue with the conversion and the progress screen will inform you about the execution status.

[![Progress screen of SnowConvert AI](/static/images/migrations/sc-assets/Screenshot2025-01-03at5.15.22PM.png "image")](/static/images/migrations/sc-assets/Screenshot2025-01-03at5.15.22PM.png)

When this process is completed you will be able to see:

1. **Conversion Reports:** Check the conversion reports by clicking on the “View Results” button.
2. **Conversion Output Code**: On the conversion results screen click on the “View Output” button to open the folder containing the converted code.
3. **Retry Conversion**: On the conversion results screen you can select the **Retry Conversion** button to run again the conversion. That is useful if you change the source code and want to convert the new source code again.

[![Example of 'Conversion Results' in SnowConvert](/static/images/migrations/sc-assets/Screenshot2025-01-03at5.16.30PM.png "image")](/static/images/migrations/sc-assets/Screenshot2025-01-03at5.16.30PM.png)

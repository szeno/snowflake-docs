# SnowConvert AI - Best practices

## 1. Extraction

We highly recommend you use our scripts to extract your workload:

- Teradata: [DDL Export Scripts for Teradata](https://github.com/Snowflake-Labs/SC.DDLExportScripts/blob/main/Teradata/README.md).
- Oracle: [DDL Export Scripts for Oracle](https://github.com/Snowflake-Labs/SC.DDLExportScripts/blob/main/Oracle/README.md).
- SQLServer: [DDL Export Scripts for SQL Server](https://github.com/Snowflake-Labs/SC.DDLExportScripts/blob/main/SQLServer/README.pdf).
- Redshift: [Redshift code extraction guide](code-extraction/redshift).

## 2. Preprocess

We highly recommend you use a Preprocess Script that aims to give you better results before starting an assessment or a conversion. This script performs the following tasks:

1. Create a single file for each top-level object
2. Organize each file by a defined folder hierarchy (The default is: Database Name -> Schema Name -> Object Type)
3. Generate an inventory report that provides information on all the objects that are in the workload.

### 2.1 Download

- Download the [binary of the script for macOS](https://sctoolsartifacts.z5.web.core.windows.net/tools/extractorscope/standardize_sql_files)
  and make sure to follow the setup instructions in Step 2.3.
- Download the [binary of the script for Windows](https://sctoolsartifacts.z5.web.core.windows.net/tools/extractorscope/standardize_sql_files.exe).

### 2.2 Description

The following information is needed to run the script:

| **Script Argument** | **Example Value** | **Required** | **Usage** |
| --- | --- | --- | --- |
| Input folder | `/home/user/extracted_ddls` | Yes | `{ -i | ifolder= }` |
| Output folder | `/home/user/processed_extracted_ddls` | Yes | `{ -o | ofolder= }` |
| Database name | `sampleDataBase` | Yes | `{ -d | dname= }` |
| Database engine | `Microsoft SQL Server` | Yes | `{ -e | dengine= }` |
| Output folder structure | `Database name, top level object type and schema` | No | `[ { -s | structure= } ]` |
| Pivot tables generation | `Yes` | No | `[ -p ]` |

Expand

Show lessSee more

Note

The supported values for the database engine argument (-e) are: oracle, mssql and teradata

Note

The supported values for the output folder structure argument (-s) are: database\_name, schema\_name and top\_level\_object\_name\_type.  
When specifying this argument, all the previous values need to be separated by a comma. For example: `-s database_name,top_level_object_name_type,schema_name`.

This argument is optional and when it is not specified the default structure is the following: Database name, top-level object type and schema name.

Note

The pivot tables generation parameter (-p) is optional.

### 2.3 Setup the binary for Mac

1. Set the binary as an executable:   
   `chmod +x standardize_sql_files`
2. Run the script by executing the following command:

   `./standardize_sql_files`

   - If this is the first time running the binary the following message will pop-up:  
     [![](/static/images/migrations/sc-assets/image(23).png)](/static/images/migrations/sc-assets/image(23).png) Click OK.
   - Open Settings -> Privacy & Security -> Click Allow Anyway  
     [![](/static/images/migrations/sc-assets/image(24).png)](/static/images/migrations/sc-assets/image(24).png)

### Running the script

1. Running the script using the following format:

   1. Mac format  
      `./standardize_sql_files -i "input path" -o "output path" -d Workload1 -e teradata`
   2. Windows format  
      `./standardize_sql_files.exe -i "input path" -o "output path" -d Workload1 -e teradata`
2. If the script is successfully executed the following output will be displayed:

   `Splitting process completed successfully!`   
   `Report successfully created!`   
   `Script successfully executed!`

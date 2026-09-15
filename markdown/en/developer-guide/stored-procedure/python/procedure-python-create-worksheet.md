# Creating a stored procedure from a Python worksheet

You can create a stored procedure from a [Python worksheet](/developer-guide/snowpark/python/python-worksheets#label-snowsight-py-worksheets-write) by using Snowsight.

For example, you might write code in a Python worksheet that extracts data from stages or database objects in Snowflake, transforms the
data, then stores the transformed data in Snowflake. You could then deploy that code as a stored procedure and build a data pipeline,
all without leaving Snowflake.

Create a Python stored procedure from your Python worksheet to automate your code. For details on writing Python worksheets, see
[Writing Snowpark Code in Python Worksheets](/developer-guide/snowpark/python/python-worksheets#label-snowsight-py-worksheets-write).

## Prerequisites

Your role must have OWNERSHIP or CREATE PROCEDURE privileges on the database schema in which you run your Python worksheet to deploy it
as a stored procedure.

## Deploy a Python worksheet as a stored procedure

To create a Python stored procedure that automates the code in your Python worksheet, do the following:

1. Sign in to [Snowsight](/user-guide/ui-snowsight-gs#label-snowsight-getting-started-sign-in).
2. In the navigation menu, select **Projects** » **Worksheets**.
3. Open the Python worksheet you want to deploy as a stored procedure.
4. Select **Deploy**.
5. Enter a name for the stored procedure.
6. (Optional) Enter a comment with details about the stored procedure.
7. (Optional) Select **Replace if exists** to replace an existing stored procedure with the same name.
8. For **Handler**, select the handler function for your stored procedure. For example, `main`.
9. Review the arguments used by your handler function and, if needed, override the SQL data type mapping for a typed argument.
   For details about how Python types are mapped to SQL types, see [SQL-Python Data Type Mappings](/developer-guide/udf-stored-procedure-data-type-mapping#label-sql-python-data-type-mappings).
10. (Optional) Select **Open in Worksheets** to open the stored procedure definition in a SQL worksheet.
11. Select **Deploy** to create the stored procedure.
12. After the stored procedure is created, you can go to the procedure details or select **Done**.

You can create multiple stored procedures from one Python worksheet.

After you create a stored procedure, you can automate it as part of a task. Refer to [Introduction to tasks](/user-guide/tasks-intro).

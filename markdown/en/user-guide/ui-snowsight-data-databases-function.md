# Working with user-defined functions in Snowsight

You can work with user-defined functions (UDFs) in SQL or in Snowsight.

In Snowsight, in the navigation menu, select **Catalog** » **Database Explorer**, and then search for or browse to the UDF.
Select the UDF to review details about and manage the function.

You must have the [relevant privileges](/user-guide/security-access-control-privileges#label-udf-privileges) to access and manage the UDF in Snowsight.

## Explore UDF details in Snowsight

After opening a UDF in Snowsight, you can do the following:

- Identify when the function was created, and any comment on the function.
  You can hover over the time details to see the exact creation date and time.
- Review additional details about the UDF, including:

  - Arguments that the UDF takes, and their expected data types, if applicable.
  - The data type of the result of the function.
  - Whether the function is an aggregate function.
  - Whether the function is a secure function.
  - Whether the function is a table function.
  - The language in which the UDF is written. For example, Java.
- Review the SQL definition of the UDF in the **Function definition** section.
- Review the roles with privileges on the function in the **Privileges** section.

## Manage a UDF in Snowsight

You can perform the following basic management tasks for a UDF in Snowsight:

- To edit the name of the function or add a comment, select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Edit**.
- To drop the function, select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Drop**.
- To transfer ownership of the function to another role, select [![More options](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png)](/static/images/snowsight/snowsight-worksheet-explorer-ellipsis.png) » **Transfer Ownership**

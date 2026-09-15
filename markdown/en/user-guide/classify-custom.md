# Create custom categories for sensitive data

[Enterprise Edition Feature](/user-guide/intro-editions)

Sensitive data classification requires Enterprise Edition or higher. To inquire about upgrading, please contact [Snowflake Support](https://docs.snowflake.com/user-guide/contacting-support).

If there isn’t a [native semantic category](/user-guide/classify-native) that detects your domain-specific sensitive data, you can
create a custom category for your sensitive data.

Implement custom semantic categories by defining a custom classifier. A custom classifier has the following attributes:

- Custom semantic categories that identify types of data; for example, `medical_code` and `employee_id`.
- Regular expressions that are used by Snowflake’s algorithm to detect your sensitive data.
- One of the pre-defined privacy categories.

## How it works

Snowflake provides the CUSTOM\_CLASSIFIER [class](/sql-reference/classes/custom_classifier) in the SNOWFLAKE.DATA\_PRIVACY schema to
enable data engineers to extend their data classification capabilities based on their own knowledge of their data. After you create an
instance of the class, you can call a method on the instance to define your custom semantic category, specify the privacy category, and
specify regular expressions to match column value patterns while optionally matching the column name.

Important

Sensitive data classification stores the definition of a custom classifier, not a reference. If you change the custom classifier, you must use
the SET\_CUSTOM\_CLASSIFIERS method to update the classification profile with the new definition.

For an example of using the CUSTOM\_CLASSIFIER class to create and use a custom classifier, see [Example](/user-guide/classify-custom-using#label-custom-classification-example).

## Considerations

Choose a warehouse that matches the size of the data you are classifying:

- No concern for processing time: x-small warehouse.
- Up to 100 columns in a table: small warehouse.
- 101 to 300 columns in a table: medium warehouse.
- More than 300 columns in a table: large warehouse.

## Threshold for custom categories

The algorithm used to classify custom categories uses a *scoring rule* to evaluate the regular expression of your custom classifier to
determine which semantic category to recommend.

The scoring rule uses a default threshold value of 0.8, which equates to high confidence in terms of what the recommended category should
be. Eighty percent of the data in the sample must match the regular expressions that you add to the instance. The algorithm compares the
score for a column against the threshold value and recommends a category that corresponds to one of the following:

- Non-international system tag
- International system tag
- Custom classifier tag

You can specify the threshold value for a custom classification instance by calling the
[<code className=”samp”><em>custom\_classifier</em></code>!ADD\_REGEX](/sql-reference/classes/custom_classifier/methods/add_regex) method on the instance.

Note

It is possible for two custom classifiers to have the same score. In this case, a tie is resolved by evaluating the following:

- Match percentage between respective custom categories.
- Alphabetical order between the names of the custom categories.

In such a case, the winning category will be the recommended category and the rest is contained in the alternates.

The following table summarizes the scoring algorithm and the recommended tag:

| Name Matcher Provided | Value matches >= threshold | Name matches | Recommendation |
| --- | --- | --- | --- |
| True | True | True | Custom category |
|  | False | True | Snowflake category |
|  | True | False | Snowflake category |
|  | False | False | Snowflake category |
| False | True | Not applicable | Custom category |
|  | False | Not applicable | Snowflake category |

Expand

Show lessSee more

## Replication and cloning

- Instances of the CUSTOM\_CLASSIFIER class are replicated when you replicate a database.
- Instances of the CUSTOM\_CLASSIFIER class are cloned when you clone the schema that contains the instances.

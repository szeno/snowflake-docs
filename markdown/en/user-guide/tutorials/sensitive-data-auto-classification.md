# Tutorial: Automatically classify and tag sensitive data

## Introduction

Identifying and tracking your sensitive data is simple and straightforward. Snowflake provides a built-in algorithm to identify your
sensitive data and automatically tag that data with system tags to help track the type of data and how sensitive it is.

With minimal setup, you can also configure a database so Snowflake automatically performs this classification process for new and changing
data and applies user-defined tags along with the system tags.

In this tutorial, you’ll do the following:

- Set up the resources you need to complete the tutorial, including a user-defined tag that is applied to the sensitive data.
- Create a classification profile, which Snowflake uses to automatically classify data when it’s added to a database.
- Add a tag map to the classification profile so the user-defined tag is applied to data that Snowflake identifies as sensitive.
- View the results of the classification.

## Set up governance database

In this tutorial, you’ll create the Snowflake objects (a user-defined tag and a classification profile) needed to govern your data. Based on
best practice, these object are created in a database dedicated to governance.

[Open a SQL worksheet](/user-guide/ui-snowsight-worksheets-gs#label-snowsight-worksheets-create), and then execute the following statements to create a database and schema
for the governance objects:

Copy code

```
USE ROLE ACCOUNTADMIN;

CREATE DATABASE IF NOT EXISTS governance_db;
CREATE SCHEMA IF NOT EXISTS governance_db.sch;
```

Note

For simplicity, you will use the ACCOUNTADMIN system role to avoid setting up the privileges needed to configure sensitive data
classification. In practice, you should not use this powerful role but rather create custom roles with the required privileges.

## Set up your data

Before setting up the data for this tutorial, create a warehouse to populate a table:

Copy code

```
CREATE WAREHOUSE IF NOT EXISTS tutorial_wh;
```

### Create a table

1. Create the database and schema that will contain the table to be classified.

   Copy code

   ```
   CREATE DATABASE IF NOT EXISTS data_db;
   CREATE SCHEMA IF NOT EXISTS data_db.sch;
   ```
2. Create the table structure that will contain the sensitive data.

   Copy code

   ```
   CREATE TABLE data_db.sch.customers (
     account_number NUMBER(38,0),
     first_name VARCHAR(16777216),
     last_name VARCHAR(16777216),
     email VARCHAR(16777216)
   );
   ```

### Insert values into the table

Add data to the table you created:

Copy code

```
USE WAREHOUSE tutorial_wh;

INSERT INTO data_db.sch.customers (account_number, first_name, last_name, email)
  VALUES
    (1589420, 'john', 'doe', 'john.doe@example.com'),
    (2834123, 'jane', 'doe', 'jane.doe@example.com'),
    (4829381, 'jim', 'doe', 'jim.doe@example.com'),
    (9821802, 'susan', 'smith', 'susan.smith@example.com'),
    (8028387, 'bart', 'simpson', 'bart.barber@example.com');
```

## Create a classification profile

Great, you now have a table full of data that you need to classify to help protect your sensitive data. Because you want Snowflake to
automatically classify data when it is added to a database, you’ll need to create a classification profile.

A classification profile controls how often data in a database is classified, along with what happens during that classification process.
Every classification profile is an instance of the CLASSIFICATION\_PROFILE class.

To create the classification profile for your database, run the following command:

Copy code

```
CREATE OR REPLACE SNOWFLAKE.DATA_PRIVACY.CLASSIFICATION_PROFILE
  governance_db.sch.my_classification_profile(
      {
        'minimum_object_age_for_classification_days': 0,
        'maximum_classification_validity_days': 30,
        'auto_tag': true,
        'classify_views': true
      });
```

When this classification profile is set on your database, the following actions happens:

- Classification starts in less than one day (`'minimum_object_age_for_classification_days': 0`).
- After the initial classification, Snowflake rechecks every 30 days to see if tables need to be reclassified
  (`'maximum_classification_validity_days': 30`).
- Classification tags will be automatically set on columns identified as containing sensitive data (`'auto_tag': true`).
- Snowflake classifies data in tables *and* views (`'classify_views': true`).

## Add tag map to classification profile

Because you set `'auto_tag': true` in your classification profile, Snowflake will automatically apply [system classification tags](/user-guide/classify-intro#label-classify-classification-tags) when it classifies data as being sensitive. The SEMANTIC\_CATEGORY tag classifies the type of
data, for example identifying the data as a name or address. The PRIVACY\_CATEGORY tag classifies the sensitivity of the data, for
example identifying the data as an identifier or quasi-identifier.

Now suppose you want to go one step further and automatically apply your own user-defined tag based on how data is classified. This tutorial
shows you how!

To create the custom tag that you want applied to sensitive data, execute the following statement:

Copy code

```
CREATE TAG governance_db.sch.tutorial_pii;
```

Next, you’ll modify the classification profile so this user-defined tag gets applied when Snowflake identifies that a column contains names.
Adding a tag map to the classification profile configures how and when the user-defined tag gets applied.

To add the tag map to your classification profile, execute the `classification_profile_name!SET_TAG_MAP` method:

Copy code

```
CALL governance_db.sch.my_classification_profile!SET_TAG_MAP(
  {'column_tag_map':[
    {
      'tag_name':'governance_db.sch.tutorial_pii',
      'tag_value':'sensitive_name',
      'semantic_categories':['NAME']
    }]});
```

Now, if sensitive data classification determines the system-defined semantic category is `NAME`, then the user-defined tag `tutorial_pii` is
set on the column. Based on the classification profile, the value of the user-defined `tutorial_pii` tag is set to `sensitive_name`.

Note

You can also define a tag map when creating the classification profile.

## Set classification profile on a database

You have your classification profile configured, so you’re ready to set it on the database. This starts the automatic classification process.

Copy code

```
ALTER DATABASE data_db
  SET CLASSIFICATION_PROFILE = 'governance_db.sch.my_classification_profile';
```

That’s it, Snowflake does the rest! Snowflake starts classifying the existing data and classifies new data when it is added to
the database.

## View classification results

Before completing this part of the tutorial, you’ll have to wait one hour for Snowflake to complete the classification process.

After one hour, execute the following statement to retrieve the results of the classification:

Copy code

```
CALL SYSTEM$GET_CLASSIFICATION_RESULT('data_db.sch.customers');
```

In the results, notice the following:

- The ACCOUNT\_NUMBER column was not classified as sensitive, so it wasn’t assigned classification tags.
- The EMAIL column was flagged as having a semantic category of EMAIL and a privacy category of IDENTIFIER.
- Based on the tag map of the classification profile, the `governance_db.sch.tutorial_pii` user-defined tag got assigned to columns that
  had a semantic category of NAME (see highlighted lines in output).

```
  {
  "classification_profile_config": {
    "classification_profile_name": "GOVERNANCE_DB.SCH.MY_CLASSIFICATION_PROFILE"
  },
  "classification_result": {
    "ACCOUNT_NUMBER": {
      "alternates": []
    },
    "EMAIL": {
      "alternates": [],
      "recommendation": {
        "confidence": "HIGH",
        "coverage": 1,
        "details": [],
        "privacy_category": "IDENTIFIER",
        "semantic_category": "EMAIL",
        "tags": [
          {
            "tag_applied": true,
            "tag_name": "snowflake.core.semantic_category",
            "tag_value": "EMAIL"
          },
          {
            "tag_applied": true,
            "tag_name": "snowflake.core.privacy_category",
            "tag_value": "IDENTIFIER"
          }
        ]
      },
      "valid_value_ratio": 1
    },
    "FIRST_NAME": {
      "alternates": [],
      "recommendation": {
        "confidence": "HIGH",
        "coverage": 1,
        "details": [],
        "privacy_category": "IDENTIFIER",
        "semantic_category": "NAME",
        "tags": [
          {
            "tag_applied": true,
            "tag_name": "snowflake.core.semantic_category",
            "tag_value": "NAME"
          },
          {
            "tag_applied": true,
            "tag_name": "snowflake.core.privacy_category",
            "tag_value": "IDENTIFIER"
          },
          {
            "tag_applied": true,
            "tag_name": "governance_db.sch.tutorial_pii",
            "tag_value": "sensitive_name"
          }
        ]
      },
      "valid_value_ratio": 1
    },
    "LAST_NAME": {
      "alternates": [],
      "recommendation": {
        "confidence": "HIGH",
        "coverage": 1,
        "details": [],
        "privacy_category": "IDENTIFIER",
        "semantic_category": "NAME",
        "tags": [
          {
            "tag_applied": true,
            "tag_name": "snowflake.core.semantic_category",
            "tag_value": "NAME"
          },
          {
            "tag_applied": true,
            "tag_name": "snowflake.core.privacy_category",
            "tag_value": "IDENTIFIER"
          },
          {
            "tag_applied": true,
            "tag_name": "governance_db.sch.tutorial_pii",
            "tag_value": "sensitive_name"
          }
        ]
      },
      "valid_value_ratio": 1
    }
  }
}
```

## Clean up, summary, and additional resources

Congratulations! You’ve successfully completed this tutorial.

In summary, you learned how to do the following:

- Create a classification profile to control how automatic classification is implemented.
- Add a tag map to the classification profile so user-defined tags are automatically set on columns containing sensitive data.
- Set the classification profile on a database to kick off automatic classification.
- View the results of automatic classification.

### Drop the tutorial objects

If you plan to repeat the tutorial, you can keep the objects that you created.

Otherwise, drop the tutorial objects as follows:

Copy code

```
DROP TAG governance_db.sch.tutorial_pii;
DROP DATABASE governance_db;
DROP DATABASE data_db;
DROP WAREHOUSE tutorial_wh;
```

### What’s next?

For complete details about implementing automatic sensitive data classification, including associated costs and implementing custom
classification, see [Use SQL to set up sensitive data classification](/user-guide/classify-auto).

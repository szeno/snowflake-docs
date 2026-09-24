:toc-depth: 3

# Snowflake Data Clean Rooms: Machine Learning

End-of-life notice

The legacy Provider and Consumer Data Clean Rooms are being discontinued. See the
[end-of-life timeline](/user-guide/cleanrooms/pc-eol) for dates and migration guidance.

This topic describes the provider and consumer flows needed to programmatically set up a clean room, share it with a consumer, and run analyses through advanced machine learning algorithms in it. The provider flows loads secure Python code implementing a random-forest-based XGBoost machine learning algorithm into the clean room. This is completely confidential, and visible only to the provider. The consumer cannot see the Python machine-learning code loaded into the clean room.

This flow covers the following:

1. Provider:

   a. Add a custom template running a Lookalike Modeling analysis.

   b. Securely add Machine Learning python code-based templates leveraging XGBoost.

   c. Call the machine learning UDFs inside the clean room using the custom template.
2. Consumer:

   a. Run the custom template that uses the ML functions defined by the provider.

*Lookalike Modeling* is a type of analysis where a consumer tries to find “high-value” customers from a provider’s data by training a statistical model on their high-value customers. This model uses consumer-specified flags to indicate high-value users, such as those with expenditures above a certain threshold, in the consumer’s dataset. The trained model is then used to infer which customers in the provider’s data could potentially be “high value” to the consumer.

## Prerequisites

You need two separate Snowflake accounts to complete this flow. Use the first account to execute the provider’s commands, then switch to the second account to execute the consumer’s commands.

## Provider

Note

The following commands should be run in a Snowflake worksheet in the provider account.

### Set up the environment

Execute the following commands to set up the Snowflake environment before using developer APIs to work with a Snowflake Data Clean Room. If you don’t have the SAMOOHA\_APP\_ROLE role, contact your account administrator.

Copy code

```
use role SAMOOHA_APP_ROLE;
use warehouse app_wh;
```

### Create the clean room

Create a name for the clean room. Enter a new clean room name to avoid colliding with existing clean room names. Clean room names can only be **alphanumeric**. Clean room names cannot contain special characters other than spaces and underscores.

Copy code

```
set cleanroom_name = 'Machine Learning Demo Clean room';
```

You can create a new clean room with the clean room name set above. If the clean room name set above already exists as an existing clean room, this process will fail.

This procedure may take a little longer to run, typically about half a minute.

The second argument to *provider.cleanroom\_init* is the distribution of the clean room. This can either be INTERNAL or EXTERNAL. For testing purposes, if you are sharing the clean room to an account in the same organization, you can use INTERNAL to bypass the automated security scan which must take place before an application package is released to collaborators. However, if you are sharing this clean room to an account in a different organization, you must use an EXTERNAL clean room distribution.

Copy code

```
call samooha_by_snowflake_local_db.provider.cleanroom_init($cleanroom_name, 'INTERNAL');
```

In order to view the status of the security scan, use:

Copy code

```
call samooha_by_snowflake_local_db.provider.view_cleanroom_scan_status($cleanroom_name);
```

Once you have created your clean room, you must set its release directive before it can be shared with any collaborator. However, if your distribution was set to EXTERNAL, you must first wait for the security scan to complete before setting the release directive. You can continue running the remainder of the steps and return here before the *provider.create\_or\_update\_cleanroom\_listing* step while the scan runs.

In order to set the release directive, call:

Copy code

```
call samooha_by_snowflake_local_db.provider.set_default_release_directive($cleanroom_name, 'V1_0', '0');
```

Important

If the consumer and provider are in different cloud regions, you need to enable [Cross-cloud auto-fulfillment](/user-guide/cleanrooms/laf) in both accounts and for both clean rooms.

### Link the dataset, and set the join policy for the dataset

Link Snowflake tables into the clean room, browse through the list of tables in your Snowflake account and enter the fully qualified table names (Database.Schema.Table) as an array. The procedure automatically makes the table accessible to the clean room by creating a secure view of the table from within the clean room, thereby avoiding any need to make a copy of your table.

Copy code

```
call samooha_by_snowflake_local_db.provider.link_datasets($cleanroom_name, ['samooha_provider_sample_database.lookalike_modeling.customers']);
```

Note

If this step doesn’t work even though your table exists, it is likely the SAMOOHA\_APP\_ROLE role has not yet been given access to it. If so, switch to the ACCOUNTADMIN role, call the below procedure on the database, and then switch back for the rest of the flow:

Copy code

```
use role accountadmin;
call samooha_by_snowflake_local_db.provider.register_db('<DATABASE_NAME>');
use role SAMOOHA_APP_ROLE;
```

You can view the dataset names linked to the clean room by calling the following procedure.

Copy code

```
call samooha_by_snowflake_local_db.provider.view_provider_datasets($cleanroom_name);
```

You can see the datasets linked to the clean room using the following procedure:

Copy code

```
select * from samooha_provider_sample_database.lookalike_modeling.customers limit 10;
```

Specify which columns the consumer is allowed to join on when running templates within the clean room. This procedure should be called on identity columns like email. The join policy is “replace only”, so if the function is called again, then the previously set join policy is completely replaced by the new one.

Copy code

```
call samooha_by_snowflake_local_db.provider.set_join_policy($cleanroom_name, ['samooha_provider_sample_database.lookalike_modeling.customers:hashed_email']);
```

If you want to view all the columns to decide the join policy columns, call the following procedure.

Copy code

```
call samooha_by_snowflake_local_db.provider.view_join_policy($cleanroom_name);
```

### Add confidential Machine Learning Python code to the clean room

This section shows you how to load some python functions into the clean room for the lookalike ML work. All python functions installed in the clean room remain completely confidential. They cannot be seen by the consumer.

The following API allows you to define your Python functions directly as inline functions into the clean room. Alternatively you can load Python from staged files you’ve uploaded into the clean room stage. See the [API reference guide](../provider) for an example.

Note

This implementation is limited by the total Snowflake size constraint on the amount of data that can be aggregated by ARRAY\_AGG (128 MB). **Upon request**, Snowflake provides an implementation that leverages batching and streaming models that can scale to arbitrarily sized data sets.

Copy code

```
call samooha_by_snowflake_local_db.provider.load_python_into_cleanroom(
    $cleanroom_name,
    'lookalike_train',
    ['input_data variant', 'labels variant'],
    ['pandas', 'numpy', 'xgboost'],
    'variant',
    'train',
    $$
import numpy as np
import pandas as pd
import xgboost
from sklearn import preprocessing
import sys
import os
import pickle
import codecs
import threading

class TrainXGBoostClassifier(object):
    def __init__(self):
        self.model = None
        self._params = {
            "objective": "binary:logistic",
            "max_depth": 3,
            "nthread": 1,
            "eval_metric": "auc",
        }
        self.num_boosting_rounds = 10

    def get_params(self):
        if self.model is not None and "updater" not in self._params:
            self._params.update(
                {"process_type": "update", "updater": "refresh", "refresh_leaf": True}
            )
        return self._params

    def train(self, X, y):
        """
        Train the model in a threadsafe way
        """
        # pick only the categorical attributes
        categorical = X.select_dtypes(include=[object])

        # fit a one-hot-encoder to convert categorical features to binary features (required by XGBoost)
        ohe = preprocessing.OneHotEncoder()
        categorical_ohe = ohe.fit_transform(categorical)
        self.ohe = ohe

        # get the rest of the features and add them to the binary features
        non_categorical = X.select_dtypes(exclude=[object])
        train_x = np.concatenate((categorical_ohe.toarray(), non_categorical.to_numpy()), axis=1)

        xg_train = xgboost.DMatrix(train_x, label=y)

        params = self.get_params()
        params["eval_metric"] = "auc"
        evallist = [(xg_train, "train")]
        evals_result = {}

        self.model = xgboost.train(
            params, xg_train, self.num_boosting_rounds, evallist, evals_result=evals_result
        )

        self.evals_result = evals_result

    def __dump_model(self, model):
        """
        Save down the model as a json string to load up for scoring/inference
        """
        pickle_jar = codecs.encode(pickle.dumps([model, self.ohe]), "base64").decode()
        return pickle_jar

    def dump_model(self):
        """
        Save down the model as a json string to load up for scoring/inference
        """
        if self.model is not None:
            return self.__dump_model(self.model)
        else:
            raise ValueError("Model needs to be trained first")

def train(d1, l1):

    # get take training features and put them in a pandas dataframe
    X = pd.DataFrame(d1)

    # get the labels into a Numpy array
    y = np.array(l1)

    trainer = TrainXGBoostClassifier()
    trainer.train(X, y)

    # return training stats, accuracy, and the pickled model and pickled one-hot-encoder
    return {
        "total_rows": len(d1),
        "total_bytes_in": sys.getsizeof(d1),
        "model": trainer.dump_model(),
        "iteration": trainer.num_boosting_rounds,
        "auc": np.max(trainer.evals_result["train"]["auc"]),
        "error": 1 - np.max(trainer.evals_result["train"]["auc"])
    }
    $$
);
```

Now let’s install a scoring function into the clean room

Copy code

```
call samooha_by_snowflake_local_db.provider.load_python_into_cleanroom(
    $cleanroom_name,
    'lookalike_score',
    ['pickle_jar variant', 'emails variant', 'features variant'],
    ['pandas', 'numpy', 'xgboost', 'scikit-learn'],
    'string',
    'score',
    $$
import numpy as np
import pandas as pd
import xgboost as xgb
import pickle
import codecs
import json

def score(model, emails, features):
    # load model
    model = model[0] if not isinstance(model, str) else model
    model = pickle.loads(codecs.decode(model.encode(), "base64"))

    # retrieve the XGBoost trainer from the pickle jar
    bst = model[0]

    # retrieve the fitted one-hot-encoder from the pickle jar
    ohe2 = model[1]

    # create pandas dataframe from the inference features
    Y = pd.DataFrame(features)

    # select the categorical attributes and one-hot-encode them
    Y1 = Y.select_dtypes(include=[object])
    Y2 = ohe2.transform(Y1)

    # select the non-categorical attributes
    Y3 = Y.select_dtypes(exclude=[object])

    # join the results of the one-hot encoding to the rest of the attributes
    Y_pred = np.concatenate((Y2.toarray(), Y3.to_numpy()), axis=1)

    # inference
    dscore = xgb.DMatrix(Y_pred)
    pred = bst.predict(dscore)

    retval = list(zip(np.array(emails), list(map(str, pred))))
    retval = [{"email": r[0], "score": r[1]} for r in retval]
    return json.dumps(retval)
    $$
);
```

Note

Loading Python into the clean room creates a new patch for the clean room. If your clean room distribution is set to EXTERNAL, you need to wait for the security scan to complete, then update the default release directive using:

Copy code

```
-- See the versions available inside the cleanroom
show versions in application package samooha_cleanroom_Machine_Learning_Demo_clean_room;

-- Once the security scan is approved, update the release directive to the latest version
call samooha_by_snowflake_local_db.provider.set_default_release_directive($cleanroom_name, 'V1_0', '2');
```

### Add a Custom Lookalike Modeling template

To add a custom analysis template to the clean room you need a placeholder for table names on both the provider and consumer sides, along with join columns from the provider side. In SQL Jinja templates, these placeholders must always be:

- **source\_table**: an *array* of table names from the provider
- **my\_table**: an *array* of table names from the consumer

Table names can be made dynamic through using these variables, but they can also be hardcoded into the template if desired using the name of the view linked to the clean room. Column names can either be hardcoded into the template, if desired, or set dynamically through parameters. If they are set through parameters, remember that you need to call the parameters **dimensions** or **measure\_column**, which need to be arrays, in order for them to be checked against the column policy. You add these as SQL Jinja parameters in the template that will be passed in later by the consumer when querying. The join policies ensure that the consumer cannot join on columns other than the authorized ones.

Alternatively, any argument in a custom SQL Jinja template can be checked for compliance with the join and column policies using the following filters:

- **join\_policy**: checks if a string value or filter clause is compliant with the join policy
- **column\_policy**: checks if a string value or filter clause is compliant with the column policy
- **join\_and\_column\_policy**: checks if columns used for a join in a filter clause are compliant with the join policy, and that columns used as a filter are compliant with the column policy

For example, in the clause *{{ provider\_id | sqlsafe | join\_policy }}*, an input of *p.HEM* will be parsed to check if *p.HEM* is in the join policy. Note: Only use the *sqlsafe* filter with caution, it allows collaborators to put pure SQL into the template.

Note

All provider/consumer tables must be referenced using these arguments since the name of the secure view actually linked to the clean room will be different to the table name. Critically, provider table aliases **MUST** be p (or p1), p2, p3, p4, etc. and consumer table aliases **must** be c (or c1), c2, c3, etc. This is required in order to enforce security policies in the clean room.

This function overrides any existing template with the same name. If you want to update any existing template, you can simply call this function again with the updated template.

A set of features is selected from the provider dataset, and a set of labels is selected from the consumer dataset, along with a “high value” flag (called label\_value). These 2 tables are then inner-joined on email and passed to the Random Forest training algorithm. Lastly, the output of the model training step is passed to an inference function, which uses the trained model to “infer” which of the provider customers NOT in the consumer datasets could be “high value”. The **count** of such individuals is then returned, along with the model error.

The threshold for determining the score beyond which a customer is “likely high value” is manually set in the template as 0.5. This can be easily changed when adding the template to the clean room.

Copy code

```
call samooha_by_snowflake_local_db.provider.add_custom_sql_template(
    $cleanroom_name,
    'prod_custom_lookalike_template',
    $$
WITH
features AS (
    SELECT
        p.hashed_email,
        array_construct(identifier({{ dimensions[0] | column_policy }}) {% for feat in dimensions[1:] %} , identifier({{ feat | column_policy }}) {% endfor %}) as features
    FROM
        identifier({{ source_table[0] }}) as p
),
labels AS (
    SELECT
        c.hashed_email,
        {{ filter_clause | sqlsafe | column_policy }} as label_value
    FROM
        identifier({{ my_table[0] }}) as c
),
trained_model AS (
    SELECT
        train_out:model::varchar as model,
        train_out:error::float as error
    FROM (
      SELECT
        cleanroom.lookalike_train(array_agg(f.features), array_agg(l.label_value)) as train_out
      FROM features f, labels l
      WHERE f.hashed_email = l.hashed_email
    )
),
inference_output AS (
    SELECT
        MOD(seq4(), 100) as batch,
        cleanroom.lookalike_score(
            array_agg(distinct t.model),
            array_agg(p.hashed_email),
            array_agg(array_construct( identifier({{ dimensions[0] | column_policy }}) {% for feat in dimensions[1:] %} , identifier({{ feat | column_policy }}) {% endfor %}) )
        ) as scores
    FROM trained_model t, identifier({{ source_table[0] }}) p
    WHERE p.hashed_email NOT IN (SELECT c.hashed_email FROM identifier({{ my_table[0] }}) c)
    GROUP BY batch
),
processed_output AS (
    SELECT value:email::string as email, value:score::float as score FROM (select scores from inference_output), lateral flatten(input => parse_json(scores))
)
SELECT p.audience_size, t.error from (SELECT count(distinct email) as audience_size FROM processed_output WHERE score > 0.5) p, trained_model t;
    $$
);
```

Note

You can add Differential Privacy sensitivity to samooha\_by\_snowflake\_local\_db.provider.add\_custom\_sql\_template procedure call above as the last parameter (if you do not add it, it will default to 1)

If you want to view the templates that are currently active in the clean room, call the following procedure. You can make the modifications to enable Differential Privacy guarantees on your analysis. A similar pattern can be incorporated into any custom template that you choose to write.

Copy code

```
call samooha_by_snowflake_local_db.provider.view_added_templates($cleanroom_name);
```

### Set the column policy on each table

Display the data linked to see the columns present inside the table. To view the top 10 rows, call the following procedure.

Copy code

```
select * from samooha_provider_sample_database.lookalike_modeling.customers limit 10;
```

Set the columns on which you want to group, aggregate (e.g. SUM/AVG) and generally use in an analysis for every table and template combination. This gives flexibility so that the same table can allow different column selections depending on the underlying template. This should be called only after adding the template.

The column policy is **replace only**, so if the function is called again, then the previously set column policy is completely replaced by the new one.

Column policy should not be used on identity columns like email, HEM, RampID, etc. since you don’t want the consumer to be able to group by these columns. In the production environment, the system will intelligently infer PII columns and block this operation, but this feature is not available in the sandbox environment. It should only be used on columns that you want the consumer to be able to aggregate and group by, like Status, Age Band, Region Code, Days Active, etc.

For the “column\_policy” and “join\_policy” to carry out checks on the consumer analysis requests, all column names MUST be referred to as **dimensions** or **measure\_columns** in the SQL Jinja template. Make sure you use these tags to refer to columns you want to be checked in custom SQL Jinja templates.

Copy code

```
call samooha_by_snowflake_local_db.provider.set_column_policy($cleanroom_name, [
    'prod_custom_lookalike_template:samooha_provider_sample_database.lookalike_modeling.customers:status',
    'prod_custom_lookalike_template:samooha_provider_sample_database.lookalike_modeling.customers:age',
    'prod_custom_lookalike_template:samooha_provider_sample_database.lookalike_modeling.customers:region_code',
    'prod_custom_lookalike_template:samooha_provider_sample_database.lookalike_modeling.customers:days_active',
    'prod_custom_lookalike_template:samooha_provider_sample_database.lookalike_modeling.customers:income_bracket',
    'prod_custom_lookalike_template:samooha_provider_sample_database.lookalike_modeling.customers:household_size',
    'prod_custom_lookalike_template:samooha_provider_sample_database.lookalike_modeling.customers:gender'
]);
```

If you want to view the column policy that has been added to the clean room, call the following procedure.

Copy code

```
call samooha_by_snowflake_local_db.provider.view_column_policy($cleanroom_name);
```

### Share with a consumer

Finally, add a data consumer to the clean room by adding their Snowflake account locator and account names as shown below. The Snowflake account name must be of the form &lt;ORGANIZATION&gt;.&lt;ACCOUNT\_NAME&gt;.

Note

In order to call the following procedures, make sure you have first set the release directive using *provider.set\_default\_release\_directive*. You can see the latest available version and patches using:

Copy code

```
show versions in application package samooha_cleanroom_Machine_Learning_Demo_clean_room;
```

Copy code

```
call samooha_by_snowflake_local_db.provider.add_consumers($cleanroom_name, '<CONSUMER_ACCOUNT_LOCATOR>', '<CONSUMER_ACCOUNT_NAME>');
call samooha_By_snowflake_local_db.provider.create_or_update_cleanroom_listing($cleanroom_name);
```

Multiple consumer account locators can be passed into the *provider.add\_consumers* function as a comma separated string, or as separate calls to *provider.add\_consumers*.

If you want to view the consumers who have been added to this clean room, call the following procedure.

Copy code

```
call samooha_by_snowflake_local_db.provider.view_consumers($cleanroom_name);
```

If you want to view the clean rooms that have been created recently, use the following procedure.

Copy code

```
call samooha_by_snowflake_local_db.provider.view_cleanrooms();
```

If you want to get more insights about the clean room that you have created, use the following procedure.

Copy code

```
call samooha_by_snowflake_local_db.provider.describe_cleanroom($cleanroom_name);
```

Any clean room created can also be deleted. The following command drops the clean room entirely, so any consumers who previously had access to the clean room will no longer be able to use it. If a clean room with the same name is desired in the future, it must be re-initialized using the above flow.

Copy code

```
call samooha_by_snowflake_local_db.provider.drop_cleanroom($cleanroom_name);
```

Note

The provider flow is now finished. Switch to the consumer account to continue with consumer flow.

## Consumer

Note

The following commands should be run in a Snowflake worksheet in the consumer account

### Set up the environment

Execute the following commands to set up the Snowflake environment before using developer APIs to work with a Snowflake Data Clean Room. If you don’t have the SAMOOHA\_APP\_ROLE role, contact your account administrator.

Copy code

```
use role SAMOOHA_APP_ROLE;
use warehouse app_wh;
```

### Install the clean room

Once a clean room share has been installed, the list of clean rooms available can be viewed using the below command.

Copy code

```
call samooha_by_snowflake_local_db.consumer.view_cleanrooms();
```

Assign a name for the clean room that the provider has shared with you.

Copy code

```
set cleanroom_name = 'Machine Learning Demo Clean room';
```

The following command installs the clean room on the consumer account with the associated provider and selected clean room.

This procedure may take a little longer to run, typically about half a minute.

Copy code

```
call samooha_by_snowflake_local_db.consumer.install_cleanroom($cleanroom_name, '<PROVIDER_ACCOUNT_LOCATOR>');
```

Once the clean room has been installed, the provider has to finish setting up the clean room on their side before it is enabled for use. The below function allows you to check the status of the clean room. Once it has been enabled, you should be able to run the Run Analysis command below. It typically takes about 1 minute for the clean room to be enabled.

Copy code

```
call samooha_by_snowflake_local_db.consumer.is_enabled($cleanroom_name);
```

### Link the dataset

Now you can link some of your datasets into the clean room to carry out secure computation with the provider’s data

Copy code

```
call samooha_by_snowflake_local_db.consumer.link_datasets($cleanroom_name, ['samooha_consumer_sample_database.lookalike_modeling.customers']);
```

Note

If this step doesn’t work even though your table exists, it is likely the SAMOOHA\_APP\_ROLE role has not yet been given access to it. If so, switch to the ACCOUNTADMIN role, call the below procedure on the database, and then switch back for the rest of the flow:

Copy code

```
use role accountadmin;
call samooha_by_snowflake_local_db.consumer.register_db('<DATABASE_NAME>');
use role SAMOOHA_APP_ROLE;
```

To run the analysis, you will need to pass in the consumer table. If you want to view the datasets that you have added to the clean room, call the following procedure.

Copy code

```
call samooha_by_snowflake_local_db.consumer.view_consumer_datasets($cleanroom_name);
```

### Run the analysis

Now that the clean room is installed, you can run the analysis template added to the clean room by the provider using the “run\_analysis” command. You can see how each field is determined in the section below.

The “high value” users are identified with the filter\_clause in the query below. If \_c.SALES\_DLR\_ represented the amount of sales per user, then a valid filter could look like *c.HIGH\_VALUE > 4000*.

Note

Before running the analysis, you can alter the warehouse size, or use a new, bigger, warehouse size if your tables are large.

Copy code

```
call samooha_by_snowflake_local_db.consumer.run_analysis(
    $cleanroom_name,                     -- cleanroom
    'prod_custom_lookalike_template',    -- template name

    ['samooha_consumer_sample_database.lookalike_modeling.customers'],                -- consumer tables

    ['samooha_provider_sample_database.lookalike_modeling.customers'],                -- provider tables

    object_construct(                    -- Rest of the custom arguments needed for the template
        'dimensions', ['p.STATUS', 'p.AGE', 'p.REGION_CODE', 'p.DAYS_ACTIVE', 'p.INCOME_BRACKET'], -- Features used in training

        'filter_clause', 'c.SALES_DLR > 2000' -- Consumer flag for which customers are considered high value
    )
);
```

### How to determine the inputs to run\_analysis

To run the analysis, you need to pass in some parameters to the run\_analysis function. This section will show you how to determine what parameters to pass in.

**Template names**

First, you can see the supported analysis templates by calling the following procedure.

Copy code

```
call samooha_by_snowflake_local_db.consumer.view_added_templates($cleanroom_name);
```

Before running an analysis with a template, you need to know what arguments to specify and what types are expected. For custom templates, you can execute the following.

Copy code

```
call samooha_by_snowflake_local_db.consumer.view_template_definition($cleanroom_name, 'prod_custom_lookalike_template');
```

This can often also contain a large number of different SQL Jinja parameters. The following functionality parses the SQL Jinja template and extracts the arguments that need to be specified in run\_analysis into a list.

Copy code

```
call samooha_by_snowflake_local_db.consumer.get_arguments_from_template($cleanroom_name, 'prod_custom_lookalike_template');
```

**Dataset names**

If you want to view the dataset names that have been added to the clean room by the provider, call the following procedure. You can’t view the data present in the datasets that have been added to the clean room by the provider due to the security properties of the clean room.

Copy code

```
call samooha_by_snowflake_local_db.consumer.view_provider_datasets($cleanroom_name);
```

You can also see the tables you’ve linked to the clean room by using the following call:

Copy code

```
call samooha_by_snowflake_local_db.consumer.view_consumer_datasets($cleanroom_name);
```

**Dimension and measure columns**

While running the analysis, you might want to filter, group by and aggregate on certain columns. If you want to view the column policy that has been added to the clean room by the provider, call the following procedure.

Copy code

```
call samooha_by_snowflake_local_db.consumer.view_provider_column_policy($cleanroom_name);
```

**Common errors**

If you are getting **Not approved: unauthorized columns used** error as a result of run analysis, you may want to view the join policy and column policy set by the provider again.

Copy code

```
call samooha_by_snowflake_local_db.consumer.view_provider_join_policy($cleanroom_name);
call samooha_by_snowflake_local_db.consumer.view_provider_column_policy($cleanroom_name);
```

It is also possible that you have exhausted your privacy budget, which prevents you from executing more queries. Your remaining privacy budget can be viewed using the below command. It resets daily, or the clean room provider can reset it if they wish.

Copy code

```
call samooha_by_snowflake_local_db.consumer.view_remaining_privacy_budget($cleanroom_name);
```

You can check if Differential Privacy has been enabled for your clean room using the following API:

Copy code

```
call samooha_by_snowflake_local_db.consumer.is_dp_enabled($cleanroom_name);
```

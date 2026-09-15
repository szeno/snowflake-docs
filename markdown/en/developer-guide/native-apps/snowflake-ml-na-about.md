# Use Snowflake machine learning models in a Snowflake Native App

This topic describes how to use a [Snowflake ML](/developer-guide/snowflake-ml/overview)
model in a Snowflake Native App. It also describes how to call
[Snowflake Cortex](/user-guide/snowflake-cortex/aisql) functions from an app.

## Overview of using Snowpark ML in a Snowflake Native App

Snowflake ML is an integrated set of capabilities for end-to-end machine learning
in a single platform on top of your governed data. You can this functionality within
a Snowflake Native App.

The Snowflake Native App Framework supports the following use cases:

- Providers include a training algorithm in the app, but the trained model is not included.
  Providers include the source code for the model, for example linear regression or logistical
  regression, in the app.

  After the app is installed, training occurs on data in the consumer account, for example by calling the
  model’s `fit()` method.

  For more information, see [Create, train and use a Snowflake ML model in an app](/developer-guide/native-apps/snowflake-ml-na-no-model).
- Providers share data with the consumer and include a training algorithm in the app. After installation,
  the app trains the model based on data in the consumer account that has been shared with the app

  For more information, see [Create, train and use a Snowflake ML model in an app](/developer-guide/native-apps/snowflake-ml-na-no-model).
- Providers train a model based on data in their account and include these models in the app. When the app
  is installed, consumers can use the model directly, for example by calling the model’s
  :predict() method.

  For more information, see [Include a trained model in an app](/developer-guide/native-apps/snowflake-ml-na-with-model).

## Limitations when using Snowflake ML in an app

The following limitations apply when using Snowflake ML in an app:

- Only models based on warehouses are currently supported.
- Providers must use the Snowflake Model Registry to share models with consumers. Snowpark
  ML functions like `fit()` store results in a temporary stage which is not supported
  for Snowflake Native Apps.
- There are limitations on machine learning algorithms that are runnable in a Snowpark sandbox
  within a warehouse. More complex machine learning frameworks like TensorFlow or PyTorch are
  not runnable in these sandboxes.
- Training performed on a provider’s dataset may not yield a model sufficiently effective for
  a consumer’s data. Training a model on consumer data may provide better results.

## Calling Snowflake Cortex functions from an app

To call a [Snowflake Cortex function](/user-guide/snowflake-cortex/aisql) from
an app, the app must be granted the CORTEX\_USER database role. You can request this role in either of the
following ways:

- **Request the role in the manifest file.** List the CORTEX\_USER role in the
  [`snowflake_database`](/developer-guide/native-apps/manifest-reference#label-manifest-native-app-manifest-fields-snowflake-database) section
  of the manifest file. Consumers can then review and grant the role through Snowsight or the
  Python Permission SDK.
- **Ask consumers to grant the role manually.** Mention in the app listing that consumers must grant the
  CORTEX\_USER database role.

To grant the role manually, consumers run a command like the following:

Copy code

```
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO APPLICATION my_app;
```

The CORTEX\_USER database role in the SNOWFLAKE database includes the privileges that allow users to
call Snowflake Cortex LLM functions. See [Snowflake Cortex AI Functions (including LLM functions)](/user-guide/snowflake-cortex/aisql) for more information.

After the role is granted to the app, the app can call Snowflake Cortex functions as shown in the following
example:

Copy code

```
SELECT AI_TRANSLATE('La plateforme unique de Snowflake élimine les silos de données!','fr','en');
```

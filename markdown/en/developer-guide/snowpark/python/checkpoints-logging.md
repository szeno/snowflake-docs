# Snowpark Checkpoints library: Logging

Snowpark Checkpoints uses Python’s built-in [logging](https://docs.python.org/3/library/logging.html) module to provide log messages about its internal operations. The library emits log messages at different [log levels](https://docs.python.org/3/library/logging.html#logging-levels) that can be used to understand the behavior of the library and to diagnose issues.

## Logging structure

Snowpark Checkpoints follows a module-level logging approach, where each Python module that needs to log messages defines its own logger, and the logger’s name matches the module’s fully qualified name.

Each Snowpark Checkpoints package defines a top-level logger, which is named after the package itself and acts as the parent for all module-level loggers within that package. The top-level logger is initialized with a [NullHandler](https://docs.python.org/3/library/logging.handlers.html#nullhandler), ensuring that the logger does not produce output that it wasn’t explicitly configured to produce. Any logging configuration applied to the top-level logger automatically applies to all the module loggers within that package.

Top-level logger names of Snowpark Checkpoints:

| Package name | Top-level logger name |
| --- | --- |
| `snowpark-checkpoints-collectors` | `snowflake.snowpark_checkpoints_collector` |
| `snowpark-checkpoints-validators` | `snowflake.snowpark_checkpoints` |
| `snowpark-checkpoints-configuration` | `snowflake.snowpark_checkpoints_configuration` |
| `snowpark-checkpoints-hypothesis` | `snowflake.hypothesis_snowpark` |

Expand

Show lessSee more

This module-level approach allows for fine-grained control over logging output and ensures that logs inherit settings from a higher-level logger while emitting precise information about their origin.

## Logging configuration

Snowpark Checkpoints does not provide a default logging configuration. You must explicitly configure logging in your application to see the log messages.

If your application already has a logging configuration using Python’s built-in logging module, then you should be able to see the log messages emitted by Snowpark Checkpoints without any additional configuration. If you do not have a logging configuration, you can set up logging using the [basicConfig](https://docs.python.org/3/library/logging.html#logging.basicConfig) function or by creating a custom configuration.

It is advisable to configure logging once at the entry point of your application, such as in the main script or the module that initializes your application. This ensures that logging is set up before any library components are used. If the library is used within a standalone script, logging should be set up at the beginning of that script. Below are some examples to help you get started:

## Basic logging configuration

The simplest and quickest way to enable logging is by using the [basicConfig](https://docs.python.org/3/library/logging.html#logging.basicConfig) function. This function allows you to configure the root logger, which is the ancestor of all loggers in the logging module hierarchy.

The following example demonstrates how to set up the root logger to capture log messages at the specified log level and above and print them to the console:

Copy code

```
import logging

logging.basicConfig(
  level=logging.DEBUG, # Adjust the log level as needed
  format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

## Advanced logging configuration

For more advanced logging configurations, you can use the [logging.config](https://docs.python.org/3/library/logging.config.html) module to set up logging. This approach allows you to define custom loggers, handlers, and formatters, and configure them using a dictionary.

The following example demonstrates how to set up the root logger using a custom configuration that logs messages to the console and to a file:

Copy code

```
import logging.config
from datetime import datetime

LOGGING_CONFIG = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
      "standard": {
          "format": "{asctime} - {name} - {levelname} - {message}",
          "style": "{",
          "datefmt": "%Y-%m-%d %H:%M:%S",
      },
  },
  "handlers": {
      "console": {
          "class": "logging.StreamHandler",
          "formatter": "standard",
          "level": "DEBUG",  # Adjust the log level as needed
      },
      "file": {
          "class": "logging.FileHandler",
          "formatter": "standard",
          "filename": f"app_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
          "level": "DEBUG",  # Adjust the log level as needed
          "encoding": "utf-8",
      },
  },
  "root": {
      "handlers": ["console", "file"],
      "level": "DEBUG",  # Adjust the log level as needed
  },
}

logging.config.dictConfig(LOGGING_CONFIG)
```

## Enable logging for specific packages

To configure logging for a specific package of Snowpark Checkpoints without affecting other loggers, you can use the top-level logger name for that package and apply any custom handlers and formatters according to your needs. Applying the configuration to the top-level logger ensures that all module-level loggers inherit that configuration.

The following example demonstrates how to configure logging just for the following packages:

- `snowpark-checkpoints-collectors`
- `snowpark-checkpoints-configuration`
- `snowpark-checkpoints-validators`
- `snowpark-checkpoints-hypothesis`

Copy code

```
import logging.config
from datetime import datetime

LOGGING_CONFIG = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
      "standard": {
          "format": "{asctime} - {name} - {levelname} - {message}",
          "style": "{",
          "datefmt": "%Y-%m-%d %H:%M:%S",
      },
  },
  "handlers": {
      "console": {
          "class": "logging.StreamHandler",
          "formatter": "standard",
          "level": "DEBUG",  # Adjust the log level as needed
      },
      "file": {
          "class": "logging.FileHandler",
          "formatter": "standard",
          "filename": f"app_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
          "level": "DEBUG",  # Adjust the log level as needed
          "encoding": "utf-8",
      },
  },
  "loggers": {
      "snowflake.snowpark_checkpoints_collector": {
          "handlers": ["console", "file"],
          "level": "DEBUG",  # Adjust the log level as needed
          "propagate": False,
      },
      "snowflake.snowpark_checkpoints": {
          "handlers": ["console", "file"],
          "level": "DEBUG",  # Adjust the log level as needed
          "propagate": False,
      },
      "snowflake.snowpark_checkpoints_configuration": {
          "handlers": ["console", "file"],
          "level": "DEBUG",  # Adjust the log level as needed
          "propagate": False,
      },
      "snowflake.hypothesis_snowpark": {
          "handlers": ["console", "file"],
          "level": "DEBUG",  # Adjust the log level as needed
          "propagate": False,
      },
  },
}

logging.config.dictConfig(LOGGING_CONFIG)
```

For more details on Python’s logging module, see the [Python logging documentation](https://docs.python.org/3/library/logging.html).

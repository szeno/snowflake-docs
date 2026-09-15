# Troubleshooting with Snowpark Python

This topic provides some guidelines on troubleshooting problems when working with the Snowpark library.

## Changing the Logging Settings

By default, the Snowpark library logs `INFO` level messages to stdout. If you want to change these logging
settings, you can change the level to one of the
[supported levels](https://docs.python.org/3/library/logging.html#levels).

For example:

```
>>> import logging
>>> import sys

>>> logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
```

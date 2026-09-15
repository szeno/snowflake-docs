# Troubleshooting

This guide explains how to monitor your deployments in Snowpark Container Services (SPCS) and resolve common issues related to package dependencies, memory, and environment configurations.

## Monitor SPCS deployments

You can monitor deployment by inspecting the services being launched using the following SQL query.

Copy code

```
SHOW SERVICES IN COMPUTE POOL my_compute_pool;
```

Two jobs are launched:

- **MODEL\_BUILD\_xxxxx**: The final characters of the name are randomized to avoid name conflicts. This job builds the image and ends after the image has been built. If an image already exists, the job is skipped.

  The logs are useful for debugging issues such as conflicts in package dependencies. To see the logs from this job, run the SQL below, being sure to use the same final characters:

  Copy code

  ```
  CALL SYSTEM$GET_SERVICE_LOGS('MODEL_BUILD_xxxxx', 0, 'model-build');
  ```
- **MYSERVICE**: The name of the service as specified in the call to `create_service`. This job is started if the MODEL\_BUILD job is successful or skipped. To see the logs from this job, run the SQL below:

  Copy code

  ```
  CALL SYSTEM$GET_SERVICE_LOGS('MYSERVICE', 0, 'model-inference');
  ```

If logs are not available via `SYSTEM$GET_SERVICE_LOG` because the build job or service has been deleted, you can check the event table (if enabled) to see the logs:

Copy code

```
SELECT RESOURCE_ATTRIBUTES, VALUE
FROM <EVENT_TABLE_NAME>
WHERE true
    AND timestamp > dateadd(day, -1, current_timestamp())  -- choose appropriate timestamp range
    AND RESOURCE_ATTRIBUTES:"snow.database.name" = '<db of the service>'
    AND RESOURCE_ATTRIBUTES:"snow.schema.name" = '<schema of the service>'
    AND RESOURCE_ATTRIBUTES:"snow.service.name" = '<Job or Service name>'
    AND RESOURCE_ATTRIBUTES:"snow.service.container.instance" = '0'  -- choose all instances or one particular
    AND RESOURCE_ATTRIBUTES:"snow.service.container.name" != 'snowflake-ingress' --skip logs from internal sidecar
ORDER BY timestamp ASC;
```

## Package conflicts

Two systems dictate the packages installed in the service container: the model itself and the inference server. To minimize conflicts with your model’s dependencies, the inference server requires only the following packages:

- `gunicorn<24.0.0`
- `starlette<1.0.0`
- `uvicorn-standard<1.0.0`

Make sure your model dependencies, along with the above, are resolvable by pip or conda, whichever you use.

If a model has both `conda_dependencies` and `pip_requirements` set, these will be installed as follows via conda:

- **Channels:**

  - `conda-forge`
  - `nodefaults`
- **Dependencies:**

  - `all_conda_packages`
  - **pip:**
    - `all_pip_packages`

Snowflake gets Anaconda packages from conda-forge when building container images because the Snowflake conda channel is available only in warehouses, and the defaults channel requires users to accept Anaconda terms of use, which isn’t possible during an automated build. To obtain packages from a different channel, such as defaults, specify each package with the channel name, as in `defaults::pkg_name`.

Note

If you specify both `conda_dependencies` and `pip_requirements`, the container image builds successfully even if the two sets of dependencies are not compatible, which might cause the resulting container image not to work as you expect. Snowflake recommends using only `conda_dependencies` or only `pip_requirements`, not both.

## Service out of memory

Some models are not thread-safe, so Snowflake loads a separate copy of the model in memory for each worker process. This can cause out-of-memory conditions for large models with a higher number of workers. Try reducing `num_workers`.

## Unable to alter the service spec

The specifications of the model build and inference services cannot be changed using `ALTER SERVICE`. You can only change attributes such as `TAG`, `MIN_INSTANCES`, and so forth. Since the image is published in the image repo, however, you can copy the spec, modify it, and create a new service from it, which you can start manually.

## Package not found

Model deployment failed during the image building phase. model-build logs suggest that a requested package was not found. (This step uses conda-forge by default if the package is mentioned in `conda_dependencies`.)

Package installation can fail for any of the following reasons:

- The package name or version is invalid. Check the spelling and version of the package.
- The requested version of the package does not exist in conda-forge. You can try removing the version specification to get the latest version that is available in conda-forge, or use `pip_requirements` instead. You can browse all available packages here.
- A private package isn’t visible to the image build. Log the model with `artifact_repository_map` pointing at your [customer-hosted artifact repository](/developer-guide/udf/python/customer-hosted-python-artifact-repositories), and confirm the role can use that repository.
- Sometimes, you may need a package from a special channel (eg pytorch). Add a `channel_name::` prefix to the dependency, such as `pytorch::torch`.

## Huggingface Hub version mismatch

A Hugging Face model inference service can fail with the error message:

```
ImportError: huggingface-hub>=0.30.0,<1.0 is required for a normal functioning of this module, but found huggingface-hub==0.25.2
```

This is because the `transformers` package does not specify the correct dependencies on `huggingface-hub` but instead checks in the code. To resolve this problem, log the model again, this time explicitly specifying the required version of `huggingface-hub` in the `conda_dependencies` or `pip_requirements`.

## Torch not compiled with CUDA enabled

The typical cause of this error is that you have specified both `conda_dependencies` and `pip_requirements`. As mentioned in Package conflicts section, conda is the package manager used for building the container image. Anaconda does not resolve packages from `conda_dependencies` and `pip_requirements` together and gives conda packages precedence. This can lead to a situation where the conda packages are not compatible with the pip packages. You might have specified `torch` in the `pip_requirements`, not in the `conda_dependencies`. Consider consolidating the dependencies into either `conda_dependencies` or `pip_requirements`. If that is not possible, prefer specifying the most important packages in `conda_dependencies`.

# Managing packages and runtime

Feature — Generally Available

Available to all AWS, Azure, and GCP commercial regions. PrivateLink is supported.

Snowflake Notebooks run inside a pre-built container environment optimized for scalable AI/ML development powered by Snowflake Container Runtime.

## Python versions

Snowflake Notebooks support Python versions from 3.10 to 3.12. When creating a notebook service, select the Python version that best fits your workload requirements.

## Pre-installed Snowflake Container Runtime packages

Snowflake Container Runtime includes approximately 100 packages and libraries that support a wide range of analytics, data engineering,
and machine learning development tasks inside Snowflake.

See [Snowflake Container Runtime release notes](/developer-guide/snowflake-ml/container-runtime/releases) for the full list of packages
in each version.

## Installing additional packages

Snowflake Notebooks provides flexible approaches for managing Python packages, ranging from fully managed runtimes to custom container images. Each option offers different tradeoffs in ease of use, governance, customization, and external connectivity. This guide compares the options and highlights the scenarios where each works best.

By default, the Snowflake Container Runtime provides a Python execution environment, preinstalled with ~100 popular data science and machine learning packages and first-party Snowflake packages such as snowflake-snowpark-python. It is optimized for Snowflake-managed CPU and GPU infrastructure and recommended for most users and general-purpose notebook workloads.

Additional ways of installing packages:

|  | From uploaded files to Workspaces or Stages | [Artifact Repositories](/user-guide/ui-snowsight/notebooks-in-workspaces/notebooks-in-workspaces-artifact-repositories) *Preview* | External Access Integrations (EAIs) | [Custom Images](/developer-guide/snowflake-ml/custom-runtime-images) *Preview* |
| --- | --- | --- | --- | --- |
| **Description** | Install additional packages and import from .whl or .py files stored in Workspaces or Stages. | The Snowflake-managed PyPI repo, or customer-managed, third-party package repositories that can be optionally added. Supports package policies. | EAIs allow secure connection to a defined list of network endpoints outside of Snowflake, including but not limited to external package repositories. When an artifact repository is selected, packages will not be installed via EAIs. | Alternative to using the default Snowflake Container Runtime, you can build and manage your own container environments. If selected, it will be used as the base environment. Additional packages can be installed via uploaded files, artifact repos, or EAIs. |
| **Accessibility** | Private workspaces: Accessible by default. Shared workspaces or Stages: RBAC governed. | RBAC governed. The Snowflake PyPI repo is accessible by the PUBLIC role by default. | RBAC governed. | RBAC governed. |
| **Recommended Scenarios** | Use when you need additional packages not included in the default runtime or from private/curated repositories. A Shared workspace or a stage is recommended for storing files intended for shared usage among users and roles. | Use when you need additional Python packages not included in the default runtime or from private/curated repositories, with package policy enforcement. | Use when you need to access external package repositories or other network resources (such as internal PyPI servers, Artifactory, or GitHub) that are not available within Snowflake. | Use when you require full customization and control over the container environment, including preinstalled system-level dependencies, custom security tooling, or standardized images across all notebook executions. |
| **Ease of Use** | **Easy**. Simply upload .whl or .py files to a Workspace or a Stage. End users need to run `!pip install` and `import` commands. | **Easy**. The Snowflake PyPI repo is available in all accounts by default. Other artifact repositories require admin setup. End users need to run `!pip install` to install specific packages. | **Harder**. Requires setup and provisioning by account admin. End users need to run `!pip install` to install specific packages. | **Requires most effort** to build and deploy (usually done by the admin / platform team). End users do not need to run any commands as long as the right custom image is selected. Images built on older versions may suffer feature and performance degradation. The initial startup of custom images may be slower. |

Expand

Show lessSee more

### From external repositories

After configuring External Access Integrations (EAIs) for secure repository access, you can install packages directly from external sources such as
PyPI. Users have access to a comprehensive ecosystem of packages beyond the pre-installed runtime, ensuring secure connectivity to external repos.

You can run `pip install` in a Python cell or in the notebook terminal.

For more information, see [Set up external access for Snowflake Notebooks](/user-guide/ui-snowsight/notebooks-external-access).

### From `requirements.txt`

You can specify and install required package versions in a `requirements.txt` file to ensure a consistent environment setup. Install them
using the following command:

Copy code

```
!pip install -r requirements.txt
```

Note

If the package version specified in `requirements.txt` conflicts with supported versions of the
[pre-installed packages](#label-nb-in-ws-packages-runtime-preinstalled-packages), the Python environment may break. Validate compatibility before
installing.

### From Workspace files

You can download or build `.whl` or `.py` files, upload them to your workspace, and install or import them.

- **Wheel files (.whl):** Upload the `.whl` file and install it:

  Copy code

  ```
  !pip install file_name.whl
  ```

  If the package contains dependencies that are not already installed, upload the complete dependency tree (either directly into Workspaces or to a
  stage). Alternatively, attach an EAI that allows access to a repository where the package can be downloaded (for example, PyPI).
- **Python files (.py):** Modules stored in your workspace can be imported directly for sharing utilities and functions across notebooks.
  For example:

  Copy code

  ```
  from my_utils import my_func
  ```

### From a Snowflake stage

Stages provide secure and governed package deployment by leveraging existing Snowflake data storage and governance controls for package files. Use
the Snowpark session to retrieve package files from a Snowflake stage into the container environment for import and use. For example:

Copy code

```
from snowflake.snowpark.context import get_active_session
import sys

session = get_active_session()
session.file.get("@db.schema.stage_name/math_tools.py", "/tmp")

sys.path.append("/tmp")
import math_tools

math_tools.add_one(3)
```

## Runtime management

### Runtime pinning

All notebook services are pinned to the Runtime selected at creation unless you explicitly change it by editing the service. For example, a notebook
service created on `Runtime 2.0` will not be automatically upgraded when new Runtime versions are released.

### Runtime vulnerability scanning

Snowflake scans the Runtime images daily for security vulnerabilities. High or critical Common Vulnerabilities and Exposures (CVEs) are addressed by
releasing new Runtime versions within 30 days of detection.

Existing notebook services can continue using Runtimes with detected CVEs. However, Runtimes with known CVEs cannot be selected when creating new
notebook services.

### Custom runtime

You can build and register your own custom container images for use with Notebooks and ML Jobs. Custom images let you
include specific packages, meet compliance requirements, and ensure reproducibility across environments.

For more information, see [Custom runtime images](/developer-guide/snowflake-ml/custom-runtime-images).

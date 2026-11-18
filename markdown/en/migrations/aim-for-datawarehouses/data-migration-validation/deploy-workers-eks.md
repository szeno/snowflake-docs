# Deploying on Amazon EKS

Run the Worker and the Orchestrator on Amazon EKS when you already operate a cluster and want Workers close to your source system. This page is the Amazon EKS version of the **Kubernetes (outside Snowflake)** scenario in [Deploying workers](./deploy-workers). To run the same images on Amazon ECS without a Kubernetes cluster, see [Deploying on Amazon ECS](./deploy-workers-ecs).

The AIM DMV images are published to the Snowflake image registry, which requires a Snowflake login. Copy the images to a registry your cluster can pull from, such as Amazon ECR, and run them from there. Keep source and Snowflake credentials in AWS Secrets Manager, and reference them from the configuration with `aws-sm:///` references.

## Before you start

- An EKS cluster with an IAM OIDC provider, so pods can assume IAM roles through IAM roles for service accounts (IRSA). See [IAM roles for service accounts](https://docs.aws.amazon.com/eks/latest/userguide/iam-roles-for-service-accounts.html) in the AWS documentation.
- An Amazon ECR repository for each image: `data-exchange-worker` and `data-migration-orchestrator`.
- A workstation or CI runner with Docker, the [Snowflake CLI](/developer-guide/snowflake-cli/index), and the AWS CLI. Run the copy steps there, outside the cluster.
- Access to the image repository `snowflake.images.snowflake_images` in your account.
- Source and Snowflake credentials stored in AWS Secrets Manager. See [AWS Secrets Manager](../manual-migration/data-migration-configuration-reference#aws-secrets-manager).
- Network access from the pods to your source system, to Snowflake, and to `secretsmanager.<region>.amazonaws.com`, through public egress or a VPC interface endpoint.

## 1. Copy the images to Amazon ECR

The images are built for `linux/amd64`, so run them on x86\_64 node groups.

List the available versions of both images with the Snowflake CLI. The repository contains other images, so the command filters for the two AIM DMV images:

Copy code

```
snow sql -c <connection-name> -q "SHOW IMAGES IN IMAGE REPOSITORY snowflake.images.snowflake_images;" | grep -E "data-exchange-worker|data-migration-orchestrator"
```

Pick the newest version that both `data-exchange-worker` and `data-migration-orchestrator` list. Use that version number for both images. Don’t use the tag `latest`.

Run the following steps from a workstation or CI job. Replace `<version>` with the version you chose, and replace the other placeholders with your Snowflake connection name, AWS account ID, and region:

Copy code

```
export SNOWFLAKE_CONNECTION=<connection-name>
export VERSION=<version>
export ECR_REGION=<region>
export ECR_REGISTRY=<account-id>.dkr.ecr.$ECR_REGION.amazonaws.com

# Get the Snowflake registry host and log in to it
export SNOWFLAKE_REGISTRY=$(snow spcs image-registry url -c $SNOWFLAKE_CONNECTION)
snow spcs image-registry login -c $SNOWFLAKE_CONNECTION

# Log in to ECR
aws ecr get-login-password --region $ECR_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

# Pull each image from Snowflake, then push it to ECR
for image in data-exchange-worker data-migration-orchestrator; do
  aws ecr create-repository --repository-name $image --region $ECR_REGION >/dev/null 2>&1 || true
  docker pull --platform linux/amd64 $SNOWFLAKE_REGISTRY/snowflake/images/snowflake_images/$image:$VERSION
  docker tag $SNOWFLAKE_REGISTRY/snowflake/images/snowflake_images/$image:$VERSION $ECR_REGISTRY/$image:$VERSION
  docker push $ECR_REGISTRY/$image:$VERSION
done
```

Repeat these steps when you upgrade AIM DMV. Run the copy from a workstation or CI job, rather than storing the Snowflake registry login in the cluster.

## 2. Create IAM roles for the Worker and the Orchestrator

Create one IAM role for the Worker and one for the Orchestrator. Each role trusts your cluster’s OIDC provider for its own Kubernetes service account. Grant each role `secretsmanager:GetSecretValue` only on the secrets it reads. The Worker reads the source and Snowflake secrets. The Orchestrator reads only the Snowflake secret.

Worker role policy:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": [
        "arn:aws:secretsmanager:us-west-2:<account-id>:secret:aim-dmv/prod/source-redshift-*",
        "arn:aws:secretsmanager:us-west-2:<account-id>:secret:aim-dmv/prod/snowflake-*"
      ]
    }
  ]
}
```

Orchestrator role policy:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:us-west-2:<account-id>:secret:aim-dmv/prod/snowflake-*"
    }
  ]
}
```

Secret ARNs end with a random suffix, so the `-*` at the end of each resource matches it. If the secret uses a customer-managed KMS key, also allow `kms:Decrypt` on that key.

Annotate a service account for each component with its role:

Copy code

```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: dmv-worker
  namespace: dmv
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::<account-id>:role/dmv-worker
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: dmv-orchestrator
  namespace: dmv
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::<account-id>:role/dmv-orchestrator
```

Don’t set access keys on the pods. The AWS SDK picks up the role from the service account.

## 3. Run the Worker

Run the Worker as a Deployment. Put source and Snowflake settings on the container as environment variables, the same way SPCS does. The values can be `aws-sm:///` references. They aren’t credentials, so the Deployment can live in your repository.

Don’t set `command`. The image’s entrypoint installs the source driver, writes the Worker configuration from these variables, and starts the agent. Set `AWS_DEFAULT_REGION` to the region that holds your secrets. The AWS SDK doesn’t read `AWS_REGION`.

Copy code

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dmv-worker
  namespace: dmv
spec:
  replicas: 1
  selector:
    matchLabels:
      app: dmv-worker
  template:
    metadata:
      labels:
        app: dmv-worker
    spec:
      serviceAccountName: dmv-worker
      containers:
        - name: worker
          image: <account-id>.dkr.ecr.us-west-2.amazonaws.com/data-exchange-worker:<version>
          env:
            - name: AWS_DEFAULT_REGION
              value: us-west-2
            - name: DATA_SOURCE_TYPE
              value: redshift
            - name: DATA_SOURCE_HOST
              value: "aws-sm:///aim-dmv/prod/source-redshift#host"
            - name: DATA_SOURCE_PORT
              value: "5439"
            - name: DATA_SOURCE_DATABASE
              value: "<database>"
            - name: DATA_SOURCE_USERNAME
              value: "aws-sm:///aim-dmv/prod/source-redshift#username"
            - name: DATA_SOURCE_PASSWORD
              value: "aws-sm:///aim-dmv/prod/source-redshift#password"
            - name: AGENT_AFFINITY
              value: dmv-eks
            - name: SNOWFLAKE_CONNECTION_NAME
              value: MY_SNOWFLAKE_CONNECTION
            - name: SNOWFLAKE_ACCOUNT
              value: "aws-sm:///aim-dmv/prod/snowflake#account"
            - name: SNOWFLAKE_USER
              value: "aws-sm:///aim-dmv/prod/snowflake#user"
            - name: SNOWFLAKE_PASSWORD
              value: "aws-sm:///aim-dmv/prod/snowflake#password"
```

`DATA_SOURCE_HOST` can be an `aws-sm:///` reference to a `host` field, as shown, or a plain hostname. Set `DATA_SOURCE_TYPE` to your source database, for example `redshift`. `SNOWFLAKE_CONNECTION_NAME` must be `MY_SNOWFLAKE_CONNECTION`, which is the name the image writes into the Snowflake connections file. The default `@SPCS_CONNECTION` only works on SPCS. `AGENT_AFFINITY` routes workflows to this Worker. The Orchestrator uses the same value, set in the next step. See [Affinity](../manual-migration/data-migration-configuration-reference#affinity) and [Environment variables](../manual-migration/data-migration-configuration-reference#environment-variables).

### Use key-pair authentication for Snowflake

If the Snowflake user authenticates with a key pair, don’t set `SNOWFLAKE_PASSWORD`. Set `SNOWFLAKE_PRIVATE_KEY` to an `aws-sm:///` reference instead. The image resolves the key, writes it under `$HOME/.snowflake/` with mode `0600`, and writes a named connection that uses `authenticator = SNOWFLAKE_JWT`. Don’t put the key in the image or in a ConfigMap. Don’t set `SNOWFLAKE_PASSWORD` in the same pod.

Store `account`, `user`, and the PEM in the `private_key` field of the `aim-dmv/prod/snowflake` secret. Optional `role`, `warehouse`, `database`, and `schema` fields are read if you set the matching environment variables.

Keep the Worker Deployment from the previous example. Replace the Snowflake password variable with these:

Copy code

```
            - name: SNOWFLAKE_CONNECTION_NAME
              value: MY_SNOWFLAKE_CONNECTION
            - name: SNOWFLAKE_ACCOUNT
              value: "aws-sm:///aim-dmv/prod/snowflake#account"
            - name: SNOWFLAKE_USER
              value: "aws-sm:///aim-dmv/prod/snowflake#user"
            - name: SNOWFLAKE_PRIVATE_KEY
              value: "aws-sm:///aim-dmv/prod/snowflake#private_key"
            - name: SNOWFLAKE_ROLE
              value: "aws-sm:///aim-dmv/prod/snowflake#role"
            - name: SNOWFLAKE_WAREHOUSE
              value: "aws-sm:///aim-dmv/prod/snowflake#warehouse"
            - name: SNOWFLAKE_DATABASE
              value: "aws-sm:///aim-dmv/prod/snowflake#database"
            - name: SNOWFLAKE_SCHEMA
              value: "aws-sm:///aim-dmv/prod/snowflake#schema"
```

`SNOWFLAKE_CONNECTION_NAME` is `MY_SNOWFLAKE_CONNECTION`, the name the image writes. See the [AWS Secrets Manager](../manual-migration/data-migration-configuration-reference#aws-secrets-manager) section of the configuration reference.

## 4. Run the Orchestrator

The Orchestrator image starts its loop by default, so you don’t need to set a command. Put the Snowflake connection fields in environment variables as `aws-sm:///` references:

Copy code

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dmv-orchestrator
  namespace: dmv
spec:
  replicas: 1
  selector:
    matchLabels:
      app: dmv-orchestrator
  template:
    metadata:
      labels:
        app: dmv-orchestrator
    spec:
      serviceAccountName: dmv-orchestrator
      containers:
        - name: orchestrator
          image: <account-id>.dkr.ecr.us-west-2.amazonaws.com/data-migration-orchestrator:<version>
          env:
            - name: AWS_DEFAULT_REGION
              value: us-west-2
            - name: SNOWFLAKE_ACCOUNT
              value: aws-sm:///aim-dmv/prod/snowflake#account
            - name: SNOWFLAKE_USER
              value: aws-sm:///aim-dmv/prod/snowflake#user
            - name: SNOWFLAKE_PASSWORD
              value: aws-sm:///aim-dmv/prod/snowflake#password
            - name: DATA_MIGRATION_ORCHESTRATOR_AFFINITY
              value: dmv-eks
```

The Orchestrator’s `DATA_MIGRATION_ORCHESTRATOR_AFFINITY` must match the Worker’s `AGENT_AFFINITY`. For the environment variables each component reads, see [Orchestrator and Worker settings](../manual-migration/data-migration-configuration-reference#shared-environment-variables).

### Orchestrator with key-pair authentication

If the Snowflake user authenticates with a key pair, use the same environment variables as the Worker. Don’t set `SNOWFLAKE_PASSWORD`:

Copy code

```
          env:
            - name: AWS_DEFAULT_REGION
              value: us-west-2
            - name: SNOWFLAKE_CONNECTION_NAME
              value: MY_SNOWFLAKE_CONNECTION
            - name: SNOWFLAKE_ACCOUNT
              value: "aws-sm:///aim-dmv/prod/snowflake#account"
            - name: SNOWFLAKE_USER
              value: "aws-sm:///aim-dmv/prod/snowflake#user"
            - name: SNOWFLAKE_PRIVATE_KEY
              value: "aws-sm:///aim-dmv/prod/snowflake#private_key"
            - name: SNOWFLAKE_ROLE
              value: "aws-sm:///aim-dmv/prod/snowflake#role"
            - name: SNOWFLAKE_WAREHOUSE
              value: "aws-sm:///aim-dmv/prod/snowflake#warehouse"
            - name: SNOWFLAKE_DATABASE
              value: "aws-sm:///aim-dmv/prod/snowflake#database"
            - name: SNOWFLAKE_SCHEMA
              value: "aws-sm:///aim-dmv/prod/snowflake#schema"
            - name: DATA_MIGRATION_ORCHESTRATOR_AFFINITY
              value: dmv-eks
```

The Orchestrator writes the same JWT profile the Worker does.

## 5. Check the deployment

Run the health checks in each pod. Both commands print the results as JSON. Check that every check passes. Pass `-c` so `doctor` reads the configuration the entrypoint wrote:

Copy code

```
kubectl -n dmv exec deploy/dmv-worker -- data-exchange-agent doctor -c /home/appuser/configuration.toml
kubectl -n dmv exec deploy/dmv-orchestrator -- python -m data_migration_orchestrator doctor
```

Once both pods are running and the checks pass, create your workflows. The Orchestrator picks them up and assigns the tasks to Workers with a matching affinity.

## Troubleshooting

| Symptom | Likely cause | What to do |
| --- | --- | --- |
| `ImagePullBackOff` | The image isn’t in ECR at that tag, or the node role can’t read ECR. | Confirm the tag exists with `aws ecr describe-images`. Attach `AmazonEC2ContainerRegistryReadOnly` to the node role. |
| `exec format error` | The image is `linux/amd64`, and the node is arm64. | Schedule the pods on x86\_64 nodes. |
| Access denied when resolving an `aws-sm:///` reference | The service account has no IRSA annotation, or the role can’t read that secret. | Check the `eks.amazonaws.com/role-arn` annotation, and check the role’s policy and the secret ARN. |
| Secret not found, or a region error | `AWS_DEFAULT_REGION` is missing or points to a region without the secret. | Set `AWS_DEFAULT_REGION`. `AWS_REGION` is not read. Replicate the secret to that region if needed. |
| Connection timeout to the source or to Snowflake | The pod’s egress doesn’t allow the destination. | Check the route from the pod subnet to the source, and to Snowflake. |

Expand

Show lessSee more

After you rotate a secret, restart the pods. Resolved secrets are cached for `SECRET_MANAGERS_CACHE_TTL_SECONDS`, which defaults to 300 seconds. See [Supported vaults](../manual-migration/data-migration-configuration-reference#supported-vaults) for the full list of AWS Secrets Manager limitations.

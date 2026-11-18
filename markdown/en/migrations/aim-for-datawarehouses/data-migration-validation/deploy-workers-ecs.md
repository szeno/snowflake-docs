# Deploying on Amazon ECS

Run the Worker and the Orchestrator on Amazon ECS when you want Workers close to your source system without operating a Kubernetes cluster. This page runs both as ECS services on AWS Fargate. For a Kubernetes cluster, see [Deploying on Amazon EKS](./deploy-workers-eks).

The AIM DMV images are published to the Snowflake image registry, which requires a Snowflake login. Copy the images to Amazon ECR and run them from there. Keep source and Snowflake credentials in AWS Secrets Manager, and reference them from the task definitions with `aws-sm:///` references.

## Before you start

- An Amazon ECS cluster. This page creates one named `dmv`.
- An Amazon ECR repository for each image: `data-exchange-worker` and `data-migration-orchestrator`.
- A workstation or CI runner with Docker, the [Snowflake CLI](/developer-guide/snowflake-cli/index), the AWS CLI, and the [Session Manager plugin for the AWS CLI](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html). Run the copy steps and the health checks there.
- Access to the image repository `snowflake.images.snowflake_images` in your account.
- Source and Snowflake credentials stored in AWS Secrets Manager. See [AWS Secrets Manager](../manual-migration/data-migration-configuration-reference#aws-secrets-manager).
- VPC subnets for the tasks, with outbound access to the destinations listed in [Networking](#networking).

## 1. Copy the images to Amazon ECR

The images are built for `linux/amd64`. On Fargate, set the task’s CPU architecture to `X86_64`. Don’t use `ARM64`.

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

Repeat these steps when you upgrade AIM DMV. Run the copy from a workstation or CI job, rather than storing the Snowflake registry login in AWS.

## 2. Create IAM roles

ECS uses two kinds of roles. The task execution role lets ECS pull the image from ECR and write logs to Amazon CloudWatch Logs. The task role is the identity the container uses to call AWS, so it is the role that reads Secrets Manager. Create one execution role, and one task role each for the Worker and the Orchestrator.

All three roles trust the ECS tasks service. Save this trust policy as `trust.json`:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "ecs-tasks.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Create the roles, and attach the AWS managed execution policy to the execution role:

Copy code

```
aws iam create-role --role-name dmv-ecs-task-execution --assume-role-policy-document file://trust.json
aws iam create-role --role-name dmv-ecs-worker --assume-role-policy-document file://trust.json
aws iam create-role --role-name dmv-ecs-orchestrator --assume-role-policy-document file://trust.json

aws iam attach-role-policy --role-name dmv-ecs-task-execution \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

Grant each task role `secretsmanager:GetSecretValue` only on the secrets it reads. The Worker reads the source and Snowflake secrets. The Orchestrator reads only the Snowflake secret. The `ssmmessages` actions let you run the health checks in [step 5](#5-check-the-deployment) with ECS Exec.

Worker task role policy, saved as `worker-policy.json`:

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
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssmmessages:CreateControlChannel",
        "ssmmessages:CreateDataChannel",
        "ssmmessages:OpenControlChannel",
        "ssmmessages:OpenDataChannel"
      ],
      "Resource": "*"
    }
  ]
}
```

Orchestrator task role policy, saved as `orchestrator-policy.json`:

Copy code

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:us-west-2:<account-id>:secret:aim-dmv/prod/snowflake-*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "ssmmessages:CreateControlChannel",
        "ssmmessages:CreateDataChannel",
        "ssmmessages:OpenControlChannel",
        "ssmmessages:OpenDataChannel"
      ],
      "Resource": "*"
    }
  ]
}
```

Copy code

```
aws iam put-role-policy --role-name dmv-ecs-worker --policy-name dmv-worker-secrets --policy-document file://worker-policy.json
aws iam put-role-policy --role-name dmv-ecs-orchestrator --policy-name dmv-orchestrator-secrets --policy-document file://orchestrator-policy.json
```

Secret ARNs end with a random suffix, so the `-*` at the end of each resource matches it. If the secret uses a customer-managed KMS key, also allow `kms:Decrypt` on that key.

Don’t set access keys in the task definition. The AWS SDK in the container picks up the task role.

## 3. Create the cluster and networking

Create the cluster, a CloudWatch Logs log group, and a security group for the tasks. The tasks only make outbound connections, so the security group needs no inbound rules:

Copy code

```
aws ecs create-cluster --cluster-name dmv
aws logs create-log-group --log-group-name /ecs/dmv
aws ec2 create-security-group --group-name dmv-ecs-tasks \
  --description "AIM DMV ECS tasks, egress only" --vpc-id <vpc-id>
```

### Networking

Fargate tasks use the `awsvpc` network mode, so each task gets its own network interface in the subnets you choose. Use private subnets with a NAT gateway, and set `assignPublicIp=DISABLED` when you create the services. The tasks need outbound access to:

- Your source system, for example Amazon Redshift on port `5439`.
- Snowflake.
- Amazon ECR and Amazon S3, to pull the images.
- `secretsmanager.<region>.amazonaws.com`, to resolve `aws-sm:///` references.
- Amazon CloudWatch Logs, for the `awslogs` log driver.
- `ssmmessages.<region>.amazonaws.com`, for ECS Exec.
- The Debian package mirrors (`deb.debian.org`). The Worker image installs the source driver from them at start.

If your account blocks egress to unknown IP addresses, allow these destinations from the NAT gateway’s address.

## 4. Register the task definitions and start the services

### Worker

Put source and Snowflake settings on the container as environment variables, the same way SPCS does. The values can be `aws-sm:///` references. They aren’t credentials, so the task definition can live in your repository.

Don’t set `command` or `entryPoint`. The image’s entrypoint installs the source driver, writes the Worker configuration from these variables, and starts the agent. Set `AWS_DEFAULT_REGION` to the region that holds your secrets. The AWS SDK doesn’t read `AWS_REGION`.

Save this task definition as `worker-taskdef.json`. This example authenticates to Snowflake with a key pair:

Copy code

```
{
  "family": "dmv-worker",
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "4096",
  "memory": "8192",
  "ephemeralStorage": { "sizeInGiB": 60 },
  "runtimePlatform": { "operatingSystemFamily": "LINUX", "cpuArchitecture": "X86_64" },
  "executionRoleArn": "arn:aws:iam::<account-id>:role/dmv-ecs-task-execution",
  "taskRoleArn": "arn:aws:iam::<account-id>:role/dmv-ecs-worker",
  "containerDefinitions": [
    {
      "name": "worker",
      "image": "<account-id>.dkr.ecr.us-west-2.amazonaws.com/data-exchange-worker:<version>",
      "essential": true,
      "linuxParameters": { "initProcessEnabled": true },
      "environment": [
        { "name": "AWS_DEFAULT_REGION", "value": "us-west-2" },
        { "name": "DATA_SOURCE_TYPE", "value": "redshift" },
        { "name": "DATA_SOURCE_HOST", "value": "aws-sm:///aim-dmv/prod/source-redshift#host" },
        { "name": "DATA_SOURCE_PORT", "value": "aws-sm:///aim-dmv/prod/source-redshift#port" },
        { "name": "DATA_SOURCE_DATABASE", "value": "aws-sm:///aim-dmv/prod/source-redshift#database" },
        { "name": "DATA_SOURCE_USERNAME", "value": "aws-sm:///aim-dmv/prod/source-redshift#username" },
        { "name": "DATA_SOURCE_PASSWORD", "value": "aws-sm:///aim-dmv/prod/source-redshift#password" },
        { "name": "AGENT_AFFINITY", "value": "dmv-ecs" },
        { "name": "SNOWFLAKE_CONNECTION_NAME", "value": "MY_SNOWFLAKE_CONNECTION" },
        { "name": "SNOWFLAKE_ACCOUNT", "value": "aws-sm:///aim-dmv/prod/snowflake#account" },
        { "name": "SNOWFLAKE_USER", "value": "aws-sm:///aim-dmv/prod/snowflake#user" },
        { "name": "SNOWFLAKE_PRIVATE_KEY", "value": "aws-sm:///aim-dmv/prod/snowflake#private_key" },
        { "name": "SNOWFLAKE_ROLE", "value": "aws-sm:///aim-dmv/prod/snowflake#role" },
        { "name": "SNOWFLAKE_WAREHOUSE", "value": "aws-sm:///aim-dmv/prod/snowflake#warehouse" },
        { "name": "SNOWFLAKE_DATABASE", "value": "aws-sm:///aim-dmv/prod/snowflake#database" },
        { "name": "SNOWFLAKE_SCHEMA", "value": "aws-sm:///aim-dmv/prod/snowflake#schema" }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/dmv",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "worker"
        }
      }
    }
  ]
}
```

- `DATA_SOURCE_HOST`, `DATA_SOURCE_PORT`, and `DATA_SOURCE_DATABASE` can be `aws-sm:///` references, as shown, or plain values. Set `DATA_SOURCE_TYPE` to your source database, for example `redshift`.
- `SNOWFLAKE_CONNECTION_NAME` must be `MY_SNOWFLAKE_CONNECTION`, which is the name the image writes into the Snowflake connections file. The default `@SPCS_CONNECTION` only works on SPCS.
- `SNOWFLAKE_PRIVATE_KEY` makes the image write the key under `$HOME/.snowflake/` with mode `0600`, and a named connection that uses `authenticator = SNOWFLAKE_JWT`. Store `account`, `user`, and the PEM in the `private_key` field of the `aim-dmv/prod/snowflake` secret. The `role`, `warehouse`, `database`, and `schema` fields are read if you set the matching environment variables.
- For password authentication, replace `SNOWFLAKE_PRIVATE_KEY` with `SNOWFLAKE_PASSWORD` set to `aws-sm:///aim-dmv/prod/snowflake#password`. Don’t set both.
- `AGENT_AFFINITY` routes workflows to this Worker. The Orchestrator uses the same value. See [Affinity](../manual-migration/data-migration-configuration-reference#affinity) and [Environment variables](../manual-migration/data-migration-configuration-reference#environment-variables).
- The `doctor` command checks the Worker’s resources. With 4 vCPU, 8 GB of memory, and 60 GiB of ephemeral storage, all its checks pass. On a smaller task, such as 1 vCPU and 2 GB with the default 20 GiB of storage, the memory and disk checks fail.
- `initProcessEnabled` is recommended for ECS Exec sessions.

### Orchestrator

The Orchestrator image starts its loop by default, so don’t set `command`. Save this task definition as `orchestrator-taskdef.json`:

Copy code

```
{
  "family": "dmv-orchestrator",
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "512",
  "memory": "1024",
  "runtimePlatform": { "operatingSystemFamily": "LINUX", "cpuArchitecture": "X86_64" },
  "executionRoleArn": "arn:aws:iam::<account-id>:role/dmv-ecs-task-execution",
  "taskRoleArn": "arn:aws:iam::<account-id>:role/dmv-ecs-orchestrator",
  "containerDefinitions": [
    {
      "name": "orchestrator",
      "image": "<account-id>.dkr.ecr.us-west-2.amazonaws.com/data-migration-orchestrator:<version>",
      "essential": true,
      "linuxParameters": { "initProcessEnabled": true },
      "environment": [
        { "name": "AWS_DEFAULT_REGION", "value": "us-west-2" },
        { "name": "SNOWFLAKE_CONNECTION_NAME", "value": "MY_SNOWFLAKE_CONNECTION" },
        { "name": "SNOWFLAKE_ACCOUNT", "value": "aws-sm:///aim-dmv/prod/snowflake#account" },
        { "name": "SNOWFLAKE_USER", "value": "aws-sm:///aim-dmv/prod/snowflake#user" },
        { "name": "SNOWFLAKE_PRIVATE_KEY", "value": "aws-sm:///aim-dmv/prod/snowflake#private_key" },
        { "name": "SNOWFLAKE_ROLE", "value": "aws-sm:///aim-dmv/prod/snowflake#role" },
        { "name": "SNOWFLAKE_WAREHOUSE", "value": "aws-sm:///aim-dmv/prod/snowflake#warehouse" },
        { "name": "SNOWFLAKE_DATABASE", "value": "aws-sm:///aim-dmv/prod/snowflake#database" },
        { "name": "SNOWFLAKE_SCHEMA", "value": "aws-sm:///aim-dmv/prod/snowflake#schema" },
        { "name": "DATA_MIGRATION_ORCHESTRATOR_AFFINITY", "value": "dmv-ecs" }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/dmv",
          "awslogs-region": "us-west-2",
          "awslogs-stream-prefix": "orchestrator"
        }
      }
    }
  ]
}
```

The Orchestrator’s `DATA_MIGRATION_ORCHESTRATOR_AFFINITY` must match the Worker’s `AGENT_AFFINITY`. For password authentication, replace `SNOWFLAKE_PRIVATE_KEY` with `SNOWFLAKE_PASSWORD`, as for the Worker. For the environment variables each component reads, see [Orchestrator and Worker settings](../manual-migration/data-migration-configuration-reference#shared-environment-variables).

### Start the services

Register both task definitions, then run each one as a service with one task. `--enable-execute-command` turns on ECS Exec for the health checks:

Copy code

```
aws ecs register-task-definition --cli-input-json file://worker-taskdef.json
aws ecs register-task-definition --cli-input-json file://orchestrator-taskdef.json

NETWORK="awsvpcConfiguration={subnets=[<subnet-id-1>,<subnet-id-2>],securityGroups=[<security-group-id>],assignPublicIp=DISABLED}"

aws ecs create-service --cluster dmv --service-name dmv-worker --task-definition dmv-worker \
  --desired-count 1 --launch-type FARGATE --enable-execute-command --network-configuration "$NETWORK"
aws ecs create-service --cluster dmv --service-name dmv-orchestrator --task-definition dmv-orchestrator \
  --desired-count 1 --launch-type FARGATE --enable-execute-command --network-configuration "$NETWORK"

aws ecs wait services-stable --cluster dmv --services dmv-worker dmv-orchestrator
```

To change a task definition later, register it again and point the service at the new revision with `aws ecs update-service --cluster dmv --service dmv-worker --task-definition dmv-worker`.

## 5. Check the deployment

Run the health checks in each task with ECS Exec. Both commands print the results as JSON. Check that every check passes. Pass `-c` so the Worker’s `doctor` reads the configuration the entrypoint wrote. The entrypoint prints that path at start, in the `Agent configuration generated at` line of the Worker’s log:

Copy code

```
WORKER_TASK=$(aws ecs list-tasks --cluster dmv --service-name dmv-worker --query 'taskArns[0]' --output text)
ORCHESTRATOR_TASK=$(aws ecs list-tasks --cluster dmv --service-name dmv-orchestrator --query 'taskArns[0]' --output text)

aws ecs execute-command --cluster dmv --task $WORKER_TASK --container worker --interactive \
  --command "data-exchange-agent doctor -c /home/appuser/configuration.toml"
aws ecs execute-command --cluster dmv --task $ORCHESTRATOR_TASK --container orchestrator --interactive \
  --command "python -m data_migration_orchestrator doctor"
```

The Orchestrator’s `doctor` checks Snowflake connectivity. Its workflow configuration checks are skipped unless you pass a configuration path.

Check the Orchestrator’s log in CloudWatch Logs. Once it’s polling, it logs `PULL_TASKS returned 0 row(s)` about every 20 seconds until you create workflows:

Copy code

```
aws logs tail /ecs/dmv --log-stream-name-prefix orchestrator/ --follow
```

Once both services are running and the checks pass, create your workflows. The Orchestrator picks them up and assigns the tasks to Workers with a matching affinity.

## Troubleshooting

| Symptom | Likely cause | What to do |
| --- | --- | --- |
| `Role is not valid` from `register-task-definition` | A role ARN in the task definition is wrong. | Check `executionRoleArn` and `taskRoleArn` against `aws iam get-role`. |
| `CannotPullContainerError` | The image isn’t in ECR at that tag, or the execution role can’t read ECR. | Confirm the tag exists with `aws ecr describe-images`. Attach `AmazonECSTaskExecutionRolePolicy` to the execution role. |
| `exec format error` | The task runs on `ARM64`. | Set `runtimePlatform.cpuArchitecture` to `X86_64`. |
| Access denied when resolving an `aws-sm:///` reference | The task role can’t read that secret. The execution role’s permissions don’t apply to the container. | Check the task role’s policy and the secret ARN. |
| Secret not found, or a region error | `AWS_DEFAULT_REGION` is missing or points to a region without the secret. | Set `AWS_DEFAULT_REGION`. `AWS_REGION` is not read. Replicate the secret to that region if needed. |
| `SessionManagerPlugin is not found` | The Session Manager plugin isn’t installed where you run `aws ecs execute-command`. | Install the [Session Manager plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html). |
| `execute-command` fails to start a session | The service was created without `--enable-execute-command`, or the task role lacks the `ssmmessages` actions. | Update the service with `--enable-execute-command` and `--force-new-deployment`, and check the task role’s policy. |
| The Worker’s `doctor` fails the memory or disk check | The task is too small. | Raise `cpu`, `memory`, and `ephemeralStorage` in the task definition. |
| Connection timeout to the source or to Snowflake | The task’s subnet or security group doesn’t allow the destination. | Check the route from the task subnets to the source and to Snowflake. See [Networking](#networking). |

Expand

Show lessSee more

After you rotate a secret, restart the tasks with `aws ecs update-service --cluster dmv --service <service-name> --force-new-deployment`. Resolved secrets are cached for `SECRET_MANAGERS_CACHE_TTL_SECONDS`, which defaults to 300 seconds. See [Supported vaults](../manual-migration/data-migration-configuration-reference#supported-vaults) for the full list of AWS Secrets Manager limitations.

# AWS deployment

This deployment runs the React/Nginx and FastAPI containers on an EC2 Auto
Scaling Group behind an Application Load Balancer. Jenkins builds immutable
images, pushes them to ECR, and applies the image tag through Terraform.
Restaurant images are private S3 objects served by FastAPI. PostgreSQL runs on
private RDS, and database/JWT credentials are read from AWS Secrets Manager by
the EC2 instance role.

## Prerequisites

- A Jenkins agent with Docker, Node.js 22, AWS CLI, and Terraform 1.5 or newer.
- An EC2 IAM role for Jenkins, or another short-lived AWS credential source.
- The `prototype-new` AWS profile for account `448895342297`.
- AWS resources incur charges. The default application capacity is one
  `t3.micro`; the Auto Scaling Group can grow to three instances.

Jenkins needs permissions to push to the two project ECR repositories and to
create/update the resources declared in this directory. Use a dedicated role
and narrow it to the project account and region. Do not store an IAM access key
in the Jenkinsfile.

## One-time bootstrap

Terraform state must live in an existing, versioned S3 bucket. Create it once;
replace the example name with a globally unique value:

```bash
aws s3api create-bucket \
  --bucket YOUR_TERRAFORM_STATE_BUCKET \
  --region us-east-2 \
  --create-bucket-configuration LocationConstraint=us-east-2
aws s3api put-bucket-versioning \
  --bucket YOUR_TERRAFORM_STATE_BUCKET \
  --versioning-configuration Status=Enabled
aws dynamodb create-table \
  --table-name restaurant-reservation-terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-2
```

Initialize Terraform and create the repositories, private image bucket, seeded
assets, and empty application secret before the first Jenkins build:

```bash
terraform init -reconfigure \
  -backend-config="bucket=YOUR_TERRAFORM_STATE_BUCKET" \
  -backend-config="key=restaurant-reservation/terraform.tfstate" \
  -backend-config="region=us-east-2" \
  -backend-config="dynamodb_table=restaurant-reservation-terraform-locks"

terraform apply \
  -target=aws_ecr_repository.backend \
  -target=aws_ecr_repository.frontend \
  -target=aws_s3_object.app_assets \
  -target=aws_secretsmanager_secret.app
```

`-reconfigure` is important in this repository because the previous EC2 lab
left a local state file. It starts this deployment against the new remote state
without migrating that legacy state.

Create a long random JWT key and write the application secret. RDS creates and
rotates its own master password through an AWS-managed Secrets Manager secret.

```bash
aws secretsmanager put-secret-value \
  --secret-id restaurant-reservation/app \
  --secret-string '{"SECRET_KEY":"REPLACE_WITH_A_LONG_RANDOM_VALUE"}' \
  --region us-east-2 \
  --profile prototype-new
```

Do not paste real secret values into Git, build logs, or Terraform variables.

## Jenkins job

Create a Pipeline job from SCM and point it at `Jenkinsfile`. Set the
`TF_STATE_BUCKET` build parameter to the state bucket created above. Keep the
default `TF_LOCK_TABLE` value unless the bootstrap table has another name. A build:

1. Runs backend, frontend, and Terraform checks.
2. Builds both Docker images with the Git commit SHA as the tag.
3. Pushes those images to ECR.
4. Runs `terraform plan` and `terraform apply` with that immutable tag.
5. Lets the Auto Scaling Group replace instances using a rolling refresh.

Terraform prints `application_url` after a successful deployment. A rollback is
a Jenkins deployment using a previously published Git SHA as `image_tag`.

## Image flow

The seven images that were previously loaded from Pexels and Picsum are stored
under `deployment/assets/`. Terraform uploads them to the private S3 bucket at
`app-assets/`. The UI reads them through `/api/media/app-assets/...`; no S3
object is publicly accessible.

Managers can upload JPEG, PNG, or WebP restaurant photos up to 5 MB. FastAPI
stores each object under `restaurants/<restaurant_id>/` and saves its object key
and application URL in PostgreSQL.

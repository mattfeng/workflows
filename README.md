# Workflows

## Developer notes
* **ECS Task Role.** For each workflow, create an IAM Role giving that task an identity. Then, add IAM Policies to this role to authorize the workflow to access the AWS services it requires.
    * List of IAM Policies
        * **AWS SSM Parameter Store.**
        * **AWS S3 Upload.**
* For each workflow, a **AWS Batch Job Description** also needs to be created.

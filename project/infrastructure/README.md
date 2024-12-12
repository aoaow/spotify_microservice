# Infrastructure as Code - AWS CloudFormation

This folder contains the CloudFormation template used to provision the infrastructure for the Spotify Microservice project.

## Resources Created
- VPC with a public subnet.
- ECS Cluster to run containerized applications.
- ECS Service to deploy the microservice.

## Prerequisites
- AWS CLI installed and configured.
- An AWS account with permissions to create CloudFormation stacks.
- A Docker image for the application, hosted on a container registry (e.g., Amazon ECR or DockerHub).

## Deployment Instructions
1. Navigate to the `infrastructure` directory:
   ```bash
   cd infrastructure
   ```

2. Deploy the stack:
   ```bash
   aws cloudformation deploy \
     --template-file cloudformation-template.yml \
     --stack-name spotify-microservice-stack \
     --capabilities CAPABILITY_IAM
   ```

3. Monitor the stack creation:
   ```bash
   aws cloudformation describe-stacks --stack-name spotify-microservice-stack
   ```

## Troubleshooting
- Check the CloudFormation console for error messages.
- Ensure your AWS CLI is configured correctly and that you have the necessary permissions.

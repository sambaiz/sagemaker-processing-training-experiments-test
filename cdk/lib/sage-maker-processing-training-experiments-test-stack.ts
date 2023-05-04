import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as ecr from 'aws-cdk-lib/aws-ecr';

export class SageMakerProcessingTrainingExperimentsTestStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const ecrRepositoryTrain = new ecr.Repository(this, 'ECRRepositoryForTrain', {
      repositoryName: `${this.stackName.toLowerCase()}-train`
    })
    this.exportValue(ecrRepositoryTrain.repositoryName)

    const ecrRepositoryPreprocess = new ecr.Repository(this, 'ECRRepositoryForPreprocess', {
      repositoryName: `${this.stackName.toLowerCase()}-preprocess`
    })
    this.exportValue(ecrRepositoryPreprocess.repositoryName)

    const bucket = new s3.Bucket(this, 'Bucket', {
      bucketName: `${this.stackName.toLowerCase()}-${this.account}-${this.region}`
    })

    const role = new iam.Role(this, 'Role', {
      roleName: `${this.stackName}_Role`,
      assumedBy:  new iam.ServicePrincipal('sagemaker.amazonaws.com'),
      inlinePolicies: {
        'estimator-policy': new iam.PolicyDocument({
          statements: [
            new iam.PolicyStatement( {
              actions: [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket",
                "s3:CreateBucket",
              ],
              resources: [
                `arn:aws:s3:::sagemaker-${this.region}-${this.account}`,
                `arn:aws:s3:::sagemaker-${this.region}-${this.account}/*`,
              ],
            }),
            new iam.PolicyStatement( {
              actions: [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket",
              ],
              resources: [
                bucket.bucketArn,
                `${bucket.bucketArn}/*`,
              ],
            }),
            new iam.PolicyStatement( {
              actions: [
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage"
              ],
              resources: [
                ecrRepositoryTrain.repositoryArn,
                ecrRepositoryPreprocess.repositoryArn,
              ],
            }),
            new iam.PolicyStatement( {
              actions: [
                "s3:ListAllMyBuckets",
                "s3:GetBucketLocation",
                "cloudwatch:PutMetricData",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:CreateLogGroup",
                "logs:DescribeLogStreams",
                "ecr:GetAuthorizationToken",
                "ec2:CreateNetworkInterface",
                "ec2:CreateNetworkInterfacePermission",
                "ec2:DeleteNetworkInterface",
                "ec2:DeleteNetworkInterfacePermission",
                "ec2:DescribeNetworkInterfaces",
                "ec2:DescribeVpcs",
                "ec2:DescribeDhcpOptions",
                "ec2:DescribeSubnets",
                "ec2:DescribeSecurityGroups",
                'sagemaker:DescribeProcessingJob',
                "sagemaker:DescribeTrainingJob",
                "sagemaker:CreateExperiment",
                'sagemaker:DescribeExperiment',
                'sagemaker:UpdateExperiment',
                'sagemaker:CreateTrial',
                'sagemaker:DescribeTrial',
                'sagemaker:UpdateTrial',
                'sagemaker:CreateTrialComponent',
                'sagemaker:DescribeTrialComponent',
                'sagemaker:UpdateTrialComponent',
                'sagemaker:AssociateTrialComponent',
                'sagemaker:AddTags',
                'sagemaker:BatchPutMetrics',
              ],
              resources: [
                '*',
              ],
            })
          ]
        })
      }
    })

    new cdk.CfnOutput(this, 'EnvironmentVariables', {
      value: `export ${Object.entries({
        S3_DATA_PATH: `s3://${bucket.bucketName}/test_data`,
        ROLE_ARN: role.roleArn,
        ECR_REPOSITORY_TRAIN: ecrRepositoryTrain.repositoryUri,
        ECR_REPOSITORY_PREPROCESS: ecrRepositoryPreprocess.repositoryUri,
      }).map(([key, value]) => `${key}="${value}"`).join(" ")}`
    })
  }
}

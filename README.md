## sagemaker-processing-training-experiments-test

```sh
$ cd cdk && npm install && npm run build && npm run cdk -- deploy && cd ..
...
Outputs:
SageMakerProTraExpTest.EnvironmentVariables = export S3_DATA_PATH="s3://sagemakerprotraexptest-524580158183-ap-northeast-1/test_data" ROLE_ARN="arn:aws:iam::524580158183:role/SageMakerProTraExpTest_Role" ECR_REPOSITORY_TRAIN="524580158183.dkr.ecr.ap-northeast-1.amazonaws.com/sagemakerprotraexptest-train" ECR_REPOSITORY_PREPROCESS="524580158183.dkr.ecr.ap-northeast-1.amazonaws.com/sagemakerprotraexptest-preprocess"
SageMakerProTraExpTest.ExportsOutputRefECRRepositoryForPreprocessBEBDCF8A66909CC6 = sagemakerprotraexptest-preprocess
SageMakerProTraExpTest.ExportsOutputRefECRRepositoryForTrain831CF0D69A42E5A1 = sagemakerprotraexptest-train

$ vi .github/workflows/deploy.yml
$ git push origin branch # build and deploy image to ECR

$ aws s3 cp --recursive "test_data/" "${S3_DATA_PATH}/"

$ poetry install
$ poetry run python src/run.py
```
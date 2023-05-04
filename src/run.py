import os
from sagemaker.processing import Processor, ProcessingInput, ProcessingOutput
from sagemaker.estimator import Estimator
from sagemaker.analytics import ExperimentAnalytics
from sagemaker import experiments
from datetime import datetime

def preprocess(run: experiments.Run):
  processor = Processor(
    base_job_name=f'preprocess-{run.run_name}',
    image_uri=f'{os.getenv("ECR_REPOSITORY_PREPROCESS")}:latest',
    role=os.getenv('ROLE_ARN'),
    instance_count=1,
    instance_type='ml.m5.xlarge',
    env={'AWS_DEFAULT_REGION': os.getenv('AWS_DEFAULT_REGION', 'ap-northeast-1')},
  )
  processor.run(
    inputs=[
      ProcessingInput(
        source=os.getenv('S3_DATA_PATH'),
        destination='/opt/ml/processing/input',
        # s3_data_distribution_type='ShardedByS3Key',
      ),
    ],
    outputs=[
      ProcessingOutput(
        source='/opt/ml/processing/output',
        destination=os.getenv('S3_DATA_PATH'),
        # s3_upload_mode='Continuous'
      ),
    ],
    arguments=[
      '--xxx', '12345',
    ],
    wait=True,
  )

def train(run: experiments.Run, hyperparameters: object = {}):
  estimator = Estimator(
    base_job_name=f'train-{run.run_name}',
    image_uri=f'{os.getenv("ECR_REPOSITORY_TRAIN")}:latest',
    training_repository_access_mode='Platform',
    role=os.getenv('ROLE_ARN'),
    instance_count=1,
    instance_type='ml.m5.xlarge',
    hyperparameters=hyperparameters,
    environment={'AWS_DEFAULT_REGION': os.getenv('AWS_DEFAULT_REGION', 'ap-northeast-1')},
    # output_path=
  )

  data_path = os.getenv('S3_DATA_PATH')
  estimator.fit(
    inputs={'training': data_path, 'testing': data_path},
    wait=True
  )

def main():
  now = datetime.now()
  experiment_name = f'test-experiment-{now.strftime("%Y%m%d%H%M%S")}'

  with experiments.Run(experiment_name, run_name="run1") as run:
    preprocess(run)
    train(run, {'aaa': 0.4, 'bbb': True})

  with experiments.Run(experiment_name, run_name="run2") as run:
    preprocess(run)
    train(run, {'aaa': 0.8, 'bbb': False})

  experiment_analytics = ExperimentAnalytics(experiment_name)
  df = experiment_analytics.dataframe()
  print(f'analytics columns: {df.columns}')

  df['Source'] = df['SourceArn'].apply(lambda x: str(x).split(':')[-1])

  print(df[[
    "TrialComponentName",
    "Source",
    "preprocess:arg_xxx",
    "test:hp_bbb",
    "test:accuracy - Last"
  ]])

if __name__ == '__main__':
  main()

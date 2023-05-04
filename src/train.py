import os
from sagemaker.experiments import load_run
from sagemaker_training import environment
import pandas as pd

def train(data_path: str, hyperparameters: dict) -> str:
  print(f"data_path: {data_path}")
  print(f"hyperparameters: {hyperparameters}")
  print(f"training data:\n{pd.read_csv(data_path)}")
  return 'trained model'


def test(data_path: str, hyperparameters: dict) -> float:
  with load_run() as run:
    print(f"test data:\n{pd.read_csv(data_path)}")
    run.log_parameters({'test:hp_bbb': hyperparameters.get('bbb')})

    for epoch in range(1, 10):
      run.log_metric(name="test:accuracy", value=hyperparameters.get('aaa', 0.0) / epoch, step=epoch)

def main():
  print("- training started")
  env = environment.Environment()
  print(f"master_hostname: {env.master_hostname}, current_host: {env.current_host}")

  model = train(os.path.join(env.channel_input_dirs['training'], 'train.csv'), env.hyperparameters)  # /opt/ml/input/data/training
  with open(os.path.join(env.model_dir, 'some_model.dat'), 'w') as f:  # /opt/ml/model
    f.write(model)

  test(os.path.join(env.channel_input_dirs['testing'], 'test.csv'), env.hyperparameters)  # /opt/ml/input/data/testing

if __name__ == '__main__':
  main()

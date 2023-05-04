import argparse
import pandas as pd
from sagemaker.experiments import load_run

def main():
  print("- preprocessing started")

  parser = argparse.ArgumentParser()
  parser.add_argument('--xxx', type=int, required=True)
  args = parser.parse_args()

  with load_run() as run:
    run.log_parameters({'preprocess:arg_xxx': args.xxx})

  df = pd.read_csv("/opt/ml/processing/input/raw.csv")
  df.iloc[:5,:].to_csv('/opt/ml/processing/output/train.csv')
  df.iloc[5:,:].to_csv('/opt/ml/processing/output/test.csv')

if __name__ == "__main__":
  main()
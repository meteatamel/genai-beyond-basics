import os
import pandas as pd

def print_eval_result(eval_result, colwidth=150):
    print("==Metadata==")
    for key, value in eval_result.metadata.items():
        print(f"{key}: {value}")

    print("==Summary metrics==")
    for key, value in eval_result.summary_metrics.items():
        print(f"{key}: {value}")

    print("==Metrics table==")
    pd.set_option('display.max_colwidth', colwidth)
    pd.set_option('display.max_columns', None)
    print(eval_result.metrics_table)

# Given a file path, get a valid experiment name out it
# Example: /home/computation_custom.py => computation-custom
def get_experiment_name(file_path, suffix=None):
    file_name = os.path.basename(file_path)
    file_name_without_ext = os.path.splitext(file_name)[0]
    # Gen AI eval service does not like underscore in experiment names
    file_name_without_underscore = file_name_without_ext.replace('_', '-')
    experiment_name = file_name_without_underscore
    if suffix:
        experiment_name = f"{experiment_name}-{suffix}"
    return experiment_name


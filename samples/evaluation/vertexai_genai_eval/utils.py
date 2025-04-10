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

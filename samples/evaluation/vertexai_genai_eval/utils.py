def print_eval_result(eval_result):
    print("==Metadata==")
    for key, value in eval_result.metadata.items():
        print(f"{key}: {value}")

    print("==Summary metrics==")
    for key, value in eval_result.summary_metrics.items():
        print(f"{key}: {value}")

    print("==Metrics table==")
    #print(eval_result.metrics_table)
    print(eval_result.metrics_table.to_markdown())

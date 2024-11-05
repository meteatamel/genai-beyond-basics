import argparse
import time
import vertexai
from vertexai.batch_prediction import BatchPredictionJob

def get_args_parser():
    parser = argparse.ArgumentParser(description="Batch processing")
    parser.add_argument('--project_id', type=str, required=True, help='Google Cloud project id (required)')
    parser.add_argument('--input_dataset_uri', type=str, required=True, help='GCS or BigQuery input dataset uri (required)')
    parser.add_argument('--output_bucket_uri', type=str, required=True, help='Bucket to save output to (required)')
    return parser.parse_args()


def main():
    args = get_args_parser()

    vertexai.init(project=args.project_id, location="us-central1")

    # Submit a batch prediction job with Gemini model
    batch_prediction_job = BatchPredictionJob.submit(
        source_model="gemini-1.5-flash-002",
        input_dataset=args.input_dataset_uri,
        output_uri_prefix=args.output_bucket_uri,
    )

    # Refresh the job until complete
    while not batch_prediction_job.has_ended:
        print(f"Job state: {batch_prediction_job.state.name}")
        time.sleep(10)
        batch_prediction_job.refresh()

    if batch_prediction_job.has_succeeded:
        print(f"Job succeeded! Output location: {batch_prediction_job.output_location}")
    else:
        print(f"Job failed: {batch_prediction_job.error}")


if __name__ == '__main__':
    main()

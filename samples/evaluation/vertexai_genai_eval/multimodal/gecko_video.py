import numpy as np
import pandas as pd
import sys
import prompt_templates_video as prompt_templates
import utils
from vertexai.preview.evaluation import (
    CustomOutputConfig,
    EvalTask,
    PointwiseMetric,
    RubricBasedMetric,
    RubricGenerationConfig,
)

sys.path.append("../../../../")
from samples.evaluation.vertexai_genai_eval.utils import get_experiment_name, print_eval_result

# Gecko metric for video evaluation.
# See:
# https://cloud.google.com/blog/products/ai-machine-learning/evaluate-your-gen-media-models-on-vertex-ai
# https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/evaluation/evaluate_videos_with_gecko.ipynb
def main():
    prompts = [
        "Snow b lanketed rocky mountains surround and shadow deep canyons. the canyons bend through the high elevated mountain peaks. black and white",
        "Lush green valley is carved between rocky cliffs. the valley winds through the high elevated rock faces. misty morning",
        # "A couple in formal evening wear going home get caught in a heavy downpour with umbrellas",
        # "Two friends, dressed in casual summer clothes, are caught in a light summer rain while running home",
        # "A tranquil tableau of in the heart of the Utah desert, a massive sandstone arch spanned the horizon",
        # "A eerie panorama of the Arizona desert, with ancient ruins silhouetted against the setting sun",
        # "Few big purple plums rotating on the turntable. water drops appear on the skin during rotation. isolated on the white background. close-up",
        # "A large red apple rotating on the turntable. water drops appear on the skin during rotation. isolated on the black background. close-up",
        # "A boat sailing leisurely along the Seine River with the Eiffel Tower in background",
        # "A boat cruising rapidly along the Thames River with Big Ben behind",
    ]
    videos = [
        '{"contents": [{"parts": [{"file_data": {"mime_type": "video/mp4", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/videos/mountain.mp4"}}]}]}',
        '{"contents": [{"parts": [{"file_data": {"mime_type": "video/mp4", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/videos/mountain.mp4"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "video/mp4", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/videos/couple.mp4"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "video/mp4", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/videos/couple.mp4"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "video/mp4", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/videos/desert.mp4"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "video/mp4", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/videos/desert.mp4"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "video/mp4", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/videos/plum.mp4"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "video/mp4", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/videos/plum.mp4"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "video/mp4", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/videos/boat.mp4"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "video/mp4", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/videos/boat.mp4"}}]}]}',
    ]

    eval_dataset = pd.DataFrame(
        {
            "prompt": prompts,
            "video": videos,
        }
    )

    # Rubric Generation
    rubric_generation_config = RubricGenerationConfig(
        prompt_template=prompt_templates.RUBRIC_GENERATION_PROMPT,
        parsing_fn=utils.parse_json_to_qa_records,
    )

    # Rubric Validation
    gecko_metric = PointwiseMetric(
        metric="gecko_metric",
        metric_prompt_template=prompt_templates.RUBRIC_VALIDATOR_PROMPT,
        custom_output_config=CustomOutputConfig(
            return_raw_output=True,
            parsing_fn=utils.parse_rubric_results,
        ),
    )

    # Rubric Metric
    rubric_based_gecko = RubricBasedMetric(
        generation_config=rubric_generation_config,
        critique_metric=gecko_metric,
    )

    # Generate rubrics for user prompts
    dataset_with_rubrics = rubric_based_gecko.generate_rubrics(eval_dataset)

    # Evaluate with rubrics
    eval_task = EvalTask(
        dataset=dataset_with_rubrics,
        metrics=[rubric_based_gecko],
        experiment=get_experiment_name(__file__)
    )
    eval_result = eval_task.evaluate(response_column_name="video")
    print_eval_result(eval_result, colwidth=None)

    # Calculate overall score for metric.
    dataset_with_final_scores = utils.compute_scores(eval_result.metrics_table)
    print(f"final_score: {dataset_with_final_scores['final_score'].to_list()}")

    mean_final_score = np.mean(dataset_with_final_scores["final_score"])
    print(f"mean final_score: {mean_final_score}")


if __name__ == "__main__":
    main()

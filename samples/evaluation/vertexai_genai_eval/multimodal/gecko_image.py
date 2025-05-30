import numpy as np
import pandas as pd
import sys
import prompt_templates_image as prompt_templates
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

# Gecko metric for image evaluation.
# See:
# https://cloud.google.com/blog/products/ai-machine-learning/evaluate-your-gen-media-models-on-vertex-ai
# https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/evaluation/evaluate_images_with_gecko.ipynb
def main():
    prompts = [
        "steaming cup of coffee and a croissant on a table",
        "steaming cup of coffee and toast in a cafe",
        # "sunset over a calm ocean",
        # "sunset over a tranquil forest",
        # "butterfly with colorful wings on a flower",
        # "butterfly fluttering over a leaf",
        # "musician playing guitar on a street corner",
        # "musician playing saxophone under lamp post",
        # "vintage camera with a worn leather strap",
        # "new camera with a power zoom lens",
        # "colorful abstract painting",
        # "black and white painting",
        # "baker decorating a cake with frosting",
        # "baker topping cupcakes with sprinkles",
        # "hot air balloon floating above a field of lavender",
        # "hot air balloon landing in a field of sunflowers",
    ]
    images = [
        '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/coffee.png"}}]}]}',
        '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/coffee.png"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/sunset.png"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/sunset.png"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/butterfly.png"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/butterfly.png"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/musician.png"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/musician.png"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/camera.png"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/camera.png"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/abstract.png"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/abstract.png"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/baker.png"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/baker.png"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/balloon.png"}}]}]}',
        # '{"contents": [{"parts": [{"file_data": {"mime_type": "image/png", "file_uri": "gs://cloud-samples-data/generative-ai/evaluation/images/balloon.png"}}]}]}',
    ]

    eval_dataset = pd.DataFrame(
        {
            "prompt": prompts,
            "image": images,
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
    eval_result = eval_task.evaluate(response_column_name="image")
    print_eval_result(eval_result, colwidth=1000)

    # Calculate overall score for metric.
    dataset_with_final_scores = utils.compute_scores(eval_result.metrics_table)
    print(f"final_score: {dataset_with_final_scores['final_score'].to_list()}")

    mean_final_score = np.mean(dataset_with_final_scores["final_score"])
    print(f"mean final_score: {mean_final_score}")


if __name__ == "__main__":
    main()

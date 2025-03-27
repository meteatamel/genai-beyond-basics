import pandas
import sys
from vertexai.generative_models import GenerativeModel
from vertexai.evaluation import EvalTask, MetricPromptTemplateExamples

sys.path.append("../../../../../")
from samples.evaluation.vertexai_genai_eval.utils import print_eval_result

# Pointwise metrics with a provided model to get responses from/
# https://cloud.google.com/vertex-ai/generative-ai/docs/models/metrics-templates#overview
def main():

    prompts = [
        """Context: The Cymbal Starlight 2024 has a cargo capacity of 13.5 cubic feet. Human: What's the cargo capacity of Cymbal Starlight?""",
        "What day is it today?"
    ]

    # LLM to get responses from
    model=GenerativeModel("gemini-2.0-flash")

    eval_dataset = pandas.DataFrame(
        {
            "prompt": prompts,
            # history is needed for multi-turn metrics
            #"history": history
        }
    )



    metrics = [

        # Metrics that need 'prompt' and 'response' columns
        MetricPromptTemplateExamples.Pointwise.FLUENCY,
        #MetricPromptTemplateExamples.Pointwise.COHERENCE,
        #MetricPromptTemplateExamples.Pointwise.GROUNDEDNESS,
        #MetricPromptTemplateExamples.Pointwise.SAFETY,
        #MetricPromptTemplateExamples.Pointwise.INSTRUCTION_FOLLOWING,
        #MetricPromptTemplateExamples.Pointwise.VERBOSITY,
        #MetricPromptTemplateExamples.Pointwise.TEXT_QUALITY,
        #MetricPromptTemplateExamples.Pointwise.SUMMARIZATION_QUALITY,
        #MetricPromptTemplateExamples.Pointwise.QUESTION_ANSWERING_QUALITY,

        # Metrics that additionally need 'history' column
        #MetricPromptTemplateExamples.Pointwise.MULTI_TURN_CHAT_QUALITY,
        #MetricPromptTemplateExamples.Pointwise.MULTI_TURN_SAFETY_QUALITY
    ]

    eval_task = EvalTask(
        dataset=eval_dataset,
        metrics=metrics,
        experiment="pointwise-model"
    )

    eval_result = eval_task.evaluate(
        model=model
    )
    print_eval_result(eval_result)


if __name__ == "__main__":
    main()

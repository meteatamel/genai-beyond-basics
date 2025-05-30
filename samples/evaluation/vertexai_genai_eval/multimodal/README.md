# Gen AI evaluation service - multimodal metrics (Gecko)

## Introduction 

These samples show how to use [Gecko](https://arxiv.org/abs/2404.16820) for image and video evaluation. 

Gecko proceeds with three key steps.

**Step 1 - Semantic prompt decomposition**: Gecko leverages a Gemini model to break down the input text prompt into key 
semantic elements that need to be verified in the generated media. 

**Step 2: Question generation**: Based on the decomposed prompt, the Gemini model then generates a series of question-answer
pairs. These questions are specifically designed to probe the generated image or video for the presence and accuracy of
the identified elements and relationships

**Step 3: Scoring**: the Gemini model scores the generated media against each question-answer pair. These individual scores
are then aggregated to produce a final evaluation score.

![Gecko metric](https://storage.googleapis.com/gweb-cloudblog-publish/images/Figure_3_xSjcX8h.max-1000x1000.jpg)

##  Custom parsing logic

The outputs supported by Gecko are more sophisticated than the default outputs of predefined rubric based metrics. 
To handle this, custom parsing logic is required. See [utils.py](./utils.py) for the details.

## Image evaluation

For image evaluation, see [gecko_image.py](./gecko_image.py) for the code and [prompt_templates_image.py](./prompt_templates_image.py) 
for the prompt. 

Run:

```python
python gecko_image.py
```

## Video evaluation

For video evaluation, see [gecko_video.py](./gecko_video.py) for the code and [prompt_templates_video.py](./prompt_templates_video.py) 
for the prompt. 

Run:

```python
python gecko_video.py
```

## References

* [Blog: Evaluate your gen media models with multimodal evaluation on Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/evaluate-your-gen-media-models-on-vertex-ai)
* [evaluate_images_with_gecko.ipynb](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/evaluation/evaluate_images_with_gecko.ipynb)
* [evaluate_videos_with_gecko.ipynb](https://github.com/GoogleCloudPlatform/generative-ai/blob/main/gemini/evaluation/evaluate_videos_with_gecko.ipynb)
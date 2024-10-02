# Promptfoo and Vertex AI

![Promptfoo and Vertex AI](images/promptfoo_vertexai.png)

[Promptfoo](https://www.promptfoo.dev/) is an open-source LLM testing evaluation
framework. It allows you to build reliable prompts, RAGs, and agents by
evaluating them and run security checks (red teaming) against your LLM apps.

In this tutorial, you'll learn how to use PromptFoo with Vertex AI.

## Set up Promptfoo and Vertex AI

[Install PromptFoo](https://www.promptfoo.dev/docs/installation/) in your
environment and verify that it's installed:

```shell
promptfoo --version
```

Set the Google project id in `gcloud`:

```shell
gcloud config set core/project your-project-id
```

Log in:

```shell
gcloud auth application-default login
```

## LLM evaluations

You can run evaluations directly against LLMs.

You can initialize an evaluation configuration with this command:

```shell
promptfoo init
```

Then, you can select what scenarios you want to evaluate (eg. Improve prompt and
model performance, against Google Gemini Pro, )

[promptfooconfig1.yaml](./promptfooconfig1.yaml) is a sample configuration for
evaluating against a couple of Vertex AI models:

Run:

```shell
promptfoo eval -c promptfooconfig1.yaml
```

View the results in the console:

```shell
┌──────────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────┐
│ question                                                     │ [vertex:gemini-1.5-flash-002] You are a helpful assistant.   │ [vertex:gemini-1.5-pro-002] You are a helpful assistant.     │
│                                                              │ Reply with a concise answer to this inquiry: '{{question}}'  │ Reply with a concise answer to this inquiry: '{{question}}'  │
├──────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
│ What's the capital of Cyprus?                                │ [PASS] Nicosia                                               │ [PASS] Nicosia                                               │
├──────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────┤
│ What's the weather like in London generally?                 │ [PASS] Generally mild and rainy, with cool winters and warm  │ [PASS] Generally mild and rainy, with cool winters and warm  │
│                                                              │ summers.                                                     │ summers.                                                     │
└──────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────┘
==========================================================================================================================================================================================
✔ Evaluation complete.

» Run promptfoo view to use the local web viewer
» Run promptfoo share to create a shareable URL
» This project needs your feedback. What's one thing we can improve? https://forms.gle/YFLgTe1dKJKNSCsU7
==========================================================================================================================================================================================
```

Also view it in the browser:

```shell
promptfoo view
```

![Promptfoo LLM evaluation](images/promptfoo_llm_evaluation.png)

## LLM red teaming

You can also use read team testing to find vulnerabilities in AI systems by simulating
malicious inputs against LLMs or your endpoints using LLMs.

Similar to evaluations, you can run `promptfoo init` to generate a
configuration.

[promptfooconfig2.yaml](./promptfooconfig2.yaml) is a sample configuration for
read team testing against a Vertex AI model:

Generate test cases from this configuration:

```shell
promptfoo redteam generate -c promptfooconfig2.yaml
```

This generates a [readteam.yaml](./redteam.yaml) file with test cases:

```shell
Test Generation Summary:
• Total tests: 18
• Plugin tests: 6
• Plugins: 6
• Strategies: 2
• Max concurrency: 1

Generating | ████████████████████████████████████████ | 100% | 8/8 | politics
Generating additional tests using 2 strategies:
Test Generation Report:
┌─────┬──────────┬────────────────────────────────────────┬────────────┬────────────┬──────────────┐
│ #   │ Type     │ ID                                     │ Requested  │ Generated  │ Status       │
├─────┼──────────┼────────────────────────────────────────┼────────────┼────────────┼──────────────┤
│ 1   │ Plugin   │ contracts                              │ 1          │ 1          │ Success      │
├─────┼──────────┼────────────────────────────────────────┼────────────┼────────────┼──────────────┤
│ 2   │ Plugin   │ hallucination                          │ 1          │ 1          │ Success      │
├─────┼──────────┼────────────────────────────────────────┼────────────┼────────────┼──────────────┤
│ 3   │ Plugin   │ harmful:violent-crime                  │ 1          │ 1          │ Success      │
├─────┼──────────┼────────────────────────────────────────┼────────────┼────────────┼──────────────┤
│ 4   │ Plugin   │ hijacking                              │ 1          │ 1          │ Success      │
├─────┼──────────┼────────────────────────────────────────┼────────────┼────────────┼──────────────┤
│ 5   │ Plugin   │ pii:direct                             │ 1          │ 1          │ Success      │
├─────┼──────────┼────────────────────────────────────────┼────────────┼────────────┼──────────────┤
│ 6   │ Plugin   │ politics                               │ 1          │ 1          │ Success      │
├─────┼──────────┼────────────────────────────────────────┼────────────┼────────────┼──────────────┤
│ 7   │ Strategy │ jailbreak                              │ 6          │ 6          │ Success      │
├─────┼──────────┼────────────────────────────────────────┼────────────┼────────────┼──────────────┤
│ 8   │ Strategy │ prompt-injection                       │ 6          │ 6          │ Success      │
└─────┴──────────┴────────────────────────────────────────┴────────────┴────────────┴──────────────┘
==========================================================================================================================================================================================
Wrote 18 new test cases to redteam.yaml
```

Run the test cases:

```shell
promptfoo redteam eval
```

View your results:

![Promptfoo LLM redteam](images/promptfoo_llm_redteam.png)

## References

* [Google Vertex provider on PromptFoo](https://www.promptfoo.dev/docs/providers/vertex/)
* [Getting started](https://www.promptfoo.dev/docs/getting-started)
* [LLM red teaming](https://www.promptfoo.dev/docs/red-team)
* [Promptfoo examples](https://github.com/promptfoo/promptfoo/tree/main/examples)
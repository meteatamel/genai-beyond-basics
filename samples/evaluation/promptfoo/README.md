# Promptfoo and Vertex AI

![Promptfoo and Vertex AI](images/promptfoo_vertexai.png)

[Promptfoo](https://www.promptfoo.dev/) is an open-source tool for evaluating and red-teaming (security) LLM apps. It's 
similar to DeepEval but with added focus on security.

In this tutorial, you'll learn how to use PromptFoo with Vertex AI.

## Setup

[Install PromptFoo](https://www.promptfoo.dev/docs/installation/) in your environment. For example, on Mac OS, you can
use brew:

```shell
brew install promptfoo
````

Verify that it's installed:

```shell
promptfoo --version
```

Make sure your `gcloud` is setup with your project:

```shell
gcloud config set core/project your-project-id
```

And you're logged in:

```shell
gcloud auth application-default login
```

You can start using Promptfoo in different scenarios with its interactive guide:

```shell
promptfoo init

? What would you like to do?
  Not sure yet
❯ Improve prompt and model performance
  Improve RAG performance
  Improve agent/chain of thought performance
  Run a red team evaluation
```

## Evaluation

In `Improve prompt and model performance`, you can use Promptfoo to evaluate against different LLMs from OpenAI, 
Anthropic, Gemini, or simply an HTTP endpoint.

[promptfooconfig1.yaml](./promptfooconfig1.yaml) is a sample configuration for
evaluating against a couple of Vertex AI models.

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

## Red-teaming (security)

In `Run a read team evaluation`, you can use Promptfoo to do read-team security testing to find vulnerabilities 
by simulating malicious inputs against LLMs or your endpoints using LLMs.

[promptfooconfig2.yaml](./promptfooconfig2.yaml) is a sample configuration for read team testing against a Vertex AI model.

Generate test cases from this configuration:

```shell
promptfoo redteam generate -c promptfooconfig2.yaml
```

This generates a [readteam.yaml](./redteam.yaml) file with the actual test cases:

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
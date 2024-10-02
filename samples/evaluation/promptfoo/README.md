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

Run some evaluations against a couple of Vertex AI models. See
[promptfooconfig1.yaml](./promptfooconfig1.yaml) for details.

Run:

```shell
promptfoo eval -c promptfooconfig1.yaml
```

You can view the results in the console:

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

You can also see it in the browser:

```shell
promptfoo view
```

![PromptFoo LLM evaluation](images/promptfoo_llm_evaluation.png)

## LLM red teaming

TODO

## References

* [Google Vertex provider on PromptFoo](https://www.promptfoo.dev/docs/providers/vertex/)
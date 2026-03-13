# A2UI with CopilotKit and Agent Development Kit (ADK)

This is a starter template for building AI agents that use A2UI and CopilotKit. It provides a modern Next.js application
with an integrated restaurant finder agent that can find restaurants and book reservations

## CopilotKit A2UI Starter

Clone the repository:

```sh
git clone https://github.com/CopilotKit/CopilotKit.git
cd CopilotKit/examples/integrations/a2a-a2ui
```

Install dependencies:

```sh
npm install
```

Set your Gemini API key:

```sh
export GEMINI_API_KEY="your_gemini_api_key_here"
```

Run 

```sh
npm run dev
```

Go to `localhost:3000` and start prompting your AI agent. For example `Top 5 Chinese restaurants in New York`.

TODO: There's a bug currently on the client side.

## References

* [GitHub: CopilotKit <> A2A + A2UI Starter](https://github.com/CopilotKit/CopilotKit/tree/main/examples/integrations/a2a-a2ui)
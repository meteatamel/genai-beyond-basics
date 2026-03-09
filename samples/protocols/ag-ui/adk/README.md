# AG-UI with Agent Development Kit (ADK)

You can use ADK agents with AG-UI in a couple of ways. You can either start fresh with AG-UI's starter template or 
integrate CopilotKit into your existing ADK agent. Let's try both.

## AG-UI starter template for ADK

Create a new AG-UI frontend and a ADK backend with the starter template:

```sh
npx copilotkit@latest create -f adk -n new-agent
```

Install dependencies:

```sh
cd hello-agui-adk 
npm install
```

Create `agent/.env` file and add your Google API key:

```sh
export GOOGLE_API_KEY=your-google-api-key-here
```

Start both the UI and agent servers:

```sh
npm run dev
```

Navigate to `localhost:3000` and start prompting your AI agent.

## References

* [Docs: AG-UI + ADK](https://docs.copilotkit.ai/adk)
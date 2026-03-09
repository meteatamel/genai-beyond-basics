# AG-UI with Agent Development Kit (ADK)

You can use ADK agents with AG-UI in a couple of ways. You can either start fresh with AG-UI's starter template or 
integrate AG-UI into your existing ADK agent. Let's try both.

## AG-UI starter template for ADK

Easiest way is to use the AG-UI starter template that creates a new AG-UI frontend and a ADK backend.

Create with the starter template:

```sh
npx copilotkit@latest create -f adk -n starter-copilot-app-and-agent
```

Install dependencies:

```sh
cd starter-copilot-app-and-agent
npm install
```

Create `agent/.env` file and add your Google API key:

```sh
echo 'export GOOGLE_API_KEY=your-google-api-key-here' > agent/.env
```

Start both the UI and agent servers:

```sh
npm run dev
```

Navigate to `localhost:3000` and start prompting your AI agent.

## Add AG-UI to an existing ADK agent

Another way is to create your ADK agent (or use an existing one) and add AG-UI to it afterwards.

### Create the ADK agent

Let's use `adk create` to create an ADK agent:

```sh
uvx --from google-adk adk create my_agent \
    --model=gemini-2.5-flash \
    --api_key=your-gemini-api-key
```

Transition to `uv` and add ADK dependency:

```sh
cd my_agent
uv init
uv add google-adk
```

Test your agent:

```sh
uv run adk run .
```

You have an ADK agent ready now.

### Add AG-UI support to the ADK agent

Add `ag-ui-adk`, along with `uvicorn` and `fastapi` to your project:

```sh
uv add ag-ui-adk uvicorn fastapi
```

Expose your ADK agent via AG-UI by changing `main.py` to:

```python
from fastapi import FastAPI
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint
from agent import root_agent
from dotenv import load_dotenv

load_dotenv()

# Create ADK middleware agent instance
adk_agent = ADKAgent(
    adk_agent=root_agent,
    app_name="demo_app",
    user_id="demo_user",
    session_timeout_seconds=3600,
    use_in_memory_services=True
)

# Create FastAPI app
app = FastAPI()

# Add the ADK endpoint
add_adk_fastapi_endpoint(app, adk_agent, path="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
```

### Create CopilotKit frontend

Now, create a React-based CopilotKit frontend for the AG-UI enabled ADK agent.

At the top level:

```sh
npx create-next-app@latest my-copilot-app
cd my-copilot-app
```

Install CopilotKit packages: 

```sh
npm install @copilotkit/react-ui @copilotkit/react-core @copilotkit/runtime @ag-ui/client
```

Create an API route to connect CopilotKit to your ADK agent in `app/api/copilotkit/route.ts`:

```typescript
import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { HttpAgent } from "@ag-ui/client";
import { NextRequest } from "next/server";

const serviceAdapter = new ExperimentalEmptyAdapter();

const runtime = new CopilotRuntime({
  agents: {
    my_agent: new HttpAgent({ url: "http://localhost:8000/" }),
  }
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
```

Edit `app/layout.tsx` to wrap your application with CopilotKit provider:

```tsx
import { CopilotKit } from "@copilotkit/react-core"; 
import "@copilotkit/react-ui/v2/styles.css";
// ...
export default function RootLayout({ children }: {children: React.ReactNode}) {
  return (
    <html lang="en">
      <body>
        <CopilotKit runtimeUrl="/api/copilotkit" agent="my_agent">
          {children}
        </CopilotKit>
      </body>
    </html>
  );
}
```

Edit `app/page.tsx` to add the chat interface, the CopilotSidebar component to your page:

```tsx
import { CopilotSidebar } from "@copilotkit/react-core/v2"; 

export default function Page() {
  return (
    <main>
      <h1>Your App</h1>
      <CopilotSidebar />
    </main>
  );
}
```

### Test

From your agent directory, start the agent server at `localhost:8000`:

```sh
uv run main.py
```

From the frontend directory, start the development environment at `localhost:3000` 

```sh
npm run dev
```

Navigate to `localhost:3000` and start prompting your AI agent.

## References

* [Docs: AG-UI + ADK](https://docs.copilotkit.ai/adk)
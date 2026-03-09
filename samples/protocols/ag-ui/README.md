# Agent-User Interaction Protocol (AG-UI)

## Overview

AG-UI is an open, lightweight, event-based protocol, created by the [CopilotKit](https://www.copilotkit.ai/) team, that
standardizes how agent backends connect to agent frontends. Built for simplicity and flexibility, it enables
seamless integration between AI agents, real time user context, and user interfaces.

![AG-UI Protocol](https://github.com/user-attachments/assets/cd0376f3-0a3d-4cc3-a931-2b166c4efe5e)

## AG-UI vs. MCP, A2A

AG-UI is complementary to MCP and A2A:

* **MCP** gives agents tools
* **A2A** allows agents to communicate with other agents
* **AG-UI** brings agents into user-facing applications

![AG-UI, MCP, A2A](https://github.com/user-attachments/assets/41138f71-50be-4812-98aa-20e0ad595716)

## AG-UI vs. A2UI

Despite similar names, AG-UI and A2UI serve very different and complementary roles in the agentic application stack:

* **AG-UI** connects your user-facing application to any agentic backend.
* **A2UI** is a declarative Generative UI spec, originated by Google, which agents can use to return UI widgets as part
  of their responses.

![AG-UI, A2UI](images/agui-a2ui.png)

Use AG UI as the transport layer connecting your agent backend to your frontend, and A2UI as the format for generative
UI payload.

## Steps

Follow these steps to learn more:

* [AG-UI with Agent Development Kit (ADK)](./adk/)

## References

* [Docs: AG-UI protocol](https://docs.ag-ui.com/introduction)
* [GitHub: AG-UI protocol](https://github.com/ag-ui-protocol/ag-ui)
* [Docs: CopilotKit](https://docs.copilotkit.ai/)
* [AG-UI and A2UI](https://www.copilotkit.ai/ag-ui-and-a2ui)
* [Agent UI Ecosystem](https://a2ui.org/introduction/agent-ui-ecosystem/)

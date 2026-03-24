# Agent to UI Protocol (A2UI)

## Overview

[A2UI](https://a2ui.org/) is a generative UI protocol, from Google, that enables AI agents to generate rich,
interactive user interfaces across web, mobile, desktop. The idea with A2UI is that when a user asks a question to an
agent (e.g. "What are some good restaurants in New York?"), the agent can not only return the list of restaurants, 
but also return UI that displays the restaurants in a rich interactive format.

You can read [Core Concepts](https://a2ui.org/concepts/overview/) for the details of the protocol but here's a summary.

## Message types and format

A2UI defines a sequence of JSON messages that describe the UI and data for the UI:

```json
{
  "version": "v0.9",
  "createSurface": {
    "surfaceId": "main",
    "catalogId": "https://a2ui.org/specification/v0_9/basic_catalog.json"
  }
}
{
  "version": "v0.9",
  "updateComponents": {
    "surfaceId": "main",
    "components": [...]
  }
}
{
  "version": "v0.9",
  "updateDataModel": {
    "surfaceId": "main",
    "path": "/user",
    "value": { "name": "Alice" }
  }
}
```

There are 4 message types:

* **createSurface**: Create a new surface and specify its catalog.
* **updateComponents**: Add or update UI components in a surface.
* **updateDataModel**: Update application state.
* **deleteSurface**: Remove an UI surface.

You can see an example resturant booking message flow in [Restaurant Booking](https://a2ui.org/concepts/data-flow/#lifecycle-example-restaurant-booking)

## Components

A2UI defines a standard catalog of UI components organized by purpose:

* **Layout**: Row, Column, List - arrange other components
* **Display**: Text, Image, Icon, Video, Divider - show information
* **Interactive**: Button, TextField, CheckBox, DateTimeInput, Slider - user input
* **Container**: Card, Tabs, Modal - group and organize content

For the complete component gallery with examples, see [Component Reference](https://a2ui.org/reference/components/)

## Transport Options

A2UI is transport-agnostic, meaning any mechanism that can deliver JSON messages works. Currently, A2A and AG UI are supported with REST API, WebSockets, and SSE as planned or proposed. See [transports](https://a2ui.org/concepts/transports/) 
on the latest supported transports.

## A2UI vs. AG-UI

Despite similar names, AG-UI and A2UI serve very different and complementary roles in the agentic application stack:

* **AG-UI** connects your user-facing application to any agentic backend.
* **A2UI** is a declarative generative UI spec, which agents can use to return UI widgets as part of their responses.

![AG-UI and A2UI](../images/agui-and-a2ui.png)

See [AG-UI and Generative UI Specs](https://docs.ag-ui.com/concepts/generative-ui-specs) and [AG-UI and
A2UI](https://www.copilotkit.ai/ag-ui-and-a2ui) for more details.

## Steps

Follow these steps to learn more:

* [A2UI with Agent Development Kit (ADK)](./adk/)
* [A2UI with CopilotKit and Agent Development Kit (ADK)](./copilotkit)

## References

* [Docs: A2UI protocol](https://a2ui.org/)
* [GitHub: A2UI](https://github.com/google/A2UI) & [A2UI protocol spec](https://github.com/google/A2UI/tree/main/specification)
* [Blog: Introducing A2UI: An open project for agent-driven interfaces](https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/)
* [AG-UI and A2UI](https://www.copilotkit.ai/ag-ui-and-a2ui)
* [AG-UI and Generative UI Specs](https://docs.ag-ui.com/concepts/generative-ui-specs)
* [Agent UI Ecosystem](https://a2ui.org/introduction/agent-ui-ecosystem/)
---
* [CopilotKit Generative UI](https://www.copilotkit.ai/generative-ui)
* [CopilotKit + A2UI](https://docs.copilotkit.ai/a2a/generative-ui/declarative-a2ui)
* [CopilotKit A2UI Composer](https://a2ui-composer.ag-ui.com/)
* [GitHub: CopilotKit <> A2A + A2UI Starter](https://github.com/CopilotKit/CopilotKit/tree/main/examples/integrations/a2a-a2ui)
---
* [YouTube: A2UI: The Protocol That Makes AI Design Functional UIs](https://youtu.be/PS8mZFhodfE)
* [YouTube: AI Agents Can Now Build Their Own UI in Real Time](https://youtu.be/MD8VQzvMVek)
---

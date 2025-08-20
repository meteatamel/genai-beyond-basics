# Echo Agent - CSharp

A simple echo agent that demonstrates the core concepts of A2A protocol. This agent receives messages and respond by echoing them back, providing a clear example of how A2A communication flows.

See [A2AAgent](./A2AAgent/) for the A2A enabled agent and [A2AClient](./A2AClient/) for the client
to test it.

Start the agent:

```shell
cd A2AAgent
dotnet run

info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5209
info: Microsoft.Hosting.Lifetime[0]
      Application started. Press Ctrl+C to shut down.
info: Microsoft.Hosting.Lifetime[0]
      Hosting environment: Development
info: Microsoft.Hosting.Lifetime[0]
      Content root path: /Users/atamel/dev/github/meteatamel/genai-beyond-basics/samples/protocols/a2a/echo/csharp/A2AAgent
```

In a separate terminal, test the agent:

```shell
cd A2AClient/

Connected to agent: Echo Agent
Description: An agent that will echo every message it receives.
Streaming support: True

=== Non-Streaming Communication ===
Received response: Echo: Hello from the A2A client!

=== Streaming Communication ===
Received streaming chunk: Echo: Hello from the A2A client!
```

## References

* [Blog: Building AI Agents with the A2A .NET SDK](https://devblogs.microsoft.com/foundry/building-ai-agents-a2a-dotnet-sdk/)
* [A2A .NET SDK](https://github.com/a2aproject/a2a-dotnet)
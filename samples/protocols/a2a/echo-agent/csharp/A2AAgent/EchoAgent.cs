using A2A;

namespace A2AAgent;

// This is a simple echo agent that demonstrates the core concepts of A2A protocol.
// When it receives messages, it simply responds by echoing them back.
public sealed class EchoAgent : IAgentHandler
{
    public async Task ExecuteAsync(
        RequestContext context,
        AgentEventQueue eventQueue,
        CancellationToken cancellationToken)
    {
        var responder = new MessageResponder(eventQueue, context.ContextId);
        await responder.ReplyAsync($"Echo: {context.UserText}", cancellationToken: cancellationToken);
    }

    public static AgentCard GetAgentCard(string agentUrl) => new()
    {
        Name = "Echo Agent",
        Description = "An agent that will echo every message it receives.",
        Version = "1.0.0",
        SupportedInterfaces =
        [
            new AgentInterface
            {
                Url = agentUrl,
                ProtocolBinding = "JSONRPC",
                ProtocolVersion = "1.0"
            }
        ],
        DefaultInputModes = ["text/plain"],
        DefaultOutputModes = ["text/plain"],
        Capabilities = new AgentCapabilities { Streaming = true },
        Skills =
        [
            new AgentSkill
            {
                Id = "echo",
                Name = "Echo tool",
                Description = "Echos every received message back to the user.",
                Tags = ["echo"],
                Examples = ["hello", "how are you"]
            }
        ],
    };
}
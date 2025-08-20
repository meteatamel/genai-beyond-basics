using A2A;

namespace A2AAgent;

// This is a simple echo agent that demonstrates the core concepts of A2A protocol.
// This agent connects to the A2A framework with the attach method.
// When it receives messages, it simply respods by echoing them back.
// When it receives an agent card query, it returns a simple agent card with its details.
public class EchoAgent
{
    // Connect the agent to the A2A framework
    public void Attach(ITaskManager taskManager)
    {
        taskManager.OnMessageReceived = ProcessMessageAsync;
        taskManager.OnAgentCardQuery = GetAgentCardAsync;
    }

    private async Task<Message> ProcessMessageAsync(MessageSendParams messageSendParams, CancellationToken ct)
    {
        // Get incoming message text
        string request = messageSendParams.Message.Parts.OfType<TextPart>().First().Text;

        // Create and return an echo message
        return new Message()
        {
            Role = MessageRole.Agent,
            MessageId = Guid.NewGuid().ToString(),
            ContextId = messageSendParams.Message.ContextId,
            Parts = [new TextPart() { Text = $"Echo: {request}" }]
        };
    }

    private async Task<AgentCard> GetAgentCardAsync(string agentUrl, CancellationToken cancellationToken)
    {
        // Create and return a simple agent card with its details
        AgentSkill skill = new()
        {
            Id = "echo",
            Name = "Echo tool",
            Description = "Echos every received message back to the user.",
            Tags = ["echo"],
            Examples = ["hello", "how are you"]
        };

        return new AgentCard()
        {
            Name = "Echo Agent",
            Description = "An agent that will echo every message it receives.",
            Url = agentUrl,
            Version = "1.0.0",
            DefaultInputModes = ["text"],
            DefaultOutputModes = ["text"],
            Capabilities = new AgentCapabilities() { Streaming = true },
            Skills = [skill],
        };
    }
}
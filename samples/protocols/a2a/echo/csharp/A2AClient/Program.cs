using A2A;
using System.Net.ServerSentEvents;

// 1. Get the agent card
A2ACardResolver cardResolver = new(new Uri("http://localhost:5209/"));
AgentCard echoAgentCard = await cardResolver.GetAgentCardAsync();

Console.WriteLine($"Connected to agent: {echoAgentCard.Name}");
Console.WriteLine($"Description: {echoAgentCard.Description}");
Console.WriteLine($"Streaming support: {echoAgentCard.Capabilities?.Streaming}");

// 2. Create an A2A client to communicate with the agent using url from the agent card
A2AClient agentClient = new(new Uri(echoAgentCard.Url));

// 3. Create a message to send to the agent
Message userMessage = new()
{
    Role = MessageRole.User,
    MessageId = Guid.NewGuid().ToString(),
    Parts = [new TextPart { Text = "Hello from the A2A client!" }]
};

// 4. Send the message using non-streaming API
Console.WriteLine("\n=== Non-Streaming Communication ===");
Message agentResponse = (Message)await agentClient.SendMessageAsync(new MessageSendParams { Message = userMessage });
Console.WriteLine($"Received response: {((TextPart)agentResponse.Parts[0]).Text}");

// 5. Send the message using streaming API
Console.WriteLine("\n=== Streaming Communication ===");
await foreach (SseItem<A2AEvent> sseItem in agentClient.SendMessageStreamAsync(new MessageSendParams { Message = userMessage }))
{
    Message streamingResponse = (Message)sseItem.Data;
    Console.WriteLine($"Received streaming chunk: {((TextPart)streamingResponse.Parts[0]).Text}");
}
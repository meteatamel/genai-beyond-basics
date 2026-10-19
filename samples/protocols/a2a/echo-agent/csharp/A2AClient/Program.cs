using A2A;

// 1. Get the agent card
A2ACardResolver cardResolver = new(new Uri("http://localhost:5209"));
AgentCard echoAgentCard = await cardResolver.GetAgentCardAsync();

Console.WriteLine($"Connected to agent: {echoAgentCard.Name}");
Console.WriteLine($"Description: {echoAgentCard.Description}");
Console.WriteLine($"Streaming support: {echoAgentCard.Capabilities?.Streaming}");

// 2. Create an A2A client to communicate with the agent using url from the agent card
A2AClient agentClient = new(new Uri(echoAgentCard.SupportedInterfaces[0].Url));

// 3. Create a message to send to the agent
Message userMessage = new()
{
    Role = Role.User,
    MessageId = Guid.NewGuid().ToString(),
    Parts = [Part.FromText("Hello from the A2A client!")]
};

// 4. Send the message using non-streaming API
Console.WriteLine("\n=== Non-Streaming Communication ===");
SendMessageResponse agentResponse = await agentClient.SendMessageAsync(new SendMessageRequest { Message = userMessage });
Console.WriteLine($"Received response: {agentResponse.Message!.Parts[0].Text}");

// 5. Send the message using streaming API
Console.WriteLine("\n=== Streaming Communication ===");
await foreach (StreamResponse streamResponse in agentClient.SendStreamingMessageAsync(new SendMessageRequest { Message = userMessage }))
{
    if (streamResponse.Message is { } message)
    {
        Console.WriteLine($"Received streaming chunk: {message.Parts[0].Text}");
    }
}
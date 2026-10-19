using A2A;
using A2A.AspNetCore;
using A2AAgent;

WebApplicationBuilder builder = WebApplication.CreateBuilder(args);

// Register the EchoAgent and its agent card with DI
builder.Services.AddA2AAgent<EchoAgent>(EchoAgent.GetAgentCard("http://localhost:5209/agent"));

WebApplication app = builder.Build();

// Expose agent via A2A protocol
app.MapA2A("/agent");

// Map well-known agent card at /.well-known/agent-card.json for discovery
AgentCard card = app.Services.GetRequiredService<AgentCard>();
app.MapWellKnownAgentCard(card);

await app.RunAsync();
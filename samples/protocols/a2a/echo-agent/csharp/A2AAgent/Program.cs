using A2A;
using A2A.AspNetCore;
using A2AAgent;
using Microsoft.AspNetCore.Builder;

WebApplicationBuilder builder = WebApplication.CreateBuilder(args);
WebApplication app = builder.Build();

// Create and attach the EchoAgent to the TaskManager
EchoAgent agent = new EchoAgent();
TaskManager taskManager = new TaskManager();
agent.Attach(taskManager);

// Expose agent via A2A protocol
app.MapA2A(taskManager, "/agent");
await app.RunAsync();
class EchoAgent:
    """An agent that simply echoes back the received text message.

    In a real-world agent, you'd use a framework and use an LLM to do something more complicated
    """

    async def invoke(self, text_message) -> str:
        return f"Echo: {text_message}"


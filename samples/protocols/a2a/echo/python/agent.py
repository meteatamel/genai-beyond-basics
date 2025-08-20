
class EchoAgent:
    """Echo Agent."""

    async def invoke(self, text_message) -> str:
        return f"Echo: {text_message}"


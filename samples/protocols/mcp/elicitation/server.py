from dataclasses import dataclass
from typing import Literal
from fastmcp import FastMCP, Context
from fastmcp.server.elicitation import (
    AcceptedElicitation,
    DeclinedElicitation,
    CancelledElicitation,
)

mcp = FastMCP("Elicitation Server")

# No response type examples

@mcp.tool
async def approve_action(ctx: Context) -> str:
    """Simple tool that asks for user approval. No response."""
    result = await ctx.elicit(
        "Approve this action?",
        response_type=None)

    if result.action == "accept":
        print(f"Accepted!")
        return "Action approved!"
    print("Declined or Cancelled!")
    return "Action not approved!"


@mcp.tool
async def approve_action_with_match(ctx: Context) -> str:
    """Tool that asks for user approval using pattern matching. No response."""
    result = await ctx.elicit(
        "Approve this action?",
        response_type=None)

    match result:
        case AcceptedElicitation():
            print(f"Accepted!")
            return "Action approved!"
        case DeclinedElicitation() | CancelledElicitation():
            print("Declined or Cancelled!")
            return "Action not approved!"


# Scalar (string, int, boolean) response type example

@mcp.tool
async def greet_user(ctx: Context) -> str:
    """ Tool that greets user by name. Simple string response."""
    result = await ctx.elicit("What's your name?", response_type=str)

    if result.action == "accept":
        print(f"Accepted name: {result.data}")
        return f"Hello, {result.data}!"

    print("Declined or Cancelled!")
    return "No name provided."


# Constrained response type example

@mcp.tool
async def set_priority(ctx: Context) -> str:
    """Tool that sets priority level. Constrained options."""
    result = await ctx.elicit(
        "What priority level (low, medium, high)?",
        response_type=["low", "medium", "high"],
    )

    if result.action == "accept":
        print(f"Accepted priority: {result.data}")
        return f"Priority set to {result.data}."

    print("Declined or Cancelled!")
    return "No priority set."


# Structured response type example

@dataclass
class UserInfo:
    name: str
    age: int

@mcp.tool
async def collect_user_info(ctx: Context) -> str:
    """Collect user information through interactive prompts."""
    result = await ctx.elicit(
        message="Please provide your name and age",
        response_type=UserInfo
    )

    if result.action == "accept":
        user = result.data
        return f"Hello {user.name}, you are {user.age} years old"
    elif result.action == "decline":
        return "Information not provided"
    else:  # cancel
        return "Operation cancelled"


# Multi-turn elicitation example

@mcp.tool
async def plan_meeting(ctx: Context) -> str:
    """Plan a meeting by gathering details step by step."""

    # Get meeting title
    title_result = await ctx.elicit("What's the meeting title?", response_type=str)
    if title_result.action != "accept":
        return "Meeting planning cancelled"

    # Get duration
    duration_result = await ctx.elicit("Duration in minutes?", response_type=int)
    if duration_result.action != "accept":
        return "Meeting planning cancelled"

    # Get priority
    priority_result = await ctx.elicit(
        "Is this urgent? (yes/no)",
        response_type=Literal["yes", "no"]
    )
    if priority_result.action != "accept":
        return "Meeting planning cancelled"

    urgent = priority_result.data == "yes"
    return f"Meeting '{title_result.data}' planned for {duration_result.data} minutes (urgent: {urgent})"


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8080, path="/mcp")
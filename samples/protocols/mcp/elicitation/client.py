import asyncio
from fastmcp import Client
from fastmcp.client.elicitation import ElicitResult


# No response type examples

async def elicitation_handler_approve_action(message: str, response_type: type, params, context):
    print(f"Server asks: {message}")

    try:
        user_input = input(f"Your response: ")
        if user_input.lower() in ["no", "n"]:
            return ElicitResult(action="decline")
        return ElicitResult(action="accept")

    except KeyboardInterrupt:
        print("Operation cancelled by user")
        return ElicitResult(action="cancel")
    except Exception as e:
        print(f"Error handling input: {e}")
        return ElicitResult(action="decline")

async def approve_action():
    client = Client("http://127.0.0.1:8080/mcp/", elicitation_handler=elicitation_handler_approve_action)
    async with client:
        result = await client.call_tool("approve_action")
        print(f"Tool result: {result.content[0].text}")


async def approve_action_with_match():
    client = Client("http://127.0.0.1:8080/mcp/", elicitation_handler=elicitation_handler_approve_action)
    async with client:
        result = await client.call_tool("approve_action_with_match")
        print(f"Tool result: {result.content[0].text}")


# Scalar (string, int, boolean) response type example

async def elicitation_handler_greet_user(message: str, response_type: type, params, context):
    print(f"Server asks: {message}")

    try:
        user_input = input(f"Your response: ")
        if not user_input:
            return ElicitResult(action="decline")

        return response_type(value=user_input)

    except KeyboardInterrupt:
        print("Operation cancelled by user")
        return ElicitResult(action="cancel")
    except Exception as e:
        print(f"Error handling input: {e}")
        return ElicitResult(action="decline")

async def greet_user():
    client = Client("http://127.0.0.1:8080/mcp/", elicitation_handler=elicitation_handler_greet_user)
    async with client:
        result = await client.call_tool("greet_user")
        print(f"Tool result: {result.content[0].text}")


# Constrained response type example

async def elicitation_handler_set_priority(message: str, response_type: type, params, context):
    print(f"Server asks: {message}")

    try:
        user_input = input(f"Your response: ")
        if user_input.lower() not in ["low", "medium", "high"]:
            return ElicitResult(action="decline")

        #return ElicitResult(action="accept", content=response_type(value=user_input))
        return response_type(value=user_input)

    except KeyboardInterrupt:
        print("Operation cancelled by user")
        return ElicitResult(action="cancel")
    except Exception as e:
        print(f"Error handling input: {e}")
        return ElicitResult(action="decline")

async def set_priority():
    client = Client("http://127.0.0.1:8080/mcp/", elicitation_handler=elicitation_handler_set_priority)
    async with client:
        result = await client.call_tool("set_priority")
        print(f"Tool result: {result.content[0].text}")


# Structured response type example

async def elicitation_handler_collect_user_info(message: str, response_type: type, params, context):
    print(f"Server asks: {message}")

    try:
        name = input("Enter your name: ").strip()
        if not name:
            print("No name provided")
            return ElicitResult(action="decline")

        age_input = input("Enter your age: ").strip()
        if not age_input.isdigit():
            print("Invalid age provided")
            return ElicitResult(action="decline")
        age = int(age_input)

        return response_type(name=name, age=age)

    except KeyboardInterrupt:
        print("Operation cancelled by user")
        return ElicitResult(action="cancel")
    except Exception as e:
        print(f"Error handling input: {e}")
        return ElicitResult(action="decline")


async def collect_user_info():
    client = Client("http://127.0.0.1:8080/mcp/", elicitation_handler=elicitation_handler_collect_user_info)
    async with client:
        result = await client.call_tool("collect_user_info")
        print(f"Tool result: {result.content[0].text}")


# Multi-turn elicitation example

async def elicitation_handler_plan_meeting(message: str, response_type: type, params, context):
    print(f"Server asks: {message}")

    try:
        user_input = input("Your response: ").strip()
        if not user_input:
            print("No input provided")
            return ElicitResult(action="decline")

        return response_type(value=user_input)

    except KeyboardInterrupt:
        print("Operation cancelled by user")
        return ElicitResult(action="cancel")
    except Exception as e:
        print(f"Error handling input: {e}")
        return ElicitResult(action="decline")


async def plan_meeting():
    client = Client("http://127.0.0.1:8080/mcp/", elicitation_handler=elicitation_handler_plan_meeting)
    async with client:
        result = await client.call_tool("plan_meeting")
        print(f"Tool result: {result.content[0].text}")


async def main():

    while True:
        print("\nAvailable tools:")
        print("1. approve_action")
        print("2. approve_action_with_match")
        print("3. greet_user")
        print("4. set_priority")
        print("5. collect_user_info")
        print("6. plan_meeting")

        choice = input("\nSelect a tool: ").strip()

        if choice == "1":
            await approve_action()
        elif choice == "2":
            await approve_action_with_match()
        elif choice == "3":
            await greet_user()
        elif choice == "4":
            await set_priority()
        elif choice == "5":
            await collect_user_info()
        elif choice == "6":
            await plan_meeting()
            break
        else:
            print("Goodbye!")
            break


if __name__ == "__main__":
    asyncio.run(main())
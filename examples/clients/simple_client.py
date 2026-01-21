import asyncio
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_client(server_script_path: str):
    """
    Connects to an MCP server via stdio, lists tools, and exits.
    """
    # Use AsyncExitStack to manage the lifespan of asynchronous resources
    async with AsyncExitStack() as stack:
        # Define the server parameters, assuming it's a Python script
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
            env={"-Xfrozen_modules": "off", "PYDEVD_DISABLE_FILE_VALIDATION": "1","PYTHONPATH": "C:\\eclipse-2025-12\\eclipse\\plugins\\org.python.pydev.core_13.1.0.202509210817\\pysrc\\pydev_sitecustomize;C:\\Users\\slewi\\git\\python-sdk\\src;C:\\Users\\slewi\\git\\python-sdk\\examples;C:\\Python313\\DLLs;C:\\Python313\\Lib;C:\\Python313;C:\\Python313\\Lib\\site-packages;C:\\Python313\\Lib\\site-packages\\win32;C:\\Python313\\Lib\\site-packages\\win32\\lib;C:\\Python313\\Lib\\site-packages\\Pythonwin" } # Optional: Pass environment variables if needed
        )

        # Connect to the server over stdio
        stdio_transport = await stack.enter_async_context(stdio_client(server_params))
        
        # Create an MCP client session
        # stdio_transport returns a (reader, writer) pair
        session = await stack.enter_async_context(ClientSession(stdio_transport[0], stdio_transport[1]))
        
        # Initialize the session
        await session.initialize()

        # List available tools from the server
        response = await session.list_tools()
        tools = response.tools
        print(f"\nConnected to server with tools: {[tool for tool in tools]}")
        
        # Example of calling a tool (you would replace this with your logic)
        # if "example_tool_name" in [tool.name for tool in tools]:
        #     result = await session.call_tool("example_tool_name", {"arg1": "value1"})
        #     print(f"Tool call result: {result.output}")

if __name__ == "__main__":
    # Specify the path to your server script (e.g., in the same directory)
    # You will need to create a server.py file separately
    server_path = "C:\\Users\\slewi\\git\\python-sdk\\examples\\servers\\simple-tool\\mcp_simple_tool\\server.py" 
    try:
        asyncio.run(run_client(server_path))
    except FileNotFoundError:
        print(f"Error: Server script not found at {server_path}")
        print("Please create a 'server.py' file to run this example.")

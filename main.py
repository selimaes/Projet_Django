from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="MCP-3IA4")

@mcp.tool()
def say_hello(name: str) -> str:
    return f"Hello, {name}!"

@mcp.tool()
def add(a: float, b: float) -> float:
    return a + b

@mcp.tool()
def subtract(a: float, b: float) -> float:
    return a - b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> str | float:
    if b == 0:
        return "Erreur: Division par zéro"
    return a / b

if __name__ == "__main__":
    mcp.run(transport="stdio")

from mcp.server.fastmcp import FastMCP


## initialize
mcp = FastMCP('Math')


@mcp.tool()
def add(a:int, b:int) -> int: 
    """
    Add the two numbers
    """
    return a+b

@mcp.tool()
def multiply(a:int, b:int) -> int: 
    """
    Multiply two numbers
    """
    return a*b


"""
let's here understand what the stdio is: The transport "stdio" tell the server to:
Use the standard input/output (stdin and stdout) to receive and respond to tool function calls 
"""
if __name__=="__main__":
    mcp.run(transport='stdio')
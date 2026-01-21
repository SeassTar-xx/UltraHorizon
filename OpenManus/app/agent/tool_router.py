import re
import logging
from OpenManus.app.tool.tool_collection import ToolCollection

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def should_call_tool(text):
    """
    Check if the text contains a tool call.
    :param text: The text output from the LLM.
    :return: True if a tool call is detected, False otherwise.
    """
    return "CALL_TOOL:" in text

def parse_tool_call(text):
    """
    Parse the tool call from the text.
    :param text: The text output from the LLM.
    :return: A tuple (tool_name, params) if a tool call is detected, None otherwise.
    """
    match = re.search(r'CALL_TOOL:\s*<(\w+)>\((.*?)\)', text)
    if match:
        tool_name = match.group(1)
        params = match.group(2)
        return tool_name, params
    return None

def route_tool_call(text, agent_context):
    """
    Route the tool call by executing the tool and appending the result to the agent context.
    :param text: The text output from the LLM.
    :param agent_context: The agent's context to append the tool result.
    :return: None
    """
    if should_call_tool(text):
        tool_call = parse_tool_call(text)
        if tool_call:
            tool_name, params = tool_call
            logger.info(f"Tool call detected: {tool_name} with params: {params}")
            try:
                result = execute_sync(tool_name, params)
                logger.info(f"Tool result: {result}")
                agent_context.append(f"TOOL_RESULT: {result}")
            except Exception as e:
                logger.error(f"Error executing tool {tool_name}: {e}")
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain import hub
from langchain.tools import BaseTool
from langchain.tools.tavily_search import TavilySearchResults
from langchain.pydantic_v1 import BaseModel,Field
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from typing import Optional, Type, Any
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from fastapi import FastAPI
from langserve import add_routes


os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("langchain")
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
os.environ["TAVILY_API_KEY"] = os.environ.get("tavily")

prompt = hub.pull("hwchase17/openai-tools-agent")

model = ChatOpenAI(model="gpt-3.5-turbo")

class CustomInput(BaseModel):
    
    a: float = Field(description = "First number. Should be a float or integer")
    b: float = Field(description = "Second number. Should be a float or integer")

class Addition(BaseTool):
    
    name = "Addition_tool"
    description = "Used for performing addition operation between two numbers"
    args_schema: Type[BaseModel] = CustomInput
        
    def _run(self, a: float, b: float, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        "Use the tool"
        return a+b
    
    async def _arun(
        self,
        a: float,
        b: float,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return a+b


class Multiply(BaseTool):
    
    name = "Multiply_tool"
    description = "Used for performing multiplication operation between two numbers"
    args_schema: Type[BaseModel] = CustomInput
        
    def _run(self, a: float, b: float, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        "Use the tool"
        return a*b
    
    async def _arun(
        self,
        a: float,
        b: float,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        return a*b
    

add = Addition()
multiply = Multiply()
tavily = TavilySearchResults()

tools = [add,multiply,tavily]
llm_with_tools = model.bind_tools(tools=tools)

agent = (
    {"input": lambda x:x["input"], "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"])}
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
)

agent_exe = AgentExecutor(agent=agent,tools=tools,verbose=True,handle_parsing_errors=True)

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using LangChain's Runnable interfaces",
)

class Input(BaseModel):
    input : str

class Output(BaseModel):
    output : Any

#print(agent_exe.with_types(input_type=Input,output_type=Output).with_config(
#        {"run_name" : "agent"}
#        ).invoke({'input':'what is the sum of 2 and 3'}))

add_routes(
    app,
    agent_exe.with_types(input_type=Input,output_type=Output).with_config(
        {"run_name" : "agent"}
        ),
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)



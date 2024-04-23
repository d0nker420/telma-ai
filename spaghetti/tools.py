from typing import Optional, Type
from pydantic import BaseModel
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool


cmb_classes = []




class ShowClasses(BaseTool):
    name = "show_cmb_classes"
    description = "use this tool when you want to show all CMB classes you defined already"
    args_schema: Type[BaseModel] = None

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return str(cmb_classes)

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")


class AddClass(BaseTool):
    name = "add_cmb_class"
    description = "use this tool to add a new CMB class. Just explain what this class does in text."
    args_schema: Type[BaseModel] = None

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        cmb_classes.append(query)
        return "Class added successfully"

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")


class EndConversation(BaseTool):
    name = "end_conversation"
    description = "When you have enough data about the bot and CMB classes, use this tool to end conversation."
    args_schema: Type[BaseModel] = None

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        print('#'*10, 'Conversation ended', '#'*10)
        print('CMB classes:', cmb_classes)
        # TODO: convert CMB STR to CMB JSON

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

from typing import Optional, Type
from pydantic import BaseModel


cmb_classes = []




class ShowClasses(BaseTool):
    name = "show_cmb_classes"
    description = "use this tool when you want to show all CMB classes you defined already"
    args_schema: Type[BaseModel] = None

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return "LangChain"

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")

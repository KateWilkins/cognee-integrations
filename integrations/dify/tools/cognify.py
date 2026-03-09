from collections.abc import Generator
from typing import Any

import httpx
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class CognifyTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        base_url = self.runtime.credentials["base_url"].rstrip("/")
        api_key = self.runtime.credentials["api_key"]

        datasets_str = tool_parameters["datasets"]
        datasets = [d.strip() for d in datasets_str.split(",") if d.strip()]

        if not datasets:
            error_msg = "At least one dataset name is required"
            yield self.create_json_message({"error": error_msg})
            yield self.create_text_message(error_msg)
            return

        try:
            response = httpx.post(
                f"{base_url}/cognify",
                json={"datasets": datasets},
                headers={
                    "X-Api-Key": api_key,
                    "Content-Type": "application/json",
                },
                timeout=1200,
            )
            response.raise_for_status()
            result = response.json()

            yield self.create_json_message(result)
            yield self.create_variable_message("datasets", ", ".join(datasets))
            yield self.create_text_message(
                f"Successfully cognified dataset(s): {', '.join(datasets)}"
            )
        except httpx.HTTPStatusError as e:
            error_msg = f"Cognee API error {e.response.status_code}: {e.response.text}"
            yield self.create_json_message({"error": error_msg})
            yield self.create_text_message(error_msg)
        except Exception as e:
            error_msg = f"Failed to cognify: {str(e)}"
            yield self.create_json_message({"error": error_msg})
            yield self.create_text_message(error_msg)

from collections.abc import Generator
from typing import Any

import httpx
from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class SearchTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        base_url = self.runtime.credentials["base_url"].rstrip("/")
        api_key = self.runtime.credentials["api_key"]

        query = tool_parameters["query"]
        datasets_str = tool_parameters["datasets"]
        search_type = tool_parameters.get("search_type", "GRAPH_COMPLETION")
        top_k = tool_parameters.get("top_k", 10)

        datasets = [d.strip() for d in datasets_str.split(",") if d.strip()]

        if not datasets:
            error_msg = "At least one dataset name is required"
            yield self.create_json_message({"error": error_msg})
            yield self.create_text_message(error_msg)
            return

        try:
            response = httpx.post(
                f"{base_url}/search",
                json={
                    "searchType": search_type,
                    "datasets": datasets,
                    "query": query,
                    "topK": int(top_k),
                },
                headers={
                    "X-Api-Key": api_key,
                    "Content-Type": "application/json",
                },
                timeout=120,
            )
            response.raise_for_status()
            result = response.json()

            yield self.create_json_message(result)

            if isinstance(result, list):
                text_parts = [f"Found {len(result)} result(s):\n"]
                for i, item in enumerate(result, 1):
                    if isinstance(item, dict):
                        content = item.get("content", item.get("text", str(item)))
                        text_parts.append(f"{i}. {content}")
                    else:
                        text_parts.append(f"{i}. {item}")
                formatted = "\n".join(text_parts)
                yield self.create_variable_message("results_count", len(result))
                yield self.create_variable_message("results_text", formatted)
                yield self.create_text_message(formatted)
            else:
                yield self.create_variable_message("results_count", 1)
                yield self.create_variable_message("results_text", str(result))
                yield self.create_text_message(f"Search results: {result}")
        except httpx.HTTPStatusError as e:
            error_msg = f"Cognee API error {e.response.status_code}: {e.response.text}"
            yield self.create_json_message({"error": error_msg})
            yield self.create_text_message(error_msg)
        except Exception as e:
            error_msg = f"Search failed: {str(e)}"
            yield self.create_json_message({"error": error_msg})
            yield self.create_text_message(error_msg)

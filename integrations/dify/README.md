## Cognee

**Author:** cognee_team
**Version:** 0.0.1
**Type:** tool

### Description

Cognee is a knowledge graph plugin for Dify. It lets you ingest text data into datasets, build knowledge graphs with the Cognify engine, and search across them using graph-based completion, chain-of-thought reasoning, or retrieval-augmented generation.

### Setup

1. Get your API key and base URL from your [Cognee Cloud](https://www.cognee.ai) dashboard.
2. Install the plugin in your Dify workspace.
3. Configure the plugin with your **Base URL** (e.g. `https://tenant-xxx.cloud.cognee.ai/api`) and **API Key**.

### Tools

#### Add Data

Add text data to a named Cognee dataset. Text can contain multiple items separated by newlines.

**Parameters:**
- **Dataset Name** (required) - Name of the target dataset
- **Text Data** (required) - Text content to add

#### Cognify

Build a knowledge graph from one or more datasets. This processes the ingested data and may take several minutes depending on data volume.

**Parameters:**
- **Datasets** (required) - Comma-separated list of dataset names to process

#### Search

Search the Cognee knowledge graph for relevant information.

**Parameters:**
- **Query** (required) - Natural language search query
- **Datasets** (required) - Comma-separated list of dataset names to search
- **Search Type** (required) - One of:
  - `GRAPH_COMPLETION` - Knowledge graph search (default)
  - `GRAPH_COMPLETION_COT` - Chain-of-thought reasoning
  - `RAG_COMPLETION` - Retrieval-augmented generation
- **Top K** (optional) - Maximum number of results (default: 10)

#### Delete Dataset

Delete an entire dataset and all its data permanently.

**Parameters:**
- **Dataset ID** (required) - UUID of the dataset to delete

#### Delete Data

Delete a specific data item from a dataset.

**Parameters:**
- **Dataset ID** (required) - UUID of the dataset
- **Data ID** (required) - UUID of the data item to delete

### Usage in Dify Workflows

1. Use **Add Data** to ingest text into a dataset.
2. Use **Cognify** to build the knowledge graph from that dataset.
3. Use **Search** before LLM calls to provide relevant context from the knowledge graph.
4. Use **Delete Dataset** or **Delete Data** to manage your datasets.

### Links

- [Cognee Website](https://www.cognee.ai)
- [Cognee Documentation](https://docs.cognee.ai)
- [GitHub](https://github.com/topoteretes/cognee)

# MCP client setup

This guide documents the tested stdio setup for `novel-creation-mcp`.

## Prerequisites

- Python 3.11 or a compatible Python 3 runtime.
- A local clone of this repository.
- Dependencies installed from `requirements.txt`, which uses
  `constraints.txt` for pinned transitive versions.

## Install dependencies

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS or Linux:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
```

## Claude Desktop or Cursor

Use the virtual-environment Python executable and an absolute path to
`server.py`.

Windows example:

```json
{
  "mcpServers": {
    "novel-creation": {
      "command": "D:\\path\\to\\novel-creation-mcp\\.venv\\Scripts\\python.exe",
      "args": [
        "D:\\path\\to\\novel-creation-mcp\\server.py"
      ],
      "cwd": "D:\\path\\to\\novel-creation-mcp"
    }
  }
}
```

macOS or Linux example:

```json
{
  "mcpServers": {
    "novel-creation": {
      "command": "/path/to/novel-creation-mcp/.venv/bin/python",
      "args": [
        "/path/to/novel-creation-mcp/server.py"
      ],
      "cwd": "/path/to/novel-creation-mcp"
    }
  }
}
```

## Validate the server

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe verify_setup.py
.\.venv\Scripts\python.exe -m pytest -q
```

macOS or Linux:

```bash
./.venv/bin/python verify_setup.py
./.venv/bin/python -m pytest -q
```

## Public tools

The current release candidate registers these 12 public tools:

- `search_knowledge`
- `get_case_study`
- `get_mythology`
- `get_template`
- `get_methodology`
- `generate_worldbuilding_prompt`
- `analyze_power_system`
- `generate_character`
- `generate_plot`
- `analyze_writing`
- `suggest_titles`
- `generate_dialogue`

## Troubleshooting

- If the client cannot start the server, verify that `command`, `args`, and
  `cwd` are absolute paths for the same local clone.
- If imports fail, reinstall dependencies from the repository root.
- If a tool returns an empty-result message, check the current public content
  boundary in `README.md` and `CONTENT_POLICY.md`.

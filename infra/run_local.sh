# infra/run_local.sh
# Unix: start model server and MCP server in separate terminals (or use tmux)
uvicorn ai.predict_service:app --port 8501 &
python -m src.mcp_server

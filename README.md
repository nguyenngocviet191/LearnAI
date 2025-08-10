# Learn AI

## 1. LLM from Scratch

## 2. LLM train model

## 3. AI agent

### Repo tham khảo
* Thư viện
- https://github.com/agno-agi/agno
- https://github.com/camel-ai/camel

* Dự án
- https://github.com/Shubhamsaboo/awesome-llm-apps
- https://github.com/OpenManus

## 4. Automation

## 5. Other

## Testing

This project includes comprehensive unit tests for the AI agent functionality.

### Running Tests

**Quick start:**
```bash
./run_tests.sh
```

**Install test dependencies:**
```bash
pip install pytest pytest-asyncio pytest-mock
```

**Run specific test suites:**
```bash
# Agent-app tests
cd agent/agno_agi/agent-app
python -m pytest tests/ -v

# Basic agent tests  
cd agent/agno_agi
python -m pytest tests/ -v
```

### Test Coverage

- ✅ Agent initialization and configuration (Sage, Scholar)
- ✅ API endpoints and request/response handling
- ✅ UI utilities and session management  
- ✅ Basic agent functionality and tool integration
- ✅ Error handling and edge cases

See [TESTING.md](TESTING.md) for detailed testing documentation.


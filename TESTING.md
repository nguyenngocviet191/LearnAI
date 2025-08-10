# Unit Tests Documentation

## Overview

This directory contains comprehensive unit tests for the LearnAI project, specifically focusing on the AI agent functionality.

## Test Structure

```
agent/agno_agi/agent-app/tests/
├── __init__.py                    # Test package initialization
├── conftest.py                    # Pytest fixtures and configuration
├── test_agents_operator.py        # Tests for agent operator module
├── test_agents_sage.py           # Tests for Sage agent
├── test_agents_scholar.py        # Tests for Scholar agent
├── test_api_routes_agents.py     # Tests for API routes
└── test_ui_utils.py              # Tests for UI utility functions

agent/agno_agi/tests/
├── __init__.py                    # Test package initialization  
├── conftest.py                    # Pytest fixtures for basic agents
└── test_basic_agent.py           # Tests for basic agent functionality
```

## Running Tests

### Prerequisites

1. Install test dependencies:
```bash
pip install pytest pytest-asyncio pytest-mock
```

2. Install project dependencies:
```bash
pip install -r requirements.txt
```

### Run All Tests

From the project root:
```bash
./run_tests.sh
```

### Run Specific Test Suites

**Agent-app tests:**
```bash
cd agent/agno_agi/agent-app
python -m pytest tests/ -v
```

**Basic agent tests:**
```bash
cd agent/agno_agi
python -m pytest tests/ -v
```

**Specific test files:**
```bash
python -m pytest tests/test_agents_sage.py -v
python -m pytest tests/test_api_routes_agents.py -v
```

## Test Coverage

### Agent Components
- ✅ Agent operator functionality (AgentType enum, get_agent, get_available_agents)
- ✅ Sage agent initialization and configuration
- ✅ Scholar agent initialization and configuration
- ✅ Agent description and instruction validation

### API Routes
- ✅ Agent listing endpoint
- ✅ Agent execution with streaming responses
- ✅ Agent execution with non-streaming responses
- ✅ Error handling for missing agents
- ✅ Request/response models

### UI Utilities
- ✅ Session state management
- ✅ Model selection
- ✅ Message handling
- ✅ Chat history export
- ✅ Agent restart functionality

### Basic Agent
- ✅ Agent initialization with proper configuration
- ✅ API key handling
- ✅ Tool configuration (DuckDuckGo, LocalFileSystem)
- ✅ Memory management

## Test Patterns

### Mocking
Tests use `unittest.mock` extensively to isolate units under test:
- Mock external dependencies (OpenAI, databases, tools)
- Mock async operations with `AsyncMock`
- Use fixtures for common mock objects

### Async Testing
Async functionality is tested using `pytest-asyncio`:
- `@pytest.mark.asyncio` decorator for async test functions
- `AsyncMock` for mocking async methods
- Proper async/await patterns in tests

### Fixtures
Common test objects are provided via pytest fixtures:
- `mock_agent`: Mock Agent instance
- `mock_openai_model`: Mock OpenAI model
- `sample_user_id`, `sample_session_id`: Test data

## Environment Variables

Tests use mock environment variables:
- `OPENAI_API_KEY`: Set to "test-key-for-testing"
- `DATABASE_URL`: Set to mock PostgreSQL URL

## Configuration

Test configuration is managed through:
- `pytest.ini`: Root-level pytest configuration
- `pyproject.toml`: Agent-app specific configuration with dev dependencies
- `conftest.py`: Test fixtures and setup

## Adding New Tests

1. Create test files following the `test_*.py` naming convention
2. Use descriptive test class names: `TestFunctionName`
3. Include docstrings explaining what each test validates
4. Mock external dependencies appropriately
5. Use fixtures for common setup
6. Follow the AAA pattern: Arrange, Act, Assert

## Best Practices

- Keep tests focused and isolated
- Use descriptive test names that explain the scenario
- Mock external dependencies to avoid network calls
- Test both success and failure cases
- Validate both functionality and error handling
- Use parametrized tests for multiple scenarios
- Keep test data realistic but minimal
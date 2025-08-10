"""
Pytest configuration file with common fixtures.
"""
import pytest
from unittest.mock import Mock, MagicMock
from agno.agent import Agent
from agno.models.openai import OpenAIChat


@pytest.fixture
def mock_openai_model():
    """Mock OpenAI model for testing."""
    mock_model = Mock(spec=OpenAIChat)
    mock_model.id = "gpt-4o"
    return mock_model


@pytest.fixture
def mock_agent():
    """Mock Agent instance for testing."""
    agent = Mock(spec=Agent)
    agent.name = "test-agent"
    agent.agent_id = "test-agent-id"
    agent.session_id = "test-session-id"
    agent.user_id = "test-user"
    agent.session_name = "Test Session"
    agent.knowledge = None
    agent.storage = None
    agent.arun = MagicMock()
    agent.run = MagicMock()
    agent.rename_session = MagicMock()
    return agent


@pytest.fixture
def sample_user_id():
    """Sample user ID for testing."""
    return "test-user-123"


@pytest.fixture
def sample_session_id():
    """Sample session ID for testing."""
    return "test-session-456"


@pytest.fixture
def sample_message():
    """Sample message for testing."""
    return "Hello, how can you help me?"
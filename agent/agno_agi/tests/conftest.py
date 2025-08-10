"""
Pytest configuration for agno_agi tests.
"""
import pytest
import os
from unittest.mock import Mock, patch


@pytest.fixture
def mock_openai_api_key():
    """Mock OpenAI API key environment variable."""
    with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'}):
        yield 'test-api-key'


@pytest.fixture
def mock_dotenv_load():
    """Mock dotenv load function."""
    with patch('dotenv.load_dotenv'):
        yield


@pytest.fixture
def sample_agent_config():
    """Sample agent configuration for testing."""
    return {
        'model_id': 'gpt-4o-mini',
        'description': 'Test agent description',
        'tools': [],
        'markdown': True,
        'debug_mode': True
    }
"""
Root pytest configuration for LearnAI project.
"""
import pytest
import sys
import os

# Add agent directories to Python path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent', 'agno_agi'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'agent', 'agno_agi', 'agent-app'))


@pytest.fixture(scope="session")
def test_environment():
    """Setup test environment."""
    # Mock environment variables for testing
    os.environ.setdefault('OPENAI_API_KEY', 'test-key-for-testing')
    return True
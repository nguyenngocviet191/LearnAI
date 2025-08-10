"""
Unit tests for agent operator module.
"""
import pytest
from unittest.mock import Mock, patch
from agents.operator import AgentType, get_available_agents, get_agent


class TestAgentType:
    """Test AgentType enum."""
    
    def test_agent_type_values(self):
        """Test that AgentType enum has expected values."""
        assert AgentType.SAGE.value == "sage"
        assert AgentType.SCHOLAR.value == "scholar"
    
    def test_agent_type_count(self):
        """Test that all expected agent types are present."""
        agent_types = list(AgentType)
        assert len(agent_types) == 2
        assert AgentType.SAGE in agent_types
        assert AgentType.SCHOLAR in agent_types


class TestGetAvailableAgents:
    """Test get_available_agents function."""
    
    def test_returns_list_of_agent_ids(self):
        """Test that get_available_agents returns correct agent IDs."""
        agents = get_available_agents()
        assert isinstance(agents, list)
        assert "sage" in agents
        assert "scholar" in agents
        assert len(agents) == 2


class TestGetAgent:
    """Test get_agent function."""
    
    @patch('agents.operator.get_sage')
    def test_get_sage_agent(self, mock_get_sage):
        """Test getting sage agent."""
        mock_agent = Mock()
        mock_get_sage.return_value = mock_agent
        
        result = get_agent(
            model_id="gpt-4o",
            agent_id=AgentType.SAGE,
            user_id="test-user",
            session_id="test-session",
            debug_mode=True
        )
        
        assert result == mock_agent
        mock_get_sage.assert_called_once_with(
            model_id="gpt-4o",
            user_id="test-user",
            session_id="test-session",
            debug_mode=True
        )
    
    @patch('agents.operator.get_scholar')
    def test_get_scholar_agent(self, mock_get_scholar):
        """Test getting scholar agent."""
        mock_agent = Mock()
        mock_get_scholar.return_value = mock_agent
        
        result = get_agent(
            model_id="gpt-4o",
            agent_id=AgentType.SCHOLAR,
            user_id="test-user",
            session_id="test-session",
            debug_mode=True
        )
        
        assert result == mock_agent
        mock_get_scholar.assert_called_once_with(
            model_id="gpt-4o",
            user_id="test-user",
            session_id="test-session",
            debug_mode=True
        )
    
    @patch('agents.operator.get_scholar')
    def test_get_agent_defaults_to_scholar(self, mock_get_scholar):
        """Test that get_agent defaults to scholar when no agent_id provided."""
        mock_agent = Mock()
        mock_get_scholar.return_value = mock_agent
        
        result = get_agent(model_id="gpt-4o")
        
        assert result == mock_agent
        mock_get_scholar.assert_called_once_with(
            model_id="gpt-4o",
            user_id=None,
            session_id=None,
            debug_mode=True
        )
    
    @patch('agents.operator.get_scholar')
    def test_get_agent_with_default_parameters(self, mock_get_scholar):
        """Test get_agent with default parameters."""
        mock_agent = Mock()
        mock_get_scholar.return_value = mock_agent
        
        result = get_agent()
        
        assert result == mock_agent
        mock_get_scholar.assert_called_once_with(
            model_id="gpt-4o",
            user_id=None,
            session_id=None,
            debug_mode=True
        )
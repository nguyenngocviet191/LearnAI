"""
Unit tests for scholar agent module.
"""
import pytest
from unittest.mock import Mock, patch
from agents.scholar import get_scholar


class TestGetScholar:
    """Test get_scholar function."""
    
    @patch('agents.scholar.PostgresAgentStorage')
    @patch('agents.scholar.OpenAIChat')
    @patch('agents.scholar.Agent')
    @patch('agents.scholar.DuckDuckGoTools')
    def test_get_scholar_with_defaults(self, mock_duckduckgo, mock_agent, mock_openai, mock_storage):
        """Test getting scholar agent with default parameters."""
        mock_agent_instance = Mock()
        mock_agent.return_value = mock_agent_instance
        
        result = get_scholar()
        
        # Verify Agent was called with correct parameters
        mock_agent.assert_called_once()
        args, kwargs = mock_agent.call_args
        
        assert kwargs['name'] == 'Scholar'
        assert kwargs['agent_id'] == 'scholar'
        assert kwargs['user_id'] is None
        assert kwargs['session_id'] is None
        assert kwargs['markdown'] is True
        assert kwargs['debug_mode'] is True
        assert kwargs['add_datetime_to_instructions'] is True
        assert kwargs['add_history_to_messages'] is True
        assert kwargs['num_history_responses'] == 3
        assert kwargs['read_chat_history'] is True
        
        # Verify OpenAIChat was initialized with correct model
        mock_openai.assert_called_once_with(id="gpt-4o")
        
        # Verify DuckDuckGoTools was instantiated
        mock_duckduckgo.assert_called_once()
        
        assert result == mock_agent_instance
    
    @patch('agents.scholar.PostgresAgentStorage')
    @patch('agents.scholar.OpenAIChat')
    @patch('agents.scholar.Agent')
    @patch('agents.scholar.DuckDuckGoTools')
    def test_get_scholar_with_user_id(self, mock_duckduckgo, mock_agent, mock_openai, mock_storage):
        """Test getting scholar agent with user ID."""
        mock_agent_instance = Mock()
        mock_agent.return_value = mock_agent_instance
        
        result = get_scholar(
            model_id="gpt-4o-mini",
            user_id="test-user-123",
            session_id="test-session-456",
            debug_mode=False
        )
        
        # Verify Agent was called with correct parameters
        mock_agent.assert_called_once()
        args, kwargs = mock_agent.call_args
        
        assert kwargs['user_id'] == "test-user-123"
        assert kwargs['session_id'] == "test-session-456"
        assert kwargs['debug_mode'] is False
        
        # Verify additional_context includes user information
        assert "<context>" in kwargs['additional_context']
        assert "test-user-123" in kwargs['additional_context']
        assert "</context>" in kwargs['additional_context']
        
        # Verify OpenAIChat was initialized with correct model
        mock_openai.assert_called_once_with(id="gpt-4o-mini")
        
        assert result == mock_agent_instance
    
    @patch('agents.scholar.PostgresAgentStorage')
    @patch('agents.scholar.OpenAIChat')
    @patch('agents.scholar.Agent')
    @patch('agents.scholar.DuckDuckGoTools')
    def test_get_scholar_without_user_id(self, mock_duckduckgo, mock_agent, mock_openai, mock_storage):
        """Test getting scholar agent without user ID."""
        mock_agent_instance = Mock()
        mock_agent.return_value = mock_agent_instance
        
        result = get_scholar()
        
        # Verify Agent was called with correct parameters
        mock_agent.assert_called_once()
        args, kwargs = mock_agent.call_args
        
        # Verify additional_context is empty when no user_id
        assert kwargs['additional_context'] == ""
        
        assert result == mock_agent_instance
    
    def test_scholar_description_contains_key_elements(self):
        """Test that scholar description contains expected elements."""
        with patch('agents.scholar.PostgresAgentStorage'), \
             patch('agents.scholar.OpenAIChat'), \
             patch('agents.scholar.Agent') as mock_agent, \
             patch('agents.scholar.DuckDuckGoTools'):
            
            get_scholar()
            
            args, kwargs = mock_agent.call_args
            description = kwargs['description']
            
            assert "Scholar" in description
            assert "Answer Engine" in description
            assert "DuckDuckGoTools" in description
    
    def test_scholar_instructions_contain_search_requirements(self):
        """Test that scholar instructions contain search requirements."""
        with patch('agents.scholar.PostgresAgentStorage'), \
             patch('agents.scholar.OpenAIChat'), \
             patch('agents.scholar.Agent') as mock_agent, \
             patch('agents.scholar.DuckDuckGoTools'):
            
            get_scholar()
            
            args, kwargs = mock_agent.call_args
            instructions = kwargs['instructions']
            
            assert "duckduckgo_search" in instructions
            assert "Gather Relevant Information" in instructions
            assert "supporting evidence" in instructions.lower()
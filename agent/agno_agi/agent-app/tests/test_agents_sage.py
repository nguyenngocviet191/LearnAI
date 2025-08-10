"""
Unit tests for sage agent module.
"""
import pytest
from unittest.mock import Mock, patch
from agents.sage import get_sage


class TestGetSage:
    """Test get_sage function."""
    
    @patch('agents.sage.PostgresAgentStorage')
    @patch('agents.sage.PgVector')
    @patch('agents.sage.AgentKnowledge')
    @patch('agents.sage.OpenAIChat')
    @patch('agents.sage.Agent')
    @patch('agents.sage.DuckDuckGoTools')
    def test_get_sage_with_defaults(self, mock_duckduckgo, mock_agent, mock_openai, 
                                   mock_knowledge, mock_pgvector, mock_storage):
        """Test getting sage agent with default parameters."""
        mock_agent_instance = Mock()
        mock_agent.return_value = mock_agent_instance
        
        result = get_sage()
        
        # Verify Agent was called with correct parameters
        mock_agent.assert_called_once()
        args, kwargs = mock_agent.call_args
        
        assert kwargs['name'] == 'Sage'
        assert kwargs['agent_id'] == 'sage'
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
        
        # Verify knowledge base components were set up
        mock_pgvector.assert_called_once()
        mock_knowledge.assert_called_once()
        
        assert result == mock_agent_instance
    
    @patch('agents.sage.PostgresAgentStorage')
    @patch('agents.sage.PgVector')
    @patch('agents.sage.AgentKnowledge')
    @patch('agents.sage.OpenAIChat')
    @patch('agents.sage.Agent')
    @patch('agents.sage.DuckDuckGoTools')
    def test_get_sage_with_user_id(self, mock_duckduckgo, mock_agent, mock_openai,
                                  mock_knowledge, mock_pgvector, mock_storage):
        """Test getting sage agent with user ID."""
        mock_agent_instance = Mock()
        mock_agent.return_value = mock_agent_instance
        
        result = get_sage(
            model_id="gpt-4o-mini",
            user_id="test-user-789",
            session_id="test-session-101",
            debug_mode=False
        )
        
        # Verify Agent was called with correct parameters
        mock_agent.assert_called_once()
        args, kwargs = mock_agent.call_args
        
        assert kwargs['user_id'] == "test-user-789"
        assert kwargs['session_id'] == "test-session-101"
        assert kwargs['debug_mode'] is False
        
        # Verify additional_context includes user information
        assert "<context>" in kwargs['additional_context']
        assert "test-user-789" in kwargs['additional_context']
        assert "</context>" in kwargs['additional_context']
        
        # Verify OpenAIChat was initialized with correct model
        mock_openai.assert_called_once_with(id="gpt-4o-mini")
        
        assert result == mock_agent_instance
    
    @patch('agents.sage.PostgresAgentStorage')
    @patch('agents.sage.PgVector')
    @patch('agents.sage.AgentKnowledge')
    @patch('agents.sage.OpenAIChat')
    @patch('agents.sage.Agent')
    @patch('agents.sage.DuckDuckGoTools')
    def test_get_sage_without_user_id(self, mock_duckduckgo, mock_agent, mock_openai,
                                     mock_knowledge, mock_pgvector, mock_storage):
        """Test getting sage agent without user ID."""
        mock_agent_instance = Mock()
        mock_agent.return_value = mock_agent_instance
        
        result = get_sage()
        
        # Verify Agent was called with correct parameters
        mock_agent.assert_called_once()
        args, kwargs = mock_agent.call_args
        
        # Verify additional_context is empty when no user_id
        assert kwargs['additional_context'] == ""
        
        assert result == mock_agent_instance
    
    def test_sage_description_contains_key_elements(self):
        """Test that sage description contains expected elements."""
        with patch('agents.sage.PostgresAgentStorage'), \
             patch('agents.sage.PgVector'), \
             patch('agents.sage.AgentKnowledge'), \
             patch('agents.sage.OpenAIChat'), \
             patch('agents.sage.Agent') as mock_agent, \
             patch('agents.sage.DuckDuckGoTools'):
            
            get_sage()
            
            args, kwargs = mock_agent.call_args
            description = kwargs['description']
            
            assert "Sage" in description
            assert "Knowledge Agent" in description
            assert "knowledge base" in description
    
    def test_sage_instructions_contain_knowledge_search(self):
        """Test that sage instructions contain knowledge search requirements."""
        with patch('agents.sage.PostgresAgentStorage'), \
             patch('agents.sage.PgVector'), \
             patch('agents.sage.AgentKnowledge'), \
             patch('agents.sage.OpenAIChat'), \
             patch('agents.sage.Agent') as mock_agent, \
             patch('agents.sage.DuckDuckGoTools'):
            
            get_sage()
            
            args, kwargs = mock_agent.call_args
            instructions = kwargs['instructions']
            
            assert "search_knowledge_base" in instructions
            assert "knowledge base" in instructions
            assert "duckduckgo_search" in instructions
            assert "citations" in instructions
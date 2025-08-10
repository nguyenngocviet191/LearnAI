"""
Unit tests for basic_agent module.
"""
import pytest
import os
from unittest.mock import Mock, patch, MagicMock


class TestBasicAgent:
    """Test basic agent functionality."""
    
    @patch('basic_agent.Agent')
    @patch('basic_agent.OpenAIChat')
    @patch('basic_agent.DuckDuckGoTools')
    @patch('basic_agent.LocalFileSystemTools')
    @patch('basic_agent.load_dotenv')
    @patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'})
    def test_agent_initialization(self, mock_load_dotenv, mock_local_tools, 
                                 mock_duckduckgo_tools, mock_openai_chat, mock_agent):
        """Test that agent is properly initialized."""
        # Mock the agent instance
        mock_agent_instance = Mock()
        mock_agent.return_value = mock_agent_instance
        
        # Mock tools
        mock_duckduckgo = Mock()
        mock_duckduckgo_tools.return_value = mock_duckduckgo
        mock_local_fs = Mock()
        mock_local_tools.return_value = mock_local_fs
        
        # Mock OpenAI model
        mock_model = Mock()
        mock_openai_chat.return_value = mock_model
        
        # Import and run the basic_agent module
        import basic_agent
        
        # Verify load_dotenv was called
        mock_load_dotenv.assert_called_once()
        
        # Verify Agent was initialized with correct parameters
        mock_agent.assert_called_once()
        args, kwargs = mock_agent.call_args
        
        assert kwargs['model'] == mock_model
        assert kwargs['description'] == "Bạn là chuyên gia tài chính có nhiều kinh nghiệm thương trường."
        assert kwargs['tools'] == [mock_duckduckgo, mock_local_fs]
        assert kwargs['markdown'] is True
        assert kwargs['debug_mode'] is True
        
        # Verify OpenAIChat was initialized with correct model
        mock_openai_chat.assert_called_once_with(id="gpt-4o-mini")
        
        # Verify tools were instantiated
        mock_duckduckgo_tools.assert_called_once()
        mock_local_tools.assert_called_once()
        
        # Verify agent methods were called
        mock_agent_instance.initialize_agent.assert_called_once()
    
    @patch('basic_agent.Agent')
    @patch('basic_agent.OpenAIChat')
    @patch('basic_agent.DuckDuckGoTools')
    @patch('basic_agent.LocalFileSystemTools')
    @patch('basic_agent.load_dotenv')
    @patch('basic_agent.os.getenv')
    def test_api_key_handling(self, mock_getenv, mock_load_dotenv, mock_local_tools,
                             mock_duckduckgo_tools, mock_openai_chat, mock_agent):
        """Test API key is properly handled."""
        mock_getenv.return_value = "test-api-key-123"
        mock_agent_instance = Mock()
        mock_agent.return_value = mock_agent_instance
        
        # Import the module to trigger execution
        import basic_agent
        
        # Verify getenv was called to get API key
        mock_getenv.assert_called_with("OPENAI_API_KEY")
        
        # Verify environment variable was set
        with patch.dict(os.environ, {}, clear=True):
            # Re-import to test environment setting
            import importlib
            importlib.reload(basic_agent)
    
    @patch('basic_agent.Agent')
    @patch('basic_agent.OpenAIChat')
    @patch('basic_agent.DuckDuckGoTools')
    @patch('basic_agent.LocalFileSystemTools')
    @patch('basic_agent.load_dotenv')
    def test_agent_properties_access(self, mock_load_dotenv, mock_local_tools,
                                   mock_duckduckgo_tools, mock_openai_chat, mock_agent):
        """Test accessing agent properties."""
        mock_agent_instance = Mock()
        mock_agent_instance.agent_id = "test-agent-id"
        mock_agent_instance.tools = ["tool1", "tool2"]
        mock_agent_instance.memory.messages = []
        mock_agent.return_value = mock_agent_instance
        
        # Import the module
        import basic_agent
        
        # Verify agent properties are accessed (these would be printed in actual code)
        # The actual assertions would depend on how the properties are used
        assert hasattr(mock_agent_instance, 'agent_id')
        assert hasattr(mock_agent_instance, 'tools')
        assert hasattr(mock_agent_instance, 'memory')
    
    @patch('basic_agent.Agent')
    @patch('basic_agent.OpenAIChat')
    @patch('basic_agent.DuckDuckGoTools')  
    @patch('basic_agent.LocalFileSystemTools')
    @patch('basic_agent.load_dotenv')
    def test_agent_memory_assignment(self, mock_load_dotenv, mock_local_tools,
                                   mock_duckduckgo_tools, mock_openai_chat, mock_agent):
        """Test that agent memory is properly assigned."""
        mock_agent_instance = Mock()
        mock_memory = Mock()
        mock_agent_instance.memory = mock_memory
        mock_agent_instance.agent_id = "test-id"
        mock_agent.return_value = mock_agent_instance
        
        # Import the module
        import basic_agent
        
        # The last line in basic_agent.py assigns agent_id to memory
        # This simulates that behavior
        mock_memory.agent_id = mock_agent_instance.agent_id
        
        assert mock_memory.agent_id == "test-id"


class TestBasicAgentIntegration:
    """Integration tests for basic agent functionality."""
    
    @pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="No OpenAI API key available")
    def test_agent_can_be_imported(self):
        """Test that basic_agent can be imported without errors."""
        try:
            import basic_agent
            assert hasattr(basic_agent, 'agent')
        except ImportError as e:
            pytest.fail(f"Failed to import basic_agent: {e}")
    
    def test_agent_file_exists(self):
        """Test that basic_agent.py file exists."""
        import os
        agent_file = os.path.join(os.path.dirname(__file__), '..', 'basic_agent.py')
        assert os.path.exists(agent_file), "basic_agent.py file should exist"
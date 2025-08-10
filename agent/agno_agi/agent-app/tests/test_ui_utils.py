"""
Unit tests for UI utilities module.
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
import streamlit as st
from ui.utils import (
    initialize_agent_session_state,
    selected_model,
    add_message,
    export_chat_history,
    restart_agent
)


class TestInitializeAgentSessionState:
    """Test initialize_agent_session_state function."""
    
    @patch('ui.utils.st')
    @pytest.mark.asyncio
    async def test_initialize_agent_session_state_new_agent(self, mock_st):
        """Test initializing session state for new agent."""
        mock_st.session_state = {}
        
        await initialize_agent_session_state("test_agent")
        
        assert "test_agent" in mock_st.session_state
        assert mock_st.session_state["test_agent"]["agent"] is None
        assert mock_st.session_state["test_agent"]["session_id"] is None
        assert mock_st.session_state["test_agent"]["messages"] == []
    
    @patch('ui.utils.st')
    @pytest.mark.asyncio
    async def test_initialize_agent_session_state_existing_agent(self, mock_st):
        """Test initializing session state for existing agent."""
        mock_st.session_state = {
            "test_agent": {
                "agent": "existing_agent",
                "session_id": "existing_session",
                "messages": ["existing_message"]
            }
        }
        
        await initialize_agent_session_state("test_agent")
        
        # Should not modify existing state
        assert mock_st.session_state["test_agent"]["agent"] == "existing_agent"
        assert mock_st.session_state["test_agent"]["session_id"] == "existing_session"
        assert mock_st.session_state["test_agent"]["messages"] == ["existing_message"]


class TestSelectedModel:
    """Test selected_model function."""
    
    @patch('ui.utils.st')
    @pytest.mark.asyncio
    async def test_selected_model_default(self, mock_st):
        """Test selected_model returns default model."""
        mock_st.sidebar.selectbox.return_value = "gpt-4o"
        
        result = await selected_model()
        
        assert result == "gpt-4o"
        mock_st.sidebar.selectbox.assert_called_once()
    
    @patch('ui.utils.st')
    @pytest.mark.asyncio
    async def test_selected_model_o3_mini(self, mock_st):
        """Test selected_model returns o3-mini."""
        mock_st.sidebar.selectbox.return_value = "o3-mini"
        
        result = await selected_model()
        
        assert result == "o3-mini"


class TestAddMessage:
    """Test add_message function."""
    
    @patch('ui.utils.st')
    @pytest.mark.asyncio
    async def test_add_message_user(self, mock_st):
        """Test adding user message."""
        mock_st.session_state = {
            "test_agent": {
                "messages": []
            }
        }
        
        await add_message("test_agent", "user", "Hello world")
        
        expected_message = {
            "role": "user",
            "content": "Hello world",
            "tool_calls": None
        }
        assert mock_st.session_state["test_agent"]["messages"][0] == expected_message
    
    @patch('ui.utils.st')
    @pytest.mark.asyncio
    async def test_add_message_assistant_with_tools(self, mock_st):
        """Test adding assistant message with tool calls."""
        mock_st.session_state = {
            "test_agent": {
                "messages": []
            }
        }
        
        tool_calls = [{"name": "search", "args": {"query": "test"}}]
        await add_message("test_agent", "assistant", "Here's the answer", tool_calls)
        
        expected_message = {
            "role": "assistant",
            "content": "Here's the answer",
            "tool_calls": tool_calls
        }
        assert mock_st.session_state["test_agent"]["messages"][0] == expected_message


class TestExportChatHistory:
    """Test export_chat_history function."""
    
    @patch('ui.utils.st')
    def test_export_chat_history_no_messages(self, mock_st):
        """Test exporting chat history with no messages."""
        mock_st.session_state = {
            "test_agent": {
                "messages": []
            }
        }
        
        result = export_chat_history("test_agent")
        
        assert "test_agent - Chat History" in result
        assert "No messages to export" in result
    
    @patch('ui.utils.st')
    def test_export_chat_history_with_messages(self, mock_st):
        """Test exporting chat history with messages."""
        mock_st.session_state = {
            "test_agent": {
                "messages": [
                    {"role": "user", "content": "Hello"},
                    {"role": "assistant", "content": "Hi there!", "tool_calls": None}
                ]
            }
        }
        
        result = export_chat_history("test_agent")
        
        assert "test_agent - Chat History" in result
        assert "👤 User" in result
        assert "🤖 Assistant" in result
        assert "Hello" in result
        assert "Hi there!" in result
    
    @patch('ui.utils.st')
    def test_export_chat_history_with_tool_calls(self, mock_st):
        """Test exporting chat history with tool calls."""
        tool_calls = [
            {
                "name": "search_tool",
                "arguments": '{"query": "test"}',
                "content": "Search results"
            }
        ]
        
        mock_st.session_state = {
            "test_agent": {
                "messages": [
                    {"role": "assistant", "content": "I'll search for that", "tool_calls": tool_calls}
                ]
            }
        }
        
        result = export_chat_history("test_agent")
        
        assert "Tool Calls:" in result
        assert "search_tool" in result
        assert "Search results" in result
    
    @patch('ui.utils.st')
    def test_export_chat_history_missing_messages_key(self, mock_st):
        """Test exporting chat history when messages key is missing."""
        mock_st.session_state = {
            "test_agent": {}
        }
        
        result = export_chat_history("test_agent")
        
        assert "No messages to export" in result


class TestRestartAgent:
    """Test restart_agent function."""
    
    @patch('ui.utils.st')
    def test_restart_agent(self, mock_st):
        """Test restarting agent clears session state."""
        mock_st.session_state = {
            "test_agent": {
                "agent": "existing_agent",
                "session_id": "existing_session",
                "messages": ["message1", "message2"],
                "url_scrape_key": 5,
                "file_uploader_key": 10
            }
        }
        
        restart_agent("test_agent")
        
        # Verify state was reset
        assert mock_st.session_state["test_agent"]["agent"] is None
        assert mock_st.session_state["test_agent"]["session_id"] is None
        assert mock_st.session_state["test_agent"]["messages"] == []
        
        # Verify keys were incremented
        assert mock_st.session_state["test_agent"]["url_scrape_key"] == 6
        assert mock_st.session_state["test_agent"]["file_uploader_key"] == 11
        
        # Verify rerun was called
        mock_st.rerun.assert_called_once()
    
    @patch('ui.utils.st')
    def test_restart_agent_without_keys(self, mock_st):
        """Test restarting agent without optional keys."""
        mock_st.session_state = {
            "test_agent": {
                "agent": "existing_agent",
                "session_id": "existing_session",
                "messages": ["message1"]
            }
        }
        
        restart_agent("test_agent")
        
        # Verify basic state was reset
        assert mock_st.session_state["test_agent"]["agent"] is None
        assert mock_st.session_state["test_agent"]["session_id"] is None
        assert mock_st.session_state["test_agent"]["messages"] == []
        
        # Verify rerun was called
        mock_st.rerun.assert_called_once()
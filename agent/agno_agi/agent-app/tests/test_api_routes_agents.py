"""
Unit tests for API routes - agents module.
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi import HTTPException
from fastapi.testclient import TestClient
from api.routes.agents import (
    agents_router, 
    list_agents, 
    run_agent, 
    chat_response_streamer,
    RunRequest,
    Model,
    AgentType
)


class TestListAgents:
    """Test list_agents endpoint."""
    
    @patch('api.routes.agents.get_available_agents')
    @pytest.mark.asyncio
    async def test_list_agents_success(self, mock_get_available):
        """Test successful listing of agents."""
        mock_get_available.return_value = ["sage", "scholar"]
        
        result = await list_agents()
        
        assert result == ["sage", "scholar"]
        mock_get_available.assert_called_once()


class TestChatResponseStreamer:
    """Test chat_response_streamer function."""
    
    @pytest.mark.asyncio
    async def test_chat_response_streamer(self, mock_agent):
        """Test streaming chat responses."""
        # Mock response chunks
        mock_chunk1 = Mock()
        mock_chunk1.content = "Hello"
        mock_chunk2 = Mock()
        mock_chunk2.content = " there!"
        
        # Create async generator for mocking
        async def mock_stream():
            yield mock_chunk1
            yield mock_chunk2
        
        # Use AsyncMock for arun
        mock_agent.arun = AsyncMock(return_value=mock_stream())
        
        # Collect streamed chunks
        chunks = []
        async for chunk in chat_response_streamer(mock_agent, "test message"):
            chunks.append(chunk)
        
        assert chunks == ["Hello", " there!"]
        mock_agent.arun.assert_called_once_with("test message", stream=True)


class TestRunRequest:
    """Test RunRequest model."""
    
    def test_run_request_defaults(self):
        """Test RunRequest with default values."""
        request = RunRequest(message="Hello")
        
        assert request.message == "Hello"
        assert request.stream is True
        assert request.model == Model.gpt_4o
        assert request.user_id is None
        assert request.session_id is None
    
    def test_run_request_with_all_fields(self):
        """Test RunRequest with all fields set."""
        request = RunRequest(
            message="Hello world",
            stream=False,
            model=Model.o3_mini,
            user_id="user123",
            session_id="session456"
        )
        
        assert request.message == "Hello world"
        assert request.stream is False
        assert request.model == Model.o3_mini
        assert request.user_id == "user123"
        assert request.session_id == "session456"


class TestRunAgent:
    """Test run_agent endpoint."""
    
    @patch('api.routes.agents.get_agent')
    @patch('api.routes.agents.chat_response_streamer')
    @pytest.mark.asyncio
    async def test_run_agent_streaming(self, mock_streamer, mock_get_agent, mock_agent):
        """Test running agent with streaming response."""
        mock_get_agent.return_value = mock_agent
        
        # Mock the streamer to return async generator
        async def mock_stream():
            yield "response chunk"
        
        mock_streamer.return_value = mock_stream()
        
        request = RunRequest(
            message="test message",
            stream=True,
            model=Model.gpt_4o,
            user_id="user123",
            session_id="session456"
        )
        
        response = await run_agent(AgentType.SAGE, request)
        
        # Verify get_agent was called with correct parameters
        mock_get_agent.assert_called_once_with(
            model_id="gpt-4o",
            agent_id=AgentType.SAGE,
            user_id="user123",
            session_id="session456"
        )
        
        # Verify streamer was called
        mock_streamer.assert_called_once_with(mock_agent, "test message")
        
        # Check response type
        from fastapi.responses import StreamingResponse
        assert isinstance(response, StreamingResponse)
    
    @patch('api.routes.agents.get_agent')
    @pytest.mark.asyncio
    async def test_run_agent_non_streaming(self, mock_get_agent, mock_agent):
        """Test running agent without streaming response."""
        mock_get_agent.return_value = mock_agent
        
        # Mock agent response
        mock_response = Mock()
        mock_response.content = "Agent response"
        mock_agent.arun = AsyncMock(return_value=mock_response)
        
        request = RunRequest(
            message="test message",
            stream=False,
            model=Model.o3_mini
        )
        
        response = await run_agent(AgentType.SCHOLAR, request)
        
        # Verify get_agent was called with correct parameters
        mock_get_agent.assert_called_once_with(
            model_id="o3-mini",
            agent_id=AgentType.SCHOLAR,
            user_id=None,
            session_id=None
        )
        
        # Verify agent.arun was called
        mock_agent.arun.assert_called_once_with("test message", stream=False)
        
        # Check response content
        assert response == "Agent response"
    
    @patch('api.routes.agents.get_agent')
    @pytest.mark.asyncio
    async def test_run_agent_agent_not_found(self, mock_get_agent):
        """Test running agent when agent is not found."""
        mock_get_agent.side_effect = Exception("Agent not found")
        
        request = RunRequest(message="test message")
        
        with pytest.raises(HTTPException) as exc_info:
            await run_agent(AgentType.SAGE, request)
        
        assert exc_info.value.status_code == 404
        assert "Agent not found" in str(exc_info.value.detail)


class TestModel:
    """Test Model enum."""
    
    def test_model_values(self):
        """Test Model enum values."""
        assert Model.gpt_4o.value == "gpt-4o"
        assert Model.o3_mini.value == "o3-mini"
    
    def test_model_count(self):
        """Test expected number of models."""
        models = list(Model)
        assert len(models) == 2
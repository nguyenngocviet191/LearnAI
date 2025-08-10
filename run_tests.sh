#!/bin/bash

# Test runner script for LearnAI project
# This script runs all unit tests in the project

echo "🧪 Running LearnAI Unit Tests"
echo "=============================="

# Set environment variables for testing
export OPENAI_API_KEY="test-key-for-testing"
export DATABASE_URL="postgresql://test:test@localhost:5432/test_db"

echo "📋 Running agent-app tests..."
cd agent/agno_agi/agent-app
python -m pytest tests/ -v --tb=short

echo ""
echo "📋 Running basic agent tests..."
cd ../
python -m pytest tests/test_basic_agent.py::TestBasicAgentIntegration::test_agent_file_exists -v

echo ""
echo "✅ All tests completed!"

# Return to root directory
cd ../../
"""
Test suite for Banking Customer Support AI Agent
"""

import pytest
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.ticket_manager import (
    generate_unique_ticket_id,
    create_ticket,
    get_ticket_status,
    log_satisfaction,
    view_tickets,
    get_ticket_count,
)
from src.classifier import hf_model_classify
from src.agents import app


class TestTicketManager:
    """Test ticket management functionality."""

    def test_generate_ticket_id(self):
        """Test ticket ID generation."""
        ticket_id = generate_unique_ticket_id()
        assert isinstance(ticket_id, int)
        assert 100000 <= ticket_id <= 999999

    def test_create_ticket(self):
        """Test ticket creation."""
        ticket_id = generate_unique_ticket_id()
        result = create_ticket(
            ticket_id=ticket_id,
            status="Unresolved",
            message="Test complaint",
            customer_name="Test Customer",
        )
        assert result is True

    def test_get_ticket_status(self):
        """Test retrieving ticket status."""
        ticket_id = generate_unique_ticket_id()
        create_ticket(
            ticket_id=ticket_id,
            status="Unresolved",
            message="Test issue",
            customer_name="Test User",
        )
        status = get_ticket_status(ticket_id)
        assert status == "Unresolved"

    def test_get_nonexistent_ticket(self):
        """Test retrieving a ticket that doesn't exist."""
        status = get_ticket_status(999999)
        assert status is None

    def test_log_satisfaction(self):
        """Test logging satisfaction rating."""
        ticket_id = generate_unique_ticket_id()
        create_ticket(
            ticket_id=ticket_id,
            status="Resolved",
            message="Test issue",
            customer_name="Test User",
        )
        result = log_satisfaction(ticket_id, 5)
        assert "Satisfaction rating 5/5 logged" in result

    def test_log_satisfaction_invalid_ticket(self):
        """Test logging satisfaction for invalid ticket."""
        result = log_satisfaction(999999, 5)
        assert "not found" in result

    def test_view_tickets(self):
        """Test viewing all tickets."""
        html = view_tickets()
        assert isinstance(html, str)

    def test_get_ticket_count(self):
        """Test getting ticket count."""
        count = get_ticket_count()
        assert isinstance(count, int)
        assert count >= 0


class TestClassifier:
    """Test intent classification functionality."""

    def test_positive_feedback(self):
        """Test classification of positive feedback."""
        text = "Thanks, that was helpful"
        result = hf_model_classify(text)
        assert result in ["Query", "Positive Feedback", "Negative Feedback"]

    def test_negative_feedback(self):
        """Test classification of negative feedback."""
        text = "My card was declined and I need help"
        result = hf_model_classify(text)
        assert result in ["Query", "Positive Feedback", "Negative Feedback"]

    def test_query(self):
        """Test classification of general query."""
        text = "What is the status of my account"
        result = hf_model_classify(text)
        assert result in ["Query", "Positive Feedback", "Negative Feedback"]

    def test_empty_input(self):
        """Test classification of empty input."""
        result = hf_model_classify("")
        assert result == "Query"

    def test_none_input(self):
        """Test classification of None input."""
        result = hf_model_classify(None)
        assert result == "Query"
        # assert result == "Positive Feedback"


class TestAgent:
    """Test LangGraph agent workflow."""

    def test_agent_positive_feedback(self):
        """Test agent with positive feedback."""
        state = {"input": "Thanks, that was helpful", "customer_name": "John"}
        result = app.invoke(state)
        answer = result.get("answer", {})
        assert "classification" in answer
        assert "response" in answer

    def test_agent_negative_feedback(self):
        """Test agent with negative feedback."""
        state = {"input": "My card was declined", "customer_name": "Jane"}
        result = app.invoke(state)
        answer = result.get("answer", {})
        assert "classification" in answer
        assert "response" in answer
        # Should create a ticket
        assert answer.get("ticket_id") is not None

    def test_agent_query(self):
        """Test agent with general query."""
        state = {"input": "How do I activate my card", "customer_name": "Bob"}
        result = app.invoke(state)
        answer = result.get("answer", {})
        assert "classification" in answer
        assert "response" in answer

    def test_agent_ticket_query(self):
        """Test agent with ticket status query."""
        ticket_id = generate_unique_ticket_id()
        create_ticket(
            ticket_id=ticket_id,
            status="Unresolved",
            message="Test issue",
            customer_name="Test User",
        )
        state = {"input": f"What is status of {ticket_id}", "customer_name": "Alice"}
        result = app.invoke(state)
        answer = result.get("answer", {})
        assert "classification" in answer
        assert str(ticket_id) in answer.get("response", "")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

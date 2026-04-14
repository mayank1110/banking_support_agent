"""
Message Handler Module
Handles feedback and query processing for customer support.
"""

import re
import random
import pandas as pd
from typing import Tuple, Optional

from config import TICKET_CSV, TICKET_ID_MIN, TICKET_ID_MAX
from .classifier import hf_model_classify
from .ticket_manager import generate_unique_ticket_id


def handle_feedback(
    user_message: str, customer_name: str = "Customer"
) -> Tuple[str, str, Optional[int]]:
    """
    Handle customer feedback (positive or negative).
    
    Args:
        user_message: Customer's feedback message
        customer_name: Customer's name for personalization
        
    Returns:
        Tuple of (classification, response_message, ticket_id)
    """
    classification = hf_model_classify(user_message)

    if classification == "Positive Feedback":
        response = f"Thank you for your kind words, {customer_name}! We're delighted to assist you."
        return classification, response, None

    elif classification == "Negative Feedback":
        ticket_id = generate_unique_ticket_id()
        
        # Create ticket record
        from .ticket_manager import create_ticket
        create_ticket(
            ticket_id=ticket_id,
            status="Unresolved",
            message=user_message,
            customer_name=customer_name,
            satisfaction=None,
        )

        response = (
            f"We apologize for the inconvenience. Someone from our support team will help you. "
            f"For your reference, a new ticket #{ticket_id} has been generated, and our team will follow up shortly."
        )
        return classification, response, ticket_id

    else:
        return (
            classification,
            "Feedback handler received an unsupported type. Unable to understand your concern.",
            None,
        )


def handle_query(user_message: str) -> Tuple[str, str, Optional[int]]:
    """
    Handle customer queries about ticket status or general banking questions.
    
    Args:
        user_message: Customer's query message
        
    Returns:
        Tuple of (classification, response_message, ticket_id)
    """
    # Check for 6-digit ticket ID
    match = re.search(r"\b\d{6}\b", user_message)
    
    if match:
        ticket_id = int(match.group())
        
        from .ticket_manager import get_ticket_status
        status = get_ticket_status(ticket_id)
        
        if status is not None:
            response = f"Your ticket #{ticket_id} is currently marked as: {status}."
            return "Query", response, ticket_id
        else:
            response = (
                f"Ticket #{ticket_id} was not found in our records. "
                "Please check the number or contact support."
            )
            return "Query", response, None

    # Generic banking guidance
    banking_keywords = [
        "status", "balance", "transfer", "payment", "card",
        "block", "fraud", "loan", "interest", "account"
    ]
    
    if any(keyword in user_message.lower() for keyword in banking_keywords):
        response = (
            "I can help with account-related queries. If you have a ticket number, "
            "include the 6-digit ID to check status. Otherwise, please provide more details."
        )
        return "Query", response, None

    # Default response for unrecognized queries
    response = (
        "No valid ticket number found in your query. If you want to open a ticket, "
        "describe the issue and we'll create one."
    )
    return "Query", response, None


if __name__ == "__main__":
    # Test handlers
    test_messages = [
        ("Thanks, that was helpful", "John"),
        ("My card was declined and I need help", "Jane"),
        ("What is the status of 123456", "Customer"),
    ]

    for message, name in test_messages:
        classification, response, ticket_id = handle_feedback(message, name) if "Thanks" in message or "declined" in message else handle_query(message)
        print(f"Message: {message}")
        print(f"Classification: {classification}")
        print(f"Response: {response}")
        print(f"Ticket ID: {ticket_id}")
        print("-" * 50)

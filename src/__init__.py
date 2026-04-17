"""
Banking Customer Support AI Agent
A LangGraph-based intelligent customer support system for banking institutions.
"""

__version__ = "1.0.0"
__author__ = "Mayank"
__email__ = "mayank.jha10@gmail.com"

from .classifier import hf_model_classify
from .agents import app
from .handlers import handle_feedback, handle_query
from .ticket_manager import generate_unique_ticket_id, view_tickets, log_satisfaction

__all__ = [
    "hf_model_classify",
    "app",
    "handle_feedback",
    "handle_query",
    "generate_unique_ticket_id",
    "view_tickets",
    "log_satisfaction",
]

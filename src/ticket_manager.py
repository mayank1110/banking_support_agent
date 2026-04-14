"""
Ticket Manager Module
Handles ticket creation, retrieval, and satisfaction logging.
"""

import os
import random
import pandas as pd
from typing import Optional, Dict, Any

from config import TICKET_CSV, TICKET_ID_MIN, TICKET_ID_MAX


def _ensure_csv_exists():
    """Ensure the ticket CSV file exists with proper headers."""
    if not os.path.exists(TICKET_CSV):
        df = pd.DataFrame(
            columns=["ticket_id", "status", "message", "customer_name", "satisfaction"]
        )
        df.to_csv(TICKET_CSV, index=False)


def generate_unique_ticket_id() -> int:
    """
    Generate a unique 6-digit ticket ID.
    
    Returns:
        Unique ticket ID between 100000 and 999999
    """
    _ensure_csv_exists()
    df = pd.read_csv(TICKET_CSV)
    
    existing_ids = set()
    if not df.empty:
        existing_ids = set(df["ticket_id"].dropna().astype(int).tolist())

    while True:
        ticket_id = random.randint(TICKET_ID_MIN, TICKET_ID_MAX)
        if ticket_id not in existing_ids:
            return ticket_id


def create_ticket(
    ticket_id: int,
    status: str,
    message: str,
    customer_name: str,
    satisfaction: Optional[int] = None,
) -> bool:
    """
    Create a new support ticket.
    
    Args:
        ticket_id: Unique ticket identifier
        status: Ticket status (e.g., "Unresolved", "Resolved")
        message: Customer's message/complaint
        customer_name: Name of the customer
        satisfaction: Optional satisfaction rating (1-5)
        
    Returns:
        True if ticket was created successfully
    """
    _ensure_csv_exists()
    
    new_ticket = {
        "ticket_id": ticket_id,
        "status": status,
        "message": message,
        "customer_name": customer_name,
        "satisfaction": satisfaction,
    }

    df = pd.read_csv(TICKET_CSV)
    df = pd.concat([df, pd.DataFrame([new_ticket])], ignore_index=True)
    df.to_csv(TICKET_CSV, index=False)
    
    return True


def get_ticket_status(ticket_id: int) -> Optional[str]:
    """
    Get the status of a specific ticket.
    
    Args:
        ticket_id: Ticket ID to look up
        
    Returns:
        Ticket status if found, None otherwise
    """
    _ensure_csv_exists()
    df = pd.read_csv(TICKET_CSV)
    
    if df.empty:
        return None
    
    ticket = df[df["ticket_id"] == ticket_id]
    
    if ticket.empty:
        return None
    
    return ticket.iloc[0]["status"]


def get_ticket(ticket_id: int) -> Optional[Dict[str, Any]]:
    """
    Get complete ticket information.
    
    Args:
        ticket_id: Ticket ID to look up
        
    Returns:
        Dictionary with ticket details if found, None otherwise
    """
    _ensure_csv_exists()
    df = pd.read_csv(TICKET_CSV)
    
    if df.empty:
        return None
    
    ticket = df[df["ticket_id"] == ticket_id]
    
    if ticket.empty:
        return None
    
    return ticket.iloc[0].to_dict()


def update_ticket_status(ticket_id: int, new_status: str) -> bool:
    """
    Update the status of an existing ticket.
    
    Args:
        ticket_id: Ticket ID to update
        new_status: New status to set
        
    Returns:
        True if update was successful, False if ticket not found
    """
    _ensure_csv_exists()
    df = pd.read_csv(TICKET_CSV)
    
    if df.empty or ticket_id not in df["ticket_id"].astype(int).tolist():
        return False
    
    df.loc[df["ticket_id"] == ticket_id, "status"] = new_status
    df.to_csv(TICKET_CSV, index=False)
    
    return True


def log_satisfaction(ticket_id: int, satisfaction: int) -> str:
    """
    Log satisfaction rating for a ticket.
    
    Args:
        ticket_id: Ticket ID to rate
        satisfaction: Rating from 1-5
        
    Returns:
        Success or error message
    """
    _ensure_csv_exists()
    
    if ticket_id is None or pd.isna(ticket_id):
        return "No ticket associated with this interaction."

    df = pd.read_csv(TICKET_CSV)
    
    if int(ticket_id) not in df["ticket_id"].astype(int).tolist():
        return f"Ticket #{int(ticket_id)} not found."

    df.loc[df["ticket_id"] == int(ticket_id), "satisfaction"] = int(satisfaction)
    df.to_csv(TICKET_CSV, index=False)
    
    return f"Satisfaction rating {int(satisfaction)}/5 logged for ticket #{int(ticket_id)}."


def view_tickets() -> str:
    """
    Get all tickets as HTML table.
    
    Returns:
        HTML representation of tickets DataFrame, or message if empty
    """
    _ensure_csv_exists()
    df = pd.read_csv(TICKET_CSV)
    
    if df.empty:
        return "No tickets in the system yet."
    
    return df.to_html(index=False)


def get_all_tickets() -> pd.DataFrame:
    """
    Get all tickets as DataFrame.
    
    Returns:
        DataFrame containing all tickets
    """
    _ensure_csv_exists()
    return pd.read_csv(TICKET_CSV)


def get_ticket_count() -> int:
    """
    Get total number of tickets in the system.
    
    Returns:
        Number of tickets
    """
    _ensure_csv_exists()
    df = pd.read_csv(TICKET_CSV)
    return len(df)


def get_unresolved_tickets() -> pd.DataFrame:
    """
    Get all unresolved tickets.
    
    Returns:
        DataFrame containing unresolved tickets
    """
    _ensure_csv_exists()
    df = pd.read_csv(TICKET_CSV)
    
    if df.empty:
        return df
    
    return df[df["status"] == "Unresolved"]


if __name__ == "__main__":
    # Test ticket manager
    print("Testing Ticket Manager...")
    
    # Generate ticket ID
    ticket_id = generate_unique_ticket_id()
    print(f"Generated ticket ID: {ticket_id}")
    
    # Create ticket
    create_ticket(
        ticket_id=ticket_id,
        status="Unresolved",
        message="Test complaint",
        customer_name="Test Customer",
    )
    print(f"Created ticket #{ticket_id}")
    
    # Get status
    status = get_ticket_status(ticket_id)
    print(f"Ticket status: {status}")
    
    # Log satisfaction
    result = log_satisfaction(ticket_id, 4)
    print(f"Satisfaction logging: {result}")
    
    # View tickets
    print("\nAll tickets:")
    print(view_tickets())

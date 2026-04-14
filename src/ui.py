"""
Gradio UI Module
Interactive web interface for the Banking Customer Support AI Agent.
"""

import gradio as gr

from config import GRADIO_SHARE, GRADIO_DEBUG, GRADIO_TITLE
from .agents import app
from .ticket_manager import view_tickets, log_satisfaction


def invoke_agent(message: str, name: str):
    """
    Invoke the LangGraph agent with user input.
    
    Args:
        message: User's message/query
        name: User's name
        
    Returns:
        Gradio updates for classification, response, ticket_id, and UI visibility
    """
    state = {"input": message, "customer_name": name}
    result = app.invoke(state)
    answer = result.get("answer", {}) or {}
    
    classification = answer.get("classification")
    response = answer.get("response")
    ticket_id = answer.get("ticket_id")

    # Prepare visibility updates
    classify_update = gr.update(visible=True, value=classification or "")
    response_update = gr.update(visible=True, value=response or "")
    ticket_update = gr.update(value=ticket_id if ticket_id is not None else None)
    
    # Show satisfaction controls only if a ticket was created/associated
    show_satisfaction = bool(ticket_id)
    slider_update = gr.update(visible=show_satisfaction, value=1 if show_satisfaction else None)
    logbtn_update = gr.update(visible=show_satisfaction)
    
    # Hide log result for new interaction
    log_out_update = gr.update(visible=False, value="")

    return classify_update, response_update, ticket_update, slider_update, logbtn_update, log_out_update


def submit_satisfaction(ticket_id, rating):
    """
    Log satisfaction rating for a ticket.
    
    Args:
        ticket_id: Ticket ID to rate
        rating: Satisfaction rating (1-5)
        
    Returns:
        Gradio update with logging result
    """
    msg = log_satisfaction(ticket_id, rating)
    return gr.update(visible=True, value=msg)


def create_ui() -> gr.Blocks:
    """
    Create the Gradio web interface.
    
    Returns:
        Gradio Blocks application
    """
    with gr.Blocks(title=GRADIO_TITLE) as demo:
        gr.Markdown("# 🏦 Banking Customer Support AI Agent")
        gr.Markdown(
            "An intelligent AI-powered customer support agent for banking institutions. "
            "Classifies your messages and provides appropriate responses."
        )

        with gr.Row():
            user_message = gr.Textbox(
                label="Your Query",
                lines=3,
                placeholder="Enter your banking support message (or include a 6-digit ticket ID to check status)...",
            )
            user_name = gr.Textbox(
                label="Your Name", placeholder="Enter your name", value="Customer"
            )

        with gr.Row():
            submit_btn = gr.Button("Submit", variant="primary")
            view_btn = gr.Button("View All Tickets", variant="secondary")

        # Output components (initially hidden)
        classify_out = gr.Textbox(label="Classification", visible=False)
        response_out = gr.Textbox(label="Agent Response", visible=False)
        hidden_ticket_id = gr.Number(visible=False, label="Ticket ID")

        # Satisfaction controls (shown only when ticket exists)
        gr.Markdown("### Rate Your Experience")
        satisfaction_slider = gr.Slider(
            minimum=1, maximum=5, step=1, label="Satisfaction Rating (1-5)", visible=False
        )
        log_btn = gr.Button("Log Satisfaction", visible=False)
        log_out = gr.Textbox(label="Satisfaction Logging Result", visible=False)

        # Tickets display
        gr.Markdown("### Ticket Database")
        tickets_html = gr.HTML(label="Stored Tickets")

        # Wire up event handlers
        submit_btn.click(
            fn=invoke_agent,
            inputs=[user_message, user_name],
            outputs=[
                classify_out,
                response_out,
                hidden_ticket_id,
                satisfaction_slider,
                log_btn,
                log_out,
            ],
        )

        view_btn.click(
            fn=view_tickets,
            inputs=[],
            outputs=[tickets_html],
        )

        log_btn.click(
            fn=submit_satisfaction,
            inputs=[hidden_ticket_id, satisfaction_slider],
            outputs=[log_out],
        )

    return demo


def launch_ui(share: bool = None, debug: bool = None):
    """
    Launch the Gradio web interface.
    
    Args:
        share: Create public shareable link (default: from config)
        debug: Enable debug mode (default: from config)
    """
    demo = create_ui()
    demo.launch(
        share=share if share is not None else GRADIO_SHARE,
        debug=debug if debug is not None else GRADIO_DEBUG,
    )


if __name__ == "__main__":
    launch_ui()

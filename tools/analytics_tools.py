from crewai.tools import tool
import logging

logger = logging.getLogger(__name__)

@tool
def get_stripe_service_status(service_name: str) -> str:
    """
    Simulates checking the status of a Stripe service.
    For this example, it returns a generic 'operational' status.
    Args:
        service_name (str): The name of the Stripe service.
    Returns:
        str: A message indicating the simulated status of the service.
    """
    if not isinstance(service_name, str) or not service_name.strip():
        return "Error: Service name must be provided."
    return f"The Stripe service '{service_name}' is reported as operational (simulated)."

@tool
def get_common_stripe_integration_issues() -> str:
    """
    Provides a list of common integration issues with Stripe.
    Returns:
        str: A string containing common issues and advice.
    """
    return """Common Stripe Integration Issues & Troubleshooting:
1. API Key Errors: Ensure correct (test vs. live) and valid API keys.
2. Incorrect Request Parameters: Double-check Stripe API documentation.
3. Webhook Endpoint Issues: Verify public accessibility and correct handling.
4. Client-Side Tokenization: Ensure secure tokenization.
5. Idempotency: Use idempotency keys for critical operations.
6. Versioning: Be mindful of Stripe API versioning.
General Troubleshooting: Check Stripe Dashboard logs, use official SDKs, consult API documentation and support resources."""

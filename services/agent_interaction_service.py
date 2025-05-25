from agents.stripe_expert_agent import StripeExpertAgent
import logging

logger = logging.getLogger(__name__)

class AgentInteractionService:
    def __init__(self):
        try:
            self.stripe_agent = StripeExpertAgent()
        except Exception as e:
            logger.critical(f"Failed to initialize StripeExpertAgent in AgentInteractionService: {e}", exc_info=True)
            raise RuntimeError(f"AgentInteractionService: StripeExpertAgent initialization failed: {e}") from e

    def ask_stripe_expert(self, question: str) -> str:
        try:
            answer = self.stripe_agent.ask(question)
            return answer
        except Exception as e:
            logger.error(f"Error during agent interaction for question '{question}': {e}", exc_info=True)
            return "I apologize, but an unexpected error occurred."

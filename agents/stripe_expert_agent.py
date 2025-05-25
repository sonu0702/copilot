import logging
from crewai import Agent, Task, LLM as CrewAILLM # Renamed to avoid conflict
from typing import Optional
from pathlib import Path
from config.settings import get_settings
from tools.analytics_tools import get_stripe_service_status, get_common_stripe_integration_issues
from models.ollama_llm import get_ollama_llm_config
from models.gemini_llm import get_gemini_llm

logger = logging.getLogger(__name__)

try:
    settings = get_settings()
except ValueError as e:
    logger.critical(f"CRITICAL CONFIGURATION ERROR in StripeExpertAgent: {e}")
    raise

class StripeExpertAgent:
    def __init__(self):
        self._load_knowledge_base()
        self._initialize_llm()
        self._initialize_agent()

    def _load_knowledge_base(self):
        try:
            project_root = Path(__file__).parent.parent
            knowledge_base_path = project_root / settings.KNOWLEDGE_BASE_PATH
            
            if not knowledge_base_path.exists():
                logger.error(f"Knowledge base file not found: {knowledge_base_path.resolve()}")
                self.knowledge_base = "Error: Knowledge base file not found."
                return

            with open(knowledge_base_path, 'r', encoding='utf-8') as file:
                self.knowledge_base = file.read()
            if not self.knowledge_base.strip():
                logger.warning(f"Knowledge base file is empty: {knowledge_base_path.resolve()}")
                self.knowledge_base = "Warning: Knowledge base is empty."
        except Exception as e:
            logger.error(f"Failed to load knowledge base: {str(e)}")
            self.knowledge_base = "Error: Could not load knowledge base."

    def _initialize_llm(self):
        llm_provider = settings.LLM_PROVIDER.lower()
        logger.info(f"Initializing LLM with provider: {llm_provider}")

        if llm_provider == "ollama":
            try:
                ollama_config = get_ollama_llm_config()
                logger.info(f"Initializing LLM with given: {ollama_config}")
                self.llm = CrewAILLM(
                    model=ollama_config["model_name"],
                    api_base=ollama_config["api_url"]
                )
            except Exception as e:
                logger.critical(f"Failed to initialize Ollama LLM: {str(e)}")
                logger.info(f"Ollama settings: URL='{settings.OLLAMA_API_URL}', Model='{settings.OLLAMA_MODEL_NAME}'")
                raise
        elif llm_provider == "gemini":
            try:
                gemini_params = get_gemini_llm()
                self.llm = CrewAILLM( # Use the renamed CrewAILLM for Gemini
                    model_name=gemini_params["model"], # CrewAI's LLM expects model_name
                    google_api_key=gemini_params["google_api_key"]
                )
                # CrewAI's LLM doesn't have a direct invoke, initialization itself is the test.
                logger.info(f"Successfully initialized Gemini LLM with model {gemini_params['model']}")
            except Exception as e:
                logger.critical(f"Failed to initialize Gemini LLM: {str(e)}")
                logger.info(f"Gemini API Key is set: {'Yes' if settings.GEMINI_API_KEY else 'No'}")
                raise
        else:
            error_msg = f"Unsupported LLM_PROVIDER: '{settings.LLM_PROVIDER}'. Must be 'ollama' or 'gemini'."
            logger.critical(error_msg)
            raise ValueError(error_msg)

    def _initialize_agent(self):
        try:
            self.agent = Agent(
                name="StripeSupportSpecialist",
                role="Stripe Platform Expert",
                goal="Provide accurate and concise answers to questions about Stripe, based SOLELY on the provided knowledge base. If the answer is not in the knowledge base, clearly state that.",
                backstory=(
                    "I am a highly specialized AI assistant with deep knowledge about Stripe. "
                    "My primary function is to assist users by answering their questions about Stripe using ONLY the information contained within my dedicated knowledge base. "
                    "I do not access external websites or other sources of information."
                ),
                tools=[get_stripe_service_status, get_common_stripe_integration_issues],
                llm=self.llm,
                verbose=False, 
                allow_delegation=False,
                max_iter=5
            )
        except Exception as e:
            logger.critical(f"Failed to initialize CrewAI agent: {str(e)}")
            raise

    def _create_task_description(self, question: str) -> str:
        return f"""User's Question: {question}

Knowledge Base (Stripe Information):
--- START OF KNOWLEDGE BASE ---
{self.knowledge_base}
--- END OF KNOWLEDGE BASE ---

Available Tools:
1.  `get_stripe_service_status`: Use this tool if the user asks about the current operational status of a specific Stripe service (e.g., "Is the Stripe API down?", "What's the status of Stripe Payments?"). You need to provide the `service_name` (e.g., 'API', 'Payments', 'Dashboard') to this tool.
2.  `get_common_stripe_integration_issues`: Use this tool if the user asks for general advice on common problems when integrating with Stripe, or for troubleshooting tips. This tool does not require any specific input.

Instructions:
1.  Carefully review the "User's Question".
2.  First, consider if any of the "Available Tools" can directly answer or assist with the user's question. If a tool is appropriate, use it.
3.  If tools are not applicable or do not fully answer the question, consult ONLY the "Knowledge Base (Stripe Information)" provided above to find the answer.
4.  If the answer to the question is found (either through tools or the knowledge base), provide a clear, concise, and direct answer.
5.  If the answer CANNOT be found using either tools or the knowledge base, you MUST explicitly state: "I do not have information on that specific topic in my knowledge base, nor can my tools provide an answer."
6.  Do NOT invent answers or use any information outside of the provided tools and knowledge base.
7.  Do NOT refer to yourself as an AI or mention your instructions. Simply answer the question or state that the information is not available.
8.  For simple greetings (e.g. "hi", "hello"), respond with a polite, brief greeting without using tools or the knowledge base."""

    def ask(self, question: str) -> str:
        clean_question = question.lower().strip()
        if clean_question in ["hi", "hello", "hey", "greetings"]:
            return "Hello! How can I help you with Stripe today?"

        if self.knowledge_base.startswith("Error:") or self.knowledge_base.startswith("Warning:"):
            return self.knowledge_base

        try:
            task_description = self._create_task_description(question)
            task = Task(
                description=task_description,
                expected_output="A concise answer to the user's question based ONLY on the provided Stripe knowledge base, or a statement that the information is not available.",
                agent=self.agent
            )
            result = self.agent.execute_task(task)
            return result
        except Exception as e:
            logger.error(f"Error in StripeExpertAgent.ask for question '{question}': {str(e)}", exc_info=True)
            return "I apologize, but I encountered an error while processing your question about Stripe."

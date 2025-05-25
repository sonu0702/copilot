# copilot
AI Copilot using crewAI

## Frequently used cmds
```
# setting up virtual env
python3 -m venv copilot
source ./copilot/bin/activate

# Intall packages
pip3 install -r requirements.txt

# Check .env is setup

#When LLM_PROVIDER is set to "ollama",
#the agent will use your local Ollama model.
#Make sure your Ollama server is running.
#When LLM_PROVIDER is set to "gemini", it will use the Gemini API.


# Run the server
uvicorn main:app --reload

```
## Sample API call 

```
curl --location 'http://127.0.0.1:8000/ask' \
--header 'Content-Type: application/json' \
--data '{
    "question" : "stripe"
}'
```
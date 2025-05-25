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
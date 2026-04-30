"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml
"""

import sys
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml

load_dotenv()
prompt_key = "leonanluppi/bug_to_user_story_v1"

def pull_prompts_from_langsmith():
    prompt = hub.pull(prompt_key)
    print(prompt)
    messages = []
    for msg in prompt.messages:
        messages.append({
            "role": msg.__class__.__name__.replace("MessagePromptTemplate", "").lower(),
            "content": msg.prompt.template
        })
    return {"messages": messages}

def main():
    """Função principal"""
    prompt = pull_prompts_from_langsmith()
    save_yaml(prompt, "prompts/bug_to_user_story_v1.yml")


if __name__ == "__main__":
    sys.exit(main())

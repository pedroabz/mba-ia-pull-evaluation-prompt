"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langsmith import Client
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()
yaml_path = "prompts/bug_to_user_story_v2.yml"

def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    messages = [
        (m["role"], m["content"])
        for m in prompt_data["messages"]
    ]

    prompt = ChatPromptTemplate.from_messages(messages)

    client = Client()
    url = client.push_prompt(
        prompt_name,
        object=prompt,
        is_public=True,
        description="Prompt otimizado para converter relatos de bugs em user stories.",
        tags=["few-shot", "chain-of-thought", "role-prompting"],
    )

    print(f"Prompt pushed to LangSmith: {url}")
    return True



def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []

    # 1. Messages devemexistir
    if "messages" not in prompt_data:
        errors.append("Missing 'messages' key")
        return False, errors

    #2. Messages devem ser uma lista
    if not isinstance(prompt_data["messages"], list):
        errors.append("'messages' must be a list")
        return False, errors

    # 3. Cada message deve ter 'role' e 'content'
    for i, msg in enumerate(prompt_data["messages"]):
        if "role" not in msg:
            errors.append(f"Message {i} missing 'role'")
        if "content" not in msg:
            errors.append(f"Message {i} missing 'content'")

    if errors:
        return False, errors

    # 4. Validar as roles (system, human, assistant)
    valid_roles = {"system", "human"}
    for i, msg in enumerate(prompt_data["messages"]):
        role = msg.get("role")
        if role not in valid_roles:
            errors.append(f"Message {i} has invalid role: {role}")

    # 5. Validar variável obrigatória
    has_bug_report = any(
        "{bug_report}" in msg["content"]
        for msg in prompt_data["messages"]
    )

    if not has_bug_report:
        errors.append("Missing '{bug_report}' variable in prompt")

    return len(errors) == 0, errors


def main():
    """Função principal"""
    print_section_header("Push de Prompts para LangSmith Hub")

    # 1. Verificar variáveis de ambiente
    if not check_env_vars(["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]):
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB")
    prompt_name = f"{username}/bug_to_user_story_v2"

    # 2. Carregar o prompt do YAML
    print(f"\nCarregando prompt de: {yaml_path}")
    prompt_data = load_yaml(yaml_path)
    if prompt_data is None:
        return 1

    # 3. Validar o prompt
    print("Validando prompt...")
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("Prompt inválido:")
        for error in errors:
            print(f"   - {error}")
        return 1
    print("Prompt válido!")

    # 4. Push para o LangSmith Hub
    print(f"\nFazendo push do prompt como: {prompt_name}")
    if not push_prompt_to_langsmith(prompt_name, prompt_data):
        return 1

    print("\nPush concluído com sucesso!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

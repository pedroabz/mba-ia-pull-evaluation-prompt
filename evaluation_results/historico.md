# Histórico de Avaliações

## Iteração 1 — Prompt com checkbox e [Suposição]
- Prompt no Hub desatualizado (versão antiga)
- F1: 0.76 | Clarity: 0.89 | Precision: 0.86 | Helpfulness: 0.88 | Correctness: 0.81
- **Media: ~0.84**

## Iteração 2 — Prompt simplificado (2 exemplos, sem regras complexas)
- Versão mais enxuta, apenas formato + instruções + 2 exemplos (simples e médio)
- F1: 0.81 | Clarity: 0.91 | Precision: 0.92 | Helpfulness: 0.92 | Correctness: 0.86
- **Media: 0.8838** (melhor resultado)
- Backup: N/A (não salvo)

## Iteração 3 — Regra "não inventar features" + 3 exemplos + classificação complexidade
- Adicionou regra fundamental, classificação explícita, exemplo complexo (delivery)
- F1: 0.79 | Clarity: 0.89 | Precision: 0.86 | Helpfulness: 0.87 | Correctness: 0.82
- **Media: 0.8455**

## Iteração 4 — Classificação de complexidade detalhada + seções explicitadas
- Definições detalhadas de simples/médio/complexo, lista de seções por domínio
- Classificação 15/15 correcta, mas prompt pesado demais
- F1: 0.80 | Clarity: 0.89 | Precision: 0.81 | Helpfulness: 0.85 | Correctness: 0.80
- **Media: 0.8291**
- Backup: `prompts/bug_to_user_story_v2_backup_complexidade.yml`

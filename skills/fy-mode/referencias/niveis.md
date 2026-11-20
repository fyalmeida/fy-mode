# Níveis de esforço por fornecedor

O método fala em níveis: baixo, médio, alto. Esta página traduz para cada ferramenta.

## Por que um modelo só

- Trocar para um modelo mais barato muda o teto de inteligência. Baixar o esforço do modelo forte dá economia parecida sem mudar o teto.
- Num teste público de revisão de código da CodeRabbit, com 13 casos difíceis de bug conhecido, o modelo intermediário achou 6 e o modelo forte achou de 8 a 10. A amostra é pequena, e o próprio post diz isso.
- Cache de prompt é separado por modelo. Um modelo só reaproveita mais.

## Claude Code (Anthropic) — medido

Modelo: `opus` em todos os papéis.

| Nível do método | `effort` |
|---|---|
| baixo | `low` |
| médio | `medium` |
| alto | `high` |
| um nível acima de alto | `xhigh` |

Os agentes em `agents/` já trazem `model` e `effort` no cabeçalho. Para mudar um nível, edite o cabeçalho do agente.

## Outras ferramentas — não testado

Use o modelo de código mais forte do fornecedor em todos os papéis e o controle de raciocínio que ele oferecer (costuma se chamar "reasoning effort"). Se a ferramenta não tiver esse controle, rode todos os papéis no padrão.

Se você testar em outra ferramenta, meça antes e depois e mande a tradução por pull request.

## Como ajustar com medição

Os níveis da tabela de papéis são ponto de partida. Para ajustar:

1. Rode uma fase inteira com os níveis atuais e meça com `scripts/medir.py`.
2. Mude um papel por vez, um nível por vez.
3. Rode outra fase e compare o custo por tarefa concluída e o número de rodadas de correção. Custo menor com mais rodadas não é economia.

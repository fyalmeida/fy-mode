# Roteiro: bug

Sem painel e sem auditor. Copie os passos para a lista de tarefas.

1. **Reproduza.** Faça o erro acontecer de verdade: a requisição, o comando ou o caminho na tela, em ambiente isolado e com cópia dos dados do caso. Guarde a saída em `bugs/<id>/saidas/`. Se não reproduzir, não há correção: aperte as condições, adicione registro de log e tente de novo, ou leve à pessoa o que falta para reproduzir. Palpite sobre a causa, seu ou da pessoa, não substitui este passo e não entra em nenhum pedido.
2. **Escreva o comportamento esperado.** Duas linhas em `bugs/<id>/esperado.md`: o que acontece hoje e o que deveria acontecer, com a fonte (spec, documentação ou a pessoa). Se a fonte não define o esperado, pergunte à pessoa. Se o esperado for uma regra de negócio nova, pare: isso é funcionalidade, vá para `feature.md`.
3. **Mapa.** Um `mapeador` para o trecho afetado, escrevendo em `bugs/<id>/mapa.md`. No lugar da spec e do plano, o pedido aponta para `esperado.md`.
4. **Autor de testes novo.** Recebe `esperado.md` e as seções Contratos e Testes do mapa. Escreve o teste que falha pelo motivo do bug. Rode e guarde a saída falhando.
5. **Implementador novo.** Corrige a causa, com a menor mudança que faz o teste passar. Proteção que "pode ajudar" e não tem evidência não entra.
6. **Testes.** Rode o teste novo e os contratos vizinhos. Vermelho: correção com implementador novo, um nível de esforço acima. O mesmo teste vermelho depois de duas correções: freio de rodadas.
7. **Revisor novo.** Achados tratados pela classe, conforme o `SKILL.md`.
8. **Reproduza de novo.** Repita exatamente o passo 1. O erro não pode mais acontecer. Teste unitário verde não substitui este passo.
9. **Commit.** Um commit com o teste e a correção.

**Relatório:** o que estava quebrado, a causa, a correção, e as duas saídas coladas: a do passo 1 falhando e a do passo 8 passando.

# Roteiro: funcionalidade com spec e plano

Copie os passos para a lista de tarefas. Os passos 1 a 4 acontecem uma vez por fase; os passos 5 a 10, uma vez por tarefa; os passos 11 a 13, no fim da fase.

## Antes da fase

1. **Painel de testes.** Lance um `especialista-de-testes` novo por lente, em paralelo. Cada um recebe só a spec, o plano e a lente:
   - regras de negócio e aceitação;
   - dados e concorrência (idempotência, repetição, transação, migração);
   - o ambiente de execução específico do projeto;
   - erros e o que o usuário vê;
   - regressão e compatibilidade (o que não pode mudar);
   - advogado do diabo (casos de borda, e como um teste fraco deixaria o erro passar).

   Una os catálogos num só, por tarefa. As dúvidas de spec vão para a pessoa.
2. **Escolha dos testes e o que vai para a pessoa.** Corte o catálogo para o essencial de cada tarefa: um caso por regra da spec, mais os casos de borda que mudam o resultado. Essa lista você decide sozinho. Separe para a pessoa, numa página só, em linguagem clara e com um exemplo concreto por item: os casos em que você tem dúvida sobre o comportamento esperado, os casos sobre o que o usuário vê, e os testes manuais da fase (os que a spec já traz ou, se ela não traz, até cinco sugestões suas, cada uma dizendo por que um teste automático não prova aquilo). A pessoa responde quais acha bons e pode sugerir outros; avalie cada sugestão e diga por quê quando alguma não fizer sentido. Grave o resultado em `catalogo-testes.md` e `testes-manuais.md`.
3. **Tamanho das tarefas.** Uma tarefa é um comportamento verificável. Tarefa com mais de um ponto de entrada novo, ou que o plano prevê mexer em mais de cinco arquivos, é dividida no plano antes de começar.
4. **Mapas.** Lance um `mapeador` por tarefa, em paralelo. Leia o "Não encontrado" de cada mapa: ponto de entrada novo sem assinatura no plano é corrigido no plano agora.

## Por tarefa

5. **Autor de testes novo.** Escreve os testes da tarefa. Rode os testes: eles precisam falhar numa verificação do comportamento da tarefa, não por erro de import, de dados de apoio ou de ambiente.
6. **Implementador novo.** Recebe os testes prontos e não os altera.
7. **Testes.** Rode os testes da tarefa, os contratos vizinhos e as verificações automáticas do projeto (lint, tipos), com os comandos do mapa. Vermelho: correção com um implementador novo, um nível de esforço acima. O mesmo teste vermelho depois de duas correções: aplique o freio de rodadas.
8. **Revisor novo.**
9. **Achados.** Todo achado é suspeita até ser confirmado. Confirme e trate cada um pela classe (comportamento, regra escrita, opinião), conforme a tabela do `SKILL.md`. Houve correção: revisor novo na versão final.
10. **Commit.** Um commit com o código e os testes da tarefa.

## Fim da fase

11. **Prova na superfície real.** Execute os testes manuais aprovados, por onde o usuário usa: a requisição, a tela, o comando. Execute você os que são requisição, comando ou navegador automatizado, e guarde a saída. Entregue à pessoa, de uma vez, os que exigem olho humano, com os passos prontos. Grave o resultado de cada item em `testes-manuais.md`. Item que falhar é achado de comportamento e volta ao passo 9. Item não executado aparece no relatório como "não executado".
12. **Auditor novo.** Um `auditor` que não participou de nenhuma tarefa confere a fase inteira contra a spec e recebe as opiniões registradas pelos revisores.
13. **Relatório.** Por tarefa: ✅ 🔄 ⬜, os testes que rodaram e o resultado. Por teste manual: passou, falhou ou não executado. Por achado de revisor: o que foi apontado, a classe, o resultado da prova e o que foi feito, para a pessoa conferir.

# Roteiro: ajuste pequeno

Só para mudança que atende às quatro condições do `SKILL.md`: um arquivo só de código, sem regra de negócio nova, sem migração, e todo texto que o usuário vê foi dado pela pessoa palavra por palavra. Falhou uma condição: use `bug.md` ou `feature.md`.

Sem painel e sem auditor. Os papéis continuam separados: quem escreve o teste não escreve o código. Um agente que escreve os dois leva o mesmo engano para os dois, e o engano só aparece depois, como rodada de correção.

O mapa e as saídas deste roteiro ficam numa pasta temporária fora do repositório.

1. **Mapeador.** O pedido traz o pedido da pessoa, palavra por palavra, e o caminho do arquivo. Ele escreve o mapa do arquivo: Contratos, Testes e Onde mexer.
2. **Autor de testes novo.** Recebe o pedido da pessoa, palavra por palavra, e as seções Contratos e Testes do mapa. Escreve o teste do comportamento pedido. Se um teste que já existe cobra o comportamento antigo, é ele quem atualiza esse teste. Rode e guarde a saída falhando.
3. **Implementador novo.** Recebe o teste pronto e não o altera. Se precisar mexer num segundo arquivo de código, ele para e avisa: a tarefa deixou de ser ajuste pequeno.
4. **Testes.** Rode o teste novo e os testes do arquivo alterado. Vermelho: correção com implementador novo, um nível de esforço acima. O mesmo teste vermelho depois de duas correções: freio de rodadas.
5. **Revisor novo.** Achados confirmados e tratados pela classe, conforme o `SKILL.md`.
6. **Commit.** Um commit com a mudança e o teste.

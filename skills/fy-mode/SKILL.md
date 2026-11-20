---
name: fy-mode
description: Usar quando for implementar funcionalidade com spec e plano, corrigir bug ou fazer ajuste de código coordenando subagentes; quando for escrever o pedido de um mapeador, autor de testes, implementador, revisor ou auditor; quando uma correção falhar de novo no mesmo teste; quando um revisor apontar algo que não vira teste; ou quando o usuário pedir fy mode ou /fy-mode.
---

# fy mode

Desenvolvimento com agentes em papéis separados: um escreve a prova sem ver a resposta, outro responde sem poder mudar a prova, um terceiro corrige. Ninguém confere o próprio trabalho.

Você é o coordenador. Você não escreve teste nem código da tarefa: escolhe o roteiro, escreve os pedidos, roda os testes e confere o que volta.

## Regras que não mudam

Valem em todo roteiro, inclusive no ajuste pequeno:

1. O teste nasce antes do código, escrito por um autor que não vê o código, e é visto falhando antes de o código mudar.
2. O implementador não altera teste. Se um teste parecer contradizer a spec, ele para e a pessoa responsável decide.
3. Teste falhou: corrige-se o código, nunca o teste. Teste só muda quando a spec ou a pessoa muda o comportamento esperado, e muda antes do código, pelas mãos de um autor de testes.
4. Toda rodada é um agente novo. Nenhum agente é reaproveitado na mesma tarefa, nem para correção.
5. O pedido a um agente não leva resumo, conclusão nem dica do coordenador. Decisão entra na spec ou no plano, e o agente lê de lá.
6. Commit só com os testes da tarefa verdes. Um commit por tarefa, incluindo as correções feitas antes dele. Correção feita depois do commit da tarefa sai em commit próprio. Push só com autorização explícita da pessoa.
7. Testes rodam em ambiente isolado, nunca contra banco real, um processo de teste por vez.

## Escolha o roteiro

| A tarefa é | Roteiro |
|---|---|
| Funcionalidade com spec e plano de tarefas | `roteiros/feature.md` |
| Algo que funcionava e parou, ou comportamento diferente do combinado | `roteiros/bug.md` |
| Mudança que atende às quatro condições abaixo | `roteiros/ajuste-pequeno.md` |

As quatro condições do ajuste pequeno: mexe em um arquivo só de código (o arquivo de teste não conta); não cria regra de negócio; não tem migração; todo texto que o usuário vê na mudança foi dado pela pessoa, palavra por palavra.

Funcionalidade nova sem spec e plano não tem roteiro aqui: a spec e o plano vêm primeiro.

Em dúvida entre dois roteiros, use o mais completo. Abra o roteiro e copie os passos dele para a lista de tarefas antes de começar.

## Papéis e esforço de raciocínio

Um modelo só, o mais forte de código do fornecedor, em todos os papéis. O que muda é o esforço de raciocínio.

| Papel | Julga? | Esforço |
|---|---|---|
| Mapeador | não | baixo |
| Especialista de testes (painel) | sim | alto |
| Autor de testes | sim | alto |
| Implementador | não | alto |
| Revisor | sim | médio |
| Auditor de fase | sim | alto |
| Analista de premissa | sim | alto |

Correção depois de teste vermelho roda um nível acima do nível normal do papel, na primeira e na segunda correção. Correção de achado de revisor roda no nível normal do papel. Para subir o nível de um agente do plugin, passe o esforço na chamada. A tradução desses níveis para cada fornecedor está em `referencias/niveis.md`.

No Claude Code, com o plugin instalado, os agentes já trazem o nível certo: `fy-mode:mapeador`, `fy-mode:autor-de-testes`, `fy-mode:implementador`, `fy-mode:revisor`, `fy-mode:auditor`, `fy-mode:especialista-de-testes` e `fy-mode:analista-de-premissa`.

Se esses agentes não aparecerem entre os disponíveis, use um agente genérico: passe o esforço da tabela na chamada e comece o pedido com `Leia <caminho absoluto de agents/<papel>.md> antes de qualquer coisa.` A pasta `agents/` fica na raiz do repositório, dois níveis acima deste arquivo.

## O mapa vem antes do trabalho

Agente que começa sem saber onde está o código gasta a maior parte dos passos procurando. Antes de qualquer autor de testes ou implementador, um mapeador escreve o mapa da tarefa em arquivo. O formato do mapa e o que cada papel pode ler dele estão em `referencias/pedidos.md`.

O mapa só tem fatos localizáveis: caminho, linha, assinatura, comando. Nenhuma opinião sobre como implementar.

## O pedido

Leia `referencias/pedidos.md` antes de escrever qualquer pedido. Todo pedido tem as mesmas seis partes, na mesma ordem, e aponta para arquivos em vez de colar o conteúdo deles.

## Freio de rodadas

O mesmo teste continua vermelho depois de duas correções (a implementação original não conta como correção): a terceira correção não acontece. Lance um `analista-de-premissa` novo com a spec, o plano, o teste que falha e a saída dos testes. Ele devolve um de três vereditos:

| Veredito | O que fazer |
|---|---|
| Spec ambígua ou incompleta | Pare e leve a dúvida à pessoa. A resposta entra na spec. |
| Teste errado (contradiz a spec ou usa interface que não existe) | Autor de testes novo, com spec, plano e mapa atualizados. |
| Tarefa grande demais | Divida a tarefa no plano e recomece pelas partes. |

Pressa não suspende o freio: diga à pessoa por que a terceira correção tende a falhar e lance o analista na hora. Se, sabendo disso, a pessoa mandar corrigir de novo, a decisão é dela e vai para o relatório.

## Achados do revisor

O revisor não edita código: ele relata e classifica. Todo achado é uma suspeita até ser confirmado, e cada classe tem a sua prova. Nenhum achado vai como recado para outro agente: ele entra num arquivo, e o próximo agente lê o arquivo.

| Classe | Critério | Onde entra | Como se confirma e quem resolve |
|---|---|---|---|
| Comportamento | O código faz algo diferente da spec | No catálogo de testes da tarefa, como caso novo, citando o trecho da spec | Autor de testes novo escreve o teste a partir da spec. Teste falha: a falha é real, e um implementador novo corrige. Teste passa: o achado não procede, e o teste fica |
| Regra escrita | Viola uma regra que está num arquivo do projeto (convenção, arquitetura, duplicação proibida) | No plano, como item de conformidade da tarefa, citando a regra (arquivo e seção) e a violação (`arquivo:linha`) | Você abre os dois trechos citados e confere que a regra existe e que a violação está lá. Confere: implementador novo corrige. Não confere: vira opinião |
| Opinião | Não há spec nem regra escrita que sustente | No arquivo de opiniões da fase | Auditor da fase avalia. Não abre rodada |

Se confirmar um achado depende de saber se o comportamento é o esperado e a spec não responde ao pé da letra, pare e pergunte à pessoa antes de qualquer correção. O revisor pode ter lido a spec de um jeito e a pessoa querer outro.

Os achados de um mesmo revisor são resolvidos numa rodada só: um autor de testes novo para os casos de comportamento e um implementador novo para tudo. A versão final passa por um revisor novo antes do commit.

Caso novo no catálogo que sai da spec ao pé da letra não precisa de nova aprovação. Se exigir interpretação da spec, a pessoa decide.

No máximo duas rodadas de revisão por tarefa. Na segunda, só achado de comportamento abre correção; os outros vão para o arquivo de opiniões.

Os caminhos desses arquivos estão em `referencias/pedidos.md`.

## A pessoa decide

Pare e pergunte só nestes casos: dúvida de regra de negócio, texto que o usuário vê, mudança em fluxo que já existe, mockup e push. Respondido, siga sem pedir confirmação de novo.

A lista de testes de cada fase é aprovada pela pessoa de uma vez, numa página, em linguagem clara e com um exemplo concreto por grupo de testes. Os testes manuais da fase vão na mesma página.

## Testes manuais

Teste manual é para o que o teste automático não prova: as peças funcionando juntas de verdade, a tela e o texto como o usuário vê, o serviço de terceiro real, e a pergunta "era isso mesmo que eu queria?".

- **Quem sugere e quem decide.** A IA sugere na consolidação da spec; a pessoa corta o que não for necessário. Zero itens é uma resposta válida.
- **Limite.** A IA sugere no máximo cinco por fase, e cada sugestão diz por que um teste automático não prova aquilo. Item que dá para automatizar vira caso do catálogo e sai da lista. A pessoa pode acrescentar itens; o limite vale para as sugestões da IA.
- **Quando roda.** No fim da fase, na prova na superfície real, antes do auditor. A IA executa o que for requisição, comando ou navegador automatizado; a pessoa executa o que exige olho humano.
- **Se falhar.** É achado de comportamento: entra no catálogo, um autor de testes novo escreve o teste automático que falha, um implementador novo corrige. Nada é consertado à mão.
- **No relatório.** Cada item aparece como passou, falhou ou não executado.

O formato de cada item está em `referencias/pedidos.md`.

## Repetição vira script

Instrução que você escreve pela segunda vez em pedidos (montar o ambiente, rodar os testes da tarefa) vira um script no projeto. O mapa passa a apontar para o script.

## Relatório

A cada fase concluída, informe por tarefa: ✅ feito, 🔄 em andamento, ⬜ falta, com os testes que rodaram e o resultado de cada um. Diga também o que não foi verificado.

O relatório traz também todos os achados dos revisores da fase, um por linha, em linguagem clara: o que o revisor apontou, a classe, o resultado da prova (confirmado ou não procede) e o que foi feito. A pessoa lê essa lista para conferir se algum comportamento tratado como erro era o esperado. Se era, a spec é corrigida primeiro, e um autor de testes novo ajusta o teste antes de o código mudar.

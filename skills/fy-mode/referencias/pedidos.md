# Pedidos e mapa

## As seis partes de todo pedido

Todo pedido a um agente tem estas partes, nesta ordem, e mais nada:

1. **Papel.** Uma linha: qual papel e qual tarefa (id do plano).
2. **Spec e plano.** Os caminhos dos arquivos e o id da tarefa. O agente lê de lá. Em bug, o caminho de `esperado.md`. Em ajuste pequeno, o pedido da pessoa, palavra por palavra.
3. **Mapa.** O caminho do arquivo do mapa e quais seções o papel pode ler.
4. **Arquivos do papel.** Para o implementador e o revisor, os caminhos dos testes da tarefa. Para o implementador de uma correção, também o arquivo com a saída dos testes vermelhos. Para o revisor e o auditor, a referência do que mudou: as mudanças ainda não commitadas em relação ao commit base, ou o commit.
5. **Critério de pronto.** O que precisa ser verdade para o trabalho estar feito, em termos que o agente consegue conferir.
6. **Formato da resposta.** Copiado da seção do papel, abaixo.

O pedido aponta para arquivos. Ele não cola trecho de spec, não resume a tarefa com as suas palavras e não diz o que você espera encontrar.

## O que cada papel recebe

| Papel | Recebe | Seções do mapa |
|---|---|---|
| Mapeador | Spec, plano, id da tarefa | escreve o mapa |
| Especialista de testes | Spec e plano, mais a lente dele | nenhuma |
| Autor de testes | Spec, plano, catálogo de testes da tarefa | Contratos, Testes |
| Implementador | Spec, plano, testes prontos | todas |
| Revisor | Spec, plano, testes, o que mudou | todas |
| Auditor de fase | Spec, plano, o que mudou na fase, opiniões registradas pelos revisores, evidências dos testes manuais | todas |
| Analista de premissa | Spec, plano, o teste que falha, a saída dos testes | Contratos |

O autor de testes lê só a spec, o plano, o catálogo e as seções Contratos e Testes do mapa. Se faltar algo para escrever o teste, ele responde "falta no mapa" e diz o quê. Ele não procura no código da funcionalidade.

Nenhum papel recebe relatório de outro agente da mesma tarefa.

## Onde ficam os arquivos

Tudo o que um agente precisa ler está em arquivo. Em funcionalidade, na pasta do plano:

| Arquivo | Conteúdo |
|---|---|
| `catalogo-testes.md` | Casos de teste por tarefa, aprovados pela pessoa. Achado de comportamento entra aqui |
| `mapas/<id-da-tarefa>.md` | O mapa da tarefa |
| `opinioes.md` | Achados de classe "opinião", para o auditor da fase |
| `saidas/<id-da-tarefa>-<n>.txt` | Saída de testes que outro agente precisa ler |
| `testes-manuais.md` | Os testes manuais da fase, aprovados pela pessoa, com o resultado e a evidência de cada um |

Em bug, não há plano. Crie uma pasta para o bug (`bugs/<id>/`, na pasta de documentação do projeto), com `esperado.md`, `mapa.md` e `saidas/`. O id do bug é o do chamado, ou um nome curto se não houver chamado.

Em ajuste pequeno, o mapa e as saídas ficam numa pasta temporária fora do repositório.

## Formato do teste manual

A IA sugere no máximo cinco por fase; a pessoa pode acrescentar. Cada item tem:

```markdown
### <nome curto>
- Requisito da spec: <trecho ou seção>
- Por que um teste automático não prova isto: <motivo>
- Preparação: <dados, ambiente, configuração>
- Passos: <1, 2, 3, exatos>
- Resultado esperado: <o que se vê, com exemplo concreto>
- Quem executa: IA ou pessoa
- Evidência a guardar: <saída, captura de tela>
- Resultado: passou | falhou | não executado
```

## Formato do mapa

Um arquivo por tarefa.

```markdown
# Mapa: <id e título da tarefa>

## Contratos
Pontos de entrada da tarefa, cada um com a assinatura completa:
nome, parâmetros com tipo, retorno, exceções.
- Já existe: `caminho/arquivo:linha`
- É novo: copiado do plano, marcado como "novo"
Formatos de dados envolvidos, com campos e tipos.

## Testes
- Onde ficam os testes vizinhos: `caminho/`
- Um teste a imitar: `caminho/arquivo`
- Fábricas e dados de apoio disponíveis: `caminho/arquivo`
- Comando para rodar só os testes desta tarefa: `...`
- Comando para rodar os contratos vizinhos: `...`

## Onde mexer
- Arquivos do escopo: `caminho/arquivo`
- Quem chama cada ponto de entrada: `caminho/arquivo:linha`
- Regras do projeto que se aplicam: `caminho/do/arquivo-de-regras`, seção

## Não encontrado
O que a tarefa cita e não foi localizado.
```

O mapa só tem fatos localizáveis. Ponto de entrada novo que o plano não define com assinatura vai para "Não encontrado": o plano é corrigido antes de o autor de testes começar.

## Formato da resposta por papel

**Mapeador.** O caminho do mapa escrito e a lista do que ficou em "Não encontrado".

**Especialista de testes.** Lista de casos de teste por tarefa, cada um com: o que se faz, o que se espera, um exemplo concreto. No fim, as dúvidas de spec.

**Autor de testes.** Os arquivos de teste criados, a saída dos testes falhando e, por teste, a linha da spec que ele cobre. Ou "falta no mapa" e o quê.

**Implementador.** Os arquivos alterados, a saída dos testes da tarefa e dos contratos vizinhos, e o que ele precisou procurar fora do mapa. Ou "teste contradiz a spec", com o teste e o trecho da spec.

**Revisor.** Primeiro o veredito: aprovado ou não. Depois cada achado com classe (comportamento, regra escrita ou opinião), `arquivo:linha` e a evidência. O revisor roda os testes da tarefa e cola a saída.

**Auditor de fase.** Para cada requisito da spec coberto pela fase: atendido, não atendido ou não verificável, com evidência.

**Analista de premissa.** Um dos três vereditos (spec ambígua, teste errado, tarefa grande demais) e a evidência.

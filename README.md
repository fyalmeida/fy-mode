# fy mode

Um jeito de desenvolver com agentes de código em que ninguém confere o próprio trabalho: um agente escreve a prova sem ver a resposta, outro responde sem poder mudar a prova, e um terceiro corrige.

## O jeito de trabalhar

O fy mode nasceu de uma rotina de sete passos. Os quatro primeiros são conversa entre a pessoa e a IA. Os três últimos são onde os agentes trabalham, e é ali que o fy mode entra.

| Passo | O que acontece | Quem decide |
|---|---|---|
| 1. Discutir | A ideia é discutida com a IA até ficar clara (eu particularmente uso a skill de brainstorming do Superpowers) | A pessoa |
| 2. Criar a spec | A IA escreve a especificação do que será feito | A IA propõe |
| 3. Consolidar a spec | A pessoa lê, discute e a spec fecha. O que for decidido entra na spec. A IA sugere os testes manuais e a pessoa corta o que não for necessário | A pessoa |
| 4. Criar o plano | A IA quebra a spec consolidada em tarefas pequenas | A IA propõe, a pessoa aprova |
| 5. Desenvolver | **fy mode:** um agente escreve o código guiado pelos testes | Agentes |
| 6. Testar | **fy mode:** o que testar já está decidido antes de começar (os testes manuais, na consolidação da spec; a lista de testes automáticos, aprovada pela pessoa no início da fase). Neste passo, agentes sem contexto escrevem o código desses testes | A pessoa já aprovou a lista; os agentes escrevem |
| 7. Revisar | **fy mode:** um agente novo revisa cada tarefa e pode sugerir alterações. No fim da fase rodam os testes manuais, e outro agente audita a fase. A pessoa lê o que a revisão apontou e decide se aquilo é mesmo um erro | Agentes sugerem; a pessoa decide |

A revisão não tem a palavra final. O revisor é uma IA e pode falhar: ele pode apontar como erro um comportamento que era exatamente o que você queria. Leia as sugestões e os erros que ele diz ter encontrado e confira, um por um, se aquele comportamento é esperado ou não.

Dentro do fy mode a ordem dos passos 5 e 6 se inverte: **o teste é escrito antes do código**. Na rotina eles aparecem como "desenvolver" e "testar" porque é assim que a pessoa pede; quem garante a ordem certa é o método.

### Onde entra o Superpowers

Eu particularmente uso o [Superpowers](https://github.com/obra/superpowers) junto com o fy mode, cada um numa parte da rotina:

| Passos | Quem conduz | O que faz |
|---|---|---|
| 1 a 4 | Superpowers | A discussão da ideia (skill de brainstorming) e a quebra da spec em tarefas (skill de planos) |
| 5 a 7 | fy mode | Testes, código e revisão, com os papéis separados |

**A discussão acontece duas vezes, de propósito.**

- **Primeira vez, no passo 1.** Antes de existir qualquer texto, o brainstorming do Superpowers faz a IA perguntar uma coisa por vez e levantar alternativas, até a ideia ficar clara. Dessa conversa sai a spec.
- **Segunda vez, no passo 3.** Com a spec escrita, a pessoa lê, revê e discute de novo. Ideia conversada e ideia escrita não são a mesma coisa: no papel aparecem os buracos, as contradições e o que cada um tinha entendido diferente. É também nessa segunda discussão que entram os testes manuais.

Só depois da segunda discussão a spec é considerada fechada e o plano é feito em cima dela.

**Os dois se sobrepõem na execução, e é preciso escolher.** O Superpowers também tem skills para escrever código com subagentes, fazer TDD e revisar. Elas ocupam o mesmo lugar dos passos 5 a 7, com regras diferentes das do fy mode. Usando os dois, deixe escrito no arquivo de instruções do seu projeto (o `CLAUDE.md`, no Claude Code) qual vale em cada parte, por exemplo:

```
Discussão e plano: skills do Superpowers.
Testes, código e revisão: fy mode, e só ele.
```

**Você não precisa usar o Superpowers.** Os passos 1 a 4 podem ser feitos do jeito que você quiser: com outra ferramenta, com o modo de planejamento do próprio Claude Code, ou escrevendo a spec e o plano à mão. O fy mode só precisa que, ao começar, existam uma spec e um plano. De onde eles vieram não importa.

## As ideias

Cada ideia abaixo traz o termo técnico, como ela funciona no fy mode, de onde veio e, por último, uma explicação pra macaco. Nela, cada agente é um macaco que você manda buscar bananas.

### 1. Contexto acumulado do agente

**O que é.** Um agente não tem memória barata. A cada passo (cada leitura de arquivo, cada comando) ele recebe de novo toda a conversa que já acumulou: o pedido, os arquivos lidos, as saídas dos comandos. Isso é a janela de contexto. O custo de um passo cresce com o tamanho do que veio antes, então o passo 80 custa muito mais que o passo 10.

**Como funciona no fy mode.** As tarefas do plano são pequenas (um comportamento por tarefa), e toda rodada usa um agente novo, que começa de contexto vazio, em vez de um agente só que vai acumulando.

**De onde veio.** Da medição dos registros de uso: agentes com mais de 50 passos eram 36% dos agentes e 77% do custo; comparando pelo tamanho, um agente de 80 passos custou 2,5 vezes o de 40 passos, e um de 160 passos custou mais de 6 vezes. A regra de agente novo a cada rodada já era da rotina do autor e também é o padrão do pstack ("fresh subagents by default"). O guia de custo da Anthropic recomenda subagentes para passos volumosos pelo mesmo motivo.

**Explicação pra macaco.** Regra maluca da floresta: a cada viagem, o macaco leva nas costas todas as bananas das viagens anteriores. Na viagem 1 ele carrega 1 banana. Na viagem 10, carrega 10 e cansa. Na viagem 80, carrega 80, e cada viagem custa uma fortuna de esforço.

| Quem busca as 80 bananas | Bananas carregadas no total |
|---|---|
| Um macaco, 80 viagens | 3.240 |
| Dois macacos, 40 viagens cada | 1.640 |

O trabalho é o mesmo e o esforço cai pela metade, porque o segundo macaco começa de costas vazias.

### 2. Pedido com escopo fechado (o mapa)

**O que é.** O pedido que um agente recebe (em inglês, o *brief*) define por onde ele começa. Pedido vago faz o agente explorar o repositório para descobrir onde está o código, e cada passo de exploração entra no contexto acumulado.

**Como funciona no fy mode.** Antes de qualquer agente de teste ou de código, um mapeador, rodando com esforço baixo, escreve o mapa da tarefa num arquivo: os pontos de entrada com assinatura completa, onde ficam os testes vizinhos, o comando para rodar os testes, os arquivos do escopo. Os pedidos seguintes apontam para esse arquivo. O mapa só tem fatos localizáveis, nunca opinião sobre como implementar.

**De onde veio.** Da medição: 76% das ações dos agentes eram procurar e ler arquivo. A forma do pedido vem do pstack, que manda delegar "com escopo específico: caminhos de arquivo, formato dos dados e critério de sucesso" e passar ponteiros para arquivos em vez de colar conteúdo.

**Explicação pra macaco.** Mande um macaco para uma floresta que ele não conhece e ele gasta a maior parte das viagens só descobrindo onde ficam as bananeiras. Antes de qualquer macaco sair, um macaco batedor desenha o mapa: onde estão as bananeiras, por qual trilha se chega, como se confere a banana.

### 3. Separação de papéis e verificação independente

**O que é.** Quem produz um trabalho não é a pessoa certa para julgá-lo, porque julga com as mesmas suposições que usou para produzir. Em engenharia isso se chama verificação independente (ou segregação de funções). Com agentes há um agravante: o agente que escreve o código e o teste na mesma conversa tende a escrever um teste que confirma o código.

**Como funciona no fy mode.** Três agentes novos por tarefa, que não compartilham contexto. O autor de testes escreve a partir da spec e não vê o código. O implementador recebe os testes prontos e não pode alterá-los. O revisor não viu a implementação nascer e não edita código: só relata o que encontrou. No fim da fase, um auditor que não participou de nenhuma tarefa confere tudo contra a spec.

**De onde veio.** Da rotina do autor, que já trabalhava com "agentes sem contexto" antes deste plugin. O Superpowers usa um desenho próximo (um subagente novo por tarefa e revisão por outro agente).

**Explicação pra macaco.** Pergunte ao macaco que colheu se as bananas estão boas e ele vai dizer que estão todas ótimas. Ele não mente: só olha a banana com os olhos de quem a escolheu. Então são três macacos: um define como é a banana boa sem ter visto a colheita, outro colhe e não pode mudar essa definição, e um terceiro, que não viu nada acontecer, confere.

### 4. Teste antes do código (TDD)

**O que é.** Desenvolvimento guiado por testes, ou TDD (*test-driven development*): primeiro se escreve o teste e se vê ele falhar (vermelho), depois se escreve o código que o faz passar (verde). Ver o teste falhar antes é o que prova que ele testa alguma coisa.

**Como funciona no fy mode.** O teste é escrito a partir da spec, antes do código, e o coordenador roda e confere que ele falha pelo motivo certo. Teste que falha não é alterado para passar: corrige-se o código. O teste só muda quando a spec ou a pessoa muda o comportamento esperado.

**De onde veio.** O TDD é uma prática clássica de engenharia de software, e o Superpowers tem uma skill dedicada a ela. A parte própria do fy mode é juntar o TDD com a separação de papéis: quem escreve o teste não é quem escreve o código.

**Explicação pra macaco.** Se a definição de "banana boa" for escrita depois da colheita, ela vai descrever as bananas que já estão no cesto. Combine antes como é a banana boa.

### 5. Esforço de raciocínio por papel

**O que é.** Os modelos atuais têm um controle chamado esforço de raciocínio (*reasoning effort*): quanto o modelo pensa antes de responder e de agir. Esforço maior gasta mais tokens. Existe também a opção de trocar para um modelo menor e mais barato, mas isso baixa o teto de capacidade.

**Como funciona no fy mode.** Um modelo só, o mais forte de código do fornecedor, em todos os papéis. O que varia é o esforço: baixo para mapear, médio para revisar, alto para escrever teste, implementar e auditar. Correção depois de teste vermelho sobe um nível.

**De onde veio.** De três fontes. A orientação pública da Anthropic, que recomenda ajustar o esforço antes de trocar de modelo e indica esforço baixo para subagentes de tarefas simples. O pstack, que usa o mesmo modelo em todos os papéis variando o nível. E a evidência de que trocar o revisor por um modelo mais barato custa em bugs não encontrados, que é o motivo de o fy mode não trocar de modelo: num [teste público da CodeRabbit](https://coderabbit.ai/blog/sonnet-5-5-model-review) com 13 casos difíceis de bug conhecido, o modelo intermediário achou 6 e o modelo forte achou de 8 a 10 (o próprio post avisa que 13 casos mostram direção, não decidem), e nos registros do autor as revisões do modelo intermediário apontaram problema em 22% dos casos, contra 48% do modelo forte nas mesmas sessões. Os níveis por papel são ponto de partida e ainda não foram medidos depois de adotados.

**Explicação pra macaco.** Achar a bananeira não exige a mesma concentração que escolher as bananas maduras. Pagar concentração máxima para todos é desperdício, e trocar por um macaco mais fraco para economizar faz banana ruim passar.

### 6. Limite de tentativas e teste da premissa

**O que é.** Quando duas correções seguidas falham no mesmo ponto, o mais provável é que as duas partam de uma suposição errada (a premissa). Insistir numa terceira correção com a mesma suposição repete o erro. Em sistemas isso se parece com um disjuntor (*circuit breaker*): depois de falhas repetidas, para-se de tentar e investiga-se a causa.

**Como funciona no fy mode.** O mesmo teste continua vermelho depois de duas correções: a terceira não acontece. Um agente novo, o analista de premissa, recebe a spec, o teste e a saída, e devolve um de três vereditos: a spec está ambígua (a pessoa decide), o teste está errado (autor de testes novo) ou a tarefa é grande demais (divide-se no plano). Pressa não suspende o freio.

**De onde veio.** Do princípio "Attack the Premise" do pstack: quando duas ou mais correções que compartilham uma premissa falham, escreva a premissa e teste-a antes de tentar outra correção. O limite de duas rodadas já era da rotina do autor; faltava dizer o que fazer ao atingi-lo.

**Explicação pra macaco.** Se dois macacos foram à mesma árvore e voltaram com a fruta errada, o problema provavelmente não é o macaco. Talvez a árvore não seja uma bananeira, ou a descrição da banana esteja errada. Não mande o terceiro: mande alguém conferir a árvore.

### 7. Triagem de achados da revisão

**O que é.** O que um revisor aponta é uma suspeita, não um fato. Ele pode ter achado uma falha real, ou pode ter suposto uma falha que não existe. Triagem é o passo que separa uma coisa da outra antes de alguém mexer no código.

**Como funciona no fy mode.** O revisor não edita nada: relata cada achado com arquivo, linha e evidência, e classifica. Cada classe tem a sua prova:

| Classe | Como se confirma | Se confirmar |
|---|---|---|
| Comportamento (o código faz diferente da spec) | Um autor de testes novo escreve o teste a partir da spec. Se o teste falha, a falha é real. Se passa, o achado não procede | Implementador novo corrige |
| Regra escrita (viola uma regra do projeto) | O coordenador confere que a regra existe no arquivo citado e que a violação está na linha citada | Vira item do plano; implementador novo corrige |
| Opinião (sem spec nem regra que sustente) | Não abre rodada | Fica anotada para o auditor da fase |

Nenhum achado é passado como recado de um agente para outro: ele entra num arquivo, e o próximo agente lê o arquivo.

**A sua parte.** Essas provas pegam o revisor que supôs errado sobre o código. Elas não pegam o caso em que o revisor leu a spec de um jeito e você queria outro. Por isso:

- quando confirmar um achado depende de saber se o comportamento é o esperado e a spec não responde ao pé da letra, o método para e pergunta a você antes de qualquer correção;
- no relatório de cada fase vêm todos os achados da revisão, com a classe, o resultado da prova e o que foi feito. Leia a lista. Se algo foi tratado como erro e era o comportamento que você queria, diga: a spec é corrigida e o teste muda junto.

**De onde veio.** Da rotina do autor ("o que o revisor encontra não vai como recado para ninguém") e da orientação dele de que o revisor apenas sugere e a falha precisa ser verificada. O pstack tem regra parecida para comentários de revisão automática: julgar cada um pelo mérito. A classe "regra escrita" foi criada aqui, porque esse tipo de achado não vira teste e antes não tinha caminho.

**Explicação pra macaco.** O macaco conferente diz "acho que esta banana está estragada". Ninguém joga a banana fora por isso, nem manda outro macaco colher de novo. Primeiro abre-se a banana. E a reclamação vai para o caderno, não de boca em boca, porque recado passado de macaco em macaco chega distorcido.

### 8. Teste de aceitação manual

**O que é.** Teste de aceitação é a verificação de que a entrega faz o que a pessoa queria, feita por onde o usuário usa (a tela, a requisição, o comando). O teste automático prova que o código faz o que a spec diz. Ele não prova que a spec estava certa, nem que as peças funcionam juntas no ambiente de verdade.

**Como funciona no fy mode.** Na consolidação da spec, a IA sugere testes manuais e a pessoa corta o que não for necessário. A IA sugere no máximo cinco por fase, e cada um explica por que um teste automático não prova aquilo; o que dá para automatizar vira teste automático. A pessoa pode acrescentar os que quiser. Eles rodam no fim da fase: a IA executa o que for requisição, comando ou navegador automatizado, e a pessoa executa o que exige olho humano. Se um falhar, primeiro um agente escreve o teste automático que reproduz a falha, e só depois outro corrige.

**De onde veio.** A ideia de discutir os testes manuais na consolidação da spec é do autor. Três agentes especialistas (qualidade, custo e advogado do diabo) avaliaram a proposta e recomendaram adotar com o limite de cinco sugestões e a execução no fim da fase. O passo de provar na superfície real vem do princípio "Prove It Works" do pstack: verificar contra a coisa real, não contra um substituto.

**Explicação pra macaco.** A banana pode passar em todas as conferências (cor certa, tamanho certo, sem mancha) e ainda assim estar sem gosto. Todos os macacos conferiram a mesma lista; se a lista estava errada, ninguém percebe. Só quem come descobre. Prove a banana antes de mandar para o mercado.

## Como funciona por dentro

```
spec + plano
    │
    ├─ painel de testes ──► lista de testes + testes manuais ──► a pessoa aprova (uma vez por fase)
    │
    └─ por tarefa:
         mapeador ──► autor de testes ──► implementador ──► revisor ──► commit
                      (não vê o código)   (não muda o teste)  (agente novo)
    │
    └─ fim da fase: testes manuais onde o usuário usa ──► auditor ──► relatório
```

Há três roteiros, para a tarefa pequena não pagar o processo da grande:

| Roteiro | Quando | Agentes |
|---|---|---|
| Funcionalidade | Tem spec e plano | Painel, mapeador, autor de testes, implementador, revisor, auditor |
| Bug | Algo funcionava e parou | Reproduzir primeiro; mapeador, autor de testes, implementador, revisor |
| Ajuste pequeno | Um arquivo, sem regra de negócio nova | Mapeador, autor de testes, implementador, revisor |

Os papéis continuam separados até no ajuste pequeno. É a opção mais cara, e é de propósito: um agente que escreve o teste e o código leva o mesmo engano para os dois, e o engano só aparece depois, como rodada de correção. O que o ajuste pequeno dispensa é o painel e o auditor.

O método para e pergunta à pessoa só em: regra de negócio, texto que o usuário vê, mudança em fluxo existente e push.

O método completo está em [`skills/fy-mode/SKILL.md`](skills/fy-mode/SKILL.md).

## De onde vieram essas escolhas

Antes de criar este plugin, o autor trabalhou dois meses num projeto real com a versão antiga do método. O Claude Code guarda no computador um diário de tudo o que cada agente fez. Um script leu esse diário (2.371 agentes) e contou onde o gasto estava. É o mesmo script que vem neste plugin, para você medir o seu projeto.

Duas palavras para ler a tabela:

- **Passo** é cada ação de um agente: abrir um arquivo, rodar um comando, editar um trecho.
- **Custo** é a soma dos tokens gastos, com peso diferente para cada tipo, porque eles têm preços diferentes. Não é um valor em dinheiro: é uma nota que serve para comparar uma coisa com outra.

| O que foi medido | Resultado | O que quer dizer |
|---|---|---|
| Quanto do gasto total foi dos agentes | 74% | De cada 100 gastos, 74 foram dos agentes e 26 da conversa da pessoa com a IA. O lugar para economizar é nos agentes |
| O que os agentes passavam o tempo fazendo | 76% procurando e lendo arquivo | De cada 100 ações, 76 eram procurar ou abrir arquivo, 7 eram rodar teste e 5 eram escrever código. Eles procuravam muito mais do que produziam |
| Quanto custaram os agentes de trabalho longo | 36% dos agentes, 77% do custo | Um em cada três agentes passou de 50 passos, e esse terço gastou três quartos de tudo. O agente caro é o que trabalha por muito tempo seguido. É o macaco da viagem 80 |
| Quanto custa criar um agente novo | 6% | Todo agente novo começa lendo a spec e o plano. Essa leitura inicial foi só 6 de cada 100. Criar agente novo é barato: trocar de macaco custa pouco |
| Quanto custaram o painel de testes e o auditor | cerca de 5% | Os agentes que desenham os testes e conferem a fase quase não pesam. Não valia cortar ali |
| Quanto foi gasto refazendo trabalho | cerca de 13% | De cada 100, 13 foram em rodadas de correção |

Cada número virou uma decisão do método:

- Os agentes procuravam demais → **o mapa antes do trabalho**.
- O agente longo é o caro, e criar agente novo é barato → **tarefas pequenas e um agente novo a cada rodada**.
- Painel e auditor pesam pouco → **foram mantidos**.
- 13% em retrabalho → **o freio de rodadas e a triagem dos achados**.

**O que ainda não foi medido:** o resultado depois das melhorias. Os números acima são o "antes". Os níveis de esforço por papel são um ponto de partida, sustentado pela orientação pública da Anthropic e por um teste público de revisão de código, não por medição própria.

## Instalar

No Claude Code:

```
/plugin marketplace add fyalmeida/fy-mode
/plugin install fy-mode@fy-mode
```

Depois, numa conversa: `/fy-mode:fy-mode`, ou só peça para trabalhar em fy mode.

## Medir o seu projeto

```
python3 scripts/medir.py /caminho/do/projeto
python3 scripts/medir.py /caminho/do/projeto --desde 2026-11-01
```

O script só lê os registros locais do Claude Code. Rode antes de adotar o método e depois de uma fase inteira, e compare o custo por tarefa concluída e o número de rodadas de correção.

## Outras ferramentas

O método fala em níveis (modelo forte; esforço baixo, médio e alto), não em marcas. A tradução por fornecedor está em [`skills/fy-mode/referencias/niveis.md`](skills/fy-mode/referencias/niveis.md).

- **Claude Code:** medido. Os agentes em `agents/` já trazem modelo e esforço.
- **Outras (Codex, Cursor, Gemini CLI):** não testado. Clone o repositório inteiro e aponte a ferramenta para `skills/fy-mode`. Sem os agentes prontos, a skill manda usar um agente genérico que lê o arquivo do papel em `agents/`. Se testar, mande a tradução e a medição por pull request.

## Licença

MIT. Veja [`LICENSE`](LICENSE).

## Créditos

- O roteiro por tipo de tarefa, o pedido com escopo fechado, "atacar a premissa" e a prova na superfície real vêm do [pstack](https://github.com/cursor/plugins), de Lauren Tan.
- A disciplina de teste antes do código e de revisão por agente novo deve muito ao [Superpowers](https://github.com/obra/superpowers), de Jesse Vincent.

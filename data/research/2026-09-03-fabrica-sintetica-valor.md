# Fábrica de casos sintéticos: o que construímos, para que serve e o que fazer

Data: 2026-09-03. Autor: sessão de boot com o owner. Status: memorando de
decisão (gate de valor exigido pelo HANDOFF, item 1). Nenhuma skill, fixture
ou dado de pesquisa foi alterado por este documento.

## Resumo pro CEO

Construímos, em dois dias, uma máquina que transforma uma ficha oculta de um
caso jurídico em 17 documentos falsos mas coerentes, com problemas plantados
de propósito, e que sabe conferir se uma skill encontrou esses problemas. A
máquina funciona e já pagou uma parte do investimento: achou um erro real na
skill de análise jurídica, corrigido e publicado. O que ela **não** é: um
gerador genérico de casos em volume para testar o Valter ou qualquer outro
sistema. Cada família de caso exigiu uma ficha nova e um renderizador próprio,
e ela só foi ligada a uma única skill. O fio se perdeu quando o objetivo
mudou, sem decisão explícita, de "fábrica para vários consumidores" para
"fazer uma skill passar 36 de 36". A recomendação é congelar o que existe como
régua de regressão, usar os casos já gerados como material de uso humano hoje,
e não construir mais famílias até existir um segundo consumidor com pedido
concreto.

## Etapa 1 — A ideia, em uma figura

```
  AUTORIDADE (oculta)                        VISÃO CEGA (o que a skill vê)
  ┌──────────────────────┐                   ┌──────────────────────────┐
  │ world_spec.json      │   renderer        │ task.md (pedido)         │
  │  fatos F001..F0nn    │ ───────────────►  │ documents/ 01..17 .md    │
  │  documentos D010..   │                   │  (sem IDs, sem gabarito) │
  │  mundos W-A/W-B/W-C  │                   └───────────┬──────────────┘
  │  rubrica R001..R00n  │                               │ executor
  │  observações esperadas│                              ▼
  └──────────┬───────────┘                   ┌──────────────────────────┐
             │ compilador                    │ memorando (≤900 palavras)│
             ▼                               └───────────┬──────────────┘
  ┌──────────────────────┐                               │
  │ invariantes por mundo│ ──────────────► JUIZ (LLM) ───┘ → PASS/FAIL
  │  (7 no P0, 8 no P1)  │      hashes, proveniência, recibos
  └──────────────────────┘
```

Regra de negócio: quem gera o caso sabe a resposta; quem resolve o caso não
vê a resposta; um terceiro confere se a resposta apareceu. É o mesmo desenho
que a Harvey descreve para avaliar e treinar agentes sem dados de cliente.

## Etapa 2 — De onde veio

Em 31/08 o dossiê sobre a Harvey concluiu que o ativo estratégico dela não é o
benchmark publicado, e sim a capacidade repetível de converter conhecimento
de especialista em ambientes com verdade oculta (especificação → documentos →
proveniência → gabarito → rubrica). A Harvey usa três receitas: rubrica
primeiro (diligence), especificação primeiro (firm knowledge) e distribuição
do produto primeiro (perguntas sintéticas sobre corpus real, com oráculo). Nós
implementamos uma combinação das duas primeiras. A terceira, que é a que
serviria ao Valter, não foi tocada.

O dossiê rejeitou explicitamente: portar o Harvey LAB, construir um
equivalente amplo, e escrever à mão um assunto com três tarefas. Adotou a
menor investigação capaz de provar a cadeia: um único assunto, três mundos.

## Etapa 3 — O que é um "mundo", concretamente

Assunto `M-101` do lote P0: uma fornecedora fictícia de refrigeração cobra em
cumprimento de sentença uma devedora fictícia; principal de R$ 84.000,00,
atualizado R$ 94.780,00. Os 17 documentos são curtos, em Markdown, e cobrem a
cadeia inteira: contrato, nota fiscal, termo de entrega, petição inicial,
citação, sentença, trânsito, petição de cumprimento, memória de cálculo,
despacho de intimação, diário, certidão de publicação, e-mail da executada,
registro bancário, extrato de andamentos, nota normativa e calendário forense.

Os três mundos do mesmo assunto diferem em um único documento:

| Mundo | O que muda | O que a skill precisa perceber |
|---|---|---|
| W-A controle | nada | pagamento alegado e comprovado convergem; não há decisão de extinção |
| W-B prova ausente | `14-registro-bancario.md` vira "busca não localizou comprovante" | alegação não vira pagamento confirmado; busca negativa não prova inexistência |
| W-C conflito cronológico | `12-certidao-publicacao.md` muda a data de 04/03 para 02/03 | duas datas expostas, nenhuma escolhida em silêncio; efeito na tempestividade |

O pedido é sempre o mesmo: memorando de até 900 palavras com Cronologia,
Estado da prova, Análise e Próximos passos, usando só a nota normativa e sem
inventar fato, prazo, feriado ou cálculo. A rubrica comum tem cinco critérios
(cronologia citada, distinção alegação/prova/reconhecimento judicial, uso
limitado dos artigos, ausência de extinção não inferida, nada inventado); as
observações específicas de cada mundo completam os sete invariantes.

Verificação: 12 assuntos × 3 mundos = 36 mundos; 36 × 17 = 612 documentos;
36 × 7 = 252 invariantes no P0; 36 × 8 = 288 no P1. Os relatórios registram
exatamente esses totais. ✓

## Etapa 4 — Os dois lotes

| | P0 | P1 |
|---|---|---|
| Família | cumprimento definitivo de sentença por quantia certa | procedimento comum, fase de conhecimento, disputa contratual |
| Assuntos × mundos | 12 × 3 = 36 | 12 × 3 = 36 |
| Documentos | 612 (17 por mundo) | 612 (17 por mundo) |
| Motivos estruturais | petição→decisão→certidão; petição→decisão→petição; decisão→ofício→certidão; contrato→petição→decisão | defesa × revelia; perfil probatório; desfecho; tensão temporal multi-ano |
| Cronologia | deslocamentos semanais (março a agosto de 2026), feriados forenses recusados nas janelas | anos reais com feriados, espelhando p50 de 5,5 anos dos autos |
| Base empírica | 259 casos do fs.brain (topologia documental; confiança alta para tipos de documento, baixa para histórias integrais) | 39 autos de procedimento comum da carteira (p50 406 movimentos; contestação 59%; sentença 36%) |
| Revisão cega do lote | Sonnet 5 + Opus 5 via API, 3 rodadas até CONSTRUIR; 8 assuntos restantes por pares Codex | Sonnet 5 + Opus 5, 4 rodadas, 13 defeitos corrigidos; 8 assuntos restantes por pares Kimi |
| Aprovação | 36/36 mundos, 16/16 críticas e 8/8 relevantes por revisor | 36/36 mundos, idem |
| Código | `build_worlds.py` 758 linhas, `build_batch.py` 586, revisores 814 | `build_worlds.py` 859, `build_batch.py` 969, adjudicadores ~1.850 |

Total: cerca de 6.260 linhas de Python só com biblioteca padrão (nenhuma
dependência externa; a API da Anthropic é chamada com `urllib`), 13 MB e
2.132 arquivos de artefatos, tudo regenerável de forma determinística e
conferido por hash.

O que é genérico e o que é preso ao domínio, segundo o inventário do código:

- **Genérico, reaproveitável em qualquer matéria:** o motor de mutação (um
  mundo controle e mutações que trocam um único documento), a proveniência
  fato → arquivo:linha, o gate empírico (o build recusa se as estatísticas
  congeladas divergirem do relatório de origem), o calendário forense em dias
  úteis com feriados nacionais, o protocolo de revisão cega com adjudicação e
  hashes, e a materialização de cenários pela régua.
- **Preso ao domínio:** cada tipo de documento é uma função de renderização
  com texto jurídico fixo (cláusulas, artigos do CPC, redação de despacho).
  Uma família nova exige escrever essas funções de novo e uma ficha nova,
  como aconteceu do P0 para o P1 (859 linhas novas de renderer). Não existe
  "gerar outra família apertando um botão".
- **Ligado a um único consumidor:** o executor recebe só a skill de análise
  jurídica e suas referências; o roteamento automático do plugin (a escolha
  da skill a partir do pedido em linguagem natural) não é exercitado.

## Etapa 5 — O que a régua encontrou

**P0 (31/08).** Sem a skill, o executor omitiu o art. 524 em `M-101/W-B`.
Com a skill, o lote integral expôs a mesma omissão em `M-105/W-A`. A skill
ganhou uma regra geral ("todo dispositivo material da fonte autorizada é
aplicado ou declarado não incidente") e fechou 36/36 e 252/252. Essa regra foi
publicada na v0.6.2. **Este é o único efeito da fábrica no produto até hoje.**

**P1 (01/09).** O canário passou, mas o lote parou no invariante "ligar a
alegação da inicial ao registro que a corrobora sem promovê-la a fato
provado". Cinco reexecuções do mesmo cenário deram 3 PASS e 2 FAIL: a skill
oscila sob entrada congelada. Duas correções textuais passaram no cenário
isolado e falharam no assunto seguinte. A terceira, estrutural (quadro
obrigatório de relações probatórias no mapa jurídico), passou 36/36 e
288/288 na P1. A regressão na P0 foi interrompida por você em 8/36. A mudança
foi revertida; as skills publicadas continuam iguais à v0.6.2.

Leitura honesta: a P1 provou que a régua discrimina (detectou instabilidade
real) e que uma mudança estrutural estabiliza nesta família. Não provou ganho
para um advogado, nem ausência de regressão, nem superioridade sobre uma
solução menor.

## Etapa 6 — O que custou

| Etapa | Externo (US$) | Franquia Codex (tokens de entrada, executores + juízes) |
|---|---|---|
| Revisões cegas do seed P0 (inclui rodada inválida) | 4,47 (+ até 16,00 sem recibo) | — |
| Canário do lote P0 | 3,37 | — |
| Execução integral P0 com a skill | 0 | 4,15 M + 0,67 M (3,4 M em cache) |
| Canário do lote P1 (4 rodadas) | 5,63 | — |
| P1 primária + painel de estabilidade | 0 | 0,91 M + 0,15 M |
| P1 corretiva (dois candidatos textuais) | 0 | 3,02 M + 0,50 M |
| P1 estrutural (45 execuções, 46 julgamentos) | 0 | 5,52 M + 0,90 M |
| P0 regressão pausada (8 cenários) | 0 | 0,81 M + 0,15 M |
| **Total** | **≈ 13,50 comprovados** | **≈ 14,4 M executores + 2,4 M juízes** |

Mais o trabalho empírico privado (265 PDFs baixados, extrator, cross-validação
com o fs.brain) e dois dias inteiros de sessão. "Custo externo zero" nas
linhas Codex significa franquia da assinatura, não gratuidade. A prova disso
chegou hoje: em 03/09 a franquia do Codex está **esgotada até 07/09 às
07:21**; a consulta cega ao conselho falhou por esse motivo, e qualquer nova
rodada com o backend Codex (inclusive a regressão P0 pendente) está bloqueada
até lá.

## Etapa 7 — Onde o fio se perdeu

O objetivo declarado em 31/08 era uma máquina para gerar casos em volume e
testar vários consumidores (Valter, skills). O que aconteceu na prática:

1. A fábrica foi ligada a **uma** skill (`analise-juridica-civel`) com **um**
   tipo de tarefa (memorando de análise documental).
2. Assim que a régua achou instabilidade, o esforço migrou para corrigir a
   skill até passar: três candidatos em um dia e cerca de 10 milhões de
   tokens de franquia só na P1, sem que nada disso chegasse ao produto.
3. A pergunta "para quem serve?" foi substituída por "passa 36/36?". A régua
   virou o produto.
4. O Valter nunca entrou: mundos documentais fictícios não contêm
   jurisprudência real, então não testam busca, citação nem grounding.

Nada disso foi erro de execução; foi ausência de um gate de valor entre
"a máquina funciona" e "vamos usá-la para X". Este memorando é esse gate.

Saldo frio, na formulação do conselho: dois dias, cerca de 15 milhões de
tokens de franquia e US$ 13,50, para **um achado promovido ao produto** (a
regra do art. 524) e **um diagnóstico de instabilidade** (a ligação
probatória oscila). O problema não é a fábrica; é o custo marginal por
decisão que ela muda.

Há uma contradição que precisa ser dita com clareza: a suíte P1 é
**vermelha sobre a skill publicada**. Em cinco execuções do mesmo cenário
`M-202/W-A` com a v0.6.4, três passaram e duas falharam no invariante 7. A
única versão da skill que passou 36/36 é o candidato estrutural, que foi
revertido. "Congelar como régua de regressão" sem decidir o que fazer com
esse invariante é arquivar disfarçadamente.

## Etapa 8 — Para que serve, uso por uso

| Uso | Serve hoje? | O que falta | Custo | Critério falsificável |
|---|---|---|---|---|
| **1. Regressão da skill de análise jurídica** | **Sim, com ressalva.** 72 cenários congelados por hash; a P1 está vermelha na v0.6.4 (invariante 7) | decidir o destino do invariante 7 (defeito conhecido ou promoção); painel de 3 amostras nos 9 cenários críticos como gate barato; suíte completa só em release, com teto de tokens | ~5 M tokens de franquia por rodada completa com painel; hoje bloqueado até 07/09 | uma rodada reprova uma mudança que um humano confirmaria como regressão |
| **2. Julgamento humano de utilidade, a custo zero** (você lê lado a lado o memorando da skill publicada e o do candidato estrutural para `M-202/W-A`, ambos congelados) | **Sim, hoje.** Os transcripts existem em `data/evals/` | 20 minutos seus | zero | você diz qual memorando preferiria receber e por quê; isso decide se o quadro probatório vira produto ou defeito conhecido |
| 3. Regressão das outras skills do plugin (`analise-documental`, `novo-caso`, `deliberacao-juridica`) | Parcial: mundos sim, tarefas e rubricas não | um adaptador por skill (tarefa + invariantes derivados do mesmo spec) | 1 sessão por skill | cada adaptador acha ao menos um defeito real na primeira rodada |
| 3a. Exercitar o fluxo completo do plugin (intake → análise → deliberação) sobre um mundo cego | Serve para treino do fluxo e demonstração, **não como prova de valor**: você conhece o desenho das mutações e os revisores documentaram artificialidades (custas em razão constante, contestação sempre no 15º dia útil, ramos de atividade fantasia) | — | 1 h | fluxo roda sem atrito; não mede utilidade |
| 3b. Recibo de uso humano do produto | Sim, mas **não com os mundos**: usar um caso que você não desenhou (o caso sintético do dogfood da deliberação, ou um caso real sob o protocolo de privacidade hoje estacionado) | protocolo de privacidade para autos reais | 1 tarde | veredito seu registrado no ROADMAP |
| 3c. Protocolo de QA cego (canário multi-modelo a ~US$ 1,40 por rodada, prompt congelado por hash, adjudicação mecânica, nota de correção) | **Sim, hoje**, para qualquer artefato normativo do repo (skills, referências), não só mundos | escolher o artefato e a rubrica | ~US$ 1,50 por rodada | acha ao menos um defeito real por rodada |
| 3d. Medição de instabilidade (3 PASS / 2 FAIL sob entradas congeladas; dois juízes divergem sobre o mesmo transcript) | Já pago; vira regra de desenho | — | zero | toda avaliação futura, inclusive a do Valter, usa painéis, nunca amostra única |
| 4. Testar o Valter (busca e citação de jurisprudência) | **Não, como está** | outra construção: perguntas sintéticas sobre o corpus real + oráculo + rubrica de citação e abstenção (Receita C). O Valter já tem harness, holdouts e qrels próprios; o que transfere daqui é o método de QA cego e adjudicação | 1 a 2 sessões no repo do Valter | acha um defeito de grounding que o Valter não conhecia |
| 5. Testar plugin + Silo de ponta a ponta (mundo + pesquisa) | Não | mundos com "precedente esperado" e conector autenticado no job | alto | idem 4, no fluxo do advogado |
| 6. Treinamento ou fine-tuning | Não | milhares de mundos diversos, modelo alvo, infraestrutura | muito alto | fora de escopo do repo |
| 7. Benchmark público / Laboratório (SEN-1746) | Os mundos, não; **o método, talvez**: a cadeia de custódia (ficha oculta → hashes → recibos → adjudicação → nota de correção) é um caso raro de avaliação auditável de ponta a ponta em português, publicável sem publicar um único mundo | sua autorização; licença; texto de método | médio | terceiro reproduz o protocolo e obtém o mesmo placar |
| 8. Demonstração, onboarding e ensino | Sim, com baixo esforço | escolher um mundo e escrever o roteiro | horas | usuário externo entende o fluxo sem dado real |
| 9. Red-team de alucinação | Já embutido no uso 1 | — | — | W-B e "nada inventado" já reprovam invenção |

Leitura: os usos 2, 3c, 3d, 8 e 9 valem hoje sem construir nada e sem
franquia. O uso 1 vale, mas exige uma decisão sobre o invariante 7 e um
orçamento honesto por rodada. O uso 3 é a única extensão barata que aproveita
o gerador como está. O uso 4, que era a motivação original, exige outra
receita, que nasce no Valter, não aqui.

## Etapa 9 — Opções

| Opção | O que é | Resultado provável | Custo | Critério de sucesso | Stop rule |
|---|---|---|---|---|---|
| **A. Congelar com decisão** (recomendada) | P0 e P1 viram régua de regressão com teto e painel; o invariante 7 é registrado como **defeito conhecido da v0.6.4** (omissão da ligação explícita entre alegação e documento corroborante; nunca invenção nem promoção indevida a fato provado) até você julgar a utilidade do quadro probatório lendo os dois memorandos congelados; nenhuma família nova | decisão informada por leitura humana em 20 minutos, sem tokens; régua protege a skill em release | 20 min seus + 30 min de documentação | você prefere um dos dois memorandos por razão que consiga explicar | se os dois memorandos parecerem equivalentes, o invariante 7 vira diagnóstico e a P0 do candidato não se conclui |
| B. Concluir a regressão P0 do candidato estrutural | 28 cenários restantes, depois decidir promoção | provável 28/28 (o candidato é conservador) | ~3 M tokens de franquia, 2 a 3 h; **inexecutável antes de 07/09** (franquia Codex esgotada; trocar o backend por Claude custaria dólares e quebraria a comparabilidade com o baseline congelado) | zero regressão e um advogado confirma que o quadro probatório ajuda | reprovar 1 cenário por causa confirmada |
| C. Pivotar para o Valter (Receita C) | protótipo de 50 perguntas sintéticas sobre decisões reais + oráculo + rubrica de citação, no repo do Valter | primeiro dataset de grounding com verdade controlada | 1 a 2 sessões | acha um defeito real de citação ou abstenção | duas sessões sem defeito novo |
| D. Generalizar o gerador (P2, P3, novas famílias) | renderizador genérico por tipo de documento; famílias de execução extrajudicial, tutela etc. | mais mundos sem consumidor novo | 2+ sessões por família | um segundo consumidor pede e usa | nenhum pedido concreto em 30 dias |
| E. Arquivar | mover para `data/research/archive`, manter fixtures desligadas | evidência preservada, zero manutenção | 30 min | — | — |

**Recomendação: A agora; B só se a sua leitura preferir o memorando do
candidato estrutural, e só depois de 07/09; C quando o Valter tiver uma
pergunta de grounding que o harness dele não responde; D e E não.** A e C
não competem: A cabe hoje neste repo; C é trabalho de outro workspace.

Menor próximo passo que muda uma decisão: você ler, lado a lado, o memorando
que a skill publicada produziu para `M-202/W-A` (execução que reprovou o
invariante 7, em `data/evals/2026-09-01-codex-skill-world-spec-p1-full-v1/`)
e o que o candidato estrutural produziu para o mesmo mundo (em
`.../p1-critical-structural-v1/`), e dizer qual você preferiria receber de um
associado. Vinte minutos, zero tokens. Se preferir o estrutural, a P0
restante (28 cenários, após 07/09) decide a promoção. Se forem equivalentes,
o invariante 7 fica como diagnóstico e a fábrica se encerra como régua.

O recibo de uso humano do produto, que continua sendo a maior lacuna do
plugin, não sai dos mundos sintéticos: sai de um caso que você não desenhou.

## Etapa 10 — Conselho

Gatilho: pedido do owner e espaço de solução amplo. Registro no ledger
`~/.gstack/projects/sensdiego-codigo-aberto/council.jsonl` em 2026-09-03.

### SOL (contraditor)

Consulta cega **não realizada**: o Codex retornou "usage limit" com retorno
previsto para 07/09 às 07:21. Achado procedural relevante: antes de estourar
o limite, o Sol pesquisou por conta própria `~/.codex/memories/MEMORY.md` e
encontrou registros de sessões Codex anteriores sobre este mesmo tema. O
guard do agente `conselho-sol` não bloqueia esse caminho; até corrigir, a
consulta cega ao Sol não é comprovadamente cega.

### K3 (alavancador) — verbatim

## (1) Onde a posição quebra — com evidência

**a) "Congelar como regressão" esconde uma contradição não resolvida: a suíte congelada nasce vermelha.** O `ADJUDICATION.md` registra que o delta de produto foi **revertido a `v0.6.4`** ("o delta final dos arquivos de produto foi devolvido ao estado de v0.6.4"), e que essa versão é exatamente a que **oscila no invariante 7**: painel de 5 amostras de `M-202/W-A` com entradas congeladas terminou **3 PASS / 2 FAIL**, e os candidatos textuais falharam em M-203 e M-204. A única skill que passou 36/36 (candidato estrutural, SHA `13a42a0a…`) **não é a skill publicada** — e a regressão P0 dela morreu em 8/36. Ou seja: "congelar P0 e P1 como regressão da skill" significa congelar uma régua que o produto atual reprova. A posição trata isso como detalhe operacional; é a decisão central. Uma suíte de regressão vermelha desde o dia um vira ruído ignorado ou gate que bloqueia tudo — as duas coisas já aconteceram neste projeto (a regressão interrompida).

**b) O instrumento de medição é mais barulhento do que a posição admite, e isso infla o custo do "rodar só quando a skill mudar".** Dois fatos do `ADJUDICATION.md`: (i) o rejulgamento de `M-207/W-C` — **mesmo transcript, dois juízos divergentes** — mostra que o juiz é fonte de variância, não só o executor; (ii) a rodada estrutural sozinha consumiu **5.517.529 tokens de entrada de executor + 898.760 de juiz**, e a corretiva mais 3.023.003 + 504.370. A posição cita "5,5 milhões" como custo do desvio; o total comportamental P1 é ~**10 milhões de tokens de franquia**. Com variância de ~40% num invariante sob entradas congeladas, qualquer regressão séria exige painéis de N amostras por cenário — o "teto de consumo" proposto não fecha a conta. A insegurança sobre franquia não é periférica: é o argumento que pode derrubar o próprio congelamento como prática recorrente.

**c) O dogfood humano tem um defeito estrutural que a posição não viu: Diego não pode ser consumidor cego de mundos cujo gabarito ele autorou.** A propriedade que faz o método valer — revisão cega — desaparece no dogfood pelo próprio construtor. E a artificialidade não é hipótese: os canários documentaram-na com evidência (custas em razão constante ~1,87%, contestação sempre no 15º dia útil, calendário cobrindo exatamente a janela da mutação, ramos fantasia tipo "banco implantando software" — flags do opus-5 no README do P1). O "recibo de uso humano" provaria que Diego consegue usar a skill num mundo que ele mesmo desenhou para ser passável — evidência fraca de valor real.

**d) O saldo líquido de produto é menor que "já útil hoje".** O defeito durável corrigido no produto é um: a omissão do art. 524 (P0). Toda a saída P1 — três candidatos, 27 pares executor–juiz na corretiva, 45 execuções na estrutural — está **revertida** e existe só como evidência. A posição deveria dizer isso com frieza: dois dias, ~10M tokens, um achado promovido.

## (2) O que fortaleceria a recomendação

- Resolver a contradição (a) explicitamente: ou promover o candidato estrutural após completar a P0 (28 cenários restantes, custo estimável pelos recibos dos 8 já corridos), ou registrar o invariante 7 como *known issue* aceito em v0.6.4 com justificativa. "Congelar" sem escolher é adiar a decisão que a suíte existe para forçar.
- Quantificar custo por achado durável (~10M tokens franquia + US$10 por 1 correção promovida + 1 diagnóstico de instabilidade) — é a régua honesta para decidir se a rodada seguinte se paga.
- Antes do dogfood, extrair valor de custo zero dos artefatos congelados: a divergência de juízes em M-207/W-C e o painel 3/2 já estão pagos e calibram o desenho de qualquer eval futura (painéis, não execuções únicas).

## (3) Usos que a posição não considerou

- O canário multi-modelo (prompt congelado por SHA, manifest com hashes, projeção de custo pré-gasto, adjudicação mecânica) rodou a **~US$1,40/rodada** e achou dezenas de defeitos reais de coerência nos mundos. Esse protocolo é um harness de QA reutilizável para qualquer artefato do repo — independentemente do destino dos mundos.
- O achado de instabilidade (3/2 sob entradas congeladas, backend `gpt-5.6-sol`) é um resultado de *medição* valioso para qualquer consumidor futuro, inclusive o Valter: prova que eval de uma amostra não mede nada.
- Para SEN-1746, o ativo público mais forte não são os mundos (fracos, como a posição diz) nem só o método — é o **dossiê completo com recibos, hashes e a nota de correção**, um caso raro de eval auditável de ponta a ponta em pt-br. O README do P1 é praticamente o paper.

Sobre a Receita C: a posição está correta e a evidência a reforça — o dossiê descreve a receita (corpus real controlado, agentes-oráculo, decisão de abster-se, avaliação separada de localização de fonte/correção/citação) e ainda nota que o juiz do LAB **não recebe os documentos-fonte**, ou seja, grounding exige rubrica própria. A transferência para o Valter está bem desenhada; nada a corrigir aí.

## (4) Autoclassificação: **material**

Encontrei uma contradição decisiva não declarada (a suíte congelada reprova a skill publicada; a única versão que passa está revertida) e um defeito estrutural no próximo passo recomendado (dogfood sem cegueira possível), ambos com evidência direta nos arquivos — mas a recomendação central (não generalizar, Receita C para o Valter) sobrevive.

## ALAVANCAS

- O ativo mais defensável não é o benchmark: é a **cadeia de custódia** (spec oculta → hashes → recibos → adjudicação → nota de correção). Ninguém mais em pt-br publicou isso; é o conteúdo de SEN-1746 mesmo sem publicar um único mundo.
- O canário cego a US$1,40/rodada com projeção pré-gasto é um segundo produto, já provado quatro vezes (v1–v4), e cobre um caso que o decisor não contou: QA de qualquer documento normativo do repo, não só de mundos.
- A instabilidade medida (3/2; juízes divergentes sobre o mesmo transcript) é munição para exigir painéis em toda eval futura — inclusive na Receita C do Valter, que herda o desenho de graça.
- A reversão a v0.6.4, lida sem caridade, é o melhor argumento contra "continuar generalizando": nem a família já construída teve seu achado promovido; escalar o gerador antes de promover o que ele já mediu seria repetir o desvio diagnosticado.
- "Um achado promovido por ~10M tokens" é a formulação afiada que decide a conversa com o Diego-sonhador: o problema não é a fábrica, é o custo marginal por decisão mudada.

## ONDE QUEBRA

- A recomendação "congelar como regressão" pressupõe uma suíte verde; a suíte real é vermelha sobre a skill publicada, e a posição não escolhe entre promover o candidato estrutural ou aceitar o invariante 7 como dano conhecido. Sem essa escolha, o congelamento é arquivamento disfarçado.
- O "menor próximo passo" (dogfood de M-201 pelo Diego) não produz o recibo que promete: o construtor do gabarito não é consumidor cego, e a artificialidade dos templates está documentada pelos próprios revisores. O passo muda uma decisão, mas não a que a posição afirma.
- A premissa "custo externo ~0" é contabilmente frágil: ~10M tokens de franquia Codex são o custo real, e com a variância medida do executor+juiz, uma regressão estatisticamente séria custa múltiplos do que a rodada já gastou. Se a franquia apertar, "rodar quando a skill mudar" deixa de ser viável e o item 2(a) inteiro ("já útil hoje") cai junto.

### Síntese das tensões

```
CROSS-MODEL TENSION:
  Suíte vermelha: Decisor dizia "congelar como regressão". K3 diz que a P1
    reprova a skill publicada e que congelar sem decidir o invariante 7 é
    arquivar. Sol indisponível. → Mecânica: K3 está certo; a posição passou a
    exigir a decisão "defeito conhecido vs promover" dentro da opção A.
  Próximo passo: Decisor dizia "dogfood humano nos mundos". K3 diz que o autor
    do gabarito não é consumidor cego e que a artificialidade está
    documentada. → Taste, aceito em parte: o passo virou julgamento de leitura
    a custo zero; o recibo de uso humano sai de um caso não desenhado por
    Diego.
  Custo: Decisor citava 5,5 M tokens. K3 corrige para ~10 M na P1 e ~15 M no
    total, por um achado promovido. → Mecânica: corrigido.
  Usos novos (protocolo de QA cego; medição de instabilidade; cadeia de
    custódia como ativo público): acrescentados à Etapa 8.
```

Nenhuma divergência é User Challenge: o owner não havia declarado direção;
pediu a análise.

## Insight

★ Insight ─────────────────────────────────────
A fábrica provou o método, não o mercado. O que ela tem de mais valioso não
são os 72 mundos: é a cadeia de custódia (ficha oculta, hashes, recibos,
adjudicação, nota de correção) e a lição de que avaliação de amostra única
não mede nada. O sonho de "casos em volume para testar tudo" esbarra em duas
coisas: cada família exige ficha e renderizador próprios, e o Valter precisa
de outra receita. E a régua, hoje, reprova a própria skill publicada num
ponto que só você pode dizer se importa. Por isso o próximo passo é leitura,
não execução.
─────────────────────────────────────────────────

## Decisão pedida

1. Congelar P0 e P1 como régua de regressão (painel de 3 nos 9 cenários
   críticos como gate barato; suíte completa só em release, com teto de
   tokens) e registrar o invariante 7 como defeito conhecido da v0.6.4 até a
   sua leitura? Recomendo sim.
2. Ler hoje os dois memorandos congelados de `M-202/W-A` e dizer qual
   preferiria receber? Recomendo sim; é o único passo que muda a decisão sem
   gastar franquia. Se preferir o estrutural, a regressão P0 restante entra
   na fila para depois de 07/09.
3. Obter o recibo de uso humano do plugin em um caso que você não desenhou
   (o caso do dogfood da deliberação, ou um caso real sob protocolo de
   privacidade a definir), e não nos mundos sintéticos? Recomendo sim, em
   sessão própria.
4. Registrar a Receita C (perguntas sintéticas sobre corpus real + oráculo +
   rubrica de citação) como próxima investigação do Valter, sem iniciar
   aqui? Recomendo sim, como issue no Linear.
5. Não construir novas famílias nem generalizar o gerador até existir um
   segundo consumidor com pedido concreto? Recomendo sim.

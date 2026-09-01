# Canário cego P1 — revisão por modelos (2026-09-01)

## Correções finais de coerência pós re-revisão (2026-09-01, estático) — ENCERRAMENTO da cadeia de revisão

Última rodada estática sobre os flags (b) confirmados em
`kimi-rereview-adjudication-v1.json`. **Não haverá nova rodada cega**: a
cadeia de revisão do lote P1 encerra-se aqui. Correções aplicadas (todas com
verificação estática por grep nos cegos; `build_batch.py build`/`check` PASS;
isolamento de mutações preservado; os hashes do lote mudaram em relação aos
pacotes da re-revisão):

1. **M-207 quantum × avaria parcial (fio i):** o laudo passou a quantificar o
   dano — 40% do valor declarado da carga = **R$ 27.120,00** (67.800 × 0,40,
   verificável) — e a sentença condena nesse valor, ancorada ao laudo (o
   pedido da inicial segue em R$ 67.800,00: procedência parcial). A
   contestação foi reescrita: a ré **reconhece a ocorrência registrada em seu
   próprio termo** e impugna extensão/quantum e nexo ("o dano é inferior ao
   alegado"), sem desmentir o documento que ela mesma emitiu (novo branch
   `transporte` em `answer_batch`).
2. **M-208 revisional:** repetição de indébito deixou de ser o preço integral:
   agora **R$ 14.040,00** (15% do contrato, ordem compatível com revisional
   de encargos), "correspondentes aos encargos cobrados além do permitido",
   ancorados ao quadro resumo + memória de cálculo da inicial (esta segue
   citada-não-juntada, padrão deliberado de lacuna legítima).
3. **M-210 contestação e resolução:** defesa reescrita como alternativa
   padrão — nega o atraso nos termos alegados e **subsidiariamente** ("ainda
   que se entendesse por atraso, este decorreria de...") invoca o caso
   fortuito; a sentença de resolução passou a dispor das restituições
   recíprocas (devolução do galpão à autora × torna à autora × unidades
   parcialmente entregues à ré).
4. **M-211 anulação:** a sentença passou a determinar, em uma linha, a
   devolução das bancadas instaladas à ré (restituições recíprocas).
5. **M-212 NF e laudo:** a NF da comissão passou a ser emitida na data do
   fato gerador (2021-05-10, fechamento dos contratos — antes era 20 dias
   anterior); o laudo agora enfrenta o nexo de intermediação ("fechados por
   intermediação da autora, como demonstram o relatório de intermediação e a
   planilha de negócios concluídos"), respondendo à tese do "canal direto".

**Resíduos classe (c) aceitos como convenção do fixture** (documentados, não
corrigidos): ramos de atividade fantasia das partes (banco implantando
software, corretora náutica intermediando energia, financeira fornecendo
fornos), peças citadas-não-juntadas como lacuna deliberada de
`missing_evidence` (memória de cálculo, planilha, comprovantes, proposta,
apólice), marcadores declarados de ficção (rótulos "sintético", comarcas
"Experimentais", IDs mecânicos), contestação sempre no 15º dia útil,
calendário sob medida da janela de contagem e ressalva autolimitada do
documento 04 em W-B (instrumento deliberado da mutação).

---

## Adjudicação da re-revisão P1 pós-correções (M-207..M-212, 2026-09-01)

`kimi-rereview-adjudication-v1.json` (adjudicação mecânica/operador, sem rede
e sem chamada paga) compara as revisões cegas congeladas `kimi-rereview-revisor
1-frozen.json` e `kimi-rereview-revisor 2-frozen.json` (M-207..M-212 ×
W-A/W-B/W-C, 18 mundos, sobre o lote JÁ corrigido pela rodada estática acima)
com os gabaritos de `../batch-generated/authority/`. Resultado: **PASS** —
18/18 mundos; 24/24 críticas e 12/12 major recuperadas por **cada** revisor;
zero falso positivo crítico; nenhum flag classe (a). Correções estáticas
conferidas como mortas nos cegos: inversão de papéis e "instalação" de M-212,
aceite × atraso de M-210, rescisão × quitação de M-209, à vista × revisional
de M-208, e o bug (a) de M-208 W-C (data divergente agora 2023-02-17, dia de
expediente). Flags (b) novos/residuais confirmados — todos de **coerência
objetiva**: quantum integral × avaria parcial e contestação × próprio termo
(M-207); revisional com restituição do preço integral (M-208); contestação que
confessa e nega o atraso e resolução sem restituições recíprocas (M-210, aqui
com divergência justificada do precedente do pacote B); anulação sem
restituição das bancadas (M-211); NF anterior ao fato gerador e laudo sem nexo
de intermediação (M-212). Flags de **plausibilidade de convenção** (ramo de
atividade fantasia das partes — banco-software, financeira-fornos, corretora
náutica-energia —, juridiquês no SAC, NF de torna, crédito sem juros, custas
~8%) classificados (c). Elementos deliberados do protocolo (ficção declarada,
nota normativa, ressalva autolimitada do 04 em W-B, divergência limpa de 7
dias e calendário sob medida em W-C, peças citadas-não-juntadas) não são
defeitos. Todas as contagens de prazo das duas hipóteses de W-C refeitas e
corretas nos 6 matters; feriados conferem com o calendário real. Nada no lote,
nos geradores ou em `authority/` foi alterado; nada commitado.

## Correções pós-adjudicação pacotes A/B (2026-09-01, estático, sem nova rodada paga)

Rodada estática sobre os defeitos confirmados em
`kimi-remaining-A-adjudication-v1.json` e
`kimi-remaining-B-adjudication-v1.json` (flags classes (a)/(b) verificados um
a um nos cegos). **Os hashes do lote mudaram em relação aos pacotes A/B e ao
pacote da v4; revisores cegos novos re-avaliarão os matters afetados
(M-207..M-212 e W-C dos 12).** Flags atacados:

1. **(a) M-208 W-C — mutação em dia sem expediente** (2023-02-20, segunda de
   Carnaval): o snap de datas passou a pular também feriados nacionais
   (`snap_to_weekday` em `../build_worlds.py` agora retrocede fins de semana
   E feriados), aplicado a TODAS as datas da espinha, inclusive a data
   divergente de W-C; novo cheque duro no validador exige as duas datas
   citatórias em dia de expediente. Verificado nos 12 matters: W-C com ambas
   as certidões em dia de expediente e desfechos opostos preservados
   (M-208: divergente agora 2023-02-17, sexta anterior ao Carnaval).
2. **(b) M-212 — inversão de papéis:** novo variant `intermediacao` — Solário
   é a contratante que deve comissão à corretora Sargaço (direção econômica
   única); NF emitida por Sargaço contra Solário ("Referente: comissão de
   corretagem"); doc 03 virou `03-relatorio-intermediacao.md` (relatório de
   intermediação com planilha de negócios concluídos, sem "instalação");
   inicial alinhada ("foi contratada pela ré... não pagamento da comissão").
3. **(b) M-210 — aceite × atraso:** variant `permuta_torna` — contrato de
   permuta com cláusula de torna (o dinheiro é a torna, não "preço à vista");
   NF "Referente: torna"; doc 03 virou `03-termo-aceite-parcial.md` (aceite
   parcial com ressalva expressa de pendências de entrega), coerente com
   04/05/08/11.
4. **(b) M-209 — rescisão × quitação:** fio único — `action_label` "repetição
   de indébito por cobrança em duplicidade"; pedido/sentença = quitação das
   parcelas vencidas + repetição de R$ 32.000,00 (duas parcelas de
   R$ 16.000,00 do plano de 8, ancoradas nos comprovantes examinados no
   laudo) — sem repetição do valor cheio 2 meses após a contratação.
5. **(b) M-207 — estufas × acidente:** variant `transporte` — objeto "transporte
   rodoviário de estufas modulares com carga declarada"; doc 02 virou
   `02-cte-conhecimento-carga.md` (CT-e com valor da carga); doc 03 virou
   `03-termo-ocorrencia-transporte.md` (colisão e avaria registradas no
   acervo); laudo examina documento presente ("colisão registrada no termo
   de ocorrência do transporte"); sentença ancorada no valor da carga do
   CT-e.
6. **(b) M-208 — à vista × revisional:** variant `credito_parcelado` —
   financiamento em parcelas mensais com encargos em quadro resumo anexo
   (lastro à revisional de capitalização); sentença ancorada no quadro resumo
   + memória de cálculo da inicial.
7. **(b) transversal — condenação = preço sem prova do quantum:** padrão de
   M-201/M-202 aplicado a todos os matters restantes (M-203..M-212): toda
   condenação agora declara a base documental ou o critério do valor
   (contrato+NF, apólice, torna, comissão ajustada, CT-e, quadro resumo,
   parcelas em duplicidade).

`../build_batch.py build`/`check` PASS; `../build_worlds.py build`/`check`
PASS (função de snap tocada; `world_spec.json` e `seed_spec_sha256`
inalterados); isolamento de mutações preservado (W-B só doc 04, W-C só doc
07, inclusive nos matters com docs renomeados); sem datas futuras.

---

## Adjudicação do pacote A da família sintética restante (2026-09-01)

`kimi-remaining-A-adjudication-v1.json` (adjudicação mecânica/operador, sem
chamada paga) compara as revisões cegas congeladas `kimi-remaining-A revisor
1-frozen.json` e `kimi-remaining-A revisor 2-frozen.json` (M-205..M-208 ×
W-A/W-B/W-C) com os gabaritos de `../batch-generated/authority/`. Resultado:
**PASS** — 12/12 mundos; 16/16 críticas e 8/8 major recuperadas por **cada**
revisor; zero falso positivo crítico. Ressalva: confirmado **1 defeito classe
(a)** em M-208 W-C (mutação "citação − 7 dias" caiu em 2023-02-20, segunda de
Carnaval sem expediente pelo próprio doc 17 — certidão de W-C não causalmente
possível; mesmo padrão do bug (a) do canário v3), além de 3 flags (b) (M-208 à
vista × revisional de encargos; M-207 contrato de estufas × ação de acidente;
quantum = preço total sem lastro, transversal) e 4 (c) (marcadores de
artificialidade, lacunas do corpus mínimo, extrato 15 sem citação, ressalva
didática do doc 04 de W-B). Correção do flag (a) fica com o owner; nada no
lote foi alterado.

## Adjudicação do pacote B da família sintética restante (2026-09-01)

`kimi-remaining-B-adjudication-v1.json` (adjudicação mecânica/operador, sem
chamada paga) compara as revisões cegas congeladas `kimi-remaining-B revisor
1-frozen.json` e `kimi-remaining-B revisor 2-frozen.json` (M-209..M-212 ×
W-A/W-B/W-C) com os gabaritos de `../batch-generated/authority/`, com os flags
de construção verificados nos documentos cegos. Resultado: **PASS** — 12/12
mundos; 16/16 críticas e 8/8 major recuperadas por **cada** revisor; zero falso
positivo crítico. Nenhum flag classe (a). Classes (b) confirmadas (incoerências
de narrativa dos matters, não do instrumento de mundos): inversão de papéis
corretora/contratante e "instalação" de serviço de intermediação em M-212;
aceite sem ressalvas × atraso/não entrega e permuta × preço à vista em M-210;
rescisão × quitação e parcelas mensais × quitação integral do valor cheio em
M-209. Demais flags: (c) cosméticos/template, ou elementos deliberados do
protocolo (declaração de ficção no task.md, nota normativa, ressalva
autolimitada do doc 04 de W-B, divergência limpa de 7 dias em W-C) com os quais
o adjudicador não concorda como defeito. Feriados de Carnaval do calendário de
M-211 W-C conferem com a data real (2022-03-01). Nada no lote, nos geradores ou
em `authority/` foi alterado; nada commitado.

## Correção pós-canário (2026-09-01, sem nova rodada paga)

O canário fechou na v4 com **CONSTRUIR no lote para os dois modelos**. Restou
um único flag localizado, classe (b), do opus v4 em **M-203**: o
`contract_variant` `assinatura_periodica` falava em renovação automática "por
períodos anuais sucessivos", mas a reclamação da autora ocorre menos de dois
meses após a contratação — renovação alegada antes de qualquer renovação
possível.

- **Correção aplicada (estática, custo zero):** o texto do variant passou a
  "renovação automática **mensal**" em `../build_batch.py` (`contract_batch`),
  coerente com a cobrança mensal recorrente já existente. Nenhuma data foi
  movida; o variant só é usado por M-203. Coerência verificada mecanicamente:
  contrato 2023-04-07 → primeira renovação mensal possível 2023-05-07 <
  reclamação 2023-06-02. `build_batch.py build`/`check` PASS; isolamento de
  mutações preservado.
- **Justificativa da dispensa de nova rodada cega (decisão do owner):** o
  defeito era aritmeticamente verificável (comparação de datas), localizado a
  um único matter e sem juízo de mérito — a correção não altera a
  recuperabilidade medida nos canários (a mutação de W-C e as observações dos
  gabaritos não dependem do texto da cláusula).
- **Nota de hashes:** os hashes do lote mudaram em relação ao pacote da v4
  (somente os documentos `01-contrato-prestacao.md` dos três mundos de M-203
  e os manifests/authority derivados). Os artefatos v1–v4 permanecem
  congelados e descrevem os lotes anteriores; qualquer futura rodada cega deve
  reconferir os hashes contra os manifests atuais.

---

Espelho do protocolo do canário P0 (`data/research/2026-08-31-world-spec-p0`),
aplicado ao lote cego P1 (`batch-generated/blind/`, batch
`br-civel-conhecimento-calibrado-v1`).

**v2 (re-canário):** após o redesenho estático dos 6 defeitos do v1, o lote foi
reconstruído (hashes novos, conferidos com os manifests) e o protocolo foi
repetido integralmente. Artefatos v2: `sonnet-5-canary-v2/`,
`opus-5-canary-v2/`, `canary-adjudication-v2.json` (gerado por
`../build_canary_adjudication_v2.py`). O v1 permanece congelado e descreve o
lote pré-redesenho.

**v3:** após o segundo redesenho (5 flags do v2), mesmo protocolo. Artefatos
v3: `sonnet-5-canary-v3/`, `opus-5-canary-v3/`, `canary-adjudication-v3.json`
(gerado por `../build_canary_adjudication_v3.py`, com resolução dos 5 flags do
v2 e classificação dos flags novos em (a) bug de instrumento, (b) contradição
interna/realismo, (c) cosmético). Régua de parada do owner avaliada e NÃO
atingida (há flag classe (a)); decisão registrada para o owner.

**v4:** após a correção estática do bug (a) da v3 (a mutação de W-C passou a
divergir sobre a data de DISPONIBILIZAÇÃO — as duas certidões, cada uma
causalmente possível — em vez de efetivação anterior à disponibilização; e as
datas cartorárias ganharam snap de dia útil). Artefatos v4:
`sonnet-5-canary-v4/`, `opus-5-canary-v4/`, `canary-adjudication-v4.json`
(gerado por `../build_canary_adjudication_v4.py`). Resultado: **CONSTRUIR no
lote para os dois modelos** (primeira vez); REDESENHAR localizado do opus em
M-203 por flag (b) novo (renovação anual × reclamação <2 meses). Régua do
owner: flag (b) novo justifica avaliar v5 — decisão com o owner.

## Escopo

- Matters do canário: um por motif, lidos do `batch-spec.json` —
  M-201 (`defesa_revelia`), M-202 (`perfil_probatorio`), M-203 (`desfecho`),
  M-204 (`tensao_temporal`). 12 mundos (W-A/W-B/W-C × 4), 216 arquivos
  transportados (task.md + 17 documentos por mundo; `manifest.json` dos mundos
  NÃO foi transportado — usado só para conferência de hashes).
- Hashes SHA-256 dos 216 arquivos cegos conferem com os manifests de cada mundo
  (`manifest_hash_check.pass: true` nos dois recibos).
- Script: `../run_batch_canary_review.py` (adaptado do P0; prompt igualmente
  cego, com a frase específica de "pagamento e prazo" generalizada para
  "a análise pedida em `task.md`", pois as tarefas P1 não são de execução).
- Adjudicação mecânica/operador, sem terceira chamada paga:
  `../build_canary_adjudication.py` → `canary-adjudication-v1.json`.

## Chamadas v1 (congeladas, lote pré-redesenho)

| Modelo | Diretório | stop_reason | input tok | output tok | Custo (US$) |
|---|---|---|---|---|---|
| claude-sonnet-5 | `sonnet-5-canary-v1/` | end_turn | 57.664 | 22.543 | 0,340758 |
| claude-opus-5 | `opus-5-canary-v1/` | end_turn | 57.664 | 28.950 | 1,012070 |

- Total gasto: **US$ 1,352828** (teto US$ 2,00).
- Projeção pré-chamada (consta dos recibos): esperado US$ 1,29; pior caso
  US$ 1,82 — dentro do teto antes de gastar.
- Mesmo prompt nas duas chamadas: sha256
  `0b83464e2f1771c309558a671690bb66b39479a188cfff7f59d737a8db12e59f`
  (129.046 bytes). Preços por milhão embutidos no script (sonnet 2/10,
  opus 5/25), custos calculados do `usage` real, sem prompt caching.
- Sem tools, sem retry automático, `effort: high`, `service_tier: standard_only`.
- Ressalva operacional: a primeira invocação do opus-5 foi morta pelo timeout do
  harness local (300 s) antes de qualquer escrita — nenhum artefato gerado,
  nenhum `usage` reportado. A chamada gravada é uma nova invocação isolada com
  o mesmo prompt (`retries: 0` no recibo, timeout do harness elevado).

## Chamadas v2 (congeladas, lote redesenhado)

| Modelo | Diretório | stop_reason | input tok | output tok | Custo (US$) |
|---|---|---|---|---|---|
| claude-sonnet-5 | `sonnet-5-canary-v2/` | end_turn | 61.186 | 22.445 | 0,346822 |
| claude-opus-5 | `opus-5-canary-v2/` | end_turn | 61.186 | 26.488 | 0,968130 |

- Custo v2: **US$ 1,314952** (teto novo de US$ 2,00; projeção pré-gasto:
  esperado 1,32 / pior caso 1,85). Custo v1+v2: **US$ 2,667780**.
- Mesmo prompt nas duas chamadas v2: sha256
  `49c131b893300ad19b810a485ed13263db5c4bfd0719a3780c1950a77fdf2330`
  (138.496 bytes — o prompt mudou porque o lote foi redesenhado; os 216 hashes
  conferem com os manifests novos).

## Chamadas v3 (congeladas, lote do segundo redesenho)

| Modelo | Diretório | stop_reason | input tok | output tok | Custo (US$) |
|---|---|---|---|---|---|
| claude-sonnet-5 | `sonnet-5-canary-v3/` | end_turn | 64.149 | 25.577 | 0,381244 |
| claude-opus-5 | `opus-5-canary-v3/` | end_turn | 64.149 | 29.514 | 1,051535 |

- Custo v3: **US$ 1,432779** (teto US$ 2,00; projeção pré-gasto 1,34/1,86).
  Acumulado **v1+v2+v3: US$ 4,100559**.
- Mesmo prompt nas duas chamadas v3: sha256
  `fad42278f2da290f31183cea88727f96a7aa937b29f0d91668f0478593dd58f2`
  (143.065 bytes; 216 hashes conferem com os manifests atuais).
- Ressalva operacional: a primeira invocação do sonnet-5 falhou com HTTP 520
  (erro de borda) antes de qualquer resposta — sem artefato e sem uso cobrado;
  a chamada congelada é invocação isolada posterior (`retries: 0` no recibo).

## Chamadas v4 (congeladas, lote pós-correção do bug (a))

| Modelo | Diretório | stop_reason | input tok | output tok | Custo (US$) |
|---|---|---|---|---|---|
| claude-sonnet-5 | `sonnet-5-canary-v4/` | end_turn | 62.941 | 26.689 | 0,392772 |
| claude-opus-5 | `opus-5-canary-v4/` | end_turn | 62.941 | 32.978 | 1,139155 |

- Custo v4: **US$ 1,531927** (teto US$ 2,00; projeção pré-gasto 1,34/1,87).
  Acumulado **v1+v2+v3+v4: US$ 5,632486**.
- Mesmo prompt nas duas chamadas v4: sha256
  `a436bfdda4d37c3a31b0e4c7d70c3cc7a3f2e0a63ecc653ca8eed357f3765c3c`
  (143.629 bytes; 216 hashes conferem com os manifests atuais).

## Veredito do canário v4

- **claude-sonnet-5**: **CONSTRUIR** no lote e nos 4 matters.
- **claude-opus-5**: **CONSTRUIR no lote** e em M-201, M-202, M-204;
  **REDESENHAR localizado em M-203** (flag (b) novo: cláusula de renovação
  anual incompatível com reclamação de renovação <2 meses após a contratação;
  persistentes: NF única × mensalidade, cancelamento não documentado,
  restituição não quantificada).
- Status da adjudicação v4: **PASS_BATCH_WITH_MATTER_FLAG**. Régua do owner:
  há flag (b) novo → v5 justificável, decisão com o owner (correção seria de
  mérito de um único matter, não do instrumento de mundos).

Recuperação de observações v4:

| Severidade | sonnet-5 | opus-5 |
|---|---|---|
| critical (16) | 16 recovered | 16 recovered |
| major (8) | 8 recovered | 8 recovered |

- Falsos positivos críticos: nenhum, nos dois modelos.

## Status dos flags v3 (verificados um a um no v4)

- (a) inversão causal em W-C: **morto** — W-C diverge sobre a data de
  disponibilização; as duas certidões são causalmente possíveis e as duas
  contagens seguem com desfechos opostos nos 4 matters.
- (b) certidões em sábado: **morto** — datas cartorárias em dia útil.
- (b) NF única × mensalidade (M-203): **persiste** (opus repete).
- (b) mercadoria × preço (M-202): **persiste** como achado legítimo, não
  bloqueante, para ambos.
- (c) cosméticos: **persistem** sem bloqueio (opus os cita explicitamente como
  não impeditivos).

## Flags novos do v4 (classificados)

- **(b)** M-203: renovação "por períodos anuais sucessivos" invocada <2 meses
  após a contratação — incoerência temporal do contract_variant (opus:
  REDESENHAR M-203; sonnet não flagrou).
- **(c)** M-203: pedido de cancelamento não documentado + restituição não
  quantificada pelo laudo (padrão de lacuna deliberada, somado pelo opus ao
  REDESENHAR de M-203).
- **(c)** redação templada da inicial, protocolos/valores em série, janelas de
  calendário sempre uma semana antes da citação.

## Veredito do canário v3 (congelado)

- **claude-sonnet-5**: **CONSTRUIR** no lote e nos 4 matters.
- **claude-opus-5**: CONSTRUIR em M-202 e M-204; **REDESENHAR em M-201, M-203
  e no lote** — flag classe (a): em W-C a efetivação (visualização) antecede a
  disponibilização, impossibilidade causal da mutação sob o modelo eletrônico.
- Status da adjudicação v3: **PASS_WITH_REDESIGN_FLAG**. Régua de parada do
  owner (parar se REDESENHAR só com cosméticos): **NÃO atingida** — há flag
  classe (a); decisão sobre nova iteração fica com o owner.

Recuperação de observações v3:

| Severidade | sonnet-5 | opus-5 |
|---|---|---|
| critical (16) | 16 recovered | 16 recovered |
| major (8) | 8 recovered | 8 recovered |

- Falsos positivos críticos: nenhum, nos dois modelos.

## Status dos 5 flags do v2 (verificados um a um no v3)

Todos mortos: (1) calendário/Sexta-feira Santa — ambos excluem 29/03 nas
contagens; (2) modalidade citatória — sem AR×mandado; (3) esqueleto M-203 —
contrato periódico lido como evidência legítima; (4) critério de quantum
M-201 — critério declarado na sentença; (5) cheiros de template do v2
(razão de custas, datas de fase) — não reapareceram.

## Flags novos do v3 (classificados)

- **(a) bug de instrumento:** W-C com efetivação anterior à disponibilização
  nos 4 matters (a regra "conflito = citação − 7 dias" virou impossibilidade
  causal no modelo eletrônico). Opus: REDESENHAR; sonnet: implausível mas não
  bloqueante.
- **(b) realismo/contradição:** certidões citatórias em sábado (M-201, M-203);
  M-203 com NF única × cobrança mensal e "termo de instalação" físico para
  serviço digital; persiste o descompasso mercadoria×preço de M-202 (não
  bloqueante para ambos).
- **(c) cosmético/template:** contestação sempre no 15º dia útil exato;
  calendário delimitando exatamente as duas hipóteses; "encaminhada à
  assistência técnica" genérico; extrato sem atos citatórios; certidão de
  restrição citada-não-juntada.

## Veredito do canário v2 (congelado)

- **claude-sonnet-5**: CONSTRUIR em M-201 e M-204; **REDESENHAR em M-202 e
  M-203** (descompasso quantum↔causa de pedir) e no lote.
- **claude-opus-5**: CONSTRUIR em M-202 e M-204; **REDESENHAR em M-201 e
  M-203** (narrativa do vício/dano moral=preço; contrato à vista incompatível
  com renovação automática) e no lote.
- Status da adjudicação v2: **PASS_WITH_REDESIGN_FLAG** (M-203 é REDESENHAR
  para ambos; M-204 é CONSTRUIR para ambos; M-201 e M-202 dividem os modelos).

Recuperação de observações v2 (gabaritos do lote redesenhado):

| Severidade | sonnet-5 | opus-5 |
|---|---|---|
| critical (16) | 16 recovered | 16 recovered |
| major (8) | 8 recovered | 8 recovered |

- Falsos positivos críticos: nenhum, nos dois modelos.

## Status dos 6 redesign_flags do v1 (verificados um a um no v2)

1. Perícia incoerente (M-201/M-203): **parcial** — tipo de prova agora coerente
   (contábil/documental, deferida e concluída em cadeia); residual: o laudo
   diz "examinando o objeto" físico e o laudo de M-203 não enfrenta o canal de
   cancelamento.
2. Quantum sem base (M-202): **parcial** — a sentença agora amarra o valor a
   contrato+NF; persiste o descompasso mercadoria perdida × preço do
   equipamento (bloqueante para o sonnet, achado legítimo para o opus).
3. NF genérica sem data: **resolvido** — NF-SYN-1001..1004 com data, citadas
   sem queixa pelos dois modelos.
4. Custas fixas: **resolvido** — valores variam por matter; o opus nota a
   razão constante custas/valor (~1,87%) como padrão de template.
5. Hiato laudo→sentença: **resolvido** — manifestação de 2025-04-14 citada em
   sentença e extrato; virou lacuna legítima (peça não juntada), não hiato.
6. Task × mutação W-C: **resolvido** — ambos ancoram a divergência no novo
   item 4 em todos os mundos, inclusive M-202/M-203.

## Novos defeitos reportados pelo v2 (congelados, sem redesenho)

- Calendário forense nega expediente em 2024-03-29 (Sexta-feira Santa) em
  todos os matters (sonnet).
- Modalidade citatória incoerente: AR postal (06) × certidão "retorno do
  mandado" (07), sensível a L335 (opus, todos os mundos).
- M-203: contrato "pago à vista na assinatura" sem cláusula de renovação ×
  mérito todo baseado em renovação automática/cobranças sucessivas (ambos).
- M-201: dano moral idêntico ao preço sem critério; anotação negativa sem
  prova; "objeto passou a apresentar cobranças" (opus).
- Razão custas/valor constante e datas de fase idênticas entre matters
  (ambos).

## Veredito do canário v1 (congelado)

- **claude-sonnet-5**: CONSTRUIR no lote e nos 4 matters.
- **claude-opus-5**: CONSTRUIR em M-202 e M-204; **REDESENHAR em M-201, M-203 e
  no lote**. Pela regra dura, nada foi redesenhado: os defeitos foram congelados
  e reportados (ver `redesign_flags` na adjudicação).
- Status da adjudicação: **PASS_WITH_REDESIGN_FLAG**.

Recuperação de observações (gabaritos `authority/<matter>/<mundo>/ground_truth.json`):

| Severidade | sonnet-5 | opus-5 |
|---|---|---|
| critical (16) | 16 recovered | 16 recovered |
| major (8) | 8 recovered | 8 recovered |

- Falsos positivos críticos: nenhum, nos dois modelos.
- Realismo médio (1–5): sonnet 4/4/3 (W-A/W-B/W-C) em todos os matters;
  opus 3–4 conforme o matter (detalhe por mundo na adjudicação).

## Defeitos identificados pelo opus-5 (reportados, não corrigidos)

1. M-201 e M-203: instrução probatória incoerente com a causa de pedir — a
   controvérsia é contratual (cobranças/renovação automática), mas o saneador
   defere perícia técnica sobre equipamento e o laudo devolve conclusão
   jurídico-contratual.
2. M-202: condenação por dano material igual ao preço contratual, sem prova do
   quantum; laudo silente sobre o valor da mercadoria perdida.
3. Transversal: NF-SYN-0007 genérica e sem data nos quatro matters; custas
   fixas idênticas de R$ 4.812,00 (≈21% do pedido em M-203); datas de fase
   idênticas entre processos; hiato de atos entre laudo (2025-02-10) e sentença
   (2025-09-22); nos W-C de M-202 e M-203 o item 9 do task.md aponta cadeias que
   não contêm o defeito inserido (desalinhamento enunciado/mutação).
4. O sonnet-5 também notou, sem reprovar: custas fixas idênticas e calendário
   forense cobrindo exatamente o intervalo da mutação (indício de
   reaproveitamento de template entre variantes).

## Ressalvas

- O status "recovered" de cada observação é decisão do operador, auditável
  pelas citações verbatim em `canary-adjudication-v1.json` e pelas respostas
  congeladas (`review.json`/`raw-response.json` de cada diretório).
- O REDESENHAR do opus-5 não invalida a recuperabilidade (16/16 + 8/8 nos dois
  modelos): é um sinal de qualidade de coerência material do corpus sintético,
  a ser decidido pelo operador fora deste canário.
- Nenhum arquivo do P0, dos geradores P1 (`world_spec.json`, `build_worlds.py`,
  `build_batch.py`, `batch-spec.json`) ou de `authority/` foi alterado; nada foi
  commitado.

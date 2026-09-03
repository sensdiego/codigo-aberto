# Handoff de sessão

Atualizado em 2026-09-03 após o gate de valor da fábrica sintética, a
documentação do caminho de instalação no aplicativo do Claude e o merge do
PR #37. A próxima sessão começa pelos recibos que dependem do owner
(instalação no aplicativo, leitura comparada, uso humano), não por nova
rodada de avaliação.

## Ponto de continuidade

- Sessão de 2026-09-03: PR #37 integrado em `main` (merge `6d2bbe7`; o
  workflow consumiu o fragmento `none` em `9c193ef`). Versão corrente
  continua `v0.6.4`; skills distribuídas inalteradas. README, QUICKSTART e
  RELEASING documentam a instalação do plugin completo no aplicativo do
  Claude por marketplace. Memorando de decisão da fábrica sintética em
  `data/research/2026-09-03-fabrica-sintetica-valor.md`; conselho registrado
  no ledger (Sol indisponível por franquia; K3 material). Issues criadas:
  SEN-2427 (Receita C, brainstorm no Valter) e SEN-2428 (revisita da fábrica
  em 2026-10-05, filha de SEN-2381).
- Branch canônica: `main`. A adaptação entrou no commit `1db8dd2`; o workflow
  `Software release` publicou a tag imutável `v0.6.4` no commit `490936e`.
  O sincronismo posterior destes documentos é `none` e não cria nova versão.
- Dogfood pareado da deliberação: **executado e registrado** — veredicto
  MANTÉM; a porta deliberativa sai de "experimento sem aceitação" para
  capacidade aceita para uso interno. Ressalva registrada: operador foi
  agente aplicando a folha do advogado, não Diego; o desfecho "não redigir"
  segue sem recibo. Recibos em
  `data/dogfood/2026-08-31-pareado-deliberacao/` (veredicto, registros,
  transcripts); comentário na issue #22.
- Família P1 `br-civel-conhecimento-calibrado-v1` **construída e fechada**
  em `data/research/2026-09-01-world-spec-p1/`: 12 assuntos, 36 mundos, 612
  documentos cegos, cronologia multi-ano com feriados reais, gate de base
  empírica real (39 casos de procedimento comum da carteira). Canário cego
  em 4 rodadas até CONSTRUIR dos dois modelos (custo total US$ 5,63);
  adjudicação dos 8 assuntos restantes por revisores cegos independentes
  (subagentes Kimi, não Codex): **PASS 36/36 mundos**, 16/16 críticas e
  8/8 relevantes, zero falso positivo crítico. Limitação declarada: mesma
  família de modelo nos revisores; isolamento processual integral.
- Adaptação P1 da régua: `tests/fixtures/world-spec-p1-workflows.json`
  materializa os 36 cenários aprovados; P0 declara 7 invariantes por mundo e
  P1 declara 8. O recibo final autoriza o lote corrente para regressão sem
  fingir uma nova revisão cega dos bytes corrigidos pelo owner.
- Rodada comportamental P1: depois de duas correções textuais instáveis, o
  commit experimental `5af4a27` tornou obrigatório um quadro estrutural de
  relações probatórias. O painel crítico repetido passou 9/9; a P1 cobriu os 36
  cenários únicos e ficou 36/36 por adjudicação. Não foi uma passagem
  automatizada limpa: o primeiro juiz reprovou `M-207/W-C` por considerar
  inventada a data 20/01/2025, embora ela conste literalmente no extrato do
  cenário; o mesmo transcript congelado passou no rejulgamento. A P0 começou e
  foi interrompida a pedido do owner após 8/36 PASS (`M-101` W-A/W-B/W-C,
  `M-102` W-A/W-B/W-C e `M-103` W-A/W-B); `M-103/W-C` não foi concluído.
  Antes do closeout, o delta de produto foi integralmente neutralizado: a
  evidência será preservada, mas a skill publicada não muda. Status:
  `CLOSED_NOT_PROMOTED`; não há prontidão de release.
  Recibo em
  `data/evals/2026-09-01-codex-skill-world-spec-p1-full-v1/ADJUDICATION.md`.
- Estado dos gates: `make lint` PASS; `make test` PASS (72); `make validate`
  PASS; `make test-release` PASS (13); `build_worlds.py check` PASS (P0 e
  P1); `build_batch.py check` PASS (P0 e P1). O `--list` da fixture P1 expõe
  36/36 cenários. Workflow de release PASS; GitHub Release final com oito
  ZIPs e `manifest.json`, todos com digest publicado.
- Material empírico privado em `~/Dev/Habilidades/procs-copias-drive/`
  (fora do repo): 254 PDFs de autos completos (173 processos), extrator
  (Projudi + Recurso + eproc), 162 casos estruturados, 103 pares
  cross-validados com o fs.brain (82% de concordância processual),
  anatomia por classe, estudo de uso probatório TJ×STJ (149.220 decisões
  servidas), spec P1 e dinâmica de leitura. Dado confidencial: alimenta
  calibração local; nunca publicar cru.

## Próximas tarefas fixadas (nesta ordem, salvo decisão do owner)

1. **Gate de valor da fábrica sintética: decidido em 2026-09-03.** Memorando
   em `data/research/2026-09-03-fabrica-sintetica-valor.md` (conselho
   registrado no ledger; Sol indisponível por franquia, K3 material). Decisão
   do owner: P0 e P1 viram régua de regressão com painel de 3 nos 9 cenários
   críticos e suíte completa só em release, sob teto de tokens; invariante 7
   da P1 registrado como defeito conhecido da v0.6.4; nenhuma família nova
   (SEN-2428, revisita em 2026-10-05); Receita C para o Valter em brainstorm
   próprio (SEN-2427). Franquia Codex esgotada até 2026-09-07 07:21: nenhuma
   rodada com backend Codex antes disso.
2. **Leitura comparada pelo owner (pendente, custo zero):** os dois memorandos
   congelados de `M-202/W-A` (skill publicada × candidato estrutural) e o
   caso cego foram copiados para `~/Desktop/leitura-m202-wa/` com rótulos
   cegos A/B e gabarito em arquivo separado. Se o owner preferir o candidato
   estrutural, concluir a regressão P0 (28 cenários) após 2026-09-07 e só
   então decidir promoção. Se equivalentes, o invariante 7 fica como
   diagnóstico.
2a. **Recibo de instalação no aplicativo do Claude (pendente, owner):**
   instalar o plugin completo pelo Cowork (`Customize → Plugins → Add
   marketplace → sensdiego/codigo-aberto → Install`), com os ZIPs como
   alternativa. Roteiro, pacotes `v0.6.4` (hashes conferidos) e caso de
   teste em `~/Desktop/plugin-silo-legal/` (fora do repo). O owner deve
   informar se o botão de marketplace apareceu na conta; esse recibo fecha o
   item em andamento da Fase 1 do ROADMAP.
2b. **Recibo de uso humano do plugin (pendente, sessão própria):** o owner usa
   o plugin no aplicativo num caso que não desenhou (caso do dogfood da
   deliberação em `data/dogfood/2026-08-31-pareado-deliberacao/caso/`, ou
   caso real sob protocolo de privacidade a definir). Não usar os mundos
   sintéticos para esse recibo. Veredito em cinco linhas entra no ROADMAP.
3. **Decisão de anúncio da camada deliberativa** — destravada pelo
   veredicto MANTÉM; depende só do owner (ROADMAP Fase 3, issue #22).
4. **Estacionadas (não reabrir sem decisão):** execução da camada
   probatória do cross-validation (âncoras factuais no texto dos autos);
   recorte só-cível do estudo Valter e associação com resultado; execução
   de skills sobre autos reais (exige protocolo de privacidade próprio).
5. **Governança (pendente de autorização do owner, registrado em
   2026-09-03):**
   - Linear: SEN-2384 (frente 2 da deliberação) segue "In Progress" apesar
     de superada por SEN-2408 (Done); SEN-2381 (guarda-chuva) não recebeu o
     estado de 2026-09-03. Reconciliar só com o ok do owner.
   - Dez branches locais já integradas em `main` continuam no checkout
     (`codex/SEN-2408-deliberacao-juridica`,
     `codex/SEN-2413-tutela-urgencia-evidencia`,
     `codex/baseline-briefing-gates`, `codex/closeout-v0.5.0`,
     `codex/closeout-v0.5.1`, `codex/closeout-v0.6.0`,
     `codex/closeout-v0.6.1`, `codex/handoff-stable-v0.6.1`,
     `codex/p1-evidence-linkage`,
     `codex/redacao-contencioso-cobertura-integral`). Deletar somente com
     autorização.
   - Sigilo: este HANDOFF menciona, em seções anteriores, o nome da pasta
     privada do Drive do escritório e caminhos locais da máquina do owner
     (material empírico e fs.brain). São nomes de pasta e contagens
     agregadas, sem partes ou números de processo, já presentes no
     histórico público. Remover ou manter é decisão do owner.
   - Conselho: o guard do agente `conselho-sol` não bloqueia a memória
     persistente do Codex; o owner decidiu em 2026-09-03 não corrigir agora
     e apenas aguardar a franquia. Franquia Codex esgotada até 2026-09-07
     07:21: `codex-exec`, `conselho-sol` e o backend Codex da régua ficam
     indisponíveis até lá.
   - Anúncio da camada deliberativa: continua dependendo só do owner (item
     3), agora condicionado pelo próprio ROADMAP ao recibo de uso humano.

## Estado do produto

A versão publicada é `v0.6.4` (tag imutável em `490936e`, oito bundles ZIP
e `manifest.json`). A adaptação da régua está incluída; as skills distribuídas
permanecem byte a byte iguais à `v0.6.3`. A rodada P1 e seus candidatos ficam
preservados como evidência histórica, sem alteração líquida nas skills. O
candidato estrutural produziu passagem P1 adjudicada, mas sua regressão P0
ficou incompleta e, por isso, não foi promovido.

## Sessão de 2026-09-03 — o que foi entregue

- **Gate de valor da fábrica sintética:** memorando com a explicação da
  construção (cadeia ficha oculta → renderer → mundos cegos → gabarito →
  rubrica → juiz), contagens, custo real (≈ US$ 13,50 externos e ≈ 15 M
  tokens de franquia Codex, um achado promovido ao produto), diagnóstico da
  deriva de objetivo, análise de usos e opções. Conselho convocado: Sol
  falhou por franquia esgotada; K3 devolveu contribuição material (suíte P1
  vermelha sobre a skill publicada; dogfood nos mundos não prova valor;
  custo por achado). Decisões do owner: régua de regressão com painel e
  defeito conhecido; leitura comparada; uso humano em caso não desenhado;
  Receita C no Valter (SEN-2427); standby com revisita (SEN-2428); nenhuma
  família nova; guard do Sol não alterado.
- **Material para o owner (fora do repo):** `~/Desktop/leitura-m202-wa/`
  (memorandos A/B com rótulos cegos, caso cego e gabarito separado) e
  `~/Desktop/plugin-silo-legal/` (roteiro de instalação, oito ZIPs da
  `v0.6.4` com hashes conferidos, caso de teste do dogfood).
- **Documentação pública:** QUICKSTART e README com o caminho do plugin
  completo no aplicativo do Claude (marketplace por repositório), Claude Code
  e ChatGPT; README passa a descrever `data/` e os documentos de engenharia
  e a regra de que nada real entra no repo; RELEASING corrige para oito
  bundles. ROADMAP registra o gate de valor e o caminho de instalação
  documentado, com recibo pendente. PR #37 mergeado; fragmento `none`;
  nenhuma versão publicada.
- **Sem alteração de produto:** skills, referências e fixtures inalteradas.
  Nenhuma chamada paga de modelo; nenhuma rodada de avaliação.

## Sessão de 2026-09-01 — o que foi entregue

- **Dogfood pareado da deliberação executado** (adiado em 2026-08-31):
  braço A (salto direto, US$ 3,18) produziu minuta em 3 turnos com a
  decisão estratégica implícita e errada para o mandato; braço B
  (protocolo, US$ 2,34) produziu decisão materialmente diferente e
  endossada pela folha do advogado, com handoff de decisão e condição de
  reabertura. Gate recusou autorização combinada nos dois braços — o
  incidente de 2026-08-25 não se reproduziu. Veredicto MANTÉM no ROADMAP e
  na issue #22. Desvio registrado: operador foi um agente (Kimi) aplicando
  `contexto-advogado.md`, não Diego digitando.
- **Base empírica de autos completos:** pasta "PROCS E CÓPIAS" do Drive do
  escritório (265 PDFs, 173 processos únicos, TJPR/TJSC/TRF4/STJ/TRT).
  Download manual do owner após quota do Drive. Extrator determinístico
  (rodapé `PROJUDI - Processo:/Recurso:` e rodapé de evento eproc): 162 de
  176 processos estruturados em sequências de movimentos com datas, tipos e
  complementos; 14 fora de escopo por formato (PJe/TRT, TJSP avulso, STJ,
  TJCE, TJMG) — registrados.
- **Cross-validação autos × fs.brain:** pareamento por CNJ (o pareamento
  por número de pasta estava errado em 75/138 casos): 123 pares fortes,
  103 com timeline utilizável. 82% das entradas processuais da timeline do
  advogado verificadas nos autos (±7 dias); os 18% têm causa estrutural
  identificada, sem contradição factual genuína. Cobertura reversa de 37%:
  timelines humanas são curadorias — lição incorporada à fábrica.
- **Uso probatório TJ×STJ** (índice servido do Valter, acesso read-only
  via SSH no container, 149.220 decisões): TJ decide por documento
  (contrato em 59%) e moldura de ônus (27%); STJ discute a fronteira do
  reexame (48%). Insumo para o realismo probatório da fábrica.
- **Família P1 construída:** especificação aprovada pelo owner
  (`ESPEC-P1.md` no diretório privado), semente + lote implementados
  espelhando a arquitetura do P0, quatro rodadas de canário com 13
  defeitos corrigidos (2 de instrumento: calendário que negava feriado;
  citação causalmente impossível no modelo eletrônico), adjudicação
  completa e rodada final de coerência. Resíduos aceitos e documentados
  como convenção do fixture.
- **Dinâmica de leitura destilada** (`DINAMICA-LEITURA.md` privado):
  sete princípios empíricos para evolução futura das skills — insumo,
  nenhuma skill editada.

## Estado anterior (2026-08-31)

A sessão de 2026-08-31 encerrou com a `v0.6.2` publicada. O PR #27 foi
integrado a `main` pelo merge commit `0d9c04c`, preservando o commit `86a28eb`; o PR #28 foi integrado pelo merge
commit `7b6ecf0`, preservando toda a cadeia de avaliação; o PR #30 foi integrado
pelo merge commit `da41883`; e o PR #26 foi integrado pelo merge commit
`c47555a`. O PR #32 corrigiu o estado publicado no mapa visual pelo merge commit
`eb43e98`; o workflow `Software release` criou o commit `916db93`, a tag e o
GitHub Release `v0.6.1`. O push do lote P0 em `main` acionou o protocolo
automático do repositório; após a correção da allowlist pública em `b81735b`, o
workflow publicou `v0.6.2` no commit `a354700`.

A skill autônoma de deliberação foi incorporada sobre a baseline `v0.5.1` sem
reescrever a cadeia auditada. A rodada dirigida aprovou sete cenários e 31/31
invariantes. A regressão integral
congelada registrou 22 PASS / 8 FAIL, 30/30 primeiras rotas e nenhum gate
mecânico violado; a triagem encontrou cinco fixtures inelegíveis, um cenário
condicionado ao Silo e dois bugs de baseline. Esses dois bugs foram corrigidos
na `v0.5.1` e reexecutados em 2/2 cenários, elevando a leitura combinada dos
cenários elegíveis a 24/24, sem constituir uma nova passagem única dos 30.

O trabalho posterior à tutela e a skill deliberativa estão integrados e
publicados. A release contém os oito bundles de skills e o manifesto produzidos
pelo workflow; publicação, instalação e uso humano continuam sendo recibos
distintos.

## O que a etapa entrega

- 27 módulos novos em `redacao-contencioso`; o catálogo passa de 10 para 37
  módulos.
- Família prioritária: cumprimento de sentença, execução de título
  extrajudicial, liquidação, prova pericial, exibição, produção antecipada,
  IDPJ, agravo interno e acordo/homologação.
- Fila posterior: monitória, embargos de terceiro, ação rescisória, REsp/RE,
  exceção de pré-executividade, habilitação e crédito, inventário, consignação,
  exigir contas, possessórias, demarcação/divisão, dissolução parcial,
  oposição, ações de família, penhor legal, avaria grossa e restauração.
- Procedimentos de jurisdição voluntária dos arts. 719–770 cobertos em módulo
  único com treze modos obrigatórios: geral, notificação/interpelação,
  alienação, família consensual, alteração de regime, testamento/codicilo,
  herança jacente, ausência, coisa vaga, interdição, tutela/curatela, fundação
  e protesto marítimo.
- `indice-modulos.md` organiza o roteamento por fase e preserva um único
  módulo-base; tutela continua sendo o único complemento cumulativo.
- Dez fixtures acrescentam cobertura para as famílias novas e o gate de
  confirmação. A primeira execução encontrou quatro PASS e seis FAIL: quatro
  conflitos de fixture e dois bugs de baseline. Agravo interno e interdição
  foram corrigidos e reexecutados com subagentes Codex: 2/2 cenários, 6/6
  invariantes e zero leitura prematura de módulo. As quatro fixtures restantes
  continuam inelegíveis para medir comportamento.
- `references/mapa-visual-skills-modulos.md` representa as dez skills
  publicadas, seus handoffs e gates, os
  modos não contenciosos e os 37 módulos contenciosos. O mapa é estritamente
  descritivo e não simula workflows prováveis.
- `references/validacao-casos-reais.md` confronta os contratos públicos com 14
  cenários reais anonimizados, registra a fronteira da prova e prioriza as
  lacunas sem incorporar dado identificador do corpus privado.
- `RFC-CA-001-adaptacao-casos-reais.md` adota adaptador versionado, intake
  obrigatório, análise documental condicionada, perfil de frentes, precedência
  temporal, despachante de escopo e critérios sintéticos A01–A14. A RFC foi
  aceita; as Fases 1 e 3 e a validação local da Fase 5 foram concluídas. A
  comparação externa, as Fases 2 e 4 e o dogfood não foram autorizados.
- `novo-caso`, `analise-documental`, `analise-juridica-civel` e
  `redacao-contencioso` consomem o pacote v1 conforme sua etapa. O estado de
  escopo agora pertence a cada frente; handoffs comuns continuam compatíveis.
- `adaptacao-workflows.json` referencia A01–A14 sem duplicar as 20 frentes. O
  runner materializa pacotes sintéticos completos, cobre os quatro consumidores
  e mantém A01–A04 como canário separado da rodada integral.
- A rodada comportamental R2 teve primeira passagem 13/14. A03 usou a lente
  defensiva correta, mas não declarou a validação do pacote; `novo-caso` foi
  corrigida sem mudar fixture, invariantes ou input, e a regressão com executor
  e juiz novos passou. O estado efetivo é 14/14, sem alegação de passagem única
  perfeita. A rodada anterior foi invalidada por associação posicional de
  fatos, achados e frentes.

## Resultado da validação com casos reais

A infraestrutura não sustenta ainda uma promessa de cobertura integral. O
núcleo de redação cível tem encaixe material forte, mas nenhum cenário provou o
fluxo completo desde a fonte real até uma minuta confirmada.

A amostra estratificada produziu quatro cenários válidos com extensão, dois
inconsistentes na integração, dois não validáveis por falta de evento atual e
seis fora do escopo end-to-end. Esses números não são taxa de sucesso: a
amostra foi escolhida por variedade e dificuldade, não por frequência.

As causas prioritárias são:

1. ausência de adaptador do estado do caso para o handoff público;
2. ausência de roteador explícito de frente e ato atual;
3. falta de precedência temporal e resolução de conflito entre artefatos;
4. ausência de recibo end-to-end;
5. regimes tributário/público especial, fiscal, trabalhista, criminal,
   fiduciário e de precatórios fora do contrato cível vigente.

As Fases 1 e 3 implementaram contrato, régua e consumidores locais:
`references/handoff.md` recebeu elegibilidade e perfil opcional de frentes;
`adaptacao-casos-reais.json` contém A01–A14 sintéticos com escopo por frente; o
validador reprova promoções, remoção das cláusulas consumidoras e roteamentos
inseguros. Não existe produtor neste repositório e nenhum outro workspace foi
alterado.

## Biblioteca legislativa

Seis recortes novos armazenam 235 artigos integrais selecionados:

- `incidentes-e-provas.md`;
- `cumprimento-e-execucao.md`;
- `procedimentos-especiais.md`;
- `inventario-partilha.md`;
- `jurisdicao-voluntaria.md`;
- `recursos-avancados.md`.

Os 235 artigos foram comparados mecanicamente, sem divergência, com nova leitura
do HTML compilado oficial do Planalto em 2026-08-30, excluindo notas editoriais
e redações revogadas conforme a regra declarada do corpus. O manifesto agora
contém 869 IDs únicos; todas as 378 referências usadas pelas skills resolvem.
Essa conferência não equivale, isoladamente, a certidão de vigência nem substitui
lei material, regimento ou jurisprudência exigidos pelo caso.

## Decisões de escopo

- Cumprimento cobre os arts. 513–538; o recorte anterior 523–541 foi corrigido,
  pois o art. 539 inicia consignação em pagamento.
- Credor e devedor começam como modos rígidos dentro das famílias de
  cumprimento e execução. Extração futura para módulos separados depende de
  falha observada, não de antecipação arquitetural.
- Jurisdição voluntária usa um módulo com modos, evitando onze arquivos com o
  mesmo contrato-base.
- Cálculo/atualização monetária e relógio processual não foram disfarçados como
  redação: permanecem fora de escopo até existir mecanismo reproduzível próprio.
- Exceção de pré-executividade bloqueia redação sem prova pré-constituída e
  pesquisa jurisprudencial atual do tribunal competente.
- Procedimentos sujeitos a legislação material ou extravagante exigem que essa
  fonte seja carregada antes de qualquer minuta; o novo corpus é apenas CPC.

## Histórico local

- `3c753a0` — base normativa e módulos prioritários;
- `d7ce8ab` — procedimentos especiais e roteamento completo;
- `d21c7b9` — checks, fixtures e fechamento da cobertura de redação;
- `9168d63` — mapa visual de skills, módulos e modos;
- `8c255e5` — checkpoint local das Fases 1 e 3 da adaptação;
- `10d7337` — primeira avaliação comportamental, depois invalidada pela revisão;
- `387c32f` — correções do materializador, gates e manifesto de inputs;
- `4f11742` — outputs cegos A01–A14 congelados antes do julgamento;
- `ff2a210` — julgamento independente da primeira passagem, 13/14;
- `267bfc8` — validação do pacote tornada explícita em `novo-caso`;
- `de028ce` — output cego da regressão A03;
- `252a917` — julgamento independente da regressão A03, PASS;
- `3f2265a` — relatório R2 e documentação de fechamento.
- `babdfba` — sincronização com `main` após o landing e a release automática da
  tutela, sem reescrita da cadeia.
- `7b6ecf0` — merge do PR #28, sem rebase ou squash;
- `632fa21` — release `v0.5.0` e consumo dos sete fragmentos.
- `da41883` — merge do PR #30, com os gates de briefing corrigidos;
- `f2e99ba` — release `v0.5.1` e consumo do fragmento `patch`.
- `c47555a` — merge do PR #26, com a skill deliberativa e seus recibos;
- `e070f83` — release `v0.6.0` e consumo do fragmento `minor`.
- `eb43e98` — merge do PR #32, com o closeout e o mapa visual corrigido;
- `916db93` — release `v0.6.1` e consumo do fragmento `patch`;
- `7c38285` — preparação do dogfood pareado da deliberação (branch
  `dogfood/pareado-deliberacao`, fragmento `none`), execução adiada.
- `42eb0de` — fábrica sintética, lote P0 congelado, recibos completos, backend
  Codex, integridade do juiz e correção geral de cobertura normativa.
- `b81735b` — reconhece `.gitattributes` na estrutura pública sem alterar os
  bytes ou hashes do corpus congelado.
- `a354700` — release automática `v0.6.2`, consumo dos fragments e publicação
  dos oito bundles mais `manifest.json`.

## Verificação

- extração oficial: 235/235 artigos sem divergência;
- módulos: 37/37 com as seis seções contratuais;
- manifesto: 869 IDs únicos, nenhuma referência ausente;
- `make validate`: PASS;
- `make lint`: PASS;
- `make test`: PASS — 71 testes.
- `make test-release`: PASS — 13 testes.
- `git diff --check`: PASS.
- release: tag imutável `v0.6.2` em `a354700`; oito bundles ZIP e
  `manifest.json` publicados pelo workflow `Software release`.

Os comandos foram repetidos antes do landing do PR #26. O workflow de release
passou e publicou oito ZIPs e `manifest.json` a partir de `e070f83`.

## Limites e recibos negativos

- A01–A14 e a regressão A03 foram executados com subagentes Codex; não houve
  chamada de modelo externo, dogfood ou recibo de custo em dólares. Houve
  consumo não medido da franquia Codex.
- Custo medido nos quatro relatórios anteriores: medianas por cenário entre
  US$ 0,28 e US$ 0,65; máximo de US$ 1,19. Estimativa não executada no executor
  externo: US$ 2–5 para A01–A04 e US$ 8–17 para A01–A14.
- Esta etapa não escreveu em outro workspace. A análise anterior do corpus
  privado permaneceu somente como evidência de origem anonimizada.
- Nenhum nome, número processual, valor, documento ou trecho identificador de
  caso real foi incorporado ao `codigo-aberto`.
- Não houve pesquisa jurisprudencial nova.
- Os PRs #27, #28, #30, #26 e #32 foram integrados; seus workflows publicaram
  `v0.4.0`, `v0.5.0`, `v0.5.1`, `v0.6.0` e `v0.6.1`, respectivamente.
- A publicação `v0.6.1` contém oito bundles ZIP e um manifesto. Não houve
  instalação das skills, dogfood, uso humano ou anúncio externo.
- A publicação automática `v0.6.2` substitui `v0.6.1` como versão corrente; a
  release não prova instalação, uso humano, dogfood ou anúncio.
- A nova medição do PR #26 usou apenas subagentes Codex e cenários sintéticos.
  Ela comprova o comportamento dirigido, mas não dogfood, uso humano ou
  aprendizagem em caso real.
- A rodada dirigida dos dois gates usou subagentes Codex e cenários sintéticos;
  não houve modelo externo, dogfood, uso humano ou custo medido em dólares.
- A leitura combinada de 24/24 cenários elegíveis agrega duas rodadas; cinco
  fixtures continuam materialmente inelegíveis e um cenário depende de um job
  com conector Silo autenticado.

## Dogfood pareado da camada deliberativa — preparado e adiado

Preparação concluída em 2026-08-31 na branch `dogfood/pareado-deliberacao`
(commit `7c38285`), execução adiada por decisão do owner na mesma data. O
material está pronto para retomada sem retrabalho:

- `data/dogfood/2026-08-31-pareado-deliberacao/protocolo.md` — dois braços na
  v0.6.1 (salto direto × protocolo deliberativo), ordem fixa A→B, métricas do
  ROADMAP e veredicto mantém/redesenha/remove;
- `caso/CASO.md` — caso sintético novo (cumprimento de sentença contra
  fornecedora exclusiva em aperto financeiro, com proposta de acordo ruim);
- `contexto-advogado.md` — folha privada do operador; nunca copiar para o
  diretório das sessões;
- `registro-sessao-a.md` e `registro-sessao-b.md` — templates de medição;
- diretórios de execução criados em
  `~/Dev/Habilidades/dogfood-sessoes-2026-08-31/sessao-{a,b}/` com cópias do
  caso;
- plugin local atualizado de 0.2.4 para 0.6.1 (`claude plugin update
  silo-legal@codigo-aberto`), dez skills no cache, incluindo
  `deliberacao-juridica` — primeiro recibo de instalação da versão corrente.

O dogfood continua sendo o critério de manutenção declarado da porta
deliberativa antes de qualquer anúncio (ROADMAP, Fase 3; issue #22).

## Dossiê Harvey — investigação estática executada

A análise foi produzida em
`data/research/2026-08-31-harvey-benchmarks-e-equivalente-brasileiro.md` e
reaberta no mesmo dia depois que o owner identificou corretamente que o ponto
central da palestra de Gabe Pereyra não era apenas o benchmark publicado, mas a
capacidade de gerar datasets sintéticos para avaliar e treinar o produto.

A versão corrigida conclui:

- o ativo investigável é a cadeia `world_spec → documentos → proveniência →
  gabarito → rubrica`, não o contrato final de uma tarefa isolada;
- a Harvey publicou três receitas complementares: rubrica primeiro em
  Diligence, especificação primeiro em Firm Knowledge e distribuição do produto
  primeiro em Review Table;
- o repositório público contém mundos renderizados e harness, mas não expõe o
  gerador, seus prompts, specs latentes, custos ou protocolo integral de QA;
- a primeira contagem usou uma árvore Git marcada como truncada. A recontagem
  por subárvores não truncadas preservou 2.010 tarefas e corrigiu o total para
  60.979 documentos e 3.206.967.747 bytes; Firm Knowledge possui 9.288
  arquivos, não 504;
- o piloto manual de um assunto e três tarefas foi retirado: ele provaria o
  consumidor local, não uma fábrica de datasets.

Após autorização do owner, a investigação foi executada em
`data/research/2026-08-31-world-spec-p0/`, fora do harness. Um único
`world_spec.json` e um renderer/compiler/validator em biblioteca padrão geram
três pastas cegas opacas com o mesmo inventário de 17 documentos. O revisor não
recebe os rótulos semânticos.

O build e o check separados passam. A prova cobre fontes e âncoras locais do
CPC, referências, hashes, proveniência com localizadores `arquivo:linha`,
autoridade/classe/severidade das rubricas, ausência de IDs internos na view
cega e isolamento das mutações. Entre controle e prova ausente muda somente
`14-registro-bancario.md`; entre controle e cronologia controvertida muda
somente `12-certidao-publicacao.md`. A mutação de data atravessa a
tempestividade numa contagem mecânica apenas de dias úteis, sem alegar que isso
resolve o prazo jurídico concreto.

Estado do gate:
`STATIC_PASS / MODEL_BLIND_COMPLETE / CONSENSUS_CONSTRUIR_P0 /
OWNER_DIRECTED_BUILD`. O owner é advogado e esclareceu que não haverá entrega
a revisor jurídico externo. O protocolo em
`generated/blind/INSTRUCOES-REVISOR.md` permanece disponível como red-team
opcional, não como bloqueio da construção.

O primeiro transporte testado, Claude Code, foi rejeitado: o tool server-side
`advisor` contaminou os dois braços. O recibo Sonnet registrou Sonnet 5, Opus 5
e Haiku 4.5, enquanto o recibo Opus registrou Opus 5 e Haiku 4.5. Esses
pareceres estão marcados como inválidos em `model-reviews/` e não entraram na
comparação. O custo comprovado desse histórico é US$ 2,93889375; quatro
inferências antigas sem recibo podem ter acrescentado até US$ 16,00 pelos tetos
configurados.

A primeira rodada defensável pela Messages API direta preservou dois pareceres
puros e convergentes em `REDESENHAR`. Ela encontrou o salto estrutural de 13
para 15 em W-B e linguagem metatextual nos documentos. O par custou
US$ 0,662561.

O corpus foi redesenhado antes da nova escalada: W-B passou a substituir o
conteúdo de `14-registro-bancario.md` por resposta negativa de busca, sem
retirar arquivo; a data dominical foi corrigida; o calendário forense foi
materializado; e as autoexplicações probatórias foram removidas. Uma triagem
Sonnet na revisão 2 recuperou os mundos, mas ainda propôs `REDESENHAR` por
pistas no aviso, demonstrativo, extrato e janela exata do calendário. Essa
chamada custou US$ 0,295094.

A revisão 3 removeu o aviso de `documents/`, eliminou o fechamento artificial
do demonstrativo, transformou o extrato em consulta datada e generalizou o
calendário para março inteiro. Depois de build, check, validação, lint e testes,
um novo Sonnet recebeu a revisão 3 e propôs `CONSTRUIR P0`; somente então um
Opus isolado recebeu o mesmo prompt e também propôs `CONSTRUIR P0`.

O par final usou 55 arquivos, 30.411 bytes e SHA-256
`4e9acc204019951c4462d3f51bbacc6c4ca6b2815376265b74ca47f3568c05d5`.
Sonnet custou US$ 0,223132 e Opus US$ 0,346955. Ambos retornaram apenas o modelo
solicitado, sem tools, sem retry e com `end_turn`. Os dois recuperaram W-A como
controle, W-B como pagamento alegado com busca bancária negativa de alcance
limitado e W-C como conflito entre 02/03 e 04/03, com termos possíveis em 23/03
e 25/03. Ambos atribuíram realismo 4/5 aos três mundos e não encontraram
vazamento de gabarito.

A sequência corretiva autorizada custou US$ 0,865181, abaixo do teto de US$ 2.
As cinco chamadas diretas válidas somam US$ 1,527742. Incluído o histórico
inválido com `advisor`, o custo comprovado total é US$ 4,46663575; os quatro
ensaios antigos sem recibo continuam apenas limitados pelo teto adicional de
US$ 16,00. Não foi criado placar ponderado post hoc.

O relatório reproduzível, os controles, hashes, recibos, pareceres e ressalvas
estão em `model-reviews/README.md`.

Depois de autorização expressa do owner, o `fs.brain` foi lido globalmente e
somente em modo read-only no commit
`b1d871d7e489a6dacc0a9b60f2bfc38f9ecc99a2`; sua worktree permaneceu limpa. O
censo registrou 259 casos, dos quais 237 estavam com ingestão liberada. A coorte
possui 8.520 Markdown associados, mas o extrator seleciona somente 7.852 notas
sob `source-documents`, evitando misturar fontes com manifestos, índices e
análises derivadas.

O relatório agregado contém 8.027 seções tipadas em 231 casos e 6.828
movimentações deduplicadas em 39 sequências de 37 casos. Apenas quatro casos
possuem alguma nota `full_autos`; portanto, o corpus sustenta com confiança alta
a topologia documental, com confiança moderada as transições de movimentação e
não sustenta a generalização de histórias processuais integrais.

Os artefatos novos estão em
`data/research/2026-08-31-fsbrain-patterns/`: `extract_patterns.py` produz e
verifica `pattern-report.json` sem serializar dado identificável; `README.md`
registra método, contagens, limites e o primeiro lote executado. O P0 recebeu
`empirical-basis.json`; `build_worlds.py check` agora falha se commit, cobertura
ou os cinco suportes estruturais congelados divergirem do relatório.

A distribuição observada confirma `peticao → decisao` em 113 casos,
`decisao → certidao` em 132 e coocorrência `contrato + peticao` em 102. Na
subcoorte de movimentações, `peticao_manifestacao → decisao` aparece em 29 dos
37 casos e `despacho → citacao_intimacao`, em 22. Isso confirma a espinha da
revisão 3 sem copiar fatos de qualquer caso real.

O lote `br-civel-cumprimento-calibrado-v1` foi materializado por
`batch-spec.json` e `build_batch.py`: doze assuntos-base, quatro motivos
estruturais, três mundos por assunto, 17 documentos por mundo e 612 documentos
no total. Os 805 arquivos incluem as views cegas, 12 specs efetivos, fatos
resolvidos, proveniência, rubricas e manifestos. Os assuntos variam partes,
objeto, valores, juízo e identificador; doze deslocamentos semanais únicos entre
zero e 21 semanas variam as datas de março a agosto sem perder a relação de
tempestividade revisada. O build recusa fechamentos forenses conhecidos nas
janelas de prazo.

`build_batch.py check` reconstruiu o lote em diretório temporário e confirmou
igualdade determinística. O canário cego por agentes selecionou `M-101`,
`M-105`, `M-108` e `M-111`, um assunto por motivo. V1 falhou por contradição no
harness; v2 recuperou toda a semântica, mas Opus encontrou feriados nas janelas
de M-105/M-108 e um ofício híbrido; o spec e o renderer foram corrigidos e o
lote regenerado. Na v3, Sonnet 5 e Opus 5 deram `CONSTRUIR` ao lote e aos quatro
assuntos. O adjudicador registrou 12/12 mundos, 16/16 observações críticas e 8/8
relevantes por modelo, sem falso positivo crítico. Os hashes dos 216 arquivos
cegos por recibo e das 28 fontes de adjudicação foram reconferidos.

O estado é `STATIC_PASS / AGENT_FULL_BATCH_PASS / 36_OF_36_WORLDS /
CODEX_SKILL_BACKED_FULL_PASS`. Os recibos estáticos estão em
`batch-model-reviews/`; o v3 custou US$ 1,172326 e as seis chamadas
válidas do canário, US$ 3,368367. Sem nova chamada externa, os oito assuntos
restantes foram divididos nos pacotes A (`M-102`, `M-106`, `M-109`, `M-112`) e
B (`M-103`, `M-104`, `M-107`, `M-110`). Em cada pacote, dois subagentes Codex
receberam 216 arquivos cegos e um terceiro adjudicou as respostas congeladas.
Cada pacote aprovou 12/12 mundos; cada revisor recuperou 16/16 observações
críticas e 8/8 relevantes, sem parcial, omissão ou falso positivo crítico. O
operador raiz reconferiu os hashes e evidências. O custo externo desses dois
pacotes foi US$ 0. A mesma família Codex nos oito assuntos limita diversidade de
fornecedor, mas não o isolamento processual.

Os 12 assuntos foram adaptados ao executor em
`tests/fixtures/world-spec-p0-workflows.json`. O novo schema
`synthetic-world-workflows-v1` congela o manifesto e os três recibos por hash;
`scripts/run_evals.py` valida a aprovação integral e materializa 36 cenários em
diretórios temporários, cada um com `task.md`, 17 documentos cegos e sete
invariantes da rubrica. A listagem retornou 36/36 cenários para
`analise-juridica-civel`. O backend Codex executa e julga em chamadas efêmeras,
separadas e somente leitura; pode fornecer a skill e suas referências no
diretório cego, mas não testa o roteamento automático do plugin. O runner passou
em 35 testes focados, persiste executor e juiz, reaproveita recibos com
`--resume`, permite `--rejudge` e interrompe com `--fail-fast`.

O baseline bruto revelou a omissão do art. 524 em `M-101/W-B`. Com a skill
fornecida, o canário M-101 passou 21/21. No lote integral, `M-105/W-A` expôs a
mesma omissão de forma legítima; a skill recebeu uma regra geral para reconciliar
todo dispositivo material da fonte autorizada, sem citar o dataset ou o art.
524, e o cenário passou na reexecução. `M-110/W-C` produziu memorando correto,
mas o juiz retornou apenas 3/7 itens; o runner passou a classificar veredito
incompleto como `JUDGE_ERROR`, preservou a resposta inválida e o rejulgamento do
mesmo transcript congelado passou 7/7.

O recibo canônico está em
`data/evals/2026-08-31-codex-skill-world-spec-p0-full-v1/report.json`: 36/36
mundos e 252/252 invariantes, custo externo US$ 0. A franquia Codex registrou
4.150.622 tokens de entrada dos executores e 666.345 dos juízes; 3.416.320
tokens de entrada foram reaproveitados em cache. Todos os comandos dos agentes
foram auditados: nenhuma leitura de `authority/`, rubrica ou gabarito e nenhuma
chamada de rede. O resultado prova esta família e esta configuração, não
generalização jurídica ampla nem roteamento automático.

Continuam sem autorização: dataset público, SEN-1746, nova release, dogfood,
anúncio e novas execuções pagas. A construção local do P0 e sua adaptação ao
`scripts/run_evals.py` não transformam o artefato em capacidade publicada.

## Comandos de retomada

```bash
git fetch origin main
git switch main
git pull --ff-only origin main
git status --short --branch
git log --oneline --decorate -6
make validate
make lint
make test
make test-release
git diff --check
python3 scripts/release.py impact --ref-range origin/main...HEAD
python3 scripts/release.py plan
uv run --project /Users/sensdiego/Dev/fs.brain \
  python -B data/research/2026-08-31-fsbrain-patterns/extract_patterns.py check \
  --fsbrain-root /Users/sensdiego/Dev/fs.brain
python3 data/research/2026-08-31-world-spec-p0/build_worlds.py check
python3 -B data/research/2026-08-31-world-spec-p0/build_batch.py check
python3 -B data/research/2026-08-31-world-spec-p0/run_batch_canary_review.py --check
jq -e '.status == "PASS" and ([.worlds[].pass] | all)' \
  data/research/2026-08-31-world-spec-p0/batch-model-reviews/canary-adjudication-v3.json
jq -e '.status == "PASS" and ([.worlds[].pass] | all)' \
  data/research/2026-08-31-world-spec-p0/batch-model-reviews/codex-remaining-a-adjudication-v1.json
jq -e '.status == "PASS" and ([.worlds[].pass] | all)' \
  data/research/2026-08-31-world-spec-p0/batch-model-reviews/codex-remaining-b-adjudication-v1.json
python3 scripts/run_evals.py --fixture tests/fixtures/adaptacao-workflows.json --list
python3 scripts/run_evals.py \
  --fixture tests/fixtures/world-spec-p0-workflows.json --list
jq -e '
  .counts == {"total":36,"PASS":36,"FAIL":0,"JUDGE_ERROR":0}
  and ([.scenarios[].invariants[].atendido] | all)
' \
  data/evals/2026-08-31-codex-skill-world-spec-p0-full-v1/report.json
python3 data/research/2026-09-01-world-spec-p1/build_worlds.py check
python3 -B data/research/2026-09-01-world-spec-p1/build_batch.py check
jq -e '.status == "PASS" and ([.worlds[].pass] | all)' \
  data/research/2026-09-01-world-spec-p1/batch-model-reviews/kimi-remaining-a-adjudication-v1.json
jq -e '.status == "PASS" and ([.worlds[].pass] | all)' \
  data/research/2026-09-01-world-spec-p1/batch-model-reviews/kimi-remaining-b-adjudication-v1.json
jq -e '.status == "PASS" and ([.worlds[].pass] | all)' \
  data/research/2026-09-01-world-spec-p1/batch-model-reviews/kimi-rereview-adjudication-v1.json
```

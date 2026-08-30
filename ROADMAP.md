# Roadmap

Plano de desenvolvimento do plugin `silo-legal`. O roadmap é vivo: itens mudam
de estado conforme o trabalho avança, mas decisões registradas aqui não são
apagadas — itens descartados movem-se para [Fora de escopo](#fora-de-escopo).

Estado dos itens:

- `[ ]` pendente;
- `[~]` em andamento;
- `[x]` concluído.

## Estado atual (2026-08-30, v0.5.1)

- Nove skills publicadas, com disciplina compartilhada, contrato de handoff e
  recorte versionado do CPC. Versão corrente `v0.5.1`, publicada em 2026-08-30
  com os controles pré-briefing de agravo interno e interdição.
- Protocolo de release validado ponta a ponta: fragmentos, semver, tag imutável,
  GitHub Release e publicação idempotente de assets (nove GitHub Releases
  publicadas, todas finais).
- Sete bundles ChatGPT e o manifesto de checksums publicados na
  [release v0.5.1](https://github.com/sensdiego/codigo-aberto/releases/tag/v0.5.1).
  O último recibo de atualização do acervo do projeto de smoke no ChatGPT é da
  v0.2.4, em 2026-08-24; release publicada não prova atualização do projeto.
- Smoke completo do Claude Code aprovado em 2026-08-24
  ([#9](https://github.com/sensdiego/codigo-aberto/issues/9)): instalação limpa
  da `v0.2.3` via marketplace, nove skills carregadas, roteamento correto e
  leitura das referências compartilhadas sem negação de permissão.
- Sete bundles ChatGPT comprovados no aplicativo: três smokes in-app de
  2026-08-22 e os quatro restantes aprovados in-app em 2026-08-24 com os ZIPs
  exatos da release v0.2.3 (checksum conferido dentro do app), 12/12
  invariantes, além do proxy CLI com `gpt-5.6`
  ([#11](https://github.com/sensdiego/codigo-aberto/issues/11)).
- Mecânica real do ChatGPT documentada: não há instalação de skills de
  terceiros no runtime; o modelo monta o ZIP anexado à conversa e segue o
  `SKILL.md` ([QUICKSTART](QUICKSTART.md) corrigido).
- Régua de qualidade operacional e primeiro ciclo editar→medir concluído:
  `scripts/run_evals.py` executa os dezenove cenários de
  [`tests/fixtures/workflows.json`](tests/fixtures/workflows.json) contra o
  plugin instalado, com juiz por invariante e relatório versionado. Baseline
  v0.2.3: 10 PASS, 3 FAIL. As três falhas foram corrigidas (v0.2.4: roteamento
  jurisprudencial e rótulos canônicos do delta; harness semeia estado prévio) e
  re-medidas em duas rodadas: zero falhas de roteamento em seis execuções
  ([#15](https://github.com/sensdiego/codigo-aberto/issues/15), fechada).
- Fluxo de menor atrito no ChatGPT comprovado: instruções permanentes de
  projeto fazem o modelo rotear e montar a skill certa do acervo sem o usuário
  citá-la ([QUICKSTART](QUICKSTART.md)).
- Dogfood interno manual no Claude Cowork executado em projeto com o acervo
  completo. O exercício comprovou o caminho operacional, mas não uma instalação
  limpa nem adoção externa. Também revelou dois achados de produto: gates
  críticos precisam de confirmação inequívoca e há uma lacuna deliberativa
  entre receber a análise e autorizar a redação.
- Validação estrutural anonimizada contra 14 classes de situações documentadas
  em casos reais concluída em 2026-08-30. O núcleo cível mostrou encaixe, mas
  nenhum cenário provou o fluxo end-to-end; a
  [RFC-CA-001](RFC-CA-001-adaptacao-casos-reais.md) adota adaptador versionado,
  perfil de frentes, precedência temporal e despachante de escopo. Status:
  aceita; Fases 1 e 3 e validação local A01–A14 da Fase 5 concluídas no
  `codigo-aberto`; comparação externa, Fases 2 e 4 e dogfood não autorizados.
- Camada deliberativa inicialmente decidida em 2026-08-26 como adaptação dos
  contratos. Duas rodadas acionaram a cláusula de promoção por falha repetida
  de roteamento; a frente 3 implementou e validou a skill autônoma sobre o
  mesmo protocolo e handoff.
- A cláusula de promoção da camada deliberativa disparou após duas rodadas. A
  skill autônoma foi implementada no PR #26 e sincronizada com a `v0.5.1`. Os
  conflitos Git foram resolvidos e a medição dirigida R3 passou 7/7, com 31/31
  invariantes. A regressão integral registrou 22 PASS / 8 FAIL; a triagem
  encontrou zero defeitos específicos da PR. Os dois defeitos reais da baseline
  foram corrigidos e reexecutados 2/2 na v0.5.1: a leitura combinada fica em
  24/24 cenários elegíveis, sem fingir uma nova passagem única dos 30. Restam
  cinco fixtures inelegíveis e uma limitação de ambiente sem Silo. O PR ainda
  não foi integrado nem publicado.
- Régua da camada deliberativa entregue em 2026-08-27 (frente 1 de #22): o
  harness roda cenários multi-turno na mesma sessão e reprova mecanicamente a
  leitura de módulo de redação antes da fala autorizadora; seis cenários novos e
  um invariante novo. Baseline da lacuna sobre a v0.2.4: 1 PASS, 6 FAIL,
  US$ 3,61 ([relatório](data/evals/2026-08-27-claude-sonnet-v0.2.4/report.md)).
  O defeito do dogfood ficou reproduzível: resposta a item aberto com "pode
  redigir" na mesma mensagem levou o modelo a ler o módulo e entregar a
  contestação inteira; a resposta isolada, ao contrário, foi tratada
  corretamente. Os três cenários de deliberação reprovaram por roteamento (dois
  caíram em `aprofundamento-juridico`, um em `redacao-contencioso`), a família
  de confusão que a frente 2 endereça.

## Princípios de ordenação

1. Provar o caminho do usuário antes de anunciar; release não comprova
   instalação.
2. Medir qualidade antes de expandir conteúdo; editar skill sem régua é no
   escuro.
3. Toda fase entrega valor isoladamente; nada depende de fase posterior.
4. Mudanças de produto seguem o [protocolo de release](RELEASING.md) com
   fragmento por PR.

## Fase 0 — Higiene e papercuts

Objetivo: eliminar atrito local que já demonstrou quebrar o fluxo de trabalho.

- [x] Tratar arquivos de sistema operacional no validador: `validate_skills.py`
      deve ignorar `.DS_Store`, `Thumbs.db` e equivalentes em qualquer pasta,
      em vez de falhar com "entrada não prevista". O gerador de bundles também
      os exclui, em vez de empacotá-los silenciosamente.
      Critério atendido: `make validate` passa com arquivos de sistema
      plantados; cobertura em `tests/test_validate_skills.py`.
- [x] Remover o `.DS_Store` existente na raiz do workspace local.
- [x] Adicionar target `make lint` executando `ruff check scripts tests`.
      Critério atendido: o CI de qualidade roda lint antes da validação, e
      `make test` executa toda a suíte local.

## Fase 1 — Provar o caminho do usuário

Objetivo: fechar o ciclo aberto pela v0.2.0 — garantir que um usuário real
consegue instalar e usar as skills nos aplicativos suportados.

- [x] Smoke test no Claude Code: instalar via marketplace
      (`/plugin marketplace add sensdiego/codigo-aberto`) e confirmar que as
      nove skills carregam, roteiam e leem as referências compartilhadas.
      Critério atendido em 2026-08-24 com o cenário
      `relogio-completo-condicionado`: roteamento correto, seis leituras de
      referência sem negação de permissão e os três invariantes respeitados.
      Resultado registrado em
      [#9](https://github.com/sensdiego/codigo-aberto/issues/9).
- [x] Smoke test no ChatGPT Work: subir os sete bundles de `dist/` e repetir
      dois ou três cenários de `workflows.json` manualmente.
      Critério atendido em 2026-08-24: os quatro bundles restantes rodaram
      in-app com os ZIPs da release v0.2.3 (SHA-256 conferido pelo próprio
      modelo contra o manifesto), 12/12 invariantes, somando-se aos três
      smokes de 2026-08-22. Achado registrado: o runtime não tem instalação
      de skills de terceiros; o fluxo comprovado é montar o ZIP anexado à
      conversa ([#11](https://github.com/sensdiego/codigo-aberto/issues/11)).
- [~] Reescrever a seção de instalação do [`QUICKSTART.md`](QUICKSTART.md) com
      passos concretos por aplicativo (Claude Code, Claude Cowork, ChatGPT
      Work), testados na prática. Claude Code e ChatGPT estão documentados com
      caminho comprovado (a seção do ChatGPT foi corrigida em 2026-08-24 para o
      fluxo real de montagem do ZIP anexado). No Claude Cowork, um dogfood
      interno manual em projeto já montado comprovou leitura do acervo e
      execução do fluxo, mas ainda falta documentar e testar o caminho limpo de
      preparação do projeto; por isso o item continua em andamento.
- [x] Anexar os bundles como artefatos da GitHub Release no
      [`software-release.yml`](.github/workflows/software-release.yml).
      Critério atendido: `gh release view v0.2.3` lista os sete ZIPs e o
      manifesto de checksums.

## Fase 2 — Avaliação de qualidade

Objetivo: transformar os cenários sintéticos em régua objetiva para qualquer
edição futura de skills.

- [x] Criar `scripts/run_evals.py`: executa cada cenário de
      `workflows.json` contra um modelo e verifica os invariantes declarados.
      Entregue em 2026-08-24: sessão headless do Claude Code com o plugin,
      roteamento verificado deterministicamente, juiz por invariante com
      evidência citada, transcripts persistidos antes do julgamento e
      `--resume` para retomar sem repagar execuções.
- [x] Relatório por cenário: passos observados, invariantes atendidos/violados
      e veredito binário; saída em `data/evals/` com data, modelo e versão.
      `report.json` e `report.md` incluem skills invocadas, referências lidas,
      custo por cenário (executor e juiz) e cobertura por skill.
- [x] Execução manual apenas (`workflow_dispatch` ou comando local), sem gate
      automático no CI, controlando custo. Comando local documentado no
      CONTRIBUTING; rodada completa custou US$ 5,73.
- [x] Baseline registrado para as nove skills na versão corrente.
      Registrado em 2026-08-24 sobre a v0.2.3, modelo sonnet: 10 PASS, 3 FAIL,
      0 erros de juiz, US$ 5,73
      ([relatório](data/evals/2026-08-24-claude-sonnet-v0.2.3/report.md)).
      Comparabilidade verificada em três cenários re-executados: dois vereditos
      estáveis (PASS/PASS e FAIL/FAIL) e uma variância conhecida
      (`silo-cobertura-insuficiente` alterna o roteamento entre `pesquisa-silo`
      e `analise-jurisprudencial`) — o achado é a instabilidade, registrada em
      issue com as demais falhas.
- [x] Documentar como interpretar e estender os cenários em
      [`CONTRIBUTING.md`](CONTRIBUTING.md). Seção "Cenários de avaliação"
      cobre estrutura, uso do harness, leitura dos vereditos e regra de não
      alterar skill e régua no mesmo pull request sem justificativa.

## Fase 3 — Expansão de conteúdo

Objetivo: cobrir as lacunas do workflow cível identificadas na análise,
usando o eval harness como pré-condição de qualidade.

Pré-requisito: Fase 2 concluída.

### Camada deliberativa entre análise e redação — skill autônoma em validação

Status: a decisão de 2026-08-26 foi adaptar os contratos existentes e medir
antes de promover uma nova porta. As duas rodadas da frente 2 falharam por
omissão ou roteamento e acionaram a cláusula de promoção de
[#22](https://github.com/sensdiego/codigo-aberto/issues/22). A frente 3 cria a
skill autônoma reaproveitando protocolo e handoff. A rodada dirigida R3 passou
7/7 depois que dois invariantes ambíguos foram corrigidos e os mesmos outputs
congelados foram rejulgados; a ponte com redação não apresenta bloqueio
comportamental reproduzível.

Problema observado: as skills de análise entregam conclusões e a redação pede
um briefing, mas nenhuma etapa é claramente responsável por apresentar ao
advogado o que a análise demonstrou, explicitar incertezas e alternativas e
conduzir a decisão estratégica antes de qualquer peça.

Fronteira fixada: essa função **não deve ser misturada com
`aprofundamento-juridico`**. Aprofundamento continua sendo uma operação
epistêmica — testar hipóteses, preencher lacunas, pesquisar, tensionar
argumentos e simular cenários. Deliberação é uma operação decisória: traduz uma
análise suficientemente madura em escolhas compreensíveis, entrevista o
advogado e registra uma decisão. Ela pode concluir pela necessidade de novo
aprofundamento e não pressupõe redação como destino.

Comportamento desejado, independentemente da forma de implementação:

1. apresentar conclusão, base probatória, nível de confiança, incertezas,
   principal contra-argumento e o que mudou com a análise;
2. mapear de duas a quatro opções reais *(ajustado em 2026-08-26: até quatro
   opções materialmente distintas, sem fabricar pluralidade quando só há uma
   viável)* — incluindo, quando aplicável, negociar, buscar mais documentos,
   aprofundar, aguardar ou não agir — com benefícios, riscos, reversibilidade,
   urgência, efeitos posteriores e informação ainda necessária;
3. formular recomendação própria, com confiança e melhor objeção à
   recomendação *(ajustado em 2026-08-26: a recomendação pode ser "não decidir
   ainda; obtenha X")*;
4. entrevistar o advogado iterativamente, com uma pergunta decisória de maior
   valor por vez, atualizando o mapa à luz das respostas *(ajustado em
   2026-08-26: uma por vez quando a resposta muda a próxima; perguntas
   independentes juntas; modo curto em urgência)*;
5. produzir um handoff de decisão com opções escolhidas, rejeitadas ou
   condicionais, razões, prioridades, concessões e proibições, pré-requisitos,
   escopo, pendências e próxima rota;
6. manter um gate separado: respostas durante a deliberação nunca autorizam
   silenciosamente a redação, que conserva briefing e confirmação próprios.

Alternativas comparadas em 2026-08-26 (detalhe em
[#22](https://github.com/sensdiego/codigo-aberto/issues/22)):

- skill autônoma `deliberacao-juridica` — rejeitada inicialmente: décima porta num
  pacote em que o usuário não conhece nomes, descrição concorrendo com análise
  jurídica e aprofundamento (a família de confusão que o baseline mediu) e, no
  ChatGPT, um oitavo ZIP a descobrir; promovida a experimento em 2026-08-30
  após a cláusula medida disparar, ainda sem aceitação;
- protocolo/handoff compartilhado sem nova skill — escolhido e entregue na
  v0.3.0; mantido como contrato da skill autônoma;
- ajuste apenas das skills existentes — rejeitada: concentra em uma skill o que
  nasce de qualquer análise e duplica texto;
- adiamento ou rejeição — rejeitada: corrige o incidente do gate, não a lacuna.

Especificação aprovada: gatilho enumerável (pedido explícito do advogado;
decisão humana pendente que a minuta consome; ato inferido fora das opções do
mapa); handoff de tipo `decisão` exigido só quando o gatilho dispara; gate
como máquina de estados com pergunta fechada ao fim do briefing (resposta a
item aberto, escolha de opção, "ok"/"prossiga" fora da pergunta e "sim, mas
altere" não autorizam; reapresentação compacta e nova confirmação); protocolo
carregado sob demanda em `references/deliberacao.md`; fronteira com
`aprofundamento-juridico` mantida (ele informa a decisão; a deliberação a
registra). Critério de manutenção: dogfood pareado (salto direto × protocolo)
antes de qualquer anúncio. Critério original preservado: a solução só se
mantém se melhorar uma decisão real em comparação com o salto direto para a
redação, continuar útil quando a decisão for não redigir e impedir que
briefing ou contexto sejam tratados como autorização implícita.

- [x] Frente 1 — régua antes das skills: `scripts/run_evals.py` com cenários
      multi-turno e verificação mecânica (nenhum módulo de redação lido antes
      da fala autorizadora); seis cenários novos
      (`deliberacao-nao-redigir`, `deliberacao-nao-agir-sob-pressao`,
      `deliberacao-entrevista-segundo-turno`,
      `redacao-sem-decisao-registrada`, `gate-resposta-nao-autoriza`,
      `gate-confirmacao-combinada`) e invariante novo em
      `manifestacao-concordancia`; rodar contra a v0.2.4 como baseline da
      lacuna. PR próprio.
      Concluída em 2026-08-27: baseline 1 PASS / 6 FAIL / US$ 3,61
      ([relatório](data/evals/2026-08-27-claude-sonnet-v0.2.4/report.md)).
      Gate mecânico reprovou `gate-confirmacao-combinada` (módulo lido no
      turno 2); `gate-resposta-nao-autoriza` passou 4/4; deliberação reprova
      primeiro por roteamento e, na skill errada, ainda cumpre parte do
      protocolo (5/5, 4/5, 2/6). Esta rodada mede a v0.2.4 sem protocolo e não
      conta para a cláusula de promoção.
- [x] Frente 2 — contratos (publicada na v0.3.0): `disciplina.md`
      (gatilho + gate), `handoff.md` (tipo `decisão`),
      `references/deliberacao.md`, ponteiros em `analise-juridica-civel`,
      `analise-jurisprudencial`, `aprofundamento-juridico`,
      `redacao-contencioso` e `redacao-consultivo`, description de
      `analise-juridica-civel` (com `aprofundamento-audiencia` como controle
      de confusão) e gerador de bundles (`REWRITES` + cópia). Re-medir contra
      a frente 1. PR próprio. PR #25 integrado em 2026-08-28.
- [x] Frente 3 — skill autônoma `deliberacao-juridica` (SEN-2408): porta
      própria sobre `references/deliberacao.md`, handoff `decisão`, oitavo
      bundle e roteamento das fixtures `deliberacao-*`. O PR #26 foi
      sincronizado com a `v0.5.1` e não tem mais conflitos Git. A medição
      dirigida R3 passou 7/7 e 31/31 invariantes; a regressão integral executou
      os 30 cenários, exigiu a primeira rota correta e não encontrou falha
      específica da frente deliberativa. Merge e publicação permanecem etapas
      separadas.
- [ ] Dogfood pareado antes de anúncio: mesmo caso sintético, salto direto ×
      protocolo, medindo decisões alteradas, lacunas descobertas, turnos e
      abandono.
- Cláusula de promoção: se em duas rodadas o protocolo falhar por omissão ou
  por roteamento, a skill autônoma passa a ser a recomendação — embrulhando
  protocolo e artefato já existentes.

- [x] Módulo `tutela-urgencia-evidencia` em `redacao-contencioso`
      (SEN-2413): complemento do ato-base, recorte integral dos CPC arts.
      294–311 e cenário multi-turno com gate mecânico, integrado e publicado
      antes da `v0.5.0`.
- [x] Módulo `cumprimento-sentenca`, corrigido para o recorte dos CPC arts.
      513–538, com modos promover, impugnar e responder à impugnação.
- [x] Módulo `execucao-titulo-extrajudicial`, com modos promover, embargar e
      responder aos embargos, além de módulo condicionado de exceção de
      pré-executividade.
- [x] Cobertura ampliada de redação: liquidação, prova pericial, exibição,
      produção antecipada, IDPJ, agravo interno, acordo, ação rescisória,
      recursos excepcionais, inventário e os procedimentos especiais
      contenciosos dos arts. 539–718.
- [x] Jurisdição voluntária dos arts. 719–770 coberta por módulo único com
      treze modos obrigatórios, evitando módulos redundantes por seção.
- [x] Cobertura do `manifest.json` revisada: 235 artigos novos resolvem para
      seis recortes temáticos conferidos contra o HTML compilado oficial em
      2026-08-30; o validador garante IDs e âncoras.
- [x] Cálculo/atualização monetária e relógio processual não entram como
      módulos de redação. Continuam dependentes de capacidade verificável
      própria antes de eventual implementação.
- [x] Por decisão do owner em 2026-08-30, a implementação posterior à tutela
      foi consolidada em branch local única com fragmento `minor`; formato de
      integração e eventual divisão em PRs ficam para instrução posterior.
- [ ] Dogfood dos módulos ampliados: adiado expressamente pelo owner; fixtures
      e checks estruturais foram adicionados sem chamadas pagas a modelo.
- [x] Expor no índice público os controles pré-briefing do agravo interno e da
      interdição, sem liberar leitura prematura dos módulos. Rodada dirigida:
      2/2 cenários, 6/6 invariantes e zero violação do gate com subagentes
      Codex.
- [ ] Tornar elegíveis as cinco fixtures que exigem handoffs, documentos e
      localizadores que não fornecem; manter o cenário de pesquisa Silo
      condicionado a job com conector autenticado.

### Adaptação segura de casos reais — RFC aceita

Problema confirmado pela
[auditoria anonimizada](references/validacao-casos-reais.md): os módulos cíveis
não recebem hoje lente, frente ativa, ato atual, cobertura e conflito temporal
em um contrato suficientemente determinístico. Mais módulos de peça não
resolvem essa lacuna.

- [x] Censo e amostra estratificada de 14 cenários reais, sem incorporar dados
      identificadores ao repositório.
- [x] Arquitetura aceita em
      [`RFC-CA-001`](RFC-CA-001-adaptacao-casos-reais.md): intake obrigatório,
      análise documental somente quando elegível, perfil opcional de frentes,
      estados de escopo e critérios sintéticos A01–A14.
- [x] Decisão do owner sobre as seis questões de fechamento da RFC.
- [x] Fase 1 — contrato público e régua determinística A01–A14; nenhuma skill
      consumidora alterada durante essa fase.
- [ ] Fase 2 — produtor no ambiente dos casos, com autorização separada e
      dry-run sem mutação.
- [x] Fase 3 — quatro consumidores públicos, escopo por frente e bloqueios de
      ato, cobertura e regime; validada apenas deterministicamente.
- [ ] Fase 4 — capacidades auxiliares de cálculo, prazo, mídia e integridade.
- [x] Fase 5 — validação local A01–A14 com subagentes Codex: primeira passagem
      13/14, correção de A03 e regressão verde; cadeia de inputs, outputs e
      julgamentos congelada por hashes e commits. Comparação externa e dogfood
      continuam sem autorização.

## Fase 4 — Adoção e comunidade

Objetivo: preparar o repositório para público externo e só então divulgar.

Pré-requisito: Fases 1 e 2 concluídas.

- [x] `SECURITY.md` com política de reporte, escopo (conteúdo de skills,
      scripts, protocolo) e expectativa de resposta.
- [x] Templates de issue (bug, sugestão de skill, problema de conteúdo
      jurídico) e template de pull request alinhado ao CONTRIBUTING.
- [x] Material de apresentação: exemplo ponta a ponta (prompt → handoff →
      peça) com caso sintético, sem dados reais.
- [ ] Anúncio público somente após smoke tests verdes e baseline de evals
      registrado.

## Fora de escopo

Decisões explícitas de não fazer, com motivação; revisáveis, mas não
silenciosas.

- Telemetria ou coleta de uso: produto jurídico; privacidade vira passivo
  maior que o aprendizado obtido.
- Código do serviço Silo neste repositório: o Silo permanece dependência
  opcional externa, conforme o README.
- Casos reais, dados de clientes ou pesquisas internas como conteúdo:
  proibido pelo CONTRIBUTING.
- Suporte a jurisdições não cíveis (trabalhista, criminal): manter o foco até
  o fluxo cível estar completo e validado.
- Cálculo financeiro e atualização monetária por geração de texto: exigir
  motor reproduzível, índices identificados e conferência própria antes de
  transformar a capacidade em produto.
- Relógio processual autônomo por geração de texto: exigir calendário,
  feriados e regra de contagem verificáveis; a redação apenas consome prazo já
  analisado.

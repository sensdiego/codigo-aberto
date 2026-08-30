# Roadmap

Plano de desenvolvimento do plugin `silo-legal`. O roadmap é vivo: itens mudam
de estado conforme o trabalho avança, mas decisões registradas aqui não são
apagadas — itens descartados movem-se para [Fora de escopo](#fora-de-escopo).

Estado dos itens:

- `[ ]` pendente;
- `[~]` em andamento;
- `[x]` concluído.

## Estado atual (2026-08-30, v0.3.0)

- Nove skills publicadas, com disciplina compartilhada, contrato de handoff e
  recorte versionado do CPC. Versão corrente `v0.3.0`: contratos deliberativos
  e gate de confirmação entregues pelo PR #25.
- Protocolo de release validado ponta a ponta: fragmentos, semver, tag imutável,
  GitHub Release e publicação idempotente de assets (quatro releases publicadas
  pelo workflow, todas verdes).
- Sete bundles ChatGPT e o manifesto de checksums publicados na
  [release v0.2.4](https://github.com/sensdiego/codigo-aberto/releases/tag/v0.2.4);
  acervo do projeto de smoke no ChatGPT atualizado com esses ZIPs em
  2026-08-24.
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
- Camada deliberativa inicialmente decidida em 2026-08-26 como adaptação dos
  contratos. As duas rodadas da frente 2 satisfizeram a cláusula de promoção
  por falha repetida de roteamento; a frente 3 implementa a skill autônoma
  `deliberacao-juridica` sobre o mesmo protocolo e handoff. A primeira medição
  dirigida confirmou o roteamento decisório e o gate combinado, mas revelou
  excesso de roteamento na ponte com redação; a branch permanece não aceita.
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
skill autônoma reaproveitando protocolo e handoff; ela ainda não está aceita,
porque a medição dirigida encontrou regressões na ponte com redação.

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
  ChatGPT, um oitavo ZIP a descobrir; promovida em 2026-08-30 após a cláusula
  medida disparar;
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
      a frente 1. PR próprio. PR #25 integrado em 2026-08-28. Duas rodadas
      medidas falharam repetidamente por omissão ou roteamento e acionaram a
      cláusula de promoção.
- [~] Frente 3 — skill autônoma `deliberacao-juridica` (SEN-2408): porta
      própria sobre `references/deliberacao.md`, handoff `decisão`, oitavo
      bundle, roteamento das três fixtures `deliberacao-*` e estado explícito
      do gate de redação. Medição dirigida parcial em 2026-08-30: dois cenários
      decisórios PASS, `gate-confirmacao-combinada` PASS, dois controles da
      ponte de redação FAIL; dois cenários iniciais foram interrompidos após
      FAIL. As falhas apontaram roteamento precoce para deliberação e uma
      primeira entrevista com perguntas agrupadas. As regras foram estreitadas
      depois da rodada, ainda sem re-medição. Não houve regressão completa,
      merge, release ou publicação desta frente.
- [ ] Dogfood pareado antes de anúncio: mesmo caso sintético, salto direto ×
      protocolo, medindo decisões alteradas, lacunas descobertas, turnos e
      abandono.
- Cláusula de promoção: se em duas rodadas o protocolo falhar por omissão ou
  por roteamento, a skill autônoma passa a ser a recomendação — embrulhando
  protocolo e artefato já existentes.

- [ ] Módulo `tutela-urgencia-evidencia` em `redacao-contencioso`
      (CPC arts. 300–310); ampliar recorte legislativo se necessário.
- [ ] Módulo `cumprimento-sentença` (CPC arts. 523–541), incluindo
      impugnação.
- [ ] Módulo `execucao` (CPC Livre II, arts. 771+), avaliando escopo mínimo
      viável antes de redigir.
- [ ] Revisar cobertura do `manifest.json` do CPC contra os novos módulos;
      o validador garante consistência de IDs.
- [ ] Avaliar skills candidatas fora do fluxo atual: cálculo e atualização
      monetária; relógio processual autônomo. Decidir entrar ou registrar em
      Fora de escopo.
- [ ] Cada módulo entra por PR próprio com fragmento `minor`.

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

# Handoff de sessão

Atualizado em 2026-08-28, após a frente 2 da camada deliberativa (contratos)
e duas rodadas de avaliação sobre ela. A decisão de 2026-08-26 e a
especificação vivem em
[#22](https://github.com/sensdiego/codigo-aberto/issues/22); o rastreamento
externo é SEN-2383 (frente 1, Done) e SEN-2384 (frente 2), sob a
guarda-chuva SEN-2381.

## Onde o produto está

A versão publicada continua sendo a `v0.2.4`. Os contratos da frente 2
estão propostos no PR #25 (branch `feat/deliberacao-contratos`, fragmento
`minor` → v0.3.0 na publicação), abertos à revisão do Diego. Claude Code e
ChatGPT têm caminhos de uso comprovados; no Claude Cowork há dogfood interno
em projeto já montado, sem prova de instalação limpa.

## O que esta sessão entregou

- `references/deliberacao.md` (novo): protocolo em seis passos —
  apresentação decisória, até quatro opções sem fabricar pluralidade,
  recomendação com confiança e melhor objeção, entrevista com uma pergunta
  decisória por vez, handoff de tipo `decisão`, rotas de saída — mais
  fronteira com o aprofundamento e o teste "o advogado podia discordar sem
  custo?".
- `references/disciplina.md`: gatilho enumerável da deliberação (pedido do
  advogado; decisão pendente nos handoffs; ato inferido fora das opções do
  mapa) e o gate de confirmação reescrito como máquina de estados: pergunta
  fechada, lista do que não conta como confirmação e reapresentação compacta
  por delta.
- `references/handoff.md`: tipo `decisão` com campos próprios (opções
  escolhidas/rejeitadas/condicionais, razões, concessões, condição de
  reabertura) e template.
- Ponteiros nas cinco skills; descrições de `analise-juridica-civel` (cobre
  deliberação) e `aprofundamento-juridico` (cede deliberação à análise);
  `redacao-contencioso` repete o gate no próprio briefing; gerador de
  bundles copia `deliberacao.md` e reescreve os links. Régua intocada.
- Duas rodadas de avaliação em `data/evals/`:
  - `2026-08-28-claude-sonnet-contratos-deliberativos/` (rodada 1): 3 PASS,
    4 FAIL, US$ 4,33;
  - `2026-08-28-claude-sonnet-contratos-deliberativos-r2/` (rodada 2, após
    reforços): 0 PASS, 4 FAIL nos quatro re-medidos, US$ 2,41.

## O que as rodadas dizem — ler antes de decidir o próximo passo

1. **Avanço real em três frentes.** `redacao-sem-decisao-registrada` virou
   PASS (o protocolo é executado antes do briefing),
   `manifestacao-concordancia` virou PASS (e resolve a dúvida de oscilação ×
   regressão de 27/08) e `gate-resposta-nao-autoriza` se manteve PASS: a
   espera que já funcionava não quebrou.
2. **A cláusula de promoção disparou.** Em duas rodadas consecutivas com o
   protocolo, os cenários de deliberação falharam por omissão ou roteamento
   — na rodada 2, os três rotearam para `aprofundamento-juridico`
   (`deliberacao-entrevista-segundo-turno` havia roteado certo na rodada 1
   com texto quase idêntico: variância n=1). Por #22 §4, a skill autônoma de
   deliberação passa a ser a recomendação, embrulhando protocolo e artefato
   já existentes.
3. **O incidente do dogfood resiste ao texto.**
   `gate-confirmacao-combinada` reprovou nas duas rodadas pelo gate
   mecânico (turno 2 leu `contestacao.md` e entregou a contestação
   inteira), mesmo com a regra na disciplina **e** no briefing da skill de
   redação. Evidência de que regra em referência compartilhada não basta
   para esse padrão.
4. Esta sessão gera as duas primeiras rodadas com protocolo; a cláusula já
   está integralmente satisfeita (duas rodadas, falha por omissão ou
   roteamento).

## Próxima tarefa com maior impacto: frente 3 — skill autônoma de deliberação

Decisão do Diego em 2026-08-28: os contratos seguem (PR #25 aberto; merge
pendente da revisão dele) e a próxima sessão, com contexto limpo, executa a
frente 3 — a skill autônoma `deliberacao-juridica`, conforme a cláusula de
promoção de #22 §4 (duas rodadas falhando por omissão ou roteamento, ambas
registradas em `data/evals/`). O primeiro ato da sessão é abrir a issue SEN
da frente 3 sob SEN-2381 e atualizar SEN-2384 com o resultado das rodadas.

### Desenho elaborado nesta sessão (não reabrir sem evidência nova)

1. **A skill embrulha o que já existe.** `references/deliberacao.md` vira a
   referência própria da skill (mover ou apontar) e o handoff de tipo
   `decisão` é o artefato de saída. Nada de protocolo novo; a falha medida
   foi de roteamento e obediência, não de conteúdo.
2. **Roteamento por porta própria, não por descrição compartilhada.** A
   fragilidade medida: "o que eu faço?" caiu em `aprofundamento-juridico` em
   três de quatro medições, com variância n=1 (um cenário oscilou entre
   rodadas com texto quase idêntico). Minuta de description:
   > Conduzir a decisão do advogado entre a análise e a ação: apresentar a
   > conclusão com confiança, até quatro opções com reversibilidade e
   > urgência, recomendação própria com a melhor objeção e entrevista
   > decisória, registrando a decisão em handoff próprio. Use quando o
   > advogado pedir caminho ("o que eu faço?", "qual caminho?", "vale a
   > pena X?", "me ajuda a decidir") ou quando uma peça pressupuser escolha
   > ainda não registrada (ato, tese, pedido, concessão). Não pesquisa, não
   > aprofunda tese e não redige.
   Ao promovê-la, **reverter** os ponteiros das outras skills: descrição de
   `analise-juridica-civel` volta a não cobrir deliberação (oferece a rota
   para a skill nova ao fechar); o "não use" de `aprofundamento-juridico`
   passa a apontar para `deliberacao-juridica` pelo nome.
3. **A redação passa a exigir o artefato, não a sugerir a rota.** Em
   `redacao-contencioso` (e `redacao-consultivo`, proporcional): quando o
   gatilho (b)/(c) dispara, o handoff de tipo `decisão` vira pré-requisito
   do briefing — é a condição sob a qual a alternativa A fechava o
   critério (d) na tabela de #22 §3. O ponteiro "conduza primeiro a
   deliberação" vira "encaminhe para `deliberacao-juridica`".
4. **O gate de confirmação é problema separado e continua aberto.**
   `gate-confirmacao-combinada` resistiu a regra na disciplina **e** no
   briefing da skill. A frente 3 não conserta isso por desenho; avaliar na
   implementação se o briefing consolidado como estado explícito (a redação
   só redige com briefing confirmado **e**, quando houver gatilho, decisão
   registrada) endurece o ponto — e re-medir.
5. **Mecânica do repositório.** Nova entrada em `skills/deliberacao-juridica/`
   (sem CPC, como `analise-jurisprudencial`); `WORKFLOW_SKILLS` em
   `scripts/validate_skills.py`; tupla `SKILLS` em
   `scripts/build_chatgpt_smoke_bundle.py` (oitavo ZIP — ponto fraco
   conhecido da alternativa A; mitigar nas instruções permanentes do
   projeto ChatGPT); README/QUICKSTART/ROADMAP passam a dez portas;
   `expected_skill` dos cenários `deliberacao-*` muda para a skill nova —
   **mudança de régua no mesmo PR, com justificativa escrita** (a promoção
   decidida), exceção prevista no CONTRIBUTING. Controle de confusão
   obrigatório: `aprofundamento-audiencia` deve continuar indo para
   `aprofundamento-juridico`.
6. **Medição.** Rodada dos sete cenários (~US$ 4,30) com o mesmo harness;
   sucesso mínimo: os três `deliberacao-*` rotear para a skill nova e
   `gate-resposta-nao-autoriza` se manter. Régua completa (19 cenários,
   ~US$ 9) antes de publicar. Fragmento `minor` (v0.3.0 se o PR #25 ainda
   não tiver sido publicado; caso contrário a release seguinte).
7. **Fora de escopo da frente 3:** anúncio público (vedado até o dogfood
   pareado), skill no regime de deliberação do ecossistema (spec externa,
   sem dependência), novos cenários além do ajuste de `expected_skill`.

A regra do CONTRIBUTING segue fora da exceção acima: não alterar skill e
régua no mesmo pull request sem justificativa.

## Pendências secundárias

- ~~Re-medir `manifestacao-concordancia`~~ — resolvido na rodada 1 (PASS,
  invariante novo incluído).
- Documentar e testar a preparação limpa de um projeto no Claude Cowork.
- Revisar, em frente separada, lacunas do recorte legislativo do CPC
  percebidas durante a redação.
- `pesquisa-silo` continua sem cenário próprio na régua.
- Classificar `data/**` explicitamente no `.release-policy.toml` na próxima
  mudança que tocar a policy (observação de #15).
- Não iniciar piloto externo ou anúncio público; o dogfood pareado (salto
  direto × protocolo) é pré-condição de anúncio.

## Avisos operacionais

- O plugin local do Claude Code está na `v0.2.4`; a branch da frente 2 não
  muda `plugin.json` até a publicação da v0.3.0. Re-medições conferem a
  versão instalada antes de rodar (`claude plugin list`).
- O projeto "Silo Legal Skills — Smoke" no ChatGPT usa instruções
  permanentes e o acervo foi atualizado com os ZIPs da v0.2.4 em 2026-08-24;
  os bundles da branch (com `deliberacao.md`) só sobem após publicação.
- Custos medidos: rodada dos sete cenários ≈ US$ 4,30; re-medição de quatro
  ≈ US$ 2,40; régua completa estimada ≈ US$ 9. Sempre manual:
  `python3 scripts/run_evals.py`.
- `--resume` reaproveita os transcripts gravados por turno; para reexecutar
  um cenário, apague seus arquivos em `transcripts/` antes (ou use out-dir
  novo). Transcripts não são versionados (`.gitignore`).
- Rodar o harness de dentro de uma sessão do Claude Code exige `env -u
  CLAUDECODE`; o `claude -p` aninhado funciona e a sessão é retomada por
  `--resume` no mesmo diretório.

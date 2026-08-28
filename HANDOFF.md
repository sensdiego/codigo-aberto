# Handoff de sessão

Atualizado em 2026-08-28, após a frente 2 da camada deliberativa (contratos)
e duas rodadas de avaliação sobre ela. A decisão de 2026-08-26 e a
especificação vivem em
[#22](https://github.com/sensdiego/codigo-aberto/issues/22); o rastreamento
externo é SEN-2383 (frente 1, Done) e SEN-2384 (frente 2), sob a
guarda-chuva SEN-2381.

## Onde o produto está

A versão publicada continua sendo a `v0.2.4`. A branch
`feat/deliberacao-contratos` leva os contratos da frente 2 com fragmento
`minor` (v0.3.0 na publicação) e ainda não foi proposta em PR ao fechar
deste handoff. Claude Code e ChatGPT têm caminhos de uso comprovados; no
Claude Cowork há dogfood interno em projeto já montado, sem prova de
instalação limpa.

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

## Próxima tarefa com maior impacto: decidir e executar a promoção

A decisão registrada em #22 §4 manda recomendar a skill autônoma
`deliberacao-juridica` (alternativa A da tabela), embrulhando
`references/deliberacao.md` e o handoff de tipo `decisão`. Antes de
implementar, o Diego precisa decidir: (a) propor/integrar os contratos como
estão — ganhos medidos em três cenários, artefatos prontos para a skill
embrulhar — e abrir a frente 3 (skill autônoma, SEN nova sob SEN-2381); ou
(b) segurar os contratos e redesenhar já com a skill autônoma. Não iterar
mais sobre descrições: seria ajuste a ruído (n=1) contra a cláusula
pré-acordada.

Se a frente 3 for aberta: roteamento deixa de depender de descrição
compartilhada, a redação passa a exigir o artefato de decisão quando o
gatilho (b)/(c) dispara, e a régua se repete (sete cenários, ~US$ 4; régua
completa de 19 antes de publicar, ~US$ 9). A regra do CONTRIBUTING segue:
não alterar skill e régua no mesmo pull request sem justificativa.

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
- Atualizar SEN-2384 (resultado das rodadas e cláusula disparada) e abrir a
  issue da frente 3 se o Diego confirmar a promoção.

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

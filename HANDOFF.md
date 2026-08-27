# Handoff de sessão

Atualizado em 2026-08-27, após a entrega da frente 1 da camada deliberativa
(a régua) e o registro do baseline da lacuna sobre a v0.2.4. A decisão de
2026-08-26 e a especificação vivem em
[#22](https://github.com/sensdiego/codigo-aberto/issues/22); o rastreamento
externo é SEN-2383 (frente 1) e SEN-2384 (frente 2), sob a guarda-chuva
SEN-2381.

## Onde o produto está

A versão corrente continua sendo a `v0.2.4`, publicada e auditada. Nenhuma
skill, referência ou bundle foi editado nesta sessão; a PR da frente 1 leva
fragmento `none` porque muda a régua, não o produto. Claude Code e ChatGPT têm
caminhos de uso comprovados; no Claude Cowork há dogfood interno em projeto já
montado, sem prova de instalação limpa.

## O que esta sessão entregou

- `scripts/run_evals.py`: `prompt` aceita lista de turnos executados na mesma
  sessão headless (`--session-id` no primeiro turno, `--resume` nos seguintes,
  mesmo diretório; transcript gravado por turno antes do julgamento, em
  `<id>.turnK.jsonl`). O campo opcional `authorizing_turn` liga a verificação
  mecânica: nenhum `skills/redacao-contencioso/references/modulos/*.md` pode
  ser lido antes do turno autorizador (`null` = nenhum turno autoriza), e a
  reprovação independe do juiz. O relatório ganhou a coluna `gate`. O validador
  e o CONTRIBUTING acompanham os campos novos.
- Seis cenários novos e o invariante "um único turno, sem deliberação" em
  `manifestacao-concordancia`: a régua tem 19 cenários.
- Baseline em `data/evals/2026-08-27-claude-sonnet-v0.2.4/`: 7 cenários,
  1 PASS, 6 FAIL, US$ 3,61 (os multi-turno custam ~US$ 0,60 cada).

## O que o baseline diz — ler antes de começar a frente 2

1. **O incidente do dogfood ficou reproduzível por máquina.** Em
   `gate-confirmacao-combinada`, "não vamos reconvir… pode redigir" na mesma
   mensagem fez o modelo ler `contestacao.md` no turno 2 e entregar a
   contestação inteira.
2. **A resposta isolada já é tratada certo.** `gate-resposta-nao-autoriza`
   passou 4/4: reapresentação por delta, espera, minuta só depois do "sim" ao
   briefing consolidado. A frente 2 precisa fechar a confirmação combinada sem
   quebrar esse comportamento.
3. **Deliberação reprova primeiro por roteamento.** Os três cenários foram para
   `aprofundamento-juridico` (2) e `redacao-contencioso` (1). Na skill errada o
   modelo improvisa: `entrevista-segundo-turno` cumpriu 5/5 invariantes;
   `nao-agir-sob-pressao` 4/5 (faltaram confiança e melhor objeção);
   `nao-redigir` 2/6 (sem recomendação própria, sem confiança, "matriz de
   perspectivas" no lugar de opções, duas perguntas em vez de uma). O que falta
   de forma sistemática é recomendação com confiança e melhor objeção e uma
   pergunta decisória por vez — exatamente o protocolo de
   `references/deliberacao.md`.
4. `redacao-sem-decisao-registrada` (3/4): identificou os dois atos, pediu a
   decisão e não redigiu; só não expôs a reversibilidade das opções.
5. **Achado colateral:** `manifestacao-concordancia` reprovou "não infla uma
   manifestação simples" (exigiu lastro completo do título e handoffs de
   análise para uma concordância já autorizada), embora tenha passado 3/3 no
   baseline v0.2.3 de 24/08. Uma execução não separa variância de regressão;
   re-medir antes de concluir. O invariante novo passou.
6. Esta rodada mede a v0.2.4, sem protocolo: **não conta** para a cláusula de
   promoção (duas rodadas com o protocolo falhando por omissão ou roteamento).

## Próxima tarefa com maior impacto: frente 2 — contratos (v0.3.0)

Escopo em #22 §5 e §7 e em SEN-2384: `references/disciplina.md` (gatilho
enumerável e gate como máquina de estados, com a lista do que não conta como
confirmação), `references/handoff.md` (tipo `decisão` e template),
`references/deliberacao.md` (carregado só quando o gatilho dispara), ponteiros
em `analise-juridica-civel`, `analise-jurisprudencial`,
`aprofundamento-juridico`, `redacao-contencioso` e `redacao-consultivo`,
description de `analise-juridica-civel` (controle de confusão:
`aprofundamento-audiencia` deve continuar indo para `aprofundamento-juridico`)
e gerador de bundles (`REWRITES` + cópia em `skill_files()`). Fragmento
`minor`. Re-medir primeiro os sete cenários desta rodada
(`python3 scripts/run_evals.py --scenario …`, ~US$ 3,60) e comparar com o
baseline de 27/08; depois a régua completa (19 cenários, ~US$ 9) antes de
publicar.

Regra do CONTRIBUTING que se aplica: não alterar skill e régua no mesmo pull
request sem justificativa. A frente 2 não deve tocar `workflows.json` salvo por
lacuna demonstrada do baseline.

## Pendências secundárias

- Re-medir `manifestacao-concordancia` isoladamente para separar variância de
  regressão no invariante "não infla".
- Documentar e testar a preparação limpa de um projeto no Claude Cowork.
- Revisar, em frente separada, lacunas do recorte legislativo do CPC percebidas
  durante a redação.
- `pesquisa-silo` continua sem cenário próprio na régua.
- Classificar `data/**` explicitamente no `.release-policy.toml` na próxima
  mudança que tocar a policy (observação de #15).
- Não iniciar piloto externo ou anúncio público; o dogfood pareado (salto
  direto × protocolo) é pré-condição de anúncio.

## Avisos operacionais

- O plugin local do Claude Code está na `v0.2.4`; re-medições conferem a versão
  instalada antes de rodar (`claude plugin list`).
- O projeto "Silo Legal Skills — Smoke" no ChatGPT usa instruções permanentes e
  o acervo foi atualizado com os ZIPs da v0.2.4 em 2026-08-24.
- Custos medidos: rodada dos sete cenários da camada deliberativa ≈ US$ 3,60;
  cenário multi-turno ≈ US$ 0,60; régua completa estimada ≈ US$ 9. Sempre
  manual: `python3 scripts/run_evals.py`.
- `--resume` reaproveita os transcripts gravados por turno; para reexecutar um
  cenário, apague seus arquivos em `transcripts/` antes.
- Rodar o harness de dentro de uma sessão do Claude Code exige `env -u
  CLAUDECODE`; o `claude -p` aninhado funciona e a sessão é retomada por
  `--resume` no mesmo diretório.

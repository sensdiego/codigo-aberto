# Handoff de sessão

Atualizado em 2026-08-24, ao fim da sessão que concluiu as Fases 0, 1 (exceto
Claude Cowork) e 2 do [ROADMAP](ROADMAP.md).

## Onde o produto está

A versão corrente é a `v0.2.4`, publicada e auditada. O caminho do usuário está
comprovado de ponta a ponta nos dois aplicativos suportados (Claude Code por
plugin; ChatGPT por ZIP montado em conversa ou projeto — ver
[QUICKSTART](QUICKSTART.md)). A régua de qualidade está operacional e já
completou um ciclo inteiro: o baseline v0.2.3 encontrou três falhas, as
correções saíram na v0.2.4 e a re-medição confirmou zero falhas de roteamento
em seis execuções (issues #9, #11 e #15, todas fechadas com evidência).

## Próxima tarefa com maior urgência: enxoval de adoção (Fase 4)

Os dois pré-requisitos do anúncio público — smokes verdes e baseline de evals
registrado — estão cumpridos. O que separa o produto de usuários externos é o
enxoval:

1. `SECURITY.md` com política de reporte, escopo e expectativa de resposta.
2. Templates de issue (bug, sugestão de skill, problema de conteúdo jurídico)
   e template de pull request alinhado ao CONTRIBUTING.
3. Material de apresentação: exemplo ponta a ponta (prompt → handoff → peça)
   com caso sintético — os transcripts dos smokes de 2026-08-24 são matéria-
   prima pronta.
4. Só então, o anúncio.

Por que é a maior urgência: cada dia entre "produto provado" e "produto
anunciado" é adoção que não acontece, e nenhum item do enxoval depende de
decisão externa — é executável numa sessão.

## Alternativas na fila

- Fase 3 (expansão de conteúdo cível: tutela de urgência, cumprimento de
  sentença, execução) — destravada, com régua para medir cada módulo novo.
- Caminho do Claude Cowork (último item da Fase 1) — sem usuário nomeado
  esperando; baixa urgência.
- Residual do harness: invariantes condicionais ao ambiente (`requires: silo`)
  para o cenário que exige conector — anotado no fechamento da issue #15.

## Avisos operacionais

- O plugin local do Claude Code está na `v0.2.4`; re-medições futuras devem
  conferir a versão instalada antes de rodar (`claude plugin list`).
- O projeto "Silo Legal Skills — Smoke" no ChatGPT tem instruções permanentes
  que roteiam e montam a skill sozinhas; o acervo foi atualizado com os ZIPs
  da v0.2.4 em 2026-08-24 (usar sempre o sufixo mais alto de cada skill).
- Rodada completa de evals custa ~US$ 6 e é sempre manual:
  `python3 scripts/run_evals.py` (ver CONTRIBUTING, seção "Cenários de
  avaliação").

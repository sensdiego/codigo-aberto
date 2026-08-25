# Handoff de sessão

Atualizado em 2026-08-24, ao fim da sessão que concluiu as Fases 0, 1 (exceto
Claude Cowork) e 2, além do enxoval preparatório da Fase 4 do
[ROADMAP](ROADMAP.md).

## Onde o produto está

A versão corrente é a `v0.2.4`, publicada e auditada. O caminho do usuário está
comprovado de ponta a ponta nos dois aplicativos suportados (Claude Code por
plugin; ChatGPT por ZIP montado em conversa ou projeto — ver
[QUICKSTART](QUICKSTART.md)). A régua de qualidade está operacional e já
completou um ciclo inteiro: o baseline v0.2.3 encontrou três falhas, as
correções saíram na v0.2.4 e a re-medição confirmou zero falhas de roteamento
em seis execuções (issues #9, #11 e #15, todas fechadas com evidência).

O PR #20 integrou a política de segurança, três modelos de issue, o template de
pull request e um exemplo sintético completo com roteiro de piloto. Essa
integração prepara a adoção; não comprova uso externo e não publicou anúncio.

## Próxima tarefa com maior impacto: primeiro piloto externo nomeado

O próximo ganho não vem de mais conteúdo: vem de observar uma pessoa externa
usando o caminho já documentado. Para isso:

1. Diego nomeia e convida uma pessoa que trabalhe com contencioso cível.
2. A sessão usa somente o caso sintético do QUICKSTART por 30 minutos.
3. Registrar aplicativo, versão, resultado, atrito e qualquer falha em uma
   issue, sem dados reais.
4. Só decidir anúncio amplo depois desse recibo humano e de estabelecer um
   canal privado real para relatos de segurança.

Bloqueio atual: não há pessoa piloto nomeada, e o relato privado nativo do
GitHub continua desabilitado. O `SECURITY.md` fornece um caminho provisório sem
detalhes públicos, mas isso não deve ser confundido com intake privado nativo.

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
- O anúncio público e qualquer convite efetivo continuam não executados.
- Rodada completa de evals custa ~US$ 6 e é sempre manual:
  `python3 scripts/run_evals.py` (ver CONTRIBUTING, seção "Cenários de
  avaliação").

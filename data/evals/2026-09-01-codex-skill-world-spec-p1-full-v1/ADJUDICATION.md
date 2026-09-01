# Adjudicação da rodada comportamental P1 v1

Status: `STOP_VARIANCE`.

## Configuração

- plugin `silo-legal` `v0.6.4`;
- backend `codex-cli`, modelo `gpt-5.6-sol`, raciocínio `high`;
- `analise-juridica-civel` e referências fornecidas diretamente ao executor;
- execuções efêmeras, sandbox somente leitura, sem rede, memórias,
  plugins ou multiagente;
- roteamento automático do plugin não medido.

Artefatos congelados durante o painel:

- `skills/analise-juridica-civel/SKILL.md`: SHA-256
  `089a0fb0e097221cdd2b6f65241f2ada8ecc26733fcc6c551b76ed51a832d759`;
- `tests/fixtures/world-spec-p1-workflows.json`: SHA-256
  `873a8622adf203b00e5d69ab7ec3dd77629370b63bfcc35caefd345fda00dd52`;
- `tests/fixtures/codex-judge-schema.json`: SHA-256
  `5fffcf33195b85638c50f353f2763e4423ca6c326b22bcef05bc65bba73312c0`.

## Rodada primária

O canário `M-201/W-A`, `M-201/W-B` e `M-201/W-C` passou 3/3 cenários e
24/24 invariantes. A continuação usou `--resume --fail-fast` e parou em
`M-202/W-A`: 7/8 invariantes, total acumulado de 3 PASS, 1 FAIL, zero
`JUDGE_ERROR` e 31/32 invariantes atendidos. Os outros 32 cenários não foram
executados.

O item reprovado foi o invariante crítico específico de `W-A`: reconhecer a
convergência entre a alegação da inicial e o registro de atendimento sem
transformá-la em fato judicialmente reconhecido. A auditoria manual confirmou
o juízo: a primeira saída descreveu o registro e a alegação em passagens
separadas, mas não declarou que o registro corroborava aquela alegação.

Recibo: `report.json`, SHA-256
`67657fa8f627b1be296b4758f33041d1dbf2e2b5393451888299526902288c1b`.

## Painel de estabilidade

`M-202/W-A` foi executado mais quatro vezes, sem alterar skill, fixture,
documentos, modelo ou configuração do juiz. O painel de cinco amostras,
incluída a execução primária, terminou em **3 PASS e 2 FAIL**. As duas falhas
reprovaram o mesmo invariante 7; os três passes declararam a ligação entre a
reclamação narrada e o registro de atendimento sem ampliar o alcance da
prova.

Este painel é diagnóstico: confirma a oscilação sob entradas congeladas, mas
não estima uma taxa populacional de acerto. Recibos das quatro reexecuções:

- `../2026-09-01-codex-skill-world-spec-p1-m202-wa-rerun-v1/report.json`:
  `874610b0ec44682915b53bf520eb18886f31fdabee3705c6e60b87709b659dcb`;
- `../2026-09-01-codex-skill-world-spec-p1-m202-wa-rerun-v2/report.json`:
  `2f8bd0da14d687d2ecdd62fe486147a73a2f2b14055e4178ecb07ca721876821`;
- `../2026-09-01-codex-skill-world-spec-p1-m202-wa-rerun-v3/report.json`:
  `8fe2868942e0dd76400e8f8546026208440a6d049c34772a564c3a6db50c4f24`;
- `../2026-09-01-codex-skill-world-spec-p1-m202-wa-rerun-v4/report.json`:
  `91776b110ebcd90310fa585015cea89f9e65615bce03898bd62b67075deda6c2`.

## Consumo e decisão

As oito execuções e oito julgamentos realizadas na P1 — os três mundos do
canário M-201 e as cinco amostras de M-202/W-A — somaram 914.864 tokens de
entrada dos executores, dos quais 695.808 em cache, e 149.242 tokens de entrada
dos juízes. O runner não reporta preço externo em dólares para o backend
Codex; houve consumo da franquia da conta.

Não há recibo de passagem integral da P1. O lote permanece bloqueado antes
dos 32 cenários restantes. Como o painel confirmou a instabilidade, o próximo
gate recomendado é fortalecer a regra geral de ligação
`alegação -> documento corroborante -> limite da prova` e então recomeçar a
regressão desde o canário M-201.

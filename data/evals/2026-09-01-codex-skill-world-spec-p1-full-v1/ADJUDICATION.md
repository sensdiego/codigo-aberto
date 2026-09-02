# Adjudicação da rodada comportamental P1 v1

Status: `STOP_VARIANCE_PERSISTS`.

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

Naquele ponto não havia recibo de passagem integral da P1. O lote permaneceu
bloqueado e abriu a rodada corretiva registrada abaixo.

## Rodada corretiva limitada

### Candidato 1

O commit `eb29024` acrescentou uma regra geral de ligação entre alegação,
documento corroborante e alcance da prova. A skill ficou no SHA-256
`9fefd0ccd67d158d178a1eea76d68bd436a6b3f3d189f976f47bdfa63e17e3ac`;
fixture e juiz permaneceram nos hashes originais.

O painel isolado de `M-202/W-A` passou 5/5, com 40/40 invariantes e zero
`JUDGE_ERROR`. A P1 integral, porém, parou em `M-203/W-A`: 6 PASS, 1 FAIL,
55/56 invariantes. A falha foi novamente o invariante 7. A auditoria manual
confirmou que a saída descreveu inicial e registro, mas não declarou a
convergência entre seus conteúdos.

Recibo da P1: `../2026-09-01-codex-skill-world-spec-p1-full-postfix-v1/report.json`,
SHA-256 `dd7b091af217fd87b69a6a501be98ad1f296a9b83f970530ef4a85445352e26d`.

### Candidato 2

O commit `d9a79d0` tornou explícita a diferença entre provar que um relato foi
feito e provar o fato relatado. A skill ficou no SHA-256
`c40ae342812ca419d0395a5c7ff87e7cb0dcc8fa1031a6a73954c1889644e240`;
fixture e juiz continuaram congelados.

O painel isolado de `M-203/W-A` passou 5/5, com 40/40 invariantes e zero
`JUDGE_ERROR`. A nova P1 integral parou em `M-204/W-A`: 9 PASS, 1 FAIL,
79/80 invariantes. A falha foi novamente o invariante 7. A auditoria manual
confirmou o juízo: a saída afirmou que a reclamação existiu, mas não ligou
expressamente a alegação da inicial ao registro.

Recibo da P1: `../2026-09-01-codex-skill-world-spec-p1-full-postfix2-v1/report.json`,
SHA-256 `9111f5523ba3d51ce0b3d9c33660c07d9b5ebec898b067f7b428d43991b971e8`.

Os dez relatórios dos painéis isolados estão nos diretórios
`../2026-09-01-codex-skill-world-spec-p1-m202-wa-postfix-v1` a `v5` e
`../2026-09-01-codex-skill-world-spec-p1-m203-wa-postfix2-v1` a `v5`.
Os hashes dos 12 relatórios corretivos estão em
`POSTFIX_REPORT_SHA256SUMS.txt`.

## Consumo corretivo e decisão final

A rodada corretiva executou 27 pares executor–juiz: 25 PASS, 2 FAIL e zero
`JUDGE_ERROR`. Consumiu 3.023.003 tokens de entrada dos executores, 2.256.640
deles em cache, e 504.370 tokens de entrada dos juízes. O custo externo
reportado permaneceu em US$ 0; houve consumo da franquia Codex.

A segunda alteração esgotou a stop rule autorizada. A P1 não passou
integralmente, a P0 não foi executada e nenhum push, PR, merge, tag ou release
foi realizado. Novo ajuste textual da mesma regra não é recomendado: se a
frente for reaberta, o próximo experimento deve testar uma superfície estrutural
obrigatória no mapa jurídico para relações probatórias, sob novo mandato e novo
orçamento.

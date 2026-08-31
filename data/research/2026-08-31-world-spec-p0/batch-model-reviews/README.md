# Prova cega por agentes do lote calibrado

Estado final: `FULL_BATCH_BLIND_PASS / 36_OF_36_WORLDS / CONSENSUS_CONSTRUIR`.

Claude Sonnet 5 e Claude Opus 5 receberam o mesmo pacote cego com quatro
assuntos, um por motivo empírico: `M-101`, `M-105`, `M-108` e `M-111`. Cada
assunto contém `W-A`, `W-B` e `W-C`, totalizando 12 mundos e 216 arquivos de
entrada. Nenhum braço recebeu tools, `authority/`, parecer anterior ou resposta
do outro braço.

## Resultado final v3

| Braço | Modelo retornado | Entrada | Saída | Custo | Gate |
| --- | --- | ---: | ---: | ---: | --- |
| Triagem | `claude-sonnet-5` | 51.723 | 24.019 | US$ 0,343636 | `CONSTRUIR` |
| Auditoria | `claude-opus-5` | 51.723 | 22.803 | US$ 0,828690 | `CONSTRUIR` |
| **Total** |  | **103.446** | **46.822** | **US$ 1,172326** | **consenso** |

O prompt final tinha 111.456 bytes e SHA-256
`f0e6ff250fe0369d89d5db1944f6b91489276d304bc23773e6a1a1355eb03063`.
Cada recibo lista e fixa o hash dos 216 arquivos cegos. Ambos terminaram com
`end_turn`, `retries: 0`, `tools_omitted: true` e somente o modelo solicitado.

O adjudicador abriu o gabarito apenas depois de congeladas as duas respostas.
Resultado: 12/12 mundos aprovados; cada modelo recuperou 16/16 observações
críticas e 8/8 relevantes; não houve parcial, omissão ou falso positivo crítico.
Os 28 hashes das fontes da adjudicação e os 216 hashes cegos de cada recibo
foram conferidos novamente pelo operador raiz.

O recibo canônico é `canary-adjudication-v3.json`. As respostas e recibos estão
em `sonnet-5-canary-v3/` e `opus-5-canary-v3/`.

## Extensão aos oito assuntos restantes

Sem novas chamadas externas, os oito assuntos fora do canário foram divididos
em dois pacotes cegos:

- pacote A: `M-102`, `M-106`, `M-109` e `M-112`;
- pacote B: `M-103`, `M-104`, `M-107` e `M-110`.

Em cada pacote, dois subagentes Codex receberam somente `task.md` e os arquivos
sob `documents/`, totalizando 216 entradas e 12 mundos por revisor. Um terceiro
subagente abriu as duas respostas congeladas e os 24 arquivos reservados de
`ground_truth.json` e `rubric.json`. Os dois pacotes passaram: 12/12 mundos por
pacote; 16/16 observações críticas e 8/8 relevantes recuperadas por cada
revisor; zero parcial, omissão ou falso positivo crítico.

Os recibos canônicos são `codex-remaining-a-adjudication-v1.json` e
`codex-remaining-b-adjudication-v1.json`. As respostas estão em
`codex-remaining-{a,b}-reviewer-{1,2}-v1/`. Cada receipt declara
`external_cost_usd: 0`, `authority_files_included: false` e
`prior_reviews_included: false`. O operador raiz reconferiu os quatro hashes de
resposta, os 56 hashes das duas adjudicações, as evidências literais e as
contagens.

## Falhas que precederam o PASS

As falhas foram preservadas porque demonstram que os revisores alteraram o lote,
em vez de apenas homologá-lo.

1. Duas requisições iniciais foram rejeitadas com HTTP 400 antes de inferência:
   o schema repetia a estrutura do mundo 12 vezes e excedia o compilador de
   gramática. Não houve resposta nem uso reportado.
2. `canary-adjudication-v1.json` é `FAIL`: o harness dizia que todo arquivo era
   evidência e, assim, contradizia `task.md`. Opus completou a análise, mas
   Sonnet deixou parciais as oito observações críticas de `W-C`.
3. `canary-adjudication-v2.json` é `FAIL`: após corrigir o harness, os dois
   modelos recuperaram integralmente a semântica, mas Opus detectou feriados
   brasileiros dentro das janelas de `M-105` e `M-108` e um ofício híbrido.
   O lote foi redesenhado, não o parecer.
4. O v3 deslocou as janelas para intervalos sem fechamento conhecido, tornou o
   calendário explícito sobre o período relevante e transformou o ofício em
   resposta do Diário da Justiça ao juízo. Só então os dois braços aprovaram.

As seis chamadas válidas dos três ensaios custaram US$ 3,368367. Os HTTP 400
não são contabilizados como custo zero porque não trouxeram campo de uso.

## Limite da prova

O lote integral prova recuperabilidade e consistência nos 12 assuntos desta
família, não generalização para todas as áreas jurídicas. O canário preserva
diversidade real entre Sonnet e Opus; os oito assuntos restantes foram avaliados
por pares da mesma família Codex e demonstram isolamento processual, não
independência entre fornecedores. O Sonnet atribuiu realismo 3/5 aos quatro
`W-C` do canário; o Opus atribuiu 4/5. A artificialidade controlada do conflito
cronológico continua visível, embora não tenha bloqueado nenhum gate final.

## Consumo pelo executor local

`tests/fixtures/world-spec-p0-workflows.json` vincula o lote e estes três
recibos por SHA-256. `scripts/run_evals.py` materializa 36 cenários temporários,
cada um com `task.md`, 17 documentos cegos e sete invariantes da rubrica. A
listagem local passou.

O baseline bruto está preservado em
`data/evals/2026-08-31-codex-world-spec-p0-canary-v1/` e expôs a omissão do art.
524. No modo skill-backed, executor e juiz usaram chamadas efêmeras separadas de
`gpt-5.6-sol`, sem custo externo em dólares. A execução integral fechou 36/36
mundos e 252/252 invariantes depois de duas correções comprovadas: reconciliação
normativa geral na skill e classificação de veredito incompleto como
`JUDGE_ERROR` no runner. O recibo canônico está em
`data/evals/2026-08-31-codex-skill-world-spec-p0-full-v1/report.json`; as
tentativas supersedidas permanecem referenciadas nele. O backend forneceu o
material da skill em pacote cego, mas não testou o roteamento automático do
plugin.

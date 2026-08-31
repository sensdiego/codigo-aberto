# Ensaio cego com Claude Opus 5 e Claude Sonnet 5

## Resultado atual

Estado:
`STATIC_PASS / MODEL_BLIND_COMPLETE / CONSENSUS_CONSTRUIR_P0 / OWNER_DIRECTED_BUILD`.

Claude Sonnet 5 e Claude Opus 5 receberam a mesma revisão 3 do corpus pela
Messages API, sem tools e sem acesso ao gabarito, aos pareceres anteriores ou
à resposta do outro braço. Os dois propuseram `CONSTRUIR P0`, recuperaram as
três variações esperadas e não identificaram vazamento de gabarito.

Esse consenso remove o bloqueio de QA por modelos. O owner, que é advogado,
dirige a construção e não exige revisão por outro advogado como condição para
o P0. O protocolo em `generated/blind/INSTRUCOES-REVISOR.md` permanece apenas
como instrumento opcional de red-team.

## Evolução do corpus

A revisão original foi reprovada pelos dois modelos porque W-B omitia o
arquivo 14 e denunciava a mutação pelo salto de numeração. Ela também continha
linguagem que explicava o valor probatório das próprias peças.

A revisão 2 corrigiu o inventário: os três mundos passaram a ter os mesmos 18
nomes, e W-B recebeu uma resposta bancária negativa no lugar da remoção do
comprovante. A triagem Sonnet recuperou corretamente os três mundos, mas
propôs `REDESENHAR` porque quatro documentos comuns ainda continham pistas de
construção: aviso dentro dos autos, fechamento artificial do demonstrativo,
declaração explícita de ausência no extrato e calendário limitado exatamente
à janela do prazo.

A revisão 3 aplicou a correção mínima:

- o aviso de ficção ficou somente em `task.md`, fora de `documents/`;
- o demonstrativo deixou de declarar que não havia lançamento posterior;
- o extrato passou a ser uma consulta datada que termina no último andamento;
- o calendário passou a cobrir março de 2026 inteiro;
- os três mundos ficaram com o mesmo inventário de 17 documentos.

Na revisão 3, somente `14-registro-bancario.md` difere entre W-A e W-B, e
somente `12-certidao-publicacao.md` difere entre W-A e W-C.

## Recibos válidos da revisão 3

| Braço | Modelo pedido e retornado | Entrada | Saída | Latência | Custo |
| --- | --- | ---: | ---: | ---: | ---: |
| Triagem | `claude-sonnet-5` | 15.046 | 19.304 | 196.664 ms | US$ 0,223132 |
| Auditoria | `claude-opus-5` | 15.046 | 10.869 | 127.389 ms | US$ 0,346955 |
| **Total** | dois modelos puros | 30.092 | 30.173 | sequencial | **US$ 0,570087** |

Os dois terminaram com `end_turn`; os únicos tipos de bloco foram `thinking` e
`text`; `reported_models` contém somente o modelo solicitado; `retries` é zero;
e `tools_omitted` é verdadeiro.

O prompt final foi idêntico nos dois braços: 55 arquivos, 30.411 bytes e
SHA-256
`4e9acc204019951c4462d3f51bbacc6c4ca6b2815376265b74ca47f3568c05d5`.

## Controles de isolamento

- operadores novos, sem histórico compartilhado, um por chamada;
- diretórios de saída separados e imutáveis;
- mesmo corpus, instrução, schema, `effort=high` e limite de 40.000 tokens;
- proibição de leitura de `world_spec.json`, `generated/authority/`,
  `HANDOFF.md`, memórias, Git, README e pareceres anteriores;
- uma inferência por braço, sem retry manual ou automático;
- corpo da Messages API sem campo `tools` e com
  `service_tier=standard_only`;
- validação fail-closed do modelo retornado, `stop_reason`, tipos de bloco,
  schema da resposta e ausência de prompt caching;
- hashes do prompt e de todos os arquivos congelados nos recibos;
- abertura do gabarito e comparação substantiva somente pelo operador raiz,
  depois de cada resposta estar gravada.

## Comparação final com o gabarito

| Mundo | Verdade oculta | Sonnet 5 | Opus 5 |
| --- | --- | --- | --- |
| W-A | controle: comprovante presente, publicação convergente, sem extinção judicial | recuperou; prazo final 25/03 e pagamento em 24/03 | recuperou; prazo final 25/03 e pagamento em 24/03 |
| W-B | pagamento alegado; busca bancária negativa não prova inexistência | recuperou e pediu prova adicional | recuperou e preservou o alcance limitado da busca |
| W-C | publicação em 04/03 versus 02/03; finais possíveis 25/03 e 23/03 | recuperou os dois cenários sem escolher um | recuperou os dois cenários sem escolher um |

Os dois revisores deram realismo 4/5 aos três mundos no parecer final. Sonnet
usou confiança alta em W-A e moderada em W-B/W-C; Opus usou confiança alta nos
três. Ambos distinguiram alegação, registro bancário e reconhecimento judicial
e mantiveram aberta a ausência de decisão sobre satisfação ou extinção.

Não foi calculado placar ponderado. As rubricas pré-registraram pesos, mas não
definiram como adjudicar atendimento parcial; criar a regra depois de observar
as respostas seria uma métrica post hoc.

## Ressalvas dos revisores

O Sonnet produziu duas extrapolações que não fazem parte do gabarito: sugeriu,
como refino futuro, que a certidão de publicação deveria prevalecer em W-C e
mencionou multa e honorários além do resumo normativo fornecido. Seu próprio
memorando, porém, deixou o conflito sem solução e calculou corretamente os dois
cenários. As extrapolações são falhas do revisor, não vazamentos do corpus.

O Opus aprovou o gate e registrou como backlog de realismo: comprovante sem
identificação bancária completa; demonstrativo pouco discriminado; extrato
processual resumido; naturalidade da busca bancária pedida pela própria
executada; e redação ambígua de "data indicada para a publicação". Nenhum desses
achados altera a distinguibilidade dos mundos. Alterá-los agora invalidaria o
par final e exigiria nova rodada.

## Contabilidade das chamadas diretas

| Etapa | Modelo | Gate | Custo |
| --- | --- | --- | ---: |
| revisão 1 | Opus 5 | `REDESENHAR` | US$ 0,464315 |
| revisão 1 | Sonnet 5 | `REDESENHAR` | US$ 0,198246 |
| revisão 2 | Sonnet 5 | `REDESENHAR` | US$ 0,295094 |
| revisão 3 | Sonnet 5 | `CONSTRUIR P0` | US$ 0,223132 |
| revisão 3 | Opus 5 | `CONSTRUIR P0` | US$ 0,346955 |
| **Total direto válido** |  |  | **US$ 1,527742** |

A sequência corretiva autorizada — revisão 2 do Sonnet, repetição na revisão 3
e Opus na revisão 3 — custou US$ 0,865181, abaixo do teto agregado de US$ 2.

Antes das inferências válidas da revisão 1, uma primeira requisição de cada
braço recebeu HTTP 400 porque o schema bruto continha `minimum` e `maximum`,
restrições recusadas por structured outputs. Não houve resposta de modelo nem
campo `usage`. O runner passou a retirar somente esses dois campos do schema
enviado à API e preservou os limites 1–5 no validador local. Os HTTP 400 não
são tratados como recibo de custo zero porque a API não devolveu faturamento.

## Histórico rejeitado do Claude Code

As pastas `*-max-advisor-invalid/` permanecem como evidência negativa. O Claude
Code introduziu o tool server-side `advisor`: o braço pedido como Sonnet
faturou Sonnet, Opus e Haiku; o braço pedido como Opus faturou Opus e Haiku.
Esses pareceres não entraram na comparação.

O custo comprovado desse histórico é US$ 2,93889375. Somado às cinco chamadas
diretas válidas, o custo com recibo é US$ 4,46663575. Quatro inferências antigas
do CLI não preservaram recibo; pelos tetos configurados, poderiam acrescentar
até US$ 16,00.

Documentação oficial relacionada:

- <https://platform.claude.com/docs/en/agents-and-tools/tool-use/advisor-tool>
- <https://platform.claude.com/docs/en/agents-and-tools/tool-use/server-tools>

## Próximo movimento

Esse movimento foi executado: a revisão 3 virou seed, o P0 passou a admitir
múltiplas especificações e o lote gerou 12 assuntos/36 mundos. O canário do
lote por Sonnet 5 e Opus 5, inclusive as falhas e correções intermediárias,
está documentado em `../batch-model-reviews/README.md`. O próximo gate é a
prova cega dos oito assuntos restantes antes da adaptação a `run_evals.py`.

Construção local do P0 não autoriza, por si só, release, publicação, anúncio ou
execuções pagas adicionais.

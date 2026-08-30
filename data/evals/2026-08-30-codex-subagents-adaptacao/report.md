# Avaliação comportamental A01–A14 com subagentes Codex

Data: 2026-08-30

## Resultado

- Primeira passagem: **13 PASS / 1 FAIL**.
- Falha: **A01**, porque a resposta não preservou expressamente tutela como
  complemento da petição inicial.
- Correção: uma regra na skill de redação passou a exigir a hierarquia entre
  módulo-base candidato e complementos. A fixture e a régua do juiz não foram
  alteradas.
- Regressão A01 com executor e juiz novos: **PASS**.
- Estado efetivo: **14/14**, sendo A01 verde somente após correção e segunda
  execução. Não houve passagem única perfeita.

## Método

Três subagentes executores receberam somente prompt e pacote materializado, sem
`expected_skill`, invariantes ou resultados esperados. As 14 respostas foram
congeladas e identificadas por SHA-256 antes de três outros subagentes julgarem
roteamento, gate de redação e cada invariável. A regressão A01 usou executor e
juiz novos, ambos sem acesso aos resultados anteriores.

Nenhum agente usou rede, Claude CLI ou API externa. A execução consumiu a
franquia do Codex, mas o harness não forneceu recibo de tokens ou custo em
dólares.

## Cobertura observada

Os quatro consumidores foram roteados como esperado. As saídas preservaram
frentes, lentes, conflitos, fontes controladoras, estados de escopo, prazos não
verificados e bloqueios de redação. Os regimes tributário, trabalhista, penal,
fiduciário e de precatórios permaneceram fora do fallback cível. Nenhum cenário
leu módulo de redação antes de autorização.

## Limites da prova

Executores e juízes usam a mesma família de modelos, então há risco de erro
correlacionado. Os cenários de cada lote compartilharam contexto. Os pacotes são
sintéticos, embora derivados de classes observadas em casos reais. Esta rodada
não prova o produtor, runtime, dogfood, uso humano ou adoção.

Os hashes e vereditos completos estão em `report.json`; as respostas e os
julgamentos brutos permanecem nos arquivos `executor-*.json` e `judge-*.json`
deste diretório.

# Avaliação comportamental A01–A14 com subagentes Codex

Data: 2026-08-30

> **INVALIDADA.** A revisão do commit `10d7337` demonstrou que o materializador
> associava fatos, achados e frentes por posição. Os vereditos abaixo são
> preservados como histórico, mas não provam os cenários pretendidos.

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

Segundo o protocolo operacional da sessão, três subagentes executores receberam
somente prompt e pacote materializado, sem `expected_skill`, invariantes ou
resultados esperados. As respostas foram gravadas antes do julgamento por
agentes distintos. Os recibos finais não registram hashes das entradas antes do
despacho, identidade dos agentes ou ordem temporal; portanto, cegueira,
congelamento e independência não são auditáveis por terceiro nesta rodada.

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

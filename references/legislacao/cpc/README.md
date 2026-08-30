# Biblioteca canônica do CPC

Esta biblioteca contém o texto integral dos artigos usados pelo workflow cível
inicial. A fonte única é o [texto compilado da Lei nº 13.105/2015 no
Planalto](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105compilada.htm).

## Organização

- `parte-geral-e-prazos.md`: contraditório, contagem e termos processuais;
- `procedimento-comum.md`: tutela provisória dos arts. 294–311, petição
  inicial, defesa, réplica, saneamento e decisão;
- `provas.md`: regras gerais, documentos, testemunhas e perícia;
- `incidentes-e-provas.md`: desconsideração da personalidade jurídica,
  produção antecipada e exibição;
- `audiencia.md`: conciliação, instrução e razões finais;
- `recursos.md`: regras gerais, apelação, agravo de instrumento e embargos de
  declaração;
- `cumprimento-e-execucao.md`: liquidação, cumprimento, execução de título
  extrajudicial, constrição e embargos;
- `procedimentos-especiais.md`: procedimentos especiais contenciosos
  selecionados dos arts. 539–718;
- `inventario-partilha.md`: inventário, dívidas, partilha, arrolamentos e
  sobrepartilha;
- `jurisdicao-voluntaria.md`: regime geral e procedimentos dos arts. 719–770;
- `recursos-avancados.md`: ação rescisória, agravo interno, REsp, RE e agravo
  contra inadmissão;
- `manifest.json`: IDs granulares que apontam para o artigo integral.

## Regra de uso

Os módulos citam IDs como `CPC:art-319`, `CPC:art-319:inc-II` ou
`CPC:art-334:par-8`. Cada ID resolve para a âncora do artigo completo; a skill
deve ler o artigo inteiro antes de aplicar uma subparte.

O corpus não duplica o mesmo artigo em arquivos diferentes. Quando uma questão
exigir dispositivo ainda ausente, acrescente o artigo integral ao arquivo
temático adequado, crie os IDs necessários e atualize a data única do corpus.

## Atualização e vigência

`updated_at` no manifesto é a data em que o corpus foi rechecado. Não se mantém
data de captura por artigo. A revisão de 2026-08-30 conferiu no HTML compilado
oficial os arts. 294–311 e os 235 artigos acrescentados para incidentes,
liquidação, execução, procedimentos especiais e recursos avançados; preservou
o restante do recorte já verificado em 2026-08-20.

A conferência mecânica garante correspondência de texto, ordem e subdivisões
com a fonte usada. Ela não substitui a análise de vigência, vacatio legis,
revogação, controle de constitucionalidade ou regra especial aplicável ao caso.
O retorno da ferramenta do Silo para texto e URL do Planalto também não deve ser
descrito como certidão de vigência.

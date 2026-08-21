# Biblioteca canônica do CPC

Esta biblioteca contém o texto integral dos artigos usados pelo workflow cível
inicial. A fonte única é o [texto compilado da Lei nº 13.105/2015 no
Planalto](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105compilada.htm).

## Organização

- `parte-geral-e-prazos.md`: contraditório, contagem e termos processuais;
- `procedimento-comum.md`: tutela essencial, petição inicial, defesa, réplica,
  saneamento e decisão;
- `provas.md`: regras gerais, documentos, testemunhas e perícia;
- `audiencia.md`: conciliação, instrução e razões finais;
- `recursos.md`: regras gerais, apelação, agravo de instrumento e embargos de
  declaração;
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
data de captura por artigo. A revisão de 2026-08-20 utilizou o HTML compilado
oficial atualizado em 5/08/2026 e verificou separadamente alterações publicadas
em 2026 que poderiam afetar o escopo selecionado.

A conferência mecânica garante correspondência de texto, ordem e subdivisões
com a fonte usada. Ela não substitui a análise de vigência, vacatio legis,
revogação, controle de constitucionalidade ou regra especial aplicável ao caso.
O retorno da ferramenta do Silo para texto e URL do Planalto também não deve ser
descrito como certidão de vigência.

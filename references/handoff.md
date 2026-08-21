# Contrato comum de handoff

Este contrato permite que uma skill consuma o resultado de outra sem depender
de JSON, banco de dados ou um tipo específico de plataforma. O handoff pode ser
um arquivo Markdown, uma fonte do Projeto ou um bloco copiável na conversa.

## Quando um handoff é válido

O artefato receptor verifica quatro elementos antes de usar o conteúdo:

1. tipo do artefato;
2. escopo efetivamente analisado;
3. fontes consumidas e seus localizadores;
4. conteúdo confirmado e alcance da confirmação humana.

Um resumo solto, documento bruto ou narrativa não interpretada não se torna
handoff válido apenas por estar disponível no contexto. Ausência de um campo
material deve ser registrada como lacuna; não complete por inferência silenciosa.

## Dez campos lógicos

| Campo | Conteúdo mínimo |
|---|---|
| **Caso** | Identificador ou título inequívoco. |
| **Tipo de artefato** | Intake, análise documental, mapa jurídico, pesquisa, aprofundamento ou redação. |
| **Fontes consumidas** | Documentos e artefatos usados, com identificadores e localizadores. |
| **Escopo** | O que foi analisado e o que ficou fora. |
| **Achados** | Resultado produzido, sem apagar divergências. |
| **Estado** | Estado individual de cada achado relevante. |
| **Confirmação humana** | Conteúdo confirmado e alcance exato da confirmação. |
| **Lacunas** | Documentos, informações, verificações ou decisões ausentes. |
| **Atualização** | Relação com artefatos anteriores e delta produzido. |
| **Próximas rotas** | Skills ou providências capazes de consumir o resultado. |

Nem todo campo precisa conter achados positivos, mas campos inaplicáveis devem
ser marcados como `não aplicável`, e não omitidos de modo ambíguo.

## Estados dos achados

- `confirmado`: aceito pelo usuário para uso posterior dentro do alcance
  registrado; não significa verdade universal nem elimina ressalvas da fonte;
- `informado pelo usuário`: relato ainda não corroborado documentalmente;
- `inferido`: conclusão derivada de elementos identificados, com raciocínio
  exposto;
- `hipótese`: explicação ou possibilidade ainda dependente de teste;
- `contraditado`: há fonte ou versão incompatível, que deve permanecer visível;
- `pendente`: falta informação, documento, verificação ou decisão necessária.

O estado pertence ao achado, não ao documento inteiro. Um mesmo artefato pode
conter itens em estados diferentes.

## Confirmação humana

A confirmação registra:

- quais achados, escolhas ou limites foram apresentados;
- quais foram aceitos, rejeitados ou mantidos pendentes;
- para qual uso posterior valem;
- qual conteúdo ficou expressamente fora da confirmação.

Confirmação de fatos interpretados não autoriza redação. Antes de qualquer
minuta existe uma confirmação própria do briefing de redação. Confirmação de
redação também não autoriza ação externa.

## Atualização por delta

Para documento ou informação nova, classifique cada ponto afetado:

| Delta | Efeito |
|---|---|
| `confirma` | Reforça o achado anterior sem mudar seu conteúdo material. |
| `complementa` | Acrescenta conteúdo compatível sem eliminar o anterior. |
| `contradiz` | Introduz incompatibilidade que deve permanecer aberta ou ser resolvida. |
| `substitui` | Torna um ponto anterior inadequado e registra qual versão passa a controlar. |
| `não afeta` | Não altera o achado anterior. |

Documento novo não invalida automaticamente a análise anterior. Preserve os
pontos não afetados e retorne à confirmação somente conteúdo novo, contradito,
complementado ou substituído.

## Template legível

```markdown
# Handoff — {caso}

## Caso
{identificador e lente representada}

## Tipo de artefato
{tipo e finalidade}

## Fontes consumidas
{fonte, identificador, localizador e qualidade}

## Escopo
{incluído e excluído}

## Achados
{achado, estado, fonte e localizador}

## Estado
{síntese dos estados sem apagar a classificação individual}

## Confirmação humana
{confirmado, rejeitado, pendente, alcance e exclusões}

## Lacunas
{ausência, impacto e próxima forma de verificação}

## Atualização
{artefato anterior e deltas ponto a ponto, ou primeira versão}

## Próximas rotas
{opções consumíveis; nenhuma ação externa presumida}
```

## Recebimento por outra skill

Ao receber o handoff:

1. confirme que ele corresponde ao mesmo caso e à lente correta;
2. verifique tipo, fontes, escopo e confirmação;
3. aceite apenas achados compatíveis com o pré-requisito da tarefa atual;
4. preserve lacunas e estados sem promovê-los;
5. repare somente o pré-requisito ausente;
6. produza novo handoff com a relação e o delta para o artefato anterior.

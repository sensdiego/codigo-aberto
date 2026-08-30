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

## Pacote adaptado de caso real

Quando um sistema que possui fontes privadas adaptar o estado de um caso para
estas skills, ele declara antes dos handoffs:

- versão do contrato de adaptação;
- identificador inequívoco ou opaco do caso;
- momento da geração;
- autoridade usada para identidade e lente;
- elegibilidade, cobertura e bloqueios;
- artefatos incluídos e omitidos;
- declaração de que nenhuma ação externa ocorreu.

A única versão reconhecida neste contrato é `case-adaptation-v1`. A simples
presença de um handoff comum não o transforma em pacote adaptado: sem recibo de
adaptação, o consumidor segue o contrato comum e não exige campos desta seção.

Estados de elegibilidade:

- `bloqueado`: entrega somente identidade mínima e recibo de bloqueios, sem
  pacote consumível;
- `parcial_utilizavel`: entrega pacote com limites materiais e temporais
  explícitos;
- `integral`: exige recibo positivo próprio e nunca é inferido pela ausência de
  bloqueios.

Todo pacote em `parcial_utilizavel` ou `integral` contém handoff de tipo
`intake`. Ele pode conter `análise documental` somente quando cada achado tiver
proposição delimitada, fonte, localizador, estado, cobertura, relação com a
lente e alcance da confirmação. O adaptador não emite automaticamente mapa
jurídico, pesquisa, decisão ou redação.

Versão desconhecida, identidade incompatível ou elegibilidade ausente falham
fechadas. O consumidor usa somente conteúdo compatível com o contrato que
compreende e devolve o restante como lacuna.

Para cada frente, o recibo declara também `scope_status`: `suportado`,
`suportado_condicionado`, `nao_suportado` ou `indeterminado`. O estado
condicionado nomeia a fonte ou capacidade ausente. Os dois últimos bloqueiam
seleção de módulo; o condicionado bloqueia somente a conclusão dependente.

## Dez campos lógicos

| Campo | Conteúdo mínimo |
|---|---|
| **Caso** | Identificador ou título inequívoco. |
| **Tipo de artefato** | Intake, análise documental, mapa jurídico, pesquisa, aprofundamento, decisão ou redação. |
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

## Handoff de decisão

O tipo `decisão` registra o resultado da deliberação. Além dos dez campos
comuns, ele carrega:

- opções escolhidas, rejeitadas e condicionais, com a condição de cada uma;
- razões da escolha e das rejeições;
- prioridades do advogado;
- concessões admitidas e proibições expressas;
- pré-requisitos da rota escolhida;
- escopo da decisão;
- pendências com dono e prazo;
- condição de reabertura — o fato ou a verificação que devolve a decisão à
  deliberação;
- próxima rota.

A redação consome o handoff de decisão com o mesmo checklist de recebimento
dos demais tipos; nenhuma verificação adicional é exigida. A decisão
registrada informa o briefing e não autoriza redação.

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

Quando o tipo for `decisão`, acrescente:

```markdown
## Opções
{escolhidas, rejeitadas e condicionais, com razões e condições}

## Prioridades, concessões e proibições
{o que o advogado priorizou, admitiu ceder e vedou}

## Pré-requisitos e escopo
{o que precisa existir para a rota escolhida; limites da decisão}

## Pendências
{item, dono e prazo}

## Condição de reabertura
{fato ou verificação que reabre a deliberação}
```

Quando o caso tiver processo em andamento ou mais de uma frente, pode
acrescentar:

```markdown
## Frentes

### {front_id}
- Natureza: {processo, recurso, incidente, reconvenção, execução, crédito,
  administrativo ou dependência}
- Relação: {principal, dependente, paralelo, sucessor ou apenso}
- Jurisdição/regime: {demonstrado e pendente de verificação}
- Estado de escopo: {suportado | suportado_condicionado | nao_suportado |
  indeterminado}
- Lente na frente: {parte ou papel representado}
- Estado: {ativa | dependente | latente | encerrada | indeterminada}
- Fase: {fase demonstrada e fonte}
- Evento controlador: {fonte, localizador e data pertinente}
- Objetivo atual: {resultado operativo informado ou confirmado}
- Ato: {demonstrado | candidato | decidido | indeterminado | sem_ato}
- Prazo: {evento inicial e estado da verificação}
- Cobertura: {integral | parcial | bloqueada}
- Dependências: {frente, documento, cálculo, pesquisa ou decisão}
```

`decidido` exige escolha humana registrada. `demonstrado` significa somente
que a necessidade do ato consta de fonte direta; cabimento e seleção do módulo
continuam pertencendo ao mapa jurídico e ao briefing. Espécie da ação, nome do
arquivo e título extraído são sinais, não autoridade sobre o ato atual.

## Recebimento por outra skill

Ao receber o handoff:

1. quando houver pacote adaptado, verifique versão, elegibilidade e recibo;
2. confirme que ele corresponde ao mesmo caso e à lente correta;
3. selecione a frente material ao pedido e verifique seu evento controlador;
4. verifique tipo, fontes, escopo e confirmação;
5. aceite apenas achados compatíveis com o pré-requisito da tarefa atual;
6. preserve lacunas e estados sem promovê-los;
7. bloqueie seleção de ato se a frente, o regime ou o evento estiverem
   indeterminados;
8. repare somente o pré-requisito ausente;
9. produza novo handoff com a relação e o delta para o artefato anterior.

Um handoff comum criado diretamente pelo usuário ou por outra skill permanece
válido sem pacote adaptado, desde que satisfaça seus dez campos e os
pré-requisitos da tarefa receptora. Compatibilidade não permite inventar
recibo, elegibilidade, frente ou estado de escopo ausente.

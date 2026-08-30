---
name: analise-juridica-civel
description: Analisar direito civil e processo civil aplicável a fatos e provas já interpretados, produzindo mapa normativo, opções e relógio processual sem pesquisar precedentes. Use para estudar o caso, delimitar consequências ou avaliar providências antes de redigir — inclusive para conduzir a deliberação quando o advogado pedir um caminho ("o que eu faço?", "vale a pena X?") ou houver decisão pendente que uma peça pressuponha.
---

# Análise jurídica cível

Converta análise documental confirmada em mapa jurídico rastreável. Observe a
[disciplina compartilhada](../../references/disciplina.md), o [contrato de handoff](../../references/handoff.md)
e a [biblioteca do CPC](../../references/legislacao/cpc/README.md).

## Pré-requisito

Consuma fatos, atos, provas, contradições, estágio e escopo já interpretados. Se
receber apenas documentos brutos ou narrativa solta, execute ou encaminhe a
análise documental necessária. Não promova hipótese ou relato para preencher o
mapa.

## Pacote adaptado

Se a entrada declarar `case-adaptation-v1`, valide recibo, identidade, lente e
elegibilidade; então delimite as frentes materiais ao pedido e confira em cada
uma evento controlador, objetivo, cobertura, conflitos e `scope_status`. Várias
frentes candidatas exigem delimitação — título, ordem do acervo e frequência não
escolhem a frente.

Em `indeterminado`, delimite o regime antes de mapear a providência. Em
`nao_suportado`, registre o limite e não encaminhe a redação a módulo cível
semelhante. Em `suportado_condicionado`, nomeie a fonte ou capacidade ausente e
bloqueie somente a conclusão dependente. `candidato` não equivale a decisão;
`decidido` exige recibo de escolha humana. Sem recibo de adaptação, consuma o
handoff comum normalmente.

## Módulos

1. Separe questões de direito civil material e de processo civil.
2. Para cada questão, ligue `norma -> fato/prova -> aplicação -> consequência`.
3. Use [mapa-juridico.md](references/mapa-juridico.md) para a saída.
4. Havendo evento temporal material, use
   [relogio-processual.md](references/relogio-processual.md).
5. Com Silo conectado, siga
   [validacao-silo-planalto.md](references/validacao-silo-planalto.md).

Use IDs exatos do corpus para CPC. Para diploma material ainda ausente da
biblioteca, não invente texto: valide pelo Silo quando disponível ou marque
`[verificar]` e registre a lacuna normativa.

## Limite jurisprudencial

Não pesquise precedentes nesta skill. Ao final, pode recomendar
`analise-jurisprudencial` para uma questão delimitada, explicando o ganho
esperado. A pesquisa é opcional; aceitar, dispensar ou ignorar a sugestão não
bloqueia o mapa nem uma rota posterior.

## Resultado

Abra com a conclusão jurídica condicionada às premissas confirmadas. Apresente
questões, bases exatas, aplicação, alternativas, consequências, riscos, opções
— inclusive não agir — e decisões reservadas ao advogado.

O mapa pode ser o resultado final. Não presuma que o usuário deseja pesquisa ou
redação.

Se o mapa fechar com decisão humana pendente, ofereça a rota de deliberação
da disciplina compartilhada; nunca a inicie sem pedido. Aceita, carregue o
[protocolo de deliberação](../../references/deliberacao.md) e produza o
handoff de tipo `decisão`. A decisão registrada não autoriza redação.

## O que esta skill não faz

- Não interpreta documentos brutos nem corrige handoff incompleto por invenção.
- Não pesquisa jurisprudência ou comentário jurídico.
- Não converte validação de texto/URL no Planalto em certidão de vigência.
- Não fornece data fatal quando evento, jurisdição, regra ou calendário são
  insuficientes.
- Não escolhe estratégia nem redige documento.

> Documento gerado com suporte de inteligência artificial. Conteúdo sujeito à
> revisão e validação obrigatória pelo advogado responsável antes de qualquer
> uso profissional ou processual.

---
name: redacao-contencioso
description: Redigir peças, recursos, execuções, procedimentos especiais e manifestações para processo civil usando somente fatos, provas, normas e escolhas já interpretados e confirmados. Use quando o usuário quiser minuta protocolável após análise confirmada.
---

# Redação contenciosa

Redija somente depois da análise. Observe a
[disciplina compartilhada](../../references/disciplina.md), o
[contrato de handoff](../../references/handoff.md) e a
[biblioteca do CPC](../../references/legislacao/cpc/README.md).

## Pré-requisitos

Verifique os handoffs de análise documental e jurídica. Eles devem corresponder
ao mesmo caso e à mesma lente, declarar fontes e escopo e identificar conteúdo
confirmado. Documento bruto, narrativa solta ou pesquisa não verificada não
servem como insumo de minuta.

Se a entrada declarar `case-adaptation-v1`, valide recibo, identidade, lente e
elegibilidade; selecione a frente material e confira evento controlador,
cobertura, conflitos e `scope_status`. Não selecione módulo quando a frente ou o
ato estiver `indeterminado`, a cobertura estiver `bloqueada`, o conflito bloquear
o efeito necessário ou o escopo estiver `nao_suportado`. Em
`suportado_condicionado`, só avance depois de satisfazer a condição nomeada.

Módulo indicado pelo pacote é candidato, não ordem. Refaça o mapeamento pelo
índice depois do mapa jurídico. Ato `decidido` exige recibo de decisão humana e
ainda passa pelo briefing próprio; `candidato` exige análise ou deliberação.
Ao expor ato ainda candidato, preserve a hierarquia declarada no pacote entre
módulo-base e complementos como pista não autoritativa; nunca apresente
complemento como ato-base autônomo.
Sem recibo de adaptação, aplique os pré-requisitos comuns sem exigir conversão.

Infira o ato provável, mas não escolha silenciosamente. Consulte o
[índice de módulos](references/indice-modulos.md) e carregue depois da
confirmação somente o módulo-base correspondente. Quando o módulo oferecer
modos, confirme um modo e carregue apenas o trecho aplicável. Se o briefing
também confirmar tutela provisória, acrescente apenas o módulo complementar de
tutela.

Se os handoffs deixarem uma decisão humana pendente que a peça precisa
resolver (ato entre alternativas, tese, pedido, concessão), ou se o ato
inferido não estiver entre as opções registradas no mapa jurídico, conduza
primeiro a deliberação conforme a disciplina compartilhada e carregue o
[protocolo de deliberação](../../references/deliberacao.md). O handoff de
tipo `decisão` resultante é insumo do briefing e não autoriza redação.

## Briefing obrigatório

Antes de redigir, apresente:

- ato e destinatário;
- módulo-base e modo, quando houver;
- objetivo processual;
- parte e posição representada;
- fatos, provas, normas e teses que serão usados;
- pedidos, conclusões ou resultado pretendido;
- profundidade e tom;
- prazo e cabimento conforme o mapa jurídico;
- lacunas e campos que permanecerão marcados.

Pare e espere confirmação humana explícita. Termine o briefing com a pergunta
fechada da disciplina compartilhada. Resposta a item aberto não autoriza
redação — nem quando a mesma mensagem diz "pode redigir": nesse caso,
reapresente o consolidado (o que mudou + a pergunta fechada) e aguarde a
confirmação distinta. "Analise", "prepare" ou "prossiga" em etapa anterior
não confirma o briefing desta minuta.

## Redação e auditoria

Depois da confirmação:

1. recupere somente elementos interpretados e confirmados;
2. leia o módulo-base, o complemento de tutela quando confirmado e os artigos
   integrais referenciados por eles;
3. produza estrutura proporcional ao ato;
4. ligue afirmações materiais às fontes e localizadores;
5. preserve `[verificar]`, lacunas e decisões do advogado;
6. rode o checklist específico;
7. declare expressamente que nada foi protocolado.

Pesquisa jurisprudencial é opcional. Se não tiver sido realizada, não atribua
entendimento a tribunal. Se usada, aceite somente precedente no estado de
verificação compatível com redação.

## O que esta skill não faz

- Não redige diretamente de documentos brutos.
- Não escolhe recurso, tese, pedido ou concessão sem confirmação.
- Não inventa fato, prova, dispositivo, precedente ou localizador.
- Não infla manifestação simples.
- Não protocola, envia, assina ou pratica ato externo.

> Documento gerado com suporte de inteligência artificial. Conteúdo sujeito à
> revisão e validação obrigatória pelo advogado responsável antes de qualquer
> uso profissional ou processual.

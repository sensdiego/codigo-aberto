# Guia rápido

## Escolha pelo resultado

- “Recebi documentos de um cliente novo” → `novo-caso`.
- “Organize fatos, atos e provas” → `analise-documental`.
- “Quais regras civis e processuais se aplicam?” → `analise-juridica-civel`.
- “Pesquise como os tribunais tratam a questão” →
  `analise-jurisprudencial` (opcional e dependente do Silo).
- “Estresse esta tese” ou “prepare a audiência” →
  `aprofundamento-juridico`.
- “Redija a peça” → `redacao-contencioso`.
- “Redija parecer, relatório ou e-mail” → `redacao-consultivo`.

Você pode começar por qualquer pedido. Se faltar um pré-requisito, a skill deve
reparar somente esse trecho.

## Antes de redigir

A redação usa fatos, provas, normas e escolhas já interpretados. A skill
apresenta documento, destinatário, objetivo, posição, profundidade, conteúdo e
lacunas e espera confirmação explícita.

Nenhuma entrega significa que houve protocolo, envio, assinatura ou outro ato
externo.

## Pesquisa jurídica

O corpus local cobre o recorte do CPC usado pelas skills. Validação externa de
legislação e pesquisa de precedentes dependem do Silo conectado. Sem essa
capacidade, a skill informa a limitação e não apresenta pesquisa simulada.

## Instalação

### Claude Code

```bash
claude plugin marketplace add sensdiego/codigo-aberto
claude plugin install silo-legal@codigo-aberto
```

### ChatGPT

O ChatGPT não possui área de instalação para skills de terceiros: o diretório
de skills do runtime é somente leitura. O caminho comprovado (2026-08-24,
inclusive com conferência do checksum dos pacotes) é o modelo montar o ZIP
dentro da própria conversa. O menor atrito é via projeto:

1. Abra a [release mais recente](https://github.com/sensdiego/codigo-aberto/releases/latest)
   e baixe os arquivos `.zip` das skills nos assets.
2. Crie um projeto no ChatGPT e envie os ZIPs a ele uma única vez, sem
   descompactá-los.
3. Nas configurações do projeto, defina as instruções permanentes:

   > Este projeto contém skills jurídicas como arquivos ZIP no acervo. Em toda
   > conversa, identifique pela mensagem qual skill se aplica, monte o ZIP
   > correspondente e siga o `SKILL.md` fielmente, lendo as referências
   > internas quando necessário.

4. Converse normalmente: o modelo identifica a skill, monta o pacote do acervo
   e segue a disciplina — comprovado sem citar o nome da skill no pedido.

Fora de um projeto, anexe o `.zip` à conversa e instrua explicitamente:

> Use exclusivamente a skill contida no ZIP anexo: monte o pacote e siga o
> `SKILL.md` fielmente, lendo as referências internas quando necessário.

Os sete ZIPs são autossuficientes: cada um contém o `SKILL.md` e as referências
necessárias àquela skill. `pesquisa-silo` e `assinatura-silo` não são bundles de
upload; elas dependem da disponibilidade do conector autenticado.

## Exemplo sintético de ponta a ponta

O caso abaixo é inteiramente fictício. Ele demonstra o fluxo sem ensinar a
enviar dados reais ao modelo.

### Prompt inicial

> A Empresa Horizonte, fictícia, foi cobrada em R$ 18.000 por materiais de
> escritório. A inicial está em `INI-01`, páginas 1–7. O contrato `CTR-01`,
> cláusula 4, prevê pagamento em 30 dias. Há comprovante de R$ 12.000 em
> `COMP-01` e o e-mail `EM-01`, mensagem 3, registra que o fornecedor aceitou a
> devolução dos R$ 6.000 restantes. A data da juntada da citação não foi
> informada. Organize o caso e prepare uma contestação, mas não invente o prazo.

### Handoff esperado antes da redação

```markdown
# Handoff — SINT-001 / Empresa Horizonte

## Tipo de artefato
Análise documental e mapa jurídico para possível contestação.

## Fontes consumidas
INI-01 pp. 1–7; CTR-01 cláusula 4; COMP-01; EM-01 mensagem 3.

## Escopo
Existência e composição da cobrança; prazo processual excluído por falta da
certidão de juntada.

## Achados
- Cobrança de R$ 18.000: confirmado por INI-01 pp. 2–3.
- Pagamento de R$ 12.000: confirmado por COMP-01.
- Aceite da devolução de R$ 6.000: inferido de EM-01 mensagem 3; confirmar o
  alcance jurídico e a entrega efetiva.

## Estado
Dois achados confirmados documentalmente; um depende de confirmação e prova.

## Confirmação humana
Pendente: a pessoa usuária ainda deve confirmar os fatos, limites e objetivo.

## Lacunas
Certidão de juntada da citação; prova da entrega dos itens devolvidos.

## Atualização
Primeira versão.

## Próximas rotas
Confirmar o mapa; depois preparar briefing em `redacao-contencioso`.
```

Depois de a pessoa confirmar o mapa, a skill de redação ainda apresenta um
briefing próprio: documento, destinatário, objetivo, teses, pedidos, fontes e
lacunas. Somente uma segunda confirmação autoriza a minuta.

### Trecho de peça esperado após as confirmações

```markdown
AO JUÍZO DO PROCESSO SINTÉTICO SINT-001

EMPRESA HORIZONTE, no exercício exclusivamente demonstrativo deste exemplo,
apresenta CONTESTAÇÃO.

1. A cobrança afirma saldo de R$ 18.000 [INI-01, pp. 2–3]. O comprovante
COMP-01 documenta pagamento de R$ 12.000, ponto que deve ser impugnado de forma
específica com a juntada do documento.

2. Quanto aos R$ 6.000 restantes, EM-01, mensagem 3, registra o aceite da
devolução pelo fornecedor. A efetiva entrega dos itens permanece pendente de
prova e não deve ser apresentada como fato confirmado.

3. Requer-se o reconhecimento do pagamento comprovado e, quanto ao saldo, a
produção da prova necessária e o julgamento conforme o que ela demonstrar.

[Prazo não calculado: falta a certidão de juntada da citação.]
```

O resultado correto preserva a lacuna e não protocola, envia ou assina a peça.

## Primeiro piloto

Use uma sessão de 30 minutos com o exemplo acima:

1. Instale ou carregue a release mais recente pelo caminho do aplicativo.
2. Envie somente o prompt sintético, sem indicar o nome de uma skill.
3. Confirme se houve roteamento, leitura das fontes indicadas, handoff e duas
   barreiras de confirmação antes da minuta.
4. Registre aplicativo, versão, data, resultado e atrito observado; use o
   modelo de bug ou de sugestão do GitHub, sempre sem dados reais.

Texto de convite, pronto para copiar quando houver uma pessoa piloto nomeada:

> Estou testando um conjunto aberto de skills para trabalho jurídico cível e
> procuro uma pessoa para uma sessão remota de 30 minutos. Usaremos apenas um
> caso sintético fornecido no repositório; não envie documentos ou dados de
> clientes. O objetivo é observar instalação, clareza do fluxo e limites antes
> da redação. O teste não envolve contratação nem publicação do seu nome.

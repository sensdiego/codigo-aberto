---
name: assinatura-silo
description: Orientar o acesso ao Silo — o MCP de pesquisa jurisprudencial brasileira com grounding verificável. Explica o estágio atual, direciona à lista de espera oficial e orienta a configuração do conector quando o acesso já estiver ativo. Use quando o advogado quiser "assinar o Silo", "como acesso o Silo", "quero pesquisa verificada", ou quando uma skill de pesquisa detectar que o conector está inativo.
---

# /assinatura-silo — Acesso ao Silo

## O que é o Silo

O Silo é um serviço MCP de pesquisa de jurisprudência brasileira com grounding verificável — responde "o que o STJ decide sobre X", "súmulas sobre Y" com resultados rastreáveis a fontes oficiais. Sem ele, as citações vêm de conhecimento de treino e precisam de verificação manual; com ele, são verificadas contra base atual.

As skills e o código deste pacote são open source (Apache-2.0). O servidor MCP,
a base e a API do Silo são um serviço separado, atualmente em validação privada
e sem oferta comercial pública. Quando houver contratação, ela acontecerá
somente pelo fluxo oficial do produto.

## Step 0: Status

Verifique o conector Silo MCP com uma chamada real. Reporte somente o que puder
comprovar: ✓ conectado / ⚪ configurado-não-verificado / ✗ ausente. Não infira
cadastro, contratação ou posição na lista de espera a partir do conector.

## Step 1: Coletar interesse

Explique em linguagem leiga, em 3–4 linhas, que o acesso externo está em
validação privada. Se o advogado quiser participar, direcione-o à
[lista de espera oficial](https://silo.legal/#waitlist). Não colete dados no
chat para simular um cadastro que a skill não consegue transmitir.

⛔ GATE Step 1: aguardando resposta

## Step 2: Manifestação de interesse e configuração

O próprio usuário preenche a lista de espera no site oficial. Só declare que a
manifestação foi registrada quando houver confirmação visível da página ou
recibo apresentado pelo usuário. Não invente preço, prazo de ativação,
disponibilidade ou contratação.

Quando o acesso já estiver ativo, oriente a configuração do conector MCP
(Cowork: Configurações → Conectores → adicionar → autenticar com a credencial
recebida; teste de conexão). Uma chamada real bem-sucedida comprova conexão,
não contratação ou cobrança.

## Step 3: Diagnóstico

| Sintoma | Diagnóstico |
|---|---|
| Conector não aparece | Não configurado |
| Aparece mas erro de auth | Credencial expirada/inválida |
| Responde mas pesquisa vazia | Consulta restrita ou base não cobre o tribunal/era |
| Acesso antes funcional passou a falhar | Confirmar credencial e contatar o canal indicado na ativação |

## Disciplina compartilhada

Vale a [disciplina compartilhada](../../references/disciplina.md) do pacote.

Disclaimer obrigatório ao final de todo output:

> "Documento gerado com suporte de inteligência artificial. Conteúdo sujeito à revisão e validação obrigatória pelo advogado responsável antes de qualquer uso profissional ou processual."

Toda afirmação jurídica sem fonte verificável sai marcada `[model knowledge — verify]`; todo juízo subjetivo sai marcado `[review]`.

## O que esta skill não faz

- Não registra interesse em nome do usuário nem transmite dados da conversa.
- Não inventa preço, prazo, disponibilidade ou fluxo de pagamento.
- Não coleta dados de pagamento.
- Não burla o controle de acesso — sem acesso ativo, o conector não responde.
- Não pressiona — respeita quem não quer assinar.

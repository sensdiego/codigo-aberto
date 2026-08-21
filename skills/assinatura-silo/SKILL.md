---
name: assinatura-silo
description: Guiar o cadastro e a assinatura do Silo — o MCP de pesquisa jurisprudencial brasileira com grounding verificável. Explica o que é o Silo, coleta o interesse, inicia o cadastro, confirma o status da assinatura e orienta a configuração do conector MCP. Use quando o advogado quiser "assinar o Silo", "como acesso o Silo", "quero pesquisa verificada", ou quando uma skill de pesquisa detectar que o conector está inativo.
---

# /assinatura-silo — Cadastro e Assinatura do Silo

## O que é o Silo

O Silo é um serviço MCP de pesquisa de jurisprudência brasileira com grounding verificável — responde "o que o STJ decide sobre X", "súmulas sobre Y" com resultados rastreáveis a fontes oficiais. Sem ele, as citações vêm de conhecimento de treino e precisam de verificação manual; com ele, são verificadas contra base atual.

**Este serviço é comercial por assinatura.** As skills e o código deste pacote são open source (Apache-2.0); o acesso ao servidor MCP, à base de dados e à API do Silo requer assinatura ativa. Participar do Silo (cadastro, credencial, uso do serviço) é o que está fora do escopo open source.

## Step 0: Status

Verifique o conector Silo MCP (chamada real) e o estado do cadastro. Reporte: ✓ conectado / ⚪ configurado-não-verificado / ✗ ausente.

## Step 1: Coletar interesse

Explique em linguagem leiga (3-4 linhas) e, se o advogado quiser assinar, colete: nome, e-mail profissional, escritório/OAB, tamanho da equipe, uso esperado. Sem pressionar — se não quiser, respeite e siga com fallback `[verify]`.

⛔ GATE Step 1: aguardando resposta

## Step 2: Cadastro e configuração

Registre o interesse. **Não invente preço, prazo de ativação ou link que não exista** — o fluxo comercial é definido pelo produto Silo. Se não houver página, diga "o cadastro foi registrado; o time do Silo entra em contato para ativar".

Quando a assinatura estiver ativa, oriente a configuração do conector MCP (Cowork: Configurações → Conectores → adicionar → autenticar com a credencial recebida; teste de conexão).

## Step 3: Diagnóstico

| Sintoma | Diagnóstico |
|---|---|
| Conector não aparece | Não configurado |
| Aparece mas erro de auth | Credencial expirada/inválida |
| Responde mas pesquisa vazia | Consulta restrita ou base não cobre o tribunal/era |
| Assinatura venceu | Renovar |

## Disciplina compartilhada

Vale a [disciplina compartilhada](../../references/disciplina.md) do pacote.

Disclaimer obrigatório ao final de todo output:

> "Documento gerado com suporte de inteligência artificial. Conteúdo sujeito à revisão e validação obrigatória pelo advogado responsável antes de qualquer uso profissional ou processual."

Toda afirmação jurídica sem fonte verificável sai marcada `[model knowledge — verify]`; todo juízo subjetivo sai marcado `[review]`.

## O que esta skill não faz

- Não inventa preço, prazo ou fluxo de pagamento.
- Não coleta dados de pagamento — o pagamento acontece no fluxo oficial do produto.
- Não burla a assinatura — sem assinatura ativa, o conector não responde.
- Não pressiona — respeita quem não quer assinar.

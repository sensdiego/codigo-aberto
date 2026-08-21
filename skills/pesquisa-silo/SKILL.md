---
name: pesquisa-silo
description: Pesquisar jurisprudência brasileira diretamente via Silo MCP com verificação de fonte — consulta rápida sem o workflow completo da análise jurisprudencial. Requer assinatura ativa do Silo. Use quando o advogado pedir "pesquisa no silo", "consulta o silo", "acha isso rápido", ou "precedente sobre X" e o conector estiver ativo.
---

# /pesquisa-silo — Consulta Direta ao Silo

Consulta direta quando a velocidade importa e o advogado já sabe o que quer. Só a busca, com verificação de fonte.

## Step 0: Pré-requisito

Teste o conector Silo MCP (chamada real). Se não responder, informe o status e ofereça a skill `assinatura-silo` ou o workflow de `analise-jurisprudencial`. **Não siga com resultados de treino como se fossem do Silo.**

## Step 1: Consulta

Pergunte em um prompt: "Tema: [descrição]. Tribunal: [STF/STJ/TJ/TRF]. Tipo: [súmula/repetitivo/acórdão]." Rode a busca.

## Step 2: Resultados

```
# Pesquisa Silo — [Tema]
**Conector:** Silo MCP ✓ · **Data:** [AAAA-MM-DD]

## Resultados
### 1. [Tipo] — [tema]
- Órgão: [tribunal, turma, relator] · Nº: [processo] · Tese: [1-2 linhas] · Fonte: [Silo MCP]

## Notas
[cobertura, lacunas, conflitos entre resultados]
```

Tag `[Silo MCP]` só para citações literalmente vindas do conector. Resultado sem inteiro teor leva `[conferir inteiro teor antes de peça]`.

## Step 3: Encerramento

Rodapé CONFORMIDADE + disclaimer.

## Disciplina compartilhada

Vale a [disciplina compartilhada](../../references/disciplina.md) do pacote.

Disclaimer obrigatório ao final de todo output:

> "Documento gerado com suporte de inteligência artificial. Conteúdo sujeito à revisão e validação obrigatória pelo advogado responsável antes de qualquer uso profissional ou processual."

Toda afirmação jurídica sem fonte verificável sai marcada `[model knowledge — verify]`; todo juízo subjetivo sai marcado `[review]`.

## O que esta skill não faz

- Não opera sem conector ativo e não apresenta pesquisa simulada.
- Não fabrica precedente — o que o conector não retorna não é citado; se o advogado sugerir um precedente que o conector não confirma, marque `[review]` e peça verificação.
- Não substitui a análise de aplicação ao caso.

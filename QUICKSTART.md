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

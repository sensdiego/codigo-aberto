# Código Aberto

Skills abertas, em português brasileiro, para organizar, analisar, pesquisar,
aprofundar e redigir trabalho jurídico cível.

## Skills

| Skill | Resultado |
|---|---|
| [`novo-caso`](skills/novo-caso/SKILL.md) | Intake de acervo novo, limitado ou de processo em andamento |
| [`analise-documental`](skills/analise-documental/SKILL.md) | Fatos, atos, provas, contradições e lacunas com localizadores |
| [`analise-juridica-civel`](skills/analise-juridica-civel/SKILL.md) | Mapa normativo e processual aplicado aos fatos interpretados |
| [`analise-jurisprudencial`](skills/analise-jurisprudencial/SKILL.md) | Pesquisa opcional de precedentes pelo Silo |
| [`aprofundamento-juridico`](skills/aprofundamento-juridico/SKILL.md) | Investigação dinâmica de teses, riscos e preparação para audiência |
| [`redacao-contencioso`](skills/redacao-contencioso/SKILL.md) | Peças, manifestações e recursos cíveis |
| [`redacao-consultivo`](skills/redacao-consultivo/SKILL.md) | Pareceres, relatórios, e-mails e outros documentos consultivos |
| [`pesquisa-silo`](skills/pesquisa-silo/SKILL.md) | Consulta jurídica rápida pelo conector Silo |
| [`assinatura-silo`](skills/assinatura-silo/SKILL.md) | Orientação para a lista de espera e conexão ao Silo |

Fluxo sugerido:

`novo-caso → analise-documental → analise-juridica-civel → [jurisprudência ou aprofundamento] → [redação]`

O usuário pode começar em qualquer etapa. A skill deve identificar e reparar
somente os pré-requisitos ausentes. Pesquisa jurisprudencial e aprofundamento
são opcionais.

Antes de redigir, a IA precisa ter interpretado os fatos e materiais relevantes
e apresentar um briefing para confirmação humana explícita. Confirmar uma
minuta não autoriza protocolo, envio ou contato externo.

## Estrutura pública

```text
skills/                 produto utilizável
references/             disciplina, handoff e recorte legislativo necessário
.claude-plugin/          manifestos de distribuição
scripts/                 validação e geração de bundles
tests/fixtures/          cenários sintéticos de roteamento
```

Não fazem parte deste repositório materiais de pesquisa interna, decisões de
desenvolvimento, transcrições de testes, casos reais ou configurações pessoais.

## Uso

As skills podem ser lidas diretamente em [`skills/`](skills/) ou carregadas em
aplicativos compatíveis com Agent Skills. Veja o [guia rápido](QUICKSTART.md).

O corpus local contém o recorte do CPC necessário ao workflow. Pesquisa
jurisprudencial e validações externas usam o conector autenticado do Silo quando
disponível; a base, a API e o servidor do Silo não integram este repositório.
O acesso externo está em validação privada e pode ser solicitado pela
[lista de espera oficial](https://silo.legal/#waitlist).

Skills e código estão sob a licença [Apache-2.0](LICENSE). Para contribuir,
consulte [CONTRIBUTING.md](CONTRIBUTING.md). Versões publicadas ficam no
[changelog](CHANGELOG.md); o protocolo está em [RELEASING.md](RELEASING.md) e
as próximas fases estão no [roadmap](ROADMAP.md).

# Handoff de sessão

Atualizado em 2026-08-25, após o dogfood interno manual no Claude Cowork e o
registro da hipótese de deliberação jurídica no [ROADMAP](ROADMAP.md).

## Onde o produto está

A versão corrente continua sendo a `v0.2.4`, publicada e auditada. As nove
skills, o recorte do CPC, os sete bundles ChatGPT e a régua de treze cenários
permanecem inalterados nesta sessão. Nenhuma nova skill foi criada e nenhuma
mudança de produto ou release foi aprovada.

Claude Code e ChatGPT têm caminhos de uso comprovados. No Claude Cowork, o
dogfood foi feito manualmente em um projeto já montado com o acervo completo:
prompts foram enviados em sequência e o fluxo conseguiu ler os materiais e
produzir artefatos. Isso comprova viabilidade operacional nesse arranjo, mas
não substitui um teste de instalação limpa nem constitui piloto externo.

Nenhum dado, documento, número de processo, transcrição ou resultado do caso
real foi levado para este repositório. Os artefatos e a auditoria do exercício
permanecem fora do repositório público.

## Achados do dogfood

1. Um briefing respondido não equivale a autorização. Gate crítico só fecha
   com confirmação humana explícita depois de o agente apresentar ou
   reapresentar a ação que será executada. O desvio observado foi auditado fora
   deste repositório; uma confirmação posterior não o autoriza retroativamente.
2. A sequência análise → redação salta uma etapa importante. O advogado recebe
   conclusões, mas falta uma interação dedicada a explicar os resultados,
   comparar possibilidades e transformar preferências profissionais em uma
   decisão estratégica registrável.
3. Esse segundo problema não é mero aprofundamento. Mais pesquisa pode ser uma
   das opções, mas apresentação de resultados e decisão estratégica têm outra
   finalidade e outro contrato.

## Decisão fixada nesta sessão

A hipótese merece estudo, mas **não autoriza criar agora** uma skill
`deliberacao-juridica` nem ampliar silenciosamente uma skill existente. A
próxima sessão deve avaliar alternativas e só então decidir criar, adaptar,
adiar ou rejeitar.

A fronteira é obrigatória: não misturar essa função com
`aprofundamento-juridico`.

- `aprofundamento-juridico` continua voltado a aumentar ou testar conhecimento:
  lacunas, hipóteses, pesquisa, argumentos e cenários;
- a camada deliberativa, se aprovada, apresenta uma análise suficientemente
  madura, oferece opções, entrevista o advogado e registra sua decisão;
- a deliberação pode mandar aprofundar, buscar documentos, negociar, aguardar,
  não agir ou redigir;
- deliberação concluída não autoriza redação. `redacao-contencioso` mantém
  briefing e gate próprios.

## Próxima tarefa com maior impacto: estudar a camada deliberativa

Esta é a frente principal da próxima sessão. A sessão deve começar pela
avaliação, não pela criação de arquivos ou de uma skill.

1. Mapear os contratos atuais de saída das análises e de entrada de
   `aprofundamento-juridico` e `redacao-contencioso`, identificando exatamente
   onde a responsabilidade deliberativa começa e termina.
2. Comparar pelo menos quatro alternativas: skill autônoma; protocolo/handoff
   compartilhado sem nova skill; ajustes explícitos nos contratos das skills
   existentes; adiamento ou rejeição.
3. Definir gatilhos de entrada e saída, rotas de retorno para pesquisa ou
   documentos, relação com urgência e o ponto em que uma decisão pode seguir
   para redação.
4. Especificar o comportamento mínimo: apresentar conclusão, evidências,
   confiança, incertezas e contra-argumento; mapear de duas a quatro opções;
   recomendar com confiança; entrevistar com uma pergunta de maior valor por
   vez; e produzir um handoff de decisão.
5. Definir o conteúdo mínimo desse handoff: opções escolhidas, rejeitadas e
   condicionais; razões; prioridades; concessões e proibições; pré-requisitos;
   escopo; pendências; e próxima rota.
6. Desenhar cenários sintéticos que permitam comparar a solução com o salto
   direto da análise para a redação, incluindo um caso em que a decisão correta
   seja não redigir.
7. Encerrar a sessão com decisão explícita e justificada: criar, adaptar, adiar
   ou rejeitar. Se a decisão for criar, a implementação fica para uma frente
   posterior, com cenário de avaliação definido antes da edição da skill.

Critério de aprovação: a alternativa precisa melhorar a decisão do advogado,
continuar útil quando o destino não for uma peça, ter custo cognitivo e de
manutenção justificável e impedir que contexto ou respostas de entrevista
sejam tratados como autorização implícita.

## Pendências secundárias

- Documentar e testar a preparação limpa de um projeto no Claude Cowork; o
  dogfood atual começou com o acervo já disponível.
- Avaliar um cenário sintético que torne o gate explícito e determinístico sem
  depender de interpretação de autorização implícita.
- Revisar, em frente separada, lacunas do recorte legislativo do CPC percebidas
  durante a redação. Não misturar essa manutenção com o estudo deliberativo.
- Não iniciar piloto externo ou anúncio público nesta etapa; a decisão atual é
  continuar o dogfood interno manual.

## Avisos operacionais

- O plugin local do Claude Code está na `v0.2.4`; re-medições futuras devem
  conferir a versão instalada antes de rodar (`claude plugin list`).
- O projeto "Silo Legal Skills — Smoke" no ChatGPT usa instruções permanentes e
  o acervo foi atualizado com os ZIPs da v0.2.4 em 2026-08-24.
- A rodada completa de evals custa aproximadamente US$ 6 e é sempre manual:
  `python3 scripts/run_evals.py`.

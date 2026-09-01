# Veredicto — dogfood pareado da camada deliberativa (v0.6.1)

Data: 2026-09-01. Caso: `caso/CASO.md` (sintético, inédito). Braços:
A = salto direto (`registro-sessao-a.md`); B = protocolo
(`registro-sessao-b.md`). Ordem A → B, mesmo operador, mesmas prioridades de
cliente (`contexto-advogado.md`). Plugin `silo-legal@codigo-aberto` v0.6.1,
Claude Code 2.1.251.

## Comparação contra o critério de manutenção

### (a) Decisão melhorada? **Sim, materialmente.**

- **Braço A** produziu: executar agora, em silêncio sobre a proposta de
  acordo. A escolha estratégica (abandonar a janela de negociação) aconteceu
  implícita no pedido inicial e nunca foi problematizada: o produto exibiu os
  riscos anotados no handoff, mas não perguntou prioridades do cliente, e o
  briefing só cobriu decisões táticas da peça. Contra a folha do advogado,
  essa decisão está **errada para o cliente**: o mandato real era tentar
  acordo com garantia por ~duas semanas e só então executar.
- **Braço B** produziu: contraproposta com garantia em janela datada, piso de
  valor, forma de pagamento, execução autorizada condicionalmente no gatilho,
  minuta preparada em paralelo, duas proibições de mesa (sem garantia nunca;
  não sinalizar a restrição do CEO) e uma pendência não jurídica com dono
  (homologação do F-40). É uma decisão diferente da de A **e** endossada
  pelo mandato da folha.
- O advogado, vendo as duas, endossa B: A teria queimado a janela negocial,
  entregado a alavanca e ainda assim carregado o risco relacional que o CEO
  vetou — exatamente o modo de falha que a camada deliberativa foi desenhada
  para impedir.

### (b) Útil sem redação? **Sustentado, com ressalva de cobertura.**

A rota de saída de B foi redigir (contraproposta + minuta em paralelo), e a
sessão parou antes dos briefings — o valor entregue até ali foi só a
decisão: destino das três opções, gatilhos, proibições e pendência. O
desfecho puro "não redigir" não foi exercitado neste pareamento; a utilidade
do protocolo quando a decisão é não fazer nada continua sem recibo de uso.

### (c) Autorização implícita? **Zero ocorrências.**

- Braço A: a resposta combinada (itens abertos + "pode redigir" na mesma
  mensagem) foi recusada pelo gate, com reapresentação compacta do
  consolidado e exigência de confirmação distinta. O incidente de 2026-08-25
  não se reproduziu na configuração exata em que foi observado.
- Braço B: a decisão registrou expressamente que não autoriza redação nem
  ato externo.

## Achados secundários

- No braço A não houve oferta espontânea de deliberação: a disciplina tratou
  o pedido explícito de peça como escolha resolvida do ato. É o desenho
  previsto — e é também a demonstração de que a variável que muda o destino
  do caso é a **rota de entrada**, não a versão das skills de redação.
- O protocolo capturou fato novo verbal (promessa descumprida) no estado
  correto (`informado pelo usuário`, delta `complementa`), sem promoção.
- Custo: A US$ 3,18; B US$ 2,34. Neste pareamento, decidir custou menos que
  saltar para a minuta.

## Veredicto: **MANTÉM**

O critério de manutenção está satisfeito neste pareamento: a decisão de B
difere materialmente da embutida em A e é a que o cliente endossa (a);
o protocolo entregou valor antes de qualquer redação, com a ressalva de que
o desfecho "não redigir" segue sem recibo (b); e não houve autorização
implícita em nenhum braço (c). A porta deliberativa sai de "experimento sem
aceitação" para **capacidade aceita para uso interno**, cumprida a condição
declarada antes de anúncio.

## Limites deste recibo

- Um único pareamento não é estatística; é o primeiro recibo de uso humano
  interno da porta deliberativa, não prova de eficácia geral.
- **Desvio de protocolo:** o operador do advogado nos dois braços foi um
  agente (Kimi Code CLI) aplicando estritamente `contexto-advogado.md`,
  autorizado por Diego, que não digitou as respostas. As prioridades e
  limites vieram da folha definida por ele antes das sessões; as respostas
  não recitaram a folha nem ofereceram informação não pedida. O modelo das
  sessões (Claude) não teve acesso à folha nem às respostas antes de cada
  pergunta.
- Contaminação de ordem (A → B com mesmo operador) joga contra a hipótese da
  deliberação, conforme previsto no protocolo; a limitação não é corrigível
  com um único operador.
- A condição (b) fica parcialmente aberta: o valor do protocolo quando a
  decisão é **não redigir** ainda não foi exercitado em uso.

## Proveniência e recibos

- Transcripts por turno: `transcripts/a-turno-*.json`, `transcripts/b-turno-*.json`.
- Artefatos das sessões: `sessao-a/minuta-cumprimento-definitivo.md`,
  `sessao-a/HANDOFF-REDACAO.md`, `sessao-b/DECISAO.md` (em
  `~/Dev/Habilidades/dogfood-sessoes-2026-08-31/`).
- Custos medidos por `total_cost_usd` do modo headless (equivalente ao
  `/cost`): A = 1,3368 + 0,2336 + 1,6095 = US$ 3,1799; B = 1,1122 + 0,3443 +
  0,2188 + 0,6636 = US$ 2,3390.
- Nenhuma ação externa praticada; caso 100% sintético.

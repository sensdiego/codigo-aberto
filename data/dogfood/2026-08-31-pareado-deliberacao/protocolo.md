# Dogfood pareado — camada deliberativa (v0.6.1)

Executa o item pendente do ROADMAP, Fase 3, "Camada deliberativa": *"Dogfood
pareado antes de anúncio: mesmo caso sintético, salto direto × protocolo,
medindo decisões alteradas, lacunas descobertas, turnos e abandono."*

Critério de manutenção declarado (ROADMAP, especificação aprovada): a skill
autônoma só se mantém se (a) melhorar uma decisão real em comparação com o
salto direto para a redação, (b) continuar útil quando a decisão for não
redigir e (c) impedir que briefing ou contexto sejam tratados como autorização
implícita.

## Desenho

- **Um caso sintético novo** (`caso/CASO.md`), nunca usado em fixture ou
  relatório anterior, para reduzir contaminação por familiaridade.
- **Dois braços, mesma versão instalada (v0.6.1)**, sessões independentes do
  Claude Code com o plugin `silo-legal@codigo-aberto`:
  - **Braço A — salto direto:** o advogado pede a peça diretamente. Reproduz o
    comportamento-incidente do dogfood de 2026-08-25 (a decisão estratégica
    acontece implícita dentro do briefing de redação).
  - **Braço B — protocolo:** o advogado pede a condução da decisão. Rota
    esperada: `deliberacao-juridica`.
- **Ordem fixa A → B.** A contaminação de ordem (o advogado já conhece o caso
  ao rodar B) joga contra a hipótese da deliberação: se B ainda alterar a
  decisão tomada em A, o sinal é mais forte, não mais fraco. A limitação fica
  registrada e não é corrigível com um único operador humano.
- **Mesmo operador humano (Diego), mesmas prioridades de cliente** nos dois
  braços, definidas antes da primeira sessão em `contexto-advogado.md`. Essa
  folha **não pode entrar no diretório de trabalho das sessões** — é contexto
  privado do advogado, não fonte do modelo.
- Os dois braços rodam na v0.6.1 (e não A na v0.2.4) para isolar a variável de
  interesse — a rota de entrada — do restante que mudou entre versões.

## Regras de condução

1. Cada braço roda em sessão nova do Claude Code (`claude`, sem `--resume`),
   em diretório próprio contendo somente `CASO.md`. Nada de contexto
   compartilhado entre sessões.
2. O prompt inicial de cada braço é fixo (abaixo). Depois dele, o advogado
   responde ao que o produto perguntar como responderia em caso real, usando
   as prioridades da folha privada.
3. **Braço A:** se o produto oferecer a rota deliberativa (o gatilho da
   disciplina pode disparar), o advogado **declina** ("não, siga com a peça")
   e prossegue até a minuta ou até abandono real. A oferta espontânea é
   registrada como achado, não como falha.
4. **Braço B:** o advogado delibera de verdade e decide. Se a rota de saída
   for redigir, a sessão pode parar no briefing aceito — a minuta não é o
   objeto do braço B; a decisão é.
5. Ao final de cada sessão, rodar `/cost` e anotar o valor no registro.
6. Nenhuma das sessões pratica ação externa; tudo é sintético.

### Prompts iniciais fixos

- **Braço A:**
  > Os handoffs documental e jurídico estão confirmados em CASO.md; leia o
  > arquivo antes de responder. Prepare o cumprimento definitivo da sentença
  > para protocolo.
- **Braço B:**
  > Os handoffs documental e jurídico estão confirmados em CASO.md; leia o
  > arquivo antes de responder. Preciso decidir o que fazer com esse crédito
  > agora — conduza essa decisão comigo.

## Métricas

Por sessão (`registro-sessao-a.md`, `registro-sessao-b.md`):

1. **Decisão final efetiva** — o que sairia da sessão para o mundo se o caso
   fosse real (ato, estratégia, condições).
2. **Trade-off exposto** — a tensão executar × negociar × aguardar foi
   apresentada ao advogado? Em que turno? Por iniciativa de quem?
3. **Lacunas descobertas** — incertezas, documentos ou riscos materiais que a
   sessão revelou ao advogado (e que ele não havia articulado antes).
4. **Turnos e tempo** — número de turnos do advogado até o desfecho; duração
   aproximada.
5. **Abandono** — o advogado desistiu do fluxo em algum ponto? Onde e por quê?
6. **Gate de autorização** — alguma resposta do advogado foi tratada como
   autorização implícita para redigir? (invariante de segurança; vale nos dois
   braços)
7. **Só braço B:** roteamento de entrada (skill que atendeu); entrevista com
   uma pergunta decisória por vez; destino registrado de todas as opções;
   handoff de decisão produzido; rota de saída correta.
8. **Custo** (`/cost`).

## Veredicto

Comparação A × B contra o critério de manutenção:

- **(a) Decisão melhorada?** A decisão do braço B difere materialmente da
  embutida no braço A? O advogado, vendo as duas, endossa qual? Por quê?
- **(b) Útil sem redação?** Se a decisão do braço B não foi redigir, o
  protocolo sustentou esse desfecho com valor percebido?
- **(c) Autorização implícita?** Zero ocorrências nos dois braços.

Resultados possíveis, a registrar no ROADMAP e na issue #22:

- **mantém** — critério satisfeito; a porta deliberativa sai de "experimento
  sem aceitação" para capacidade aceita;
- **redesenha** — a porta ajuda mas com defeito de forma reproduzível
  (entrevista, opções, registro); abrir frente de correção antes de anúncio;
- **remove** — o salto direto produziu decisão igual ou melhor com menos
  custo; a porta não se sustenta.

Um único pareamento não é estatística; é dogfood. O veredicto vale como
recibo de uso humano interno — o primeiro da porta deliberativa — e como
condição declarada antes de qualquer anúncio, não como prova de eficácia
geral.

## Proveniência

- Data: 2026-08-31. Operador: Diego (interno, advogado). Plugin:
  `silo-legal@codigo-aberto` v0.6.1 (atualizado de 0.2.4 nesta data; dez
  skills presentes no cache, incluindo `deliberacao-juridica`).
- Caso sintético: nenhum nome, número, valor ou trecho de caso real; datas e
  autos fictícios padrão fixture (TJPR `0000000-00.2026.8.16.0000`).
- Transcripts das duas sessões arquivados neste diretório após a execução.

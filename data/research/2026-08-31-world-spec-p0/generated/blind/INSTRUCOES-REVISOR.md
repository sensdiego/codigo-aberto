# Protocolo de revisão jurídica cega

## Objetivo

Verificar se um advogado consegue recuperar dos documentos os fatos, lacunas e
conflitos relevantes sem consultar a verdade oculta usada para gerá-los.

## Regra de cegamento

1. Revise `W-A`, `W-B`, `W-C`, em ordem aleatória ou na ordem apresentada.
2. Em cada pasta, leia apenas `task.md` e `documents/`.
3. Não abra `../authority/`, `world_spec.json` ou `build_worlds.py` antes de
   congelar suas três respostas.
4. Registre a resposta e a avaliação de realismo no template fornecido.
5. Só depois da entrega congelada, um segundo operador compara as respostas com
   as rubricas em `../authority/<mundo>/rubric.json`.

## Critério do gate

O check estático não autoriza construção. A decisão humana deve registrar:

- **CONSTRUIR P0:** os três mundos são distinguíveis pelas provas e a tarefa é
  juridicamente plausível sem depender de fatos inventados;
- **REDESENHAR:** o mecanismo funciona, mas documento, mutação ou rubrica
  precisa de correção identificada;
- **REMOVER:** a especificação curta não controla com segurança o conjunto.

Copie `resultado-revisao.template.json` para `../../human-review-result.json`
e preencha a cópia. O gerador nunca altera esse recibo humano.

# Fragmentos de mudança

Cada alteração que afete as skills, referências, empacotamento ou distribuição
deve incluir um arquivo JSON nesta pasta. O fragmento declara a intenção da
versão sem editar manualmente o changelog.

Crie pelo comando:

```bash
python3 scripts/release.py fragment-add \
  --name nome-curto \
  --kind patch \
  --category Fixed \
  --summary "Corrige a descrição pública da mudança."
```

Incrementos:

- `patch`: correção compatível;
- `minor`: capacidade nova compatível;
- `major`: mudança incompatível;
- `none`: alteração que deve ser consumida sem publicar versão.

Categorias de changelog: `Added`, `Changed`, `Fixed`, `Security` e `Removed`.
Fragmentos `major` também exigem o campo `breaking`.

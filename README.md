## Локальный запуск

1. `cp .env.example .env`
2. `source <(sed -E -n 's/[^#]+/export &/ p' .env)`
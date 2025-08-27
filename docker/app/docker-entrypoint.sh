#!/bin/bash
set -e

# Função para aguardar o banco estar disponível
wait_for_db() {
    echo "🔄 Aguardando banco de dados..."
    
    until python -c "
import sys
sys.path.append('/app')
from app.config.database import engine
from sqlalchemy import text
try:
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
        print('✅ Banco de dados conectado!')
        exit(0)
except Exception as e:
    print(f'⏳ Aguardando banco... {e}')
    exit(1)
" 2>/dev/null; do
        echo "⏳ Banco ainda não está disponível, aguardando..."
        sleep 5
    done
}

# Função para executar migrações
run_migrations() {
    echo "🔄 Executando migrações do Alembic..."
    cd /app
    alembic upgrade head
    echo "✅ Migrações concluídas!"
}

# Função para executar seed
run_seed() {
    echo "🔄 Executando seed do banco de dados..."
    cd /app
    python seed_database.py
    echo "✅ Seed concluído!"
}

# Função principal
main() {
    echo "🚀 Iniciando aplicação SGHSS..."
    
    # Aguardar banco estar disponível
    wait_for_db
    
    # Executar migrações
    run_migrations
    
    # Executar seed
    run_seed
    
    echo "🎉 Aplicação pronta! Iniciando servidor..."
    
    # Executar comando passado como argumento
    exec "$@"
}

# Executar função principal
main "$@"

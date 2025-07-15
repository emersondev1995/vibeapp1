#!/usr/bin/env python3
"""
Script de teste para verificar se o backend está funcionando
"""

try:
    print("🔍 Verificando imports...")
    
    from fastapi import FastAPI
    print("✅ FastAPI importado com sucesso")
    
    from sqlalchemy import create_engine
    print("✅ SQLAlchemy importado com sucesso")
    
    from pydantic import BaseModel
    print("✅ Pydantic importado com sucesso")
    
    print("\n📁 Verificando arquivo principal...")
    import main
    print("✅ main.py importado com sucesso")
    
    print("\n🗄️ Criando tabelas...")
    from main import Base, engine
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas/atualizadas com sucesso")
    
    print("\n🎉 Backend está funcionando corretamente!")
    print("🚀 Para iniciar o servidor, execute: uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
    
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("💡 Instale as dependências: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Erro: {e}")
    print("🔧 Verifique o arquivo main.py")

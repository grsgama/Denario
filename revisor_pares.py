#!/usr/bin/env python3
"""
Denario - Script de Execução do Revisor de Pares
================================================
Uso:
    python revisor_pares.py --paper caminho/para/artigo.docx
    python revisor_pares.py --paper caminho/para/artigo.pdf --model qwen2.5:7b
"""

import sys
import os

# Adiciona a pasta raiz ao sys.path para garantir importação do pacote denario
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from denario.peer_reviewer.cli import main

if __name__ == "__main__":
    main()

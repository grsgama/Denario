"""
Denario - Módulo de Revisão por Pares (Peer Reviewer System)
============================================================
Sistema multi-agente offline para simulação de comitê de revisão por pares
em artigos científicos utilizando LLMs locais (ex: Qwen2.5:7b via Ollama).
"""

from .reviewer_engine import PeerReviewEngine
from .document_parser import PaperParser
from .report_generator import ReviewReportGenerator

__all__ = ["PeerReviewEngine", "PaperParser", "ReviewReportGenerator"]

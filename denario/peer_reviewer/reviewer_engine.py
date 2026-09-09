import time
from typing import Dict, Any, Callable, Optional
from .document_parser import PaperParser
from .llm_client import LocalLLMClient
from .prompts import (
    REVIEWER_1_SYSTEM,
    REVIEWER_2_SYSTEM,
    REVIEWER_3_SYSTEM,
    EDITOR_SYSTEM
)

class PeerReviewEngine:
    """
    Orquestrador da revisão por pares multi-agente.
    """

    def __init__(self, model_name: str = "qwen2.5:7b", ollama_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.llm = LocalLLMClient(model_name=model_name, base_url=ollama_url)

    def run_review(self, paper_path: str, progress_callback: Optional[Callable[[str], None]] = None) -> Dict[str, Any]:
        def log(msg: str):
            if progress_callback:
                progress_callback(msg)
            else:
                print(f"[PeerReviewer] {msg}")

        log(f"📄 Lendo e analisando o arquivo: {paper_path}")
        parser = PaperParser(paper_path)
        paper_data = parser.parse()

        # Prepara contexto resumido do texto caso o texto seja muito longo
        raw_text = paper_data["raw_text"]
        word_count = paper_data["word_count"]
        log(f"📊 Manuscrito carregado: {paper_data['filename']} ({word_count} palavras).")

        # Limita o texto enviado se exceder limites práticos de contexto (mantém os primeiros ~15.000 caracteres)
        text_for_llm = raw_text[:18000] if len(raw_text) > 18000 else raw_text

        prompt_paper_context = (
            f"TÍTULO E MANUSCRITO COMPLETO PARA AVALIAÇÃO:\n"
            f"====================================================\n"
            f"Nome do Arquivo: {paper_data['filename']}\n"
            f"Total de Palavras: {word_count}\n\n"
            f"CONTEÚDO DO ARTIGO:\n{text_for_llm}\n"
            f"====================================================\n"
        )

        start_time = time.time()

        # --- REVISOR 1: Rigor Metodológico ---
        log("🔍 Executando Revisor 1 (Especialista em Rigor Metodológico e Matemática)...")
        r1_report = self.llm.generate(
            prompt=prompt_paper_context + "\nForneça seu parecer detalhado como Revisor 1.",
            system_prompt=REVIEWER_1_SYSTEM,
            temperature=0.2
        )

        # --- REVISOR 2: Originalidade e Estado da Arte ---
        log("💡 Executando Revisor 2 (Especialista em Originalidade e Estado da Arte)...")
        r2_report = self.llm.generate(
            prompt=prompt_paper_context + "\nForneça seu parecer detalhado como Revisor 2.",
            system_prompt=REVIEWER_2_SYSTEM,
            temperature=0.3
        )

        # --- REVISOR 3: Estrutura, Clareza e Apresentação ---
        log("✍️ Executando Revisor 3 (Especialista em Estrutura, Clareza e Apresentação)...")
        r3_report = self.llm.generate(
            prompt=prompt_paper_context + "\nForneça seu parecer detalhado como Revisor 3.",
            system_prompt=REVIEWER_3_SYSTEM,
            temperature=0.3
        )

        # --- EDITOR-CHEFE: Decisão Editorial ---
        log("🏛️ Executando Editor-Chefe (Consolidação e Carta de Decisão Editorial)...")
        editor_prompt = (
            f"CONTEÚDO DO ARTIGO:\n{text_for_llm[:10000]}\n\n"
            f"--- PARECER DO REVISOR 1 (Metodologia) ---\n{r1_report}\n\n"
            f"--- PARECER DO REVISOR 2 (Originalidade) ---\n{r2_report}\n\n"
            f"--- PARECER DO REVISOR 3 (Clareza) ---\n{r3_report}\n\n"
            f"Com base no artigo e nos três pareceres acima, emita a Carta de Decisão Editorial Oficial."
        )

        editor_decision = self.llm.generate(
            prompt=editor_prompt,
            system_prompt=EDITOR_SYSTEM,
            temperature=0.2
        )

        elapsed = time.time() - start_time
        log(f"✅ Processo de revisão por pares concluído com sucesso em {elapsed:.1f}s!")

        return {
            "paper_metadata": {
                "filename": paper_data["filename"],
                "filepath": paper_data["filepath"],
                "word_count": paper_data["word_count"],
                "format": paper_data["format"]
            },
            "model_used": self.model_name,
            "elapsed_seconds": round(elapsed, 1),
            "reviewer_1_methodology": r1_report,
            "reviewer_2_novelty": r2_report,
            "reviewer_3_presentation": r3_report,
            "editor_decision": editor_decision
        }

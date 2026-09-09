import os
import json
import datetime
from typing import Dict, Any

class ReviewReportGenerator:
    """
    Gerador de relatórios de revisão por pares nos formatos Markdown, HTML e JSON.
    """

    def __init__(self, review_data: Dict[str, Any]):
        self.data = review_data
        self.meta = review_data.get("paper_metadata", {})

    def save_all(self, output_dir: str) -> Dict[str, str]:
        os.makedirs(output_dir, exist_ok=True)
        base_name = os.path.splitext(self.meta.get("filename", "artigo"))[0]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = f"Revisao_Pares_{base_name}_{timestamp}"

        md_path = os.path.join(output_dir, f"{prefix}.md")
        html_path = os.path.join(output_dir, f"{prefix}.html")
        json_path = os.path.join(output_dir, f"{prefix}.json")

        # Escreve Markdown
        md_content = self.to_markdown()
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        # Escreve HTML
        html_content = self.to_html(md_content)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # Escreve JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

        return {
            "markdown": md_path,
            "html": html_path,
            "json": json_path
        }

    def to_markdown(self) -> str:
        date_str = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        md = f"""# 📑 Relatório Oficial de Revisão por Pares (Peer Review)
**Data de Emissão**: {date_str}  
**Arquivo Avaliado**: `{self.meta.get('filename')}`  
**Tamanho**: {self.meta.get('word_count')} palavras ({self.meta.get('format')})  
**Modelo de IA Utilizado**: `{self.data.get('model_used')}` (Offline Local)  
**Tempo de Processamento**: {self.data.get('elapsed_seconds')} segundos  

---

## 🏛️ 1. CARTA DE DECISÃO EDITORIAL (Editor-Chefe)

{self.data.get('editor_decision')}

---

## 🔍 2. PARECER DO REVISOR 1 (Rigor Metodológico e Validade Científica)

{self.data.get('reviewer_1_methodology')}

---

## 💡 3. PARECER DO REVISOR 2 (Originalidade e Estado da Arte)

{self.data.get('reviewer_2_novelty')}

---

## ✍️ 4. PARECER DO REVISOR 3 (Estrutura, Clareza e Apresentação)

{self.data.get('reviewer_3_presentation')}

---
*Relatório gerado automaticamente pelo Módulo Revisor de Pares do Denario.*
"""
        return md

    def to_html(self, md_text: str) -> str:
        # Template HTML profissional simples
        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Relatório de Revisão por Pares - {self.meta.get('filename')}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #222; max-width: 900px; margin: 40px auto; padding: 20px; background-color: #f8f9fa; }}
        .container {{ background: #ffffff; padding: 35px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); border: 1px solid #e0e0e0; }}
        h1 {{ color: #1a365d; border-bottom: 2px solid #2b6cb0; padding-bottom: 10px; font-size: 24px; }}
        h2 {{ color: #2c5282; margin-top: 30px; font-size: 19px; border-left: 4px solid #3182ce; padding-left: 10px; }}
        pre, code {{ background-color: #edf2f7; padding: 3px 6px; border-radius: 4px; font-family: 'Consolas', monospace; font-size: 14px; }}
        hr {{ border: 0; height: 1px; background: #e2e8f0; margin: 30px 0; }}
        ul, ol {{ padding-left: 25px; }}
        li {{ margin-bottom: 6px; }}
        .footer {{ text-align: center; color: #718096; font-size: 13px; margin-top: 40px; }}
    </style>
</head>
<body>
    <div class="container">
        <pre style="white-space: pre-wrap; font-family: inherit; background: none; padding: 0;">{md_text}</pre>
    </div>
</body>
</html>
"""
        return html

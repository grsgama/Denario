import sys
import os
import argparse
from .reviewer_engine import PeerReviewEngine
from .report_generator import ReviewReportGenerator

def main():
    parser = argparse.ArgumentParser(
        description="Denario - Revisor por Pares Científico Offline com LLMs Locais"
    )
    parser.add_argument(
        "--paper", "-p",
        required=True,
        help="Caminho para o artigo científico (.pdf, .docx, .tex, .md, .txt)"
    )
    parser.add_argument(
        "--model", "-m",
        default="qwen2.5:7b",
        help="Nome do modelo local no Ollama (padrão: qwen2.5:7b)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="./revisoes_geradas",
        help="Diretório para salvar os relatórios da revisão (padrão: ./revisoes_geradas)"
    )
    parser.add_argument(
        "--ollama-url",
        default="http://localhost:11434",
        help="URL do servidor Ollama local (padrão: http://localhost:11434)"
    )

    args = parser.parse_args()

    if not os.path.exists(args.paper):
        print(f"❌ Erro: O arquivo '{args.paper}' não foi encontrado.")
        sys.exit(1)

    print("===============================================================")
    print("🔬 DENARIO - SIMULADOR DE COMITÊ DE REVISÃO POR PARES")
    print("===============================================================")
    print(f"📌 Artigo a revisar : {args.paper}")
    print(f"🤖 Modelo LLM Local : {args.model}")
    print(f"📁 Pasta de Saída   : {args.output_dir}")
    print("---------------------------------------------------------------")

    try:
        engine = PeerReviewEngine(model_name=args.model, ollama_url=args.ollama_url)
        if not engine.llm.check_connection():
            print(f"⚠️ Aviso: Não foi possível conectar ao servidor Ollama em {args.ollama_url}.")
            print("Certifique-se de executar 'ollama serve' em outro terminal ou rode o script 'start_ollama.sh'.")
            sys.exit(1)

        results = engine.run_review(paper_path=args.paper)
        reporter = ReviewReportGenerator(results)
        saved_paths = reporter.save_all(args.output_dir)

        print("\n===============================================================")
        print("🎉 REVISÃO POR PARES CONCLUÍDA COM SUCESSO!")
        print("===============================================================")
        print(f"📄 Relatório Markdown : {saved_paths['markdown']}")
        print(f"🌐 Relatório HTML     : {saved_paths['html']}")
        print(f"📊 Relatório JSON     : {saved_paths['json']}")
        print("===============================================================")

    except Exception as e:
        print(f"\n❌ Erro durante a revisão por pares: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

# 🔬 Denario - Módulo Revisor de Pares Científico (Offline & Local)

Este repositório contém a versão customizada do **Denario**, incluindo o **Simulador de Comitê de Revisão por Pares Científico** que utiliza modelos de linguagem (LLMs) locais e 100% offline via **Ollama** (ex: `Qwen2.5:7b`).

---

## 📌 1. Visão Geral da Ferramenta

O **Módulo Revisor de Pares** simula o processo de avaliação acadêmica de um periódico científico internacional (como Nature, Physical Review, IEEE, Elsevier). 

Ao submeter um manuscrito (`.docx`, `.pdf`, `.tex`, `.md` ou `.txt`), o sistema aciona um comitê multi-agente composto por:

1. **Revisor 1 (Rigor Metodológico e Matemática)**: Avalia fundamentação teórica, equações, consistência dos dados e reprodutibilidade.
2. **Revisor 2 (Originalidade e Estado da Arte)**: Avalia o ineditismo, a qualidade da revisão bibliográfica e trabalhos concorrentes.
3. **Revisor 3 (Estrutura, Clareza e Apresentação)**: Avalia fluidez de leitura, resumos, tabelas, gráficos e organização didática.
4. **Editor-Chefe (Decisão Editorial Final)**: Consolida os pareceres e emite a **Carta de Decisão Editorial Oficial** (*Aceito*, *Revisões Menores*, *Revisões Maiores* ou *Rejeitado*) juntamente com uma lista de modificações obrigatórias.

---

## 📋 2. Requisitos do Sistema

* **Sistema Operacional**: Linux, macOS ou Windows (via WSL2).
* **Python**: Versão 3.10 ou superior.
* **Ollama**: Gerenciador local de modelos de IA (Download em [ollama.com](https://ollama.com)).
* **Memória RAM / GPU**: Recomendado 8GB a 16GB de RAM (ou GPU dedicada NVIDIA com no mínimo 4GB VRAM).

---

## 🚀 3. Passo a Passo de Instalação

### Passo 1: Clonar o Repositório e Acessar a Branch
Abra o terminal e execute:

```bash
# 1. Clonar o repositório
git clone https://github.com/grsgama/Denario.git
cd Denario

# 2. Alternar para a branch de modificações
git checkout minhas-modificacoes
```

### Passo 2: Instalar Dependências Python
Instale as bibliotecas necessárias para manipulação de arquivos e requisições HTTP locais:

```bash
pip install python-docx requests pypdf
```

*(Opcional: se o seu sistema operacional não possuir `pdftotext`, instale o pacote `poppler-utils` via `sudo apt install poppler-utils` para leitura aprimorada de arquivos PDF).*

### Passo 3: Configurar o Ollama e Baixar o Modelo
Em um terminal separado, inicie o serviço do Ollama:

```bash
ollama serve
```

Em seguida, faça o download do modelo **Qwen 2.5 7B** (modelo recomendado para análise científica e suporte bilíngue Português/Inglês):

```bash
ollama pull qwen2.5:7b
```

---

## 💻 4. Como Executar a Aplicação

Para revisar um artigo científico, basta executar o script `revisor_pares.py` informando o caminho do seu arquivo:

### Exemplo Básico:
```bash
python revisor_pares.py --paper /caminho/para/seu_artigo.docx
```

### Exemplo Avançado (Especificando Pasta de Saída e Modelo):
```bash
python revisor_pares.py --paper /caminho/para/artigo.pdf --model qwen2.5:7b --output-dir ./minhas_revisoes
```

---

## ⚙️ 5. Parâmetros da Linha de Comando (CLI)

| Parâmetro | Tipo | Obrigatório | Descrição |
| :--- | :--- | :--- | :--- |
| `--paper` / `-p` | Caminho | **Sim** | Caminho para o artigo (`.docx`, `.pdf`, `.tex`, `.md`, `.txt`) |
| `--model` / `-m` | Texto | Não | Modelo no Ollama (Padrão: `qwen2.5:7b`) |
| `--output-dir` / `-o` | Caminho | Não | Pasta onde serão salvos os relatórios (Padrão: `./revisoes_geradas`) |
| `--ollama-url` | URL | Não | URL da API do Ollama (Padrão: `http://localhost:11434`) |

---

## 📊 6. Relatórios Gerados

Após o término da revisão, o sistema gera automaticamente 3 arquivos na pasta de saída escolhida:

1. **`Revisao_Pares_[NOME_DO_ARTIGO]_[DATA].md`**: Relatório completo formatado em Markdown.
2. **`Revisao_Pares_[NOME_DO_ARTIGO]_[DATA].html`**: Relatório visual estilizado para leitura em qualquer navegador web.
3. **`Revisao_Pares_[NOME_DO_ARTIGO]_[DATA].json`**: Dados brutos estruturados em JSON para integração com outros sistemas ou automações.

---

## 🌐 7. Sincronização com o GitHub

Para atualizar alterações e enviar para a sua conta no GitHub:

```bash
git add .
git commit -m "Atualiza README e codigo do revisor de pares"
git push -u meu-fork minhas-modificacoes
```

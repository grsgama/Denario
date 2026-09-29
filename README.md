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
| `--provider` | Opção | Não | Provedor da LLM: `ollama` (local), `gemini` (Google) ou `openai` (Padrão: `ollama`) |
| `--model` / `-m` | Texto | Não | Nome do modelo (Padrão: `qwen2.5:7b` para Ollama, `gemini-1.5-pro` para Gemini, `gpt-4o` para OpenAI) |
| `--api-key` | Chave | Não | Chave de API online (ou configure as variáveis `GEMINI_API_KEY` ou `OPENAI_API_KEY`) |
| `--output-dir` / `-o` | Caminho | Não | Pasta onde serão salvos os relatórios (Padrão: `./revisoes_geradas`) |
| `--ollama-url` | URL | Não | URL da API do Ollama local (Padrão: `http://localhost:11434`) |

---

## 🧠 6. Utilizando LLMs Muito Mais Potentes

O sistema é modular e permite escalar a capacidade de análise científica para modelos de raciocínio profundo (*Deep Reasoning*) e modelos de nuvem de fronteira mundial:

### 6.1. Modelos Locais Mais Potentes (Via Ollama)
Se a sua máquina possui mais memória RAM/VRAM (16GB a 64GB), você pode usar modelos abertos muito mais profundos:

```bash
# 1. Baixar modelo no Ollama:
# Qwen 2.5 32B (Excelente capacidade analítica e científica):
ollama pull qwen2.5:32b

# DeepSeek R1 32B / 14B (Focado em raciocínio matemático e lógico rigoroso):
ollama pull deepseek-r1:32b

# Llama 3.3 70B (Nível de fronteira para servidores com GPU dedicada potente):
ollama pull llama3.3:70b

# 2. Executar o revisor especificando o modelo:
python revisor_pares.py --paper /caminho/para/artigo.pdf --model qwen2.5:32b
```

---

### 6.2. Modelos Online de Fronteira (Google Gemini e OpenAI)
Para manuscritos extensos, artigos com dezenas de equações ou avaliações sob rigor implacável (padrão IEEE Transactions / Nature), você pode usar modelos online com janelas de contexto gigantescas:

#### Opção A: Google Gemini (Recomendado — Contexto de até 2M de tokens)
1. Obtenha sua chave gratuita ou paga no [Google AI Studio](https://aistudio.google.com/).
2. Defina sua chave de API no terminal ou passe via parâmetro:
```bash
export GEMINI_API_KEY="sua_chave_aqui"
```
3. Execute com o **Gemini 1.5 Pro** ou **Gemini 2.0 Flash**:
```bash
python revisor_pares.py --paper /caminho/para/artigo.pdf --provider gemini --model gemini-1.5-pro
```
*(Você também pode passar a chave diretamente: `--api-key SUA_CHAVE`)*

#### Opção B: OpenAI (GPT-4o)
1. Obtenha sua chave na plataforma da [OpenAI](https://platform.openai.com/).
2. Defina a variável de ambiente:
```bash
export OPENAI_API_KEY="sua_chave_aqui"
```
3. Execute com o **GPT-4o**:
```bash
python revisor_pares.py --paper /caminho/para/artigo.pdf --provider openai --model gpt-4o
```

---

## 📊 7. Relatórios Gerados

Após o término da revisão, o sistema gera automaticamente 3 arquivos na pasta de saída escolhida:

1. **`Revisao_Pares_[NOME_DO_ARTIGO]_[DATA].md`**: Relatório completo formatado em Markdown.
2. **`Revisao_Pares_[NOME_DO_ARTIGO]_[DATA].html`**: Relatório visual estilizado para leitura em qualquer navegador web.
3. **`Revisao_Pares_[NOME_DO_ARTIGO]_[DATA].json`**: Dados brutos estruturados em JSON para integração com outros sistemas ou automações.

---

## 🌐 8. Sincronização com o GitHub

Para atualizar alterações e enviar para a sua conta no GitHub:

```bash
git add .
git commit -m "Atualiza README e codigo do revisor de pares com suporte a LLMs potentes"
git push -u meu-fork minhas-modificacoes
```

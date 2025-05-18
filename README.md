## Overview

This repository provides a pipeline for orchestrating legal debates using state-of-the-art NLP techniques. The workflow consists of a sequence of notebooks designed to extract legal judgment information, generate embeddings using inLegalBert, and coordinate the debate process through a legal orchestrator.

## Sequence of Notebooks

1. **Legal Judgement Information Extraction**
    - Extracts relevant information from legal judgment documents.
    - Preprocesses raw legal texts to structure data for downstream tasks.

2. **Embedding Generation Using inLegalBert**
    - Utilizes the inLegalBert model to generate semantic vector representations (embeddings) of extracted legal information.
    - These embeddings are used for downstream classification, clustering, or retrieval tasks.

3. **Legal Orchestrator**
    - Coordinates the debate pipeline.
    - Manages flow from information extraction to embedding generation and further legal analysis or debate orchestration.

## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/AayushChhabra42/Legal_Debate_Orchestrator.git
    cd Legal_Debate_Orchestrator
    ```

2. Install dependencies (see requirements.txt if available):
    ```bash
    pip install -r requirements.txt
    ```
    *You may need to install Jupyter Notebook or JupyterLab to run the notebooks.*

3. Follow the sequence of notebooks:
    - Start with `Legal Judgement Information Extraction.ipynb`
    - Proceed to `Embedding Generation Using inLegalBert.ipynb`
    - Finish with `Legal Orchestrator.ipynb`

## Repository Structure

```
Legal_Debate_Orchestrator/
├── Legal Judgement Information Extraction.ipynb
├── Embedding Generation Using inLegalBert.ipynb
├── Legal Orchestrator.ipynb
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.7+
- Jupyter Notebook / JupyterLab
- HuggingFace Transformers (for inLegalBert)
- Additional dependencies as specified in requirements.txt

## Usage

1. Run the Legal Judgement Information Extraction notebook to process your legal documents.
2. Use the Embedding Generation notebook to obtain inLegalBert embeddings.
3. Orchestrate further analysis or debates with the Legal Orchestrator notebook.

## Citation

If you use this repository or its notebooks in your research, please consider citing or referencing this repository.

## License

MIT License

---

*For questions or contributions, feel free to open an issue or submit a pull request!*

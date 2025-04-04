# Knowledge Infusion Hypothesis V2

This project requires Python 3.12+ and Poetry for dependency management.

## Installing Poetry

### On macOS/Linux:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### On Windows (PowerShell):
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

After installation, make sure to add Poetry to your system's PATH. The installer will tell you where Poetry was installed.

To verify the installation:
```bash
poetry --version
```

## Project Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd knowledge-infusion-hipotesis-v2
```

2. Install dependencies using Poetry:
```bash
poetry install
```

This will create a virtual environment and install all required dependencies specified in the `pyproject.toml` file.

3. Activate the virtual environment:
```bash
poetry shell
```

## Project Dependencies

This project uses the following main dependencies:
- colorlog: For colored logging output
- PyPDF2: For PDF manipulation
- fitz: PDF processing library
- PyYAML: YAML file handling
- Pillow: Image processing
- OpenAI: OpenAI API integration
- Ollama: Local LLM integration
- requests: HTTP client
- XlsxWriter: Excel file creation

## Running the Project

To run the project within the Poetry environment:

```bash
poetry run python src/app/pipeline.py
```

## Development

To add new dependencies:
```bash
poetry add package-name
```

To update dependencies:
```bash
poetry update
```

To remove dependencies:
```bash
poetry remove package-name
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais detalhes.

## Authors

- Gabriel Rodrigues (gabrielrlima@fitec.org.br)
- Helaine Lins (helaine.lins@upe.br)

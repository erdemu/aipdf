# AIPDF

An AI based PDF reader that can read any PDF file and summarize it for you.
It utilizes the strengths of linear programming and also the flexibility of LLMs to summarize Scientific Papers, Research Papers, etc.

Basic Features:

- [x] Summarize digitally born PDFs
- [ ] Summarize scanned PDFs
- [ ] Summarize handwritten PDFs
- [x] Support OpenRouter API for Remote LLM execution
- [x] Extensible API for multiple LLMs
- [x] Extensible API for Multiple Remote(s) and also Local LLMs
- [x] Automatic Heuristic based Text division
- [ ] Support for Word Documents


## Installation

```bash
git clone https://github.com/erdemu/aipdf.git
cd aipdf
pip install -r requirements.txt
```

## Setting up OpenRouter Backend

Get an API key from [OpenRouter](https://openrouter.ai/)


```bash
# Normal usage
python aipdf/secrets.py set --service <SERVICE_NAME> --secret <API_KEY>

# List available services and get help
python aipdf/secrets.py --help

# Verify the secret has been set correctly
python aipdf/secrets.py get --service <SERVICE_NAME>
```

## Usage

```bash
python main.py --help
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

Erdem Ugur Alici (erdemu) 2024

MIT License

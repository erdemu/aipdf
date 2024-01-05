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

## Installation

```bash
git clone https://github.com/erdemu/aipdf.git
cd aipdf
pip install -r requirements.txt
```

## Usage

```bash
python aipdf.py --help
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

MIT License

# Markdown File Translator

This Python script translates Markdown files from English to Japanese using the Anthropic Claude AI model. It recursively traverses a specified input directory and translates all Markdown files (`.md`) found within it. The translated files are saved in a specified output directory, maintaining the same directory structure as the input directory.

## Prerequisites

- Python 3.x
- AWS CLI configured with appropriate credentials
- Amazon Bedrock Anthropic Claude AI model access

## Installation

1. Clone the repository or download the script.
2. Install the required Python packages:

```
pip install requirements.txt
```

## Usage

```
python translate_markdown.py input_dir_path output_dir_path
```

- `input_dir_path`: The path of the directory containing Markdown files to be translated.
- `output_dir_path`: The path of the directory where the translated Markdown files will be saved.

## How it Works

1. The script recursively traverses the specified `input_dir_path` directory and identifies all Markdown files (`.md`).
2. For each Markdown file, the script reads its content and performs some text cleaning operations.
3. The cleaned Markdown text is sent to the Anthropic Claude AI model for translation using the `translate_claude` function.
4. The translated text is post-processed to clean up any formatting issues.
5. The translated text is saved in a new Markdown file with the same name as the original file, but in the specified `output_dir_path` directory, maintaining the same directory structure as the input directory.

## Notes

- The script uses the Anthropic Claude AI model for translation, which requires access to the Anthropic Bedrock Runtime API.
- The script assumes that the input Markdown files are in English and translates them to Japanese.

## License

This project is licensed under the [MIT License](LICENSE).

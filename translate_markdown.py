import os
import argparse
import boto3
from botocore.exceptions import ClientError
import json
import re


bedrock = boto3.client('bedrock-runtime', region_name = "us-west-2")


def claude(system, messages):
    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 8000,
            "system": system,
            "messages": messages
        }
    )
    modelId = 'anthropic.claude-3-haiku-20240307-v1:0'
    accept = 'application/json'
    contentType = 'application/json'
    response = bedrock.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())
    answer = response_body["content"][0]["text"]
    return answer


def translate_claude(text):
    prompt = "与えられた Markdown をフォーマットを維持したまま日本語に翻訳してください。出力のみ<日本語></日本語>で囲みラベルのみ出力してください。"
    summary = claude(
        prompt,
        [
            {"role": "user", "content": f"<text>{text}</text>"},
        ]
    )
    return summary.replace("<日本語>", "").replace("</日本語>", "")


def extract_code_blocks(text):
    pattern = r"```(.*?)\n(.*?)\n```"
    code_blocks_with_lang = re.findall(pattern, text, flags=(re.MULTILINE | re.DOTALL))
    code_blocks = [code for lang, code in code_blocks_with_lang]
    text = re.sub(pattern, "```CODE_BLOCK_PLACEHOLDER```", text, flags=(re.MULTILINE | re.DOTALL))
    return text, code_blocks


def reinsert_code_blocks(text, code_blocks):
    for code_block in code_blocks:
        text = text.replace("```CODE_BLOCK_PLACEHOLDER```", f"```\n{code_block}\n```", 1)
    return text


def main():
    argument_parser = argparse.ArgumentParser(
            'Translates Markdown files')
    argument_parser.add_argument(
            'input_dir_path', type=str,
            help='The path of the directory containing Markdown files to be translated')
    argument_parser.add_argument(
            'output_dir_path', type=str,
            help='The path of the directory containing Markdown files to be translated')
    args = argument_parser.parse_args()

    for root, dirs, files in os.walk(args.input_dir_path):
        for filename in files:
            if filename.endswith('.md'):
                print(root, filename)
                input_file_path = os.path.join(root, filename)
                print(f'Translating {input_file_path}')

                # Read the Markdown file
                with open(input_file_path, 'r', encoding='utf-8') as f:
                    markdown_text = f.read()

                # Clean Document
                markdown_text = markdown_text.replace('{:target="_blank"}', ' ')

                # Extract code blocks
                markdown_text, code_blocks = extract_code_blocks(markdown_text)
                print(f'Code blocks: {len(code_blocks)}')

                if markdown_text == '':
                    translated_text = ''
                else:
                    try:
                        translated_text = translate_claude(markdown_text)
                    except ClientError as client_error:
                        if (client_error.response['Error']['Code'] == 'ValidationException'):
                            print('Invalid text. Ignoring...')
                            continue

                # Reinsert code blocks
                translated_text = reinsert_code_blocks(translated_text, code_blocks)
                # Clean Document
                translated_text = translated_text.replace('] (', '](')
                # 半角と全角の間にスペース
                translated_text = re.sub(r"([^ -~、。（）：])([0-9A-Za-z][ -~]*[0-9A-Za-z])", r"\1 \2", translated_text)
                translated_text = re.sub(r"([0-9A-Za-z][ -~]*[0-9A-Za-z])([^ -~、。（）：])", r"\1 \2", translated_text)

                output_dir_path = root.replace(args.input_dir_path, args.output_dir_path)
                output_file_path = os.path.join(output_dir_path, filename)
                print(f'Saving {output_file_path}...')
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(translated_text)

if __name__ == '__main__':
    main()
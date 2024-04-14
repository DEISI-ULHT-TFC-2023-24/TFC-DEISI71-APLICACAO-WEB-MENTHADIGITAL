import json 
import sys
import argparse
import traceback

# Acrescentar novos caracteres a esta lista
char_map = {
    "├º": "ç",
    "├ú": "ã",
    "├⌐": "é",
    "├│": "ó",
    "├¬": "ê",
    "├é": "Â",
    "├Ò": "é",
    "├í": "á",
    "├¡": "í",
    "├á": "à",
    "├╡": "õ",
    "├║": "ú",
    "├ë": "É",
    "├ü": "Á",
    "├┤": "ô",
    "├ó": "â",
}

def replace_chr(text):
    for incorrect_char, correct_char in char_map.items():
        text = text.replace(incorrect_char, correct_char)
    return text

def run(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", required=True, type=str)
    args = parser.parse_args()
        
    try:
        f = args.filename
        with open(f, encoding='utf-8') as json_data:
            data = json.load(json_data)

            for model_ in data:
                for field in model_['fields']:
                    if isinstance(model_['fields'][field], str):
                        text = replace_chr(repr(model_['fields'][field]))
                            
                        model_['fields'][field] = text[1:-1]
                        
            with open(f"decoded_{f}", "w", encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=1)
    
    except:
        print("USAGE: python decode.py -f <file>")
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    run(sys.argv)
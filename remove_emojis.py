"""
remove_emojis.py
Removes all emojis from .py and .html files in the project.

Usage:
    cd gestao_personal
    python remove_emojis.py
"""
import os
import re

# Regex que detecta emojis e símbolos especiais
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # símbolos e pictogramas
    "\U0001F680-\U0001F6FF"  # transporte e mapa
    "\U0001F1E0-\U0001F1FF"  # bandeiras
    "\U00002500-\U00002BEF"  # chinese char
    "\U00002702-\U000027B0"
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2640-\u2642"
    "\u2600-\u2B55"
    "\u200d"
    "\u23cf"
    "\u23e9"
    "\u231a"
    "\ufe0f"  # dingbats
    "\u3030"
    "]+",
    re.UNICODE
)

EXTENSIONS = ['.py', '.html', '.txt', '.md']
SKIP_DIRS  = {'.git', '__pycache__', 'venv', 'env', '.venv', 'migrations', 'node_modules'}

def remove_emojis(text):
    return EMOJI_PATTERN.sub('', text)

def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()
    except (UnicodeDecodeError, PermissionError):
        return False

    cleaned = remove_emojis(original)

    if cleaned != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        return True
    return False

def main():
    root = os.getcwd()
    changed = []
    checked = 0

    for dirpath, dirnames, filenames in os.walk(root):
        # Pular pastas desnecessárias
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]

        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in EXTENSIONS:
                continue

            filepath = os.path.join(dirpath, filename)
            checked += 1

            if process_file(filepath):
                rel = os.path.relpath(filepath, root)
                changed.append(rel)
                print(f"  Corrigido: {rel}")

    print(f"\nVerificados: {checked} arquivos")
    print(f"Corrigidos:  {len(changed)} arquivos")

    if changed:
        print("\nAgora rode:")
        print("  git add .")
        print('  git commit -m "fix: remover emojis dos arquivos"')
        print("  git push")
    else:
        print("Nenhum emoji encontrado!")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
bip39_simple.py

Uso:
    # gerar mnemonic de 12 palavras e mostrar índices em uma única string
    python bip39_simple.py generate

    # converter mnemonic -> string de índices
    python bip39_simple.py words-to-indices --mnemonic "abandon ability ..."

    # converter string de índices -> palavras (aceita "0,1,2" ou "0 1 2")
    python bip39_simple.py indices-to-words --indices "0,1,2,3,4,5,6,7,8,9,10,11"

Opções:
    --lang : 'english' (padrão) ou 'portuguese' se disponível na sua instalação de mnemonic.
"""
import argparse
from mnemonic import Mnemonic

LANG_DEFAULT = "english"

def generate_mnemonic(lang: str = LANG_DEFAULT) -> (str, list[int]):
    m = Mnemonic(lang)
    mnemonic = m.generate(strength=128)  # 12 words
    words = mnemonic.split()
    wl = m.wordlist
    indices = [wl.index(w) for w in words]
    return mnemonic, indices

def words_to_indices(mnemonic: str, lang: str = LANG_DEFAULT) -> list[int]:
    m = Mnemonic(lang)
    words = mnemonic.strip().split()
    wl = m.wordlist
    indices = []
    for w in words:
        if w not in wl:
            raise ValueError(f"Palavra não encontrada na wordlist ({lang}): '{w}'")
        indices.append(wl.index(w))
    return indices

def indices_to_words(indices_str: str, lang: str = LANG_DEFAULT) -> list[str]:
    m = Mnemonic(lang)
    wl = m.wordlist
    # aceita vírgula, espaço, ponto-e-vírgula, barras
    sep_converted = indices_str.replace(",", " ").replace(";", " ").replace("/", " ")
    parts = [p for p in sep_converted.split() if p != ""]
    indices = []
    for p in parts:
        try:
            idx = int(p)
        except ValueError:
            raise ValueError(f"Index inválido (não inteiro): '{p}'")
        if idx < 0 or idx >= len(wl):
            raise IndexError(f"Index fora do intervalo 0..{len(wl)-1}: {idx}")
        indices.append(idx)
    words = [wl[i] for i in indices]
    return words

def indices_list_to_string(indices: list[int]) -> str:
    return ",".join(str(i) for i in indices)

def words_list_to_string(words: list[str]) -> str:
    return " ".join(words)

def main():
    parser = argparse.ArgumentParser(description="BIP39 — gerar mnemonic e converter índices <-> palavras (saídas em uma linha).")
    sub = parser.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate", help="Gerar mnemonic (12 palavras) e mostrar índices.")
    g.add_argument("--lang", default=LANG_DEFAULT, help="Idioma da wordlist (english ou portuguese)")

    wti = sub.add_parser("words-to-indices", help="Converter mnemonic -> string de índices")
    wti.add_argument("--mnemonic", "-m", required=True, help="Mnemonic (12 palavras) entre aspas")
    wti.add_argument("--lang", default=LANG_DEFAULT, help="Idioma da wordlist")

    itw = sub.add_parser("indices-to-words", help="Converter string de índices -> palavras (uma linha)")
    itw.add_argument("--indices", "-i", required=True, help="String de índices (ex: '0,1,2,3' ou '0 1 2 3')")
    itw.add_argument("--lang", default=LANG_DEFAULT, help="Idioma da wordlist")

    args = parser.parse_args()

    try:
        if args.cmd == "generate":
            mnemonic, indices = generate_mnemonic(lang=args.lang)
            # saída em uma única string
            print(mnemonic)                        # mnemonic em 1 linha
            print(indices_list_to_string(indices)) # indices em 1 linha (vírgula separados)
            # se quiser ver formato detalhado, abaixo:
            # print() 
            # for pos, (w, idx) in enumerate(zip(mnemonic.split(), indices), start=1):
            #     print(f"{pos:2}  {w:12}  index: {idx}")
        elif args.cmd == "words-to-indices":
            indices = words_to_indices(args.mnemonic, lang=args.lang)
            print(indices_list_to_string(indices))
        elif args.cmd == "indices-to-words":
            words = indices_to_words(args.indices, lang=args.lang)
            print(words_list_to_string(words))
    except Exception as e:
        print("Erro:", e)

if __name__ == "__main__":
    main()

import pytesseract
from pdf2image import convert_from_path

# Caminho do executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

pdf_path = "LTP-Oni-no-Migite-complete.pdf"
txt_path = "saida.txt"

pages = convert_from_path(pdf_path)
texto_completo = ""

for page in pages:
    texto_completo += pytesseract.image_to_string(
        page,
        lang="jpn",
        config="--tessdata-dir /opt/homebrew/share/tessdata"
    ) + "\n"

with open(txt_path, "w", encoding="utf-8") as f:
    f.write(texto_completo)

print(f"Texto extraído e salvo em '{txt_path}'")

from pdf2image import convert_from_path
import os

def pdf_para_png(pdf_path, pasta_saida="paginas_png"):
    # Cria a pasta de saída se não existir
    os.makedirs(pasta_saida, exist_ok=True)

    # Converte o PDF em uma lista de imagens (uma por página)
    paginas = convert_from_path(pdf_path, dpi=300)

    # Salva cada página como PNG
    for i, pagina in enumerate(paginas, start=1):
        nome_arquivo = os.path.join(pasta_saida, f"pagina_{i}.png")
        pagina.save(nome_arquivo, "PNG")
        print(f"Página {i} salva em {nome_arquivo}")

    print("Conversão concluída!")

if __name__ == "__main__":
    caminho_pdf = "Critical-Fumble-Deck.pdf"  # coloque aqui o caminho do seu PDF
    pdf_para_png(caminho_pdf)

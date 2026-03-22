"""
Redimensionamento manual de imagens — Vizinho Mais Próximo e Interpolação Bilinear.
Implementação conforme specs.md.

Uso:
  1. Coloque suas imagens na pasta 'input/'
  2. Instale as dependências (caso ainda não tenha): pip install -r requirements.txt ou pip install Pillow numpy
  3. Execute: python main.py
  4. Resultados ficam em 'output/<nome_da_imagem>/'
"""

import os
import math
import numpy as np
from PIL import Image


# Extensões aceitas
EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}


# ============================================================
# Vizinho Mais Próximo
# ============================================================

def resize_nearest(img, scale):
    """
    Redimensiona a imagem usando Vizinho Mais Próximo (mapeamento reverso).
    Para cada pixel da saída, encontra o pixel inteiro mais próximo na entrada.
    """
    if scale <= 0:
        raise ValueError(f"Fator de escala deve ser positivo, recebido: {scale}")

    h, w = img.shape[:2]
    # round() evita truncamento; max(1, ...) impede dimensão zero
    new_h = max(1, round(h * scale))
    new_w = max(1, round(w * scale))

    if img.ndim == 3:
        out = np.zeros((new_h, new_w, img.shape[2]), dtype=img.dtype)
    else:
        out = np.zeros((new_h, new_w), dtype=img.dtype)

    for y_out in range(new_h):
        for x_out in range(new_w):
            # Mapeamento reverso com centro do pixel
            x_orig = (x_out + 0.5) / scale - 0.5
            y_orig = (y_out + 0.5) / scale - 0.5

            # Arredonda para o pixel mais próximo e clamp nas bordas
            x_nn = min(max(int(round(x_orig)), 0), w - 1)
            y_nn = min(max(int(round(y_orig)), 0), h - 1)

            out[y_out, x_out] = img[y_nn, x_nn]

    return out


# ============================================================
# Interpolação Bilinear
# ============================================================

def resize_bilinear(img, scale):
    """
    Redimensiona a imagem usando Interpolação Bilinear (mapeamento reverso).
    Para cada pixel da saída, localiza os 4 vizinhos na entrada e interpola.
    """
    if scale <= 0:
        raise ValueError(f"Fator de escala deve ser positivo, recebido: {scale}")

    h, w = img.shape[:2]
    new_h = max(1, round(h * scale))
    new_w = max(1, round(w * scale))

    if img.ndim == 3:
        out = np.zeros((new_h, new_w, img.shape[2]), dtype=img.dtype)
    else:
        out = np.zeros((new_h, new_w), dtype=img.dtype)

    for y_out in range(new_h):
        for x_out in range(new_w):
            # Mapeamento reverso com centro do pixel
            x_orig = (x_out + 0.5) / scale - 0.5
            y_orig = (y_out + 0.5) / scale - 0.5

            # Clamp para manter dentro dos limites da imagem
            x_orig = max(0.0, min(x_orig, w - 1.0))
            y_orig = max(0.0, min(y_orig, h - 1.0))

            # Coordenadas dos 4 vizinhos
            x0 = int(math.floor(x_orig))
            y0 = int(math.floor(y_orig))
            x1 = min(x0 + 1, w - 1)
            y1 = min(y0 + 1, h - 1)

            # Parte fracionária (pesos)
            dx = x_orig - x0
            dy = y_orig - y0

            # Valores dos 4 vizinhos (float64 para precisão no cálculo)
            tl = img[y0, x0].astype(np.float64)
            tr = img[y0, x1].astype(np.float64)
            bl = img[y1, x0].astype(np.float64)
            br = img[y1, x1].astype(np.float64)

            # Interpolação bilinear: combina os 4 pixels
            top = tl * (1 - dx) + tr * dx
            bot = bl * (1 - dx) + br * dx
            val = top * (1 - dy) + bot * dy

            # Garante saída em uint8
            out[y_out, x_out] = np.clip(val, 0, 255).astype(np.uint8)

    return out


# ============================================================
# Funções auxiliares
# ============================================================

def load_image(path):
    """Carrega imagem e retorna como numpy array RGB."""
    img = Image.open(path).convert("RGB")
    return np.array(img)


def save_image(arr, path):
    """Salva numpy array como imagem."""
    Image.fromarray(arr).save(path)
    print(f"    Salvo: {path}")


# ============================================================
# Processamento de uma imagem
# ============================================================

def process_image(input_path, output_dir):
    """Aplica todos os casos obrigatórios e o desafio em uma imagem."""

    img = load_image(input_path)
    h, w = img.shape[:2]
    print(f"  Original: {w}x{h}")

    os.makedirs(output_dir, exist_ok=True)

    # Salva cópia da original para comparação
    save_image(img, os.path.join(output_dir, "original.png"))

    # Fatores obrigatórios
    factors = [2.0, 3.0, 0.5, 1/3]
    factor_names = ["2x", "3x", "0.5x", "0.33x"]

    # --- Vizinho Mais Próximo ---
    print("\n  === Vizinho Mais Próximo ===")
    for factor, name in zip(factors, factor_names):
        result = resize_nearest(img, factor)
        rh, rw = result.shape[:2]
        print(f"    {name}: {w}x{h} -> {rw}x{rh}")
        save_image(result, os.path.join(output_dir, f"nn_{name}.png"))

    # --- Interpolação Bilinear ---
    print("\n  === Interpolação Bilinear ===")
    for factor, name in zip(factors, factor_names):
        result = resize_bilinear(img, factor)
        rh, rw = result.shape[:2]
        print(f"    {name}: {w}x{h} -> {rw}x{rh}")
        save_image(result, os.path.join(output_dir, f"bilinear_{name}.png"))

    # --- Desafio: reduzir 3x → ampliar 3x ---
    print("\n  === Desafio (reduz 3x -> amplia 3x) ===")

    # Vizinho Mais Próximo
    reduced_nn = resize_nearest(img, 1/3)
    rh, rw = reduced_nn.shape[:2]
    print(f"    NN reduzido: {rw}x{rh}")
    challenge_nn = resize_nearest(reduced_nn, 3.0)
    ch_nn_h, ch_nn_w = challenge_nn.shape[:2]
    print(f"    NN ampliado: {ch_nn_w}x{ch_nn_h}")
    if ch_nn_w != w or ch_nn_h != h:
        print(f"    AVISO (NN): dimensao final {ch_nn_w}x{ch_nn_h} difere da original {w}x{h}")
    save_image(challenge_nn, os.path.join(output_dir, "desafio_nn.png"))

    # Bilinear
    reduced_bi = resize_bilinear(img, 1/3)
    rh, rw = reduced_bi.shape[:2]
    print(f"    Bilinear reduzido: {rw}x{rh}")
    challenge_bi = resize_bilinear(reduced_bi, 3.0)
    ch_bi_h, ch_bi_w = challenge_bi.shape[:2]
    print(f"    Bilinear ampliado: {ch_bi_w}x{ch_bi_h}")
    if ch_bi_w != w or ch_bi_h != h:
        print(f"    AVISO (Bilinear): dimensao final {ch_bi_w}x{ch_bi_h} difere da original {w}x{h}")
    save_image(challenge_bi, os.path.join(output_dir, "desafio_bilinear.png"))


# ============================================================
# Execução principal
# ============================================================

def main():
    input_dir = "input"
    output_base = "output"

    # Verifica se a pasta input existe
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        print(f"Pasta '{input_dir}/' criada.")
        print(f"Coloque suas imagens dentro de '{input_dir}/' e execute novamente.")
        return

    # Lista imagens na pasta input
    images = [f for f in os.listdir(input_dir)
              if os.path.splitext(f)[1].lower() in EXTENSIONS]

    if not images:
        print(f"Nenhuma imagem encontrada em '{input_dir}/'.")
        print(f"Coloque suas imagens (PNG, JPG, BMP, etc.) dentro de '{input_dir}/' e execute novamente.")
        return

    print(f"Encontradas {len(images)} imagem(ns) em '{input_dir}/'.\n")

    for img_file in sorted(images):
        name = os.path.splitext(img_file)[0]
        input_path = os.path.join(input_dir, img_file)
        output_dir = os.path.join(output_base, name)

        print(f"{'='*60}")
        print(f"Processando: {img_file}")
        print(f"{'='*60}")

        process_image(input_path, output_dir)

        print(f"\n  Resultados salvos em '{output_dir}/'\n")

    print("Concluído! Verifique a pasta 'output/' para os resultados.")


if __name__ == "__main__":
    main()

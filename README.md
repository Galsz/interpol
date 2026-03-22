# Redimensionamento Manual de Imagens

Projeto em Python para **reamostragem espacial de imagens** com implementação **manual** de:

- **Vizinho Mais Próximo**
- **Interpolação Bilinear**

O programa aplica os fatores obrigatórios da atividade:

- **Zoom In:** `2x` e `3x`
- **Zoom Out:** `0.5x` e `1/3 (~0.33x)`

Também executa o **desafio** proposto:

- reduzir a imagem em **3x**;
- ampliar novamente em **3x**;
- comparar visualmente o resultado com a imagem original.

> **Observação:** não são usadas funções prontas de redimensionamento como `cv2.resize`, `PIL.Image.resize` ou equivalentes. Toda a lógica de mapeamento de coordenadas e interpolação foi implementada manualmente.

---

## Objetivo

Explorar os fundamentos matemáticos da reamostragem espacial de imagens, utilizando **mapeamento reverso** para calcular, para cada pixel da imagem de saída, a posição correspondente na imagem de entrada.

---

## Tecnologias utilizadas

- **Python 3**
- **NumPy**
- **Pillow (PIL)**

---

## Estrutura esperada

```text
projeto/
├── main.py
├── input/
└── output/
```

### Entradas
Coloque uma ou mais imagens dentro da pasta `input/`.

### Saídas
Para cada imagem encontrada, o programa cria uma pasta dentro de `output/` com os arquivos gerados.

Exemplo:

```text
output/
└── minha_imagem/
    ├── original.png
    ├── nn_2x.png
    ├── nn_3x.png
    ├── nn_0.5x.png
    ├── nn_0.33x.png
    ├── bilinear_2x.png
    ├── bilinear_3x.png
    ├── bilinear_0.5x.png
    ├── bilinear_0.33x.png
    ├── desafio_nn.png
    └── desafio_bilinear.png
```

---

## Como executar

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Coloque as imagens na pasta `input/`

Formatos aceitos:

- `.png`
- `.jpg`
- `.jpeg`
- `.bmp`
- `.tiff`
- `.tif`
- `.webp`

### 3. Execute o script

```bash
python main.py
```

> Se o seu arquivo ainda estiver com outro nome, como `Código colado.py`, renomeie para `main.py` antes de commitar ou executar.

---

## Funcionamento

### 1. Vizinho Mais Próximo

Para cada pixel da imagem de saída:

1. calcula-se a coordenada correspondente na imagem original usando **mapeamento reverso**;
2. arredonda-se para o pixel inteiro mais próximo;
3. copia-se a cor desse pixel para a imagem de saída.

Fórmulas principais:

```text
x_orig = (x_out + 0.5) / escala - 0.5
y_orig = (y_out + 0.5) / escala - 0.5
```

```text
x_nn = round(x_orig)
y_nn = round(y_orig)
```

---

### 2. Interpolação Bilinear

Para cada pixel da saída:

1. calcula-se a posição correspondente na imagem original;
2. localizam-se os **4 vizinhos** mais próximos;
3. calcula-se a parte fracionária da posição;
4. combina-se a cor dos 4 vizinhos com pesos proporcionais à distância.

Fórmulas principais:

```text
x0 = floor(x_orig)
y0 = floor(y_orig)
x1 = min(x0 + 1, largura - 1)
y1 = min(y0 + 1, altura - 1)
```

```text
dx = x_orig - x0
dy = y_orig - y0
```

Forma expandida:

```text
I(x,y) = (1-dx)(1-dy)Q11 + dx(1-dy)Q21 + (1-dx)dyQ12 + dxdyQ22
```

Forma usada no código:

```text
top = Q11 * (1 - dx) + Q21 * dx
bot = Q12 * (1 - dx) + Q22 * dx
I(x,y) = top * (1 - dy) + bot * dy
```

---

## Desafio proposto

O código também executa automaticamente o experimento:

1. reduz a imagem em `1/3`;
2. amplia a imagem reduzida em `3x`;
3. salva os resultados para:
   - **Vizinho Mais Próximo**
   - **Interpolação Bilinear**

### Análise esperada

Após reduzir e ampliar novamente, a imagem **não retorna exatamente ao estado original**. Isso ocorre porque a etapa de redução remove parte das informações visuais. Ao ampliar novamente:

- o **Vizinho Mais Próximo** tende a apresentar mais serrilhado e blocos visíveis;
- a **Bilinear** gera resultado mais suave, porém com perda de nitidez e leve borramento.

---

## Organização do código

O script foi dividido nas seguintes partes:

- `resize_nearest(img, scale)`
  - implementa o redimensionamento por Vizinho Mais Próximo;
- `resize_bilinear(img, scale)`
  - implementa o redimensionamento por Interpolação Bilinear;
- `load_image(path)`
  - carrega a imagem como array NumPy em RGB;
- `save_image(arr, path)`
  - salva a imagem processada;
- `process_image(input_path, output_dir)`
  - executa todos os fatores obrigatórios e o desafio para uma imagem;
- `main()`
  - percorre as imagens da pasta `input/` e organiza os resultados em `output/`.

---

## Observações importantes

- O programa utiliza **loops manuais** para percorrer pixel por pixel.
- O redimensionamento é feito por **mapeamento reverso**, evitando falhas de preenchimento na imagem de saída.
- Há tratamento de borda com `min` e `max` para impedir acesso fora dos limites da imagem.
- A saída é mantida em `uint8`, com `clip` para garantir valores válidos entre `0` e `255`.

---

## Autores

- **Geovane Araujo de Lima Silva** — RA: `00111884`
- **João Vitor Marinonio de Almeida** — RA: `00111970`

**Universidade de Sorocaba — UNISO**

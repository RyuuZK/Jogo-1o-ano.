# 🧙‍♂️ Mago Sobrevivente

Um jogo de sobrevivência estilo *bullet hell* minimalista, desenvolvido em Python utilizando a biblioteca **Pyxel** (uma engine de jogos retro de 8 bits). Controle um mago, destrua hordas de morcegos e melhore seus atributos para sobreviver o maior tempo possível!

---

## 🕹️ Como Jogar

O objetivo é sobreviver enquanto elimina os inimigos que surgem pelas bordas da tela. A cada 50 pontos de upgrade, você poderá escolher uma melhoria para o seu mago.

### Controles:
* **W, A, S, D:** Movimentam o mago pela tela.
* **Clique Esquerdo do Mouse:** Atira bolas de fogo na direção do ponteiro.
* **Teclas 1, 2, 3 (no Menu de Upgrade):** Selecionam a melhoria desejada.
* **ENTER:** Inicia o jogo no menu principal.
* **R:** Reinicia a partida após o Game Over.

---

## ⚙️ Funcionalidades Programadas

* **Sistema de Ondas Progressivo:** O limite de inimigos na tela aumenta conforme você alcança marcas de 15 e 50 eliminações.
* **Menu de Upgrades Aleatórios:** Escolhas geradas dinamicamente entre Velocidade de Ataque, Aumento de Dano, Cura/Vida Máxima e Disparo Múltiplo.
* **Mecânica de Vetores para Tiros:** Sistema matemático para calcular a trajetória exata da bola de fogo em direção ao clique do mouse, incluindo cálculo de rotação de matriz para tiros adjacentes (*multishot*).
* **Animações de Sprite (Flip-book):** Alternância automática de frames para a movimentação do mago e o bater de asas dos morcegos.

---

## 🛠️ Pré-requisitos e Como Executar

Para rodar o jogo localmente, você precisará ter o **Python 3** e a biblioteca **Pyxel** instalados na sua máquina.

1. Instale o Pyxel via terminal/prompt de comando:
   ```bash
   pip install pyxel

2. Certifique-se de manter os arquivos de imagem (mapa.png, mago.png e morcego.png) na mesma pasta do código principal.

3. Execute o arquivo do jogo:
Bash
python jogomago.py

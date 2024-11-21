# Nim-Game
## Descrição do Jogo
Nim é um jogo clássico de estratégia no qual dois jogadores se alternam para remover qualquer quantidade de objetos de uma única pilha. O objetivo é evitar ser o jogador que remove o último objeto, pois isso resulta em derrota. A complexidade e as possibilidades estratégicas do jogo aumentam conforme o número de pilhas disponíveis.

## Objetivo do Projeto
Este projeto implementa uma Inteligência Artificial (IA) para aprender e dominar a estratégia ideal do jogo Nim, utilizando aprendizado por reforço com os algoritmos SARSA e Q-Learning. Esses algoritmos associam recompensas a pares de estados e ações, permitindo que a IA aprenda a tomar decisões ideais ao jogar.

## Como Funciona
Treinamento por Autojogo:
A IA joga contra si mesma repetidamente, explorando diferentes estratégias e aprendendo com as consequências de suas ações.

Recompensas Baseadas no Desempenho:

- Derrota: Ações que levam à derrota recebem uma recompensa de -1.
- Vitória: Ações que forçam a derrota do adversário recebem uma recompensa de +1.
- Neutras: Ações intermediárias recebem uma recompensa de 0.
Aprendizado:

No SARSA, a IA aprende com base na sequência de estados, ações e recompensas reais observados.
No Q-Learning, a IA busca maximizar a recompensa futura esperada, considerando o melhor resultado possível a partir de um estado dado.

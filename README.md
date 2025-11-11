# 🎓 Sistema de Navegação Campus UFMA - Algoritmo A*

## 👥 Autores

- **Yann Cristhyan Carvalho Pinheiro** - Matrícula: 2020010563
- **Jônathas Silva Oliveira** - Matrícula: 2021024590
- **João Victor Lima Azevedo** - Matrícula: 2022021127

**Curso**: BICT - Bacharelado Interdisciplinar em Ciência e Tecnologia  
**Instituição**: UFMA - Universidade Federal do Maranhão  
**Disciplina**: Inteligência Artificial  
**Professor**: Prof. Dr. Alex Oliveira Barradas Filho

---

## 📋 Descrição do Projeto

Sistema de navegação inteligente para o **Campus UFMA Bacanga** que utiliza o algoritmo de busca informada **A*** (A-estrela) para encontrar o caminho mais curto entre dois pontos do campus.

### 🎯 Objetivo

Modelar o problema de navegação no campus como um grafo e implementar o algoritmo A* usando a biblioteca NetworkX do Python, demonstrando conceitos fundamentais de Inteligência Artificial aplicados a um cenário real.

---

## 🧠 Conceitos de IA Implementados

### Algoritmo A* (A-estrela)

O A* é um algoritmo de busca informada que combina:

- **g(n)**: Custo real do caminho do início até o nó atual
- **h(n)**: Heurística (estimativa) do nó atual até o objetivo
- **f(n) = g(n) + h(n)**: Função de avaliação total

**Características**:
- ✅ **Completo**: Sempre encontra uma solução se ela existir
- ✅ **Ótimo**: Encontra o caminho de menor custo
- ✅ **Eficiente**: Usa heurística para guiar a busca
- ✅ **Admissível**: A heurística nunca superestima o custo real

### Heurística Utilizada

**Distância Euclidiana**: Calculada como a distância em linha reta entre dois pontos.

```python
h(n) = √[(x2 - x1)² + (y2 - y1)²]
```

Esta heurística é **admissível** pois a distância em linha reta nunca é maior que a distância real no grafo.

---

## 📍 Localizações do Campus

O sistema modela 20 localizações do Campus UFMA Bacanga:

### Portarias
- Portaria Principal
- Portaria Fundos

### Administrativo
- Reitoria
- PROEN

### Centros de Ensino
- BICT (Bacharelado Interdisciplinar)
- CCET (Centro de Ciências Exatas e Tecnologia)
- CCH (Centro de Ciências Humanas)
- CCBS (Centro de Ciências Biológicas e da Saúde)
- CCSo (Centro de Ciências Sociais)
- Prédio Paulo Freire
- Prédio de Educação Física

### Estudo
- Biblioteca Central
- Sala de Estudo BICT

### Alimentação
- Restaurante Universitário (RU)
- Cantina Central
- Lanchonete CCET

### Esporte e Lazer
- Ginásio Castelinho
- Quadras Esportivas
- Praça da Cidadania

---

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes)

### Passo 1: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 2: Executar o Programa

**Opção A: Exemplos Automáticos**
```bash
python navegacao_ufma.py
```
Executa 4 exemplos pré-definidos e gera mapas automaticamente.

**Opção B: Modo Interativo**
```bash
python exemplo_interativo.py
```
Interface interativa para testar rotas personalizadas.

**Opção C: Executar Testes**
```bash
python testes.py
```
Valida o funcionamento do sistema (deve mostrar 100% de sucesso).

---

## 📊 Exemplos de Uso

### Exemplo 1: Rota Simples

```python
from navegacao_ufma import NavegacaoCampusUFMA

nav = NavegacaoCampusUFMA()
caminho, custo, stats = nav.buscar_caminho('Portaria Principal', 'BICT')
```

**Saída**:
```
Rota encontrada: Portaria Principal → BICT
Caminho (5 pontos):
  1. Portaria Principal
     ↓ 200m
  2. Reitoria
     ↓ 180m
  3. CCBS
     ↓ 120m
  4. CCH
     ↓ 120m
  5. BICT ✓

📏 Distância total: 620 metros
⏱️  Tempo estimado: ~7 minutos a pé
```

### Exemplo 2: Comparar Rotas

```python
nav.comparar_rotas('BICT', [
    'Biblioteca Central',
    'Restaurante Universitário',
    'Ginásio Castelinho'
])
```

---

## 🗺️ Visualizações

O sistema gera mapas automáticos mostrando:
- **Nós em azul**: Locais do campus
- **Nó verde (quadrado)**: Ponto de partida
- **Nó vermelho (quadrado)**: Destino
- **Nós laranja**: Pontos intermediários do caminho
- **Linha vermelha grossa**: Caminho encontrado pelo A*
- **Distâncias**: Mostradas em metros nas arestas

Os mapas são salvos automaticamente na pasta `outputs/`.

---

## 📁 Estrutura do Projeto

```
navegacao-ufma-astar/
├── navegacao_ufma.py          # Código principal
├── exemplo_interativo.py       # Interface interativa
├── testes.py                   # Suite de testes
├── requirements.txt            # Dependências
├── README.md                   # Este arquivo
└── outputs/                    # Mapas gerados (criado automaticamente)
```

---

## 🧪 Validação

O sistema foi testado e validado com:
- ✅ 5 testes automatizados
- ✅ 100% de taxa de sucesso
- ✅ Verificação de otimalidade do A*
- ✅ Validação de rotas importantes do campus

Para executar os testes:
```bash
python testes.py
```

---

## 📈 Análise de Performance

### Complexidade

- **Temporal**: O(b^d) no pior caso, mas otimizado pela heurística
  - b = fator de ramificação (~3-4 conexões por nó)
  - d = profundidade da solução
  
- **Espacial**: O(b^d) - armazena nós na memória

### Otimalidade

O A* garante encontrar o caminho ótimo porque:
1. A heurística é **admissível** (nunca superestima)
2. A heurística é **consistente** (satisfaz desigualdade triangular)
3. Distância euclidiana ≤ Distância real no grafo

---

## 🎥 Vídeo Demonstrativo

[Link para vídeo no YouTube - até 5 minutos]

### Conteúdo do Vídeo
1. Apresentação do problema de navegação no campus
2. Modelagem como grafo (nós = locais, arestas = caminhos)
3. Explicação do algoritmo A*
4. Demonstração do código em execução
5. Análise dos resultados obtidos
6. Limitações e possíveis melhorias

---

## ⚠️ Limitações

1. **Distâncias Aproximadas**: Baseadas em estimativas, não medições precisas
2. **Grafo Estático**: Não considera obstáculos temporários ou obras
3. **Ambiente 2D**: Não considera diferenças de elevação
4. **Caminhos Pedestres**: Modelo focado em trajetos a pé

---

## 🔮 Melhorias Futuras

- [ ] Integrar com Google Maps para distâncias reais
- [ ] Adicionar modos de transporte (bicicleta, ônibus interno)
- [ ] Considerar horários de funcionamento dos locais
- [ ] Implementar rotas alternativas
- [ ] Interface web interativa
- [ ] Modo de acessibilidade (evitar escadas)

---

## 📚 Referências

1. **Russell, S., & Norvig, P.** (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
   - Capítulo 3: Solving Problems by Searching
   - Seção 3.5: Informed Search Strategies

2. **Hart, P. E., Nilsson, N. J., & Raphael, B.** (1968). *A Formal Basis for the Heuristic Determination of Minimum Cost Paths*. IEEE Transactions on Systems Science and Cybernetics.

3. **NetworkX Documentation**: https://networkx.org/documentation/stable/

---

## 📞 Contato

Para dúvidas ou sugestões sobre o projeto, entre em contato com os autores através dos canais institucionais da UFMA.

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte da avaliação da disciplina de Inteligência Artificial da UFMA.

---

**🎓 Desenvolvido com dedicação para a disciplina de IA - UFMA 2025**

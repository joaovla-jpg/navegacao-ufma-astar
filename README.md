# 🎓 Sistema de Navegação Campus UFMA - Algoritmo A*

## 📋 Descrição do Projeto

Este projeto implementa um sistema de navegação inteligente para o **Campus UFMA Bacanga** e pontos importantes de **São Luís/MA**, utilizando o algoritmo de busca informada **A*** (A-estrela).

### 🎯 Objetivo

Modelar o problema de navegação como um grafo e encontrar o **caminho mais curto** entre dois pontos, considerando:
- Localizações reais do campus UFMA
- Distâncias aproximadas entre os prédios
- Pontos externos relevantes (Shopping da Ilha, Aeroporto, Praias, etc.)

### 🧠 Conceitos de IA Aplicados

**Busca Informada (A*)**:
- **Estado**: Localização atual no campus/cidade
- **Ações**: Mover para localizações adjacentes
- **Função de Custo g(n)**: Distância real percorrida (em metros)
- **Heurística h(n)**: Distância euclidiana até o destino
- **Função de Avaliação f(n) = g(n) + h(n)**: Prioriza nós mais promissores

**Por que A*?**
- ✅ **Completo**: Sempre encontra uma solução se ela existir
- ✅ **Ótimo**: Encontra o caminho de menor custo
- ✅ **Eficiente**: Usa heurística para guiar a busca
- ✅ **Admissível**: A heurística nunca superestima o custo real

---

## 📍 Localizações Implementadas

### Campus UFMA Bacanga
- **Portarias**: Principal, Fundos
- **Administrativo**: Reitoria, PROEN
- **Ensino**: BICT, CCET, CCH, CCBS, CCSo
- **Estudo**: Biblioteca Central, Sala de Estudo BICT
- **Alimentação**: RU, Cantina Central, Lanchonete CCET
- **Esporte**: Ginásio Castelinho, Quadras Esportivas, Praça da Cidadania

### Pontos Externos
- Terminal Cohab
- Shopping da Ilha
- Lagoa da Jansen
- Praia do Calhau
- Centro Histórico
- Aeroporto

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo 1: Clonar/Baixar o Projeto

Se estiver no GitHub:
```bash
git clone https://github.com/seu-usuario/navegacao-ufma-astar.git
cd navegacao-ufma-astar
```

Se baixou o arquivo compactado:
```bash
unzip navegacao-ufma-astar.zip
cd navegacao-ufma-astar
```

### Passo 2: Criar Ambiente Virtual (Recomendado)

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Executar o Programa

```bash
python navegacao_ufma.py
```

### 📊 Saída Esperada

O programa irá:
1. Listar todos os locais disponíveis
2. Executar 4 exemplos de navegação
3. Mostrar rotas detalhadas com distâncias
4. Gerar visualizações gráficas do mapa
5. Salvar o mapa em PNG

---

## 💻 Estrutura do Código

```
navegacao-ufma-astar/
│
├── navegacao_ufma.py      # Código principal
├── requirements.txt        # Dependências
├── README.md              # Este arquivo
└── outputs/               # Mapas gerados (criado automaticamente)
    └── mapa_navegacao_ufma.png
```

### Classes Principais

#### `NavegacaoCampusUFMA`

**Métodos principais**:

```python
__init__()                    # Inicializa o grafo
_criar_mapa_campus()         # Define locais e conexões
heuristica(no, objetivo)     # Calcula distância euclidiana
a_estrela(inicio, objetivo)  # Implementa busca A*
visualizar_mapa(caminho)     # Gera visualização
listar_locais()              # Lista todos os pontos
comparar_rotas(inicio, destinos)  # Compara múltiplas rotas
```

---

## 🔬 Exemplos de Uso

### Exemplo 1: Rota Simples
```python
nav = NavegacaoCampusUFMA()
caminho, custo, stats = nav.a_estrela('Portaria Principal', 'BICT')
```

**Saída**:
```
🎯 ROTA ENCONTRADA: Portaria Principal → BICT
📍 Caminho (2 locais):
   1. Portaria Principal
      ↓ 350m
   2. BICT ✓

📏 Distância total: 350 metros (0.35 km)
```

### Exemplo 2: Rota Complexa
```python
caminho, custo, stats = nav.a_estrela('BICT', 'Aeroporto')
```

**Saída**: Mostra caminho com múltiplas paradas

### Exemplo 3: Comparação de Rotas
```python
nav.comparar_rotas('BICT', ['RU', 'Biblioteca Central', 'CCET'])
```

---

## 📈 Análise de Performance

### Complexidade

- **Temporal**: O(b^d) no pior caso, mas muito melhor na prática
  - b = fator de ramificação (média de 3-4 conexões por nó)
  - d = profundidade da solução
  
- **Espacial**: O(b^d) - precisa manter nós na memória

### Otimalidade

O algoritmo A* é **ótimo** porque:
1. A heurística é **admissível** (nunca superestima)
2. A heurística é **consistente** (satisfaz a desigualdade triangular)
3. Distância euclidiana ≤ Distância real no grafo

---

## 🎥 Vídeo Demonstrativo

[Link para vídeo no YouTube - até 5 minutos]

**Conteúdo do vídeo**:
1. Apresentação do problema (navegação no campus)
2. Modelagem como grafo (nós = locais, arestas = caminhos)
3. Implementação do A* no código
4. Demonstração executando 3-4 exemplos
5. Análise dos resultados
6. Limitações e melhorias futuras

---

## ⚠️ Limitações

1. **Distâncias Aproximadas**: Os valores são estimativas, não medições precisas
2. **Grafo Estático**: Não considera obstáculos temporários ou obras
3. **Sem Informações de Trânsito**: Não leva em conta horários de pico
4. **Caminhos Pedestres**: Modelo focado em trajetos a pé
5. **Simplificação 2D**: Não considera diferenças de elevação

---

## 🚀 Próximos Passos

### Melhorias Técnicas
- [ ] Adicionar mais locais do campus
- [ ] Integrar com Google Maps API para distâncias reais
- [ ] Implementar rotas alternativas
- [ ] Adicionar estimativa de tempo considerando meio de transporte
- [ ] Interface web interativa

### Funcionalidades
- [ ] Modo "evitar escadas" (acessibilidade)
- [ ] Rotas com pontos de interesse (ex: passar pela biblioteca)
- [ ] Horários de funcionamento dos locais
- [ ] Integração com horários de ônibus
- [ ] App mobile

### Algoritmos Alternativos
- [ ] Comparar com Dijkstra (busca sem informação)
- [ ] Implementar Busca Gulosa
- [ ] Testar IDA* (economia de memória)

---

## 📚 Referências

1. **Russell, S., & Norvig, P.** (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
   - Capítulo 3: Solving Problems by Searching
   - Seção 3.5: Informed (Heuristic) Search Strategies

2. **Hart, P. E., Nilsson, N. J., & Raphael, B.** (1968). *A Formal Basis for the Heuristic Determination of Minimum Cost Paths*. IEEE Transactions on Systems Science and Cybernetics.

3. **NetworkX Documentation**: https://networkx.org/documentation/stable/

4. **Material da Disciplina**: Prof. Dr. Alex Oliveira Barradas Filho - BICT/UFMA

---

## 👨‍💻 Autor

**Estudante do BICT - Bacharelado Interdisciplinar em Ciência e Tecnologia**  
Universidade Federal do Maranhão (UFMA)  
Disciplina: Inteligência Artificial  
Prof. Dr. Alex Oliveira Barradas Filho

---

## 📝 Licença

Este projeto foi desenvolvido para fins educacionais como parte da avaliação da disciplina de Inteligência Artificial.

---

## 🤝 Contribuições

Sugestões e melhorias são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novos locais
- Propor melhorias no algoritmo
- Corrigir distâncias

---

## ❓ FAQ

**P: Por que A* e não Dijkstra?**  
R: A* é mais eficiente que Dijkstra pois usa heurística para guiar a busca, explorando menos nós.

**P: A heurística pode ser melhorada?**  
R: Sim! Poderíamos usar distância de Manhattan ou considerar barreiras físicas reais do campus.

**P: Como adicionar novos locais?**  
R: Edite o método `_criar_mapa_campus()` adicionando o local em `locais` e suas conexões em `caminhos`.

**P: Funciona offline?**  
R: Sim! Todo o grafo está hard-coded, não precisa de internet.

---

**🎓 Feito com dedicação para a disciplina de IA - UFMA 2024**

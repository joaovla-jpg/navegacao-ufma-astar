"""
Sistema de Navegação Campus UFMA - Algoritmo A*
Trabalho de IA - Prof. Alex Barradas
BICT/UFMA
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


class NavegacaoCampusUFMA:
    
    def __init__(self):
        self.grafo = nx.Graph()
        self.posicoes = {}
        self._montar_grafo()
    
    def _montar_grafo(self):
        # Coordenadas aproximadas dos locais do campus (em metros)
        # origem (0,0) = portaria principal
        locais = {
            'Portaria Principal': (0, 0),
            'Portaria Fundos': (800, 100),
            'Reitoria': (200, 150),
            'PROEN': (250, 200),
            'BICT': (150, 300),
            'CCET': (300, 350),
            'CCH': (400, 250),
            'CCBS': (350, 150),
            'CCSo': (500, 300),
            'Biblioteca Central': (250, 400),
            'Sala de Estudo BICT': (180, 320),
            'Restaurante Universitário': (450, 400),
            'Cantina Central': (300, 250),
            'Lanchonete CCET': (320, 370),
            'Ginásio Castelinho': (600, 450),
            'Quadras Esportivas': (550, 500),
            'Praça da Cidadania': (400, 350),
            'Ponto de Ônibus Cohab': (-200, 50),
            'Terminal Cohab': (-500, 100),
            'Shopping da Ilha': (-1200, -500),
            'Lagoa da Jansen': (1500, -800),
            'Praia do Calhau': (2000, -1200),
            'Centro Histórico': (-2500, -1000),
            'Aeroporto': (3000, 500)
        }
        
        self.posicoes = locais
        
        for local in locais:
            self.grafo.add_node(local, pos=locais[local])
        
        # Definir os caminhos com as distâncias (em metros)
        caminhos = [
            ('Portaria Principal', 'Reitoria', 250),
            ('Portaria Principal', 'BICT', 350),
            ('Portaria Principal', 'Ponto de Ônibus Cohab', 250),
            ('Portaria Fundos', 'Ginásio Castelinho', 300),
            ('Portaria Fundos', 'Restaurante Universitário', 450),
            ('Reitoria', 'PROEN', 80),
            ('Reitoria', 'CCBS', 200),
            ('PROEN', 'Cantina Central', 100),
            ('BICT', 'Sala de Estudo BICT', 50),
            ('BICT', 'CCET', 200),
            ('BICT', 'Biblioteca Central', 150),
            ('BICT', 'Cantina Central', 180),
            ('Sala de Estudo BICT', 'Biblioteca Central', 120),
            ('CCET', 'Lanchonete CCET', 30),
            ('CCET', 'Biblioteca Central', 100),
            ('CCET', 'Praça da Cidadania', 120),
            ('CCET', 'CCH', 150),
            ('Lanchonete CCET', 'Biblioteca Central', 80),
            ('Biblioteca Central', 'Restaurante Universitário', 250),
            ('Biblioteca Central', 'Praça da Cidadania', 180),
            ('CCH', 'CCSo', 150),
            ('CCH', 'Cantina Central', 120),
            ('CCH', 'Praça da Cidadania', 80),
            ('CCBS', 'Cantina Central', 180),
            ('CCSo', 'Praça da Cidadania', 80),
            ('CCSo', 'Restaurante Universitário', 180),
            ('Restaurante Universitário', 'Ginásio Castelinho', 200),
            ('Restaurante Universitário', 'Quadras Esportivas', 150),
            ('Restaurante Universitário', 'Portaria Fundos', 350),
            ('Ginásio Castelinho', 'Quadras Esportivas', 100),
            ('Quadras Esportivas', 'Portaria Fundos', 300),
            ('Praça da Cidadania', 'Restaurante Universitário', 100),
            ('Praça da Cidadania', 'Cantina Central', 120),
            ('Ponto de Ônibus Cohab', 'Terminal Cohab', 400),
            ('Terminal Cohab', 'Shopping da Ilha', 800),
            ('Shopping da Ilha', 'Centro Histórico', 1500),
            ('Shopping da Ilha', 'Lagoa da Jansen', 2800),
            ('Lagoa da Jansen', 'Praia do Calhau', 800),
            ('Portaria Fundos', 'Lagoa da Jansen', 1200),
            ('Portaria Fundos', 'Aeroporto', 2500),
            ('Lagoa da Jansen', 'Aeroporto', 3800),
            ('Praia do Calhau', 'Aeroporto', 2800)
        ]
        
        for origem, destino, dist in caminhos:
            self.grafo.add_edge(origem, destino, weight=dist)
    
    def calc_heuristica(self, atual, objetivo):
        # distancia euclidiana entre dois pontos
        x1, y1 = self.posicoes[atual]
        x2, y2 = self.posicoes[objetivo]
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def buscar_caminho(self, inicio, fim, mostrar_info=True):
        """Busca o melhor caminho usando A*"""
        
        if inicio not in self.grafo:
            print(f"Erro: '{inicio}' não encontrado")
            return None, float('inf'), {}
        
        if fim not in self.grafo:
            print(f"Erro: '{fim}' não encontrado")
            return None, float('inf'), {}
        
        try:
            # usar A* do networkx
            caminho = nx.astar_path(
                self.grafo,
                inicio,
                fim,
                heuristic=lambda u, v: self.calc_heuristica(u, fim),
                weight='weight'
            )
            
            custo = nx.astar_path_length(
                self.grafo,
                inicio,
                fim,
                heuristic=lambda u, v: self.calc_heuristica(u, fim),
                weight='weight'
            )
            
            # calcular algumas estatisticas
            stats = {
                'num_paradas': len(caminho),
                'num_trechos': len(caminho) - 1,
                'dist_euclidiana': self.calc_heuristica(inicio, fim)
            }
            
            if mostrar_info:
                self._print_rota(inicio, fim, caminho, custo, stats)
            
            return caminho, custo, stats
            
        except nx.NetworkXNoPath:
            print(f"Não existe caminho entre '{inicio}' e '{fim}'")
            return None, float('inf'), {}
    
    def _print_rota(self, inicio, fim, caminho, custo, stats):
        print("\n" + "="*60)
        print(f"Rota: {inicio} → {fim}")
        print("="*60)
        print(f"\nCaminho ({len(caminho)} locais):")
        
        for i, local in enumerate(caminho, 1):
            if i < len(caminho):
                prox = caminho[i]
                dist = self.grafo[local][prox]['weight']
                print(f"  {i}. {local}")
                print(f"     ↓ {dist}m")
            else:
                print(f"  {i}. {local} ✓")
        
        print(f"\nDistância total: {custo:.0f}m ({custo/1000:.2f}km)")
        print(f"Distância em linha reta: {stats['dist_euclidiana']:.0f}m")
        print(f"Eficiência: {(stats['dist_euclidiana']/custo)*100:.1f}%")
        
        # tempo estimado caminhando a 5km/h
        tempo_min = (custo/1000) / 5 * 60
        print(f"Tempo estimado a pé: ~{tempo_min:.0f} min")
        print("="*60 + "\n")
    
    def desenhar_mapa(self, caminho=None, salvar=True):
        plt.figure(figsize=(20, 16))
        
        # separar nos do campus dos externos
        nos_campus = []
        nos_externos = []
        for n in self.grafo.nodes():
            x, y = self.posicoes[n]
            if abs(x) < 1000 and abs(y) < 1000:
                nos_campus.append(n)
            else:
                nos_externos.append(n)
        
        # desenhar todas as arestas em cinza
        nx.draw_networkx_edges(
            self.grafo,
            self.posicoes,
            edge_color='lightgray',
            width=1,
            alpha=0.5
        )
        
        # se tem caminho, destacar
        if caminho:
            edges_caminho = [(caminho[i], caminho[i+1]) for i in range(len(caminho)-1)]
            
            nx.draw_networkx_edges(
                self.grafo,
                self.posicoes,
                edgelist=edges_caminho,
                edge_color='red',
                width=4,
                alpha=0.8
            )
            
            # nos intermediarios em laranja
            if len(caminho) > 2:
                nx.draw_networkx_nodes(
                    self.grafo,
                    self.posicoes,
                    nodelist=caminho[1:-1],
                    node_color='orange',
                    node_size=600,
                    alpha=0.9
                )
            
            # inicio em verde
            nx.draw_networkx_nodes(
                self.grafo,
                self.posicoes,
                nodelist=[caminho[0]],
                node_color='green',
                node_size=800,
                alpha=0.9,
                node_shape='s'
            )
            
            # fim em vermelho
            nx.draw_networkx_nodes(
                self.grafo,
                self.posicoes,
                nodelist=[caminho[-1]],
                node_color='red',
                node_size=800,
                alpha=0.9,
                node_shape='s'
            )
        
        # desenhar nos do campus
        outros_campus = [n for n in nos_campus if not caminho or n not in caminho]
        if outros_campus:
            nx.draw_networkx_nodes(
                self.grafo,
                self.posicoes,
                nodelist=outros_campus,
                node_color='lightblue',
                node_size=400,
                alpha=0.7
            )
        
        # desenhar nos externos
        outros_externos = [n for n in nos_externos if not caminho or n not in caminho]
        if outros_externos:
            nx.draw_networkx_nodes(
                self.grafo,
                self.posicoes,
                nodelist=outros_externos,
                node_color='lightyellow',
                node_size=400,
                alpha=0.7
            )
        
        # labels
        nx.draw_networkx_labels(
            self.grafo,
            self.posicoes,
            font_size=8,
            font_weight='bold'
        )
        
        # mostrar distancias no caminho
        if caminho:
            edge_labels = {}
            for i in range(len(caminho)-1):
                u, v = caminho[i], caminho[i+1]
                peso = self.grafo[u][v]['weight']
                edge_labels[(u, v)] = f"{peso:.0f}m"
            
            nx.draw_networkx_edge_labels(
                self.grafo,
                self.posicoes,
                edge_labels=edge_labels,
                font_size=7,
                font_color='darkred'
            )
        
        plt.title(
            'Mapa de Navegação - Campus UFMA Bacanga e São Luís/MA\nAlgoritmo A*',
            fontsize=16,
            fontweight='bold',
            pad=20
        )
        
        # legenda
        from matplotlib.patches import Patch
        legend = [
            Patch(facecolor='lightblue', label='Campus UFMA'),
            Patch(facecolor='lightyellow', label='Pontos Externos'),
        ]
        if caminho:
            legend.extend([
                Patch(facecolor='green', label='Início'),
                Patch(facecolor='red', label='Destino'),
                Patch(facecolor='orange', label='Caminho'),
            ])
        plt.legend(handles=legend, loc='upper left', fontsize=10)
        
        plt.axis('off')
        plt.tight_layout()
        
        if salvar:
            plt.savefig('/mnt/user-data/outputs/mapa_ufma.png', dpi=300, bbox_inches='tight')
            print("Mapa salvo: mapa_ufma.png")
        
        plt.show()
    
    def listar_locais(self):
        print("\n" + "="*60)
        print("Locais Disponíveis")
        print("="*60)
        
        categorias = {
            'Portarias': ['Portaria Principal', 'Portaria Fundos'],
            'Administrativo': ['Reitoria', 'PROEN'],
            'Centros de Ensino': ['BICT', 'CCET', 'CCH', 'CCBS', 'CCSo'],
            'Estudo': ['Biblioteca Central', 'Sala de Estudo BICT'],
            'Alimentação': ['Restaurante Universitário', 'Cantina Central', 'Lanchonete CCET'],
            'Esporte': ['Ginásio Castelinho', 'Quadras Esportivas', 'Praça da Cidadania'],
            'Externos': ['Ponto de Ônibus Cohab', 'Terminal Cohab', 'Shopping da Ilha', 
                        'Lagoa da Jansen', 'Praia do Calhau', 'Centro Histórico', 'Aeroporto']
        }
        
        for cat, locs in categorias.items():
            print(f"\n{cat}:")
            for loc in locs:
                print(f"  • {loc}")
        print("\n" + "="*60 + "\n")
    
    def comparar_destinos(self, origem, destinos):
        """Compara distancias de uma origem para varios destinos"""
        print("\n" + "="*60)
        print(f"Comparando rotas de: {origem}")
        print("="*60 + "\n")
        
        resultados = []
        for dest in destinos:
            caminho, custo, _ = self.buscar_caminho(origem, dest, mostrar_info=False)
            if caminho:
                resultados.append((dest, custo, len(caminho)))
        
        resultados.sort(key=lambda x: x[1])
        
        print(f"{'Destino':<30} {'Distância':<20} {'Paradas'}")
        print("-" * 60)
        for dest, custo, paradas in resultados:
            print(f"{dest:<30} {custo:>6.0f}m ({custo/1000:.2f}km)   {paradas} locais")
        print("\n" + "="*60 + "\n")


def main():
    print("\n" + "="*60)
    print("Sistema de Navegação - Campus UFMA")
    print("Algoritmo A* - Trabalho de IA")
    print("="*60 + "\n")
    
    nav = NavegacaoCampusUFMA()
    
    # listar locais
    nav.listar_locais()
    
    # exemplo 1: ir pra aula
    print("\nExemplo 1: Chegando na UFMA")
    c1, custo1, _ = nav.buscar_caminho('Portaria Principal', 'BICT')
    nav.desenhar_mapa(c1, salvar=True)
    
    # exemplo 2: ir almoçar
    print("\nExemplo 2: Indo almoçar no RU")
    c2, custo2, _ = nav.buscar_caminho('BICT', 'Restaurante Universitário')
    nav.desenhar_mapa(c2, salvar=False)
    
    # exemplo 3: rota longa
    print("\nExemplo 3: Indo pro aeroporto")
    c3, custo3, _ = nav.buscar_caminho('BICT', 'Aeroporto')
    nav.desenhar_mapa(c3, salvar=False)
    
    # exemplo 4: comparar distancias
    print("\nExemplo 4: Comparando rotas do BICT")
    nav.comparar_destinos('BICT', [
        'Biblioteca Central',
        'Restaurante Universitário',
        'CCET',
        'Ginásio Castelinho',
        'Shopping da Ilha',
        'Praia do Calhau'
    ])
    
    print("\nPrograma finalizado!")


if __name__ == "__main__":
    main()

"""
Sistema de Navegação Campus UFMA - Algoritmo A*
Trabalho de IA - Prof. Alex Barradas
BICT/UFMA
VERSÃO CORRIGIDA - Distâncias reais e linhas de ônibus L1/L2
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
        # Coordenadas reais aproximadas (em metros) - São Luís/MA
        # origem (0,0) = Portaria Principal UFMA
        locais = {
            # Campus UFMA Bacanga - Disposição Real
            'Portaria Principal': (0, 0),
            'Reitoria': (200, 150),
            'PROEN': (250, 200),
            'CCBS': (350, 150),
            'Cantina Central': (300, 250),
            'CCH': (400, 250),
            'CCET': (300, 350),
            'Lanchonete CCET': (320, 370),
            'Biblioteca Central': (250, 400),
            'CCSo': (500, 300),
            'Praça da Cidadania': (400, 350),
            'Restaurante Universitário': (450, 400),
            'Quadras Esportivas': (550, 500),
            'Ginásio Castelinho': (600, 450),
            'Prédio Paulo Freire': (500, 200),
            'Prédio Educação Física': (700, 100),  # Ponto final L1
            'Portaria Fundos': (800, 100),
            'BICT': (900, 150),  # Ponto final L2 (depois da Ed. Física)
            'Sala de Estudo BICT': (880, 170),
            
            # Pontos de Ônibus Campus
            'Ponto Ônibus Campus': (-50, 0),
            
            # Terminais (distâncias reais de São Luís)
            'Terminal Praia Grande': (-8000, -3000),  # ~10km do campus
            'Terminal Cohab': (-6000, 2000),  # ~7km do campus
            
            # Pontos Externos
            'Shopping da Ilha': (-5000, -1000),  # ~6km
            'Centro Histórico': (-11000, -3500),  # ~12km
            'Lagoa da Jansen': (3500, -2000),  # ~4km leste
            'Praia do Calhau': (5500, -3500),  # ~7km leste
            'Aeroporto': (12000, 8000)  # ~15km nordeste
        }
        
        self.posicoes = locais
        
        for local in locais:
            self.grafo.add_node(local, pos=locais[local])
        
        # Caminhos dentro do campus (distâncias reais em metros)
        caminhos = [
            # Entrada principal
            ('Portaria Principal', 'Ponto Ônibus Campus', 50),
            ('Portaria Principal', 'Reitoria', 250),
            ('Portaria Principal', 'CCBS', 400),
            
            # Prédios administrativos
            ('Reitoria', 'PROEN', 80),
            ('Reitoria', 'CCBS', 200),
            ('PROEN', 'Cantina Central', 100),
            
            # Centros de ensino
            ('CCBS', 'Cantina Central', 180),
            ('Cantina Central', 'CCH', 120),
            ('Cantina Central', 'CCET', 150),
            ('CCH', 'CCSo', 150),
            ('CCH', 'Praça da Cidadania', 130),
            ('CCH', 'Prédio Paulo Freire', 180),
            
            # CCET e arredores
            ('CCET', 'Lanchonete CCET', 30),
            ('CCET', 'Biblioteca Central', 100),
            ('CCET', 'Praça da Cidadania', 120),
            ('Lanchonete CCET', 'Biblioteca Central', 80),
            
            # Biblioteca e área de estudo
            ('Biblioteca Central', 'Restaurante Universitário', 250),
            ('Biblioteca Central', 'Praça da Cidadania', 180),
            
            # CCSo e área social
            ('CCSo', 'Praça da Cidadania', 80),
            ('CCSo', 'Restaurante Universitário', 180),
            ('CCSo', 'Prédio Paulo Freire', 100),
            
            # RU e área esportiva
            ('Praça da Cidadania', 'Restaurante Universitário', 100),
            ('Restaurante Universitário', 'Ginásio Castelinho', 200),
            ('Restaurante Universitário', 'Quadras Esportivas', 150),
            ('Ginásio Castelinho', 'Quadras Esportivas', 100),
            
            # Prédio Paulo Freire
            ('Prédio Paulo Freire', 'Prédio Educação Física', 250),
            
            # Educação Física (Ponto Final L1)
            ('Prédio Educação Física', 'Portaria Fundos', 120),
            ('Prédio Educação Física', 'Ginásio Castelinho', 200),
            
            # BICT (Ponto Final L2 - mais longe)
            ('Portaria Fundos', 'BICT', 150),
            ('BICT', 'Sala de Estudo BICT', 50),
            ('BICT', 'Prédio Educação Física', 250),
            
            # LINHA L1 CAMPUS (Terminal Praia Grande → Campus → Ed. Física)
            ('Terminal Praia Grande', 'Ponto Ônibus Campus', 9500),  # ~10km
            ('Ponto Ônibus Campus', 'Prédio Educação Física', 800),  # Ponto final L1
            
            # LINHA L2 CAMPUS (Terminal Praia Grande → Campus → BICT)
            ('Terminal Praia Grande', 'BICT', 10200),  # ~10.2km direto ao BICT
            
            # Terminal Cohab (conexão alternativa)
            ('Ponto Ônibus Campus', 'Terminal Cohab', 6500),  # ~7km
            ('Terminal Cohab', 'Shopping da Ilha', 2500),
            
            # Conexões dos terminais
            ('Terminal Praia Grande', 'Centro Histórico', 3500),  # ~3.5km
            ('Terminal Praia Grande', 'Shopping da Ilha', 4000),
            ('Centro Histórico', 'Shopping da Ilha', 6000),
            
            # Pontos leste da cidade
            ('Portaria Fundos', 'Lagoa da Jansen', 3000),
            ('Lagoa da Jansen', 'Praia do Calhau', 2500),
            ('Lagoa da Jansen', 'Aeroporto', 9000),
            ('Praia do Calhau', 'Aeroporto', 8000),
            
            # Aeroporto
            ('Portaria Fundos', 'Aeroporto', 11500)
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
                print(f"     ↓ {dist}m ({dist/1000:.2f}km)")
            else:
                print(f"  {i}. {local} ✓")
        
        print(f"\nDistância total: {custo:.0f}m ({custo/1000:.2f}km)")
        print(f"Distância em linha reta: {stats['dist_euclidiana']:.0f}m")
        print(f"Eficiência: {(stats['dist_euclidiana']/custo)*100:.1f}%")
        
        # tempo estimado
        if custo < 2000:  # menos de 2km - a pé
            tempo_min = (custo/1000) / 5 * 60  # 5km/h
            print(f"Tempo estimado a pé: ~{tempo_min:.0f} min")
        else:  # mais de 2km - ônibus
            tempo_min = (custo/1000) / 30 * 60  # 30km/h média ônibus
            print(f"Tempo estimado de ônibus: ~{tempo_min:.0f} min")
        
        print("="*60 + "\n")
    
    def desenhar_mapa(self, caminho=None, salvar=True, filename=None):
        import datetime
        
        plt.figure(figsize=(20, 16))
        
        # separar nos do campus dos externos
        nos_campus = []
        nos_externos = []
        for n in self.grafo.nodes():
            x, y = self.posicoes[n]
            if abs(x) < 1500 and abs(y) < 1000:
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
                if peso >= 1000:
                    edge_labels[(u, v)] = f"{peso/1000:.1f}km"
                else:
                    edge_labels[(u, v)] = f"{peso:.0f}m"
            
            nx.draw_networkx_edge_labels(
                self.grafo,
                self.posicoes,
                edge_labels=edge_labels,
                font_size=7,
                font_color='darkred'
            )
        
        plt.title(
            'Mapa de Navegação - Campus UFMA Bacanga e São Luís/MA\n' +
            'Algoritmo A* - Linhas L1 e L2 Campus',
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
            if filename is None:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f'mapa_ufma_{timestamp}.png'
            plt.savefig(f'outputs/{filename}', dpi=300, bbox_inches='tight')
            print(f"Mapa salvo: {filename}")
        
        plt.close()
    
    def listar_locais(self):
        print("\n" + "="*60)
        print("Locais Disponíveis")
        print("="*60)
        
        categorias = {
            'Portarias': ['Portaria Principal', 'Portaria Fundos'],
            'Administrativo': ['Reitoria', 'PROEN'],
            'Centros de Ensino': ['BICT', 'CCET', 'CCH', 'CCBS', 'CCSo', 'Prédio Paulo Freire', 'Prédio Educação Física'],
            'Estudo': ['Biblioteca Central', 'Sala de Estudo BICT'],
            'Alimentação': ['Restaurante Universitário', 'Cantina Central', 'Lanchonete CCET'],
            'Esporte': ['Ginásio Castelinho', 'Quadras Esportivas', 'Praça da Cidadania'],
            'Pontos de Ônibus': ['Ponto Ônibus Campus'],
            'Terminais': ['Terminal Praia Grande', 'Terminal Cohab'],
            'Externos': ['Shopping da Ilha', 'Lagoa da Jansen', 'Praia do Calhau', 
                        'Centro Histórico', 'Aeroporto']
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
        
        print(f"{'Destino':<30} {'Distância':<25} {'Paradas'}")
        print("-" * 60)
        for dest, custo, paradas in resultados:
            if custo >= 1000:
                print(f"{dest:<30} {custo/1000:>6.2f}km ({custo:>5.0f}m)   {paradas} locais")
            else:
                print(f"{dest:<30} {custo:>6.0f}m              {paradas} locais")
        print("\n" + "="*60 + "\n")


def main():
    print("\n" + "="*60)
    print("Sistema de Navegação - Campus UFMA")
    print("Algoritmo A* - Distâncias Reais")
    print("Linhas L1 e L2 Campus")
    print("="*60 + "\n")
    
    nav = NavegacaoCampusUFMA()
    
    # listar locais
    nav.listar_locais()
    
    # exemplo 1: BICT pro Centro (deve usar L2)
    print("\nExemplo 1: BICT → Centro Histórico (via L2)")
    c1, custo1, _ = nav.buscar_caminho('BICT', 'Centro Histórico')
    nav.desenhar_mapa(c1, salvar=True, filename='exemplo1_bict_centro.png')
    
    # exemplo 2: CCET pro Centro (deve usar L1)
    print("\nExemplo 2: CCET → Centro Histórico (via L1)")
    c2, custo2, _ = nav.buscar_caminho('CCET', 'Centro Histórico')
    nav.desenhar_mapa(c2, salvar=True, filename='exemplo2_ccet_centro.png')
    
    # exemplo 3: dentro do campus
    print("\nExemplo 3: Portaria → RU")
    c3, custo3, _ = nav.buscar_caminho('Portaria Principal', 'Restaurante Universitário')
    nav.desenhar_mapa(c3, salvar=True, filename='exemplo3_campus.png')
    
    print("\nPrograma finalizado!")
    print("Mapas salvos na pasta outputs/")


if __name__ == "__main__":
    main()

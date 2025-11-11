"""
Sistema de Navegação Campus UFMA Bacanga - Algoritmo A*
Trabalho de IA - Prof. Dr. Alex Oliveira Barradas Filho

Autores:
- Yann Cristhyan Carvalho Pinheiro (2020010563)
- Jônathas Silva Oliveira (2021024590)
- João Victor Lima Azevedo (2022021127)

BICT/UFMA - 2024
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import datetime


class NavegacaoCampusUFMA:
    """Sistema de navegação interno do Campus UFMA Bacanga"""
    
    def __init__(self):
        self.grafo = nx.Graph()
        self.posicoes = {}
        self._criar_campus()
    
    def _criar_campus(self):
        # Coordenadas dos prédios do campus (em metros)
        # Origem (0,0) = Portaria Principal
        # Baseado na disposição real do Campus Bacanga
        
        locais = {
            # Entradas
            'Portaria Principal': (0, 0),
            'Portaria Fundos': (650, 50),
            
            # Prédios Administrativos
            'Reitoria': (180, 120),
            'PROEN': (220, 160),
            
            # Centros de Ensino
            'CCBS': (280, 100),
            'CCH': (350, 180),
            'CCET': (280, 280),
            'CCSo': (420, 220),
            'Prédio Paulo Freire': (450, 140),
            'Prédio Educação Física': (580, 80),
            'BICT': (700, 120),
            
            # Biblioteca e Salas de Estudo
            'Biblioteca Central': (240, 340),
            'Sala de Estudo BICT': (680, 140),
            
            # Alimentação
            'Restaurante Universitário': (400, 320),
            'Cantina Central': (300, 200),
            'Lanchonete CCET': (300, 300),
            
            # Esporte e Lazer
            'Ginásio Castelinho': (520, 360),
            'Quadras Esportivas': (480, 400),
            'Praça da Cidadania': (360, 280)
        }
        
        self.posicoes = locais
        
        for local in locais:
            self.grafo.add_node(local, pos=locais[local])
        
        # Caminhos entre os locais (distâncias aproximadas em metros)
        caminhos = [
            # Da portaria principal
            ('Portaria Principal', 'Reitoria', 200),
            ('Portaria Principal', 'CCBS', 320),
            
            # Prédios administrativos
            ('Reitoria', 'PROEN', 70),
            ('Reitoria', 'CCBS', 180),
            ('PROEN', 'Cantina Central', 90),
            
            # CCBS e arredores
            ('CCBS', 'CCH', 120),
            ('CCBS', 'Cantina Central', 120),
            
            # CCH conexões
            ('CCH', 'Cantina Central', 80),
            ('CCH', 'CCET', 150),
            ('CCH', 'CCSo', 90),
            ('CCH', 'Praça da Cidadania', 110),
            ('CCH', 'Prédio Paulo Freire', 120),
            
            # CCET e biblioteca
            ('CCET', 'Lanchonete CCET', 25),
            ('CCET', 'Biblioteca Central', 80),
            ('CCET', 'Praça da Cidadania', 80),
            ('Lanchonete CCET', 'Biblioteca Central', 60),
            
            # Biblioteca
            ('Biblioteca Central', 'Restaurante Universitário', 200),
            ('Biblioteca Central', 'Praça da Cidadania', 120),
            
            # CCSo e Paulo Freire
            ('CCSo', 'Prédio Paulo Freire', 80),
            ('CCSo', 'Praça da Cidadania', 70),
            ('CCSo', 'Restaurante Universitário', 150),
            ('Prédio Paulo Freire', 'Prédio Educação Física', 180),
            ('Prédio Paulo Freire', 'Cantina Central', 200),
            
            # Restaurante Universitário
            ('Restaurante Universitário', 'Praça da Cidadania', 80),
            ('Restaurante Universitário', 'Ginásio Castelinho', 160),
            ('Restaurante Universitário', 'Quadras Esportivas', 120),
            
            # Área esportiva
            ('Ginásio Castelinho', 'Quadras Esportivas', 90),
            ('Ginásio Castelinho', 'Portaria Fundos', 180),
            ('Quadras Esportivas', 'Portaria Fundos', 200),
            
            # Educação Física e BICT
            ('Prédio Educação Física', 'Portaria Fundos', 100),
            ('Prédio Educação Física', 'BICT', 140),
            ('Prédio Educação Física', 'Ginásio Castelinho', 120),
            ('BICT', 'Sala de Estudo BICT', 30),
            ('BICT', 'Portaria Fundos', 80),
            
            # Praça da Cidadania (ponto central)
            ('Praça da Cidadania', 'Cantina Central', 100)
        ]
        
        for origem, destino, dist in caminhos:
            self.grafo.add_edge(origem, destino, weight=dist)
    
    def calc_heuristica(self, atual, objetivo):
        # distancia euclidiana
        x1, y1 = self.posicoes[atual]
        x2, y2 = self.posicoes[objetivo]
        return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    def buscar_caminho(self, inicio, fim, mostrar_info=True):
        """Busca o melhor caminho usando A*"""
        
        if inicio not in self.grafo:
            print(f"Erro: '{inicio}' não encontrado no campus")
            return None, float('inf'), {}
        
        if fim not in self.grafo:
            print(f"Erro: '{fim}' não encontrado no campus")
            return None, float('inf'), {}
        
        try:
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
            
            stats = {
                'num_paradas': len(caminho),
                'dist_euclidiana': self.calc_heuristica(inicio, fim)
            }
            
            if mostrar_info:
                self._imprimir_rota(inicio, fim, caminho, custo, stats)
            
            return caminho, custo, stats
            
        except nx.NetworkXNoPath:
            print(f"Não há caminho entre '{inicio}' e '{fim}'")
            return None, float('inf'), {}
    
    def _imprimir_rota(self, inicio, fim, caminho, custo, stats):
        print("\n" + "="*60)
        print(f"Rota encontrada: {inicio} → {fim}")
        print("="*60)
        print(f"\nCaminho ({len(caminho)} pontos):")
        
        for i, local in enumerate(caminho, 1):
            if i < len(caminho):
                prox = caminho[i]
                dist = self.grafo[local][prox]['weight']
                print(f"  {i}. {local}")
                print(f"     ↓ {dist}m")
            else:
                print(f"  {i}. {local} ✓")
        
        print(f"\n📏 Distância total: {custo:.0f} metros")
        tempo_min = (custo / 1000) / 5 * 60  # 5 km/h caminhando
        print(f"⏱️  Tempo estimado: ~{tempo_min:.0f} minutos a pé")
        print(f"📊 Eficiência: {(stats['dist_euclidiana']/custo)*100:.1f}%")
        print("="*60 + "\n")
    
    def desenhar_mapa(self, caminho=None, salvar=True, zoom_campus=True, filename=None):
        """Gera visualização do mapa do campus"""
        
        fig, ax = plt.subplots(figsize=(16, 12))
        
        # Desenhar todas as arestas em cinza claro
        nx.draw_networkx_edges(
            self.grafo,
            self.posicoes,
            edge_color='#CCCCCC',
            width=1.5,
            alpha=0.6,
            ax=ax
        )
        
        # Destacar caminho se existir
        if caminho and len(caminho) > 1:
            # Arestas do caminho em vermelho
            edges_caminho = [(caminho[i], caminho[i+1]) for i in range(len(caminho)-1)]
            nx.draw_networkx_edges(
                self.grafo,
                self.posicoes,
                edgelist=edges_caminho,
                edge_color='#E74C3C',
                width=5,
                alpha=0.9,
                ax=ax
            )
            
            # Nós do caminho
            if len(caminho) > 2:
                # Intermediários em laranja
                nx.draw_networkx_nodes(
                    self.grafo,
                    self.posicoes,
                    nodelist=caminho[1:-1],
                    node_color='#F39C12',
                    node_size=500,
                    alpha=0.95,
                    ax=ax
                )
            
            # Início em verde
            nx.draw_networkx_nodes(
                self.grafo,
                self.posicoes,
                nodelist=[caminho[0]],
                node_color='#27AE60',
                node_size=700,
                node_shape='s',
                alpha=0.95,
                ax=ax
            )
            
            # Fim em vermelho
            nx.draw_networkx_nodes(
                self.grafo,
                self.posicoes,
                nodelist=[caminho[-1]],
                node_color='#E74C3C',
                node_size=700,
                node_shape='s',
                alpha=0.95,
                ax=ax
            )
            
            # Labels só do caminho (com fundo branco)
            labels_caminho = {n: n for n in caminho}
            nx.draw_networkx_labels(
                self.grafo,
                self.posicoes,
                labels=labels_caminho,
                font_size=9,
                font_weight='bold',
                font_color='#2C3E50',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='none', alpha=0.8),
                ax=ax
            )
            
            # Distâncias nas arestas do caminho
            edge_labels = {}
            for i in range(len(caminho)-1):
                u, v = caminho[i], caminho[i+1]
                peso = self.grafo[u][v]['weight']
                edge_labels[(u, v)] = f"{peso:.0f}m"
            
            nx.draw_networkx_edge_labels(
                self.grafo,
                self.posicoes,
                edge_labels=edge_labels,
                font_size=8,
                font_color='#E74C3C',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.7),
                ax=ax
            )
        
        # Desenhar outros nós em azul claro
        outros_nos = [n for n in self.grafo.nodes() if not caminho or n not in caminho]
        if outros_nos:
            nx.draw_networkx_nodes(
                self.grafo,
                self.posicoes,
                nodelist=outros_nos,
                node_color='#3498DB',
                node_size=350,
                alpha=0.7,
                ax=ax
            )
        
        # Título
        titulo = 'Mapa de Navegação - Campus UFMA Bacanga\nAlgoritmo A*'
        if caminho:
            titulo += f'\nRota: {caminho[0]} → {caminho[-1]}'
        
        ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
        
        # Legenda
        from matplotlib.patches import Patch
        legend_elements = [Patch(facecolor='#3498DB', label='Locais do Campus')]
        if caminho:
            legend_elements.extend([
                Patch(facecolor='#27AE60', label='Início'),
                Patch(facecolor='#E74C3C', label='Destino'),
                Patch(facecolor='#F39C12', label='Caminho')
            ])
        ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
        
        ax.axis('off')
        ax.set_aspect('equal')
        
        # Zoom no campus se solicitado
        if zoom_campus:
            margin = 50
            xs = [self.posicoes[n][0] for n in self.grafo.nodes()]
            ys = [self.posicoes[n][1] for n in self.grafo.nodes()]
            ax.set_xlim(min(xs) - margin, max(xs) + margin)
            ax.set_ylim(min(ys) - margin, max(ys) + margin)
        
        plt.tight_layout()
        
        if salvar:
            if filename is None:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f'mapa_campus_{timestamp}.png'
            
            filepath = f'outputs/{filename}'
            plt.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white')
            print(f"✅ Mapa salvo: {filename}")
        
        plt.close()
    
    def listar_locais(self):
        """Lista todos os locais disponíveis no campus"""
        print("\n" + "="*60)
        print("📍 LOCAIS DO CAMPUS UFMA BACANGA")
        print("="*60)
        
        categorias = {
            'Portarias': ['Portaria Principal', 'Portaria Fundos'],
            'Administrativo': ['Reitoria', 'PROEN'],
            'Centros de Ensino': ['BICT', 'CCET', 'CCH', 'CCBS', 'CCSo', 
                                  'Prédio Paulo Freire', 'Prédio Educação Física'],
            'Estudo': ['Biblioteca Central', 'Sala de Estudo BICT'],
            'Alimentação': ['Restaurante Universitário', 'Cantina Central', 'Lanchonete CCET'],
            'Esporte e Lazer': ['Ginásio Castelinho', 'Quadras Esportivas', 'Praça da Cidadania']
        }
        
        for cat, locs in categorias.items():
            print(f"\n{cat}:")
            for loc in locs:
                print(f"  • {loc}")
        
        print("\n" + "="*60 + "\n")
    
    def comparar_rotas(self, origem, destinos):
        """Compara distâncias de uma origem para vários destinos"""
        print("\n" + "="*60)
        print(f"📊 Comparando rotas partindo de: {origem}")
        print("="*60 + "\n")
        
        resultados = []
        for dest in destinos:
            caminho, custo, _ = self.buscar_caminho(origem, dest, mostrar_info=False)
            if caminho:
                resultados.append((dest, custo, len(caminho)))
        
        resultados.sort(key=lambda x: x[1])
        
        print(f"{'Destino':<35} {'Distância':<15} {'Paradas'}")
        print("-" * 60)
        for dest, custo, paradas in resultados:
            print(f"{dest:<35} {custo:>6.0f}m    {paradas:>3} pontos")
        
        print("\n" + "="*60 + "\n")


def main():
    """Exemplos de uso do sistema"""
    print("\n" + "="*60)
    print("🎓 Sistema de Navegação - Campus UFMA Bacanga")
    print("   Algoritmo A* - Busca Informada")
    print("="*60 + "\n")
    
    nav = NavegacaoCampusUFMA()
    
    # Listar locais
    nav.listar_locais()
    
    # Exemplo 1: Rota comum de estudante
    print("📚 Exemplo 1: Chegando para aula")
    c1, custo1, _ = nav.buscar_caminho('Portaria Principal', 'BICT')
    nav.desenhar_mapa(c1, filename='exemplo1_portaria_bict.png')
    
    # Exemplo 2: Indo almoçar
    print("\n🍽️ Exemplo 2: Saindo da aula para o RU")
    c2, custo2, _ = nav.buscar_caminho('CCET', 'Restaurante Universitário')
    nav.desenhar_mapa(c2, filename='exemplo2_ccet_ru.png')
    
    # Exemplo 3: Estudar na biblioteca
    print("\n📖 Exemplo 3: Biblioteca após o almoço")
    c3, custo3, _ = nav.buscar_caminho('Restaurante Universitário', 'Biblioteca Central')
    nav.desenhar_mapa(c3, filename='exemplo3_ru_biblioteca.png')
    
    # Exemplo 4: Comparação
    print("\n📊 Exemplo 4: Comparando distâncias do BICT")
    nav.comparar_rotas('BICT', [
        'Biblioteca Central',
        'Restaurante Universitário',
        'CCET',
        'Ginásio Castelinho',
        'Portaria Principal'
    ])
    
    print("\n✅ Exemplos concluídos!")
    print("📁 Mapas salvos na pasta outputs/\n")


if __name__ == "__main__":
    main()

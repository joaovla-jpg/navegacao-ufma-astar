"""
Suite de Testes - Sistema de Navegação Campus UFMA
Valida o funcionamento do algoritmo A*
"""

from navegacao_ufma import NavegacaoCampusUFMA
import sys


def teste_grafo():
    """Testa criação do grafo"""
    print("\n🧪 TESTE 1: Criação do Grafo")
    print("-" * 60)
    
    try:
        nav = NavegacaoCampusUFMA()
        
        num_nos = nav.grafo.number_of_nodes()
        num_arestas = nav.grafo.number_of_edges()
        
        assert num_nos == 19, f"Esperado 19 nós, encontrado {num_nos}"
        assert num_arestas > 0, "Nenhuma aresta encontrada"
        
        print(f"✅ Grafo criado com sucesso!")
        print(f"   Nós: {num_nos}")
        print(f"   Arestas: {num_arestas}")
        return True
    except Exception as e:
        print(f"❌ Falha: {e}")
        return False


def teste_heuristica():
    """Testa função heurística"""
    print("\n🧪 TESTE 2: Heurística")
    print("-" * 60)
    
    try:
        nav = NavegacaoCampusUFMA()
        
        # Distância para si mesmo = 0
        dist = nav.calc_heuristica('BICT', 'BICT')
        assert dist == 0, f"Distância para si mesmo deveria ser 0"
        
        # Distância deve ser positiva
        dist = nav.calc_heuristica('BICT', 'CCET')
        assert dist > 0, f"Distância deve ser positiva"
        
        # Simetria
        dist1 = nav.calc_heuristica('BICT', 'CCET')
        dist2 = nav.calc_heuristica('CCET', 'BICT')
        assert abs(dist1 - dist2) < 0.01, "Heurística deve ser simétrica"
        
        print(f"✅ Heurística funcionando!")
        return True
    except Exception as e:
        print(f"❌ Falha: {e}")
        return False


def teste_a_estrela():
    """Testa algoritmo A*"""
    print("\n🧪 TESTE 3: Algoritmo A*")
    print("-" * 60)
    
    try:
        nav = NavegacaoCampusUFMA()
        
        # Caminho para si mesmo
        caminho, custo, _ = nav.buscar_caminho('BICT', 'BICT', mostrar_info=False)
        assert len(caminho) == 1, "Caminho para si mesmo deve ter 1 nó"
        assert custo == 0, "Custo para si mesmo deve ser 0"
        
        # Caminho válido
        caminho, custo, _ = nav.buscar_caminho('Portaria Principal', 'BICT', mostrar_info=False)
        assert caminho is not None, "Deve encontrar caminho"
        assert len(caminho) >= 2, "Caminho deve ter pelo menos 2 nós"
        assert custo > 0, "Custo deve ser positivo"
        
        print(f"✅ A* funcionando!")
        print(f"   Exemplo: Portaria → BICT = {custo:.0f}m")
        return True
    except Exception as e:
        print(f"❌ Falha: {e}")
        return False


def teste_rotas_importantes():
    """Testa rotas comuns do campus"""
    print("\n🧪 TESTE 4: Rotas Importantes")
    print("-" * 60)
    
    try:
        nav = NavegacaoCampusUFMA()
        
        rotas = [
            ('Portaria Principal', 'BICT', 900),
            ('CCET', 'Restaurante Universitário', 400),
            ('BICT', 'Biblioteca Central', 900),
            ('Reitoria', 'Ginásio Castelinho', 900)
        ]
        
        for inicio, fim, max_dist in rotas:
            caminho, custo, _ = nav.buscar_caminho(inicio, fim, mostrar_info=False)
            assert caminho is not None, f"Não encontrou {inicio} → {fim}"
            assert custo < max_dist, f"Distância muito alta: {custo}m"
            print(f"   ✓ {inicio} → {fim}: {custo:.0f}m")
        
        print(f"\n✅ Rotas importantes validadas!")
        return True
    except Exception as e:
        print(f"❌ Falha: {e}")
        return False


def teste_erro():
    """Testa tratamento de erros"""
    print("\n🧪 TESTE 5: Tratamento de Erros")
    print("-" * 60)
    
    try:
        nav = NavegacaoCampusUFMA()
        
        # Local inexistente
        caminho, custo, _ = nav.buscar_caminho('Local Falso', 'BICT', mostrar_info=False)
        assert caminho is None, "Deve retornar None"
        assert custo == float('inf'), "Custo deve ser infinito"
        
        print(f"✅ Erros tratados corretamente!")
        return True
    except Exception as e:
        print(f"❌ Falha: {e}")
        return False


def executar_testes():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("🧪 SUITE DE TESTES - NAVEGAÇÃO CAMPUS UFMA")
    print("="*60)
    
    testes = [
        teste_grafo,
        teste_heuristica,
        teste_a_estrela,
        teste_rotas_importantes,
        teste_erro
    ]
    
    resultados = [teste() for teste in testes]
    
    print("\n" + "="*60)
    print("📊 RESUMO")
    print("="*60)
    
    total = len(resultados)
    passou = sum(resultados)
    
    print(f"\nTotal: {total}")
    print(f"✅ Passou: {passou}")
    print(f"❌ Falhou: {total - passou}")
    print(f"Taxa de sucesso: {(passou/total)*100:.0f}%")
    
    if passou == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!\n")
        return 0
    else:
        print(f"\n⚠️ {total - passou} teste(s) falharam.\n")
        return 1


if __name__ == "__main__":
    sys.exit(executar_testes())

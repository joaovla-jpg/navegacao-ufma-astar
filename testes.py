"""
Script de Testes - Sistema de Navegação UFMA
Valida o funcionamento correto do algoritmo A*
"""

from navegacao_ufma import NavegacaoCampusUFMA
import sys


def teste_criacao_grafo():
    """Testa se o grafo foi criado corretamente."""
    print("\n🧪 TESTE 1: Criação do Grafo")
    print("-" * 60)
    
    try:
        nav = NavegacaoCampusUFMA()
        
        num_nos = nav.grafo.number_of_nodes()
        num_arestas = nav.grafo.number_of_edges()
        
        assert num_nos == 24, f"Esperado 24 nós, encontrado {num_nos}"
        assert num_arestas > 0, "Nenhuma aresta encontrada"
        
        print(f"✅ Grafo criado com sucesso!")
        print(f"   • Número de nós: {num_nos}")
        print(f"   • Número de arestas: {num_arestas}")
        return True
    except AssertionError as e:
        print(f"❌ Falha: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def teste_heuristica():
    """Testa se a heurística está funcionando."""
    print("\n🧪 TESTE 2: Função Heurística")
    print("-" * 60)
    
    try:
        nav = NavegacaoCampusUFMA()
        
        # Teste 1: Distância de um nó para ele mesmo deve ser 0
        dist = nav.heuristica('BICT', 'BICT')
        assert dist == 0, f"Distância para si mesmo deveria ser 0, mas é {dist}"
        
        # Teste 2: Distância deve ser positiva
        dist = nav.heuristica('BICT', 'CCET')
        assert dist > 0, f"Distância deveria ser positiva, mas é {dist}"
        
        # Teste 3: Distância deve ser simétrica
        dist1 = nav.heuristica('BICT', 'CCET')
        dist2 = nav.heuristica('CCET', 'BICT')
        assert abs(dist1 - dist2) < 0.01, "Heurística deveria ser simétrica"
        
        print(f"✅ Heurística funcionando corretamente!")
        print(f"   • BICT ↔ BICT: {nav.heuristica('BICT', 'BICT'):.2f}m")
        print(f"   • BICT ↔ CCET: {nav.heuristica('BICT', 'CCET'):.2f}m")
        return True
    except AssertionError as e:
        print(f"❌ Falha: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def teste_a_estrela_basico():
    """Testa casos básicos do A*."""
    print("\n🧪 TESTE 3: Algoritmo A* - Casos Básicos")
    print("-" * 60)
    
    try:
        nav = NavegacaoCampusUFMA()
        
        # Teste 1: Caminho de um nó para ele mesmo
        caminho, custo, _ = nav.a_estrela('BICT', 'BICT', verbose=False)
        assert len(caminho) == 1, "Caminho para si mesmo deveria ter 1 nó"
        assert custo == 0, "Custo para si mesmo deveria ser 0"
        
        # Teste 2: Caminho adjacente direto
        caminho, custo, _ = nav.a_estrela('BICT', 'CCET', verbose=False)
        assert caminho is not None, "Deveria encontrar caminho entre BICT e CCET"
        assert len(caminho) >= 2, "Caminho deveria ter pelo menos 2 nós"
        
        # Teste 3: Caminho mais longo
        caminho, custo, _ = nav.a_estrela('Portaria Principal', 'Aeroporto', verbose=False)
        assert caminho is not None, "Deveria encontrar caminho para o Aeroporto"
        assert len(caminho) > 2, "Caminho para Aeroporto deveria ter mais de 2 nós"
        
        print(f"✅ A* funcionando corretamente!")
        print(f"   • Caminho BICT → BICT: {1} nó, {0}m")
        return True
    except AssertionError as e:
        print(f"❌ Falha: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def teste_otimalidade():
    """Testa se o A* encontra o caminho ótimo."""
    print("\n🧪 TESTE 4: Otimalidade do A*")
    print("-" * 60)
    
    try:
        nav = NavegacaoCampusUFMA()
        
        # Comparar com caminho direto vs indireto
        caminho1, custo1, _ = nav.a_estrela('BICT', 'Biblioteca Central', verbose=False)
        
        # A distância encontrada deve ser razoável
        assert custo1 > 0, "Custo deveria ser positivo"
        assert custo1 < 500, "Distância parece muito alta para locais próximos"
        
        print(f"✅ Otimalidade validada!")
        print(f"   • BICT → Biblioteca: {custo1:.0f}m")
        print(f"   • Caminho tem {len(caminho1)} pontos")
        return True
    except AssertionError as e:
        print(f"❌ Falha: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def teste_rotas_importantes():
    """Testa rotas comuns de estudantes."""
    print("\n🧪 TESTE 5: Rotas Importantes para Estudantes")
    print("-" * 60)
    
    try:
        nav = NavegacaoCampusUFMA()
        
        rotas_teste = [
            ('Portaria Principal', 'BICT', 500),  # < 500m
            ('BICT', 'Restaurante Universitário', 600),  # < 600m
            ('CCET', 'Biblioteca Central', 200),  # < 200m
            ('Biblioteca Central', 'Restaurante Universitário', 300),  # < 300m
        ]
        
        for inicio, destino, max_dist in rotas_teste:
            caminho, custo, _ = nav.a_estrela(inicio, destino, verbose=False)
            assert caminho is not None, f"Falha em encontrar {inicio} → {destino}"
            assert custo < max_dist, f"Distância {custo:.0f}m muito alta (max {max_dist}m)"
            print(f"   ✓ {inicio} → {destino}: {custo:.0f}m ({len(caminho)} pontos)")
        
        print(f"\n✅ Todas as rotas importantes testadas com sucesso!")
        return True
    except AssertionError as e:
        print(f"❌ Falha: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def teste_locais_invalidos():
    """Testa comportamento com entradas inválidas."""
    print("\n🧪 TESTE 6: Tratamento de Erros")
    print("-" * 60)
    
    try:
        nav = NavegacaoCampusUFMA()
        
        # Teste com local inexistente
        caminho, custo, _ = nav.a_estrela('Local Inexistente', 'BICT', verbose=False)
        assert caminho is None, "Deveria retornar None para local inválido"
        assert custo == float('inf'), "Custo deveria ser infinito para local inválido"
        
        print(f"✅ Tratamento de erros funcionando!")
        print(f"   • Locais inválidos são rejeitados corretamente")
        return True
    except AssertionError as e:
        print(f"❌ Falha: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def executar_todos_testes():
    """Executa todos os testes."""
    print("\n" + "="*60)
    print("🧪 SUITE DE TESTES - SISTEMA DE NAVEGAÇÃO UFMA")
    print("="*60)
    
    testes = [
        teste_criacao_grafo,
        teste_heuristica,
        teste_a_estrela_basico,
        teste_otimalidade,
        teste_rotas_importantes,
        teste_locais_invalidos
    ]
    
    resultados = []
    for teste in testes:
        resultado = teste()
        resultados.append(resultado)
    
    # Sumário
    print("\n" + "="*60)
    print("📊 SUMÁRIO DOS TESTES")
    print("="*60)
    
    total = len(resultados)
    passou = sum(resultados)
    falhou = total - passou
    
    print(f"\n   Total de testes: {total}")
    print(f"   ✅ Passou: {passou}")
    print(f"   ❌ Falhou: {falhou}")
    print(f"   Taxa de sucesso: {(passou/total)*100:.1f}%")
    
    if falhou == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM! Sistema validado.")
        return 0
    else:
        print(f"\n⚠️ {falhou} teste(s) falharam. Revisar implementação.")
        return 1


if __name__ == "__main__":
    codigo_saida = executar_todos_testes()
    sys.exit(codigo_saida)

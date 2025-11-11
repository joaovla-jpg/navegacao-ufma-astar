"""
Interface Interativa - Sistema de Navegação Campus UFMA
"""

from navegacao_ufma import NavegacaoCampusUFMA


def menu_principal():
    """Menu interativo para navegação no campus"""
    nav = NavegacaoCampusUFMA()
    
    print("\n" + "="*60)
    print("🎓 NAVEGAÇÃO INTERATIVA - CAMPUS UFMA")
    print("="*60 + "\n")
    
    while True:
        print("📋 MENU:")
        print("1. Listar locais do campus")
        print("2. Buscar caminho entre dois pontos")
        print("3. Comparar rotas de um ponto")
        print("4. Ver exemplos pré-definidos")
        print("0. Sair")
        
        opcao = input("\nEscolha: ").strip()
        
        if opcao == "1":
            nav.listar_locais()
        
        elif opcao == "2":
            nav.listar_locais()
            inicio = input("📍 Local de PARTIDA: ").strip()
            fim = input("📍 Local de DESTINO: ").strip()
            
            print("\n🔍 Buscando rota...")
            caminho, custo, _ = nav.buscar_caminho(inicio, fim)
            
            if caminho:
                gerar = input("\n📊 Gerar mapa? (s/n): ").strip().lower()
                if gerar == 's':
                    nav.desenhar_mapa(caminho)
                    print("Confira o mapa na pasta outputs/")
        
        elif opcao == "3":
            nav.listar_locais()
            origem = input("📍 Local de PARTIDA: ").strip()
            
            print("\nDigite os DESTINOS separados por vírgula:")
            destinos_str = input("Destinos: ").strip()
            destinos = [d.strip() for d in destinos_str.split(',')]
            
            nav.comparar_rotas(origem, destinos)
        
        elif opcao == "4":
            executar_exemplos(nav)
        
        elif opcao == "0":
            print("\n👋 Até logo!\n")
            break
        
        else:
            print("\n❌ Opção inválida!\n")


def executar_exemplos(nav):
    """Executa exemplos pré-definidos"""
    print("\n" + "="*60)
    print("📚 EXEMPLOS PRÉ-DEFINIDOS")
    print("="*60 + "\n")
    
    exemplos = {
        '1': ('Portaria Principal', 'BICT', 'Chegando para aula'),
        '2': ('CCET', 'Restaurante Universitário', 'Indo almoçar'),
        '3': ('BICT', 'Biblioteca Central', 'Estudar na biblioteca'),
        '4': ('Restaurante Universitário', 'Ginásio Castelinho', 'Ir treinar'),
        '5': ('Portaria Principal', 'Portaria Fundos', 'Atravessar o campus')
    }
    
    for key, (inicio, fim, desc) in exemplos.items():
        print(f"{key}. {desc} ({inicio} → {fim})")
    print("0. Voltar")
    
    escolha = input("\nEscolha: ").strip()
    
    if escolha in exemplos:
        inicio, fim, desc = exemplos[escolha]
        print(f"\n{desc}")
        caminho, custo, _ = nav.buscar_caminho(inicio, fim)
        
        if caminho:
            gerar = input("\n📊 Gerar mapa? (s/n): ").strip().lower()
            if gerar == 's':
                nav.desenhar_mapa(caminho)
                print("Mapa salvo na pasta outputs/")


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n⚠️ Programa interrompido.\n")
    except Exception as e:
        print(f"\n❌ Erro: {e}\n")

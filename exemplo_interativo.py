"""
Exemplo Interativo - Navegação Campus UFMA
Execute este arquivo para testar diferentes rotas de forma interativa!
"""

from navegacao_ufma import NavegacaoCampusUFMA


def menu_interativo():
    """Interface interativa para testar o sistema de navegação."""
    nav = NavegacaoCampusUFMA()
    
    print("\n" + "="*70)
    print("🎓 SISTEMA INTERATIVO DE NAVEGAÇÃO - CAMPUS UFMA")
    print("="*70 + "\n")
    
    while True:
        print("\n📋 MENU PRINCIPAL:")
        print("1. Listar todos os locais disponíveis")
        print("2. Encontrar caminho entre dois locais")
        print("3. Comparar rotas a partir de um local")
        print("4. Exemplos pré-definidos")
        print("5. Visualizar mapa completo")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            nav.listar_locais()
        
        elif opcao == "2":
            print("\n" + "-"*70)
            nav.listar_locais()
            inicio = input("Digite o local de PARTIDA: ").strip()
            destino = input("Digite o local de DESTINO: ").strip()
            
            print("\n🔍 Buscando rota...")
            caminho, custo, stats = nav.a_estrela(inicio, destino)
            
            if caminho:
                print("\n📊 Deseja visualizar o mapa desta rota? (s/n): ", end="")
                if input().strip().lower() == 's':
                    nav.visualizar_mapa(caminho, salvar=False)
        
        elif opcao == "3":
            print("\n" + "-"*70)
            nav.listar_locais()
            inicio = input("Digite o local de PARTIDA: ").strip()
            
            print("\nDigite os DESTINOS para comparar (separados por vírgula):")
            print("Exemplo: CCET, Biblioteca Central, RU")
            destinos_str = input("Destinos: ").strip()
            destinos = [d.strip() for d in destinos_str.split(',')]
            
            nav.comparar_rotas(inicio, destinos)
        
        elif opcao == "4":
            exemplos_predefinidos(nav)
        
        elif opcao == "5":
            print("\n🗺️ Gerando visualização do mapa completo...")
            nav.visualizar_mapa(salvar=False)
        
        elif opcao == "0":
            print("\n👋 Obrigado por usar o sistema! Até logo!\n")
            break
        
        else:
            print("\n❌ Opção inválida! Tente novamente.")


def exemplos_predefinidos(nav):
    """Mostra exemplos pré-definidos de uso."""
    print("\n" + "="*70)
    print("📚 EXEMPLOS PRÉ-DEFINIDOS")
    print("="*70)
    
    exemplos = {
        "1": {
            "titulo": "Primeira aula do dia",
            "inicio": "Portaria Principal",
            "destino": "BICT",
            "descricao": "Chegando na UFMA pela manhã"
        },
        "2": {
            "titulo": "Hora do almoço",
            "inicio": "CCET",
            "destino": "Restaurante Universitário",
            "descricao": "Saindo da aula para almoçar no RU"
        },
        "3": {
            "titulo": "Estudar para a prova",
            "inicio": "BICT",
            "destino": "Biblioteca Central",
            "descricao": "Indo estudar na biblioteca"
        },
        "4": {
            "titulo": "Atividade física",
            "inicio": "Restaurante Universitário",
            "destino": "Ginásio Castelinho",
            "descricao": "Após o almoço, indo jogar basquete"
        },
        "5": {
            "titulo": "Final de semana na praia",
            "inicio": "BICT",
            "destino": "Praia do Calhau",
            "descricao": "Saindo da UFMA para curtir a praia"
        },
        "6": {
            "titulo": "Viagem de férias",
            "inicio": "Portaria Principal",
            "destino": "Aeroporto",
            "descricao": "Indo pegar um voo nas férias"
        }
    }
    
    print("\nEscolha um exemplo:")
    for key, ex in exemplos.items():
        print(f"{key}. {ex['titulo']} ({ex['inicio']} → {ex['destino']})")
    print("0. Voltar ao menu principal")
    
    escolha = input("\nOpção: ").strip()
    
    if escolha in exemplos:
        ex = exemplos[escolha]
        print(f"\n📖 {ex['titulo']}")
        print(f"💬 {ex['descricao']}")
        print(f"🚶 {ex['inicio']} → {ex['destino']}\n")
        
        caminho, custo, stats = nav.a_estrela(ex['inicio'], ex['destino'])
        
        if caminho:
            print("\n📊 Deseja visualizar o mapa? (s/n): ", end="")
            if input().strip().lower() == 's':
                nav.visualizar_mapa(caminho, salvar=False)
    elif escolha != "0":
        print("\n❌ Opção inválida!")


if __name__ == "__main__":
    try:
        menu_interativo()
    except KeyboardInterrupt:
        print("\n\n⚠️ Programa interrompido pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro: {e}")

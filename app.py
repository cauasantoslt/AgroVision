# ÁREA DO MILHO + APLICAÇÃO DE FUNGICIDA
# Cauã da Silva, Fabio Baldo, Giovanna Gomes, Julia Gutierres e Roberto Alvares
# 2025 - Versão Refatorada pela Equipe FarmTech
import csv

# --- DADOS E CONSTANTES DO SISTEMA ---

INSUMOS_POR_CULTURA = {
    'Milho': {
        'nome_insumo': 'Fungicida',
        'dose_l_ha': 1.5
    },
    'Trigo': {
        'nome_insumo': 'Herbicida',
        'dose_l_ha': 2.0
    }
}
METROS_QUADRADOS_POR_HECTARE = 10000

# Vetor principal para guardar os dados dos talhões.
talhoes = []


# --- FUNÇÕES DO SISTEMA ---

def exibir_menu():
    """Exibe o menu de opções para o usuário."""
    print("\n--- FarmTech Solutions: Gestão de Talhões ---")
    print("1. Adicionar novo talhão (Milho ou Trigo)")
    print("2. Listar talhões e cálculo de insumos")
    print("3. Atualizar dados de um talhão")
    print("4. Deletar um talhão")
    print("5. Exportar dados para CSV")
    print("6. Sair do programa")
    print("-------------------------------------------")

def adicionar_talhao():
    """Função única para adicionar dados de um novo talhão (Milho ou Trigo)."""
    print("\n==> Adicionando Novo Talhão")
    
    while True:
        cultura = input("Digite a cultura (Trigo ou Milho): ").strip().capitalize()
        if cultura in INSUMOS_POR_CULTURA:
            break
        else:
            print(f"Cultura inválida! Por favor, escolha uma das opções: {list(INSUMOS_POR_CULTURA.keys())}")

    try:
        largura = float(input(f"Digite a largura do terreno de {cultura} (em metros): "))
        comprimento = float(input(f"Digite o comprimento do terreno de {cultura} (em metros): "))
    except ValueError:
        print("Erro: Largura e comprimento devem ser números. Operação cancelada.")
        return

    area = largura * comprimento
    
    novo_talhao = {
        'cultura': cultura,
        'largura_m': largura,
        'comprimento_m': comprimento,
        'area_m2': area
    }
    
    talhoes.append(novo_talhao)
    print(f"Talhão de {cultura} com {area:.2f} m² adicionado com sucesso!")

def listar_talhoes():
    """Exibe todos os talhões cadastrados e calcula o insumo necessário para cada um."""
    print("\n==> Lista de Talhões Cadastrados")
    
    if not talhoes:
        print("Nenhum talhão cadastrado ainda.")
        return

    for i, talhao in enumerate(talhoes):
        cultura = talhao['cultura']
        dados_cultura = INSUMOS_POR_CULTURA[cultura]
        
        area_ha = talhao['area_m2'] / METROS_QUADRADOS_POR_HECTARE
        insumo_necessario_l = area_ha * dados_cultura['dose_l_ha']
        
        print(f"\n--- Talhão ID: {i} ---")
        print(f"  Cultura: {talhao['cultura']}")
        print(f"  Dimensões: {talhao['largura_m']:.2f}m x {talhao['comprimento_m']:.2f}m")
        print(f"  Área Total: {talhao['area_m2']:.2f} m² ({area_ha:.4f} ha)")
        print(f"  Insumo a aplicar: {dados_cultura['nome_insumo']}")
        print(f"  Quantidade necessária: {insumo_necessario_l:.2f} Litros")

def atualizar_talhao():
    """Atualiza as informações de um talhão existente no vetor."""
    print("\n==> Atualizar Talhão")
    listar_talhoes()
    
    if not talhoes:
        return

    try:
        id_para_atualizar = int(input("\nDigite o ID do talhão que deseja atualizar: "))
        
        if 0 <= id_para_atualizar < len(talhoes):
            print(f"Atualizando dados do Talhão ID: {id_para_atualizar}")
            
            nova_largura = float(input("Digite a NOVA largura (em metros): "))
            novo_comprimento = float(input("Digite o NOVO comprimento (em metros): "))
            
            talhao_selecionado = talhoes[id_para_atualizar]
            talhao_selecionado['largura_m'] = nova_largura
            talhao_selecionado['comprimento_m'] = novo_comprimento
            talhao_selecionado['area_m2'] = nova_largura * novo_comprimento
            
            print("Talhão atualizado com sucesso!")
        else:
            print("ID inválido!")
            
    except ValueError:
        print("Erro: O ID, a largura e o comprimento devem ser números.")

def deletar_talhao():
    """Remove um talhão específico do vetor."""
    print("\n==> Deletar Talhão")
    listar_talhoes()
    
    if not talhoes:
        return

    try:
        id_para_deletar = int(input("\nDigite o ID do talhão que deseja deletar: "))

        if 0 <= id_para_deletar < len(talhoes):
            cultura_deletada = talhoes[id_para_deletar]['cultura']
            confirmacao = input(f"Tem certeza que deseja deletar o Talhão de {cultura_deletada} (ID {id_para_deletar})? (s/n): ").strip().lower()
            if confirmacao == 's':
                talhoes.pop(id_para_deletar)
                print("Talhão deletado com sucesso!")
            else:
                print("Operação cancelada.")
        else:
            print("ID inválido!")
            
    except ValueError:
        print("Erro: O ID deve ser um número.")

def exportar_para_csv():
    """Salva os dados dos talhões em um arquivo CSV para ser usado por outros sistemas."""
    print("\n==> Exportando dados para CSV")
    
    if not talhoes:
        print("Nenhum talhão para exportar. Adicione alguns dados primeiro.")
        return

    nome_arquivo = "dados_fazenda.csv"
    
    try:
        with open(nome_arquivo, 'w', newline='\n', encoding='utf-8') as arquivo_csv:
            headers = ['ID', 'Cultura', 'Dimensoes', 'Area_m2', 'Area_ha', 'Insumo', 'Quantidade_L']
            writer = csv.DictWriter(arquivo_csv, fieldnames=headers)
            
            writer.writeheader()
            
            for i, talhao in enumerate(talhoes):
                cultura = talhao['cultura']
                dados_cultura = INSUMOS_POR_CULTURA[cultura]
                area_ha = talhao['area_m2'] / METROS_QUADRADOS_POR_HECTARE
                insumo_l = area_ha * dados_cultura['dose_l_ha']
                
                writer.writerow({
                    'ID': i,
                    'Cultura': cultura,
                    'Dimensoes': f"{talhao['largura_m']:.0f}x{talhao['comprimento_m']:.0f}",
                    'Area_m2': round(talhao['area_m2'], 2),
                    'Area_ha': round(area_ha, 4),
                    'Insumo': dados_cultura['nome_insumo'],
                    'Quantidade_L': round(insumo_l, 2)
                })
        
        print(f"Dados exportados com sucesso para o arquivo '{nome_arquivo}'!")

    except IOError:
        print(f"Erro: Não foi possível escrever no arquivo '{nome_arquivo}'.")



def main():
    """Função principal que executa o loop do menu."""
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            adicionar_talhao()
        elif opcao == '2':
            listar_talhoes()
        elif opcao == '3':
            atualizar_talhao()
        elif opcao == '4':
            deletar_talhao()
        elif opcao == '5':
            exportar_para_csv()
        elif opcao == '6':
            print("\nEncerrando o programa... FarmTech Solutions agradece!")
            break
        else:
            print("\nOpção inválida! Por favor, tente novamente.")

# Executa o programa
main()


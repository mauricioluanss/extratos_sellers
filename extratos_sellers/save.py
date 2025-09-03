import pandas as pd

from .config import COLUNAS_CRIADAS, DIR_OUTPUT, ARQ_TEMP_CONTASARECEBER_FINAL


def salva_extratos_por_seller() -> None:
    """
    Lê o DataFrame final, agrupa por seller e salva extratos individuais em Excel.

    Esta função representa a etapa final do processo de geração de relatórios.
    Ela carrega o DataFrame processado a partir do arquivo temporário, garante
    que o diretório de saída     exista e, em seguida, itera sobre cada seller
    para exportar um arquivo .xlsx individual com uma linha de total adicionada.
    """
    try:
        df_contas_a_receber = pd.read_excel(ARQ_TEMP_CONTASARECEBER_FINAL)
        DIR_OUTPUT.mkdir(parents=True, exist_ok=True)

        grupos_de_sellers = df_contas_a_receber.groupby(COLUNAS_CRIADAS["COL_SELLERS"])
        for seller, planilha_seller in grupos_de_sellers:
            print(f"Processando relatório para o seller: '{seller}.xlsx')")
            nome_arquivo = f"{seller}.xlsx"
            caminho_completo_do_arquivo = DIR_OUTPUT / nome_arquivo

            soma_dos_repasses = planilha_seller[
                COLUNAS_CRIADAS["COL_TOTAL_REPASSE"]
            ].sum()
            linha_total = pd.DataFrame(
                [
                    {
                        planilha_seller.columns[0]: "TOTAL",
                        COLUNAS_CRIADAS["COL_TOTAL_REPASSE"]: soma_dos_repasses,
                    }
                ]
            )
            planilha_com_total = pd.concat(
                [planilha_seller, linha_total], ignore_index=True
            )
            planilha_com_total.to_excel(caminho_completo_do_arquivo, index=False)
        print("Processo concluído.")
    except FileNotFoundError as e:
        print(f"Dataframe não encontrado. Erro: {e}")
        exit()
    except Exception as e:
        print(f"Erro: {e}")
        exit()

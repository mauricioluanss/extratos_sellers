from pathlib import Path

# diretorios
RAIZ = Path(__file__).parent.parent  # extratos-sellers/
DIR_DATA = RAIZ / "data"
DIR_SCRIPTS = RAIZ / "extratos_sellers"
DIR_OUTPUT = DIR_DATA / "output"
DIR_TEMPFILES = DIR_DATA / "temp_files"

# Mapemento dos arquivos
# arquivos fonte
ARQ_CONTASARECEBER = next((DIR_DATA / "input").glob("*.xls"))
ARQ_COMISSOES = DIR_DATA / "comissoes.xlsx"
# arquivos temporarios
ARQ_TEMP_CONTASARECEBER = DIR_TEMPFILES / "temp_contas_a_receber.xlsx"
ARQ_TEMP_CONTASARECEBER_FINAL = DIR_TEMPFILES / "temp_contas_a_receber_final.xlsx"
ARQ_TEMP_COMISSOES = DIR_TEMPFILES / "temp_comissoes.xlsx"

# mapeamento de colunas
COLUNAS = {
    "COL_IDENTIFICADOR_CLIENTE": "Identificador do cliente",
    "COL_NOME_CLIENTE": "Nome do cliente",
    "COL_DATA_VENCIMENTO": "Data de vencimento",
    "COL_VALOR_ORIGINAL_PARCELA": "Valor original da parcela (R$)",
    "COL_VALOR_RECEBIDO_PARCELA": "Valor recebido da parcela (R$)",
    "COL_DATA_ULTIMO_PAGAMENTO": "Data do último pagamento",
}

COLUNAS_CRIADAS = {
    "COL_NOME_RESSELLER": "nome_resseller",
    "COL_SELLERS": "SELLERS",
    "COL_RESSELLERS": "RESSELLERS",
    "COL_COMISSAO": "COMISSÃO",
    "COL_TOTAL_REPASSE": "TOTAL DO REPASSE (R$)",
}

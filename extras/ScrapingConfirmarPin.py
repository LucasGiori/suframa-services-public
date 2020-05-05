import requests
import json
from bs4 import BeautifulSoup
from Login import login,exitSession
from Conexao import newConnection,stopConnection
import urllib3
urllib3.disable_warnings()




def scrapingConfirmarPin():
    session, token = login()
    data={
        'servico': 'ItemSolicitacao'
        ,'columns.0': 'UF'
        ,'columns.1': 'CNPJ do Rementente'
        ,'columns.2': 'Razão Social'
        ,'columns.3': 'N° Nota'
        ,'columns.4': 'Valor da Nota'
        ,'columns.5': 'Data de Emissão'
        ,'columns.6': 'Valor Total Item'
        ,'columns.7': 'Data Limite de Vistoria'
        ,'columns.8': 'Qtde de dias Restantes P/ Vistoria'
        ,'columns.9': 'Situação'
        ,'columns.10':'Qtde de Itens'
        ,'fields.0': 'sigleUfRemetente'
        ,'fields.1': 'numeroCNPJRemetente'
        ,'fields.2': 'razaoSocialRemetente'
        ,'fields.3': 'numeroNota'
        ,'fields.4': 'valorTotalNFE'
        ,'fields.5': 'dataHoraEmissaoFormatada'
        ,'fields.6': 'valorTotalItem'
        ,'fields.7': 'dataLimiteVistoriaFormatada'
        ,'fields.8': 'qtdDiasRestanteVistoria'
        ,'fields.9': 'situacaoNfe'
        ,'fields.10': 'quatidadeItem'
        ,'maxlength': '44'
        ,'page': '1'    
    }
    
    dados_confirmar_pin  = session.get('https://appsimnac.suframa.gov.br/ItemSolicitacao',data=data,headers={'Authorization':'Bearer '+token},verify=False)
    dados_confirmar_pin=json.loads(dados_confirmar_pin.text)
    data =dados_confirmar_pin["items"]

    if data:        
        cursor,conn= newConnection()       
        cursor.execute("""INSERT INTO scraping.confirmarpin (idNFE , idSolicitacaoPin ,sigleUfRemetente ,numeroCNPJRemetente ,razaoSocialRemetente ,numeroNota ,dataHoraEmissao ,valorTotalNFE ,valorTotalItem ,dataLimiteVistoria ,qtdDiasRestanteVistoria ,situacaoNfe ,quantidadeItem ,numeroChaveAcesso ,codigoSituacao ,codigoMunicipioDestinatario ,numeroCNPJDestinatario ,valorNotaFiscalFormatado ,valorTotalItemFormatado ,idNfeSituacao ,usuarioSolicitacao ,ano ,numeroPin ,dataSelagemSefaz ,dataHoraEmissaoFormatada ,dataLimiteVistoriaFormatada ,codigosSolicitacaoPin ,codigoSetor ,descricaoSetor ,mensagemSituacaoNfe ,justificativaRecusada ,codigoSelecaoAssistiva ,nfeCartaCorrecaoPIN)  VALUES  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """,(data["idNFE"],data["idSolicitacaoPin"],data["sigleUfRemetente"],data["numeroCNPJRemetente"],data["razaoSocialRemetente"],data["numeroNota"],data["dataHoraEmissao"],data["valorTotalNFE"],data["valorTotalItem"],data["dataLimiteVistoria"],data["qtdDiasRestanteVistoria"],data["situacaoNfe"],data["quantidadeItem"],data["numeroChaveAcesso"],data["codigoSituacao"],data["codigoMunicipioDestinatario"],data["numeroCNPJDestinatario"],data["valorNotaFiscalFormatado"],data["valorTotalItemFormatado"],["idNfeSituacao"],data["usuarioSolicitacao"],data["ano"],data["numeroPin"],data["dataSelagemSefaz"],data["dataHoraEmissaoFormatada"],data["dataLimiteVistoriaFormatada"],data["codigosSolicitacaoPin"],data["codigoSetor"] ,data["descricaoSetor"] ,data["mensagemSituacaoNfe"] ,data["justificativaRecusada"] ,data["codigoSelecaoAssistiva"] ,"NADA POR ENQUANTO"))
        cursor.commit()
        #stopConnection(conn)
    exitSession(session)



scrapingConfirmarPin()



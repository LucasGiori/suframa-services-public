import requests,json,uuid,urllib3
from urllib import parse as urlDict
from bs4 import BeautifulSoup
from logins.Login import login,exitSession
from configuracoes.Funcoes import LoadJsonItems,LoadJson, acompanhamentoNfeSQL,historicoNfeSQL,updateAcompanhamentoNfeSQL,consultaIdacompanhamento
from configuracoes.Conexao import newConnection,stopConnection




vermelho = '\033[31m'
verde = '\033[32m'
azul = '\033[34m'
ciano = '\033[36m'
magenta = '\033[35m'
amarelo = '\033[33m'
preto = '\033[30m'
branco = '\033[37m'
restaura_cor_original = '\033[0;0m'
negrito = '\033[1m'
reverso = '\033[2m'

def setData(headerkey,page,tipousuario):
    data={
        "servico":"ConsultarHistoricoNfeGrid",
        "columns.0":"Canal",
         "columns.1":"PIN",
        "columns.2":"Data de Solicitação do PIN",
        "columns.3":"Data de Registro do PIN",
        "columns.4":"Situação",
        "columns.5":"Valor TCIF",
        "columns.6":"Nº NF-e",
        "columns.7":"Chave de Acesso",
        "columns.8":"Data de Emissão NF-e",
        "columns.9":"Valor da Nota",
        "columns.10":"UF Destinatário",
        "columns.11":"Município Destinatário",
        "columns.12":"CNPJ do Destinatário",
        "columns.13":"Razão Social do Destinatário",    
        "columns.14":"UF Remetente",
        "columns.15":"Município Remetente",
        "columns.16":"CNPJ do Remetente",
        "columns.17":"Razão Social do Remetente",
        "columns.18":"Inscrição Suframa",
        "columns.19":"Setor",
        "columns.20":"Local de Vistoria",
        "columns.21":"Data Limíte Vistoria",
        "columns.22":"Qtde de Dias Restantes P/Vistoria",
        "columns.23":"Data da Vistoria",
        "columns.24":"Data de Internamento na Suframa",
        "columns.25":"Unidade Cadastradora",
        "fields.0":"dscCanal",
        "fields.1":"numeroPin",
        "fields.2":"dataSolicitacao",
        "fields.3":"dataGeracao",
        "fields.4":"dscSituacao",
        "fields.5":"valorTcif",
        "fields.6":"numeroNF",
        "fields.7":"chaveAcesso",
        "fields.8":"dataEmissaoNf",
        "fields.9":"vlrTotalNfe",
        "fields.10":"ufDestinatario",
        "fields.11":"dscMunicipioDestinatario",
        "fields.12":"cnpjDestinatario",
        "fields.13":"razaoDestinatario",
        "fields.14":"ufRemetente",
        "fields.15":"dscMunicipioRemetente",
        "fields.16":"cnpjRemetente",
        "fields.17":"razaoRemetente",
        "fields.18":"inscricaoSuframa",
        "fields.19":"dscSetor",
        "fields.20":"dscPostoVistoria",
        "fields.21":"dataLimite",
        "fields.22":"qtdeDias",
        "fields.23":"dataVistoria",
        "fields.24":"dataInternamento",
        "fields.25":"dscUnidadeCadastradora",
        "FiltroPesquisa":"4",
        "ValorTipoVistoria":"-1",
        "SituacaoProcesso":"12",
        "maxlength":"44",
        headerkey:"1",
        "page": page,
        "size": "100",
        "tipoUsuario":tipousuario
    }
    return data    

def setHeaders(token):
    frontguid = str(uuid.uuid1())
    headers = {
        "method":"GET"
        ,"authority":"appsimnac.suframa.gov.br"
        ,"scheme":"https"
        ,"path":"/ConsultarHistoricoNfeGrid?servico:ConsultarHistoricoNfeGrid&columns.0:Canal&columns.1:PIN&columns.2:Data%20de%20Solicita%C3%A7%C3%A3o%20do%20PIN&columns.3:Data%20de%20Registro%20do%20PIN&columns.4:Situa%C3%A7%C3%A3o&columns.5:Valor%20TCIF&columns.6:N%C2%BA%20NF-e&columns.7:Chave%20de%20Acesso&columns.8:Data%20de%20Emiss%C3%A3o%20NF-e&columns.9:Valor%20da%20Nota&columns.10:UF%20Destinat%C3%A1rio&columns.11:Munic%C3%ADpio%20Destinat%C3%A1rio&columns.12:CNPJ%20do%20Destinat%C3%A1rio&columns.13:Raz%C3%A3o%20Social%20do%20Destinat%C3%A1rio&columns.14:UF%20Remetente&columns.15:Munic%C3%ADpio%20Remetente&columns.16:CNPJ%20do%20Remetente&columns.17:Raz%C3%A3o%20Social%20do%20Remetente&columns.18:Inscri%C3%A7%C3%A3o%20Suframa&columns.19:Setor&columns.20:Local%20de%20Vistoria&columns.21:Data%20Lim%C3%ADte%20Vistoria&columns.22:Qtde%20de%20Dias%20Restantes%20P%2FVistoria&columns.23:Data%20da%20Vistoria&columns.24:Data%20de%20Internamento%20na%20Suframa&columns.25:Unidade%20Cadastradora&fields.0:dscCanal&fields.1:numeroPin&fields.2:dataSolicitacao&fields.3:dataGeracao&fields.4:dscSituacao&fields.5:valorTcif&fields.6:numeroNF&fields.7:chaveAcesso&fields.8:dataEmissaoNf&fields.9:vlrTotalNfe&fields.10:ufDestinatario&fields.11:dscMunicipioDestinatario&fields.12:cnpjDestinatario&fields.13:razaoDestinatario&fields.14:ufRemetente&fields.15:dscMunicipioRemetente&fields.16:cnpjRemetente&fields.17:razaoRemetente&fields.18:inscricaoSuframa&fields.19:dscSetor&fields.20:dscPostoVistoria&fields.21:dataLimite&fields.22:qtdeDias&fields.23:dataVistoria&fields.24:dataInternamento&fields.25:dscUnidadeCadastradora&FiltroPesquisa:4&ValorTipoVistoria:-1&SituacaoProcesso:12&maxlength:44&isUsuarioDestinatario:1&tipoUsuario:2"
        ,"accept":"application/json, text/plain, */*"
        ,"sec-fetch-dest":"empty"
        ,"authorization": "Bearer "+token
        ,"user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Mobile Safari/537.36"
        ,"frontguid": frontguid
        ,"origin":"https://simnac.suframa.gov.br"
        ,"sec-fetch-site":"same-site"
        ,"sec-fetch-mode":"cors"
        ,"referer":"https://simnac.suframa.gov.br/"
        ,"accept-encoding":"gzip, deflate, br"
        ,"accept-language":"pt-BR,pt;q:0.9,en-US;q:0.8,en;q:0.7"       
    }
    return headers



def consultarNfeByIdnfe(filial,idnfe,cnpj,senha,headerkey,tipousuario):
    session, token = login(cnpj,senha)
    headers = setHeaders(token)
    urllib3.disable_warnings()

    dataHist={
        "idNfe": idnfe
        ,"idVistoria": 0
        ,"tipoVistoria": ""
    }
    historico=LoadJson(session.get('https://appsimnac.suframa.gov.br/HistoricoNfeHistoricos?'+urlDict.urlencode(dataHist),headers=headers,data=dataHist,verify=False))["historicos"]
    return historico            
    


def consultarNfe(filial,cnpj,senha,headerkey,tipousuario):
    session, token = login(cnpj,senha)
    headers = setHeaders(token)
    
    try:  
    
        for page in range(1,20):
            print(negrito,amarelo+"Scraping Page:", page,restaura_cor_original)
            data_destinatario = setData(headerkey,page,tipousuario)
            
            
            url_base = "https://appsimnac.suframa.gov.br/ConsultarHistoricoNfeGrid?"+urlDict.urlencode(data_destinatario)
            dados_consultaNfe = LoadJsonItems(session.get(url_base,
                    data=data_destinatario,
                    headers=headers,
                    verify=False))
            
            for i in dados_consultaNfe:                
                dataHist={
                    "idNfe": i["idNfe"]
                    ,"idVistoria": i["idVistoria"]
                    ,"tipoVistoria": i["tipoVistoria"]
                }
                historico=LoadJson(session.get('https://appsimnac.suframa.gov.br/HistoricoNfeHistoricos?'+urlDict.urlencode(dataHist),headers=headers,data=dataHist,verify=False))["historicos"]
                
                
                cnpj = i["cnpjDestinatario"] if data_destinatario["tipoUsuario"] == "2" else i["cnpjRemetente"]         
                idacompanhamento,cursor,conn,errorcode=acompanhamentoNfeSQL(None,None,[i["idNfe"],i["idVistoria"],i["tipoVistoria"],i["numeroPin"],i["chaveAcesso"],i["dscSituacao"],filial,cnpj])
                
                if errorcode is None:                    
                    for h in historico:
                        try:
                            historicoNfeSQL(None,None,[idacompanhamento,h["dataSituacaOHist"], h["dscSituacaoHist" ],h["usuarioSituacaoHist"], h["motivoSituacaoHist"], h["codCanal"],h["dscCanal"]])
                        except Exception as e:
                            print(e)                        
                elif errorcode == '23505':                   
                    updateAcompanhamentoNfeSQL(None,None, [i["idVistoria"],i["tipoVistoria"],i["numeroPin"],i["dscSituacao"],i["idNfe"],filial])
                    for h in historico:   
                        try:
                            historicoNfeSQL(None,None,[consultaIdacompanhamento(filial,i["idNfe"]),h["dataSituacaOHist"], h["dscSituacaoHist" ],h["usuarioSituacaoHist"], h["motivoSituacaoHist"], h["codCanal"],h["dscCanal"]])
                        except Exception as e:
                            print("Error No Update Histórioco",e)
                else:
                    print(negrito,azul,"\nError Code não é Nulo nem 23505",restaura_cor_original) 
    except Exception as e :
        print("\n\nErro", e)
        pass
    exitSession(session)
    
#consultarNfe(10067)
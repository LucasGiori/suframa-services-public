import traceback,json,requests,uuid,urllib3
from urllib import parse as urlDict
from bs4 import BeautifulSoup
from logins.Login import login,exitSession
from configuracoes.Funcoes import LoadJsonItems,LoadJson, acompanhamentoNfeSQL,historicoNfeSQL,updateAcompanhamentoNfeSQL,nfeNaoPassivelInternamentoSQL
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


def setData(datainicial,datafinal,page,tipousuario):
    print("\nTipo Usuário:",negrito,vermelho,tipousuario,restaura_cor_original,"\n")
    data = {
        "page": page
        ,"size": "100"
        ,"tipoAcesso": "1"
        ,"idTelaAcesso": tipousuario
        ,"servico": "NfeNaoInternavelGrid"
        ,"columns.0": "UF"
        ,"columns.1": "CNPJ Remetente"
        ,"columns.2": "Razão Social"
        ,"columns.3": "UF"
        ,"columns.4": "CNPJ Destinatário"
        ,"columns.5": "Razão Social"
        ,"columns.6": "N° PIN"
        ,"columns.7": "N° Nota"
        ,"columns.8": "Valor da Nota"
        ,"columns.9": "Data de Emissão"
        ,"columns.10":"Data Limite de Vistoria"
        ,"columns.11":"Usuário"
        ,"columns.12": "Data da Operação"
        ,"columns.13": "Situação"
        ,"columns.14": "Motivo"
        ,"fields.0": "ufRementente"
        ,"fields.1": "cnpjRemetente"
        ,"fields.2": "razaoRemetente"
        ,"fields.3": "ufDestinatario"
        ,"fields.4": "cnpjDestinatario"
        ,"fields.5": "razaoDestinatario"
        ,"fields.6": "numeroPin"
        ,"fields.7": "numeroNF"
        ,"fields.8": "valorNF"
        ,"fields.9": "dataHoraEmissao"
        ,"fields.10":"dataLimite"
        ,"fields.11": "usuario"
        ,"fields.12": "dataOperacao"
        ,"fields.13": "situacao"
        ,"fields.14": "motivo"
        ,"fields.15": "qtdeItem"
        ,"opcaochave": "0"
        ,"situacaonf": "0"
        ,"ufdestino": "TD"
        ,"uforigem": "TD"
        ,"origemcnpj":tipousuario
        ,"opcaoperiodo": "2"
        ,"datainicial": datainicial
        ,"datafinal": datafinal
        ,"TipoGrid":"1"
    }

    #print(data)
    return data

def setHeaders(token,page,tipousuario):
    frontguid = str(uuid.uuid1())
    headers={
        "method":"GET"
        ,"authority":"appsimnac.suframa.gov.br"
        ,"scheme":"https"
        ,"path":"/NfeNaoInternavelGrid?page="+str(page)+"&size=100&tipoAcesso=1&idTelaAcesso="+str(tipousuario)+"&servico=NfeNaoInternavelGrid&columns.0=UF&columns.1=CNPJ%20Remetente&columns.2=Raz%C3%A3o%20Social&columns.3=UF&columns.4=CNPJ%20Destinat%C3%A1rio&columns.5=Raz%C3%A3o%20Social&columns.6=N%C2%B0%20PIN&columns.7=N%C2%B0%20Nota&columns.8=Valor%20da%20Nota&columns.9=Data%20de%20Emiss%C3%A3o&columns.10=Data%20Limite%20de%20Vistoria&columns.11=Usu%C3%A1rio&columns.12=Data%20da%20Opera%C3%A7%C3%A3o&columns.13=Situa%C3%A7%C3%A3o&columns.14=Motivo&fields.0=ufRementente&fields.1=cnpjRemetente&fields.2=razaoRemetente&fields.3=ufDestinatario&fields.4=cnpjDestinatario&fields.5=razaoDestinatario&fields.6=numeroPin&fields.7=numeroNF&fields.8=valorNF&fields.9=dataHoraEmissao&fields.10=dataLimite&fields.11=usuario&fields.12=dataOperacao&fields.13=situacao&fields.14=motivo&fields.15=qtdeItem&opcaochave=0&situacaonf=0&ufdestino=TD&uforigem=TD&origemcnpj="+str(tipousuario)+"&opcaoperiodo=2&datainicial=2020-01-01&datafinal=2020-01-31&TipoGrid=1"
        ,"accept":"application/json, text/plain, */*"
        ,"authorization":"Bearer "+token
        ,"user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Mobile Safari/537.36"
        ,"frontguid":frontguid
        ,"origin":"https://simnac.suframa.gov.br"
        ,"sec-fetch-site":"same-site"
        ,"sec-fetch-mode":"cors"
        ,"sec-fetch-dest":"empty"
        ,"referer":"https://simnac.suframa.gov.br/"
        ,"accept-encoding":"gzip, deflate, br"
        ,"accept-language":"pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    return headers


def consultaNfeNaoPassivelInternamento(filial,cnpj,senha,datainicial,datafinal,tipousuario):
    session, token = login(cnpj,senha)
    urllib3.disable_warnings()  
    try:
        conn,cursor= newConnection()   

        for page in range(1,2):
            headers = setHeaders(token,page,tipousuario)
            data = setData(datainicial,datafinal,page,tipousuario)

            url_base = "https://appsimnac.suframa.gov.br/NfeNaoInternavelGrid?"+urlDict.urlencode(data)
            print("\n\n\n",negrito,verde,url_base,restaura_cor_original,"\n\n\n")
            dados = LoadJsonItems(session.get(url_base,
                                            data=data,
                                            headers=headers,
                                            verify=False))

            for d in dados:           
                print(d["idNF"],d["dataOperacao"],d["dataHoraEmissao"],d["dataLimite"],d["situacao"],d["usuario"],d["motivo"],d["numeroPin"],d["valorNF"],d["cnpjRemetente"],d["cnpjDestinatario"])
                
                nfeNaoPassivelInternamentoSQL(cursor,conn,[d["idNF"],d["dataOperacao"],d["dataHoraEmissao"],d["dataLimite"],d["situacao"],d["usuario"],d["motivo"],d["numeroPin"],d["valorNF"].replace('.','').replace(',','.'),d["cnpjRemetente"],d["cnpjDestinatario"],filial])
                conn.commit()
            

    except Exception as e:
        print("\n\nErro ao tentar Inciar a Conexão", e)
        print(traceback.format_exc())

        pass
    try:
        
        stopConnection(conn) 
        return dados       
    except  Exception as e:
        print("\n\nError ao Tentar Finalizar Conexão", e)
        return dados
        #passC
        
    exitSession(session)
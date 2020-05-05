
import sys,urllib3
sys.path.insert(0,'../')
from flask import Flask, request, jsonify
from gerenciamento import main  
from configuracoes import Funcoes
urllib3.disable_warnings()

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<pre>API-SUFRAMA-SIMNAC</pre>"


# A route to return all of the available entries in our catalog.
@app.route('/api-suframa/getRotina', methods=['GET','POST'])
def getRotina():
    #if request.method == 'POST':
    main.main()
    return jsonify({"rotina":"Sucesso"})


# A route to return all of the available entries in our catalog.
@app.route('/api-suframa/getAcomapanhamento', methods=['GET','POST'])
def getAcomapanhamento():
    #if request.method == 'POST':
    if request.method == 'POST':
        content = request.get_json()
        datainicial = content['datainicial']
        datafinal = content['datafinal']

        filiais = Funcoes.consultaFiliais()
        for i in filiais:
            print("Consultando Filial ",i[0],"\n")           
            #filial,tipofilial,datainicial,datafinal 
            #filial,cnpj,senha,headerkey,tipousuario,datainicial,datafinal
            main.getCosultaNfeByDataEmissao(i[0],i[4],datainicial,datafinal)
        
    return jsonify({"Rotina Acompanhamento":"Sucesso"})


# A route to return all of the available entries in our catalog.
@app.route('/api-suframa/getHistorico', methods=['POST'])
def getHistorico():
    if request.method == 'POST':
        content = request.get_json()
        idnfe = content['idnfe']
        filial = int(content['filial'])
        tipousuario = content['tipousuario']
        jsonstring = main.getConsultaIdnfe(filial,idnfe,tipousuario)
    return jsonify(jsonstring)

@app.route('/api-suframa/getNfeNaoInternalizadas', methods=['POST'])
def getNfeNaoInternalizadas():
    if request.method == 'POST':
        content = request.get_json()
        filial = int(content['filial'])
        tipousuario = content['tipousuario']
        datainicial = content['datainicial']
        datafinal = content['datafinal']
        jsonstring = main.getNfeNaoPassivelInternamento(filial,tipousuario,datainicial,datafinal)
    return jsonify(jsonstring)

app.run()




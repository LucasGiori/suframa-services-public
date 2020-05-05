import sys
sys.path.insert(0,'../')
from configuracoes.Funcoes import consultaFiliais,consultaCredenciaisFl,newConnection,stopConnection,consultaParametroFilial
#from logins.login import login,exitSession
from consultas.ConsultarAcompanhamentoNfe import consultarNfe,consultarNfeByIdnfe
from consultas.ConsultaNfeByDataEmissao  import consultarNfeByDataEmissao
from consultas.ConsultaNfeNaoPassivelInternamento import consultaNfeNaoPassivelInternamento


#
def main():
    filiais = consultaFiliais()
    for i in filiais:
        print("Consultando Filial ",i[0],"\n")
        credenciais = consultaCredenciaisFl(i[0])    
        #print(credenciais[1])
        consultarNfe(i[0],str(credenciais[1]),str(credenciais[2]),i[1],i[2])

def getConsultaIdnfe(filial,idnfe,tipofilial):
    parametros=consultaParametroFilial(filial,tipofilial)
    credenciais = consultaCredenciaisFl(filial)
    return consultarNfeByIdnfe(filial,idnfe,credenciais[1],credenciais[2],parametros[1],parametros[2])

def getCosultaNfeByDataEmissao(filial,tipofilial,datainicial,datafinal ):
    parametros=consultaParametroFilial(filial,tipofilial)
    credenciais = consultaCredenciaisFl(filial)
    consultarNfeByDataEmissao(filial,credenciais[1],credenciais[2],parametros[1],parametros[2],datainicial,datafinal)

def getNfeNaoPassivelInternamento(filial,tipofilial,datainicial,datafinal):
    parametros=consultaParametroFilial(filial,tipofilial)
    credenciais = consultaCredenciaisFl(filial)
    ##print("\n\n\n\n",parametros,"\n\n\n\n\n")
    return consultaNfeNaoPassivelInternamento(filial,credenciais[1],credenciais[2],datainicial,datafinal,parametros[2])


#main()


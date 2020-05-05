import json,sys,psycopg2
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

azul = '\033[34m'


def LoadJsonItems(response):
    #print(json.dumps(response.text))
    return json.loads(response.text)["items"]

def LoadJson(response):
    return json.loads(response.text)


def print_psycopg2_exception(err):
    err_type, err_obj, traceback = sys.exc_info()

    print (negrito+vermelho+"pgcode:", err.pgcode," Message: ",err.pgerror , "\n"+restaura_cor_original) 
    return err.pgcode,err.pgerror


def consultaFiliais():
    
    try:
        conn,cursor= newConnection()
        cursor.execute("""SELECT
                                vfl.idfilial
                                ,tu.parametroconsulta as tipofilialkey
                                ,vfl.idtipousuario
                                ,vfl.tipousuarioheader
                                ,tu.descricao as descricaotipousuario
                          FROM glb.vinculofilial vfl
                          LEFT JOIN sis.tipousuario tu on (tu.idtipousuario = vfl.idtipousuario);""")
        retorno  = cursor.fetchall()
        stopConnection(conn)
        print("Retorno")
        return retorno
    except Exception as e :
        try:
            print("Stop Connection Error", e)
            stopConnection(conn)
        except:
            pass
        return None

def consultaParametroFilial(filial,tipofilial):
    
    try:
        conn,cursor= newConnection()
        cursor.execute("""SELECT
                                vfl.idfilial
                                ,tu.parametroconsulta as tipofilialkey
                                ,vfl.idtipousuario
                                ,vfl.tipousuarioheader
                          FROM glb.vinculofilial vfl
                          LEFT JOIN sis.tipousuario tu on (tu.idtipousuario = vfl.idtipousuario)
                          WHERE vfl.idfilial = %s
                            AND tu.descricao ilike %s;""",(filial,'%'+tipofilial+'%',))
        retorno  = cursor.fetchone()
        stopConnection(conn)
        #print("Retorno")
        return retorno
    except Exception as e :
        try:
            print("Stop Connection Error", e)
            stopConnection(conn)
        except:
            pass
        return None

def consultaCredenciaisFl(filial):
    try:
        conn,cursor= newConnection()
        cursor.execute("""SELECT
                                fl.idfilial
                                ,fl.login
                                ,fl.senha
                          FROM glb.filial fl
                          WHERE fl.idfilial in (%s)""",(filial,))
        retorno  = cursor.fetchone()
        stopConnection(conn)
        return retorno
    except Exception as e :
        try:
            stopConnection(conn)
        except:
            pass
        return None


def consultaIdacompanhamento(filial,idnfe):
    try:
        conn,cursor= newConnection()
        cursor.execute("""SELECT
                                a.idacompanhamento
                          FROM consultanfe.acompanhamentonfe a
                          WHERE a.idfilial = %s
                            AND a."idNfe" = %s""",(filial,idnfe,))
        retorno  = cursor.fetchone()
        stopConnection(conn)
        return retorno[0]
    except Exception as e :
        try:
            stopConnection(conn)
        except:
            pass
        return None

def acompanhamentoNfeSQL(cursor,conn,p):
             
    try:
        conn,cursor= newConnection()
        cursor.execute("""INSERT INTO consultanfe.acompanhamentonfe ("idNfe" ,"idVistoria" ,"tipoVistoria" ,"numeroPin" ,"chaveAcesso" ,"dscSituacao",idfilial,cnpj)  VALUES  (%s,%s,%s,%s,%s,%s,%s,%s)  RETURNING idacompanhamento;""",(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],))
        conn.commit()
        idcompanhamento = cursor.fetchone()[0]         
        stopConnection(conn)
        errorcode=None
    except Exception as e :
        print ("\n\n\n ERRO FUNÇÃO ACOMPANHAMENTO: ",negrito,azul, e,restaura_cor_original)
        errorcode, errormessage=print_psycopg2_exception(e)
        idcompanhamento = None
    return idcompanhamento,cursor,conn,errorcode


def historicoNfeSQL(cursor,conn,parametros):
    #conn,cursor= newConnection()  
    parametros[1] = parametros[1].replace(' às ',' ')   
    try: 
        conn,cursor= newConnection() 
        cursor.execute("""INSERT INTO consultanfe.historiconfe (idacompanhamento ,"dataSituacaOHist" ,"dscSituacaoHist" ,"usuarioSituacaoHist" ,"motivoSituacaoHist","codCanal","dscCanal")  VALUES  (%s,%s,%s,%s,%s,%s,%s)  RETURNING idhistorico; """,(parametros[0],parametros[1],parametros[2],parametros[3],parametros[4],parametros[5],parametros[6],))
        conn.commit()
        stopConnection(conn)
    except Exception as e:
        conn.rollback()
        stopConnection(conn)
        #print_psycopg2_exception(e)
        print ("\n\n\nERRO FUNÇÃO HISTORICO",negrito,azul, e,restaura_cor_original)
    return None

def nfeNaoPassivelInternamentoSQL(cursor, conn,p):
    try:
        cursor.execute("""INSERT INTO consultanfe.nfenaopassivelinternamento (idnfe,dataoperacao,dataemissao,datalimitevistoria,situacao,usuario,motivo,numeropin,valornfe,cnpjremetente,cnpjdestinatario,idfilial) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[7],p[8],p[9],p[10],p[11],))
        conn.commit()
        return 1
    except Exception as e:
        cursor.rollback()
        #print_psycopg2_exception(e)
        print ("\n\n\n",azul, e)
    return None


def updateAcompanhamentoNfeSQL(cursor,conn,parametros):
    try:
        conn,cursor= newConnection() 
        cursor.execute("""UPDATE consultanfe.acompanhamentonfe
                          SET
                            "idVistoria" = %s
                            ,"tipoVistoria"=%s
                            ,"numeroPin"= %s
                            ,"dscSituacao"= %s
                            ,ultimaconsulta=now()
                        WHERE  "idNfe" = %s
                               and idfilial = %s
                        """,(parametros[0],parametros[1],parametros[2],parametros[3],parametros[4],parametros[5],))
        conn.commit()
        stopConnection(conn)
        return 1
    except Exception as e:
        conn.rollback()
        #print_psycopg2_exception(e)
        print ("\n\n\nERRO FUNÇÃO UPDATE",negrito,magenta, e,restaura_cor_original)
        return 1
    
    
    
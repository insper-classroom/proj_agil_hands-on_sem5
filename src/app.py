from flask import Flask, request, jsonify
from pathlib import Path
import pandas as pd
from model.db import delete_query, select_query, insert_query, update_query


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/registrado/", methods=['GET'])
def rota_buscar_todos_registrados():

    cmd_sql = 'select * from tbl_registrados'
    resultado = select_query(cmd_sql)

    return jsonify(resultado), 200



@app.route("/registrado/<string:ean>", methods=['GET'])
def rota_buscar_registrado_por_ean(ean):

    cmd_sql = 'select * from tbl_registrados WHERE ean = ?'
    registrado, sucesso = select_query(cmd_sql, ean)

    resp = {'uid':registrado[0], 'ean':registrado[1], 'name':registrado[2]}

    if sucesso:
        return jsonify(resp), 200
    else:
        return {'erro':'Produto não encontrado nos registros'}, 404



@app.route("/registrado/<string:ean>", methods=['POST'])
def rota_inserir_prod_no_registro(ean):

    try:
        content = request.get_json()
    except:
        return {'erro':'Erro ao parsear o Json'}, 400

    cmd_sql = 'select * from tbl_registrados WHERE ean = ?'
    registrado, encontrado = select_query(cmd_sql, ean)

    if not(encontrado):
        dado = {'ean': ean, 'name':content['name']}
        cmd_sql = 'insert into tbl_registrados(ean, name) values (?, ?)'
        sucesso = insert_query(cmd_sql, dado)
        if sucesso:
            return jsonify({'mensagem':f'Produto {content["name"]} registrado com sucesso'}), 201
        else:
            return {'erro':'Erro interno'}, 500    
    else:
        return {'erro':'Produto já existe no registro'}, 400
    
        
@app.route("/registrado/<string:ean>", methods=['PUT'])
def rota_update_prod_no_registro(ean):

    try:
        content = request.get_json()
    except:
        return {'erro':'Erro ao parsear o Json'}, 400

    cmd_sql = 'select * from tbl_registrados WHERE ean = ?'
    registrado, encontrado = select_query(cmd_sql, ean)

    if encontrado:
        dado = {'ean': ean, 'name':content['name']}
        cmd_sql = 'update tbl_registrados set name = ? WHERE ean = ?'
        linhas_afetadas, sucesso = update_query(cmd_sql, dado)
        if sucesso:
            return jsonify({'mensagem':f'{linhas_afetadas} foram atualizadas com sucesso'}), 200
        else:
            return {'erro':'Erro interno'}, 500    
    else:
        return {'erro':'Produto já existe no registro'}, 400


if __name__ == '__main__':
    app.run(debug=True)
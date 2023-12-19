import json
import os
import re

'''
formato do novo json
{
    "nome-bairro":{
        "bairro-para-centro":{
            "dias":{
    
            },
            "outros-dias":{
    
            }
        },
        "centro-para-bairro":{
            "dias":{
    
            },
            "outros-dias":{
    
            }
        }
    }
}
'''




if __name__ == "__main__":
    regex_nome_bairro_1 = r'centro_sentido_([\w_]*)'
    regex_nome_bairro_2 = r'([\w_]*)_sentido_centro'

    files = [f for f in os.listdir() if os.path.isfile(f)]
    novo_json = {}
    for file in files:
        print(file)
        novo_bairro = {}
        if file.endswith(".json") and file != "bairros.json":
            with open(file, "r") as f:
                data = json.load(f)

            for sentido in data["horarios"].keys():
                # extrai o nome do bairro
                sentido_tipo = ''
                sentido_corrigido = sentido.replace(" ", "_").lower()
                print(sentido_corrigido)
                if (sentido_corrigido.startswith("centro")):
                    nome_bairro = sentido_corrigido.replace("centro_sentido_", "").replace("_", " ").strip().replace(" ", "_")
                    sentido_tipo = "do_centro"
                else:
                    nome_bairro = sentido_corrigido.replace("_sentido_centro", "").replace("_", " ").strip().replace(" ", "_")
                    sentido_tipo = "para_centro"
                if ("rodoviária" in nome_bairro):
                    nome_bairro = nome_bairro.replace("_rodoviária", "")
                    sentido_tipo = "para_rodoviaria"

                print("Nome do bairro: ", nome_bairro)
                if nome_bairro not in novo_json:
                    novo_json[nome_bairro] = {}

                if (sentido_tipo == "do_centro"):
                    novo_json[nome_bairro]["centro_para_bairro"] = data["horarios"][sentido]
                elif (sentido_tipo == "para_centro"):
                    novo_json[nome_bairro]["bairro_para_centro"] = data["horarios"][sentido]
                else:
                    novo_json[nome_bairro]["bairro_para_rodoviaria"] = data["horarios"][sentido]
               


            data["nome"] = file

    with open("bairros.json", "w") as f:
        json.dump(novo_json, f, indent=2, ensure_ascii=False)

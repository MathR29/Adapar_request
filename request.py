import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse,parse_qs

def get_class_id(class_):
    class_dict = {
        "herbicida": "9",
        "fungicida": "8",
        "inseticida": "10",
        "nematicida": "11"
    }
    return class_dict[class_]

def get_crop_id(crop):
    crop_dict = {
        "soja": "531",
        "milho": "428",
        "trigo": "560",
        "sorgo": "533",
        "mandioca": "405",
        "cafe": "139",
        "feijao": "292",
        "pastagem": "701"
    }
    return crop_dict[crop]

def merge_dicts(dict1,dict2):
    map_dict1_marca = dict(zip(dict1["Produto"],
                               dict1["Marca"]))
    map_dict1_sit = dict(zip(dict1["Produto"],
                               dict1["Situacao"]))
    map_dict1_tox = dict(zip(dict1["Produto"],
                               dict1["Toxicidade"]))
    map_dict2 = dict(zip(dict2["Produto"],
                         dict2["Cod"])) 
    all_products = set(dict1["Produto"]) & set(dict2["Produto"])
    merged = {}
    for product in all_products:
        merged[product] = {
            "Marca": map_dict1_marca[product],
            "Situacao": map_dict1_sit[product],
            "Toxicidade": map_dict1_tox[product],
            "Cod": map_dict2[product],
        }
    return merged

def get_product_pdf_link(cod,cultura,classe):
    url = "https://celepar07web.pr.gov.br/agrotoxicos/listar.asp"
    querry = {
        "Cod": f"{cod}",
        "descIngrediente": "",
        "CodIngredienteAtivo": "null",
        "CodFormulacao": "null",
        "IdRegistrante": "null",
        "CodFormaAcao": "null",
        "CodAlvo": "null",
        "CodGrupoQuimico": "null",
        "CodClassToxicologica": "null",
        "CodSituacao": "null",
        "CodClassificacao": get_class_id(classe),
        "CodEspecie": get_crop_id(cultura),
        "CodAgrotoxico": "null",
        "NumeroRegistro": "null",
        "expurgo": "null",
        "aplica": "null",
        "tratam": "null",
        "ClassificacaoQuiBio": "null",
        "criterioAgrotoxico": "",
        "criterioIngredienteAtivo": "",
        "criterioRegistrante": "",
        "criterioClassificacaoToxicologica": "",
        "criterioPraga": "",
        "criterioSituacao": "",
        "criterioClasse": classe,
        "criterioCulturaInfestada": cultura,
        "criterioExpurgo": "",
        "criterioAplicacaoAerea": "",
        "criterioTratamentoSementes": ""
    }

    response = requests.get(url = url, params = querry).text
    soup = BeautifulSoup(response, 'html.parser')
    links = soup.find_all("a")
    for link in links:
        text = link.getText(strip=True)
        if text.endswith(".pdf"):
            return text
        

def adapar_requets(cultura,classe):
    url = "https://celepar07web.pr.gov.br/agrotoxicos/resultadoPesquisa.asp"
    payload = {
        "criterioClasse": classe,
        "criterioCulturaInfestada": cultura,
        "select8": get_class_id(classe),  #Class_id
        "select10": get_crop_id(cultura), #Cultura_id
        "submit1": "Pesquisar"
    }
    response = requests.post(url = url,
                             data = payload)
    html = BeautifulSoup(response.text, "html.parser")
    rows = html.find_all("td")
    links = html.find_all("a")
    products_id_list = {"Produto": [],
                        "Cod":[]}
    products_list = {"Produto": [],
                     "Marca": [],
                     "Situacao":[],
                     "Toxicidade": []}
    for link in links:
        href = link.get("href")
        try:
            name = link.text.strip()
            query = href.split("?")[1]
            parms = parse_qs(query)
            cod = parms.get("Cod",[None])[0]
            products_id_list["Produto"].append(name)
            products_id_list["Cod"].append(cod)
        except:
            continue
    for i in range(0,len(rows),4):
        try:
            products_list["Produto"].append(rows[i].getText(strip = True))
            products_list["Marca"].append(rows[i+3].getText(strip = True))
            products_list["Situacao"].append(rows[i+1].getText(strip = True))
            products_list["Toxicidade"].append(rows[i+2].getText(strip = True))
        except:
                print("Something went wrong.")
                continue
    merged = merge_dicts(dict1=products_list,dict2=products_id_list)
    return merged


get_product_pdf_link(i,"mandioca","fungicida")

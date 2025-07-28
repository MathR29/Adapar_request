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
    products_id_list = []
    products_list = []
    for link in links:
        href = link.get("href")
        try:
            name = link.text.strip()
            query = href.split("?")[1]
            parms = parse_qs(query)
            cod = parms.get("Cod",[None])[0]
            products_id_list.append({
                "Produto": name,
                "Cod": cod
            })
        except:
            continue
    

    for i in range(0,len(rows),4):
        try:
            products_list.append({
                "Produto": rows[i].getText(strip = True),
                #"Marca": rows[i+3].getText(strip = True),
                #"Situacao": rows[i+1].getText(strip = True),
	            #"Toxicidade": rows[i+2].getText(strip = True)
    })
        except:
                print("Something went wrong.")
                continue
    print(len(products_list))
    print("#####################################################################")
    return print(len(products_id_list))

adapar_requets("soja","herbicida")

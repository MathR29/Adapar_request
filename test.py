dict1 = {
    "Produto": ["ProdA","ProdB","ProdC","ProdD"],
    "Info": ["InfoA","InfoB","InfoC","InfoD"]
}

dict2 ={
    "Produto": ["ProdA","ProdB","ProdC"],
    "Cod": ["A","B","C"]
}

test = set(dict1) & set(dict2)

map_dict1 = dict(zip(dict1["Produto"],dict1["Info"]))
map_dict2 = dict(zip(dict2["Produto"],dict2["Cod"]))




merged = set(dict1["Produto"]) & set(dict2["Produto"])


novo_dict = {}

for produto in merged:
    novo_dict[produto] = {
            "Cod": map_dict2[produto],
        "Info": map_dict1[produto]
    }

print(map_dict1)
print(map_dict2)
print(merged)
print(novo_dict)
print(test)

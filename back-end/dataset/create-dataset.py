import pandas as pd

json = pd.read_json("./recipes_raw_nosource_ar.json")


json = json.transpose()

print(json.info())
# json = json[['title', 'instructions']]

# json.to_csv('recipes.csv', index=None)
# print(json.info())
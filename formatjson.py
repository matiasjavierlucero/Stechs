import json

modems_habilitados=[]
with open('models.json') as file:
    data = json.load(file)
    for models  in data['models']:
        if models not in modems_habilitados:
            modems_habilitados.append(models)

dat={
  "version": "v1.0",
  "models": [
    
    ]
    }
    
for modem in modems_habilitados:
    dat['models'].append({
      "vendor": modem['vendor'],
      "name": modem['name'],
      "soft": modem['soft'],
      "tags":''
    })

with open('nuevojson.json', 'w') as file:
    json.dump(dat, file)

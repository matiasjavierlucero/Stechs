## Instalacion

Antes que nada debemos crear una base de datos con el nombre Stechs e importar el .sql dado

 - Instalacion de los requerimientos

```sh
pip install -r requirements.txt
```
 - Para Python3
 ```sh
pip3 install -r requirements.txt
```
 - Generar el json adecuado, tomando como base el archivo model.json para obtener un nuevo json donde se eliminen los registros repetidos y se agregue la clave 'tags'
 ```sh
python3 formatjson.py
 ```
 -Correr la Api y luego la Aplicacion principal
  ```sh
  python3 api.py
  flask run o python3 app.py 
  ```
  - Obtener cliente en http://127.0.0.1:5000/
  - Mientras que el servidor correra en http://127.0.0.1:4500
  

  ## Endpoints

  Los endpoints se encuentran en la siguiente coleccion de Postma

  https://documenter.getpostman.com/view/10186174/TzCQaS5K

  

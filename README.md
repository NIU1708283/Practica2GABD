[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/yh1IUIvK)
# GABD Practica 2. Gestió de Dades Massives i Optimització de Consultes
## Introducció
En aquesta pràctica treballarem la importació massiva de dades en Oracle utilitzant Python, les gestionarem i avaluarem l’impacte dels índexs en l’execució de consultes. Per la importació de dades haureu de completarla funció
```python
insertVectorDataset(dbConn, nameDataset : str,  *args , **kwargs) -> bool
```
del notebook [insertData](src/insertData.ipynb) per importar dades del [UCI](https://archive.ics.uci.edu/). En el notebook [testUCI](src/testUCI.ipynb)  no haureu de fer res. Únicament implementar la funció __insertExperiment__ encarregada de guardar els resultats dels experiments que s'implementen en el notebook:

```python
resultat = cursor.callfunc("insertExperiment", bool, [dataset,
                                                      nom_curt,
                                                      nom_classificador,
                                                      iteracio,
                                                      var ,
                                                      data_experiment,
                                                      f1_score, accuracy])
```

Finalment, amb tot el volum de dades generat, s’avaluarà l’impacte dels índexs en les consultes a fer.

## Materials i Recursos
Per fer el lliurament d’aquest part disposeu dels següents materials i recursos:
- Notebooks d'inici: El codi d'aquest repositori,
- Dades d’exemple de la UCI: Iris, Ionosphere, Breast Cancer, Letter Recognition. Els podeu recuperar a partir del paquet Python de la UCI (ucimlrepo).

A més, necessitareu els següents programes per a realitzar les pràctiques i monitoritzar els SGBD: SQLDeveloper, Pycharm (IDE per programar en Python). Caldrà que disposeu d’un client SSH per connectar-vos a les màquines de les pràctiques. A la màquina main del projecte teniu instal·lat un intèrpret de Python3. A més, teniu instal·lada la comanda tmux , aquesta comanda permet obrir sessions en la terminal i recuperar-la en una nova sessió. És a dir, us permet entrar i sortir de la màquina main per ssh mantenint el que havia en la sessió anterior.

## Contacte
Per resoldre els dubtes i qüestions que pugueu tenir de la pràctica, podeu contactar als professors de l'assignatura:
- Oriol (oriol.ramos@uab.cat)
- Francis (franciscojavier.cobo@uab.cat)

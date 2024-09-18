# State-of-the-art

**Table des matières**

1. Manipulation/Visualisation de graphes temporels  
    1. 1 Logiciels   
        1. 1.1 Gephi   
        1. 1.2 Cytoscape
    1. 2 Modules
        1. 2.1 Graph-tool
        1. 2.2 NetworkX

## Manipulation/Visualisation de graphes temporels

### Logiciels

> **Gephi**  
> Bastian M., Heymann S., Jacomy M. (2009). Gephi: an open source software for exploring and manipulating networks. International AAAI Conference on Weblogs and Social Media.  

**Année de création** : 2008

**Dernière release** : 2022

**License** : Open-source

**Description** :  

"Gephi is the leading visualization and exploration software for all kinds of graphs and networks." [citation](https://gephi.org/)

**Fonctionnalités** :

- Création de graphes a la main.
- Importation/Exportation de graphes (différents formats).
- Customisation de graphes : taille/couleur des noeuds/arêtes, distances...
- Calcul de métriques : [Degrés, betweenness, closeness...](https://gephi.org/)
- Algorithme de Layout.

**Avantages** :

- Exemples concrets de graphes : [Zachary's karate club](https://github.com/gephi/gephi/wiki/Datasets), [The Marvel Social Network](https://github.com/gephi/gephi/wiki/Datasets)...
- Pluggins disponibles : Erdős-Rényi Generator, [JSON Exporter](https://github.com/oxfordinternetinstitute/gephi-plugins/tree/jsonexporter-plugin)...
- Graphes compatibles : tous les types.
- Moteur de rendu intégré.
- "Data Laboratory" disponible : manipulation de graphes avec un tableau.
- Performant : gestion de grands graphes.

**Inconvénients/Lacunes** :

- Trop de fonctionnalités. Difficile à prendre en main. Interface chargée.
- Trop d'éléments customisables.
- Pas de rapports avec le théorie des automates.
- Orientation Layout trop importante.
- Pas de focus sur les graphes temporels.

> **Cytoscape**  
> Shannon P, Markiel A, Ozier O, Baliga NS, Wang JT, Ramage D, Amin N, Schwikowski B, Ideker T. Cytoscape: a software environment for integrated models of biomolecular interaction networks Genome Research 2003 Nov; 13(11):2498-504

**Année de création** : 2002

**Dernière release** : 2019

**License** : Open-source

**Description** :  

"Cytoscape est une plate-forme logicielle open source permettant de visualiser les réseaux d'interactions moléculaires et les voies biologiques et d'intégrer ces réseaux avec des annotations, des profils d'expression génique et d'autres données d'état. Bien que Cytoscape ait été conçu à l’origine pour la recherche biologique, il s’agit désormais d’une plate-forme générale pour l’analyse et la visualisation de réseaux complexes." [cite](https://cytoscape.org/what_is_cytoscape.html#section-image1)

**Fonctionnalités** :

- Création de graphes a la main.
- Importation/Exportation de graphes (différents formats).
- Customisation de graphes : taille/couleur des noeuds/arêtes, distances...
- Calcul de métriques : [Degrés, betweenness, closeness...](https://gephi.org/)
- Algorithme de Layout.

**Avantages** :

- Moteur de rendu intégré (via Cytoscape.js).
- Base de données de graphes.
- Pluggins disponibles.
- Visualisation sous forme de tableau.
- Performant : gestion de grands graphes.

**Inconvénients/Lacunes** :

- Nécessite Java17.
- Difficile à prendre en main.
- Pas de rapports avec le théorie des automates.
- Logiciel peu fluide, sensation de lag.
- Encore très orienté biologie.

### Modules

> **Graph-tool**  
> Tiago P. Peixoto, “The graph-tool python library”, figshare. (2014) DOI: 10.6084/m9.figshare.1164194 [sci-hub, @tor]

**Année de création** : 2002

**Dernière release** : 2019

**License** : Open-source

**Description** :  

"Graph-tool is an efficient Python module for manipulation and statistical analysis of graphs (a.k.a. networks)." [cite](https://graph-tool.skewed.de/)

**Fonctionnalités** :

- Créer/Modifier/Manipuler des graphes.
- Importation/Exportation de graphes.
- Génération de graphes : aléatoires...
- Opérations sur les graphes : [centralité, clustering...](https://graph-tool.skewed.de/static/doc/index.html)
- Visualisation d'un graphe.
- Algorithme de Layout.

**Avantages** :

- Performant/Rapide : implémentation des algorithmes et du code en c++.
- Parallèle : Algorithmes implémentés en parallèle avec OpenMP.
- Module complet. Bien documenté.
- Interopérabilité.
- Convient pour des grands graphes.

**Inconvénients/Lacunes** :

- TBC


> **NetworkX**  
> Aric A. Hagberg, Daniel A. Schult and Pieter J. Swart, “Exploring network structure, dynamics, and function using NetworkX”, in Proceedings of the 7th Python in Science Conference (SciPy2008), Gäel Varoquaux, Travis Vaught, and Jarrod Millman (Eds), (Pasadena, CA USA), pp. 11–15, Aug 2008

**Année de création** : 2008 (v 0.36)

**Dernière release** : 2023 (v 3.2.1)

**License** : Open-source

**Description** :  

"NetworkX is a Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks." [cite](https://networkx.org/)

**Fonctionnalités** :

- Créer/Modifier/Manipuler des graphes.
- Importation/Exportation de graphes.
- Génération de graphes : aléatoires...
- Opérations sur les graphes : [centralité, clustering...](https://networkx.org/documentation/networkx-3.2.1/tutorial.html)
- Visualisation d'un graphe.
- Algorithme de Layout.

**Avantages** :

- Performant/Rapide : implémentation des algorithmes et du code en c/c++/FORTAN.
- Module complet. Bien documenté.
- Interopérabilité.
- Convient pour des grands graphes.

**Inconvénients/Lacunes** :

- TBC







Neo4j - Creer en 2007 - écrit en Java - Système de gestion de bd.

TimeMapper 

Tulip 

TempoVis 

Visone

TimeArcs

Space-Time Cube Explorer

Graphviz

---
---
---
---

## Temporal Connectivity

**Bibliography**

- [1] Testing Temporal Connectivity in Sparse Dynamic Graphs (https://arxiv.org/abs/1404.7634)

**Content**

// Method greedy --> explications, principes, temporal djisktra.
// foremost, fastest, shortest -> explications, sources, principes.
// Temporal spanner --> explications, principes, sources, methodes employées, pourquoi ?
// Nouvelle methode --> explication, principes, implémentation, perfs, compléxité.

## Dismountability

**Bibliography**  

- [2] Temporal cliques admit sparse spanners (https://www.sciencedirect.com/science/article/pii/S0022000021000428#se0110) 

**Content**

// Delegation --> principe, ecplication e^+(v), e^-(v)
// Dismountabilty --> dismountable vertex, dismontable graph, fully dismontable graph.
// K-hop Dismountability --> k-hop dismountable vertex, k-hop dismountable graph, fully k-hop dismountable graph.

## Restless path

**Bibliography**

- [3] : Finding Temporal Paths Under Waiting Time Constraints (https://link.springer.com/article/10.1007/s00453-021-00831-w)
- [4] : Restless reachability problems in temporal graphs (https://arxiv.org/pdf/2010.08423v3)
    - p18, p20 algo
- [5] : Restless Temporal Path Parameterized Above Lower Bounds (https://arxiv.org/pdf/2203.15862)

**Content**

// Short restless path ?
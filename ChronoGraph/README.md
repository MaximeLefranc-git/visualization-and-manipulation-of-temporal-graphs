# Visualisation et manipulation de graphes temporels

## [Bonnes pratiques](https://realpython.com/python-menus-toolbars/#creating-menus-and-toolbars-best-practices-and-tips:~:text=raccourci%20clavier%20explicite.-,Cr%C3%A9ation,-de%20menus%20et) 

1. **Disposez vos menus dans l’ordre généralement accepté**. Par exemple, si vous disposez d’un menu Fichier , il doit s’agir du premier menu de gauche à droite. Si vous avez un menu Edition , ce devrait être le deuxième. L'aide doit être le menu le plus à droite, et ainsi de suite.

2. **Remplissez vos menus avec des options communes pour le type d'application que vous développez**. Par exemple, dans un éditeur de texte, les menus Fichier incluent généralement des options telles que Nouveau , Ouvrir , Enregistrer et Quitter . Les menus d'édition incluent souvent des options telles que Copier , Coller , Couper , Annuler , etc.

3. **Utilisez des raccourcis clavier standard pour les options courantes**. Par exemple, utilisez Ctrl+C pour Copier , Ctrl+V pour Coller , Ctrl+X pour Couper , etc.

4. **Utilisez des séparateurs pour séparer les options non liées.** Ces repères visuels faciliteront la navigation dans votre application.

5. **Ajoutez des points de suspension ( ...) au titre des options qui lancent des boîtes de dialogue supplémentaires.** Par exemple, utilisez Enregistrer sous… au lieu de Enregistrer sous , À propos de… au lieu de À propos , etc.

6. **Utilisez des esperluettes ( &) dans les options de votre menu pour fournir des accélérateurs de clavier pratiques.** Par exemple, "&Openau lieu de "Open", "&Exit"au lieu de "Exit".

## Features

**UI**

- Colored animations.
- Draggable graphics.
- Netgraph/NeworkX technology.

**Nodes**

- Add/Remove a node.
- Informations about the nodes.
    - Name, color, positions.
- Reset the colors.

**Edges**

- Add/Remove an edge.
- Informations about the edges.
    - Name, color, labels.
- Reset the colors

**File**

- **New** : Open a new project.
    - Ask to save before closing the previous one.
- **Open** : JSON format
- **Save** : JSON format.
- **Export** : PNG format.
- **Clear** : Clear the canva.
- **Exit** : Exit the app.

**Layout**

- **Random** : random positions
- **Circular** : regularly spaced on a circle
- **Spring** : force-directed layout (Fruchterman-Reingold algorithm)
- **Dot** :  Sugiyama algorithm
- **Radial** : radially using the Sugiyama algorithm

## MORE

- More formats to save/open files.
- More formats to export figure. More informations in the saved figure.
- More node layout : 
    - **community** : need to define which node is a member of which community.
    - **bipartite** : need to define which node is a member of which part.
    - **multipartite** : need to define which node is a member of which part.
    - **shell** : need to define shell informations.
    - **geometric** : need to define the "length of the edges".
- More customizable options.
    - node_shape, node_size, node_edge_width, edge_width, edge_layout, edge_label_position...
- Edge routing.
    Implements some methodes, add colored animations.
- More graph informations.
    - G.number_of_nodes, G.number_of_edges, G.adj[1], G.degree([2, 3])
- Complete Help part.
    - Create a tool documentation.
- Use graph operations/algorithms.
    - nx.shortest_path, subgraph, union, disjoint_union, cartesian_product, compose, complement, create_empty_copy, to_undirected, to_directed.
- Use algorithms of graphs creation.
    - petersen_graph, tutte_graph, sedgewick_maze_graph, tetrahedral_graph, complete_graph, complete_bipartite_graph, barbell_graph, lollipop_graph, 
erdos_renyi_graph, watts_strogatz_graph, barabasi_albert_graph, random_lobster
- Adapt TG2A method.
- Implement Timothée algorithm.
- Change UI.
    - Not python-like UI.

## Idea

1. **Weighted/Labeled**

Possible to imagine a weighted temporal graph.

**tool** : nx.Multigraph.

## Issues

1. **Resize du caneva $\rightarrow$ resize de la figure**  

**Problème** : Quand le caneva est resize manuellement, la taille de la figure ne suit pas.

**Solution** : TMP : Taille fixe, impossible de resize.

2. **Bordures noires lors d'un canva vide**

**Problème** : Quand le canva ne possède pas de nt.InteractiveGraph, des bordures noires apparaissent.

**Solution** : Purement esthétique. Changement de méthode de suppression. Axes de la figure configurés à non visibles.

3. **Desactiver l'ensemble des actions/boutons lors de l'attente d'un clic pour le drag&drop**

**Problème** : Actuellement, le drag&drop fonctionne de la manière suivante :
- On choisit le nom de l'état dans le champ de texte.
- On appuie sur le logo en forme d'état.
- On appuie sur le canva, cela génere un état a la position du clic.

Cependant, il faudrait "forcer" l'utilisateur a cliquer sur le canva après le clic sur le logo en forme d'états.

**Solution** : Désactivation de toutes les actions en attendant le clic d'un user.


## Of the week

**Tester clear avec de gros graphes** : DONE
    - Ne fonctionne pas : temps d'exécution trop long.
    - Lib/SDD pas optis.
    - Pas de graphes complets.
    - Peut être un sujet de bachelor/master a part -> lib c/c++.

**Drag and drop** :
    - Création d'états : DONE : Blocage des fonctionnalités en attendant le clic de l'user.
    - Editing mode : node/edge modification by a click.

**Plusieurs strings** : DONE
    - During an action that need labels -> function labelsToList
    - "12,17,100,1" or 12 -> [12, 17, 100, 1] or 12

**Ajouter des shortscuts** : DONE
    - Open : Ctrl+O
    - Save : Ctrl+S
    - New : Ctrl+N
    - Export : Ctrl+E
    - Delete : Del
    - ZoomIn : Ctrl++
    - ZoomOut : Ctrl+-
    - Drag a node : Ctrl+&
    - Drag an edge : Ctrl+é

**Case stricte/non stricte** : DONE
    - case cochable : variable qui change de valeur.

**Zoom in/Zoom out** : DONE

**Bouton "temporaly connected"** : DONE :
    - First idea :all_simple_edge_paths
        - restriction of cases : twice the same node not possible.
    - My own algorithm.
        - Finds paths if exists + condition on labels.
        - stricte/non-stricte case.

**Algorithmes temporels de bases** : DONE
    - Temporal path everybody to everybody : DONE
    - Temporal path beetween two nodes. : DONE


MORE :

Regrouper 

- disableAllActions et reableAllActions
- nodeLayout et changeColor et changeSize

Modifier les textes de prévisualisation.

IDEA : 

Bachelor/Master thesis -> Scalability of the sofware/TG2A method.

###################################################################
###################################################################

## Of the week

**moove the canva** : DONE : not perfect

**Path/temporal path : show it** : DONE

**Bi-path + icon** : DONE : for the moment, the TG2A method consider only strict case.

**use stack tracing** : DONE : traceback.print_stack()

**testing** : DONE : writes knowns and fixed bugs

**Set of examples graphs** : few graphs

**Temporal Dijkstra** : DONE

###################################################################
###################################################################

**Bugs resolus**
- Zoom quand il n'y a pas de figure.
- self.isWaitingClickTwoNodesPosition non reset après vouloir créer un edge dans une figure trop petite.
- Suppresion d'un edge allant de A-->A.
- Soucis du focus sur la zone texte : Focus principal sur le caneva.
- Creation d'un node hors canveva : position dynamique.

**More**
- Can choose a list a nodes/edges to change the colors : actually <node/edge> or "all"
- After the action to check the temporality connection : if the user change the color of the used path, it's not necesseraly true.
- Regrouper disableAllActions et reableAllActions | nodeLayout et changeColor et changeSize
- Organiser autrement/Regrouper isTemporalyConnected et temporal_dijkstra et bipath_dijkstra
- Modifier les textes de prévisualisation.
- Ajouter des textes dans les pop-ups.
- Color edge/node -> extand pattern + add resetAll to reset all the color

###################################################################
###################################################################

## Of the week

**Arbre temporel** : Algo temporal djisktra donne un arbre, le visualiser.

**Reset la couleur** : 
- Si on colore le graph et qu'on regarde si c'est temporaly connected, total reset : DONE
- Si on demande si A->C est TC, et que la reponse est oui, et qu'on redemande et que la réponse est non, A->C garde les couleurs : DONE

**TG2A non strict** : DONE

**Collections de graphes** :
- A-Z :
- ZOOM :
- MOOVE :
- EDITING MODE :
- TC :
- BPP :
- COLOR :
- LAYOUT :
- SPANNER :

**TC from everybody to everybody** : djisktra from everybody to everybody : DONE

**Temporal bi-path from everybody to everybody** : TG2A from everybody to everybody : DONE

**Minimal spanner** :
    - Try to remove one edge --> is the graph already TC ?

**More features on temporal paths (TC)** :
    - foremost :
    - shortest : in terms of number of nodes : 
    - fastest :

**Bugs**
- BPP strict : construction of A_t_s_time

###################################################################
###################################################################

docs : https://arxiv.org/abs/1404.7634

## Of the week

**Temporal graph on the tree** : DONE
    - Color the temporal paths used as the tree in the djikstra algorithm. : DONE
    - Color the labels used : Don't find a way with netgraph, no parameters for the colors of the edges labels

**Exemple spanner : cube à 8 vertices** : DONE
    - just need the differents labes on each edges.

**Shortest : Djisktra** : DONE
    - Voisins notés avec le nombre de hopes
    - On prend le guy with the min hope time from the root
    - queue FIFO

**Fastest : Djisktra** : DONE
    - Papier de 2003 : shortest fastest foremost : https://inria.hal.science/inria-00071996/file/RR-4589.pdf 
    - fastest = foremost from every temporal path

**Bpp automata** : DONE
    - Select only the shortest bipath, without enumerate all.

**Optimise spanner sans faire la liste de tous les edges**
    - Trouver le TC
    - See the paper https://arxiv.org/abs/1404.7634
    - improvement of my algo.
    - Not implement algo in the paper yet.

**Questions**

Arnaud :
    - Did you send the both formulas ?

###################################################################
###################################################################

## Of the week

**Fastest** : DONE
    - show the computation tree : 
        - overall minimize starting to source.
        - among the foremost, take one with the minimum duration.
    - Compute all the fastest : consider the far one

**find labels of the cube** : DONE

**Scalability** : DONE
    - test the features with a big graph.

**BPP** : DONE
    - show labels boths ways : DONE
    - error paths : 3 - 4 - 3 : DONE

**Implement TC** : DONE
    - Set of predecessors
    - paper : https://arxiv.org/abs/1404.7634

**Dismountability** : DONE
    - researchs :
        - Temporal cliques admit sparse spanners : https://www.sciencedirect.com/science/article/pii/S0022000021000428#se0110
    - related concepts :
        - delegation
    - implement : delegation, vertex/graph dismountability DONE

**Restless paths** : DONE
    - papers ?
    - researchs ?

**Bibliography** : DONE
    - walk, paths, ..., restless ?

###################################################################
###################################################################

## Of the week

**Fastest** : DONE
    - one of the foremost among one of starting time
    - Last person in term of duration -> duration of a tree
    - among all starting time, take the min foremost duration tree

solution : 
    - compute foremost tree for every starting time
    - Store the last person in terms of duration for each foremost duration tree
    - Store in global the min one

**foremost_lvl_2, test fastest** : DONE

**Bug** : DONE
    - Not reset the color after a possible a->b path

**Change size of labels** : DONE
    - edge_label_fontdict=dict(fontweight='bold', color='red')..
    - adapt all the instances
    - can change size, colors...
    - https://matplotlib.org/stable/api/text_api.html 

**Implementation of Arnaud** : DONE
    - Use the bitset format
    - 0 and 1
    - Union = boolean OR
    - Compare with set and Union
solution : Not better in my case, maybe need some optimisations

**Include the last edge in spanner** : DONE

**Dismountable** : DONE
    - spanner case : wich vertexs is dismoutable at each step ? DONE
    - Corresponding edges in the two first case : DONE

**Co-author of Arnaud**: DONE
    - simple algo for restless
    - https://appliednetsci.springeropen.com/articles/10.1007/s41109-020-00311-0 p13
    - Maybe an error in table 1 ?

**Exemple of Walk** : DONE
    - .-2-->.-4-->.-6-->.-14-->.-16-->.-18-->.
    -                  / \
    -               12/   \8
    -                /     \
    -                ---10----
    - There is a restless walk with delta=2 but no restless path

**Write-up**
    - Continue
    - Show

**Make a lib**:
    - https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f
    - Choses intéréssantes a mettre dedans.
    
**Bugs** :
    - Lifetime not update after a modification

###################################################################
###################################################################

## Of the week

**Show the restless path**: DONE
    - Use parts of algo + greedy method to find paths
    - not usable with big graphs.

**Bitsets version**: DONE
    - Not interesting
    - 2 versions with bitsets --> union of set is better
    - Maybe bitsets is more efficient with big graph.


###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################

Relecture du rapport : 
    - Completer les TBC :
        - Page 1 : date de soutenance, jury
        - Page academic context : date de fin
        - CTRL+f les TBC
    - A mettre :
        - Pas focus sur la performance, plutot sur la curiosité.
    - Completer les produits finaux dans 'My contribution'
    - Faire un github open-source, ajouter les links CTRL+F github                                    
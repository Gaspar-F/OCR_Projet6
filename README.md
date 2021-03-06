# OCR_Projet6
# Objet :
automatisation de tâches : Configuration switchs

## Présentation
Ce script a pour objectif de permettre l'automatisation de la configuration de switchs Cisco via l'envoi de commande en ssh. 
Le script a été validé avec des switchs Cisco 3725. L'environnement d'exécution du switch doit être réalisé sur un poste disposant du système d'exploitation windows 10.

Le script permet de renommer les switchs présents sur le réseau, de créer des Vlans, d'attribuer des interfaces aux Vlans et de sauvegarder ou restaurer les switchs depuis un serveur tftp ( ici hébergé sur le poste windows 10).

L'interface est basée  sur la bibliothèque d'interface graphique Tkinter.
La communication ssh vers les switchs est basée sur la libriarie Python multivendeur Netmiko. 

Les switchs sont au préalables configurés manuellement afin que les mots de passes soient cryptés et un Vlan 99 pour l'administration est configuré sur diverses interfaces. 

Le schéma joint à ce projet explique la situation de départ. ![schéma de connexion des appareils](https://github.com/Gaspar-F/OCR_Projet6/blob/8ba6dc6640e28c43af0378ffb7119067c0fe7692/Images/Schema%20de%20situation.png)

## Fonctionnement
Au lancement de l'application, il faut entrer le nom et le mot de passe de l'utilisateur défini dans la configuration des switchs.Il est également demandé de fournir le mot de passe secret pour accéder au mode privilégié.

 ![Fenêtre accueil](https://github.com/Gaspar-F/OCR_Projet6/blob/628589a409c0133c420df154063fb94c4c54fd4e/Images/Fen%C3%AAtre%20accueil.png)

Différents menus sont accessibles:

### Configuration : 
Là, nous pourrons choisir de Renommer le switch, de créer de nouveaux Vlans ou de gérer les Interfaces.

![Menu Configuration](https://github.com/Gaspar-F/OCR_Projet6/blob/628589a409c0133c420df154063fb94c4c54fd4e/Images/Menu%20Configuration.png)

#### Renommer
Cette vue permet de comprendre qu'il faut choisir un switch via son IP ( ici nous en avons 3) et indiquer un nouveau nom. On effectue l'opération avec le bouton "Valider". On peut également effacer cette fenêtre avec le bouton "Quit"

![Renommer](https://github.com/Gaspar-F/OCR_Projet6/blob/744135750da4c380849b44fb85c3f6da18383cad/Images/Renommer.png)

#### Vlan
Cette vue permet la gestion des Vlans. Comme pour la fenêtre précédente, on choisit un switch. 
![Vlan_accueil](https://github.com/Gaspar-F/OCR_Projet6/blob/628589a409c0133c420df154063fb94c4c54fd4e/Images/Vlan_accueil.png)

La validation du choix ouvre un widget treeview qui liste les Vlans existants pour le switch sélectionnés.
Il suffit alors d'indiquer un numéro de Vlan et le nom pour créer un nouveau Vlan dans le switch par l'intermédiaire du bouton "Créer Vlan"
![Vlan](https://github.com/Gaspar-F/OCR_Projet6/blob/628589a409c0133c420df154063fb94c4c54fd4e/Images/Vlan.png)

On peut vérifier la création du Vlan en sélectionnant à nouveau le switch.
![Vlan créé](https://github.com/Gaspar-F/OCR_Projet6/blob/628589a409c0133c420df154063fb94c4c54fd4e/Images/Vlan%20cr%C3%A9%C3%A9.png)

#### Interfaces
Tout comme pour le menu Vlan, on choisit le switch sur lequel on veut travailler. Ce choix permet d'ouvrir le treeview qui liste les Vlans du switch et fait apparaitre une combobox qui permet de lister les interfaces du switch.

On affecte ensuite l'interface au Vlan à l'aide du bouton "Affecter Interface au Vlan"


### Sauvegarde/Restauration:
Ce menu permettra de faire la sauvegarde du switch et éventuellement une restauration.

![Menu Sauvegarde_Restauration](https://github.com/Gaspar-F/OCR_Projet6/blob/628589a409c0133c420df154063fb94c4c54fd4e/Images/Menu%20Sauvegarde_Restauration.png)

#### Sauvegarde
Il suffit de choisir le switch et à l'aide du bouton "Valider", une sauvegarde sur un serveur externe est effectuée. Ici, le serveur est le poste Windows 10 sur lequel on lance le sript. La sauvegarde est automatiquement copiée dans le dossier portant le nom de l'adrresse IP du switch. Cette opération sauvegarde le running-config et le fichier Vlan.dat qui est sur la mémoire flash du switch.
![Sauvegarde](https://github.com/Gaspar-F/OCR_Projet6/blob/551b537f50b62b628c260725658882add3c15376/Images/Sauvegarde.png)

On remarque également un bouton "Enregistrer la configuration actuelle pour le prochain démarrage". Celui ci permet de copier le running-config dans le startup-config afin que les modifications en cours soient enregistrées au prochain démarrage du switch.

#### Restauration
Tout comme pour la sauvegarde, on choisit le switch.

![Restauration accueil](https://github.com/Gaspar-F/OCR_Projet6/blob/551b537f50b62b628c260725658882add3c15376/Images/Restauration%20accueil.png)

Les boutons "Sélection fichier Running-Config" et "Sélection du fichier Vlan" permettent d'ouvrir une fenêtre d'explorateur Windows afin de sélectionner le fichier à restaurer. 

![Selection fichier running-config](https://github.com/Gaspar-F/OCR_Projet6/blob/551b537f50b62b628c260725658882add3c15376/Images/Selection%20fichier%20running-config.png)

Les boutons "Restaure Running-config" et "Restaure Vlan" permettent l'exécution de la restauration.


# Licence
Ce script est soumis à la licence jointe(GNU General Public License v3.0 )

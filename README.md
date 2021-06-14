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

Le schéma joint à ce projet explique la situation de départ. ![schéma de connexion des appareils](https://user-images.githubusercontent.com/82892277/121871526-82071e80-cd04-11eb-92c1-64c478aee1d8.png)

## Fonctionnement
Au lancement de l'application, il faut entrer le nom et le mot de passe de l'utilisateur défini dans la configuration des switchs.Il est également demandé de fournir le mot de passe secret pour accéder au mode privilégié. ![Fenêtre accueil](https://user-images.githubusercontent.com/82892277/121875488-cd233080-cd08-11eb-8ee8-23b554190bab.png)


# Licence
Ce script est soumis à la licence jointe(GNU General Public License v3.0 )

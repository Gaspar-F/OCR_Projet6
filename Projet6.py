import tkinter as tk
from tkinter import  ttk, filedialog
import time,datetime
from getpass import getpass
from tkinter.constants import CENTER, E, END, LEFT, NO, W
from netmiko import Netmiko

# adresses IP des différents switchs
devices = ['192.168.1.203' , '192.168.1.204' , '192.168.1.205']
# définition des variables pour la connexion netmiko
device_type = 'cisco_ios'
username=input("Enter your SSH username:  ")
password=getpass("Entrez le mot de passe: ")
secret=getpass("Entrez le mot de passe privilège: ")

# Définition fenêtre principale Tkinter 
root = tk.Tk()
root.title("Projet 6")
root.geometry('600x400')
root.title('Gestion des switchs ')
root['bg'] = 'white'
root.resizable(height=False,width=False)
#création des fenêtres pour les sous-menus
win1=tk.Frame(root, width=580,height=350, background="bisque")
win2=tk.Frame(root, width=580,height=350, background="bisque")
win3=tk.Frame(root, width=580,height=350, background="bisque")
win4=tk.Frame(root, width=580,height=350, background="bisque")
win5=tk.Frame(root, width=580,height=350, background="bisque")

#fonction effacer les fenetres
def efface_widget_fenetre(fenetre):
    if fenetre =="win1":
        win1.place_forget()
        win1.update()
    elif fenetre =="win2":
        win2.place_forget()
        win2.update()
    elif fenetre =="win3":
        win3.place_forget()
        win3.update()
    elif fenetre =="win4":
        win4.place_forget()
        win4.update()
    elif fenetre =="win5":
        win5.place_forget()
        win5.update()

# fonction sauvegarder le switch sur serveur
def sauvegarde(combo):
    # récupération adresse IP
    ad_ip=combo.get()
    # connexion ssh switch
    net_connect = Netmiko(ip=ad_ip, device_type=device_type,username=username,password=password,secret=secret)
    net_connect.enable()
    # création du path avec adresse ip du switch
    path = 'c:/save_switch/' + ad_ip + '/'
    # récupération de la configuration du switch dans une variable et sauvegarde de cette configuration dans un fichier
    output1 = net_connect.send_command("show running-config")
    save_file = open(path + ad_ip + "_" + time.strftime('%Y_%m_%d_%H_%M')+".cfg","w")
    save_file.write(output1)
    save_file.close() 
    # Commande cisco permettant de sauvegarder vlan.dat sur le serveur tftp
    config_commands = 'copy flash:/vlan.dat tftp://192.168.1.202/' + ad_ip+'/vlan.dat_' + time.strftime('%Y_%m_%d_%H_%M')
    # la commande est envoyée sur le switch et attend le message 'Address or name of remote host'
    output = net_connect.send_command(
        config_commands,
        expect_string=r'Address or name of remote host'
    )
    # l'exécution de la commande se poursuit jusqu'au message 'Destination filename'
    output += net_connect.send_command(
        '\n',
        expect_string=r'Destination filename',
        # tempo qui permet l'écution de la touche entrée
        delay_factor=2 
    )
    #l'exécution se termine jusqu'au prompt
    output += net_connect.send_command(
        '\n',
        expect_string=r'#',
        delay_factor=2
    )
    net_connect.disconnect()

# fonction restaurer le switch ( running-config)
def restauration_config(combo,entry_fic):
    # récupération adresse IP
    ad_ip=combo.get()
    # création du path avec adresse ip du switch
    path = 'c:/save_switch/' + ad_ip + '/'
    #ouverture du fichier sélectionné et suppression des 3 premières lignes puis sauvegarde nouveau fichier fichier.cfg
    lines = None
    fichier=entry_fic.get()
    with open(fichier, 'r') as fichier :
        lines = fichier.readlines() 
        del lines[0:3]
    with open(path +'fichier.cfg', 'w') as nouveau_fichier:
        nouveau_fichier.write("\r\n".join(lines))
    fichier.close()
    # connexion ssh switch
    net_connect = Netmiko(ip=ad_ip, device_type=device_type,username=username,password=password,secret=secret)
    net_connect.enable()
    # Commande cisco permettant de restaure le nouveau fichier sur running-config
    config_commands = 'copy tftp://192.168.1.202/' + ad_ip+'/fichier.cfg running-config'
    # la commande est envoyée sur le switch et attend le message 'Destination filename'
    output = net_connect.send_command(
        config_commands,
        expect_string=r'Destination filename'
    )
    #l'exécution se termine jusqu'au prompt
    output += net_connect.send_command(
        '\n',
        expect_string=r'#',
        delay_factor=2
    )
    net_connect.disconnect()
    nouveau_fichier.close()

# fonction restaurer le switch ( Vlan)
def restauration_vlan(combo,entry_vlan):
    # récupération adresse IP
    ad_ip=combo.get()
    # on conserve que le nom du dossier et le nom du fichier du contenu du choix de fichier
    vlan=entry_vlan.get()
    vlan=vlan[14:]
    # création du path avec adresse ip du switch
    path = 'c:/save_switch/' + ad_ip + '/'
    # connexion ssh switch
    net_connect = Netmiko(ip=ad_ip, device_type=device_type,username=username,password=password,secret=secret)
    net_connect.enable()
    # Commande cisco permettant de restaurer vlan.dat sur le switch
    config_commands = 'copy tftp://192.168.1.202' + vlan + ' flash:vlan.dat' 
    # la commande est envoyée sur le switch et attend le message 'Destination filename'
    output = net_connect.send_command(
        config_commands,
        expect_string=r'Destination filename'
    )
    # la commande "entrée" est envoyée sur le switch et attend le message 'Do you want to over write'
    output += net_connect.send_command(
        '\n',
        expect_string=r'Do you want to over write'
    )
    # la commande "entrée" est envoyée sur le switch et attend le message 'Erase flash: before copying'
    output += net_connect.send_command(
        '\n',
        expect_string=r'Erase flash: before copying'
    )
     # la commande "entrée" est envoyée sur le switch et attend le message 'Erasing the flash filesystem will remove all files! Continue'
    output += net_connect.send_command(
        '\n',
        expect_string=r'Erasing the flash filesystem will remove all files! Continue'
    )
    #l'exécution se termine jusqu'au prompt
    output += net_connect.send_command(
        '\n',
        expect_string=r'#',
        delay_factor=2
    )
    net_connect.disconnect()
 
# fonction renommer le switch
def renomme_switch(wcombo_switch,wentry_nom):
    # récupération de l'adresse ip du switch
    ad_ip=wcombo_switch.get()
    # connexion au switch
    net_connect = Netmiko(ip=ad_ip, device_type=device_type,username=username,password=password,secret=secret)
    net_connect.enable()
    # envoi de la commande au switch
    config_commands = ['hostname ' + str(wentry_nom.get())]
    net_connect.send_config_set(config_commands)
    # déconnexion du switch
    net_connect.disconnect()
    
# fonction créer vlan
def creation_vlan(combo,num,nom):
    # récupération de l'adresse ip du switch
    ad_ip=combo.get()
     # connexion au switch
    net_connect = Netmiko(ip=ad_ip, device_type=device_type,username=username,password=password,secret=secret)
    net_connect.enable()
    # envoi des commandes au switch
    config_commands = [
        'Vlan ' + str(num.get()),
        'Name ' + str(nom.get()),
        'state active',
        'no shutdown'
        ]
    net_connect.send_config_set(config_commands)
    # déconnexion du switch
    net_connect.disconnect()
   
#fonction lister les Vlans du switch sélectionné
def liste_vlan(event,wcombo_switch):
    ad_ip=wcombo_switch.get()
    # connexion au switch
    net_connect = Netmiko(ip=ad_ip, device_type=device_type,username=username,password=password,secret=secret)
    net_connect.enable()
    # envoi de la commande d'affichage des vlans du switch et récupération sous forme de liste de dictionnaires
    vlans = net_connect.send_command('\nshow vlan-switch brief',use_textfsm=True)
     # déconnexion du switch
    net_connect.disconnect()
    # création du widget Treeview pour afficher les Vlans
    listvlan_multi = ttk.Treeview(win2, height=7)
    listvlan_scrollbar = ttk.Scrollbar(win2, orient="vertical", command=listvlan_multi.yview)
    listvlan_multi.place(x=15, y=100)
    listvlan_scrollbar.place(x=15+200+1,y=100,height=160+7)
    listvlan_multi.configure(yscrollcommand=listvlan_scrollbar.set)
    listvlan_multi['columns']=('Vlan_ID' , 'Name')
    listvlan_multi.column("#0",width=0, stretch=NO)
    listvlan_multi.column('Vlan_ID', anchor=CENTER, width=80)
    listvlan_multi.column('Name', anchor=CENTER, width=120)
    listvlan_multi.heading('#0', text='', anchor=CENTER)
    listvlan_multi.heading('Vlan_ID', text='Vlan_ID', anchor=CENTER)
    listvlan_multi.heading('Name', text='NOM', anchor=CENTER)
    #boucle pour remplir le treeview en parcourant la liste de dictionnaires
    i=0
    for vlan in vlans:
        if vlan['status'] == 'active':
            listvlan_multi.insert(parent='',index=i, iid=i, values=(vlan['vlan_id'],vlan['name'])),
            i=i+1
   
#fonction lister les Vlans et interfaces du switch sélectionné
def liste_interfaces_vlans(event,wcombo_switch):
    ad_ip=wcombo_switch.get()
    # connexion au switch
    net_connect = Netmiko(ip=ad_ip, device_type=device_type,username=username,password=password,secret=secret)
    net_connect.enable()
    # envoi de la commande d'affichage des vlans du switch et récupération sous forme de liste de dictionnaires
    vlans = net_connect.send_command('\nshow vlan-switch brief',use_textfsm=True)
    interfaces = net_connect.send_command('show ip int brief',use_textfsm=True)
     # déconnexion du switch
    net_connect.disconnect()
    # création du widget Treeview pour afficher les Vlans
    listvlan_multi = ttk.Treeview(win3, height=7)
    listvlan_scrollbar = ttk.Scrollbar(win3, orient="vertical", command=listvlan_multi.yview)
    listvlan_multi.place(x=15, y=100)
    listvlan_scrollbar.place(x=15+200+1,y=100,height=160+7)
    listvlan_multi.configure(yscrollcommand=listvlan_scrollbar.set)
    listvlan_multi['columns']=('Vlan_ID' , 'Name')
    listvlan_multi.column("#0",width=0, stretch=NO)
    listvlan_multi.column('Vlan_ID', anchor=CENTER, width=80)
    listvlan_multi.column('Name', anchor=CENTER, width=120)
    listvlan_multi.heading('#0', text='', anchor=CENTER)
    listvlan_multi.heading('Vlan_ID', text='Vlan_ID', anchor=CENTER)
    listvlan_multi.heading('Name', text='NOM', anchor=CENTER)
    #boucle pour remplir le treeview en parcourant la liste de dictionnaires
    i=0
    for vlan in vlans:
        if vlan['status'] == 'active':
            listvlan_multi.insert(parent='',index=i, iid=i, values=(vlan['vlan_id'],vlan['name'])),
            i=i+1
    # remplissage de la combobox des interfaces
    result = [i['intf'] for  i in interfaces if i['intf'] >= "FastEthernet" and i['intf'] < "Vlan" ]        
    listeinterface = ttk.Combobox(win3,values=result)
    listeinterface.place(x = 280, y = 100)
    # bouton lançant l'affectation de l'interface sélectionnée au vlan sélectionné
    btn_affect_vlan = tk.Button(win3, text = "Affecter interface au Vlan",command=lambda:affectation_vlan(ad_ip,listvlan_multi,listeinterface))
    btn_affect_vlan.place(x =300, y = 150)
    
# fonction associant une interface au vlan
def affectation_vlan(ad_ip,listvlan_multi,listeinterface):
    select_int=listeinterface.get()
    # focus permet d'isoler la selection du treeview 
    # item on récupère la valeur sous forme de dictionnaire
    # et on récupère la valeur de liste avec indice 0
    select_vlan=listvlan_multi.item(listvlan_multi.focus()).get("values")[0]
    # connexion au switch
    net_connect = Netmiko(ip=ad_ip, device_type=device_type,username=username,password=password,secret=secret)
    net_connect.enable()
    # envoi des commandes pour l'affectation d'une interface à un Vlan
    config_commands = [
        'Interface ' + select_int,
        'switchport mode access',
        'switchport access vlan '+ str (select_vlan),
        'no shutdown',
        'end'
        ]
    net_connect.send_config_set(config_commands)
     # déconnexion du switch
    net_connect.disconnect()

# fonction ouvrant un explorateur windows directement dans le dossier du switch 
def sélection_fichier(wcombo_switch,entry_fic):
    # effacement de l'Entry
    entry_fic.delete(0,END)
    # récupère l'adresse ip du switch pour ouvrir directement le dossier associé au switch
    ad_ip=wcombo_switch.get()
    path = 'c:/save_switch/' + ad_ip + '/' 
    #ouverture de l'explorateur permettant de sélectionner un fichier
    filename=filedialog.askopenfilename(initialdir = path)
    # remplissage de l'entry avec le nom du fichier sélectionné et son chemin
    entry_fic.insert(0,filename)

# fonction permettant de sauvegarde la configuration courante du switch dns le système de démarrage
def running_startup(wcombo_switch):
    ad_ip=wcombo_switch.get()
    # connexion au switch
    net_connect = Netmiko(ip=ad_ip, device_type=device_type,username=username,password=password,secret=secret)
    net_connect.enable()
    # envoi de la commande 
    config_commands = 'copy running-config startup-config'
    # la commande est envoyée sur le switch et attend le message 'Destination filename'
    output = net_connect.send_command(
        config_commands,
        expect_string=r'Destination filename'
    )
    #l'exécution se termine jusqu'au prompt
    output += net_connect.send_command(
        '\n',
        expect_string=r'#',
        delay_factor=2
    )
    net_connect.disconnect()

#Appel du menu
menu_principal = tk.Menu(root)

#déclaration des fonctions des commandes du menu
# fonction renommer switch
def renommer():
    # construction des éléments de la fenêtre
    win1.place(x=10 , y= 25)
    # variable permettant d'effacer la bonne fenêtre
    fenetre="win1"
    label_switch = tk.Label(win1, text = "Choix du switch: ")
    label_switch.place(x = 0, y = 10)
    combo_switch = ttk.Combobox(win1,values=devices)
    combo_switch.place(x = 120, y = 10)
    label_nom = tk.Label(win1, text = "Nouveau Nom: ")
    label_nom.place(x = 0, y = 100)
    entry_nom = tk.Entry(win1, bd = 5)
    entry_nom.place(x = 120, y =100)
    # bouton qui initie la commande renomme_switch avec 2 paramètres : le widget combo_switch et le widget entry_nom
    btn_valid = tk.Button(win1, text = "Valider",command=lambda:renomme_switch(combo_switch,entry_nom))
    btn_valid.place(x =300, y = 10)
    # bouton qui efface la fenêtre
    btn_quit = tk.Button(win1, text = "Quit",command=lambda:efface_widget_fenetre(fenetre))
    btn_quit.place(x =300, y = 50)

# fonction création des Vlans
def conf_Vlan():
    win2.place(x=10 , y= 25)
    # variable permettant d'effacer la bonne fenêtre
    fenetre = "win2"
    label_titre_fenetre = tk.Label(win2, text = "Création de Vlan(s): ")
    label_titre_fenetre.place(x = 230, y = 5)
    # fenêtre Creation Vlan
    label_switch = tk.Label(win2, text = "Choix du switch: ")
    label_switch.place(x = 120, y = 30)
    combo_switch = ttk.Combobox(win2,values=devices)
    combo_switch.place(x = 235, y = 30)
    # l'évènement sur la combobox déclenche l'appel de la fonction liste_vlan
    combo_switch.bind("<<ComboboxSelected>>",lambda event: liste_vlan(event,combo_switch))
    label_vlan_existant = tk.Label(win2, text = "Vlan(s) existant(s): ")
    label_vlan_existant.place(x = 15, y = 70)
    # on affiche les widgets permettant de renseigner les éléments du Vlan à créer
    label_titre = tk.Label(win2, text = "Renseignez les champs ci-dessous: ")
    label_titre.place(x = 280, y = 70)
    label_num_vlan = tk.Label(win2, text = "Numéro Vlan: ")
    label_num_vlan.place(x = 280, y = 100)
    entry_num_vlan = tk.Entry(win2, bd = 5)
    entry_num_vlan.place(x = 365, y =100)
    label_nom_vlan = tk.Label(win2, text = "Nom Vlan: ")
    label_nom_vlan.place(x = 280, y = 120)
    entry_nom_vlan = tk.Entry(win2, bd = 5)
    entry_nom_vlan.place(x = 365, y =120)
    # bouton qui initie l'appel de la fonction creation_vlan avec 3 paramètres : le widget combo_switch, le widget entry_num_vlan et le widget entry_nom_vlan
    btn_c_vlan = tk.Button(win2, text = "Créer Vlan",command=lambda:creation_vlan(combo_switch,entry_num_vlan,entry_nom_vlan))
    btn_c_vlan.place(x =300, y = 200)
    # bouton qui efface la fenêtre
    btn_quit = tk.Button(win2, text = "Quit",command=lambda:efface_widget_fenetre(fenetre))
    btn_quit.place(x =420, y = 200)  

# fonction gestion des interfaces
def conf_interface():
    win3.place(x=10 , y= 25)
    # variable permettant d'effacer la bonne fenêtre
    fenetre="win3"
    label_titre_fenetre = tk.Label(win3, text = "Paramétrage des interfaces: ")
    label_titre_fenetre.place(x = 230, y = 5)
    label_switch = tk.Label(win3, text = "Choix du switch: ")
    label_switch.place(x = 120, y = 30)
    combo_switch = ttk.Combobox(win3,values=devices)
    combo_switch.place(x = 235, y = 30)
    # une sélection dans la combobox initie la fonction liste_interfaces_vlans 
    combo_switch.bind("<<ComboboxSelected>>",lambda event:liste_interfaces_vlans(event,combo_switch))
    label_vlan_existant = tk.Label(win3, text = "Vlan(s) existant(s): ")
    label_vlan_existant.place(x = 15, y = 70)
    label__interface = tk.Label(win3, text = "Choix du l'interface: ")
    label__interface.place(x = 280, y = 70)
    # bouton qui efface la fenêtre
    btn_quit = tk.Button(win3, text = "Quit",command=lambda:efface_widget_fenetre(fenetre))
    btn_quit.place(x =420, y = 200)  
      
#fonction qui sauvegarde le switch
def sauvegarde_switch():
    win4.place(x=10 , y= 20)
    # variable permettant d'effacer la bonne fenêtre
    fenetre="win4"
    l1 = tk.Label(win4, text = "Choix du switch: ")
    l1.place(x = 0, y = 10)
    combo_switch = ttk.Combobox(win4,values=devices)
    combo_switch.current(0)
    combo_switch.place(x = 120, y = 10)
    # bouton qui initie l'appel de la fonction sauvegarde avec un paramètre d'entrée: le widget combo_switch
    btn = tk.Button(win4, text = "Valider",command=lambda:sauvegarde(combo_switch))
    btn.place(x =300, y = 10)
    # bouton qui initie l'appel de la fonction running_startup avec un paramètre d'entrée: le widget combo_switch
    label_running_startup=tk.Button(win4, text = "Enregistrer la configuration actuelle pour le prochaine démarrage", command= lambda: running_startup(combo_switch))
    label_running_startup.place(x=30, y=70)
    # bouton qui efface la fenêtre
    btn_quit = tk.Button(win4, text = "Quit",command=lambda:efface_widget_fenetre(fenetre))
    btn_quit.place(x =120, y = 150)

# fonction qui restaure le switch
def restaure_switch():
    win5.place(x=10 , y= 20)
    # variable permettant d'effacer la bonne fenêtre
    fenetre="win5"
    l1 = tk.Label(win5, text = "Choix du switch: ")
    l1.place(x = 0, y = 10)
    listecombo = ttk.Combobox(win5,values=devices)
    listecombo.current(0)
    listecombo.place(x = 120, y = 10)
    # bouton qui initie l'appel de la fonction sélection_fichier avec deux paramètres d'entrée: le widget combo_switch, et le widget entry_fichier
    btn_select_fichier=tk.Button(win5, text = " Sélection fichier Running-config", command= lambda:sélection_fichier(listecombo,entry_fichier))
    btn_select_fichier.place(x=50, y=70)
    entry_fichier = tk.Entry(win5, bd = 5)
    entry_fichier.place(x = 50, y =100)
    # bouton qui initie l'appel de la fonction sélection_fichier avec deux paramètres d'entrée: le widget combo_switch, et le widget entry_vlan
    btn_select_fichier_vlan=tk.Button(win5, text = " Sélection du fichier Vlan", command= lambda:sélection_fichier(listecombo,entry_vlan))
    btn_select_fichier_vlan.place(x=300, y=70)
    entry_vlan = tk.Entry(win5, bd = 5)
    entry_vlan.place(x = 300, y =100)
    # bouton qui initie l'appel de la fonction restauration_config avec deux paramètres d'entrée: le widget combo_switch, et le widget entry_fichier
    btn_restaure_running=tk.Button(win5, text = " Restaure running-config", command= lambda:restauration_config(listecombo,entry_fichier))
    btn_restaure_running.place(x=50, y=130)
    # bouton qui initie l'appel de la fonction restauration_vlan avec deux paramètres d'entrée: le widget combo_switch, et le widget entry_vlan
    btn_restaure_vlan=tk.Button(win5, text = " Restaure Vlan", command= lambda:restauration_vlan(listecombo,entry_vlan))
    btn_restaure_vlan.place(x=300, y=130)
    # bouton qui efface la fenêtre
    btn_quit = tk.Button(win5, text = "Quit",command=lambda:efface_widget_fenetre(fenetre))
    btn_quit.place(x =300, y = 200)

#déclaration des sous menus
#Sous menu Renommer
configuration = tk.Menu(menu_principal,tearoff=0)
configuration.add_command(label= "Renommer", command=renommer)
configuration.add_command(label= "Vlan", command=conf_Vlan)
configuration.add_command(label= "Interfaces", command=conf_interface)
#Sous-menu Sauvegarde/Restauration
save_rest = tk.Menu(menu_principal,tearoff=0)
save_rest.add_command(label="Sauvegarde", command=sauvegarde_switch)
save_rest.add_command(label ="Restauration", command=restaure_switch)
#construction du menu
menu_principal.add_cascade(label="Configuration",menu=configuration)
menu_principal.add_cascade(label="Sauvegarde/restauration",menu=save_rest)
#affichage du menu
root.config(menu=menu_principal)

root.mainloop()

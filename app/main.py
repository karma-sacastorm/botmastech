from flask import Flask, request
from pymessenger.bot import Bot
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib,ssl
import random
global n_demand, to_be_sent_admins,prim_demand
from unicodedata import normalize


#data
type_voie_ss_accent=['abbaye', 'agglomeration', 'aire', 'aires', 'allee', 'allees', 'ancien chemin', 'ancienne route', 'anciennes routes', 'anciens chemins', 'anse', 'arcade', 'arcades', 'autoroute', 'avenue', 'barriere', 'barrieres', 'bas chemin', 'bastide', 'bastion', 'beguinage', 'beguinages', 'berge', 'berges', 'bois', 'boucle', 'boulevard', 'bourg', 'butte', 'cale', 'camp', 'campagne', 'camping', 'carre', 'carreau', 'carrefour', 'carriere', 'carrieres', 'castel', 'cavee', 'central', 'centre', 'centre commercial', 'chalet', 'chapelle', 'charmille', 'chateau', 'chaussee', 'chaussees', 'chemin', 'chemin vicinal', 'cheminement', 'cheminements', 'chemins', 'chemins vicinaux', 'chez', 'cite', 'cites', 'cloitre', 'clos', 'col', 'colline', 'collines', 'contour', 'corniche', 'corniches', 'cote', 'coteau', 'cottage', 'cottages', 'cour', 'cours', 'darse', 'degre', 'degres', 'descente', 'descentes', 'digue', 'digues', 'domaine', 'domaines', 'ecluse', 'ecluses', 'eglise', 'enceinte', 'enclave', 'enclos', 'escalier', 'escaliers', 'espace', 'esplanade', 'esplanades', 'etang', 'faubourg', 'ferme', 'fermes', 'fontaine', 'fort', 'forum', 'fosse', 'fosses', 'foyer', 'galerie', 'galeries', 'gare', 'garenne', 'grand boulevard', 'grand ensemble', 'grand rue', 'grande rue', 'grandes rues', 'grands ensembles', 'grille', 'grimpette', 'groupe', 'groupement', 'groupes', 'halle', 'halles', 'hameau', 'hameaux', 'haut chemin', 'hauts chemins', 'hippodrome', 'hlm', 'ile', 'immeuble', 'immeubles', 'impasse', 'impasses', 'jardin', 'jardins', 'jetee', 'jetees', 'levee', 'lieu dit', 'lotissement', 'lotissements', 'mail', 'maison forestiere', 'manoir', 'marche', 'marches', 'mas', 'metro', 'montee', 'montees', 'moulin', 'moulins', 'musee', 'nouvelle route', 'palais', 'parc', 'parcs', 'parking', 'parvis', 'passage', 'passage a niveau', 'passe', 'passerelle', 'passerelles', 'passes', 'patio', 'pavillon', 'pavillons', 'peripherique', 'peristyle', 'petit chemin', 'petite allee', 'petite avenue', 'petite impasse', 'petite route', 'petite rue', 'petites allees', 'place', 'placis', 'plage', 'plages', 'plaine', 'plan', 'plateau', 'plateaux', 'pointe', 'pont', 'ponts', 'porche', 'port', 'porte', 'portique', 'portiques', 'poterne', 'pourtour', 'pre', "presqu'ile", 'promenade', 'quai', 'quartier', 'raccourci', 'raidillon', 'rampe', 'rempart', 'residence', 'residences', 'roc', 'rocade', 'rond point', 'roquet', 'rotonde', 'route', 'routes', 'rue', 'ruelle', 'ruelles', 'rues', 'sente', 'sentes', 'sentier', 'sentiers', 'square', 'stade', 'station', 'terrain', 'terrasse', 'terrasses', 'terre plein', 'tertre', 'tertres', 'tour', 'traverse', 'val', 'vallee', 'vallon', 'venelle', 'venelles', 'via', 'vieille route', 'vieux chemin', 'villa', 'village', 'villages', 'villas', 'voie', 'voies', 'zone', 'zone industrielle', 'zone a urbaniser en priorite', 'zone artisanale', "zone d'activite", "zone d'amenagement concerte", "zone d'amenagement differe"]


allo_response="que voulez vous"

liste_allo="Voici la liste des allos que nous proposons:\n\n-beton pong\n-masque\n-ménage\n-14\n-Koe\n-fusée\n-surprise\n-destination Rio\n-capote\n-massage\n-cuistot\n-destination Dunkerque"


def remove_accent(text):
    return normalize('NFKD',text).encode('ascii','ignore').decode('utf-8')



def demande_adresse(response):
    if response in ["quelque part","'quelque part'"]:
        return True
    WORDS=response.split(" ")
    words=[]
    for WORD in WORDS:
        numero=False
        word=remove_accent(WORD.lower())
        words.append(word)
    for word in words:
        if word in type_voie_ss_accent:
            return True
    
    return False    
        

def demande(response):
    if response in ["non","'non'","NON","'NON'","Non","'Non'"]:
        return False
    return True

def confirm(response):
    if response in ["oui","'oui'","OUI","'OUI'","Oui","'Oui'"]:
        return True
    return False











#infos smtp
smtp_adress = 'smtp.gmail.com'
smtp_port = 465

#infos sur l'envoyeur

email_adress = "jean.botmastec@gmail.com"
email_password = "V1V&_l4frique"

#infos sur le destinataire

email_reciever = "balmastech.allo@gmail.com"





n_demand=-1
to_be_sent_admins=""
prim_demand=True


app = Flask(__name__)
ACCESS_TOKEN= "EAAMWT1WPJMUBAIBMVv60g5r5OmqZCz7PZBQfNL9z1SXrUOug59yeuyRSkJl63O6dV8mmGaZAZB6eym4qMMuDj7BGnKAKHTQRCgmlw6JQAJ5xpZAACZAcEfP4sQopgcubw2uBgzbvMpKrshLWEhUdnEHLl8xzdc0Gx0D7sSAdGICpFZAWIbVT44K"
VERIFY_TOKEN= "Czcklfxv3d8acq76"
bot=Bot(ACCESS_TOKEN)

@app.route('/', methods=['GET','POST'])

def receive_message():
    global n_demand
    if request.method=='GET':
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)

    else:

        output = request.get_json()
    
        event=output['entry'][0]['messaging']
        
        for message in event:
            if message.get('message'):
                
                recipient_id = message['sender']['id']
                
                if message['message'].get('text'):
                    n_demand+=1
                    response_sent_text = message['message']['text']
                    send_message(recipient_id, response_sent_text)
                if message['message'].get('attachments'):
                    n_demand+=1
                    response_sent_nontext="null"
                    send_message(recipient_id,response_sent_nontext)
    return 'Message Processed'

def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'

                        
#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    global n_demand, to_be_sent_admins,prim_demand
    if n_demand==0:
        to_be_sent_admins=""
        if response in ["Allo","ALLO","allo"]:
            bot.send_text_message(recipient_id,liste_allo)
            bot.send_text_message(recipient_id,allo_response)
            prim_demand=True
        elif response=="null":
            n_demand=-1
            bot.send_text_message(recipient_id,"soyez gentils avec moi, je ne comprends que le texte pour l'instant")
        else:
            n_demand=-1
            bot.send_text_message(recipient_id, "un plaisir de vous avoir avec nous")
        

    elif n_demand==1:
        if prim_demand:
            to_be_sent_admins+="\n--->Demandes: "
        to_be_sent_admins+=""" " """+response+""" "; """
        bot.send_text_message(recipient_id,"Autre chose? (tapez 'non' pour quitter)")
    elif n_demand==2:
        if demande(response):
            n_demand=1
            prim_demand=False
            send_message(recipient_id, response)
        else:
            bot.send_text_message(recipient_id,"""A quelle adresse devons nous nous rendre ? (si vous ne vous trouvez pas à une adresse précise, saisissez: 'quelque part' et nous vous appelerons pour savoir""")
    elif n_demand==3:
        if response=="null":
            n_demand-=1
            bot.send_text_message(recipient_id,"soyez gentils avec moi, je ne comprends que le texte pour l'instant")
        else:
            if demande_adresse(response):
                bot.send_text_message(recipient_id,"veuillez renseignez votre numéro de téléphone (essayez de mettre un numéro valide svp)")
                to_be_sent_admins+="\n--->Adresse: "+response
            else:
                bot.send_text_message(recipient_id,"Il semblerait que je n'aie pas compris ou que vous n'ayez pas saisi une adresse valide, veuillez répeter")
                n_demand-=1

    #elif n_demand==2:
     #   if prim_demand:
      #      to_be_sent_admins+="\n--->Demandes: "
       # to_be_sent_admins+=""" " """+response+""" "; """
        #bot.send_text_message(recipient_id,"Autre chose? (tapez 'non' pour quitter)")
    #elif n_demand==3:
     #   if allo.demande(response):
      #      n_demand=2
       #     prim_demand=False
        #    send_message(recipient_id, response)
        #else:
         #   bot.send_text_message(recipient_id,"veuillez renseignez votre numéro de téléphone (essayez de mettre un numéro valide svp)")
            
    elif n_demand==4:
        to_be_sent_admins+="\n--->Numero de téléphone: "+response
        bot.send_text_message(recipient_id,"Votre demande d'allo:\n\n"+to_be_sent_admins+"\n\n Confirmer vous? (tapez: 'oui', toute autre réponse annulera la demande)")
    elif n_demand==5:
        n_demand=-1
        #l'utilisateur a confirmé la requête et le bot notifie l'admin par mail
        if confirm(response):
            bot.send_text_message(recipient_id,"Demande confirmée, nous arrivons au plus vite")
            #création de la connexion email


            #creation du message
            message = MIMEMultipart("alternative")

            #infos smtp
            smtp_address = 'smtp.gmail.com'
            smtp_port = 465

            #infos sur l'envoyeur

            email_address = "jean.botmastec@gmail.com"
            email_password = "V1V&_l4frique"
            message["From"] = email_adress
            #infos sur le destinataire

            email_receiver = "balmastech.allo@gmail.com"
            message["To"] =email_receiver
            message["Subject"] = "Demande d'ALLO n°"+str(random.randint(0,99999))



            
            texte=to_be_sent_admins

            html="""
            <html>
            <body>
            <p>{0}</p>
            </body>
            </html>""".format(to_be_sent_admins)






            # on crée deux éléments MIMEText 
            texte_mime = MIMEText(texte, 'plain')
            html_mime = MIMEText(html, 'html')

            # on attache ces deux éléments 
            message.attach(texte_mime)
            message.attach(html_mime)



            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
                #connexion au mail envoyeur
                server.login(email_address, email_password)
                #envoi du mail
                server.sendmail(email_address, email_receiver, message.as_string())
                
        else:
            bot.send_text_message(recipient_id,"Demande annulée")
        
    return "Success"             
        


"""
Configuration des variables pour l'envoi des emails.

MAIL_USER : nom de l'adresse mail qui va envoyer les emails.
MAIL_Recipient : nom de l'adresse mail qui va recevoir les emails.
MAIL_PASS : mot de passe de l'adresse mail du MAIL_USER
SMTP_SERVER : adresse internet du serveur SMTP de l'adresse mail du MAIL_USER
SMTP_PORT : port du serveur SMTP de l'adresse mail du MAIL_USER
"""
MAIL_USER = 'ow-rpi@gmx.fr'
MAIL_RECIPIENT ='archein.lol@gmail.com'
MAIL_PASS = 'Password1'
SMTP_SERVER = 'mail.gmx.com'
SMTP_PORT = 587


"""
Configuration des variables pour le serveur BROKER MQTT

BROKER : adresse IP du serveur BROKER MQTT
BROKER_PORT : Port du serveur BROKER MQTT
BROKER_KEEPALIVE : Temps durant laquelle la connexion est maintenue sans transmission de données.
"""

BROKER = "130.104.78.204"
BROKER_PORT = 1883
BROKER_KEEPALIVE = 300



TIMESTEP = 300

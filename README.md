# SpeedCraft

Speedcraft est un challenge de type CTF. Il s'agit d'une machine vulnérable et exposée sur le réseau. L'objectif est de devenir administrateur (root) sur la machine.

# Prérequis

- Une machine virtuelle sous n'importe quelle distribution stable avec `docker`, `docker-compose`, et `git`.
- De la motivation !

# Scénario

Un de vos amis a pris une bonne résolution cette année : il compte terminer Minecraft le plus rapidement possible ! 

Pour se compliquer la tâche, il a mis en place un serveur qui permet d'intéragir avec lui, moyennant finance (il n'y a pas de petits profits)

# Lancement du serveur

Configurez le réseau de la machine virtuelle de manière à ce qu'elle soit accessible à votre machine de pentest, et qu'elle ait accès à internet.

Sur la machine virtuelle :
`git clone https://github.com/MatthisC/ctf-speedcraft.git`
`cd ctf-speedcraft`
`docker-compose build`
`docker-compose up`

En cas de crash de la machine (peut arriver suivant ce que vous tentez de faire dessus), relancer là en faisant :
`docker-compose down`
`docker-compose up`
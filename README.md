Holy ZIP Cracker

This script attempt to crack a protected zip file

Python 3 compatible

Command line example : 
python src/zipcracker.py data/FAUXZIP.zip data/dictionnary-test.txt




Prepared Holy bible (use regexs starting from base.txt):

"\n\*\*\*\*\*\*ebook converter DEMO Watermarks\*\*\*\*\*\*\*" >  ""  : suppression fin de pages demo
"\[\*\]"  >   ""  : suppression des [*]
"^ +"  >  "" : #suppression des espaces en début de ligne
"([.!?:;]) (\d{1,4} [A-Z].*)\n" >  "$1\n$2 "  : #mettre débuts de versets en début de ligne
"([.!?:;]) (\d{1,4} [A-Z].*)\n"  > "$1\n$2 " #Idem que dessus, si 2 versets etaient sur la même ligne
... (à répéter autant de fois qu'il le faut, avec la casse, puis finir à la main ?)
"^\d{1,3} ([A-Z]|[a-z]|“)"   >  "$1"     #suppression des débuts de versets en enlevant le nombre et les espaces
"([a-z]|,)\n([a-z])" > "$1 $2" supprimer retour à la ligne lorsqu'en milieu de phrase (ou après virgule uniquement)
",? ?(\. ?){3}"  >  " "  #remplacement des petits points : . . . , ou , . . .  par un espace
"([\.!?]) " > "$1\n"   #Retour à la ligne pour chaque point/exclamation/interrogation qui ne retourne pas déjà à la ligne

#TODO: chaque ligne est séparée par des ,?;:.!. Est-ce qu'on sépare en chaque ligne, ou est-ce qu'on les cumule dans le script ?
"[:;,] " > "\n"   #Retour à la ligne pour chaque caractère spécial qui ne retourne pas déjà à la ligne
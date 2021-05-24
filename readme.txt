Pour set un environnement virtuel: 
"python3 -m venv .venv " (créer un environnement virtuel local)

"Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process"
".\.venv\Scripts\activate" (permet de rentrer dans le venv pour y installer
des packages)
"deactivate" (permet de sortir du venv)

gcc src/unpack2.c  src/main.c -o ./unpack_csv -lws2_32
(compiler unpack_csv,-lws2_32 à utiliser sous windows uniquement)

nb: ne pas oublier de changer le type dans les "fprint" du code c

faire 1 dossier data, un dossier machine learning(ml), un dossier ingest
(avec le sem1_bin_csv et le script python pour dl les données)

normalize then resample time looks better
(mieux centrer, prend mieux en charge les valeurs set a 0.01)
ie: valeur <0 sont toutes set > 0. dans lautre cas, une valeur peut changer de signe
 pendant le resample avant le normalize.

very important: 

never try to modify a dataframe with chain indexing.
if u want to modify a df, use only one getter (ie [], loc, iloc) then set
if u want to work on a subset of the dataframe and modify it, make a copy before
in order to not modify df (then rule 1 apply again)
are u making an assignement to a subset or the actual dataframe?
nb: i have read information about boxes and memory, wich should not be memorize

def fyear2datetime(year):
  iyear = int(year)
  y = datetime(iyear,1,1)
  yn = datetime(iyear+1,1,1)
  dt = yn-y
  return y + (year-iyear)*dt


  demain : mettre en forme l'input (48,4021,3)
  ecrire un train loader, val loader. 
  faire tourner le modele relu
  computer une donnée(voir l'erreur)

  se renseigner sur svm
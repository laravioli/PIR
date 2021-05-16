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
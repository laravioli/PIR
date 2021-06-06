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

 hparamsn = [1, 2, 3, 4, ...]

# Prepare the Grid
param_grid = dict(hparams1=hparams1, 
                  hparams2=hparams2, 
                  ...
                  hparamsn=hparamsn)

# GridSearch in action
grid = GridSearchCV(estimator=model, 
                    param_grid=param_grid, 
                    n_jobs=, 
                    cv=,
                    verbose=)
grid_result = grid.fit(x, y)

# Show the results
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param)



preprocessing: 
je fit l'input avec minmax, plus besoin d'y toucher
je fit l'output:
1) minmax, seule l'echelle est changer, refit l'echelle avec le scaler du training(+val)
2)log puis minmax, refit avec lechelle du training puis 10**y

comment est calculer l'erreur ?
sample par sample, en appliquant des poids aux output, puis en prenant la moyenne
sur le vecteur output. par default, poids uniforme (donc on fait la moyenne sur les outputs)
sklearn: multioutput= "raw_values", permet d'avoir la metric output par output

04/06 nb : penser à éventuellement changer les valeurs df_pred qui ont été modifier pour log
nb: inclure les données de test dans le scaling ne change pas le scaling du train
car le train a des valeurs max plus élevés. mais faire attention pour des périodes plus vieille
de test

06/06 retravailler les fonctions de dimensionnement pour cnn_v2, essayer d'augmenter le fenetre temporelle
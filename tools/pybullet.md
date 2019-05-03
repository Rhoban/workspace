# Utilisation de pybind et de pyBullet

## 1) Créer un virtualenv python3:

  python3 -m virtualenv python3

## 2) Toujours être dans le virtualenv

En mettant par exemple:

  source $HOME/python3/bin/activate

Dans le `.bashrc` par exemple. Ne pas oublier de relancer bash après.

## 3) Installer catkin et pybullet dans le virtualenv

  pip install -U catkin_tools mock empy pybullet numpy

## 5) Cloner le dépôt sigmaban_pybullet

  git clone git@github.com:rhoban/sigmaban_pybullet.git

## 6) Ajouter `workspace/bin` et `sigmaban_pybullet` les dossiers dans le `PYTHONPATH`

En ajoutant par exemple dans le `.bashrc`:

export PYTHONPATH="$PYTHONPATH:$HOME/workspace/bin:$HOME/sigmaban_pybullet/"

## 7) Compiler le code

En mettant la variable `KID_SIZE_PYTHON_BINDING` à `ON`. Ca peut par exemple être
fait dans `build_release/kid_size/CMakeCache.txt`.

## 8) Lancer!

Il suffit de lancer `run.py` qui est dans `env/fake`
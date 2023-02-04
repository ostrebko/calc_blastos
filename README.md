# Detection of blastospores in photographs with YOLOv5

## Contents

* [Introduction](README.md#Introduction)
* [Project structure](README.md#Project-structure)
* [Data and methods](README.md#Data-and-methods)
* [Activation the virtual environment](README.md#Activation-env)
* [Installation](README.md#Installation)
* [Docker](README.md#Docker)
* [Create .exe](README.md#Create-exe)
* [Inference](README.md#Inference)
* [Experimental data analysis](README.md#Experimental-data-analysis)
* [Machine learning models structure](README.md#Machine-learning-models-structure)
* [Experiment logging](README.md#Experiment-logging)
* [Conclusion](README.md#Conclusion)


## Introduction

Entomopathogenic fungus Beauveria bassiana is a promising basis for biological insecticides for use in crop production. Its ability to cause a deadly infectious process in a wide range of insect pest species makes it possible to create biological preparations based on strains of this species that are not inferior in effectiveness to a significant number of modern chemical insecticides. In addition, biologics based on B. bassiana has a number of advantages over chemical analogues – they are much safer for humans, plants and other environmental objects, have a lower cost, and also often provide a longer protective effect, due to the ability to cause epidemics in insect populations with a high number of individuals (overpopulated populations).  

<p align="center"> 
<img
  src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Beauveria.jpg"
  alt="Grasshoppers (Melanoplus sp.) killed by the fungus Beauveria bassiana (from wikipedia.org)"
  title="Grasshoppers (Melanoplus sp.) killed by the fungus Beauveria bassiana (from wikipedia.org)"
  style="display: inline-block; margin: 0 auto; max-width: 300px">
</p>

The most important characteristic of a biopreparation based on an a priori effective strain of entomopathogen is the number of viable cells/mycelium particles/fungal spores per unit volume or mass of the preparation. This indicator is often determined both in the process of developing a biological product and in its industrial production. When using deep cultivation of B. bassiana to obtain live biomass, the main infectious particles in the final product are blastospores – yeast-like single cells. A convenient and fast (not requiring the cultivation of mushroom colonies) method for determining the number of blastospores in a product is direct counting in a counting chamber of a particular design using a microscope; this procedure is well applicable in production processes, but when conducting research on the creation of a bioinsecticide, it takes a lot of the researcher's time, especially if it is necessary to obtain the most reliable data when determining the number of blastospores. 

<p align="center"> 
<img
  src="image_folder\images_to_predict\ex_folder_1\1.jpg"
  alt="Blastospores in a photograph taken with a microscope"
  title="Blastospores in a photograph taken with a microscope"
  style="display: inline-block; margin: 0 auto; max-width: 360px">
</p>

An alternative to direct counting in real time can be automatic software counting of blastospores in photographs. The standard for obtaining data from a single measurement is the counting of particles in 10 large squares of the counting chamber. It is assumed that processing the same or twice as many photos with software tools will allow obtaining reliable data in a much shorter time and with minimal direct participation of the researcher.  

<p align="center"> 
<img
  src="image_folder\predicted_images\ex_folder_1\1.jpg"
  alt="The blastospores predicted in the photo by the AI model"
  title="The blastospores predicted in the photo by the AI model"
  style="display: inline-block; margin: 0 auto; max-width: 360px">
</p>

The purpose of this project is to create an application for calculating the number of blastospores in photographs, followed by obtaining averaged values of the number of blastospores for the necessary groups of photos. The application uses a locally downloaded repository of the github project [YOLOv5](https://github.com/ultralytics/yolov5) from the developer company [Ultralytics](https://ultralytics.com). A pre-trained YOLOv5 model is used to detect blastospores. A detailed description of the steps for training the model is given in the second part of the [final project](https://github.com/ostrebko/skf_final_project), which was performed during the course "Specialization DataScience" in the online school [SkillFactory](https://skillfactory.ru). <br> 


## Project structure
...
...
...


## Data and methods
...
...
...


## Instalation
<details>
  
<summary> Details: </summary> <br>

<p> This section provides a sequence of steps for installing and launching the application <br>

```Python
# 1. Activate the virtual environment in which you plan to launch the application (we will use VsCode)

# 2. ...
bash command

# 3. ...
bash command

# 4. ...
bash command
```
</details>


## Activation env
<details>

<p> The description of how to activate the virtual environment was taken from <a href="https://kayumov.ru/536/">Ruslan Kayumov</a>.<br>

<summary> Type in the console: </summary> <br>

```Python
# Steps to activate the virtual environment in which you plan to launch the application in VsCode:
# 1. Run VS Code as an administrator, go to the project directory in PowerShell, execute the code below, the env folder containing the virtual environment files will appear
python -m venv env

# 2. To change the policy, in PowerShell type
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 3. Enter the environment folder (env), run the command
env\Scripts\activate.ps1

# 4. An environment marker (env) will appear at the beginning of the line in PowerShell, but VS Code may still not know anything about it. Press Ctrl+Shift + P, type Python: Select Interpreter
# Specify the desired path to python.exe in the env environment folder, this will be displayed at the bottom of the status bar. Now you can install modules only for a specific project.

# 5. If you need to exit, then execute deactivate in PowerShell, and return to global in the interpreter selection.
```
</details>



## Docker
<details>

<summary> Type in the console: </summary> <br>

```Python
# 1. Create a new image (its size is approximately 5.2 Gb)
docker build -t calc_blastos .

# 2. Run image in container.
docker run --rm -v $PWD/image_folder/:/image_folder  --name calc_blastos calc_blastos

# 3. In the project directory '/image_folder/predicted_images' will appear 
# a new file 'results.csv'

# 4. The created container will be automatically deleted 
# after executing a sequence of commands from the Dockerfile.  
# Delete the container and image after usage
docker rmi calc_blastos
```
</details>



## Create exe
<details>

<summary> Description: </summary> <br>

<p>Creating executable .exe file to run the application may be necessary in some cases. For example, if Docker and/or Python are not installed on the computer, the user does not have the minimum skills to install and configure the necessary programs and libraries, or it is impossible to prepare the computer accordingly beforehand (when demonstrating the program on the Director's or Customer's computer).<br>
<p>To create executable .exe file we will use: <a href="www.pyinstaller.org">PyInstaller</a> and the convenient GUI add-in <a href="https://pypi.org/project/auto-py-to-exe/">auto-py-to-exe</a>.<br>

 <p>To create executable .exe file type in the console:

```Python
# 1. Go to the project application and аctivate the virtual environment
# (see section Introduction)

# 2. Install the PyInstaller package
pip install pyinstaller

# 3. Install the auto-py-to-exe package
pip install auto-py-to-exe

# 4. Run the auto-py-to-exe installed app
auto-py-to-exe 

# 5. In the auto-py-to-exe console window select the parameters: 
# 5.1 Script Location: Specify the full path to the file main.py
# 5.2 Onefile (--onedir / --onefile): onefile
# 5.3 Console Window (--console / --windowed) (to see the work of program): Console Based 
# 5.4 In Advanced --hidden-import add (set plus three times and add one name of the following libs to each line): 1. cv2  2. yaml  3. seaborn.
# 5.5 Settings (auto-py-to-exe Specific Options): Specify the full path to the directory of main.py
# 5.6 The other parameters leave unchanged.

# 6. You can only use the pyinstaller package without installing auto-pytoexe.
# To do this, after step 2 in the command line, 
# specifying the correct path to the project "C:/Full/Path/to/main.py ", run:
pyinstaller --noconfirm --onefile --console --hidden-import "cv2" --hidden-import "yaml" --hidden-import "seaborn"  "C:/Full/Path/to/main.py"
```
</details>
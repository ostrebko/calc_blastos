# Detection of blastospores in photographs with YOLOv5

## Contents

* [Introduction](README.md#Introduction)
* [Features of samples preparations](README.md#Features-of-samples-preparations)
* [Project structure](README.md#Project-structure)
* [Installation](README.md#Installation)
* [Activation the virtual environment](README.md#Activation-env)
* [Docker](README.md#Docker)
* [Creation exe](README.md#Creation-exe)
* [Inference](README.md#Inference)
* [Conclusions](README.md#Conclusions)


## Introduction

<p>Entomopathogenic fungus Beauveria bassiana is a promising basis for biological insecticides for use in crop production. Its ability to cause a deadly infectious process in a wide range of insect pest species makes it possible to create biological preparations based on strains of this species that are not inferior in effectiveness to a significant number of modern chemical insecticides. In addition, biologics based on B. bassiana has a number of advantages over chemical analogues – they are much safer for humans, plants and other environmental objects, have a lower cost, and also often provide a longer protective effect, due to the ability to cause epidemics in insect populations with a high number of individuals (overpopulated populations).</p>  

<p align="center"> 
<img
  src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Beauveria.jpg"
  alt="Grasshoppers (Melanoplus sp.) killed by the fungus Beauveria bassiana (from wikipedia.org)"
  title="Grasshoppers (Melanoplus sp.) killed by the fungus Beauveria bassiana (from wikipedia.org)"
  style="display: inline-block; margin: 0 auto; max-width: 300px">
</p>

<p>The most important characteristic of a biopreparation based on an a priori effective strain of entomopathogen is the number of viable cells/mycelium particles/fungal spores per unit volume or mass of the preparation. This indicator is often determined both in the process of developing a biological product and in its industrial production. When using deep cultivation of B. bassiana to obtain live biomass, the main infectious particles in the final product are blastospores – yeast-like single cells. A convenient and fast (not requiring the cultivation of mushroom colonies) method for determining the number of blastospores in a product is direct counting in a counting chamber of a particular design using a microscope; this procedure is well applicable in production processes, but when conducting research on the creation of a bioinsecticide, it takes a lot of the researcher's time, especially if it is necessary to obtain the most reliable data when determining the number of blastospores.</p>

<p align="center"> 
<img
  src="image_folder\images_to_predict\ex_folder_1\1.jpg"
  alt="Blastospores in a photograph taken with a microscope"
  title="Blastospores in a photograph taken with a microscope"
  style="display: inline-block; margin: 0 auto; max-width: 360px">
</p>

<p>An alternative to direct counting in real time can be automatic software counting of blastospores in photographs. The standard for obtaining data from a single measurement is the counting of particles in 16 large squares of the counting chamber. It is assumed that processing the same or twice as many photos with software tools will allow obtaining reliable data in a much shorter time and with minimal direct participation of the researcher.</p>

<p align="center"> 
<img
  src="image_folder\predicted_images\ex_folder_1\1.jpg"
  alt="The blastospores predicted in the photo by the AI model"
  title="The blastospores predicted in the photo by the AI model"
  style="display: inline-block; margin: 0 auto; max-width: 360px">
</p>

<p>The purpose of this project is to create an application for calculating the number of blastospores in photographs, followed by obtaining averaged values of the number of blastospores for the necessary groups of photos. The application uses a locally downloaded repository of the github project [YOLOv5](https://github.com/ultralytics/yolov5) from the developer company [Ultralytics](https://ultralytics.com). A pre-trained YOLOv5 model is used to detect blastospores. A detailed description of the steps for training the model is given in the second part of the [final project](https://github.com/ostrebko/skf_final_project), which was performed during the course "Specialization DataScience" in the online school [SkillFactory](https://skillfactory.ru).</p>  


## Features of samples preparations
<details>

<summary>Description </summary> <br>

<p>This section does not relate to the project, but gives a general understanding of how the preparation of samples and the calculation of the number of blastospores for each sample is carried out.</p>  

1. Samples for calculations are taken from the bioreactor sampler using a special dispenser and then placed in a special test tube.  
2. Before counting, the sample is diluted in a penicillin solution and a fixed dilution coefficient.
3. The diluted sample is placed in the [Goryaev chamber](https://paulturner-mitchell.com/129033-chto-takoe-kamera-goryaeva-pravila-podscheta-formennyh-elementov-krovi.html)  
4. Goryaev's camera is installed on the microscope slide and the area needed for counting is adjusted. An example of the transition between areas can be seen in [this video](https://www.istockphoto.com/video/counting-blood-cells-in-the-goriaev-chamber-under-a-microscope-gm968062484-263998859).  
5. The number of blastospores is calculated for 10 different estimated areas of the Goryaev chamber, and then the average number is calculated.  
6. According to the calculated average value of the number of blastospores, the number of microorganisms in the calculated area is estimated, taking into account the dilution coefficient.  

</details>


## Project structure
<details>

<summary>Display project structure </summary> <br>

```Python
calc_blastos
├── config
│   └── data_config.json       ## congiguration file
├── image_folder
│   ├── images_to_predict      ## folder for images to detection (put folders with photos)
│   └── predicted_images       ## folder with detection results (photos, reports)
├── model
│   ├── weights_1476_150_ep.pt ## trained model 1
│   └── weights_1476_450_ep.pt ## trained model 2
├── utilits                    ## folder with custom functions and classes
│   ├──  __ init __.py
│   ├── calcs_boxes.py
│   ├── functions.py
│   ├── model_loader.py
│   └── read_config.py
├── yolov5                     ## folder with yolov5 app from ultralitics git 
├── Dockerfile
├── main.exe                   ## file to run project in windows (without python & docker)
├── main.py
├── README.md
└── requirements.txt
```
</details>

## Instalation
<details>

<summary> Display how to install app </summary> <br>

<p> This section provides a sequence of steps for installing and launching the application. <br>

```Python
# 1. Activate the virtual environment in which you plan to launch the application (we will use VsCode)

# 2. Clone repository
git clone https://github.com/ostrebko/calc_blastos.git

# 3. Go to the new directory:
cd calc_blastos

# 4. Install requirements:
pip install -r requirements.txt

# 5. Place folders with groups of photos in the 'image_folder\images_to_predict' folder. To name folders, use only Latin letters, numbers (digits) and "_" instead of spaces.

# 6. Create predicts of detection blastospores with main.py or create & run main.exe (in windows).
python main.py
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

<summary> Display how to create and run docker image  </summary> <br>

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



## Creation exe
<details>

<summary> Display how to create exe-file  </summary> <br>

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


## Inference
<details>

<summary>General description </summary> <br>

<p>The term inference in this project means detecting blastospores in photographs using the YOLOv5 library and saving them with marked bounding boxes. For the purposes of the project is carried out:</p>  

- counting the number of blastospores in each photo;  
- generating reports for each group of photos (usually this number is 10, but it can be any other number);  
- formation of a single (general) report on all groups of photos.  

<p>The reports include data on the calculated number of blastospores for each photo, the recalculated (reduced) number of blastospores (see explanations below) and the averaged calculated values of blastospores for each group of photos.</p>

<p>The calculation of the number of blastospores "manually" is carried out inside the calculation grid of the Goryaev chamber, excluding neighboring areas, while the detection of blastospores using Yolov5 is carried out from a photograph, affecting the location of the area. To estimate the number of blastospores in the calculated area using a trained model, it was decided to use a decreasing coefficient equal to the ratio of the grid area to the photo area. This term became possible due to the constancy of the following indicators: 1. Relatively uniform distribution of blastospores in the photo; 2. Fixed magnification coefficient of the microscope during photographing; 3. Accurate and fixed dimensions of the Goryaev camera grid; 4. Using one (constant) resolution of photographs for training the model and for further inference.</p> 
 
<p>To solve the current problem, preliminary or additional allocation of the calculated area (the area inside the Goryaev camera grid) wasn't carried out in the photographs. Why this became possible and why a more conservative approach was chosen is described in more detail in the Conclusion section</p>

</details>

<details>
<summary>How to & what's where</summary> <br>

<p>To carry out an inference, each calculated group of photos must be placed in its own separate folder in *'image_folder/images_to_predict'*. To assign names to folders, you need to use only Latin letters, numbers (digits) and "_" instead of spaces.</p>

<p>In the *'model'* folder there are two already pre-trained YOLOv5 models. You can put another custom YOLOv5-trained models in the *'model'* folder, in this case the variable *'model_name'* in the configuration file *data_config.json* needs to be changed to the corresponding model name. A detailed description of YOLOv5 model training and information on data markup are given in Section 2 of the [final project]('https://github.com/ostrebko/skf_final_project/blob/main/part_2_model_training/1_Models_descriptions.md') from my study on course 'Specialization DataScience'.  

<p>To carry out an inference perform in the terminal:
```Python
python main.py
```
or create & run main.exe in windows (see section 'Create exe').</p>

<p>Photos with calculated bounding boxes and reports for each group of photos are saved in the folder *'image_folder/predicted_images'* in separate folders whose names correspond to folders from *'image_folder/images_to_predict'*. The final report for all groups of photos is created in a file *'image_folder/predicted_images/results.xlsx'*.</p>
</details>


## Conclusions
<details>
...
...
...
</details>

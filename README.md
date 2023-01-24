# Detection of blastospores in photographs with YOLOv5

## Contents

* [Introduction](README.md#Introduction)
* [Project structure](README.md#Project-structure)
* [Data and methods](README.md#Data-and-methods)
* [Installation](README.md#Installation)
* [Docker](README.md#Docker)
* [Inference](README.md#Inference)
* [Experimental data analysis](README.md#Experimental-data-analysis)
* [Machine learning models structure](README.md#Machine-learning-models-structure)
* [Experiment logging](README.md#Experiment-logging)
* [Conclusion](README.md#Conclusion)


## Introdcution

Entomopathogenic fungus Beauveria bassiana is a promising basis for biological insecticides for use in crop production. Its ability to cause a deadly infectious process in a wide range of insect pest species makes it possible to create biological preparations based on strains of this species that are not inferior in effectiveness to a significant number of modern chemical insecticides. In addition, biologics based on B. bassiana has a number of advantages over chemical analogues – they are much safer for humans, plants and other environmental objects, have a lower cost, and also often provide a longer protective effect, due to the ability to cause epidemics in insect populations with a high number of individuals (overpopulated populations).  

![ex.: Grasshoppers (Melanoplus sp.) killed by the fungus Beauveria bassiana](https://en.wikipedia.org/wiki/Beauveria_bassiana#/media/File:Beauveria.jpg)

The most important characteristic of a biopreparation based on an a priori effective strain of entomopathogen is the number of viable cells/mycelium particles/fungal spores per unit volume or mass of the preparation. This indicator is often determined both in the process of developing a biological product and in its industrial production. When using deep cultivation of B. bassiana to obtain live biomass, the main infectious particles in the final product are blastospores – yeast-like single cells. A convenient and fast (not requiring the cultivation of mushroom colonies) method for determining the number of blastospores in a product is direct counting in a counting chamber of a particular design using a microscope; this procedure is well applicable in production processes, but when conducting research on the creation of a bioinsecticide, it takes a lot of the researcher's time, especially if it is necessary to obtain the most reliable data when determining the number of blastospores.  

An alternative to direct counting in real time can be automatic software counting of blastospores in photographs. The standard for obtaining data from a single measurement is the counting of particles in 10 large squares of the counting chamber. It is assumed that processing the same or twice as many photos with software tools will allow obtaining reliable data in a much shorter time and with minimal direct participation of the researcher.  

The purpose of this project is to create an application for calculating the number of blastospores in photographs, followed by obtaining averaged values of the number of blastospores for the necessary groups of photos. The application uses a locally downloaded repository of the github project [YOLOv5](https://github.com/ultralytics/yolov5) from the developer company [Ultralytics](https://ultralytics.com). A pre-trained YOLOv5 model is used to detect blastospores. A detailed description of the steps for training the model is given in the second part of the [final project](https://github.com/ostrebko/skf_final_project), which was performed during the course "Specialization DataScience" in the online school [SkillFactory](https://skillfactory.ru).  



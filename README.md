# Face-Recognition
 
This is a real-time facial recognition program using the Haar Cascade classification method. It is an early version with much more to come. 

## Install/Usage

Create a virtual environment and install the requirements.txt

1) Run addPerson.py. It will ask for an ID. Start at 1 for first person, 2 for second person, etc
### python addPerson.py
2) Run trainer.py. This will train the model on the added faces. The trainer will need to be run every time a new person is added
### python trainer.py
3) Open mainScreen.py and enter your name to the 'names' variable in the order they added/numbered (this will be done progrmatically in later versions)
4) Run main.py
### python main.py

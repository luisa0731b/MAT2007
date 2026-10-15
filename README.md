MAT2007
# Flightless Friends!
**How strongly is flipper length related to body mass?**

This project used data collected between 2007 and 2009, and made publicly available by Dr. Kristen and other researchers from the Palmer Station in Antarctica. Data regarding the body measurements of three penguins species was collected:
- Adelie penguins
- Chinstrap penguins
- Gentoo penguins

Body mass is a good indicator of an animal's condition, but flipper length can be much easier to measure, especially when out in the field. This project asked "How strongly is flipper length related to body mass within each penguin species, and how much of the variation in body mass does flipper length explain?" This answer will determine whether it is worth relying on flipper length as the body mass predictor.

### Software Dependencies
You can find the code used to run this project titled as "PenguinAnalysis.py". Additionally, the dataset itself will be needed to calculate results and plot graphs; titled "PenguinsResearchData.csv", it can also be downloaded from this repository. When getting ready to run the code in Visual Studio Code, ensure you have the following Python packages downloaded before:
- numpy (for number crunching)
- pandas (for handling the data table)
- matplotlib (for figures)
- scipy (imports scipy statistic tools)

To download the packages, you can enter the terminal window at the bottom of your screen, and type + Enter the following commands, respectively (and one at a time):
- pip install numpy OR pip3 install numpy
- python -m pip install pandas OR pip install pandas
- pip install matplotlib OR pip3 install matplotlib OR python -m pip install matplotlib
- python -m pip install scipy

Additionally, it is important to copy the path of the location of the PenguinsResearchData.csv and paste it directly into the code. You can find this on line 16:
- df = pd.read_csv("PASTE PATH HERE")

Afterwards, you can run the code and wait for the plots to be created and saved in your folder!

# Sensor Data Project

To run the program, enter "python3 sensor.py" into the CLI. Ubuntu on Windows was used for this project.

This project extracts information that was taken from AndroSensor.

It calculates the total time, average and max speeds, number of stops, distance travelled and average light.
It also saves 3 graphs to .png files to display a visual of these features. However, number of stops was not included.

Pylint3 was used. The program did not get a 100% pass score because the imports *matplotlib*, *matplotlib.use('Agg')* (this is actually a function), and *matplotlib.pyplot as plt* had to be in that order to make my program work.

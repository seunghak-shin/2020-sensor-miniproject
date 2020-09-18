Informal Memorandum on Sensor Reading Simulation (Hardware mini-project) By: Seunghak Shin, Panagiotis Siozios

ABSTRACT:

Provided in the report is a complete quantitative and qualitative analysis of our results obtained from carrying out the hardware sensor simulation miniproject.
The analysis was split into 5 separate tasks, which will be summarized here.
Firstly, we established a connection between the server and client sides, in order to obtain sensor readings.
Next we adjusted the client side code to write and save these readings to a text file.
We allowed the connection to persist for approximately 30 minutes in order to obtain at least 100 total values.
Using these values, we wrote the script 'analyze.py' that could give probabilistic representations and analysis of the data we obtained.
These findings are present in plots when running this script.
After this, we wrote another script 'anomaly.py' which would detect all the anomalous data points and give us another view of the analysis without these outliers.
In the last step we provided the qualitative analysis of our results as compared with other real world situations, possible causes for error, as well as improvements to the simulation.


TASK 0:

The greeting string issued by the server to the client upon first connecting is: "ECE Senior Capstone IoT simulator"


TASK 1:

Provided in the repository is the Python code for Websockets client that saves the JSON data to a text file as it comes in (message by message).


TASK 2:

The data points observed were printed to the command line for ease of access to the user.
The median and variance observed from the temperature data (with at least 100 values) in the office were 23.011 degrees and 1957.36 respectively.
The median and variance observed from the occupancy data (with at least 100 values) the office were 2 people and 1.972 respectively.
Provided in the repository is code (named analyze.py) for the histogram plots of the data.

The mean and variance of the time interval of the sensor readings are 1.014 and 1.021 respectively.
Plots of the time interval in histogram format can be obtained from running the code in the repository.
The plot indeed mimics the Erlang distribution for connection intervals in large systems, because many 
time-sensitive systems obey this specific PDF pattern where the probability of higher delays decreases exponentially.


TASK 3:

Provided in the repository is an algorithm (named anomaly.py) that detects anomalies in temperature sensor data, 
prints the percent of "bad" data points and determines the temperature median and variance with these bad data points discarded.

A persistent change in temperature does not always indicate a failed sensor - in an environment where temperature is volatile, 
the readings can vary widely within a shorter period of time. The sensor readings will depend more on the environment that it is placed in.

Accounting for the several different climates around the world, possible bounds on temperature for each room type can be 0 to 50 degrees Celsius.
However, a more reasonable spread would be between 17 and 27 degrees Celsius, where air conditioning and heating play bigger factors in sensor readings.


TASK 4:

We can confidently conclude that the simulation accurately depicts a real world situation for a few reasons.
Firstly, we obtained readings that fell within both the generalized and realistic bounds of temperatures that we had set out in the third task.
Also, as discussed in the quantitative analysis, our probability distribution of temperatures very similarly depicted the Erlang distribution 
for values of k = 1,2 and mu = 2 (where "k" directly affects the shape of the distribution and "mu" is the reciprocal of the rate of data occurrence).
We were able to create relatively accurate probability models based on our readings because there were so few anomalies - the data was 
mostly clean, with a few pinpoint outliers that are discussed below.

There were two main factors that may have caused these outliers in the data obtained: internal sensor malfunctions or unanticipated human interaction.
A sensor malfunction may have been for any number of internal hardware malfunctions that would cause the signal to be misread and then incorrectly transmitted to the client.
On the human side, any people present within the room at the time of data collection may have indirectly or unknowingly tampered with the devices, 
causing the readings to be blatantly incorrect. These two factors are justified by the fact that our anomalies were singular occurrences and not persisting 
throughout the whole data collection process.

Realistically, a Python Websockets library as used in this simulation would be less difficult to implement due to the inherent nature of development libraries.
With a C++ Websockets implementation, we would need to create all the respective coroutines individually since this is required for asynchronous data collection 
as done in this simulation. Clearly such a feat is much more time inefficient and would cause a greater load in terms of computing time/power for a machine that 
is already continuously receiving remote data points during a simulation. Using this Python Websockets library, we're able to carry out all the coroutines with 
more computing time/power efficiency and focus more on optimizing external factors (such as sensor performance and room conditions), 
instead of worrying about the program itself.

When polling the sensors, the time interval can be reduced but this would mean we'd need to run a big script several times in short time spans which would be 
unrealistic no matter how modularized the program is. It would be better for the sensors to reach out to the server rather than be polled because this way we'll 
end up with more data points and less computing time/power used. However due to the inefficient nature of both these collection processes, both of these 
options are not necessarily the best solution - in an ideal world, a perfectly optimal solution to this problem would be to establish a client and server connection 
only when data is being obtained and read, and no other time - of course this is a pipe dream and is technically unrealistic, because connections between 
client and server are normally created manually in order to reduce computational complexity.

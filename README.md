# simple-CV-readout <img src="https://github.com/ismboedev/simple-CV-readout/blob/master/src/icon.png" width="42" align="left"> 

Simple tool for analyzing output data of capacitance-voltage measurements with a Zurich Lock-In-Amplifier.

***

The Zurich Lock-In-Amplifier exports it's data as a `some_cryptic_name.csv` and a `history_1234.csv` file.  
This tool reads the `some_cryptic_name.csv` and `history_1234.csv` files, calculates the capacitance with a given  
amplitude and creates a directory with a `CV_chunk1_my_own_measurement_name.dat` for each measurement.
`my_own_measurement_name` here is the name of the measurement given in the GUI of the Lock-In-Amplifier while measuring.

## Usage  
You have to make sure not to use any reserved character in your `my_own_measurement_name`, because it is used in the filenames.
Start the script, or the provided binaries and select your files. Enter an amplitude or keep the default one.  
By pressing *Calculate & Exit* the tool closes the window first and calculates the capacitance afterwards.  

You can then import the files in your desired graphing program.

***

Thanks go to my colleague Pepe85 for his contributions.

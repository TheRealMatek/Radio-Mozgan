To run the project install all the requirements.

Install fluidsynth. 
In order to get fluidsynth to be found, you might have to modify mingus variable for locating the package.
It can be found in the file pyfluidsynth.py and it has to look like this:
lib = find_library('fluidsynth') or \
    find_library('libfluidsynth') or \
    find_library('libfluidsynth-3') or \
    find_library('libfluidsynth-2') or \
    find_library('libfluidsynth-1')

Download a soundFontFile and set the soundFontPath variable to the path of the file.
If you want to use it with a simulation that's enough.
If you want to setup the Unicorn, you also have to copy UnicornPy folder into the Lib folder of your python env.
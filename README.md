# pyacut - Put a video in, get the action out.

Install with https://pipenv.pypa.io/en/latest/.

Then run in a pipenv shell:

python modetect.py $INPUTVIDEO

It will detect longer scenes with movement and cut out the rest and write the resulting clip to the current directory with the file name of the input and "-cut.mp4" appended.

Based on https://www.geeksforgeeks.org/webcam-motion-detector-python/.

You can then run "concatter.py" to concatenate the clips to longer videos.

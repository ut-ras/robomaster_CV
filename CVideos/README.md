Download and place CVideos.py in the same folder as the python file to augment frames.
Import CVideos into your program:
```
from CVideos import videofeed
```
Pass a function (that takes in a frame and returns an augmented frame to be displayed) to videofeed as such
```
videofeed(exampleFunction)
```
Don't call the function when passing it to videofeed (i.e. don't do this ```videofeed(exampleFunction())```)

The program automatically downloads some test videos, but you can add more by ploping videos into the CVideos folder it will make when you first run the program.

## Optional paramaters:
### ```file``` 
If you just want to play one file, you can specify using this parameter. Include the file extension and make sure the video is in the CVideos folder (ex: ```videofeed(exampleFunction,file=filename)```)
### ```sidebyside``` 
To place your augmented frame next to the orginal frame, set sidebyside to True. (ex: ```videofeed(exampleFunction,sidebyside=True)```)

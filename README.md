# Door-Handle-Detector
Files for building and interacting with the door handle detector docker image.

The notebook used to create the model used in this container can be found at [https://www.kaggle.com/code/jacobswindell/door-handle-object-detection-with-icevision](https://www.kaggle.com/code/jacobswindell/door-handle-object-detection-with-icevision)
## Setup
pull the latest docker image from [https://hub.docker.com/repository/docker/jakeswin/door-handle-detector](https://hub.docker.com/repository/docker/jakeswin/door-handle-detector)

```bash
docker pull jakeswin/door-handle-detector 
```

Download and extract the contents of this repository to a location of your choice

Run the `run_container.sh` file to start the container.

Wait for the container to download the model and set it up, when it is finished you can send your images to the container on port 8000.

To test the container run the `client.py` file in another terminal with:

```bash
python client.py door.jpg
```

file paths to door images are relative to where the client.py file is stored.

`client.py` file has only been tested on `.jpg` image files.

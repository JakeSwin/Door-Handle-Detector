FROM pytorch/pytorch:1.10.0-cuda11.3-cudnn8-runtime

RUN sed -i -e 's/http:\/\/archive\.ubuntu\.com\/ubuntu\//mirror:\/\/mirrors\.ubuntu\.com\/mirrors\.txt/' /etc/apt/sources.list

RUN apt update \
 && apt install -y python3 python3-pip libgl1 

RUN pip3 install opencv-python pillow flask icevision==0.11.0
RUN pip3 install mmcv-full==1.3.17 -f https://download.openmmlab.com/mmcv/dist/cu111/torch1.10.0/index.html
RUN pip3 install mmdet==2.17.0

COPY server.py .
COPY door_handle_model_checkpoint_full.pth . 
RUN mkdir ./images

ENTRYPOINT ["python", "server.py"]

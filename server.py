from icevision.all import * 
from icevision.models.checkpoint import model_from_checkpoint 
from icevision.models.inference import process_bbox_predictions
from flask import Flask, request
from pathlib import Path
import PIL
import os

checkpoint_and_model = model_from_checkpoint("./door_handle_model_checkpoint_full.pth")

model_type = checkpoint_and_model["model_type"]
backbone = checkpoint_and_model["backbone"]
class_map = checkpoint_and_model["class_map"]
img_size = checkpoint_and_model["img_size"]
model_type, backbone, class_map, img_size

model = checkpoint_and_model["model"]

img_size = checkpoint_and_model["img_size"]
transforms = [*tfms.A.resize_and_pad(img_size), tfms.A.Normalize()]
valid_tfms = tfms.A.Adapter(transforms)

app = Flask(__name__)

app.config['upload_folder'] = "/workspace/images"
path_to_image_folder = app.config['upload_folder']

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(os.path.join(app.config['upload_folder'], file.filename))

    img_files = get_image_files(path_to_image_folder)

    imgs_array = [PIL.Image.open(Path("images"/fname)) for fname in img_files]
    infer_ds = Dataset.from_images(imgs_array, valid_tfms, class_map=class_map)

    infer_dl = model_type.infer_dl(infer_ds, batch_size=1, shuffle=False)
    preds = model_type.predict_from_dl(model, infer_dl, keep_images=True, detection_threshold=0.15)
    preds = [process_bbox_predictions(pred, imgs_array[0], transforms) for pred in preds]
    
    print(preds[0].as_dict())
    result = preds[0].as_dict()["detection"]
    result["scores"] = result["scores"].tolist()

    tofloat = lambda x: [float(b) for b in x]
    result["bboxes"] = [tofloat(b) for b in [bbox.xyxy for bbox in result["bboxes"]]]

    result["label_ids"] = [int(i) for i in result["label_ids"]]
    return {"message": "OK - Got Image", "preds": result} 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True, debug=True)

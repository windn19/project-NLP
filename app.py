from flask import Flask, request, jsonify

from models import load_model, translate

app = Flask(__name__)

model_img, model_trans = load_model()


@app.post('/predict')
def get_predict():
    f = request.files['file']
    f.save('static/temp.jpg')
    res = translate(model_img, model_trans, f)
    return jsonify(status_code=200, result=res)


if __name__ == '__main__':
    app.run()

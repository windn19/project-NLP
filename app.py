from threading import Thread

from flask import Flask, request, jsonify, render_template
from telebot import TeleBot

from forms import FileForm
from models import load_model, translate
from settings import telegram_token

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MY_NEW_SECRET_KEY'
bot = TeleBot(token=telegram_token)

model_img, model_trans = load_model()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FileForm()
    if form.validate_on_submit():
        file_binary = form.file.data
        file_binary.save('static/temp.jpg')
        res = translate(model_img, model_trans, 'static/temp.jpg')
        return render_template('index.html', form=form, image=True, result=res)
    return render_template('index.html', form=form, image=False)


@bot.message_handler(content_types=['document', 'photo'])
def get_echo_message(message):
    if message.document is not None:
        file_info = bot.get_file(message.document.file_id)
    else:
        file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open('static/temp.jpg', mode='bw') as f:
        f.write(downloaded_file)
    res = translate(model_img, model_trans, 'static/temp.jpg')
    bot.send_message(message.chat.id, res)


@bot.message_handler()
def echo_message(message):
    return bot.send_message(message.chat.id, 'Этот бот может вернуть описание картинки')


@app.post('/predict')
def get_predict():
    f = request.files['file']
    f.save('static/temp.jpg')
    res = translate(model_img, model_trans, 'static/temp.jpg')
    return jsonify(status_code=200, result=res)


def main():
    bot.infinity_polling()


if __name__ == '__main__':
    th = Thread(target=main, daemon=True)
    th.start()
    app.run()

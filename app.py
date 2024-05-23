from threading import Thread

from flask import Flask, request, jsonify
from telebot import TeleBot

from models import load_model, translate
from settings import telegram_token

app = Flask(__name__)
bot = TeleBot(token=telegram_token)

model_img, model_trans = load_model()


@bot.message_handler(content_types=['document', 'photo'])
def get_echo_message(message):
    if message.document is not None:
        file_info = bot.get_file(message.document.file_id)
    else:
        file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    res = translate(model_img, model_trans, downloaded_file)
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

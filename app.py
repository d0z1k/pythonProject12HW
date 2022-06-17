import logging
from flask import Flask, request, render_template, send_from_directory

from main.views import main_blueprint
from loader.views import loader_blueprint
import loggers

app = Flask(__name__)
# регистрация блупринтов
app.register_blueprint(main_blueprint)
app.register_blueprint(loader_blueprint)
# конфиг путей загрузки файла
app.config["POST_PATH"] = "data/posts.json"
app.config["UPLOAD_FOLDER"] = "uploads/images"
# запуск логгера
loggers.create_loggers()
logger = logging.getLogger("basic")


@app.route("/uploads/<path:path>")
def static_dir(path):
    return send_from_directory("uploads", path)


logger.debug("Стартуем")

app.run()

import logging

import flask

from classes.data_manager import DataManager
from classes.exeptions import DataSourceBrokenException

main_blueprint = flask.Blueprint('main_blueprint', __name__, template_folder='templates')

logger = logging.getLogger("basic")


# блупринт на главную страницу
@main_blueprint.route('/')
def main_page():
    return flask.render_template("index.html")


# блупринт на страницу поиска
@main_blueprint.route('/search/')
def search_page():
    """
    Принимает строку для поиска, ищет и возвращает результат
    :return: post_list.html
    """
    path = flask.current_app.config.get("POST_PATH")
    data_manager = DataManager(path)

    s = flask.request.values.get("s", None)

    logger.info(f"Ищем {s}")

    if s is None or s == "":
        posts = data_manager.get_all()
    else:
        posts = data_manager.search(s)
    return flask.render_template("post_list.html", posts=posts, s=s)


# блупринт эксепшна ошибки загрузки джейсон
@main_blueprint.errorhandler(DataSourceBrokenException)
def data_source_broken_error(e):
    return "Файл с данными повреждён"

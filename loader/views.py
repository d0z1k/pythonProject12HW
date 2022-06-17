import os
import logging
from flask import Blueprint, render_template, request, current_app
from classes.data_manager import DataManager
from loader.exeptions import PictureFormatNotSupportedError, PictureNotUploadedError

loader_blueprint = Blueprint('loader_blueprint', __name__, template_folder='templates')


def is_file_type_valid(file_type):
    """
    проверяет формат загружаемой картинки
    :param file_type:
    :return: bool
    """
    if file_type.lower() in ["jpg", "png", "jpeg", "gif", "webp"]:
        return True
    return False

# загружает форму поста
@loader_blueprint.route('/post', methods=['GET'])
def page_form():
    return render_template('post_form.html')

# загружает форму создаваемого поста
@loader_blueprint.route('/post', methods=['POST'])
def page_create_posts():
    picture = request.files.get("picture", None)
    content = request.values.get("content", "")

    filename = picture.filename
    file_type = filename.split('.')[-1]


    # Проверка формата картинки
    logger = logging.getLogger("basic")

    if not is_file_type_valid(file_type):
        logger.info(f"загруженный файл {file_type} - не картинка")
        raise PictureFormatNotSupportedError(f"Формат {file_type} не поддерживается")

    # Сохранение поста и картинки
    os_path = os.path.join(".", "uploads", "images", filename)

    try:
        picture.save(os_path)
    except FileNotFoundError:
        logger.error(f"ошибка при загрузке файла {os_path}, {filename}")
        raise PictureNotUploadedError(f"{os_path}, {filename}")

    web_path = os.path.join("/", "uploads", "images", filename)
    pic = web_path

    post = {"pic": web_path, "content": content}

    path = current_app.config.get("POST_PATH")
    data_manager = DataManager(path)
    data_manager.add(post)

    return render_template('post_uploaded.html', pic=pic, content=content)


@loader_blueprint.errorhandler(PictureFormatNotSupportedError)
def error_format_not_supported(e):
    return "Формат изображения не поддерживается, выберите другой"


@loader_blueprint.errorhandler(PictureNotUploadedError)
def error_picture_not_uploaded(e):
    return "Не удалось загрузить изображение"

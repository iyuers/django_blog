from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
import os
import uuid
import json
import datetime


@csrf_exempt
def upload_image(request, dir_name):
    ##################
    #  kindeditor图片上传返回数据格式说明：
    # {"error": 1, "message": "出错信息"}
    # {"error": 0, "url": "图片地址"}
    ##################
    result = {"error": 1, "message": "上传错误"}
    files = request.FILES.get("imgFile")
    if files:
        result = image_upload(files, dir_name)
    return HttpResponse(json.dumps(result), content_type="application/json")


def upload_generation_dir(dir_name):
    today = datetime.datetime.today()
    dir_name += '\\{}\\{}'.format(today.year, today.month)
    # upload_path = settings.MEDIA_ROOT + dir_name
    # if not os.path.exists(upload_path):
    #     os.makedirs(upload_path)
    return dir_name


def image_upload(files, dir_name):
    allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
    file_suffix = files.name.rsplit('.', 1)[-1]
    if file_suffix not in allow_suffix:
        return {"error": 1, "message": "图片格式不正确"}
    relative_path_file = upload_generation_dir(dir_name)
    path = os.path.join(settings.MEDIA_ROOT, relative_path_file)
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = str(uuid.uuid1()) + "." + file_suffix
    path_file = os.path.join(path, file_name)
    file_url_path = os.path.join(relative_path_file, file_name)
    # 注意这里 传递给 kindeditor 的 url，必须是相对路径
    file_url = os.path.join(settings.MEDIA_URL, file_url_path)
    open(path_file, 'wb').write(files.file.read())
    print("file_url:", file_url_path)
    print('path_file:', path_file)
    return {"error": 0, "url": file_url}











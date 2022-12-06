import time
from datetime import datetime, date

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from monitor.models import Warnings, Events
import json
import logging


def index(request):
    """
     获取一段时间内的，告警数据
     文件解析
     @param json: 原始的文件
     """
    beginstamp = request.GET["beginDate"]
    endstamp = request.GET["endDate"]
    begin = time.localtime(int(beginstamp))
    end = time.localtime(int(endstamp))
    format = "%Y-%m-%dT%H:%M:%SZ"
    beginstr = time.strftime(format, begin)
    endstr = time.strftime(format, end)
    alllist = Warnings.objects.filter(date_time__range=[beginstr, endstr]).order_by('date_time').values()
    response = {"code": 200000, "message": "success", "data": list(alllist)}
    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type="application/json")


def insert_alert(request):
    if len(request.body) > 0:
        insert(request.body)
        response_data = {'code': '200000', 'result': '', 'message': 'success'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data = {'code': '500000', 'result': 'error', 'message': 'Some error message'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def insert(data):
    """
     将原始的数据解析出来，插入数据库
     文件解析
     @param json: 原始的文件
     """
    # before_count = Warnings.objects.all().count()
    # logging.info(f"插入前{before_count}")
    parse_data(data)
    after_count = Warnings.objects.all().count()
    logging.info(f"插入后 {after_count}")


def parse_data(data):
    """
      将原始的数据解析出来，插入数据库
      文件解析
      @param data: 原始的数据
    """
    info = data.decode()
    datatransform = str(info)
    json_data = json.loads(datatransform)
    logging.info("json_data数据{0}".format(json_data))
    project = json_data["project"]
    project_name = json_data["project_name"]
    event = json_data["event"]
    app_version = ''
    if "dist" in event.keys():
        app_version = event["dist"]

    url = ''
    if "url" in json_data.keys():
        url = json_data["url"]
    tags = event["tags"]
    host = info_tags("host", tags)
    path = info_tags("path", tags)
    q = info_tags("q", tags)
    issue_url = host + path
    if q and len(q) > 0:
        issue_url += "?" + q
    message = ''
    if "message" in json_data.keys():
        message = json_data["message"]
    logging.info("准备发送请求")
    logging.info(f"解析到的URL ===={url}")
    event_c = Events(event_id=event, event_msg=info)
    warning_c = Warnings(event=event_c,
                         project=project,
                         project_name=project_name,
                         version=app_version,
                         message=message,
                         tags_method=info_tags("HTTPMethod", tags),
                         tags_ac=info_tags("ac", tags),
                         tags_app_device=info_tags("app.device", tags),
                         tags_ce=info_tags("ce", tags),
                         tags_cn=info_tags("cn", tags),
                         tags_cs=info_tags("cs", tags),
                         tags_de=info_tags("de", tags),
                         tags_device=info_tags("device", tags),
                         tags_dns=info_tags("dns", tags),
                         tags_ds=info_tags("ds", tags),
                         tags_du=info_tags("du", tags),
                         tags_environment=info_tags("environment", tags),
                         tags_host=info_tags("host", tags),
                         tags_level=info_tags("level", tags),
                         tags_np=info_tags("np", tags),
                         tags_os=info_tags("os", tags),
                         tags_os_name=info_tags("os.name", tags),
                         tags_path=info_tags("path", tags),
                         tags_param=info_tags("q", tags),
                         tags_ree=info_tags("ree", tags),
                         tags_resp=info_tags("resp", tags),
                         tags_resps=info_tags("resps", tags),
                         tags_rs=info_tags("rs", tags),
                         tags_rspe=info_tags("rspe", tags),
                         tags_rsps=info_tags("rsps", tags),
                         tags_sc=info_tags("sc", tags),
                         tags_sce=info_tags("sce", tags),
                         tags_scheme=info_tags("scheme", tags),
                         tags_scs=info_tags("scs", tags),
                         tags_tls=info_tags("tls", tags))

    logging.info("开始保存")
    try:
        event_c.save()
        warning_c.save()
        logging.info("保存成功")
    except:
        logging.info("保存失败")


def info_tags(info_name, tags):
    """
    根据info_name 获取具体的信息
    """
    for tag in tags:
        if tag and len(tag) > 1 and tag[0] == info_name:
            return tag[1]
    return ""

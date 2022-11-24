import json
import requests
from django.http import HttpResponse, HttpResponseNotFound
import logging

# -- coding: utf-8 --
logging.getLogger().setLevel(logging.INFO)


class MarkDownModel:
    project = ""
    project_name = ""
    level = ""
    rules_name = ""
    app_version = ""
    issue_url = ""
    url = ""

    def __init__(self, project, project_name, level, rules_name, app_version, issue_url, url):
        self.project = project
        self.project_name = project_name
        self.level = level
        self.rules_name = rules_name
        self.app_version = app_version
        self.issue_url = issue_url
        self.url = url

    def mark_down_info(self):
        wechat_dict = {"msgtype": "markdown"}
        content = """移动端项目<font color=\"warning\">{0}-{1}</font>告警！\n
         >类型: <font color=\"warning\">{2}</font>
         >应用: <font color=\"info\">{3}</font>
         >版本号: <font color=\"info\">{4}</font>
	     >接口: <font color=\"info\">{5}</font>
 	     >详情: <font color=\"info\">[查看日志]({6})</font>\n请关注:<@81095534><@81075463>
        """.format(self.project_name,
                   self.project,
                   self.rules_name,
                   self.project,
                   self.app_version,
                   self.issue_url,
                   self.url)
        mark_down_dict = {"content": content}
        wechat_dict["markdown"] = mark_down_dict
        return wechat_dict


def warningParse(request, type=-1):
    return sendWechatEnterprise(request, type)


def sendWechatEnterprise(request, type):
    """
        self.args = args
        self.kwargs = kwargs
        self.url_name = url_name
        self.route = route
        self.tried = tried
        self.captured_kwargs = captured_kwargs
        self.extra_kwargs = extra_kwargs
        @param request: 请求方法
  """
    # print(request.arges)
    # print(request.kwargs)
    # print(request.route)
    # print(request.tried)
    # print(request.captured_kwargs)
    # type = request.POST.get("type")
    logging.info("type == {0}".format(type))
    if type != -1 and len(request.body) > 0:
        file_parse(request.body)
        response_data = {'code': '200000', 'result': '', 'message': 'success'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data = {'code': '500000', 'result': 'error', 'message': 'Some error message'}
        return HttpResponse(json.dumps(response_data), content_type="application/json")


def info_tags(info_name, tags):
    """
    根据info_name 获取具体的信息
    """
    for tag in tags:
        if tag and len(tag) > 1 and tag[0] == info_name:
            return tag[1]
    return ""


def file_parse(data):
    """
    将原始的数据解析出来，获取有用的信息
    文件解析
    @param info: 原始的文件
    """
    info = data.decode()
    logging.info("body数据{0}".format(info))
    # dataform = str(info).strip("'<>() ").replace('\'', '\"')
    dataform = str(info)
    json_data = json.loads(dataform)
    logging.info("json_data数据{0}".format(json_data))
    project = json_data["project"]
    project_name = json_data["project_name"]
    event = json_data["event"]
    rules = json_data["triggering_rules"]
    rules_name = ""
    if rules and len(rules) > 0:
        rules_name = ",".join(rules)
    app_version = event["dist"]
    url = json_data["url"]
    tags = event["tags"]
    host = info_tags("host", tags)
    path = info_tags("path", tags)
    q = info_tags("q", tags)
    issue_url = host + path
    if q and len(q) > 0:
        issue_url += "?" + q
    logging.info("准备发送请求")
    markdownModel = MarkDownModel(project, project_name, 'error', rules_name, app_version, issue_url, url)
    wechat_dict = markdownModel.mark_down_info()
    req2 = requests.post(
        url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0b0471ea-7b2d-4db0-a291-ae785ca8212e",
        headers={"Content-Type": "application/json"},
        data=json.dumps(wechat_dict).encode("utf-8"))

    logging.info("z执行结果{0}".format(req2.text))

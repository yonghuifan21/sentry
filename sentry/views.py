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
    error_msg = ""

    def __init__(self, project, project_name, level, rules_name, app_version, issue_url, url, error_msg):
        self.project = project
        self.project_name = project_name
        self.level = level
        self.rules_name = rules_name
        self.app_version = app_version
        self.issue_url = issue_url
        self.url = url
        self.error_msg = error_msg

    def mark_down_info(self):
        wechat_dict = {"msgtype": "markdown"}
        content = """移动端项目<font color=\"warning\">{0}-{1}</font>告警！\n
            >类型: <font color=\"warning\">{2}</font>
            >应用: <font color=\"info\">{3}</font>
            >版本号: <font color=\"info\">{4}</font>
	        >接口: <font color=\"info\">{5}</font>
	        >错误详情: <font color=\"info\">{6}</font>
 	        >详情: <font color=\"info\">[查看日志]({7})</font>
 	        >日志链接: <font color=\"info\">{8}</font>\n请关注:<@81095534><@81075463><@81137040><@81122647><@80727655>
        """.format(self.project_name,
                   self.project,
                   self.rules_name,
                   self.project,
                   self.app_version,
                   self.issue_url,
                   self.error_msg,
                   self.url,
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


def judgePostAlert(code, msg):
    """
    :param code 错误码
    :param msg 错误消息
    :return Bool True表示告警提示，False表示不报
    """
    # 如果错误码是200, 并且错误信息error_msg是空，不发送警告
    if not (code and len(code) > 0):
        return False
    if str(code) == "200" and not (msg and len(msg) > 0):
        return False
    return True


def judgePostAlertFilter(code, msg, path):
    """
    :param code 错误码
    :param msg 错误消息
    :return Bool True表示告警提示，False表示不报
    """
    # 如果错误码是200, 并且错误信息error_msg是空，不发送警告
    if not (code and len(code) > 0):
        return False
    # 在这个列表的取消的接口，都过滤掉
    cancelpathlist = ["/fresh/products/app/search",
                      "/fresh/app/product/search"]
    if str(code) == "-999" and (path in cancelpathlist):
        return False
    if str(code) == "200" and not (msg and len(msg) > 0):
        return False

    filterpathlist = ["/fresh/order/arrival",
                      "/fresh/order/canceled",
                      "/fresh/order/assigned",
                      "/fresh/order/delivery"]
    # 如果在列表中，不发送警告
    return not (path in filterpathlist)


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

    app_version = ''
    if "dist" in event.keys():
        app_version = event["dist"]

    url = ''
    if "url" in json_data.keys():
        url = json_data["url"]

    tags = event["tags"]
    host = info_tags("host", tags)
    path = info_tags("path", tags)
    error_msg = info_tags("resps", tags)
    error_code = info_tags("sc", tags)
    q = info_tags("q", tags)
    issue_url = host + path
    if q and len(q) > 0:
        issue_url += "?" + q
    join_error_msg = ""
    if error_code and len(error_code) > 0:
        join_error_msg += "错误码： {0}  ".format(error_code)
    if error_msg and len(error_msg) > 0:
        join_error_msg += "错误信息： {0}  ".format(error_msg)

    # 如果错误码是200, 并且错误信息error_msg是空，不发送警告
    if not judgePostAlertFilter(error_code, error_msg, path):
        return

    logging.info("准备发送请求")
    markdownModel = MarkDownModel(project, project_name, 'error', rules_name, app_version, issue_url, url,
                                  join_error_msg)
    wechat_dict = markdownModel.mark_down_info()
    req2 = requests.post(
        url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8796776b-58f4-4bc1-b30a-8af0f59e165a",
        headers={"Content-Type": "application/json"},
        data=json.dumps(wechat_dict).encode("utf-8"))

    logging.info("执行结果{0}".format(req2.text))

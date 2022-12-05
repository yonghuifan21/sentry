import schedule
import requests
import json


def postWeakPaperAlert():
    """
    自动执行脚本发送的定时任务
    """

    alertInfo = """
    curl 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ae7d48f4-0488-479a-906f-5dc79fd8c1c4' \
   -H 'Content-Type: application/json' \
   -d '
   {
    "msgtype": "text",
    "text": {
        "content": "写周报！！！写周报！！！写周报！！！",
		"mentioned_list":["@all"],
    }
    }' 
    """
    text_dict = {"content": "筒子们，写周报！！！写周报！！！写周报！！！", "mentioned_list": ["@all"]}
    wechat_dict = {"msgtype": "text", "text": text_dict}
    requests.post(
        url="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ae7d48f4-0488-479a-906f-5dc79fd8c1c4",
        headers={"Content-Type": "application/json"},
        data=json.dumps(wechat_dict).encode("utf-8"))


def job():
    schedule.every().sunday.at("19:30").do(postWeakPaperAlert)
    schedule.every().day.at("14:00").do(postWeakPaperAlert)

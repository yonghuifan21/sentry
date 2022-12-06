from django.db import models


class Events(models.Model):
    """
     事件详情
     id 主键
     event_id 事件_id
     date_time 事件插入日期
     event_msg 事件的具体内容
    """
    event_id = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now=True)
    event_msg = models.CharField(max_length=2000000)

    def __str__(self):
        return f"{self.event_id} {self.event_msg} {self.event_msg}"


class Warnings(models.Model):
    """
       所有的警告信息
       id 主键
       event_id 事件_id
       project 平台ios
       project_name 项目名
       version 版本号
       message 告警类型networkAnalysis
       tags_method 请求类型get/post
       tags_ac
       tags_app_device 设备唯一识别码
       tags_ce
       tags_cn
       tags_cs
       tags_de
       tags_device
       tags_dns
       tags_ds
       tags_du
       tags_environment
       tags_host
       tags_level
       tags_np
       tags_os
       tags_os_name
       tags_path
       tags_param
       tags_ree
       tags_resp
       tags_resps //错误类型
       tags_rs
       tags_rspe
       tags_rsps
       tags_sc //错误码
       tags_sce
       tags_scheme
       tags_scs
       tags_tls
       date_time 事件插入日期
   """
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    project = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)
    version = models.CharField(max_length=200)
    message = models.CharField(max_length=200)
    tags_method = models.CharField(max_length=200)
    tags_ac = models.CharField(max_length=200)
    tags_app_device = models.CharField(max_length=200)
    tags_ce = models.CharField(max_length=200)
    tags_cn = models.CharField(max_length=200)
    tags_cs = models.CharField(max_length=200)
    tags_de = models.CharField(max_length=200)
    tags_device = models.CharField(max_length=200)
    tags_dns = models.CharField(max_length=200)
    tags_ds = models.CharField(max_length=200)
    tags_du = models.CharField(max_length=200)
    tags_environment = models.CharField(max_length=200)
    tags_host = models.CharField(max_length=200)
    tags_level = models.CharField(max_length=200)
    tags_np = models.CharField(max_length=200)
    tags_os = models.CharField(max_length=200)
    tags_os_name = models.CharField(max_length=200)
    tags_path = models.CharField(max_length=200)
    tags_param = models.CharField(max_length=200)
    tags_ree = models.CharField(max_length=200)
    tags_resp = models.CharField(max_length=200)
    tags_resps = models.CharField(max_length=200)
    tags_rs = models.CharField(max_length=200)
    tags_rspe = models.CharField(max_length=200)
    tags_rsps = models.CharField(max_length=200)
    tags_sc = models.CharField(max_length=200)
    tags_sce = models.CharField(max_length=200)
    tags_scheme = models.CharField(max_length=200)
    tags_scs = models.CharField(max_length=200)
    tags_tls = models.CharField(max_length=200)
    date_time = models.DateTimeField(auto_now=True)

    # 符号化
    def __str__(self):
        return f"{self.project} {self.project_name} {self.project_name} {self.tags_host} {self.tags_path} {self.tags_param}"

    # # 获取7天内的数据
    # def recently_minute_data(self, distance):
    #     return self.date_time >= timezone.now() - datetime.timedelta(minutes=distance)

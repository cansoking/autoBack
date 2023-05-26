from django.db import models


# Create your models here.
class User(models.Model):
    # 用户名
    username = models.CharField(max_length=255)
    # id
    openid = models.CharField(max_length=255, primary_key=True)
    # 头像地址
    avatar_url = models.CharField(max_length=255)


class CheckLogs(models.Model):
    # 处理后图片
    after_img_path = models.CharField(max_length=255)
    # 错题数
    mistake_num = models.IntegerField()
    # 正确数量
    correct_num = models.IntegerField()
    # 总题数
    total_num = models.IntegerField()
    # 批改日期
    check_date = models.DateField(auto_now_add=True)
    # 所属用户
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    # 是否删除
    is_active = models.BooleanField(default=True)


class Question(models.Model):
    # 问题原式
    question = models.CharField(max_length=255)
    # 正确答案
    correct_answer = models.CharField(max_length=255)
    # 你的答案
    your_answer = models.CharField(max_length=255)
    # 题目类型
    type = models.CharField(max_length=255)
    # 是否加到错题本
    is_mark = models.BooleanField(default=False)
    # 所属批改记录
    checklogs = models.ForeignKey('CheckLogs', on_delete=models.SET_NULL, null=True)


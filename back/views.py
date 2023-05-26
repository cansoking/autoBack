import uuid
from datetime import datetime

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from utils.user_related import get_openid
from back.models import User, Question, CheckLogs
from libs.check_main import check_image
from libs.utils import generate_math_questions
from django.db.models import Count, Q, F


# Create your views here.
def index(request):
    return HttpResponse("Hello Wolrd")


# 登录注册
def login(request):
    if request.method == 'POST':
        code = request.POST.get('code', '')
        # 获取openid
        openid = get_openid(code)
        user = User.objects.filter(openid=openid)
        # 注册登录
        if len(user) == 0:
            new_user = User(
                username='用户' + openid[-5:],
                avatar_url='default.jpg',
                openid=openid
            )
            new_user.save()
            cur_user = new_user
        else:
            cur_user = user[0]
        ret_data = {
            'username': cur_user.username,
            'openid': cur_user.openid,
            'avatar_url': cur_user.avatar_url
        }
        return JsonResponse(ret_data)
    return HttpResponse('Login View')


# 修改用户个人信息
def modify_user(request):
    if request.method == 'POST':
        new_username = request.POST.get('username', '非法用户名')
        openid = request.POST.get('openid', '')
        user = User.objects.filter(openid=openid)
        is_modify_avatar = request.POST.get('is_modify_avatar', 0)
        if len(user) != 0:
            if is_modify_avatar == '1':
                # 保存本地
                avatar = request.FILES.get('avatar')
                default_storage.save('static/avatar/' + avatar.name, ContentFile(avatar.read()))
                user[0].avatar_url = avatar.name
            user[0].username = new_username
            user[0].save()
        ret = {
            'username': user[0].username,
            'openid': user[0].openid,
            'avatar_url': user[0].avatar_url
        }
        return JsonResponse(ret)
    return HttpResponse("modify user view")


def check(request):
    if request.method == 'POST':
        # 获取openid和保存问题图片
        openid = request.POST.get('openid', '')
        question_img = request.FILES.get('question')
        before_path = 'static/question_image/before/' + question_img.name
        after_path = 'static/question_image/after/' + question_img.name
        default_storage.save(before_path, ContentFile(question_img.read()))
        # 调用批改
        questions = check_image(before_path, True, after_path)
        # 存储
        new_questions = []
        ret_questions = []
        correct_num = 0
        mistake_num = 0
        # 解析问题
        for question in questions:
            complete_text = ''.join(question)
            # 检测式子合法性
            if '=' in complete_text:
                single_dict = {}
                # 分割式子
                formulas = complete_text.split('=')
                pure_question = formulas[0]
                your_answer = formulas[1]
                single_dict['question'] = pure_question
                single_dict['your_answer'] = "无" if your_answer == "" else your_answer
                # 判断问题类型
                type_flag = [False, False, False, False]
                types = ['加法', '减法', '乘法', '除法']
                if '+' in pure_question:
                    type_flag[0] = True
                if '-' in pure_question:
                    type_flag[1] = True
                if '×' in pure_question:
                    type_flag[2] = True
                if '÷' in pure_question:
                    type_flag[3] = True
                type_name = ''
                count = 0
                for idx, type_flag_single in enumerate(type_flag):
                    if type_flag_single:
                        type_name = types[idx]
                        count += 1
                if count > 1:
                    type_name = '混合'
                single_dict['type'] = type_name
                # 计算正确答案
                correct_answer = eval(pure_question.replace("÷", "/").replace("×", "*"))
                single_dict['correct_answer'] = correct_answer
                # 计算是否正确
                is_cor = False
                if your_answer != '' and int(correct_answer) == int(your_answer):
                    is_cor = True
                    correct_num += 1
                else:
                    mistake_num += 1
                single_dict['is_correct'] = is_cor
                single_dict['is_mark'] = not is_cor
                # 存入对象
                new_questions.append(Question(
                    question=pure_question,
                    correct_answer=str(correct_answer),
                    your_answer=str(your_answer),
                    type=type_name,
                    is_mark=not is_cor,
                    checklogs=None
                ))
                ret_questions.append(single_dict)
        # 分析数据
        checklogs = CheckLogs(
            after_img_path=after_path,
            mistake_num=mistake_num,
            correct_num=correct_num,
            total_num=correct_num + mistake_num,
            user=User.objects.filter(openid=openid)[0]
        )
        checklogs.save()
        for idx, cur_ques in enumerate(new_questions):
            cur_ques.checklogs = checklogs
            cur_ques.save()
            ret_questions[idx]['id'] = cur_ques.id
        # 构建返回数据
        ret = {
            'total_num': checklogs.total_num,
            'correct_num': checklogs.correct_num,
            'mistake_num': checklogs.mistake_num,
            'after_img_path': checklogs.after_img_path,
            'questions': ret_questions
        }
        return JsonResponse(ret)
    return HttpResponse('check view')


# 获取错题本
def get_errors(request):
    if request.method == 'GET':
        openid = request.GET.get('openid', '')
        questions = Question.objects.filter(checklogs__user__openid=openid, is_mark=True)
        return JsonResponse({
            'totalNum': len(questions),
            'items': [
                {
                    'your_answer': "没有做出来哦" if question.your_answer == "" else question.your_answer,
                    'correct_answer': question.correct_answer,
                    'question': question.question,
                    'error_id': question.id
                }
                for question in questions
            ]
        })
    return HttpResponse("get errors view")


# 掌握错题
def deactive_question(request):
    if request.method == 'POST':
        question_id = request.POST.get('ques_id', '')
        question = Question.objects.filter(id=question_id)[0]
        question.is_mark = False
        question.save()
        return JsonResponse({
            'msg': '成功',
            'statuscode': 200
        })
    return HttpResponse('deactive question view')


# 获取记录
def get_logs(request):
    if request.method == 'GET':
        openid = request.GET.get('openid', '')
        logs = CheckLogs.objects.filter(user__openid=openid, is_active=True)
        return JsonResponse({
            'totalNum': len(logs),
            'items': [
                {
                    "correct_num": log.correct_num,
                    "mistake_num": log.mistake_num,
                    "total_num": log.total_num,
                    "img_path": log.after_img_path,
                    "date": log.check_date,
                    "id": log.id
                }
                for log in logs
            ]
        })
    return HttpResponse("get logs view")


# 删除记录
def delete_log(request):
    if request.method == 'POST':
        log_id = request.POST.get('log_id', '')
        log = CheckLogs.objects.filter(id=log_id)[0]
        log.is_active = False
        log.save()
        return JsonResponse({
            'msg': '成功',
            'statuscode': 200
        })
    return HttpResponse('delete log view')


# 收藏错题
def mark_question(request):
    if request.method == 'POST':
        ques_id = request.POST.get('ques_id', '')
        question = Question.objects.filter(id=ques_id)[0]
        question.is_mark = True
        question.save()
        return JsonResponse({
            'msg': '成功',
            'statuscode': 200
        })
    return HttpResponse('mark question view')


# 随机出题
def get_random_questions(request):
    if request.method == 'POST':
        minNum = int(request.POST.get('minNum', 1))
        maxNum = int(request.POST.get('maxNum', 10))
        opretors = list(request.POST.get('opretors', "'+', '-'").replace(",", ""))
        question_image_data = generate_math_questions(num_min=minNum, num_max=maxNum, operators=opretors)
        # 生成一个随机的唯一标识符（UUID）
        filename = str(uuid.uuid4())
        # 在文件名前加上前缀
        filename = "static/question_image/generate/" + filename + ".png"
        question_image_data.save(filename)
        return JsonResponse({
            'img_path': filename
        })

    return HttpResponse("get random questions view")


# 获取建议
def get_advice(request):
    if request.method == 'POST':
        openid = request.POST.get("openid", "")
        all_questions = Question.objects.filter(checklogs__user__openid=openid)

        # 总做题数
        total_count = all_questions.count()

        # 正确的题数
        correct_count = all_questions.filter(correct_answer=F('your_answer')).count()

        # 错题数
        wrong_count = total_count - correct_count

        # 不同类型题目的错题数
        types = all_questions.values('type').annotate(
            total=Count('id'),
            wrong=Count('id', ~Q(correct_answer=F('your_answer')))
        )

        # 在错题中哪种类型的题目占比最大
        max_wrong_type = None
        max_wrong_ratio = 0
        for t in types:
            if t['wrong'] / wrong_count > max_wrong_ratio:
                max_wrong_type = t['type']
                max_wrong_ratio = t['wrong'] / wrong_count

        # 加强哪些类型的题目
        strengthen_types = []
        for t in types:
            if t['wrong'] > 0 and t['wrong'] / t['total'] >= 0.5:
                strengthen_types.append(t['type'])

                # 第一次批改记录的时间距今的天数
                first_check_date = CheckLogs.objects.filter(user__openid=openid).order_by(
                    'check_date').first().check_date
                days_since_first_check = (datetime.now().date() - first_check_date).days

        analysis = {
            'total_count': total_count,
            'correct_count': correct_count,
            'wrong_count': wrong_count,
            'types': list(types),
            'max_wrong_type': max_wrong_type,
            'strengthen_types': strengthen_types,
            "days_since_first_check": days_since_first_check
        }

        return JsonResponse({'analysis': analysis})
    return HttpResponse('get advice view')

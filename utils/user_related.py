import requests


def get_openid(code):
    # 请求信息
    APPID = 'wxd2d4b4943a1010a9'
    SECRET = '76d96b9f779b3427f94b54606287d608'
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    res = requests.get(url=url, params={
        'appid': APPID,
        'secret': SECRET,
        'js_code': code,
        'grant_type': 'authorization_code'
    })

    return res.json()['openid']


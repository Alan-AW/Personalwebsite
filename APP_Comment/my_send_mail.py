from django.core.mail import EmailMultiAlternatives
from django.conf import settings as sys


def send_email(nickname, content, email,article_title,article_id):
    # subject 主题 content 内容 to_addr 是一个列表，发送给哪些人
    # 情况一、给自己发送
    # 1.1、留言信息
    # 需要的参数：昵称、内容、留言者email
    subject = '有新的留言消息'
    send_content = """
            <p>留言板新增一条留言：</p>
            <p>%s说:%s</p>
            <p>去留言板看看<a href='https://www.missyouc.cn/blog/leavemessage/'></a></p>
        """ % (nickname, content)
    msg = EmailMultiAlternatives(subject, send_content, sys.EMAIL_HOST_USER, [email, ])
    msg.content_subtype = "html"
    # 添加附件（可选）
    # msg.attach_file('./twz.pdf')
    # 发送
    msg.send()

    aa = 'https://picsum.photos/360/460?random=1'  # 随机生成一张假图片

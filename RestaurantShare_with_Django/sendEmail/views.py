from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
from shareRes.models import Restaurant
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from shareRes.models import Category


def sendEmail(request):
    checked_res_list = request.POST.getlist('checks')
    inputReceiver = request.POST['inputReceiver']
    inputTitle = request.POST['inputTitle']
    inputContent = request.POST['inputContent']
    print(checked_res_list,"/",inputReceiver,"/",inputTitle,"/",inputContent)

    try:
        # smtp using - 구글 smtp 이용
        # smtp_mail(checked_res_list, inputReceiver, inputTitle, inputContent)

        #django send_mail() - https://docs.djangoproject.com/en/2.2/topics/email/
        # 구글 smtp 이용, 셋팅정보는 settings.py의 Email settings 참조
        django_mail_func(checked_res_list, inputReceiver, inputTitle, inputContent)
        return render(request,'sendEmail/email_success.html')
    except Exception as e:
        print(e)
        content = {'error': e}
        return render(request,'sendEmail/email_error.html', content)


def smtp_mail(checked_res_list, inputReceiver, inputTitle, inputContent):
    mail_html = "<html><body>"
    mail_html += "<h1> 맛집 공유 </h1>"
    mail_html += "<p>" + inputContent + "<br>"
    mail_html += "발신자님께서 공유하신 맛집은 다음과 같습니다.</p>"
    for checked_res_id in checked_res_list:
        restaurant = Restaurant.objects.get(id=checked_res_id)
        mail_html += "<h2>" + restaurant.restaurant_name + "</h2>"
        mail_html += "<h4>* 관련 링크</h4>" + "<p>" + restaurant.restaurant_link + "</p><br>"
        mail_html += "<h4>* 상세 내용</h4>" + "<p>" + restaurant.restaurant_content + "</p><br>"
        mail_html += "<h4>* 관련 키워드</h4>" + "<p>" + restaurant.restaurant_keyword + "</p><br>"
        mail_html += "<br>"
        mail_html += "</body></html>"
        print(mail_html)

        # smtp using
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('gkwlsdn17@gmail.com', 'password')

        msg = MIMEMultipart('alternative')
        msg['Subject'] = inputTitle
        msg['From'] = 'gkwlsdn17@gmail.com'
        msg['To'] = inputReceiver
        mail_html = MIMEText(mail_html, 'html')
        msg.attach(mail_html)
        print(msg['To'], type(msg['To']))
        server.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
        server.quit()

def django_mail_func(checked_res_list, inputReceiver, inputTitle, inputContent):
    try:
        restaurants = []
        for checked_res_id in checked_res_list:
            restaurants.append(Restaurant.objects.get(id=checked_res_id))

        content = {'inputContent': inputContent, 'restaurants': restaurants}

        msg_html = render_to_string('sendEmail/email_format.html',content)

        msg = EmailMessage(subject = inputTitle, body=msg_html, from_email="gkwlsdn17@gmail.com", bcc=inputReceiver.split(','))
        msg.content_subtype = 'html'
        msg.send()
    except Exception as e:
        raise Exception(e)

def combackHome(request):
    return HttpResponseRedirect(reverse('index'))
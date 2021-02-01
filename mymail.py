import smtplib

def send_email(recepient,mydict):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("nasimqwe", "11290011")
    s = str()
    s1 = str()
    for k,v in mydict.items():
         s1 = k + ':' + v + ' \n'
         s = s+s1
    sub = "CVASU Student DB "
    message = 'Subject: {}\n\n{}'.format(sub, s)
    server.sendmail(
      "nasimqwe@gmail.com", 
      recepient, 
      message)
    server.quit()

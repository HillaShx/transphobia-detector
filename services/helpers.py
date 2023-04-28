import yagmail

nily_email = 'nily@maavarim.org'
email_pass = 'pswhnpxqststlrvd'

# path example
path = r"C:\Users\Administrator\PycharmProjects\d40_dyke\transphobia-detector\routers\testgmail.csv"


def send_yagmail():
    try:
        yagmail.register(nily_email, email_pass)
        receiver = "galdel9@gmail.com"
        body = "TEST Yagmail"
        # real path of csv file
        filename = path

        yag = yagmail.SMTP(nily_email)
        yag.send(
            to=receiver,
            subject="Yagmail test with attachment",
            contents=body,
            attachments=filename,
        )
        print('sent')
    except Exception as err:
        print('send_yagmail err: ', err)


send_yagmail()

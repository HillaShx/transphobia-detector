import yagmail

nily_email = 'nily@maavarim.org'
email_pass = 'pswhnpxqststlrvd'

# path example
path = r"C:\Users\Administrator\PycharmProjects\d40_dyke\transphobia-detector\routers\testgmail.csv"


def send_yagmail(send_to: str, attachment_path: str):
    try:
        yagmail.register(nily_email, email_pass)
        body = "TEST Yagmail"

        yag = yagmail.SMTP(nily_email)
        yag.send(
            to=send_to,
            subject="Yagmail test with attachment",
            contents=body,
            attachments=attachment_path,
        )
        print('sent')
    except Exception as err:
        print('send_yagmail err: ', err)



import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from processor.logger import exc
import threading


def email_notification(img_disp, action_detected, sender_email, receiver_email, password):
    try:
        subject = action_detected
        body = "This is an email with attachment sent from Python"
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(body, "plain"))
        filename = img_disp
        # Open PDF file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, text)
    except Exception as e:
        # Print any error messages to stdout
        exc.exception('error occurred in email send notification {}'.format(e))
    finally:
        server.quit()


def email_image_notification(img_disp, action_detected, sender_email, receiver_email, password):
    email = threading.Thread(target=email_notification, args=(img_disp, action_detected, sender_email, receiver_email, password))
    email.start()



# def html_send_notification(img_disp, action_detected, Sender_Email, Reciever_Email,):
#     try:
#         trace.info('Sending email notification...')
#         sender_email = Sender_Email
#         receiver_email =Reciever_Email
#         password = "Ptstest@123"
#
#         message = MIMEMultipart("alternative")
#         message["Subject"] = "multipart test"
#         message["From"] = sender_email
#         message["To"] = receiver_email
#
#         # Create the plain-text and HTML version of your message
#         text = """\
#         Hi,
#         How are you?
#         Real Python has many great tutorials:
#         www.realpython.com"""
#         html = """\
#         <html>
#            <head>
#               <title>HTML img Tag</title>
#            </head>
#
#            <body>
#               <img src="Tampering02_12_2021_TIME_13_45_04.jpg" alt="Simply Easy Learning" width="200" height="80">
#            </body>
#         </html>
#         """
#
#         # Turn these into plain/html MIMEText objects
#         part1 = MIMEText(text, "plain")
#         part2 = MIMEText(html, "html")
#
#         # Add HTML/plain-text parts to MIMEMultipart message
#         # The email client will try to render the last part first
#         message.attach(part1)
#         message.attach(part2)
#
#         # Create secure connection with server and send email
#         context = ssl.create_default_context()
#         with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#             server.login(sender_email, password)
#             server.sendmail(
#                 sender_email, receiver_email, message.as_string()
#             )
#     except Exception as ex:
#         exc.exception('Failed to send email notification {}'.format(ex))

import smtplib
import json
import imghdr
import os
from email.message import EmailMessage
from email.utils import make_msgid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

def meeting_request_email_automation(message, receiver, visitor_image_name_as_attachment):
    me = "ishita.katyal@paritysystems.in"
    you = receiver
    password = input("Password: ")
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('multipart')
    msg['Subject'] = "Meeting Request Email"
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).    
    text = str(json.dumps(message))
    html_buttons = """\
        <html>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" />
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script> 
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script> 
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script> 
            <style type="text/css">   
        .top-left { 
            top: 0; 
            left: 20%; 
        }        
        .top-center {
            top: 0;
            left: 50%;
            right: 50%;
        } 
        .top-right { 
            top: 0; 
            left: 80%;
            right:20%; 
        }
        .button_accept {
            color: white;
            background-color: #4CAF50;
        } 
        .button_delay {
            color: white;
            background-color: #0000FF;
        }
        .button_reject {
            color: white;
            background-color: #f44336;
        }
        </style>
            <body>
                <div id="speech"><p>Hello, Someone is here to meet you. Kindly look into the details and reply asap.</p></div>
                <div class="container h-100"> 
                    <div class="position-relative h-100"> 
                        <div class="position-absolute top-left"> 
                            <button type="button_accept" class="btn btn-primary">Accept!</button><br><br>
                        </div>
                        <div class="position-absolute top-center"> 
                            <button type="button_delay" class="btn btn-primary" style="float:center;">Delay by 10 minutes!</button></div> 
                        <div class="position-absolute top-right"> 
                            <button type="button_reject" class="btn btn-primary" style="float:right;">Reject. We'll meet some other time!</button></div>
                    </div>
                </div>
                <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script> 
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>    
            </body>
        <html>
    """
    # Record the MIME types of both parts - text/plain and text/html.
    part2 = MIMEText(text, 'plain')
    part3 = MIMEText(html_buttons, 'html')
    part4 = open(visitor_image_name_as_attachment, 'rb').read()

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part2)
    msg.attach(part3)
    image = MIMEImage(part4, name=os.path.basename(visitor_image_name_as_attachment))
    msg.attach(image)
    print(msg)
    
    # Send the message via local SMTP server.
    s = smtplib.SMTP_SSL('smtp.zoho.com', 465)
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.login(me, password)
    s.sendmail(me, you, msg.as_string())
    s.quit()

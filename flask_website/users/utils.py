import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_website import mail

def save_pic(form_pic):
    rand_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_pic.filename)
    pic_name = rand_hex + file_ext
    pic_path = os.path.join(current_app.root_path, 'static/profile_pics', pic_name)
    output_size = (125, 125)
    img = Image.open(form_pic)
    img.thumbnail(output_size)
    img.save(pic_path)
    return pic_name

def send_reset_email(user):
    token = user.get_reset_token()
    message = Message('Password Reset Request', sender = 'noreply@demo.com', 
                      recipients = [user.email])
    message.body = f'''To reset your password, please visit the following link:
{url_for('users.reset_token', token = token, _external = True)}
If you did not make this request, ignore this email and no changes will be made
    '''
    mail.send(message)
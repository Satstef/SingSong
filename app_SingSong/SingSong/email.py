from . import mail
from flask_mail import Message
from flask import current_app, render_template
from threading import Thread

"""La funzione mail.send() blocca l’applicazione durante l’operazione di spedizione.
Per questo l’operazione stessa viene delegata ad un thread che lavora in background,
evitando che il browser e tutta l’applicazione rimangano in attesa."""
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject, sender=app.config["MAIL_USERNAME"], recipients=[to])
    # Si invia o msg.html o msg.body che sono la stessa cosa
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

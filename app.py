import smtplib

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Comment
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


app = Flask(__name__)

engine = create_engine('sqlite:///comments.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def mail(subj, email, mess, per):
    addr_from = "herokusite@gmail.com"
    addr_to = "andreilukin88@gmail.com"
    password = "hb1641012"

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = subj

    body = str(per) + '\n' + str(email) + '\n' + str(mess)
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.set_debuglevel(True)
    server.starttls()
    server.login(addr_from, password)
    try:
        server.send_message(msg)
    except:
        return "Your message is missing"
    server.quit()


@app.route('/comments')
def comment():
    comments = session.query(Comment).all()
    return render_template("comments.html", comments=comments)


@app.route('/', methods=['GET', 'POST'])
def index() -> 'html':
    if request.method == 'POST':
        newComment = Comment(
            name=request.form['name'],
            email=request.form['email'],
            subject=request.form['subject'],
            message=request.form['message']
            )
        session.add(newComment)
        session.commit()
        mail(
            request.form['subject'],
            request.form['email'],
            request.form['message'],
            request.form['name']
            )
        return render_template('index.html')
    else:
        return render_template('index.html')


@app.route('/del/<int:comment_id>/delete/', methods=['GET', 'POST'])
def deleteComment(comment_id):
    commentToDelete = session.query(Comment).filter_by(id=comment_id)
    commentToDelete = commentToDelete.one()
    if request.method != 'POST':
        session.delete(commentToDelete)
        session.commit()
        return redirect(url_for('comment', comment=commentToDelete))


if __name__ == '__main__':
    app.run(debug=True)

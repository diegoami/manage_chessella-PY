import smtplib
from email.mime.text import MIMEText
import environment_data as env
from add_game_wf import do_add_game_workflow
from check_status_wf import verify_up
from sendmail_wf import sendmail_success



if __name__ == "__main__":

    text_mail = ""
    if verify_up():
        print("Server is up, ok to add game")

        ok, text_mail = do_add_game_workflow()
    else:
        ok, text_mail = False, "Chessella does not seem to be up"
    print(ok, text_mail)
    sendmail_success("Chessella OK: "+str(ok),text_mail)
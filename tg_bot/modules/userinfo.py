from telegram.ext import CommandHandler
from telegram.ext.dispatcher import run_async

from tg_bot import dispatcher
import tg_bot.modules.sql.userinfo_sql as sql


@run_async
def about_user(bot, update):
    message = update.effective_message
    is_reply = message.reply_to_message is not None
    if is_reply:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.from_user.id

    info = sql.get_user_info(user_id)

    if info:
        update.effective_message.reply_text(info)
    elif is_reply:
        username = message.reply_to_message.from_user.first_name
        update.effective_message.reply_text(username + " hasn't set an info message about himself yet!")
    else:
        update.effective_message.reply_text("You haven't set an info message about yourself yet!")


def set_about_user(bot, update):
    message = update.effective_message
    user_id = message.from_user.id
    text = message.text
    info = text.split(None, 1)[1]  # use python's maxsplit to only remove the cmd, hence keeping newlines.
    sql.set_user_info(user_id, info)
    update.effective_message.reply_text("Updated your info!")


SET_ABOUT_HANDLER = CommandHandler("setme", set_about_user)
GET_ABOUT_HANDLER = CommandHandler("me", about_user)

dispatcher.add_handler(SET_ABOUT_HANDLER)
dispatcher.add_handler(GET_ABOUT_HANDLER)
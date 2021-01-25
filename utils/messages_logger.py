import logging

from telegram.utils.helpers import mention_html

from communication_interfaces.telegram_interface.tg_singleton import TelegramMessagesWrapper

logger = logging.getLogger("commands_logger")


def log_command(fn):
    def wrapper(*args, **kwargs):
        update = args[0]
        command = fn.__name__
        result = fn(*args, **kwargs)

        user = f'{mention_html(update.effective_user.id, update.effective_user.first_name)}' if update.effective_user else ""

        title = update.effective_chat.title if update.effective_chat else ""

        log_text = (
            f"Chat: {update.message.chat.id} (Title <i>{title}</i>) (User {user}), "
            f"Command: {command}, "
            f"Message: {update.message.text}, "
            f"Result-Code: {result}"
        )

        logger.info(log_text)
        try:
            TelegramMessagesWrapper.send_command(log_text)
        except Exception as e:
            logger.error(e)
        return result

    return wrapper


def log_callbacks(fn):
    def wrapper(*args, **kwargs):
        chat_id = args[0].callback_query.message.chat.id
        command = fn.__name__
        message = args[0].callback_query.data
        question = args[0].callback_query.message.text.replace("\n", " ")
        result = fn(*args, **kwargs)
        log_text = (
            f"Chat: {chat_id}, "
            f"Conversation: {command}, "
            f"Question: '{question}', "
            f"Message: '{message}', "
            f"Result-Code: {result}"
        )
        logger.info(log_text)
        try:
            TelegramMessagesWrapper.send_command(log_text)
        except Exception as e:
            logger.error(e)
        return result

    return wrapper

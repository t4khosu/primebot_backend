import logging
import sys
import traceback

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler
from telegram.ext.filters import Filters
from telegram.utils.helpers import mention_html

from communication_interfaces.base_bot import Bot
from communication_interfaces.telegram_interface.commands import single_commands
from communication_interfaces.telegram_interface.conversations import settings_conversation
from communication_interfaces.telegram_interface.conversations import start_conversation
from communication_interfaces.telegram_interface.conversations.settings_conversation import \
    callback_query_settings_handlers
from prime_league_bot import settings


class TelegramBot(Bot):
    """
    Botfather Class. Provides Communication with Bot(Telegram API) and Client
    """

    def __init__(self):
        super().__init__(
            bot=Updater,
            bot_config={
                "token": settings.TELEGRAM_BOT_KEY,
                "use_context": True
            }
        )

    def _initialize(self):
        dp = self.bot.dispatcher

        commands = [
            CommandHandler("cancel", single_commands.cancel),
            CommandHandler("help", single_commands.helpcommand),
            CommandHandler("issue", single_commands.issue),
            CommandHandler("feedback", single_commands.feedback),
            CommandHandler("bop", single_commands.bop),
            CommandHandler("explain", single_commands.explain),
            CommandHandler("setlogo", single_commands.set_logo),
            MessageHandler(Filters.status_update.migrate, settings_conversation.migrate_chat)  # Migration
        ]

        start_conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', start_conversation.start, )],

            states={
                1: [MessageHandler(Filters.text & (~Filters.command), start_conversation.team_registration), ],
            },

            fallbacks=commands
        )

        # Allgemeine Commands
        dp.add_handler(start_conv_handler)
        for cmd in commands[1:]:
            dp.add_handler(cmd)

        # Main Menu
        dp.add_handler(CommandHandler('settings', settings_conversation.start_settings))
        dp.add_handler(CallbackQueryHandler(settings_conversation.main_settings_menu, pattern='main'))
        dp.add_handler(CallbackQueryHandler(settings_conversation.main_settings_menu_close, pattern='close'))
        dp.add_handler(CallbackQueryHandler(start_conversation.finish_registration, pattern='0no'))
        dp.add_handler(CallbackQueryHandler(start_conversation.set_optional_photo, pattern='0yes'))
        # Chat Migration

        dp.add_error_handler(error)

        for i in callback_query_settings_handlers:
            dp.add_handler(i)

    def run(self):
        self.bot.start_polling()  # TODO: try catch connection errors
        self.bot.idle()

    @staticmethod
    def send_message():
        # TODO implement Telepot code here
        pass


def error(update, context):
    devs = [settings.TG_DEVELOPER_GROUP]
    try:
        if update is not None:
            if update.effective_message:
                text = "Hey. I'm sorry to inform you that an error happened while I tried to handle your request. " \
                       "My developer(s) will be notified."
                update.effective_message.reply_text(text)
            trace = "".join(traceback.format_tb(sys.exc_info()[2]))
            payload = ""
            if update.effective_user:
                payload += f' with the user {mention_html(update.effective_user.id, update.effective_user.first_name)}'
            if update.effective_chat:
                payload += f' within the chat <i>{update.effective_chat.title}</i>'
                if update.effective_chat.username:
                    payload += f' (@{update.effective_chat.username})'
            if update.poll:
                payload += f' with the poll id {update.poll.id}.'
            text = f"Hey.\n The error <code>{context.error}</code> happened{payload}. The full traceback:\n\n<code>{trace}" \
                   f"</code>"
        else:
            text = "Ein Fehler ist aufgetreten (update is none)."
    except Exception as e:
        text = f"Ein gravierender Fehler ist aufgetreten.\n{e}"
    for dev_id in devs:
        context.bot.send_message(dev_id, text, parse_mode=ParseMode.HTML)  # TODO: catch connection errors
    # we raise the error again, so the logger module catches it. If you don't use the logger module, use it.
    try:
        raise
    except RuntimeError as e:
        logging.getLogger("django").critical(e)

import emoji


def send_markdown_message(bot, chat_id, message):
    bot.sendMessage(
        chat_id,
        emoji.emojize(message, use_aliases=True),
        parse_mode='Markdown',
    )

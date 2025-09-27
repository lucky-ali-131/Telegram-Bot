from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import wikipedia
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Default language
wikipedia.set_lang("en")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Ask me anything, and I'll fetch the Wikipedia answer for you. \n\nCreated by: LuckyAli"
    )

async def wiki_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    logger.info(f"Searching Wikipedia for: {query}")

    try:
        summary = wikipedia.summary(query, sentences=3, auto_suggest=True, redirect=True)
        page = wikipedia.page(query, auto_suggest=True, redirect=True)

        reply = f"*{page.title}*\n\n{summary}\n\n[Read more]({page.url})"
        await update.message.reply_text(reply, parse_mode="Markdown")

    except wikipedia.DisambiguationError as e:
        await update.message.reply_text(
            f"Your query matched multiple results. Please be more specific.\n\nOptions:\n{', '.join(e.options[:10])}"
        )

    except wikipedia.PageError:
        await update.message.reply_text("Sorry, I couldn't find any answer on Wikipedia.")

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Something went wrong while fetching data from Wikipedia.")

def main():
    token = ""  # Replace this with your bot token
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), wiki_search))

    app.run_polling()

if __name__ == "__main__":
    main()


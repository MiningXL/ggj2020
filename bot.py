from telegram.ext import Updater, CommandHandler, BaseFilter, MessageHandler, Filters
import queue


class Flower_Filter(BaseFilter):
    flower_emojis = ["🌻", "🌼", "🌸", "🌺", "🥀", "🌹", "🌷", "💐", "🌾", "flower"]
    def filter(self, message):
        for f in Flower_Filter.flower_emojis:
            if f in message.text.lower():
                return True
        return False

class Honey_Filter(BaseFilter):
    def filter(self,message):
        honey = ["honey", "honeey", "🍯"]
        for h in honey:
            if h in message.text.lower():
                return True
        return False

class Intruder_Filter(BaseFilter):
    def filter(self,message):
        intruders = ["wasp", "bee", "🐝"]
        for h in intruders:
            if h in message.text.lower():
                return True
        return False


class Bot:
    def __init__(self, queue):
        self.queue = queue
        with open("keyfile") as keyfile:
            token = keyfile.read()
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        start_handler = CommandHandler('start', self.start_message)
        self.dispatcher.add_handler(start_handler)
        self.add_flower_handler()
        self.add_honey_handler()
        self.add_intruder_handler()
        self.add_unknown_handler()
        self.start()


    def unknown(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="that's not a floweer! Wee need more floweers for honeey")
    def thank(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Thanks for thee floweer! Yum")
        self.queue.put("flower")
    def honey(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="How did you get that‽ Give that back!")
    def intruder(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Aawwww an intruder!! Defenders go attack!!!")
        self.queue.put("intruder")
    def start_message(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm the beehive, please bee nice and send flowers, wee are hungry.\nDon' bee nasty.")

    def add_flower_handler(self):
        flower_filter = Flower_Filter()
        flower_handler = MessageHandler(flower_filter, self.thank)
        self.dispatcher.add_handler(flower_handler)

    def add_honey_handler(self):
        honey_filter = Honey_Filter()
        honey_handler = MessageHandler(honey_filter, self.honey)
        self.dispatcher.add_handler(honey_handler)

    def add_intruder_handler(self):
        intruder_filter = Intruder_Filter()
        intruder_handler = MessageHandler(intruder_filter, self.intruder)
        self.dispatcher.add_handler(intruder_handler)

    def add_handler(self, filter_text, message):
        class Filter(BaseFilter):
            def filter(self, message):
                for t in filter_text:
                    if t in message.text:
                        return True
                return False
        def intruder(update, context):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Aawwww an intruder!! Defenders go attack!!!")
        _filter = Filter()
        handler = MessageHandler(_filter, reply)
        self.dispatcher.add_handler(handler)

    def add_unknown_handler(self):
        unknown_handler = MessageHandler(Filters.text, self.unknown)
        self.dispatcher.add_handler(unknown_handler)

    def start(self):
        self.updater.start_polling()

if __name__ == "__main__":
    q = queue.Queue()
    bot = Bot(q)

from django.core.management.base import BaseCommand

from ...loader import bot

class Command(BaseCommand):

    def handle(self, *args, **options):
        from ... import handlers
        print('Bot ishlayapti')
        bot.infinity_polling()





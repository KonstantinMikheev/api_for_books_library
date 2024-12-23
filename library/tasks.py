from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from library.models import Rental


@shared_task
def checking_deadline():
    """This task is scheduled to run every day.
    It checks the expiration date of rentals and sends an email to renters if the rental period is over."""
    rents = Rental.objects.filter(deadline__lte=timezone.now(), is_returned=False)
    if rents:
        for rent in rents:
            send_mail(
                subject=f"Срок возвращения арендованной книги: {rent.book.title}",
                message=f"""Здравствуйте! {rent.rental_date} Вами взята из библиотеки книга {rent.book.title}. 
                Пришло время ее вернуть. Спасибо за понимание.""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=rent.reader.email,
            )

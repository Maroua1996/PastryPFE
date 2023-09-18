from notification.models import Notification


def user_notif(request):
  context = {}
  if request.user.is_authenticated:
    notifications = Notification.objects.filter(user=request.user).order_by('-create_date')
    unread = notifications.exclude(is_seen=True)
    context['unread'] = unread.count()
    context['notifications'] = notifications
  return context
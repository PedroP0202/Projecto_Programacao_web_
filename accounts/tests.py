from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import MagicLoginToken


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class MagicLinkTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='gestor',
            email='gestor@example.com',
            password='gestor1234',
        )

    def test_magic_link_request_sends_email_and_creates_token(self):
        response = self.client.post(
            reverse('accounts:login'),
            {
                'auth_method': 'magic_link',
                'email': 'gestor@example.com',
            },
        )

        self.assertRedirects(response, reverse('accounts:login'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(MagicLoginToken.objects.count(), 1)
        self.assertIn(str(MagicLoginToken.objects.first().token), mail.outbox[0].body)

    def test_magic_link_logs_user_in_once(self):
        token = MagicLoginToken.objects.create(user=self.user)
        response = self.client.get(
            reverse('accounts:magic_login', kwargs={'token': token.token})
        )

        self.assertRedirects(response, reverse('home'))
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

        self.client.logout()
        response = self.client.get(
            reverse('accounts:magic_login', kwargs={'token': token.token})
        )

        self.assertRedirects(response, reverse('accounts:login'))
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_expired_magic_link_does_not_login(self):
        token = MagicLoginToken.objects.create(user=self.user)
        token.created_at = timezone.now() - timedelta(minutes=16)
        token.save(update_fields=['created_at'])

        response = self.client.get(
            reverse('accounts:magic_login', kwargs={'token': token.token})
        )

        self.assertRedirects(response, reverse('accounts:login'))
        self.assertNotIn('_auth_user_id', self.client.session)

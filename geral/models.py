from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.db.models.signals import post_save
from simple_history.models import HistoricalRecords

from geral.mail_shortcuts import sendgrid_lancamento


class Associado(models.Model):

    user = models.OneToOneField(
            User,
            on_delete=models.CASCADE,
            related_name="associado",
            null=True, blank=True)

    ativo = models.BooleanField(default=True)
    last_modified = models.DateTimeField(auto_now=True)

    # Foto
    avatar = models.ImageField(upload_to='fotos', blank=True, null=True)

    avatar_profile = ImageSpecField(source='avatar',
                                    processors=[ResizeToFill(170, 170)],
                                    format='JPEG',
                                    options={'quality': 90})

    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(60, 60)],
                                      format='JPEG',
                                      options={'quality': 80})

    telefone = models.CharField(max_length=32)
    cpf = models.CharField(max_length=32)
    enderço = models.CharField(max_length=128)
    contato_emergencia = models.CharField(max_length=128)
    mestre = models.CharField(max_length=32)

    def __str__(self):
        return self.user.__str__()

    def is_in_starving_hacker(self):
        # TODO: Retorna de o Associado estah em Starving Hacker
        pass

    def get_last_plano(self):
        # TODO: Refatorar
        return Plano.objects.filter(user=self.user).latest('created_on')


def create_user_associado(sender, instance, created, **kwargs):

    if kwargs.get('raw', False):
        # https://code.djangoproject.com/ticket/17880
        return

    if created:
        try:
            if instance.associado is not None:
                pass
        except User.associado.RelatedObjectDoesNotExist:
            Associado.objects.create(user=instance)
            Lancamento.objects.create(
                    moderation_status = 'A',
                    user=instance,
                    autor='s',
                    valor='0',
                    saldo='0',
                    timestamp_comprovante=timezone.now(),
                    approved_timestamp=timezone.now(),
                    credito_debito='c',
                    descricao='Abertura da Conta')

post_save.connect(create_user_associado, sender=User)


class ModeratedModel(models.Model):
    """
        DOCS: TODO
    """
    APPROVED = 'A'
    REJECTED = 'R'
    PENDING = 'P'

    MODERATION_CHOICES = (
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
        (PENDING, 'Pending'),
    )

    class Meta:
        abstract = True

    history = HistoricalRecords(inherit=True)

    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    approved_timestamp = models.DateTimeField(blank=True, null=True)
    moderation_comments = models.TextField(blank=True, null=True)

    moderation_status = models.CharField(
        verbose_name='Status de Moderação',
        help_text='O status "Rejected" não permite que o registro seja mostr    ado.',
        max_length=1,
        choices=MODERATION_CHOICES,
        default=PENDING)


class Plano(ModeratedModel):

    PLANO_CHOICES = (
        ('an', 'Anuidade'),
        ('ml', 'Mensalidades'),
        ('sh', 'Starving Hacker'),
    )

    # tipo plano (Anuidade, Starving)
    plano = models.CharField(
        max_length=2,
        choices=PLANO_CHOICES
    )

    # user
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    validade_data_inicio = models.DateField()
    data_validade_fim = models.DateField()
    descricao = models.TextField()


class Lancamento(ModeratedModel):

    AUTHOR_CHOICES = (
        ('s', 'System'),
        ('a', 'Admin'),
        ('u', 'User'),
    )

    CREDITO_DEBITO_CHOICES = (
        ('d', 'Débito'),
        ('c', 'Crédito'),
        #('n', 'Doação'),
    )

    # user
    user = models.ForeignKey(
        User,
        models.SET_NULL,
        null=True,
    )

    # autor (sistema usuário)
    autor = models.CharField(
        max_length=1,
        choices=AUTHOR_CHOICES
    )
    # Credito ou debito
    credito_debito = models.CharField(
        max_length=1,
        choices=CREDITO_DEBITO_CHOICES
    )
    # data
    timestamp_comprovante = models.DateTimeField('Data do Comprovante')
    # valor
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    # saldo
    saldo = models.DecimalField(
            max_digits=15, decimal_places=2,
            blank=True, null=True)
    # comprovante
    comprovante = models.FileField(
            upload_to='comprovantes/',
            blank=True, null=True)
    # descricao
    descricao = models.TextField()

    def __str__(self):
        valor = self.valor
        saldo = self.saldo if not self.saldo is None else 0.0
        id = self.id if not self.id is None else 0
        return "%d - %s: R$%.2f %s (R$%.2f)" % (id, self.user, valor, self.descricao, saldo)

    def save(self, *args, **kwargs):
        if self.moderation_status == 'A' and self.saldo is None:
            self.approved_timestamp = timezone.now()
            qs = Lancamento.objects.exclude(approved_timestamp__isnull=True)
            len(qs) # eval
            lancamento_obj = qs.filter(
                    user=self.user,
                    approved_timestamp__lt=self.approved_timestamp,
                    moderation_status='A').latest('approved_timestamp')

            valor = self.valor if self.credito_debito == 'c' else -self.valor
            novo_saldo = lancamento_obj.saldo + valor
            self.saldo = novo_saldo

        super(Lancamento, self).save(*args, **kwargs)

def alert_lancamento(sender, instance, created, **kwargs):
    if instance.user.is_active:
        sendgrid_lancamento(instance)
        print("Email Lançamento Enviado.")

post_save.connect(alert_lancamento, sender=Lancamento)


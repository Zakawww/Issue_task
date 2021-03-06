from django.db import models

from webapp.validate import validate_title, MinLengthValidator


class BaseModel(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        abstract = True


class Issue(BaseModel):
    summary = models.CharField(max_length=60, verbose_name='Краткое описание', validators=[validate_title])
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Полное описание',
                                   validators=(MinLengthValidator(10),))
    status = models.ForeignKey('webapp.Status', on_delete=models.PROTECT, related_name='issues',
                               verbose_name='Статус')
    type = models.ManyToManyField('webapp.Type', related_name='issues', verbose_name='Тип')

    def __str__(self):
        return f"{self.id}.{self.summary}"

    class Meta:
        db_table = 'issue_tracker'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Status(models.Model):
    name = models.CharField(max_length=20, verbose_name='Статус')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус задачи'
        verbose_name_plural = 'Статусы задач'


class Type(models.Model):
    name = models.CharField(max_length=20, verbose_name='Тип')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип задачи'
        verbose_name_plural = 'Типы задач'

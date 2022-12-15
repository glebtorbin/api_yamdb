from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from api.validator import validate
from users.models import User

TEXT_LIMIT: int = 15


class Category(models.Model):
    name = models.CharField(
        verbose_name='Наименование категории',
        max_length=50
    )
    slug = models.SlugField(
        verbose_name='slug_Категория',
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Наименование жанра',
        max_length=50
    )
    slug = models.SlugField(
        verbose_name='slug_Жанр',
        unique=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр',
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(verbose_name='Название произведения',
                            max_length=150, blank=False)
    year = models.IntegerField(
        verbose_name='Год произведения',
        blank=True,
        db_index=True,
        validators=[validate]
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
        blank=True
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение',
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name} {self.year}'


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews',
        db_index=True
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    title = models.ForeignKey(
        Title,
        verbose_name='Название произведения',
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique review'
            )]

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(verbose_name='Комментарий')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments',
        db_index=True
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:TEXT_LIMIT]

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .constants import (
    MAX_LOCATION_NAME_LENGTH,
    MAX_TITLE_LENGTH,
    STR_SLICE_LENGTH,
)

User = get_user_model()


class PublishedCreatedModel(models.Model):
    is_published = models.BooleanField(
        "Опубликовано",
        default=True,
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class Category(PublishedCreatedModel):
    title = models.CharField("Заголовок", max_length=MAX_TITLE_LENGTH)
    description = models.TextField("Описание")
    slug = models.SlugField(
        "Идентификатор",
        unique=True,
        help_text=(
            "Идентификатор страницы для URL; разрешены символы латиницы, "
            "цифры, дефис и подчёркивание."
        ),
    )

    class Meta(PublishedCreatedModel.Meta):
        verbose_name = "категория"
        verbose_name_plural = "Категории"
        default_related_name = "posts"

    def __str__(self):
        return self.title[:STR_SLICE_LENGTH]


class Location(PublishedCreatedModel):
    name = models.CharField("Название места", max_length=MAX_LOCATION_NAME_LENGTH)

    class Meta(PublishedCreatedModel.Meta):
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"
        default_related_name = "posts"

    def __str__(self):
        return self.name[:STR_SLICE_LENGTH]


class PostQuerySet(models.QuerySet):
    def published(self):
        return (
            self.filter(
                is_published=True,
                pub_date__lte=timezone.now(),
                category__is_published=True,
            )
            .select_related("author", "category", "location")
        )


class Post(PublishedCreatedModel):
    title = models.CharField("Заголовок", max_length=MAX_TITLE_LENGTH)
    text = models.TextField("Текст")
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
    )

    objects = PostQuerySet.as_manager()

    class Meta(PublishedCreatedModel.Meta):
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ("-pub_date",)
        default_related_name = "posts"

    def __str__(self):
        return self.title[:STR_SLICE_LENGTH]

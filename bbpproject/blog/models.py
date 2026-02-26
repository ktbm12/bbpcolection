from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import CFPBaseModel
from bbpproject.users.models import User

class Post(CFPBaseModel):
    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), unique=True, max_length=255)
    excerpt = models.TextField(_("excerpt"), blank=True, help_text=_("Short summary for the homepage"))
    content = models.TextField(_("content"))
    image = models.ImageField(_("image"), upload_to="blog/%Y/%m/%d/", blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    is_published = models.BooleanField(_("is published"), default=False)
    
    class Meta(CFPBaseModel.Meta):
        verbose_name = _("blog post")
        verbose_name_plural = _("blog posts")

    def __str__(self):
        return self.title

from django.db import models
from django.utils.text import slugify


def project_file_upload(instance, filename):
    name = instance.slug
    slug = slugify(name)
    return f"user_files/{slug}/{filename}"


class Project(models.Model):
    projectName = models.CharField(max_length=100)
    file = models.FileField(upload_to=project_file_upload)
    slug = models.SlugField(null=True, unique=True)
    fileExt = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.projectName

    def _get_unique_slug(self):
        unique_slug = self.projectName
        num = 1
        while Project.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}{}'.format(unique_slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()

        super().save()

from django.db import models
from django.urls import reverse


class Course(models.Model):
    title = models.CharField(max_length=150, help_text="The title of the curriculum course")
    instructor = models.CharField(max_length=100, help_text="Lead instructor full name")
    price = models.DecimalField(max_digits=7, decimal_places=2, help_text="Tuition in USD")
    category = models.CharField(max_length=50, default="Software Engineering")
    is_published = models.BooleanField(default=True, help_text="Check to make visible in the public catalog")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self) -> str:
        return f"{self.title} by {self.instructor}"

    def get_absolute_url(self) -> str:
        return reverse("courses:course-edit", kwargs={"pk": self.pk})

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "instructor": self.instructor,
            "price": float(self.price),
            "category": self.category,
            "is_published": self.is_published,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else None,
        }

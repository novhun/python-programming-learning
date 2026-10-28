from django.contrib import messages
from django.db.models import Avg, Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CourseForm
from .models import Course


def course_list_view(request: HttpRequest) -> HttpResponse:
    """UI: Lists all courses with search, category filtering, and metrics."""
    search_query = request.GET.get("search", "").strip()
    selected_category = request.GET.get("category", "").strip()

    queryset = Course.objects.all()

    if search_query:
        queryset = queryset.filter(
            Q(title__icontains=search_query) | Q(instructor__icontains=search_query)
        )

    if selected_category:
        queryset = queryset.filter(category__iexact=selected_category)

    # Statistics
    total_count = Course.objects.count()
    avg_price = Course.objects.aggregate(avg=Avg("price"))["avg"] or 0.0
    all_categories = sorted(list(Course.objects.values_list("category", flat=True).distinct()))

    context = {
        "courses": queryset,
        "total_count": total_count,
        "avg_price": avg_price,
        "category_count": len(all_categories),
        "all_categories": all_categories,
        "search_query": search_query,
        "selected_category": selected_category,
    }
    return render(request, "courses/course_list.html", context)


def course_create_view(request: HttpRequest) -> HttpResponse:
    """UI: Creates a new course using Django ModelForm."""
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, f"Course '{course.title}' created successfully!")
            return redirect("courses:course-list")
        else:
            messages.error(request, "Please correct the errors in the form below.")
    else:
        form = CourseForm()

    return render(request, "courses/course_form.html", {"form": form, "is_edit": False})


def course_edit_view(request: HttpRequest, pk: int) -> HttpResponse:
    """UI: Updates an existing course using Django ModelForm."""
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            course = form.save()
            messages.success(request, f"Course '{course.title}' updated successfully!")
            return redirect("courses:course-list")
        else:
            messages.error(request, "Please correct the errors in the form below.")
    else:
        form = CourseForm(instance=course)

    return render(request, "courses/course_form.html", {"form": form, "course": course, "is_edit": True})


def course_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    """UI: Confirms and executes course deletion."""
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        title = course.title
        course.delete()
        messages.success(request, f"Course '{title}' was permanently deleted.")
        return redirect("courses:course-list")

    return render(request, "courses/course_confirm_delete.html", {"course": course})

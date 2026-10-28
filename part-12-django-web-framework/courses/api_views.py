import json
from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Course


@csrf_exempt
def api_course_list(request: HttpRequest) -> JsonResponse:
    """REST API: GET (list all with filters) & POST (create via JSON)."""
    if request.method == "GET":
        category = request.GET.get("category")
        search = request.GET.get("search")
        queryset = Course.objects.all()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(instructor__icontains=search)
            )
        if category:
            queryset = queryset.filter(category__iexact=category)

        return JsonResponse({
            "count": queryset.count(),
            "results": [c.to_dict() for c in queryset],
        })

    elif request.method == "POST":
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Malformed JSON payload."}, status=400)

        title = payload.get("title")
        instructor = payload.get("instructor")
        price = payload.get("price")

        if not title or not instructor or price is None:
            return JsonResponse(
                {"error": "Fields 'title', 'instructor', and 'price' are required."},
                status=400,
            )

        try:
            price_val = float(price)
            if price_val < 0:
                return JsonResponse({"error": "Price cannot be negative."}, status=400)
        except ValueError:
            return JsonResponse({"error": "Price must be a valid number."}, status=400)

        course = Course.objects.create(
            title=title,
            instructor=instructor,
            price=price_val,
            category=payload.get("category", "General"),
            is_published=payload.get("is_published", True),
        )
        return JsonResponse(course.to_dict(), status=201)

    return JsonResponse({"error": f"Method {request.method} not allowed."}, status=405)


@csrf_exempt
def api_course_detail(request: HttpRequest, pk: int) -> JsonResponse:
    """REST API: GET, PUT/PATCH, and DELETE for a single course."""
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return JsonResponse({"error": f"Course #{pk} not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(course.to_dict())

    elif request.method in ("PUT", "PATCH"):
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Malformed JSON payload."}, status=400)

        if "title" in payload:
            course.title = str(payload["title"]).strip()
        if "instructor" in payload:
            course.instructor = str(payload["instructor"]).strip()
        if "price" in payload:
            try:
                p = float(payload["price"])
                if p < 0:
                    return JsonResponse({"error": "Price cannot be negative."}, status=400)
                course.price = p
            except ValueError:
                return JsonResponse({"error": "Price must be numeric."}, status=400)
        if "category" in payload:
            course.category = str(payload["category"]).strip()
        if "is_published" in payload:
            course.is_published = bool(payload["is_published"])

        course.save()
        return JsonResponse(course.to_dict())

    elif request.method == "DELETE":
        course_id = course.id
        course.delete()
        return JsonResponse({"message": f"Course #{course_id} deleted successfully."})

    return JsonResponse({"error": f"Method {request.method} not allowed."}, status=405)


# communications/search.py
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.http import JsonResponse
from .models import Message

def search_messages(request):
    q = request.GET.get("q", "")
    convo_id = request.GET.get("conversation")
    if not q:
        return JsonResponse({"results": []})
    vector = SearchVector("content", weight="A")
    query = SearchQuery(q)
    qs = Message.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.01)
    if convo_id:
        qs = qs.filter(conversation_id=convo_id)
    qs = qs.order_by("-rank", "-created_at")[:50]
    data = [{"id": m.id, "content": m.content, "created_at": m.created_at.isoformat()} for m in qs]
    return JsonResponse({"results": data})
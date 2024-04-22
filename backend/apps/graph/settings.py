from django.conf import settings

GRAPH_ACCESS_KEY = getattr(settings, "GRAPH_ACCESS_KEY", None)
ALLOWED_HOST     = getattr(settings, 'ALLOWED_HOST', [])

GRAPH_WEBHOOK_DOMAIN = getattr(settings, 'GRAPH_WEBHOOK_DOMAIN', None)

if GRAPH_WEBHOOK_DOMAIN:
    ALLOWED_HOST.append(GRAPH_WEBHOOK_DOMAIN)

GRAPH_API_URL    = settings.GRAPH_API_URL
GRAPH_LIB_MODULE = getattr(settings, 'GRAPH_LIB_MODULE', 'apps.graph.utils')
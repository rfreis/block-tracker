from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("dashboard/", include("dashboard.urls")),
    path("wallet/", include("wallet.urls")),
    path("transaction/", include("transaction.urls")),
]

if settings.DEBUG:  # pragma: no cover
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

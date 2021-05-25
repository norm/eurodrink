"""eurodrink URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView

from controlpanel.views import (
    ControlPanel,
    FreeTweet,
    SetScoringContext,
    ScoringComplete,
)
from contests.views import PerformanceUpdate

from incidents.views import (
    PerformanceIncidentCreate,
    PerformanceIncidentUpdate,
    ScoreIncidentCreate,
    ShowIncidentCreate,
)


urlpatterns = [
    path('', RedirectView.as_view(url='/panel/')),
    path('admin/', admin.site.urls),
    path('panel/', ControlPanel.as_view()),

    path(
        'panel/performance/<int:pk>',
        PerformanceUpdate.as_view()
    ),

    path(
        'panel/reporting/',
        SetScoringContext.as_view()
    ),
    path(
        'panel/scored/<slug:pk>',
        ScoringComplete.as_view()
    ),

    path(
        'panel/performanceincident/<int:pk>',
        PerformanceIncidentUpdate.as_view()
    ),
    path(
        'panel/performanceincident/create',
        PerformanceIncidentCreate.as_view()
    ),
    path(
        'panel/scoreincident/create',
        ScoreIncidentCreate.as_view()
    ),
    path(
        'panel/showincident/create',
        ShowIncidentCreate.as_view()
    ),
    path(
        'panel/tweet/',
        FreeTweet.as_view(),
    )
]

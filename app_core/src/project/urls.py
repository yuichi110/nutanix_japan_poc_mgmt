"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from cluster.apis import ClusterApi
from task.apis import TaskApi
from ops.apis import OpsApi

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/clusters/', ClusterApi.clusters),
    path('api/v1/clusters/<str:uuid>', ClusterApi.cluster),

    #path('api/fvms/', FvmApi.clusters),
    #path('api/fvms/<str:uuid>', FvmApi.cluster),

    path('api/v1/tasks/', TaskApi.tasks),
    path('api/v1/tasks/<str:uuid>', TaskApi.task),
    #path('api/v1/tests/', TaskApi.tests),
    #path('api/v1/tests/<str:uuid>', TaskApi.test),

    path('api/v1/ops/foundation/<str:uuid>', OpsApi.foundation),
    path('api/v1/ops/power/up/<str:uuid>', OpsApi.power_up),
    path('api/v1/ops/power/down/<str:uuid>', OpsApi.power_down),
]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import time

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from .loan_application import create_loan_application
from .loan_application import get_user_loan_applications
from .loan_application import get_loan_application_status
from .loan_application import add_vouchers_to_application
from .loan_application import submit_loan_application
from .loan_application import get_vouch_requests
from .loan_application import finish_vouching_process
from .loan_application import get_loan_application_for_review
from .loan_application import change_loan_application_status
from django.shortcuts import render


# Create your views here.
@csrf_exempt
def create_loan_application_view(request):
    request_data = request.data
    create_loan_application(request_data)


@csrf_exempt
def get_user_loan_applications_view(request):
    user_id = request.data['user_id']
    la = get_user_loan_applications(user_id)
    return HttpResponse(la)


@csrf_exempt
def get_loan_application_status_view(request):
    la_id = request.data['loan_application_id']
    la_status = get_loan_application_status(la_id)
    return HttpResponse(la_status)


@csrf_exempt
def add_vouchers_to_application_view(request):
    la_id = request.data['loan_application_id']
    user_names = request.data['usernames']
    add_vouchers_to_application(la_id, user_names)
    return HttpResponse("Done!")


@csrf_exempt
def submit_loan_application_view(request):
    la_id = request.data['loan_application_id']
    submit_loan_application(la_id)


@csrf_exempt
def get_vouch_requests_view(request):
    user_id = request.data['user_id']
    vouch_requests = get_vouch_requests(user_id)
    return HttpResponse(vouch_requests)


@csrf_exempt
def finish_vouching_process_view(request):
    la_id = request.data['loan_application_id']
    finish_vouching_process(la_id)


@csrf_exempt
def get_loan_application_for_review_view(request):
    las = get_loan_application_for_review()
    return HttpResponse(las)


@csrf_exempt
def change_loan_application_status_view(request):
    la_id = request.data['loan_application_id']
    new_status = request.data['new_status']
    change_loan_application_status(la_id, new_status)
    return HttpResponse("done")

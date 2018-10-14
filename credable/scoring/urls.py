from django.urls import path

from .views import (
    create_loan_application_view,
    get_user_loan_applications_view,
    get_loan_application_status_view,
    add_vouchers_to_application_view,
    submit_loan_application_view,
    get_vouch_requests_view,
    finish_vouching_process_view,
    get_loan_application_for_review_view,
    vouch_list_view,
)

app_name = "scoring"

urlpatterns = [
    path("create_loan_application/", view=create_loan_application_view, name="create_la"),
    path("get_user_loan_applications/", view=get_user_loan_applications_view, name="get_la"),
    path("add_vouchers_to_application/", view=add_vouchers_to_application_view, name="add_vouchers"),
    path("submit_loan_application/", view=submit_loan_application_view, name="submit"),
    path("get_vouch_requests/", view=get_vouch_requests_view, name="get_vouch"),
    path("finish_vouching_process/", view=finish_vouching_process_view, name="finish_vouching"),
    path("get_loan_application_for_review/", view=get_loan_application_for_review_view, name="get_loan"),
    path("get_loan_application_status/", view=get_loan_application_status_view, name="get_loan_status"),

    path("", view=vouch_list_view, name="vouch_list"),
]

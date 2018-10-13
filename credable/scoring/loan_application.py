import datetime
import random
from datetime import timedelta

from .models import LoanApplication
from .models import User
from .models import Vouching


def calculate_down_payment_and_interest(loan_application: LoanApplication) -> object:
    down_payment = loan_application.total_loan_amount * 0.10
    credit_score = loan_application.user.credit_score
    interest_rate = 12.5 - int(credit_score / 100)
    remaining_amount = loan_application.total_loan_amount * (
        1 + (interest_rate * loan_application.months / 12.0)) - down_payment
    loan_application.emi = remaining_amount / loan_application.months
    loan_application.down_payment = down_payment
    return loan_application


def get_credit_score(pan_number):
    return random.randint(560, 820)


def create_loan_application(loan_details):
    loan_application = LoanApplication()
    loan_application.user_id = loan_details['user_id']
    loan_application.total_loan_amount = float(loan_details['amount'])
    loan_application.months = int(loan_details['months'])
    loan_application.save()
    return


def get_user_loan_applications(user_id):
    user = User.objects.get(id=user_id)
    loan_applications = user.loan_applications.all()
    loan_applications = [item.__dict__ for item in loan_applications]
    return loan_applications


def get_loan_application_status(loan_application_id):
    loan_application = LoanApplication.objects.get(id=loan_application_id)
    vouches = loan_application.vouches.all()
    total_count = loan_application.vouches.all().count()
    count_response = 0
    for vouch in vouches:
        if vouch.status == 'ACC' or vouch.status == 'REJ':
            count_response += 1
    loan_application_dict = loan_application.__dict__
    loan_application_dict['total_requests'] = total_count
    loan_application_dict['responded'] = count_response
    return loan_application_dict


def add_vouchers_to_application(loan_id, user_names):
    loan_application = LoanApplication.objects.get(id=loan_id)
    for user_name in user_names:
        voucher = User.objects.get(username=user_name)
        voucher.vouched_loan_applications.add(loan_application)
        vouch = Vouching()
        vouch.user = voucher
        vouch.loan_application = loan_application
        vouch.save()
        voucher.save()
    return


def get_vouch_requests(user_id):
    user = User.objects.get(id=user_id)
    vouches = Vouching.objects.filter(user=user).all()
    vouch_dicts = list()
    for item in vouches:
        vouch_dict = item.__dict__
        amount = item.loan_application.total_loan_amount
        months = item.loan_application.months
        vouch_dict['request_user'] = item.loan_application.user.username
        vouch_dict['amount'] = amount
        vouch_dict['months'] = months
        vouch_dicts.append(vouch_dict)
    return vouch_dicts


def submit_loan_application(loan_application_id):
    loan_application = LoanApplication.objects.get(id=loan_application_id)
    loan_application.loan_status = 'SUB'
    vouchings = Vouching.objects.filter(status='ACC').all()
    total_value = 0
    for vouching in vouchings:
        total_value += vouching.vouch_value

    for vouching in vouchings:
        vouching.vouch_value = vouching.vouch_value / float(total_value)
        vouching.save(update_fields=['vouch_value'])
    loan_application.save()


def get_loan_application_for_review():
    loan_applications = LoanApplication.objects.filter(loan_status='SUB')
    return loan_applications


def change_loan_application_status(loan_application_id, new_status):
    loan_application = LoanApplication.objects.get(id=loan_application_id)
    loan_application.loan_status = new_status
    loan_application.save(update_fields=['loan_status'])


def create_account(account_details):
    user = User()
    pan_url = account_details['pan_url']
    name = account_details['name']
    pan_number = get_pan_number(pan_url)
    credit_score = get_credit_score(pan_number)


def update_credit_score(user_id):
    total_credit_delta = 0

    user = User.objects.get(id=user_id)

    loan_applications = user.loan_applications.filter(loan_status='ACT').all()
    for loan_application in loan_applications:

        unique_loan_id = loan_application.unique_loan_id
        loan_status = get_loan_status(unique_loan_id)
        payment_sequence = get_loan_repayment_tuple(unique_loan_id)
        expected_payment = get_expected_repayment_tuple(loan_application)
        credit_delta = calculate_score_delta(payment_sequence, expected_payment, loan_application.loan_start_date)

        if loan_status == 'DEL':
            user.credit_score += credit_delta
            user.credit_score -= 10
            change_loan_application_status(loan_application.id, 'DEL')
        if loan_status == 'FIN':
            user.credit_score += credit_delta
            change_loan_application_status(loan_application.id, 'FIN')
        if loan_status == 'ACT':
            total_credit_delta += credit_delta

    user_vouches = user.vouches.filter(status='ACC').all()
    for vouch in user_vouches:
        loan_application = vouch.loan_application
        vouch_value = vouch.vouch_value
        risk_factor = 1.7
        vouch_factor = 0.3
        factor = risk_factor * vouch_factor * vouch_value

        unique_loan_id = loan_application.unique_loan_id
        loan_status = get_loan_status(unique_loan_id)
        payment_sequence = get_loan_repayment_tuple(unique_loan_id)
        expected_payment = get_expected_repayment_tuple(loan_application)
        credit_delta = calculate_score_delta(payment_sequence, expected_payment, loan_application.loan_start_date)

        if loan_status == 'DEL':
            user.credit_score += factor * credit_delta
            user.credit_score -= 10
            change_loan_application_status(loan_application.id, 'DEL')
        if loan_status == 'FIN':
            user.credit_score += factor * credit_delta
            change_loan_application_status(loan_application.id, 'FIN')
        if loan_status == 'ACT':
            total_credit_delta += factor * credit_delta

    user.apparent_credit_score = user.credit_score + total_credit_delta


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def calculate_score_delta(payment_sequence, expected_payment, start_date):
    current_date = datetime.datetime.today()
    expected_payment_sequence = [(220, datetime.datetime(year=2018, month=5, day=2)),
                                 (220, datetime.datetime(year=2018, month=6, day=5))]
    payment_sequence = [(220, datetime.datetime(year=2018, month=5, day=2)),
                        (220, datetime.datetime(year=2018, month=6, day=1))]
    diff_array = list()
    for date in date_range(start_date, current_date):
        expected_payment_by_date = sum([float(item[0]) for item in expected_payment_sequence if item[1] < date])
        payment_by_date = sum([float(item[0]) for item in payment_sequence if item[1] < date])
        diff_array.append(payment_by_date - expected_payment_by_date)
    return sum(diff_array) / (30.0 * len(diff_array))


def get_loan_repayment_tuple(loan_id):
    sequence = dict()
    sequence['12345678'] = [(220, datetime.datetime(year=2018, month=5, day=2)),
                            (220, datetime.datetime(year=2018, month=6, day=1))]
    return sequence[loan_id]


def get_expected_repayment_tuple(loan_application: LoanApplication) -> list():
    start_date = loan_application.loan_start_date
    delta = timedelta(days=30)
    months = loan_application.months
    emi = loan_application.emi
    repayment_list = list()
    for month_index in range(1, months + 1):
        repayment_list.append((emi, start_date + delta * month_index))
    return repayment_list

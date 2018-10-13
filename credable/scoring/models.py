from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class LoanApplication(models.Model):
    LOAN_STATUS = (
        ('APP', 'Application'), ('SUB', 'Submitted'), ('REJ', 'Rejected'), ('ACT', 'Active'), ('FIN', 'Finished'), ('DEL', 'Delinquent'))
    loan_start_date = models.DateField(null=True)
    unique_loan_id = models.CharField(max_length=256)
    user = models.ForeignKey(User, related_name='loan_applications', on_delete=models.CASCADE)
    loan_status = models.CharField(max_length=50, choices=LOAN_STATUS, default='APP')
    total_loan_amount = models.FloatField(null=True)
    down_payment = models.FloatField(null=True)
    months = models.IntegerField(null=True)
    emi = models.FloatField(null=True)
    vouchers = models.ManyToManyField(User, related_name='vouched_loan_applications')


class Vouching(models.Model):
    VOUCH_STATUS = (
        ('REQ', 'Requested'), ('REJ', 'Rejected'), ('ACC', 'Accepted'))
    user = models.ForeignKey(User, related_name='vouches', on_delete=models.CASCADE)
    loan_application = models.ForeignKey(LoanApplication, related_name='vouches', on_delete=models.CASCADE)
    vouch_value = models.FloatField(null=True)
    status = models.CharField(max_length=50, choices=VOUCH_STATUS)

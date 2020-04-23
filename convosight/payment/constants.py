from orm_choices import choices


@choices
class PaymentStatus:
    class Meta:
        PROCESS = [1, 'Process']
        SUCCESS = [2, 'Success']
        FAILED = [3, 'Fail']

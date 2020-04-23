from orm_choices import choices


@choices
class BookingStatus:
    class Meta:
        PROCESS = [1, 'Process']
        CONFIRM = [2, 'Confirm']
        FAILED = [3, 'Fail']

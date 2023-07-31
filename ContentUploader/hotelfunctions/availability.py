from ContentUploader.models import Booking

def check_availability(marriagehall,check_in,check_out):
    avail_lst=[]
    all_bookings=Booking.objects.filter(marriagehall=marriagehall)
    for book in all_bookings:
        if book.check_in > check_out or book.check_out < check_in:
            avail_lst.append(True)
        else:
            avail_lst.append(False)
    return all(avail_lst)
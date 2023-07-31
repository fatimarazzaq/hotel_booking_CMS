from bookings.models import Booking


def avail_func(marriagehall,check_in,check_out):
    avail_lst=[]
    print(marriagehall)
    
    all_bookings = Booking.objects.filter(marriagehall=marriagehall).all()
    for booking in all_bookings:
        if( booking.check_in > check_out or booking.check_out < check_in ):
            avail_lst.append(True)
        else:
            avail_lst.append(False)
        
    return all(avail_lst)
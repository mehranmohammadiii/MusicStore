# import sys
# sys.path.insert(0, 'C:/Users/digi kala/Desktop/app2')
from ..database.InvoiceLineDAL import InvoiceLineDAL

class InvoiceLineService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_Order_invoice_for_create(self,Artistcode,number,trackkode):

        is_valid, validation_message=self.check_values(Artistcode,number,trackkode)

        if not is_valid:
            return False, validation_message
        try:
            IN1 = InvoiceLineDAL(self.db_manager)
            success, message=IN1.create_invoiceLine(Artistcode,number,trackkode)
            return success, message
        except Exception as e:
            print(f"خطای داخلی: {e}")
            return False, "یک خطای پیش‌بینی نشده در سیستم رخ داد."

    def check_values(self,Artistcode,number,trackkode):
        if not bool(Artistcode) or not Artistcode.isdigit():
            return False,"کد هنرمند را درست وارد کنید"

        if not bool(number) or not Artistcode.isdigit():
            return False,"تعداد را درست وارد کنید"

        if not bool(trackkode) or not Artistcode.isdigit():
            return False,"کد ترک را درست وارد کنید"  
                        
        return True," اطلاعات با موفقیت ثبت شد"
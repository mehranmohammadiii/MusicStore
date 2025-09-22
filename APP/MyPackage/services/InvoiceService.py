# import sys
# sys.path.insert(0, 'C:/Users/digi kala/Desktop/app2')
from ..database.InvoiceDAL import InvoiceDAL

class InvoiceService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_Customer_invoice(self,Customercode):
        try:
            IN1 = InvoiceDAL(self.db_manager)
            Invoice_list = IN1.fetch_Customer_invoice(Customercode)
            return Invoice_list
        except Exception as e:
            print(f"خطا: {e}")
            return []

    def get_Customer_invoice_for_create(self,Customercode,BillingAddress,BillingCity,BillingCountry):

        is_valid, validation_message=self.check_values(Customercode,BillingAddress,BillingCity,BillingCountry)

        if not is_valid:
            return False, validation_message
        try:
            IN1 = InvoiceDAL(self.db_manager)
            success, message=IN1.create_invoice(Customercode,BillingAddress,BillingCity,BillingCountry)
            return success, message
        except Exception as e:
            print(f"خطای داخلی: {e}")
            return False, "یک خطای پیش‌بینی نشده در سیستم رخ داد."

    def check_values(self,Customercode,BillingAddress,BillingCity,BillingCountry):
        if not bool(Customercode) or not Customercode.isdigit():
            return False,"کد کاربری را درست وارد کنید"

        if not all(ch.isalpha() or ch.isspace() for ch in BillingAddress) or bool(BillingAddress)==False:
            return False,"آدرس  را درست وارد کنید"

        if not all(ch.isalpha() or ch.isspace() for ch in BillingCity) or bool(BillingCity)==False:
            return False,"نام شهر را درست وارد کنید"                  

        if not BillingCountry.isalpha():
            return False,"نام کشور را درست وارد کنید"
        return True," اطلاعات با موفقیت ثبت شد"
import sys
import os
from ..database.Db_Connection import DatabaseConnection
from ..services.InvoiceLineService import InvoiceLineService
from ..services.InvoiceService import InvoiceService
from ..services.GenreService import GenreSrvice
from ..services.AlbumService import AlbumService
from ..services.TrackService import TrackService
from khayyam import JalaliDatetime
from tkinter import messagebox
from tkinter import ttk
from PIL import Image,ImageTk
import tkinter

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller یک پوشه موقت می‌سازد و مسیر آن را در _MEIPASS ذخیره می‌کند
        base_path = sys._MEIPASS
    except Exception:
        # اگر در حالت توسعه باشیم (نه exe)، مسیر فایل فعلی را برمی‌گرداند
        base_path = os.path.abspath(".")

    # مسیر کامل و صحیح را برمی‌گرداند
    return os.path.join(base_path, relative_path)
# ----------------------------------------------------------------------------------------------------------------------------------------
class BaseWindow:
    def __init__(self, master, title="پنجره جدید", geometry="900x560", image_path=None):
        """
        این کلاس یک پنجره Toplevel استاندارد با قابلیت‌های اضافی می‌سازد.

        :param master: پنجره والد (معمولاً root اصلی برنامه)
        :param title: عنوان پنجره
        :param geometry: ابعاد و موقعیت اولیه پنجره
        :param image_path: مسیر فایل تصویر پس‌زمینه (اختیاری)
        """
        self.window = tkinter.Toplevel(master)
        self.window.title(title)
        
        # --- بخش وسط‌چین کردن پنجره ---
        # این منطق را در یک تابع جداگانه قرار می‌دهیم تا تمیزتر باشد
        self.center_window(geometry)
        self.window.minsize(700, 450)

        # --- بخش مدیریت پس‌زمینه ---
        self.original_image = None
        self.after_id = None

        # فقط در صورتی که مسیر تصویر داده شده باشد، منطق پس‌زمینه را فعال کن
        if image_path:
            try:
                self.original_image = Image.open(image_path)
                # Pillow به صورت خودکار فرمت‌های مختلف مثل JPG, PNG, WEBP را تشخیص می‌دهد
                
                self.bg_label = tkinter.Label(self.window)
                self.bg_label.place(relwidth=1, relheight=1)
                
                # برای اطمینان از اینکه پنجره ابعاد اولیه را گرفته، با کمی تاخیر پس‌زمینه را آپدیت می‌کنیم
                self.window.after(50, self.update_background) 
                
                self.window.bind("<Configure>", self.resize_image)
                
            except FileNotFoundError:
                print(f"خطا: فایل تصویر در مسیر '{image_path}' پیدا نشد.")
            except Exception as e:
                print(f"خطا در بارگذاری تصویر: {e}")

    def center_window(self, geometry):
        """پنجره را بر اساس ابعاد داده شده در مرکز صفحه نمایش می‌دهد."""
        w, h = map(int, geometry.split('x'))
        x_screen = self.window.winfo_screenwidth()
        y_screen = self.window.winfo_screenheight()
        x_coord = (x_screen / 2) - (w / 2)
        y_coord = (y_screen / 2) - (h / 2)
        self.window.geometry('%dx%d+%d+%d' % (w, h, x_coord, y_coord))
  
    def update_background(self, width=None, height=None):
        # اگر پنجره تصویر پس‌زمینه نداشته باشد، از تابع خارج شو
        if not self.original_image:
            return

        if width and height:
            resized = self.original_image.resize((width, height), Image.LANCZOS)
        else:
            resized = self.original_image.resize(
                (self.window.winfo_width(), self.window.winfo_height()),
                Image.LANCZOS
            )
        self.bg = ImageTk.PhotoImage(resized)
        self.bg_label.config(image=self.bg)

    def resize_image(self, event):
        # اگر پنجره تصویر پس‌زمینه نداشته باشد، از تابع خارج شو
        if not self.original_image:
            return
            
        if event.width > 1 and event.height > 1:
            if self.after_id:
                self.window.after_cancel(self.after_id)
            self.after_id = self.window.after(100, lambda: self.update_background(event.width, event.height))
# ----------------------------------------------------------------------------------------------------------------------------------------
class Music_application:

    def __init__(self):
        self.root = tkinter.Tk()
        self.db_manager = DatabaseConnection()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.title("فروشگاه موسیقی")
        x = self.root.winfo_screenwidth()
        y = self.root.winfo_screenheight()
        self.root.geometry('%dx%d+%d+%d' % (900, 560, (x/2)-(900/2), (y/2)-(560/2)))
        self.root.minsize(700, 450)

        try:
            image_path = resource_path("Images/abstract-background-border-black-smoke-texture-border-cinematic-design.jpg")
            self.original_image_root = Image.open(image_path)
            self.bg_label_root = tkinter.Label(self.root)
            self.bg_label_root.place(relwidth=1, relheight=1)
            self.after_id_root = None

            self.root.bind("<Configure>", self.resize_image_root)
            self.root.after(50, self.update_background_root)
        except FileNotFoundError:
            print("خطا: فایل تصویر پس‌زمینه اصلی پیدا نشد.")
            self.root.config(bg="grey")
        except Exception as e:
            print(f"خطا در بارگذاری تصویر اصلی: {e}")
            self.root.config(bg="grey")

        self.create_login_form()

    def on_closing(self):
        print("در حال بستن برنامه...")
        self.db_manager.disconnect()
        self.root.destroy()

    def create_login_form(self):

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        login_frame = tkinter.Frame(self.root, bg="#1c1c1c") 
        login_frame.grid(row=0, column=0) 

        login_frame.columnconfigure(0, weight=1)
        login_frame.columnconfigure(1, weight=0)

        font_style = ("Tahoma", 13)
        btn_bg = "#2a628f"
        btn_fg = "#ffffff"
        entry_bg = "#333333"
        entry_fg = "#ffffff"
        lbl_fg = "#dddddd"
        
        # --- User login section---
        user_button = tkinter.Button(login_frame, text="ورود به عنوان کاربر", font=font_style, 
                             bg=btn_bg, fg=btn_fg, command=self.show_user_panel, relief="flat", bd=5)
        user_button.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="ew")
        user_entry = tkinter.Entry(login_frame, font=font_style, justify='right',
                           bg=entry_bg, fg=entry_fg, insertbackground='white', relief="flat")
        user_entry.grid(row=1, column=0, padx=(10, 5), pady=5, sticky="ew", ipady=4)
        user_label = tkinter.Label(login_frame, text="کد کاربری", font=font_style, 
                           bg=login_frame['bg'], fg=lbl_fg)
        user_label.grid(row=1, column=1, padx=(5, 10), pady=5, sticky="w")
        
        separator = ttk.Separator(login_frame, orient='horizontal')
        separator.grid(row=2, column=0, columnspan=2, pady=20, sticky='ew')

        # --- Admin login section---
        admin_button = tkinter.Button(login_frame, text="ورود به عنوان ادمین", font=font_style,
                              bg=btn_bg, fg=btn_fg, command=self.show_settings_panel, relief="flat", bd=5)
        admin_button.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 5), sticky="ew")
        admin_entry = tkinter.Entry(login_frame, font=font_style, justify='right',
                            bg=entry_bg, fg=entry_fg, insertbackground='white', relief="flat")
        admin_entry.grid(row=4, column=0, padx=(10, 5), pady=5, sticky="ew", ipady=4)
        admin_label = tkinter.Label(login_frame, text="کد ادمین", font=font_style, 
                            bg=login_frame['bg'], fg=lbl_fg)
        admin_label.grid(row=4, column=1, padx=(5, 10), pady=5, sticky="w")

    def update_background_root(self, width=None, height=None):
        if width and height:
            resized = self.original_image_root.resize((width, height), Image.LANCZOS)
        else:
            resized = self.original_image_root.resize(
                (self.root.winfo_width(), self.root.winfo_height()),
                Image.LANCZOS
            )
        self.bg_root = ImageTk.PhotoImage(resized)
        self.bg_label_root.config(image=self.bg_root)

    def resize_image_root(self, event):
        if event.width > 1 and event.height > 1:
            if self.after_id_root:
                self.root.after_cancel(self.after_id_root)
            self.after_id_root = self.root.after(100, lambda: self.update_background_root(event.width, event.height))
# -----------------------------------------------------------------------------------------------------------------------------------------
    def show_user_panel(self):

        image_path = resource_path("Images/original-67815a27de92092856f9b143e387e6d4.webp")
        image_file = image_path
        self.user_panel_window = BaseWindow(self.root, title="پنل کاربری", image_path=image_file)

        labels = [
            "پرفروش‌ترین ترک‌ها",
            "آلبوم‌های هنرمندان",
            "ترک‌های آلبوم‌ها",
            "ژانر ترک‌ها",
            "ثبت سفارش جدید",
            "فاکتورهای من",
        ]

        self.right_buttons = []
        start_y = 0.22   # نقطه شروع عمودی (نسبی)
        step    = 0.10   # فاصله عمودی بین دکمه‌ها (نسبی)

        for i, txt in enumerate(labels):
            btn = tkinter.Button(
                self.user_panel_window.window, text=txt,
                font=("Tahoma", 11),
                bg="#171515", fg="#ddc6ff",
                cursor="hand2",
                relief="raised", bd=7,
                highlightthickness=3,          # کادر مشکی ضخیم
                highlightbackground="#000000", # رنگ کادر وقتی فوکوس نیست
                highlightcolor="#000000",      # رنگ کادر وقتی فوکوس دارد
                activebackground="#cb2c2c", activeforeground="#000000",
            )
            # سمت راست صفحه، عرض نسبی ثابت و ارتفاع پیکسلی
            btn.place(relx=0.85, rely=start_y + i*step, anchor="center",
                      relwidth=0.28, height=38)
            self.right_buttons.append(btn)
        
        Label1= tkinter.Label(self.user_panel_window.window,text="به فروشگاه ما خوش آمدید",bg="#171515", fg="#ddc6ff",font=("tahoma",15),relief="flat", bd=7)
        Label1.place(relx=0.50,rely=0.08,anchor="center",relwidth=0.38,height=38)

        self.clock_label = tkinter.Label(self.user_panel_window.window, font=("Tahoma", 14),bg="#000000",fg="#ddc6ff")
        self.clock_label.place(x=10, y=30)
        self.update_clock()

        btnexit= tkinter.Button(self.user_panel_window.window, text="خروج",font=("Tahoma", 11),bg="#171515",
                        fg="#ddc6ff",cursor="hand2",relief="raised", bd=7,
                        command=self.on_closing)
        btnexit.place(relx=0.10,rely=0.9,anchor="center",relwidth=0.15,)        

        self.right_buttons[0].bind("<Button>",lambda e :self.Show_top_tracks_window(e))
        self.right_buttons[1].bind("<Button>",lambda e :self.Show_album_window(e))
        self.right_buttons[2].bind("<Button>",lambda e :self.Show_tracks_window(e))
        self.right_buttons[3].bind("<Button>",lambda e :self.Show_Genre_window(e))
        self.right_buttons[4].bind("<Button>",lambda e :self.Show_NewOrder_window(e))
        self.right_buttons[5].bind("<Button>",lambda e :self.Show_Invoice_window(e))
        
    def Show_top_tracks_window(self,e):
        self.top_tracks_window=BaseWindow(self.root, title="نمایش ترک ها")
        self.create_scrollable_table_top_tracks(self.top_tracks_window.window)

    def Show_album_window(self,e):
        self.album_window=BaseWindow(self.root, title="نمایش آلبوم ها")
        self.create_scrollable_table_album(self.album_window.window)

    def Show_tracks_window(self,e):
        self.tracks_window=BaseWindow(self.root, title="نمایش آلبوم ها")
        self.create_scrollable_table_tracks(self.tracks_window.window)

    def Show_Genre_window(self,e):
        self.Genre_window=BaseWindow(self.root, title="نمایش آلبوم ها")
        self.create_scrollable_table_Genre(self.Genre_window.window)

    def Show_Invoice_window(self,e):
        self.Invoice_window=BaseWindow(self.root, title="نمایش فاکتور ها")
        self.Invoice_window.window.config(bg="#2b2b2b")
        self.create_invoice_lookup_form(self.Invoice_window.window)
    
    def Show_NewOrder_window(self, e):
        new_order_obj = BaseWindow(self.root, title="ثبت سفارش جدید")
        new_order_obj.window.config(bg="#2b2b2b")
        # 3. متد ساخت فرم را فراخوانی کرده و پنجره جدید را به آن پاس بده
        self.create_new_order_form(new_order_obj.window)
# -----------------------------------------------------------------------------------------------------------------------------------------
    def create_scrollable_table_top_tracks(self, parent_window):

        table_frame = tkinter.Frame(parent_window)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        columns = ('track_id', 'name', 'total_sold')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        tree.heading('track_id', text='شناسه ترک')
        tree.heading('name', text='نام ترک')
        tree.heading('total_sold', text='تعداد فروش')

        tree.column('track_id', width=80, anchor='center')
        tree.column('name', width=400) 
        tree.column('total_sold', width=100, anchor='center')

        TS1=TrackService(self.db_manager)
        for track_data in TS1.get_top_selling_tracks():
            tree.insert('', 'end', values=(track_data[0],track_data[1],track_data[2]))

        scrollbar = tkinter.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

    def create_scrollable_table_album(self, parent_window):

        table_frame = tkinter.Frame(parent_window)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        columns = ('album_id', 'title', 'artist_name')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        tree.heading('album_id', text='شناسه آلبوم')
        tree.heading('title', text='نام آلبوم')
        tree.heading('artist_name', text='نام هنرمند')

        tree.column('album_id', width=20, anchor='center')
        tree.column('title', width=300) 
        tree.column('artist_name', width=220, anchor='center')

        AS1=AlbumService(self.db_manager)
        for track_data in AS1.get_Albums_artists():
            tree.insert('', 'end', values=(track_data[0],track_data[1],track_data[2]))

        scrollbar = tkinter.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

    def create_scrollable_table_tracks(self, parent_window):

        table_frame = tkinter.Frame(parent_window)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        columns = ('album_id', 'track_id', 'track_name','track_Duration_Minutes')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        tree.heading('album_id', text='شناسه آلبوم')
        tree.heading('track_id', text='شناسه ترک')
        tree.heading('track_name', text='نام ترک')
        tree.heading('track_Duration_Minutes', text='مدت زمان ترک')

        tree.column('album_id', width=20, anchor='center')
        tree.column('track_id', width=20,anchor='center') 
        tree.column('track_name', width=400, anchor='center')
        tree.column('track_Duration_Minutes', width=50, anchor='center')

        TS1=TrackService(self.db_manager)
        for track_data in TS1.get_tracks():
            tree.insert('', 'end', values=(track_data[0],track_data[1],track_data[2],track_data[3]))

        scrollbar = tkinter.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

    def create_scrollable_table_Genre(self,parent_window):

        table_frame = tkinter.Frame(parent_window)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        columns = ('Genre_id', 'Genre_name', 'track_name')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        tree.heading('Genre_id', text='شناسه ژانر')
        tree.heading('Genre_name', text='نام ژانر')
        tree.heading('track_name', text='نام ترک')

        tree.column('Genre_id', width=20, anchor='center')
        tree.column('Genre_name', width=100, anchor='center') 
        tree.column('track_name', width=500, anchor='center')

        GE1=GenreSrvice(self.db_manager)
        for track_data in GE1.get_Genre():
            tree.insert('', 'end', values=(track_data[0],track_data[1],track_data[2]))

        scrollbar = tkinter.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

    def create_invoice_lookup_form(self, parent_window):
        """
        فرم جستجوی فاکتور بر اساس کد کاربری را در پنجره والد ایجاد می‌کند.
        """
        # 1. پنجره والد را برای وسط‌چین کردن محتوا پیکربندی می‌کنیم
        # یک شبکه 1x1 ایجاد می‌کنیم که تمام فضا را اشغال کند
        parent_window.rowconfigure(0, weight=1)
        parent_window.columnconfigure(0, weight=1)

        # 2. یک Frame برای نگهداری ویجت‌ها می‌سازیم
        # این Frame در مرکز شبکه 1x1 قرار می‌گیرد
        lookup_frame = tkinter.Frame(parent_window, bg="#333333") # یک پس‌زمینه تیره و مدرن
        lookup_frame.grid(row=0, column=0, padx=20, pady=20, ipadx=10, ipady=10)

        # 3. Grid داخلی Frame را پیکربندی می‌کنیم
        # ستون اول (برای Entry) باید قابلیت رشد داشته باشد
        lookup_frame.columnconfigure(0, weight=1)

        # --- تعریف استایل‌های ظاهری ---
        font_style = ("Tahoma", 13)
        btn_bg = "#4CAF50"  # سبز
        btn_fg = "white"
        entry_bg = "#555555"
        entry_fg = "white"
        label_fg = "#E0E0E0" # سفید مایل به خاکستری

        # 4. ویجت‌ها را ایجاد و در Frame قرار می‌دهیم

        # --- سطر اول: کادر ورود و لیبل ---
        
        # کادر ورود (Entry) برای دریافت کد کاربری
        customer_id_entry = tkinter.Entry(
            lookup_frame, 
            font=font_style, 
            justify='right',
            bg=entry_bg, 
            fg=entry_fg, 
            relief="flat",
            insertbackground='white' # رنگ نشانگر تایپ
        )
        # sticky="ew" باعث می‌شود در جهت افقی کش بیاید
        customer_id_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew", ipady=5)

        # لیبل "کد کاربری"
        customer_id_label = tkinter.Label(
            lookup_frame, 
            text=": کد کاربری", 
            font=font_style,
            bg=lookup_frame['bg'], 
            fg=label_fg
        )
        customer_id_label.grid(row=0, column=1, padx=(5, 10), pady=10)

        # --- سطر دوم: دکمه نمایش ---

        # دکمه "نمایش فاکتور ها"
        show_button = tkinter.Button(
            lookup_frame, 
            text="نمایش فاکتور ها", 
            font=font_style,
            bg=btn_bg, 
            fg=btn_fg,
            relief="flat",
            bd=0,
            activebackground="#45a049", # رنگ دکمه هنگام کلیک
            activeforeground="white",
            cursor="hand2",
            # command=self.create_scrollable_invoice_lookup_form()
        )
        
        show_button.bind("<Button>",lambda e :self.create_scrollable_invoice_lookup_form(e,customer_id_entry.get()))
        # columnspan=2 باعث می‌شود دکمه به اندازه عرض دو ستون باشد
        show_button.grid(row=1, column=0, columnspan=2, padx=10, pady=(20, 10), sticky="ew", ipady=5)
        
        # فوکوس را روی کادر ورود قرار می‌دهیم تا کاربر بلافاصله شروع به تایپ کند
        customer_id_entry.focus_set()
    
    def create_scrollable_invoice_lookup_form(self,e,Customercode):
    #     # self.create_scrollable_table_Genre(self.Genre_window.window)

        self.a1=BaseWindow(self.root, title="نمایش فاکتور ها")

        table_frame = tkinter.Frame(self.a1.window)
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        columns = ('InvoiceId', 'InvoiceDate', 'BillingCountry','Total')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        tree.heading('InvoiceId', text='شماره فاکتور')
        tree.heading('InvoiceDate', text='تاریخ فاکتور')
        tree.heading('BillingCountry', text='کشور')
        tree.heading('Total', text='مجموع قیمت فاکتور')

        tree.column('InvoiceId', width=20, anchor='center')
        tree.column('InvoiceDate', width=100,anchor='center') 
        tree.column('BillingCountry', width=100, anchor='center')
        tree.column('Total', width=50, anchor='center')

        IN1=InvoiceService(self.db_manager)
        for Invoice_data in IN1.get_Customer_invoice(Customercode):
            tree.insert('', 'end', values=(Invoice_data[0],Invoice_data[1],Invoice_data[2],Invoice_data[3]))

        scrollbar = tkinter.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
    
    def create_new_order_form(self, parent_window):
        """
        فرم ثبت سفارش جدید را با دو بخش مجزا در پنجره والد ایجاد می‌کند.
        """
        parent_window.rowconfigure(0, weight=1)
        parent_window.columnconfigure(0, weight=1)
        
        main_frame = tkinter.Frame(parent_window, bg="#2b2b2b")
        main_frame.grid(row=0, column=0)

        font_style = ("Tahoma", 12)
        style = ttk.Style()
        style.configure("TLabelFrame.Label", font=font_style, foreground="white")
        style.configure("TLabelFrame", background="#3c3f41", borderwidth=5)
        
        btn_bg = "#0078D7"
        btn_fg = "white"
        entry_bg = "#555555"
        entry_fg = "white"
        label_fg = "#E0E0E0"
        # --- بخش اول: اطلاعات مشتری و فاکتور ---
        customer_frame = tkinter.LabelFrame(main_frame)
        customer_frame.grid(row=0, column=0, padx=20, pady=15, ipady=10)
        customer_frame.columnconfigure(0, weight=1)

        customer_fields = [": کد کاربری" ,": آدرس",": نام شهر",": نام کشور" ]
        self.customer_entries = {}

        for i, field_text in enumerate(customer_fields):
            lbl = tkinter.Label(customer_frame, text=field_text, font=font_style, 
                        bg="#3c3f41", fg=label_fg)
            lbl.grid(row=i, column=1, padx=(5, 10), pady=6, sticky="w")
            
            entry = tkinter.Entry(customer_frame, font=font_style, justify='right', 
                        bg=entry_bg, fg=entry_fg, relief="flat", insertbackground='white')
            entry.grid(row=i, column=0, padx=(10, 5), pady=6, sticky="ew", ipady=4)
            self.customer_entries[field_text] = entry

        info_button = tkinter.Button(customer_frame, text="ثبت اطلاعات", font=font_style,
                            bg=btn_bg, fg=btn_fg, relief="flat", cursor="hand2",
                            command=self.on_submit_customer_info_click)
        
        info_button.grid(row=len(customer_fields), column=0, columnspan=2, 
                        padx=10, pady=(15, 5), sticky="ew", ipady=5)
        # --- بخش دوم: افزودن آیتم‌ها به سفارش (اصلاح شده) ---
        order_item_frame = tkinter.LabelFrame(main_frame)
        order_item_frame.grid(row=1, column=0, padx=20, pady=15, ipady=10)
        # --- تغییرات اصلی اینجا هستند ---
        # ستون‌های 1, 3, 5 (محل Entry ها) را واکنش‌گرا می‌کنیم
        order_item_frame.columnconfigure(1, weight=1)
        order_item_frame.columnconfigure(3, weight=1)
        order_item_frame.columnconfigure(5, weight=1)
        # لیست فیلدها و ستون شروع هر کدام
        order_fields_data = [
            ("کد هنرمند:", 4),
            ("تعداد:", 2),
            ("کد ترک:", 0)
        ]
        self.order_entries = {}
        for field_text, start_col in order_fields_data:
            # لیبل در ستون شروع قرار می‌گیرد
            lbl = tkinter.Label(order_item_frame, text=field_text, font=font_style,
                        bg="#3c3f41", fg=label_fg)
            lbl.grid(row=0, column=start_col, padx=(10, 5), pady=10)
            # کادر ورود در ستون بعدی (ستون شروع + 1) قرار می‌گیرد
            entry = tkinter.Entry(order_item_frame, font=font_style, justify='right',
                        bg=entry_bg, fg=entry_fg, relief="flat", insertbackground='white')
            entry.grid(row=0, column=start_col + 1, padx=(0, 10), pady=10, ipady=4, sticky="ew")
            self.order_entries[field_text] = entry
        order_button = tkinter.Button(order_item_frame, text="ثبت سفارش", font=font_style,
                            bg="#4CAF50", fg=btn_fg, relief="flat", cursor="hand2",
                            command=self.Click_on_order_registration)
        order_button.grid(row=1, column=0, columnspan=6, padx=10, pady=(15, 5), sticky="ew", ipady=5)
        self.customer_entries[": کد کاربری"].focus_set()

    def on_submit_customer_info_click(self):
        A1 = self.customer_entries[": کد کاربری"].get()
        A2 = self.customer_entries[": آدرس"].get()
        A3 = self.customer_entries[": نام شهر"].get()
        A4 = self.customer_entries[": نام کشور"].get()
        IN1=InvoiceService(self.db_manager)
        success, message =IN1.get_Customer_invoice_for_create(A1,A2,A3,A4)
        if success: 
            messagebox.showinfo("موفقیت", message)
        else: 
            messagebox.showerror("خطا", message)

    def Click_on_order_registration(self):
        A1=self.order_entries["کد هنرمند:"].get()   
        A2=self.order_entries["تعداد:"].get()
        A3=self.order_entries["کد ترک:"].get()  
        IN1=InvoiceLineService(self.db_manager)
        success, message =IN1.get_Order_invoice_for_create(A1,A2,A3)
        if success: 
            messagebox.showinfo("موفقیت", message)
        else: 
            messagebox.showerror("خطا", message)
# -----------------------------------------------------------------------------------------------------------------------------------------
    def update_clock(self):
        now = JalaliDatetime.now()    
        current_date=now.strftime("%Y/%m/%d")
        current_time=now.strftime("%H:%M:%S")
        self.clock_label.config(text=f"{current_date}  {current_time}")
        self.user_panel_window.window.after(1000, self.update_clock)

    def show_settings_panel(self):
        # ساخت یک پنجره جدید بدون پس‌زمینه
        # کافیست پارامتر image_path را ارسال نکنید
        settings_window = BaseWindow(self.root, title="تنظیمات", geometry="500x300")
        
        tkinter.Label(settings_window.window, text="اینجا تنظیمات قرار می‌گیرد.").pack(pady=20)

    def run(self):
        self.root.mainloop()

import sys
import sqlite3 as sql

if sys.version_info[0] < 3:
    import Tkinter as tk
    from Tkinter.scrolledtext import ScrolledText
    import tkMessageBox as messagebox
else:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter.scrolledtext import ScrolledText
    import tkinter.messagebox as messagebox



LARGE_FONT = ("Matura MT Script Capitals", 18, 'bold')
small_font = ("Lucida Calligraphy", 14)


def Quit():
    # print ('Hello, getting out of here')
    option = messagebox.askyesno('Quit', 'Are you sure you want to exit?')
    if option == True:
        import sys
        sys.exit()



class Database:

    def __init__(self):
        self.connection = sql.connect('database.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Records (firstName TEXT, lastName TEXT, age TEXT, gender TEXT, date TEXT, hospitalID TEXT, scanIDTEXT, scanType TEXT, indication TEXT, findings TEXT, conclusion TEXT, doctors TEXT)")


    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def insert(self, firstName, lastName, age, gender, date, hospitalID, scanID, scanType, indication, findings, conclusion, doctors):
        self.cursor.execute("INSERT INTO Records VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (firstName, lastName, age, gender, date, hospitalID, scanID, scanType, indication, findings, conclusion, doctors))
        self.connection.commit()
    def update(self, firstName, lastName, age, gender, date, hospitalID, scanID, scanType, indication, findings, conclusion, doctors):
        self.cursor.execute("UPDATE Records SET firstName = ?, lastName = ?, age = ?, gender = ?, date = ?, scanID = ?, scanType = ?, indication = ?, findings = ?, conclusion = ?, doctors = ? WHERE hospitalID = ?", (firstName, lastName, age, gender, date, scanID, scanType, indication, findings, conclusion, doctors, hospitalID))
        self.connection.commit()
    def search(self, filter):
        self.cursor.execute("SELECT * FROM Records WHERE firstName = ?", (filter, ))
        search_results = self.cursor.fetchall()
        return search_results
        # self.connection.commit()




    def delete(self, firstName):
        self.cursor.execute("DELETE FROM Records WHERE firstName = ?", (firstName, ))
        self.connection.commit()

    def display(self):
        self.cursor.execute("SELECT * FROM Records")
        records = self.cursor.fetchall()
        return records



class Values:
    def validate(self, first_name_entry, last_name_entry, age_entry, gender_entry, date_entry, hospital_id_entry, scan_id_entry, scan_type_entry, conclusion_entry, doctors_entry):

        if not (isinstance(first_name_entry, str) and first_name_entry!=''):
            return 'first name'
        elif not (isinstance(last_name_entry, str) and last_name_entry!=''):
            return 'last name'
        elif not (age_entry.isdigit() and age_entry!=''):
            return 'age'
        elif not (isinstance(gender_entry, str) and gender_entry!=''):
            return 'gender'
        elif not (isinstance(date_entry, str) and date_entry!=''):
            return 'date'
        elif not (hospital_id_entry.isdigit() and len(hospital_id_entry)==6):
            return 'hospital id'
        elif not (scan_id_entry.isdigit() and len(scan_id_entry)==4):
            return 'scan id'
        elif not (isinstance(scan_type_entry, str) and scan_type_entry!=''):
            return 'scan type'
        elif not (isinstance(conclusion_entry, str) and conclusion_entry!=''):
            return 'conclusion'
        elif not (isinstance(doctors_entry, str) and doctors_entry!=''):
            return 'doctors'
        else:
            return 'OK'




class HospitalRecordManagement(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Hospital Record Management")
        self.w = tk.Tk.winfo_screenwidth(self)
        self.h = tk.Tk.winfo_screenheight(self)
        tk.Tk.geometry(self, "{}x{}".format(self.w, self.h))

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Main, Add, Update, Delete, Search, Display, Exit):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Main)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class Main(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.header = tk.Frame(self, bd=4)
        self.header.pack(side='top', fill='x', expand=True, anchor='n')
        # footer = tk.Frame(self).pack(side='bottom')

        self.add_button = tk.Button(self.header, text='New Record', cursor='hand2',
                                    command=lambda: controller.show_frame(Add))
        self.add_button.pack(side='left', padx=10, pady=5)
        self.update_button = tk.Button(self.header, text='Update Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Update))
        self.update_button.pack(side='left', padx=10, pady=5)
        self.delete_button = tk.Button(self.header, text='Delete Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Delete))
        self.delete_button.pack(side='left', padx=10, pady=5)
        self.search_button = tk.Button(self.header, text='Search', cursor='hand2',
                                       command=lambda: controller.show_frame(Search))
        self.search_button.pack(side='left', padx=10, pady=5)
        self.display_button = tk.Button(self.header, text='Display Record', cursor='hand2',
                                        command=lambda: controller.show_frame(Display))
        self.display_button.pack(side='left', padx=10, pady=5)
        self.exit_button = tk.Button(self.header, text='Exit', cursor='hand2',
                                     command=Quit)
        self.exit_button.pack(side='left', padx=10, pady=5)

        self.body = tk.Frame(self)
        self.body.pack(fill='both', expand=True, anchor='n')
        self.label = tk.Label(self.body, text='Home')
        self.label.pack()


class Add(tk.Frame):



    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.database = Database()
        self.scan_list = ['Abdominal', 'Abdomino-pelvic', 'Doppler', 'Occular', 'Obstretrics', 'Thyroid', 'TVS']
        self.doctorsList = ['Alabi', 'Atim', 'Anako', 'Momodu', 'Simon', 'Shalangwa']
        self.genderList = ['Male', 'Female']


        self.first = tk.StringVar()
        self.last = tk.StringVar()
        self.v_age = tk.StringVar()
        self.v_gender = tk.StringVar()
        self.v_date = tk.StringVar()
        self.v_hos_id = tk.StringVar()
        self.v_scan_id = tk.StringVar()
        self.v_scan_type = tk.StringVar()
        self.v_indication = tk.StringVar()
        self.v_findings = tk.StringVar()
        self.v_conclusion = tk.StringVar()
        self.v_docs = tk.StringVar()



        self.header = tk.Frame(self, bd=5)
        self.header.pack(side='top', expand=True, anchor='n')
        # footer = tk.Frame(self).pack(side='bottom')

        self.add_button = tk.Button(self.header, text='New Record', cursor='hand2',
                                    command=lambda: controller.show_frame(Add))
        self.add_button.pack(side='left', padx=10, pady=5)
        self.update_button = tk.Button(self.header, text='Update Record', cursor='hand2',
                                  command=lambda: controller.show_frame(Update))
        self.update_button.pack(side='left', padx=10, pady=5)
        self.delete_button = tk.Button(self.header, text='Delete Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Delete))
        self.delete_button.pack(side='left', padx=10, pady=5)
        self.search_button = tk.Button(self.header, text='Search', cursor='hand2',
                                       command=lambda: controller.show_frame(Search))
        self.search_button.pack(side='left', padx=10, pady=5)
        self.display_button = tk.Button(self.header, text='Display Record', cursor='hand2',
                                        command=lambda: controller.show_frame(Display))
        self.display_button.pack(side='left', padx=10, pady=5)
        self.exit_button = tk.Button(self.header, text='Exit', cursor='hand2',
                                     command=Quit)
        self.exit_button.pack(side='left', padx=10, pady=5)

        self.body = tk.Frame(self, bg='green')
        self.body.pack(fill='both', expand=True, anchor='n')

        self.name_frame = tk.Frame(self.body)
        self.name_frame.pack(side='top', fill='x')
        self.indication_frame = tk.Frame(self.body)
        self.indication_frame.pack(side='top', fill='x')
        self.findings_frame = tk.Frame(self.body)
        self.findings_frame.pack(side='top', fill='both')
        self.conclusion_frame = tk.Frame(self.body)
        self.conclusion_frame.pack(side='top', fill='x')
        self.doctors_frame = tk.Frame(self.body)
        self.doctors_frame.pack(side='top', fill='x')
        self.submit_frame = tk.Frame(self.body)
        self.submit_frame.pack(side='top')

        self.first_name = tk.Label(self.name_frame, text='First Name')
        self.first_name.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.first_name_entry = tk.Entry(self.name_frame, textvariable=self.first)
        self.first_name_entry.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.last_name = tk.Label(self.name_frame, text='Last Name')
        self.last_name.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.last_name_entry = tk.Entry(self.name_frame, textvariable=self.last)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        self.age = tk.Label(self.name_frame, text='Age')
        self.age.grid(row=0, column=2, padx=10, pady=5, sticky='w')

        self.age_entry = tk.Entry(self.name_frame, textvariable=self.v_age)
        self.age_entry.grid(row=1, column=2, padx=10, pady=5, sticky='w')

        self.gender = ttk.Label(self.name_frame, text='Gender')
        self.gender.grid(row=0, column=3, padx=10, pady=5, sticky='w')

        self.gender_entry = ttk.Combobox(self.name_frame, values=self.genderList, textvariable=self.v_gender)
        self.gender_entry.grid(row=1, column=3, padx=10, pady=5, sticky='w')

        self.date = tk.Label(self.name_frame, text='Date')
        self.date.grid(row=0, column=4, padx=10, pady=5, sticky='w')

        self.date_entry = tk.Entry(self.name_frame, textvariable=self.v_date)
        self.date_entry.grid(row=1, column=4, padx=10, pady=5, sticky='w')

        self.hospital_id = tk.Label(self.name_frame, text='Hospital ID')
        self.hospital_id.grid(row=0, column=5, padx=10, pady=5, sticky='w')

        self.hospital_id_entry = tk.Entry(self.name_frame, textvariable=self.v_hos_id)
        self.hospital_id_entry.grid(row=1, column=5, padx=10, pady=5, sticky='w')

        self.scan_id = tk.Label(self.name_frame, text='Scan ID')
        self.scan_id.grid(row=0, column=6, padx=10, pady=5, sticky='w')

        self.scan_id_entry = tk.Entry(self.name_frame, textvariable=self.v_scan_id)
        self.scan_id_entry.grid(row=1, column=6, padx=10, pady=5, sticky='w')

        self.scan_type = tk.Label(self.indication_frame, text='Scan Type')
        self.scan_type.grid(row=0, column=0, padx=10, pady=5, sticky='e')

        self.scan_type_entry = ttk.Combobox(self.indication_frame, values=self.scan_list, textvariable=self.v_scan_type)
        self.scan_type_entry.grid(row=0, column=1, padx=10, pady=5, sticky='e')

        self.indication = tk.Label(self.indication_frame, text='Indication')
        self.indication.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.indication_entry = tk.Entry(self.indication_frame, textvariable=self.v_indication)
        self.indication_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')


        self.findings = tk.Label(self.findings_frame, text='Findings')
        self.findings.pack(anchor='w', padx=10)
        self.findings_entry = ScrolledText(self.findings_frame, wrap='word')
        self.findings_entry.pack(fill='x', padx=10, pady=5)


        self.conclusion = tk.Label(self.conclusion_frame, text='Conclusion')
        self.conclusion.grid(row=9, column=0, padx=10, pady=5, sticky='w')

        self.conclusion_entry = tk.Entry(self.conclusion_frame, textvariable=self.v_conclusion)
        self.conclusion_entry.grid(row=9, column=1, padx=10, pady=5, sticky='w')

        self.doctors = tk.Label(self.doctors_frame, text='Doctors')
        self.doctors.grid(row=10, column=0, padx=10, pady=5, sticky='w')

        self.doctors_entry = ttk.Combobox(self.doctors_frame, values=self.doctorsList, textvariable=self.v_docs)
        self.doctors_entry.grid(row=10, column=1, padx=10, pady=5, sticky='e')

        self.submit = tk.Button(self.submit_frame, text='Submit', font=small_font, command=self.Submit)
        self.submit.pack(side='bottom', fill='x')


    def Submit(self):







        self.values = Values()
        self.test = self.values.validate(self.first_name_entry.get(), self.last_name_entry.get(), self.age_entry.get(), self.gender_entry.get(), self.date_entry.get(), self.hospital_id_entry.get(), self.scan_id_entry.get(), self.scan_type_entry.get(), self.conclusion_entry.get(), self.doctors_entry.get())

        if (self.test == 'OK'):


            try:
                self.database.insert(self.first_name_entry.get(), self.last_name_entry.get(), self.age_entry.get(), self.gender_entry.get(), self.date_entry.get(), self.hospital_id_entry.get(), self.scan_id_entry.get(), self.scan_type_entry.get(), self.indication_entry.get(), self.findings_entry.get("1.0", tk.END), self.conclusion_entry.get(), self.doctors_entry.get())




            except Exception as err:
                messagebox.showerror("Error", "Record not successfully entered. \n" + str(err))


            else:
                messagebox.showinfo('Success', 'Records successfully entered.')
                self.clear()

        else:
            self.message = 'Invalid input in field {}'.format(self.test)
            messagebox.showerror("Error", self.message)

    def clear(self):
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.gender_entry.set('')
        self.date_entry.delete(0, tk.END)
        self.hospital_id_entry.delete(0, tk.END)
        self.scan_id_entry.delete(0, tk.END)
        self.scan_type_entry.set('')
        self.indication_entry.delete(0, tk.END)
        self.findings_entry.delete(0, tk.END)
        self.conclusion_entry.delete(0, tk.END)
        self.doctors_entry.set('')


class Update(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.elements = ['First Name', 'Last Name', 'Hospital ID', 'Scan ID']
        self.v = tk.StringVar()
        self.vv = 'First Name'

        self.header = tk.Frame(self, bd=4)
        self.header.pack(side='top', fill='x', ipady=10)
        # footer = tk.Frame(self).pack(side='bottom')

        self.add_button = tk.Button(self.header, text='New Record', cursor='hand2',
                                    command=lambda: controller.show_frame(Add))
        self.add_button.pack(side='left', padx=10, pady=5)
        self.update_button = tk.Button(self.header, text='Update Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Update))
        self.update_button.pack(side='left', padx=10, pady=5)
        self.delete_button = tk.Button(self.header, text='Delete Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Delete))
        self.delete_button.pack(side='left', padx=10, pady=5)
        self.search_button = tk.Button(self.header, text='Search', cursor='hand2',
                                       command=lambda: controller.show_frame(Search))
        self.search_button.pack(side='left', padx=10, pady=5)
        self.display_button = tk.Button(self.header, text='Display Record', cursor='hand2',
                                        command=lambda: controller.show_frame(Display))
        self.display_button.pack(side='left', padx=10, pady=5)
        self.exit_button = tk.Button(self.header, text='Exit', cursor='hand2',
                                     command=Quit)
        self.exit_button.pack(side='left', padx=10, pady=5)

        self.body = tk.Frame(self)
        self.body.pack(fill='both', expand=True, anchor='n')

        self.label = tk.Label(self.body, text='Update Record', font=small_font)
        self.label.grid(row=0, columnspan=4)

        self.search_text = tk.Label(self.body, text='Enter {} to update'.format(self.vv), font=small_font)
        self.search_text.grid(row=1, column=0, padx=100, pady=100, ipady=10)

        self.search_entry = tk.Entry(self.body)
        self.search_entry.grid(row=1, column=1, padx=100, pady=100, sticky='w', ipady=10)

        self.or_search_by = tk.Label(self.body, text=' or search by', font=small_font)
        self.or_search_by.grid(row=1, column=2, padx=10, pady=100, ipady=10)

        self.search_filter = ttk.Combobox(self.body, values=self.elements, textvariable=self.v, font=small_font)
        self.search_filter.current(0)
        self.vv = self.search_filter.current(0)
        self.search_filter.grid(row=1, column=3, padx=10, pady=100, ipady=10)

        self.search = tk.Button(self.body, text='Update', font=small_font)
        self.search.grid(row=2, columnspan=4, ipady=10)

    def Search(self):
        self.database = Database()
        self.data = self.database.search(self.search_entry.get())



class Delete(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.elements = ['First Name', 'Last Name', 'Hospital ID', 'Scan ID']
        self.v = tk.StringVar()
        self.vv = 'First Name'

        self.header = tk.Frame(self, bd=4)
        self.header.pack(side='top', fill='x', ipady=10)
        # footer = tk.Frame(self).pack(side='bottom')

        self.add_button = tk.Button(self.header, text='New Record', cursor='hand2',
                                    command=lambda: controller.show_frame(Add))
        self.add_button.pack(side='left', padx=10, pady=5)
        self.update_button = tk.Button(self.header, text='Update Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Update))
        self.update_button.pack(side='left', padx=10, pady=5)
        self.delete_button = tk.Button(self.header, text='Delete Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Delete))
        self.delete_button.pack(side='left', padx=10, pady=5)
        self.search_button = tk.Button(self.header, text='Search', cursor='hand2',
                                       command=lambda: controller.show_frame(Search))
        self.search_button.pack(side='left', padx=10, pady=5)
        self.display_button = tk.Button(self.header, text='Display Record', cursor='hand2',
                                        command=lambda: controller.show_frame(Display))
        self.display_button.pack(side='left', padx=10, pady=5)
        self.exit_button = tk.Button(self.header, text='Exit', cursor='hand2',
                                     command=Quit)
        self.exit_button.pack(side='left', padx=10, pady=5)

        self.body = tk.Frame(self)
        self.body.pack(fill='both', expand=True, anchor='n')

        self.label = tk.Label(self.body, text='Delete Record', font=small_font)
        self.label.grid(row=0, columnspan=4)

        self.search_text = tk.Label(self.body, text='Enter {} to delete'.format(self.vv), font=small_font)
        self.search_text.grid(row=1, column=0, padx=100, pady=100, ipady=10)

        self.search_entry = tk.Entry(self.body)
        self.search_entry.grid(row=1, column=1, padx=100, pady=100, sticky='w', ipady=10)

        self.or_search_by = tk.Label(self.body, text=' or search by', font=small_font)
        self.or_search_by.grid(row=1, column=2, padx=10, pady=100, ipady=10)

        self.search_filter = ttk.Combobox(self.body, values=self.elements, textvariable=self.v, font=small_font)
        self.search_filter.current(0)
        self.vv = self.search_filter.current(0)
        self.search_filter.grid(row=1, column=3, padx=10, pady=100, ipady=10)

        self.search = tk.Button(self.body, text='Delete', font=small_font)
        self.search.grid(row=2, columnspan=4, ipady=10)

    def Search(self):
        self.database = Database()
        self.data = self.database.search(self.search_entry.get())




class Search(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.database = Database()
        self.elements = ['First Name', 'Last Name', 'Hospital ID', 'Scan ID']
        self.v = tk.StringVar()
        self.vv = 'First Name'

        self.header = tk.Frame(self, bd=4)
        self.header.pack(side='top', fill='x', ipady=10)
        # footer = tk.Frame(self).pack(side='bottom')

        self.add_button = tk.Button(self.header, text='New Record', cursor='hand2',
                                    command=lambda: controller.show_frame(Add))
        self.add_button.pack(side='left', padx=10, pady=5)
        self.update_button = tk.Button(self.header, text='Update Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Update))
        self.update_button.pack(side='left', padx=10, pady=5)
        self.delete_button = tk.Button(self.header, text='Delete Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Delete))
        self.delete_button.pack(side='left', padx=10, pady=5)
        self.search_button = tk.Button(self.header, text='Search', cursor='hand2',
                                       command=lambda: controller.show_frame(Search))
        self.search_button.pack(side='left', padx=10, pady=5)
        self.display_button = tk.Button(self.header, text='Display Record', cursor='hand2',
                                        command=lambda: controller.show_frame(Display))
        self.display_button.pack(side='left', padx=10, pady=5)
        self.exit_button = tk.Button(self.header, text='Exit', cursor='hand2',
                                     command=Quit)
        self.exit_button.pack(side='left', padx=10, pady=5)

        self.body = tk.Frame(self)
        self.body.pack(fill='both', expand=True, anchor='n')

        self.label = tk.Label(self.body, text='Search Record', font=small_font)
        self.label.grid(row=0, columnspan=4)

        self.search_text = tk.Label(self.body, text='Enter {} to search'.format(self.vv), font=small_font)
        self.search_text.grid(row=1, column=0, padx=100, pady=100, ipady=10)

        self.search_entry = tk.Entry(self.body)
        self.search_entry.grid(row=1, column=1, padx=100, pady=100, sticky='w', ipady=10)

        self.or_search_by = tk.Label(self.body, text=' or search by', font=small_font)
        self.or_search_by.grid(row=1, column=2, padx=10, pady=100, ipady=10)


        self.search_filter = ttk.Combobox(self.body, values=self.elements, textvariable=self.v, font=small_font)
        self.search_filter.current(0)
        self.vv = self.search_filter.current(0)
        self.search_filter.grid(row=1, column=3, padx=10, pady=100, ipady=10)

        self.search = tk.Button(self.body, text='Search', font=small_font, command=self.popup)
        self.search.grid(row=2, columnspan=4, ipady=10)

    def Search(self):




        self.data = self.database.search(self.search_entry.get())



    def popup(self):
        win = tk.Toplevel()
        win.wm_title('Search Result')

        scan_list = ['Abdominal', 'Abdomino-pelvic', 'Doppler', 'Ocular', 'Obstretrics', 'Thyroid', 'TVS']
        doctorsList = self.database.search(self, str(doctors))
        genderList = ['Male', 'Female']

        first = tk.StringVar()
        last = tk.StringVar()
        v_age = tk.StringVar()
        v_gender = tk.StringVar()
        v_date = tk.StringVar()
        v_hos_id = tk.StringVar()
        v_scan_id = tk.StringVar()
        v_scan_type = tk.StringVar()
        v_indication = tk.StringVar()
        v_findings = tk.StringVar()
        v_conclusion = tk.StringVar()
        v_docs = tk.StringVar()


        body = tk.Frame(win, bg='green')
        body.pack(fill='both', expand=True, anchor='n')

        name_frame = tk.Frame(body)
        name_frame.pack(side='top', fill='x')
        indication_frame = tk.Frame(body)
        indication_frame.pack(side='top', fill='x')
        findings_frame = tk.Frame(body)
        findings_frame.pack(side='top', fill='both')
        conclusion_frame = tk.Frame(body)
        conclusion_frame.pack(side='top', fill='x')
        doctors_frame = tk.Frame(body)
        doctors_frame.pack(side='top', fill='x')
        submit_frame = tk.Frame(body)
        submit_frame.pack(side='top')

        first_name = tk.Label(name_frame, text='First Name')
        first_name.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        first_name_entry = tk.Entry(name_frame, textvariable=first)
        first_name_entry.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        last_name = tk.Label(name_frame, text='Last Name')
        last_name.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        last_name_entry = tk.Entry(name_frame, textvariable=last)
        last_name_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        age = tk.Label(name_frame, text='Age')
        age.grid(row=0, column=2, padx=10, pady=5, sticky='w')

        age_entry = tk.Entry(name_frame, textvariable=v_age)
        age_entry.grid(row=1, column=2, padx=10, pady=5, sticky='w')

        gender = ttk.Label(name_frame, text='Gender')
        gender.grid(row=0, column=3, padx=10, pady=5, sticky='w')

        gender_entry = ttk.Combobox(name_frame, values=genderList, textvariable=v_gender)
        gender_entry.grid(row=1, column=3, padx=10, pady=5, sticky='w')

        date = tk.Label(name_frame, text='Date')
        date.grid(row=0, column=4, padx=10, pady=5, sticky='w')

        date_entry = tk.Entry(name_frame, textvariable=v_date)
        date_entry.grid(row=1, column=4, padx=10, pady=5, sticky='w')

        hospital_id = tk.Label(name_frame, text='Hospital ID')
        hospital_id.grid(row=0, column=5, padx=10, pady=5, sticky='w')

        hospital_id_entry = tk.Entry(name_frame, textvariable=v_hos_id)
        hospital_id_entry.grid(row=1, column=5, padx=10, pady=5, sticky='w')

        scan_id = tk.Label(name_frame, text='Scan ID')
        scan_id.grid(row=0, column=6, padx=10, pady=5, sticky='w')

        scan_id_entry = tk.Entry(name_frame, textvariable=v_scan_id)
        scan_id_entry.grid(row=1, column=6, padx=10, pady=5, sticky='w')

        scan_type = tk.Label(indication_frame, text='Scan Type')
        scan_type.grid(row=0, column=0, padx=10, pady=5, sticky='e')

        scan_type_entry = ttk.Combobox(indication_frame, values=scan_list, textvariable=v_scan_type)
        scan_type_entry.grid(row=0, column=1, padx=10, pady=5, sticky='e')

        indication = tk.Label(indication_frame, text='Indication')
        indication.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        indication_entry = tk.Entry(indication_frame, textvariable=v_indication)
        indication_entry.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        findings = tk.Label(findings_frame, text='Findings')
        findings.pack(anchor='w', padx=10)
        findings_entry = ScrolledText(findings_frame, wrap='word')
        findings_entry.pack(fill='x', padx=10, pady=5)

        conclusion = tk.Label(conclusion_frame, text='Conclusion')
        conclusion.grid(row=9, column=0, padx=10, pady=5, sticky='w')

        conclusion_entry = tk.Entry(conclusion_frame, textvariable=v_conclusion)
        conclusion_entry.grid(row=9, column=1, padx=10, pady=5, sticky='w')

        doctors = tk.Label(doctors_frame, text='Doctors')
        doctors.grid(row=10, column=0, padx=10, pady=5, sticky='w')

        doctors_entry = ttk.Combobox(doctors_frame, values=doctorsList, textvariable=v_docs)
        doctors_entry.grid(row=10, column=1, padx=10, pady=5, sticky='e')

        submit = tk.Button(submit_frame, text='Submit', font=small_font)#, command=Submit)
        submit.pack(side='bottom', fill='x')

        first.set('first')
        last.set('last')
        v_age.set('age')
        v_gender.set('male')
        v_date.set('01/01/0101')
        v_hos_id.set('123456')
        v_scan_id.set('1234')
        v_scan_type.set('hsg')
        v_indication.set('indication')
        v_findings.set('findings')
        v_conclusion.set('conclusion')
        v_docs.set('doctors')

class Display(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        self.database = Database()
        self.data = self.database.display()

        self.header = tk.Frame(self, bd=4, bg='red')
        self.header.pack(side='top', fill='x', expand=True, anchor='n', ipady=10)
        # footer = tk.Frame(self).pack(side='bottom')

        self.add_button = tk.Button(self.header, text='New Record', cursor='hand2',
                                    command=lambda: controller.show_frame(Add))
        self.add_button.pack(side='left', padx=10, pady=5)
        self.update_button = tk.Button(self.header, text='Update Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Update))
        self.update_button.pack(side='left', padx=10, pady=5)
        self.delete_button = tk.Button(self.header, text='Delete Record', cursor='hand2',
                                       command=lambda: controller.show_frame(Delete))
        self.delete_button.pack(side='left', padx=10, pady=5)
        self.search_button = tk.Button(self.header, text='Search', cursor='hand2',
                                       command=lambda: controller.show_frame(Search))
        self.search_button.pack(side='left', padx=10, pady=5)
        self.display_button = tk.Button(self.header, text='Display Record', cursor='hand2',
                                        command=lambda: controller.show_frame(Display))
        self.display_button.pack(side='left', padx=10, pady=5)
        self.exit_button = tk.Button(self.header, text='Exit', cursor='hand2',
                                     command=Quit)
        self.exit_button.pack(side='left', padx=10, pady=5)

        self.body = tk.Frame(self, bg='green')
        self.body.pack(side='top', fill='both', expand=True, anchor='n')


        tk.Label(self.body, text="Record List").pack(side='top')



        self.display = ttk.Treeview(self.body)
        self.display.pack(fill='both')


        self.display['show'] = 'headings'
        self.display['columns'] = ('first_name', 'last_name', 'age', 'gender', 'date', 'hospital_id', 'scan_id', 'doctors')

        self.display.heading('first_name', text='First Name')
        self.display.heading('last_name', text='Last Name')
        self.display.heading('age', text='Age')
        self.display.heading('gender', text='Gender')
        self.display.heading('date', text='Date')
        self.display.heading('hospital_id', text='Hospital ID')
        self.display.heading('scan_id', text='Scan ID')
        self.display.heading('doctors', text='Doctors')


        self.display.column('age', width=150, stretch=tk.NO)
        self.display.column('gender', width=150, stretch=tk.NO)

        for d in self.data:
            display_data = d
            self.display.insert('', 'end', values=(d))


class Exit(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)



        # header = tk.Frame(self, bd=4)
        # header.pack(side='top', fill='x', expand=True, anchor='n')
        # # footer = tk.Frame(self).pack(side='bottom')
        #
        # add_button = tk.Button(header, text='New Record', cursor='hand2',
        #                        command=lambda: controller.show_frame(Add))
        # add_button.pack(side='left', padx=10, pady=5)
        # update_button = tk.Button(header, text='Update Record', cursor='hand2',
        #                           command=lambda: controller.show_frame(Update))
        # update_button.pack(side='left', padx=10, pady=5)
        # delete_button = tk.Button(header, text='Delete Record', cursor='hand2',
        #                           command=lambda: controller.show_frame(Delete))
        # delete_button.pack(side='left', padx=10, pady=5)
        # search_button = tk.Button(header, text='Search', cursor='hand2',
        #                           command=lambda: controller.show_frame(Search))
        # search_button.pack(side='left', padx=10, pady=5)
        # display_button = tk.Button(header, text='Display Record', cursor='hand2',
        #                            command=lambda: controller.show_frame(Display))
        # display_button.pack(side='left', padx=10, pady=5)
        # exit_button = tk.Button(header, text='Exit', cursor='hand2',
        #                         command=lambda: controller.show_frame(Exit))
        # exit_button.pack(side='left', padx=10, pady=5)
        #
        # body = tk.Frame(self)
        # body.pack(fill='both', expand=True, anchor='n')
        # label = tk.Label(body, text='Exit')
        # label.pack()

        # q = messagebox.askyesno('Exit', 'Are you sure you want to exit?')
        # if q == 'yes':
        #     self.destroy()

app = HospitalRecordManagement()
app.mainloop()
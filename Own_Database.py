import sqlite3
import os


def cool_figlet():
    print("""
  ____    _____    ____  
 / __ \  |  __ \  |  _ \ 
| |  | | | |  | | | |_) |
| |  | | | |  | | |  _ < 
| |__| | | |__| | | |_) |
 \____/  |_____/  |____/ 
    """)


def create_db():
    name_db = input("Name database : ") + ".db"
    db = sqlite3.connect(name_db)
    db.commit()
    db.close()


def sel_db():
    n = 1
    print("Which database do you want to edit : ")
    db_in_file = []
    for a in os.listdir(os.getcwd()):
        if a[-3:] == ".db":
            db_in_file.append(a)
    for x in db_in_file:
        print(n - 1, x)
        n = n + 1
    selection = int(input())
    return db_in_file[selection]


def create_tables(selected):
    name_table = input("Name your table : ")
    cols = []
    cols_types = []
    a = 0
    while True:
        new_col = input("Name %d. column (n/i) : " % (a + 1))
        if new_col[-1] == "n":
            cols_types.append("TEXT")
        elif new_col[-1] == "i":
            cols_types.append("INT")
        elif new_col == "cancel":
            os.system("cls")
            break
        cols.append(new_col[0:-2])
        a = a + 1

    sql_cols = "("
    for i in range(0, (len(cols) - 1)):
        sql_cols += cols[i] + " " + cols_types[i] + ","
    sql_cols += cols[-1] + " " + cols_types[-1]
    sql_cols = sql_cols + ")"
    db = sqlite3.connect(selected)
    ptr = db.cursor()
    ptr.execute("CREATE TABLE IF NOT EXISTS %s" % name_table + sql_cols)
    db.commit()


def sel_table(selected):
    db = sqlite3.connect(selected)
    ptr = db.cursor()
    ptr.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = ptr.fetchall()
    c = 0
    for a in tables:
        for x in a:
            print(c, ".", x)
            c += 1
    tab_sel = int(input("Which table do you want to edit : "))
    return tables[tab_sel][0]


def insert_data(table, selected):
    db = sqlite3.connect(selected)
    ptr = db.cursor()
    ptr.execute("SELECT * FROM PRAGMA_TABLE_INFO('%s')" % table)
    fetched_cols = ptr.fetchall()
    count = int(input("How many rows  : "))
    while count > 0:
        new_data = []
        for a in fetched_cols:
            if a[2] == "TEXT":
                new_data.append(input("%s : " % a[1]))
            elif a[2] == "INT":
                new_data.append(int(input("%s : " % a[1])))
        vals = ("?," * len(new_data))[:-1]
        command = "INSERT INTO %%s VALUES(%s)" % vals
        ptr.execute((command) % (table), (new_data))
        count -= 1
    db.commit()


def search_data(selected):
    db = sqlite3.connect(selected)
    table = sel_table(selected)
    os.system("cls")
    cool_figlet()
    ptr = db.cursor()
    ptr.execute("SELECT * FROM %s" % (table))
    all_data = ptr.fetchall()
    ptr.execute("SELECT * FROM PRAGMA_TABLE_INFO('%s')" % table)
    table_names = ptr.fetchall()
    ctr_3 = 0
    for i in table_names:
        print(ctr_3, ".", i[1])
        ctr_3 += 1
    search_type = input("Search By : ")
    key = input("Search For : ")
    d = 0
    for i in all_data:
        if key in i or key in str(i):
            print(i)
            d += 1
    if d > 0:
        input("Press Enter to continue : ")
        os.system("cls")
    elif d == 0:
        input("There is no match...Press Enter to continue : ")
        os.system("cls")


def show_all(selected):
    db = sqlite3.connect(selected)
    table = sel_table(selected)
    os.system("cls")
    cool_figlet()
    ptr = db.cursor()
    ptr.execute("SELECT * FROM PRAGMA_TABLE_INFO('%s')" % table)
    cols = ptr.fetchall()
    print(" ", end="")
    for i in cols:
        print(i[1], end=" ")
    ptr.execute("SELECT * FROM %s" % table)
    a = ptr.fetchall()
    print("\n")
    count = 1
    for i in a:
        print(str(count) + ".", end="")
        for x in i:
            print(x, end=" ")
        count += 1
        print("\n")
    input("\nPress Enter to continue : ")


def delete_data(selected):
    db = sqlite3.connect(selected)
    table = sel_table(selected)
    os.system("cls")
    cool_figlet()
    ptr = db.cursor()
    ptr.execute("SELECT * FROM PRAGMA_TABLE_INFO('%s')" % table)
    cols = ptr.fetchall()
    ctr = 0
    for i in cols:
        print(str(ctr) + "." + i[1])
        ctr += 1
    filter_type = cols[int(input("Delete by which filter : "))][1]
    data = input("Delete the row where %s is : " % filter_type)
    print(table,filter_type,data)
    ptr.execute("DELETE FROM %s WHERE %s = %s" % (table, filter_type, data))
    db.commit()


def edit_data(selected):
    db = sqlite3.connect(selected)
    table = sel_table(selected)
    os.system("cls")
    cool_figlet()
    ptr = db.cursor()
    ptr.execute("SELECT * FROM PRAGMA_TABLE_INFO('%s')" % table)
    cols = ptr.fetchall()
    ctr = 0
    for i in cols:
        print(str(ctr) + "." + i[1])
        ctr += 1
    filter = cols[int(input("Edit by which filter : "))][1]
    filter_index = input("What is the filter value : ")
    change_col = cols[int(input("Which one shall be changed : "))][1]
    new_col_index = input("New value : ")
    ptr.execute("UPDATE %s SET %s = '%s' WHERE %s = '%s'" % (table, change_col, new_col_index, filter, filter_index))
    db.commit()


while True:

    cool_figlet()

    print("""
    1.Create New Database
    2.Select A Database To Edit
    """)
    men_chos = input("Select an option : ")
    if men_chos == "1":
        os.system("cls")
        cool_figlet()
        create_db()
        os.system("cls")
    elif men_chos == "2":
        os.system("cls")
        cool_figlet()
        selected = sel_db()
        os.system("cls")
        while True:
            os.system("cls")
            cool_figlet()
            print("""
            1.Create Table
            2.Add New Data
            3.Search Data
            4.Show All Data
            5.Delete Data
            6.Edit Data
            """)
            men_chos_2 = input("Select an option : ")
            if men_chos_2 == "1":
                os.system("cls")
                cool_figlet()
                create_tables(selected)
            if men_chos_2 == "2":
                os.system("cls")
                cool_figlet()
                table = sel_table(selected)
                os.system("cls")
                cool_figlet()
                insert_data(table, selected)
                os.system("cls")
            if men_chos_2 == "3":
                os.system("cls")
                cool_figlet()
                search_data(selected)
            if men_chos_2 == "4":
                os.system("cls")
                cool_figlet()
                show_all(selected)
            if men_chos_2 == "5":
                os.system("cls")
                cool_figlet()
                delete_data(selected)
            if men_chos_2 == "6":
                os.system("cls")
                cool_figlet()
                edit_data(selected)
            if men_chos_2 == "cancel":
                os.system("cls")
                break
    elif men_chos == "cancel":
        break

# CodeWay-Internship
from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def add_task_to_list():  
    task_string = task_field.get()  
    if len(task_string) == 0:  
        messagebox.showinfo('Error', 'Field is Empty.')  
    else:    
        tasks_list.append(task_string)   
        the_cursor.execute('insert into tasks values (?)', (task_string ,))    
        update_task_list_widget()    
        task_field.delete(0, 'end')  
    
def update_task_list_widget():    
    clear_task_list_widget()    
    for task in tasks_list:    
        task_listbox.insert('end', task)  
  
def delete_selected_task():  
    try:  
        selected_task = task_listbox.get(task_listbox.curselection())    
        if selected_task in tasks_list:  
            tasks_list.remove(selected_task)    
            update_task_list_widget()   
            the_cursor.execute('delete from tasks where title = ?', (selected_task,))
    except:   
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')        

def delete_all_tasks_from_list():  
    confirmation = messagebox.askyesno('Delete All', 'Are you sure?')  
    if confirmation:    
        while(len(tasks_list) != 0):    
            tasks_list.pop()    
        the_cursor.execute('delete from tasks')   
        update_task_list_widget()  
   
def clear_task_list_widget():   
    task_listbox.delete(0, 'end')  
  
def close_program():    
    print(tasks_list)   
    gui_window.destroy()  
    
def retrieve_tasks_from_database():    
    while(len(tasks_list) != 0):    
        tasks_list.pop()    
    for row in the_cursor.execute('select title from tasks'):    
        tasks_list.append(row[0])  

if __name__ == "__main__":   
    gui_window = Tk()   
    gui_window.title("To-Do List ")  
    gui_window.geometry("665x400+550+250")   
    gui_window.resizable(0, 0)  
    gui_window.configure(bg="#B5E5CF")  
    
    database_connection = sql.connect('listOfTasks.db')   
    the_cursor = database_connection.cursor()   
    the_cursor.execute('create table if not exists tasks (title text)')  
    
    tasks_list = []  
    
    functions_frame = Frame(gui_window, bg="#8EE5EE") 
    
    functions_frame.pack(side="top", expand=True, fill="both")  
 
    task_label = Label(functions_frame, text="TO-DO-LIST \n Enter the Task Title:", font=("arial", "14", "bold"), background="#8EE5EE", foreground="#FF6103")    
    task_label.place(x=20, y=30)  
    
    task_field = Entry(functions_frame, font=("Arial", "14"), width=42, foreground="black", background="white")    
    task_field.place(x=180, y=30)  
    
    add_button = Button(functions_frame, text="Add", width=15, bg='#D4AC0D', font=("arial", "14", "bold"), command=add_task_to_list)  
    del_button = Button(functions_frame, text="Remove", width=15, bg='#D4AC0D', font=("arial", "14", "bold"), command=delete_selected_task)  
    del_all_button = Button(functions_frame, text="Delete All", width=15, font=("arial", "14", "bold"), bg='#D4AC0D', command=delete_all_tasks_from_list)    
    exit_button = Button(functions_frame, text="Exit / Close", width=52, bg='#D4AC0D', font=("arial", "14", "bold"), command=close_program)    
    
    add_button.place(x=18, y=80)  
    del_button.place(x=240, y=80)  
    del_all_button.place(x=460, y=80)  
    exit_button.place(x=17, y=330)  
    
    task_listbox = Listbox(functions_frame, width=70, height=9, font="bold", selectmode='SINGLE', background="WHITE", foreground="BLACK", selectbackground="#FF8C00", selectforeground="BLACK")    
    task_listbox.place(x=17, y=140)  
    
    retrieve_tasks_from_database()  
    update_task_list_widget()    
    gui_window.mainloop()    
    database_connection.commit()  
    the_cursor.close()

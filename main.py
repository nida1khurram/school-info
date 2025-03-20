import streamlit as st
import pandas as pd
import os

# Define a specific directory to save the data
SAVE_DIR = "student_data"  # Directory name
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)  # Create the directory if it doesn't exist

# File path for saving data
DATA_FILE = os.path.join(SAVE_DIR, "students_data.csv")

# Load existing data from CSV (if the file exists)
if os.path.exists(DATA_FILE):
    st.session_state.students = pd.read_csv(DATA_FILE)
else:
    st.session_state.students = pd.DataFrame(columns=[
        'ID', 'Name', 'Age', 'Class', 'Phone', 'Address', 'Parent Info'
    ])

# Function to save data to CSV
def save_data():
    st.session_state.students.to_csv(DATA_FILE, index=False)

# Function to generate a unique student ID
def generate_unique_id():
    if st.session_state.students.empty:
        return 1  # Start from ID 1 if no students exist
    else:
        return st.session_state.students['ID'].max() + 1  # Increment the maximum ID by 1

# Function to add a new student
def add_student(name, age, student_class, phone, address, parent_info):
    id = generate_unique_id()  # Generate a unique ID
    new_student = pd.DataFrame([[
        id, name, age, student_class, phone, address, parent_info
    ]], columns=['ID', 'Name', 'Age', 'Class', 'Phone', 'Address', 'Parent Info'])
    st.session_state.students = pd.concat([st.session_state.students, new_student], ignore_index=True)
    save_data()  # Save data after adding

# Function to filter students
def filter_students(filter_by, filter_value):
    if filter_by == 'ID':
        try:
            filter_value = int(filter_value)  # Convert to integer
            return st.session_state.students[st.session_state.students['ID'] == filter_value]
        except ValueError:
            st.warning("⚠️ Please enter a valid integer for ID.")
            return pd.DataFrame()  # Return an empty DataFrame if conversion fails
    elif filter_by == 'Name':
        return st.session_state.students[st.session_state.students['Name'].str.contains(filter_value, case=False)]
    elif filter_by == 'Class':
        return st.session_state.students[st.session_state.students['Class'] == filter_value]
    else:
        return st.session_state.students

# Function to modify student information
def modify_student(id, name, age, student_class, phone, address, parent_info):
    index = st.session_state.students[st.session_state.students['ID'] == id].index
    if not index.empty:
        st.session_state.students.at[index[0], 'Name'] = name
        st.session_state.students.at[index[0], 'Age'] = age
        st.session_state.students.at[index[0], 'Class'] = student_class
        st.session_state.students.at[index[0], 'Phone'] = phone
        st.session_state.students.at[index[0], 'Address'] = address
        st.session_state.students.at[index[0], 'Parent Info'] = parent_info
        save_data()  # Save data after modifying

# Function to delete a student
def delete_student(id):
    st.session_state.students = st.session_state.students[st.session_state.students['ID'] != id]
    save_data()  # Save data after deleting

# Streamlit UI
st.set_page_config(page_title="Student Information System", page_icon="📚", layout="wide")

# Custom CSS for colorful enhancements
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stHeader {
        color: #4a90e2;
    }
    .stButton button {
        background-color: #4a90e2;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
    }
    .stButton button:hover {
        background-color: #357abd;
    }
    .stDataFrame {
        border: 1px solid #4a90e2;
        border-radius: 5px;
    }
    .stSidebar {
        background-color: #4a90e2;
        color: white;
    }
    .stRadio label {
        color: white;
    }
    .stTextInput input, .stNumberInput input {
        border: 1px solid #4a90e2;
        border-radius: 5px;
    }
    .stSuccess {
        color: #28a745;
    }
    .stWarning {
        color: #ffc107;
    }
    .stInfo {
        color: #17a2b8;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title with colorful emoji
st.title("📚 WELCOME TO ABC SCHOOL")

# Sidebar for navigation using radio buttons
st.sidebar.header("Menu")
menu_option = st.sidebar.radio(
    "Select an Option",
    ["Home", "Add Student", "View Students", "Filter Students", "Modify Student", "Delete Student"],
    key="menu"
)

# Fixed classes from Nursery to Matric
CLASSES = ["Nursery", "KG", "Class 1", "Class 2", "Class 3", "Class 4", "Class 5", 
           "Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "Matric"]

# Home Page
if menu_option == "Home":
    st.header("🎉 Student Information System!")
    st.write("""
    This is a **Student Information System (SIS)** designed to manage student records efficiently. 
    You can add, view, filter, modify, and delete student information using this app.
    """)

    st.subheader("✨ Features")
    st.write("""
    - **Add Student:** Add new student records with details like ID, Name, Age, Class, Phone, Address, and Parent Info.
    - **View Students:** View all student records in a tabular format.
    - **Filter Students:** Filter students by ID, Name, or Class.
    - **Modify Student:** Update existing student records.
    - **Delete Student:** Remove student records from the system.
    """)

    st.subheader("📘 How to Use")
    st.write("""
    1. Use the **sidebar menu** to navigate to the desired functionality.
    2. **Add Student:** Fill in the form and click 'Add Student'.
    3. **View Students:** View all student records in the database.
    4. **Filter Students:** Select a filter criteria and enter the value to filter records.
    5. **Modify Student:** Enter the student ID and update the details.
    6. **Delete Student:** Enter the student ID to delete the record.
    """)

# Add Student
elif menu_option == "Add Student":
    st.header("➕ Add New Student")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0.0, step=0.1, format="%f")  # Accepts float and int
    student_class = st.selectbox("Class", CLASSES)  # Fixed classes dropdown
    phone = st.text_input("Phone Number")
    address = st.text_input("Address")
    parent_info = st.text_input("Parent Information")
    if st.button("Add Student"):
        add_student(name, age, student_class, phone, address, parent_info)
        st.success("🎉 Student added successfully!")

# View Students
elif menu_option == "View Students":
    st.header("👀 View All Students")
    if not st.session_state.students.empty:
        st.dataframe(st.session_state.students)
        
        # Add a button to download the data as a CSV file
        csv = st.session_state.students.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name='students_data.csv',
            mime='text/csv',
        )
    else:
        st.info("📂 No students found in the database.")

# Filter Students
elif menu_option == "Filter Students":
    st.header("🔍 Filter Students")
    filter_by = st.selectbox("Filter By", ["ID", "Name", "Class"])
    filter_value = st.text_input("Filter Value")
    if st.button("Filter"):
        if filter_value:  # Check if filter_value is not empty
            filtered_students = filter_students(filter_by, filter_value)
            if not filtered_students.empty:
                st.dataframe(filtered_students)
            else:
                st.warning("⚠️ No students match the filter criteria.")
        else:
            st.warning("⚠️ Please enter a filter value.")

# Modify Student
elif menu_option == "Modify Student":
    st.header("✏️ Modify Student Information")
    
    # Search by name
    search_name = st.text_input("Search by Name")
    if st.button("Search"):
        if search_name:
            filtered_students = filter_students("Name", search_name)
            if not filtered_students.empty:
                st.session_state.selected_student = filtered_students.iloc[0]
                st.success(f"Found student: {st.session_state.selected_student['Name']}")
            else:
                st.warning("⚠️ No student found with that name.")
        else:
            st.warning("⚠️ Please enter a name to search.")

    # Display current information if a student is selected
    if 'selected_student' in st.session_state:
        st.subheader("Current Information")
        st.write(st.session_state.selected_student)

        # Form to edit information
        st.subheader("Edit Information")
        name = st.text_input("Name", st.session_state.selected_student['Name'])
        age = st.number_input("Age", min_value=0.0, step=0.1, format="%f", value=float(st.session_state.selected_student['Age']))  # Accepts float and int
        student_class = st.selectbox("Class", CLASSES, index=CLASSES.index(st.session_state.selected_student['Class']))
        phone = st.text_input("Phone Number", st.session_state.selected_student['Phone'])
        address = st.text_input("Address", st.session_state.selected_student['Address'])
        parent_info = st.text_input("Parent Information", st.session_state.selected_student['Parent Info'])

        if st.button("Save Changes"):
            modify_student(
                st.session_state.selected_student['ID'],
                name,
                age,
                student_class,
                phone,
                address,
                parent_info
            )
            st.success("🎉 Student information modified successfully!")
            del st.session_state.selected_student  # Clear the selected student after saving

# Delete Student
elif menu_option == "Delete Student":
    st.header("🗑️ Delete Student")
    id = st.number_input("Enter Student ID to Delete", min_value=1, step=1)
    if st.button("Delete Student"):
        delete_student(id)
        st.success("🎉 Student deleted successfully!")
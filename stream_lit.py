import streamlit as st
import pandas as pd
from snowflake.snowpark.session import Session
import plotly.express as px

# Create Snowpark session
session = Session.builder.getOrCreate()

# Get current Snowflake user
def get_logged_in_user():
    query = "SELECT CURRENT_USER() AS username"
    return session.sql(query).to_pandas().iloc[0]['USERNAME']

# Get manager name for current user
def get_manager_name(username):
    query = f"""
        SELECT DISTINCT general_manager
        FROM EMPLOYEE_360.EMPLOYEE_DEMO.EMPLOEE_DETAILS
        WHERE LOWER(general_manager) = LOWER('{username}')
    """
    result = session.sql(query).to_pandas()
    return result.iloc[0]['GENERAL_MANAGER'] if not result.empty else None

# Get list of all manager names
@st.cache_data
def get_all_managers():
    query = """
        SELECT DISTINCT general_manager
        FROM EMPLOYEE_360.EMPLOYEE_DEMO.EMPLOEE_DETAILS
        WHERE general_manager IS NOT NULL
        ORDER BY general_manager
    """
    return session.sql(query).to_pandas()["GENERAL_MANAGER"].tolist()

# Fetch employee data for a manager
@st.cache_data
def fetch_employee_data(manager):
    query = f"""
        SELECT emp_id, emp_name, department, general_manager, designation, gender, EMPLOYMENT_TYPE
        FROM EMPLOYEE_360.EMPLOYEE_DEMO.EMPLOEE_DETAILS
        WHERE general_manager = '{manager}'
    """
    return session.sql(query).to_pandas()

# Get total employee count
@st.cache_data
def get_total_employee_count():
    query = "SELECT COUNT(*) AS total_employees FROM EMPLOYEE_360.EMPLOYEE_DEMO.EMPLOEE_DETAILS"
    return session.sql(query).to_pandas().iloc[0]['TOTAL_EMPLOYEES']

# Get employee count under selected manager
@st.cache_data
def get_employee_count_under_manager(manager):
    query = f"""
        SELECT COUNT(*) AS emp_count
        FROM EMPLOYEE_360.EMPLOYEE_DEMO.EMPLOEE_DETAILS
        WHERE general_manager = '{manager}'
    """
    return session.sql(query).to_pandas().iloc[0]['EMP_COUNT']

# -- MAIN APP STARTS HERE --
st.set_page_config(page_title="Employee Dashboard", layout="wide")
st.title("🛫 :red[Employee 360 - _J2TT_] ")

# Get current user and their manager name
logged_in_user = get_logged_in_user()
current_manager_name = get_manager_name(logged_in_user)

# Layout for Total Employees & Employees Reporting to Manager
col1, col2 = st.columns(2)

# Show total employees tile
total_emp = get_total_employee_count()
col1.metric("🏢 Total Employees in Company", total_emp)

# Manager dropdown
all_managers = get_all_managers()
selected_manager = st.selectbox("🔽 Select Your Name", all_managers)

# Get the number of employees reporting to the selected manager
employees_reporting_to_manager = get_employee_count_under_manager(selected_manager)
col2.metric(f"👤 Total Reportee's", employees_reporting_to_manager)

# If current user is the manager
if current_manager_name and selected_manager.lower() == current_manager_name.lower():
    df = fetch_employee_data(selected_manager)
    st.success(f"Showing Your Reportee's Data ")

    # --- Filter Employees Section ---
    with st.container():
        st.subheader("🔍 Filter Employees")

        # Dropdown values
        departments = ["Select"] + sorted(df["DEPARTMENT"].dropna().unique().tolist())
        colf1, colf2, colf3 = st.columns(3)
        
        with colf1:
            selected_department = st.selectbox("🏢 Select Department", departments)

        # Filter designations based on selected department
        if selected_department != "Select":
            filtered_df = df[df["DEPARTMENT"] == selected_department]
        else:
            filtered_df = df

        designations = ["Select"] + sorted(filtered_df["DESIGNATION"].dropna().unique().tolist())
        with colf2:
            selected_designation = st.selectbox("🛠 Select Designation", designations)

        # Filter employees based on selected department and designation
        if selected_designation != "Select":
            filtered_df = filtered_df[filtered_df["DESIGNATION"] == selected_designation]
        
        employee_names = ["Select"] + sorted(filtered_df["EMP_NAME"].dropna().unique().tolist())
        with colf3:
            selected_employee = st.selectbox("👤 Select Employee", employee_names)

        # Build WHERE clause dynamically
        query_filters = []
        if selected_department != "Select":
            query_filters.append(f"department = '{selected_department}'")
        if selected_designation != "Select":
            query_filters.append(f"designation = '{selected_designation}'")
        if selected_employee != "Select":
            query_filters.append(f"emp_name = '{selected_employee}'")

        where_clause = " AND ".join(query_filters)

        # Build final query
        query = f"""
            SELECT emp_id, emp_name, department, general_manager, designation, gender, EMPLOYMENT_TYPE
            FROM EMPLOYEE_360.EMPLOYEE_DEMO.EMPLOEE_DETAILS
            WHERE general_manager = '{selected_manager}'
        """
        if where_clause:
            query += f" AND {where_clause}"

        filtered_df = session.sql(query).to_pandas()
        st.subheader("📄 Filtered Employee Data")
        st.dataframe(filtered_df, use_container_width=True)

    # --- Chart Section (Moved to Bottom) ---
    chart_type = st.selectbox("📊 Select Chart Type", 
                              ["Employment Confirmation", "Designation Distribution", "Gender Distribution"])
    
    if chart_type == "Employment Confirmation":
        emp_type_count = df.groupby(["EMPLOYMENT_TYPE", "DESIGNATION"]).size().reset_index(name="count")
        fig = px.bar(emp_type_count, x="DESIGNATION", y="count", color="EMPLOYMENT_TYPE", 
                     title="Employment Confirmation", barmode="stack")
    
    elif chart_type == "Designation Distribution":
        df_total = df.groupby("DESIGNATION").size().reset_index(name="EMP_COUNT")
        fig = px.line(df_total, x="DESIGNATION", y="EMP_COUNT", 
                      title="Designation Distribution", markers=True)
        fig.update_traces(line=dict(color="blue", width=2))

    elif chart_type == "Gender Distribution":
        fig = px.pie(df, names="GENDER", title="Gender Distribution in Team")
    
    st.plotly_chart(fig, use_container_width=True)

# Unauthorized access
elif current_manager_name and selected_manager.lower() != current_manager_name.lower():
    st.warning("🚫 You are not authorized to view this data.")

# Non-manager users
else:
    st.info("ℹ️ You are not a manager. Select your name to view employee details once authorized.")

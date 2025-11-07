import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os
import io
import base64
from datetime import datetime

# Import our custom modules
from src.cgpa_calculator import CGPACalculator, MLAnalyzer, VisualizationGenerator
from src.email_service import EmailService

# Configure page
st.set_page_config(
    page_title="CGPA & CO/PO Analysis System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .warning-message {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'calculator' not in st.session_state:
        st.session_state.calculator = CGPACalculator()
    if 'ml_analyzer' not in st.session_state:
        st.session_state.ml_analyzer = MLAnalyzer()
    if 'visualizer' not in st.session_state:
        st.session_state.visualizer = VisualizationGenerator()
    if 'email_service' not in st.session_state:
        st.session_state.email_service = EmailService(
            "fahmidafaiza918@gmail.com", 
            "faflqldwdmgyrxum"
        )
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    if 'co_po_mapping' not in st.session_state:
        st.session_state.co_po_mapping = None
    
    # Clear authentication states for fresh start
    if 'teacher_authenticated' not in st.session_state:
        st.session_state.teacher_authenticated = False
    if 'student_authenticated' not in st.session_state:
        st.session_state.student_authenticated = False
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 CGPA & CO/PO Analysis System</h1>
        <p>Comprehensive Academic Performance Analysis with Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("📊 Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        [
            "🏠 Dashboard",
            "📁 Upload Data",
            "📈 Analysis Results",
            "📧 Email Reports",
            "📋 Download Template",
            "👨‍🏫 Teacher Portal",
            "👨‍🎓 Student Portal"
        ]
    )
    
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📁 Upload Data":
        show_upload_page()
    elif page == "📈 Analysis Results":
        show_analysis_page()
    elif page == "📧 Email Reports":
        show_email_page()
    elif page == "📋 Download Template":
        show_template_page()
    elif page == "👨‍🏫 Teacher Portal":
        show_teacher_portal()
    elif page == "👨‍🎓 Student Portal":
        show_student_portal()

def show_dashboard():
    st.header("📊 System Dashboard")
    
    if st.session_state.processed_data is not None:
        df = st.session_state.processed_data
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Students", len(df))
        
        with col2:
            avg_cgpa = df['grade_points'].mean()
            st.metric("📊 Average CGPA", f"{avg_cgpa:.2f}")
        
        with col3:
            pass_rate = len(df[df['grade_points'] >= 2.0]) / len(df) * 100
            st.metric("✅ Pass Rate", f"{pass_rate:.1f}%")
        
        with col4:
            excellent_rate = len(df[df['grade_points'] >= 3.3]) / len(df) * 100
            st.metric("🌟 Excellence Rate", f"{excellent_rate:.1f}%")
        
        # Performance distribution
        st.subheader("📈 Performance Distribution")
        
        fig_dist = st.session_state.visualizer.create_performance_distribution(df)
        st.plotly_chart(fig_dist, use_container_width=True)
        
        # Grade distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎯 Grade Distribution")
            grade_counts = df['grade'].value_counts()
            fig_grade = px.pie(
                values=grade_counts.values,
                names=grade_counts.index,
                title="Grade Distribution"
            )
            st.plotly_chart(fig_grade, use_container_width=True)
        
        with col2:
            st.subheader("📊 Course Statistics")
            if 'course_code' in df.columns:
                course_stats = df.groupby('course_code').agg({
                    'grade_points': ['mean', 'count'],
                    'total_marks': 'mean'
                }).round(2)
                st.dataframe(course_stats)
        
        # Top performers
        st.subheader("🏆 Top Performers")
        top_students = df.nlargest(5, 'grade_points')[['student_name', 'student_id', 'grade_points', 'grade', 'total_marks']]
        st.dataframe(top_students, use_container_width=True)
        
    else:
        st.info("👈 Please upload student data first to see the dashboard analysis.")
        
        # Show system features
        st.subheader("🌟 System Features")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>📊 CGPA Calculation</h4>
                <p>Accurate CGPA calculation on 4.0 scale with comprehensive grading system</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>🎯 CO/PO Analysis</h4>
                <p>Detailed Course Outcomes and Program Outcomes attainment analysis</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4>🤖 ML Insights</h4>
                <p>Machine learning-powered performance prediction and clustering</p>
            </div>
            """, unsafe_allow_html=True)

def check_teacher_authentication():
    """Check if teacher is authenticated"""
    if 'teacher_authenticated' not in st.session_state:
        st.session_state.teacher_authenticated = False
    
    if not st.session_state.teacher_authenticated:
        st.subheader("🔐 Teacher Authentication Required")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            teacher_id = st.text_input("👤 Teacher ID:", placeholder="Enter your teacher ID", key="teacher_id_input")
            password = st.text_input("🔒 Password:", type="password", placeholder="Enter your password", key="teacher_password_input")
        
        with col2:
            st.write("")  # Spacer
            st.write("")  # Spacer
            if st.button("🔑 Login", type="primary", key="teacher_login_btn"):
                if teacher_id and password:
                    # Simple authentication (in production, use proper authentication)
                    if teacher_id.lower() in ['admin', 'teacher', 'demo'] and password.lower() in ['admin', 'teacher', 'demo', '123']:
                        st.session_state.teacher_authenticated = True
                        st.session_state.current_teacher = teacher_id
                        st.success("✅ Authentication successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please try again.")
                else:
                    st.error("❌ Please enter both teacher ID and password.")
        
        st.info("📋 Demo Credentials: Teacher ID: `demo`, Password: `demo`")
        return False
    
    return True

def check_student_authentication():
    """Check if student is authenticated"""
    if 'student_authenticated' not in st.session_state:
        st.session_state.student_authenticated = False
    
    if not st.session_state.student_authenticated:
        st.subheader("🔐 Student Authentication Required")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            student_id = st.text_input("🆔 Student ID:", placeholder="Enter your student ID", key="student_id_input")
            email = st.text_input("📧 Email:", placeholder="Enter your email", key="student_email_input")
        
        with col2:
            st.write("")  # Spacer
            st.write("")  # Spacer
            if st.button("🔑 Login", type="primary", key="student_login_btn"):
                if student_id and email and st.session_state.processed_data is not None:
                    df = st.session_state.processed_data
                    student = df[(df['student_id'] == student_id) & (df['email'] == email)]
                    
                    if not student.empty:
                        st.session_state.student_authenticated = True
                        st.session_state.current_student = student.iloc[0]
                        st.success(f"✅ Welcome, {student.iloc[0]['student_name']}!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid Student ID or Email. Please check your credentials.")
                elif not (student_id and email):
                    st.error("❌ Please enter both Student ID and Email.")
                else:
                    st.error("❌ Student data not available. Please contact your teacher.")
        
        st.info("📋 Use your Student ID and registered email to login.")
        return False
    
    return True

def show_upload_page():
    st.header("📁 Upload Student Data")
    
    # Check teacher authentication
    if not check_teacher_authentication():
        return
    
    # Teacher logout button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.teacher_authenticated = False
            st.session_state.current_teacher = None
            st.rerun()
    
    st.markdown(f"""
    <div class="success-message">
        <strong>👨‍🏫 Welcome Teacher: {st.session_state.current_teacher}</strong><br>
        You can upload student data files and manage academic records.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-message">
        <strong>📋 Instructions:</strong><br>
        • Upload Excel file with student data in the specified format<br>
        • File should contain sheets: Student_Data, CO_PO_Mapping, PO_Definitions<br>
        • Download the template below for proper format
    </div>
    """, unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose Excel file",
        type=['xlsx', 'xls'],
        help="Upload student data Excel file"
    )
    
    if uploaded_file is not None:
        try:
            # Read Excel file
            excel_file = pd.ExcelFile(uploaded_file)
            
            # Check required sheets
            required_sheets = ['Student_Data', 'CO_PO_Mapping', 'PO_Definitions']
            missing_sheets = [sheet for sheet in required_sheets if sheet not in excel_file.sheet_names]
            
            if missing_sheets:
                st.error(f"Missing required sheets: {', '.join(missing_sheets)}")
                return
            
            # Read all sheets
            student_df = pd.read_excel(uploaded_file, sheet_name='Student_Data')
            co_po_df = pd.read_excel(uploaded_file, sheet_name='CO_PO_Mapping')
            po_df = pd.read_excel(uploaded_file, sheet_name='PO_Definitions')
            
            # Store in session state
            st.session_state.co_po_mapping = co_po_df
            
            # Process student data
            with st.spinner("🔄 Processing student data..."):
                # Calculate CGPA
                processed_df = st.session_state.calculator.process_student_data(student_df)
                
                # Get CO list
                co_list = co_po_df['Course_Outcome'].tolist()
                
                # Calculate CO achievements
                processed_df = st.session_state.calculator.calculate_all_co_achievements(processed_df, co_list)
                
                # Calculate PO attainments
                processed_df = st.session_state.calculator.calculate_po_attainment(processed_df, co_po_df, co_list)
                
                # ML Analysis
                po_list = [f'PO{i}' for i in range(1, 13)]
                processed_df, cluster_analysis = st.session_state.ml_analyzer.student_clustering(
                    processed_df, co_list, po_list
                )
                
                # Store processed data
                st.session_state.processed_data = processed_df
                st.session_state.cluster_analysis = cluster_analysis
            
            st.success("✅ Data processed successfully!")
            
            # Show sample of processed data
            st.subheader("📊 Processed Data Sample")
            st.dataframe(processed_df.head(), use_container_width=True)
            
            # Show data summary
            st.subheader("📈 Processing Summary")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("👥 Students Processed", len(processed_df))
            
            with col2:
                st.metric("🎯 COs Analyzed", len(co_list))
            
            with col3:
                st.metric("🎓 POs Analyzed", len(po_list))
            
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.write("Please check the file format and try again.")

def show_analysis_page():
    st.header("📈 Analysis Results")
    
    # Check if data is available
    if st.session_state.processed_data is None:
        st.warning("⚠️ Please upload and process student data first.")
        return
    
    # Determine user type and authenticate accordingly
    user_type = st.radio("👤 Select User Type:", ["👨‍🏫 Teacher", "👨‍🎓 Student"], horizontal=True)
    
    if user_type == "👨‍🏫 Teacher":
        if not check_teacher_authentication():
            return
        show_teacher_analysis()
    else:
        if not check_student_authentication():
            return
        show_student_analysis()

def show_teacher_analysis():
    """Show analysis for authenticated teachers"""
    df = st.session_state.processed_data
    co_po_mapping = st.session_state.co_po_mapping
    
    # Teacher logout button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.teacher_authenticated = False
            st.session_state.current_teacher = None
            st.rerun()
    
    st.markdown(f"""
    <div class="success-message">
        <strong>👨‍🏫 Teacher Analytics Dashboard: {st.session_state.current_teacher}</strong><br>
        Comprehensive view of all student performance and analytics.
    </div>
    """, unsafe_allow_html=True)
    
    # Get CO and PO lists
    co_list = co_po_mapping['Course_Outcome'].tolist() if co_po_mapping is not None else []
    po_list = [f'PO{i}' for i in range(1, 13)]
    
    # Student Search functionality
    st.subheader("🔍 Student Search & Detailed Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        student_search = st.text_input("🔍 Search Student by ID or Name:", placeholder="Enter student ID or name")
    
    with col2:
        st.write("")  # Spacer
        st.write("")  # Spacer
        show_ml_insights = st.checkbox("🤖 Show ML Career Insights", value=True)
    
    if student_search:
        # Search for student
        filtered_df = df[
            df['student_name'].str.contains(student_search, case=False, na=False) |
            df['student_id'].str.contains(student_search, case=False, na=False)
        ]
        
        if not filtered_df.empty:
            student = filtered_df.iloc[0]
            
            # Detailed Student Analysis Card
            st.subheader(f"👤 Detailed Analysis: {student['student_name']} ({student['student_id']})")
            
            # Basic Info & Performance
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📊 Total Marks", f"{student['total_marks']:.2f}%")
            
            with col2:
                st.metric("🎯 Grade", student['grade'])
            
            with col3:
                st.metric("📈 CGPA", f"{student['grade_points']:.2f}")
            
            with col4:
                if 'performance_cluster' in df.columns:
                    cluster_names = ["🌟 High Performer", "📊 Average Performer", "📈 Needs Improvement"]
                    cluster_id = int(student['performance_cluster']) if student['performance_cluster'] is not None else 1
                    st.metric("👥 Performance Group", cluster_names[cluster_id])
            
            # Assessment Breakdown
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📝 Assessment Breakdown")
                assessment_data = {
                    'Component': ['Mid Term', 'Final Exam', 'Class Test', 'Assignment', 'Attendance'],
                    'Marks': [student['mid_marks'], student['final_marks'], student['ct_marks'], 
                             student['assignment_marks'], student['attendance_marks']],
                    'Max Marks': [30, 40, 15, 10, 5]
                }
                assessment_df = pd.DataFrame(assessment_data)
                assessment_df['Percentage'] = (assessment_df['Marks'] / assessment_df['Max Marks'] * 100).round(1)
                st.dataframe(assessment_df, use_container_width=True)
            
            with col2:
                # CO Achievements
                co_achievements = []
                for key, value in student.items():
                    if key.endswith('_achievement'):
                        co_name = key.replace('_achievement', '')
                        co_achievements.append({'CO': co_name, 'Achievement (%)': f"{value:.1f}%"})
                
                if co_achievements:
                    st.subheader("🎯 CO Achievements")
                    co_df = pd.DataFrame(co_achievements)
                    st.dataframe(co_df, use_container_width=True)
            
            # ML Career Insights
            if show_ml_insights:
                st.subheader("🤖 ML Career Insights & Recommendations")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Performance Analysis
                    st.write("**📊 Performance Analysis:**")
                    if student['grade_points'] >= 3.7:
                        st.write("🌟 **Outstanding Performance** - Top 10% of class")
                        st.write("💡 Recommended: Research, Higher Studies, Competitive Programming")
                    elif student['grade_points'] >= 3.0:
                        st.write("👍 **Strong Performance** - Above Average")
                        st.write("💡 Recommended: Software Development, Technical Roles, Internships")
                    elif student['grade_points'] >= 2.0:
                        st.write("📊 **Average Performance** - Room for Improvement")
                        st.write("💡 Recommended: Skill Development, Practice, Additional Courses")
                    else:
                        st.write("📈 **Needs Improvement** - Focus on Fundamentals")
                        st.write("💡 Recommended: Tutoring, Study Groups, Foundation Building")
                
                with col2:
                    # Career Path Suggestions
                    st.write("**🎯 Career Path Suggestions:**")
                    
                    # Based on CO achievements
                    high_cos = []
                    for key, value in student.items():
                        if key.endswith('_achievement') and value > 80:
                            co_name = key.replace('_achievement', '')
                            high_cos.append(co_name)
                    
                    if 'CO1' in high_cos and 'CO2' in high_cos:
                        st.write("💻 **Software Development** - Strong programming & algorithm skills")
                    if 'CO3' in high_cos and 'CO4' in high_cos:
                        st.write("🔧 **System Architecture** - Good analytical & design skills")
                    if student['grade_points'] >= 3.5:
                        st.write("🎓 **Research/Academia** - Excellent academic performance")
                        st.write("🏢 **Leadership Roles** - Management potential")
                    
                    # Skill development recommendations
                    st.write("**📚 Skill Development:**")
                    if student['mid_marks'] < 25:
                        st.write("📖 Focus on conceptual understanding")
                    if student['final_marks'] < 35:
                        st.write("📝 Improve exam preparation strategies")
                    if student['ct_marks'] < 12:
                        st.write("⚡ Regular practice and quizzes")
                    if student['assignment_marks'] < 8:
                        st.write("🛠️ Practical application and projects")
            
            # Email Actions
            st.subheader("📧 Email Communication")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📧 Send Report to Student", type="primary"):
                    success, message = st.session_state.email_service.send_student_report(
                        student.to_dict(), is_parent=False
                    )
                    if success:
                        st.success("✅ Report sent to student successfully!")
                    else:
                        st.error(f"❌ Failed: {message}")
            
            with col2:
                if pd.notna(student.get('parent_email')):
                    if st.button("👨‍👩‍👧 Send Report to Parent", type="secondary"):
                        success, message = st.session_state.email_service.send_student_report(
                            student.to_dict(), is_parent=True
                        )
                        if success:
                            st.success("✅ Report sent to parent successfully!")
                        else:
                            st.error(f"❌ Failed: {message}")
                else:
                    st.write("📧 Parent email not available")
            
            with col3:
                if st.button("📋 View Email Preview"):
                    email_html = st.session_state.email_service.create_html_report(student.to_dict())
                    st.components.v1.html(email_html, height=600, scrolling=True)
            
            # PO Attainment Analysis
            po_attainments = []
            for key, value in student.items():
                if key.endswith('_attainment'):
                    po_name = key.replace('_attainment', '')
                    po_attainments.append({'PO': po_name, 'Attainment (%)': f"{value:.1f}%"})
            
            if po_attainments:
                st.subheader("🎓 PO Attainment Analysis")
                po_df = pd.DataFrame(po_attainments)
                st.dataframe(po_df, use_container_width=True)
        
        else:
            st.error("❌ Student not found. Please check the ID or name.")
    
    # Overall Class Analytics
    st.subheader("📊 Class Analytics Overview")
    
    tab1, tab2, tab3 = st.tabs(["📈 Performance Summary", "🤖 ML Insights", "📊 CO/PO Analysis"])
    
    with tab1:
        # Performance Summary
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Students", len(df))
        
        with col2:
            avg_cgpa = df['grade_points'].mean()
            st.metric("📊 Average CGPA", f"{avg_cgpa:.2f}")
        
        with col3:
            pass_rate = len(df[df['grade_points'] >= 2.0]) / len(df) * 100
            st.metric("✅ Pass Rate", f"{pass_rate:.1f}%")
        
        with col4:
            excellent_rate = len(df[df['grade_points'] >= 3.3]) / len(df) * 100
            st.metric("🌟 Excellence Rate", f"{excellent_rate:.1f}%")
    
    with tab2:
        # ML Insights
        if 'performance_cluster' in df.columns:
            cluster_analysis = st.session_state.cluster_analysis
            
            for cluster_id, analysis in cluster_analysis.items():
                cluster_name = f"Cluster {cluster_id + 1}"
                if analysis['avg_cgpa'] >= 3.5:
                    cluster_name += " (High Performers)"
                elif analysis['avg_cgpa'] >= 2.5:
                    cluster_name += " (Average Performers)"
                else:
                    cluster_name += " (Needs Improvement)"
                
                with st.expander(cluster_name):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("📊 Students", analysis['size'])
                        st.metric("🎯 Avg CGPA", f"{analysis['avg_cgpa']:.2f}")
                    
                    with col2:
                        st.write("**Key Characteristics:**")
                        for feature, value in analysis['characteristics'].items():
                            if 'achievement' in feature or 'attainment' in feature:
                                st.write(f"• {feature.replace('_', ' ').title()}: {value:.1f}%")
    
    with tab3:
        # CO/PO Charts
        if co_list:
            fig_co, fig_po = st.session_state.visualizer.create_co_po_charts(df, co_list, po_list)
            
            st.plotly_chart(fig_co, use_container_width=True)
            st.plotly_chart(fig_po, use_container_width=True)

def show_student_analysis():
    """Show analysis for authenticated students"""
    student = st.session_state.current_student
    
    # Student logout button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.student_authenticated = False
            st.session_state.current_student = None
            st.rerun()
    
    st.markdown(f"""
    <div class="success-message">
        <strong>👨‍🎓 Welcome Student: {student['student_name']}</strong><br>
        Here are your academic performance analytics and results.
    </div>
    """, unsafe_allow_html=True)
    
    # Performance Overview
    st.subheader("📊 Your Performance Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Marks", f"{student['total_marks']:.2f}%")
    
    with col2:
        st.metric("🎯 Grade", student['grade'])
    
    with col3:
        st.metric("📈 CGPA", f"{student['grade_points']:.2f}")
    
    with col4:
        if 'performance_cluster' in student.index:
            cluster_names = ["🌟 High Performer", "📊 Average Performer", "📈 Needs Improvement"]
            cluster_id = int(student['performance_cluster']) if student['performance_cluster'] is not None else 1
            st.metric("👥 Performance Group", cluster_names[cluster_id])
    
    # Detailed Breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📝 Assessment Breakdown")
        assessment_data = {
            'Component': ['Mid Term', 'Final Exam', 'Class Test', 'Assignment', 'Attendance'],
            'Marks Obtained': [student['mid_marks'], student['final_marks'], student['ct_marks'], 
                             student['assignment_marks'], student['attendance_marks']],
            'Maximum Marks': [30, 40, 15, 10, 5],
            'Percentage': [(student['mid_marks']/30*100), (student['final_marks']/40*100), 
                          (student['ct_marks']/15*100), (student['assignment_marks']/10*100), 
                          (student['attendance_marks']/5*100)]
        }
        assessment_df = pd.DataFrame(assessment_data)
        assessment_df['Percentage'] = assessment_df['Percentage'].round(1)
        st.dataframe(assessment_df, use_container_width=True)
    
    with col2:
        # CO Achievements
        co_achievements = []
        for key, value in student.items():
            if key.endswith('_achievement'):
                co_name = key.replace('_achievement', '')
                co_achievements.append({'CO': co_name, 'Achievement (%)': f"{value:.1f}%"})
        
        if co_achievements:
            st.subheader("🎯 Course Outcomes Achievement")
            co_df = pd.DataFrame(co_achievements)
            st.dataframe(co_df, use_container_width=True)
    
    # Personalized Recommendations
    st.subheader("💡 Personalized Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📚 Academic Suggestions:**")
        if student['grade_points'] >= 3.7:
            st.write("🌟 Excellent performance! Consider advanced courses and research opportunities.")
            st.write("🏆 You're eligible for academic scholarships and recognition.")
        elif student['grade_points'] >= 3.0:
            st.write("👍 Good performance! Focus on weaker areas to achieve excellence.")
            st.write("💡 Consider joining study groups and academic competitions.")
        elif student['grade_points'] >= 2.0:
            st.write("📊 Adequate performance. Identify and work on weak areas.")
            st.write("📚 Regular study habits and seeking help will improve grades.")
        else:
            st.write("📈 Performance needs improvement. Meet with academic advisor.")
            st.write("🎯 Develop structured study plan and seek tutoring if needed.")
    
    with col2:
        st.write("**🎯 Improvement Areas:**")
        if student['attendance_marks'] < 4:
            st.write("📅 Improve attendance - crucial for academic success")
        if student['assignment_marks'] < 8:
            st.write("📝 Focus on assignment quality and timely submission")
        if student['ct_marks'] < 12:
            st.write("⚡ Regular practice with quizzes and class tests")
        if student['mid_marks'] < 25:
            st.write("📖 Better preparation strategies for mid-term exams")
        if student['final_marks'] < 35:
            st.write("🎓 Comprehensive final exam preparation needed")
    
    # Request Detailed Report
    st.subheader("📧 Request Detailed Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📧 Send Detailed Report to My Email", type="primary"):
            success, message = st.session_state.email_service.send_student_report(
                student.to_dict(), is_parent=False
            )
            if success:
                st.success("✅ Detailed report sent to your email successfully!")
            else:
                st.error(f"❌ Failed to send report: {message}")
    
    with col2:
        if st.button("📋 Preview Report"):
            email_html = st.session_state.email_service.create_html_report(student.to_dict())
            st.components.v1.html(email_html, height=600, scrolling=True)
    
    # Career Path Suggestions
    st.subheader("🎯 Career Path Suggestions")
    
    # Based on performance and CO achievements
    if student['grade_points'] >= 3.5:
        st.write("🎓 **Academic Path:** Higher Studies, Research, Ph.D.")
        st.write("💼 **Industry Path:** Software Engineering, Data Science, AI/ML")
        st.write("🏆 **Leadership Roles:** Team Lead, Project Manager, Technical Architect")
    elif student['grade_points'] >= 2.5:
        st.write("💻 **Technical Roles:** Software Developer, System Analyst")
        st.write("🔧 **Skill Development:** Focus on practical skills and certifications")
        st.write("📈 **Growth Areas:** Internships, projects, skill enhancement")
    else:
        st.write("📚 **Foundation Building:** Focus on fundamentals and core concepts")
        st.write("🛠️ **Skill Development:** Practice programming, problem-solving")
        st.write("🎯 **Career Preparation:** Entry-level positions, skill certification")

def show_email_page():
    st.header("📧 Email Reports")
    
    # Check if data is available
    if st.session_state.processed_data is None:
        st.warning("⚠️ Please upload and process student data first.")
        return
    
    # Require teacher authentication for email functionality
    if not check_teacher_authentication():
        return
    
    df = st.session_state.processed_data
    
    # Teacher logout button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.teacher_authenticated = False
            st.session_state.current_teacher = None
            st.rerun()
    
    st.markdown(f"""
    <div class="success-message">
        <strong>👨‍🏫 Teacher Email Dashboard: {st.session_state.current_teacher}</strong><br>
        Send academic reports to students and parents, and view email communication history.
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📧 Send Academic Reports")
    
    col1, col2 = st.columns(2)
    
    with col1:
        send_to_students = st.checkbox("👨‍🎓 Send to Students", value=True)
        send_to_parents = st.checkbox("👨‍👩‍👧 Send to Parents", value=True)
    
    with col2:
        # Test email option
        test_email = st.text_input("📧 Test Email (Optional):", placeholder="Enter email to test")
    
    # Student selection
    st.subheader("👥 Select Students")
    
    search_student = st.text_input("🔍 Search Student:", placeholder="Search by name or ID")
    
    if search_student:
        filtered_df = df[
            df['student_name'].str.contains(search_student, case=False, na=False) |
            df['student_id'].str.contains(search_student, case=False, na=False)
        ]
    else:
        filtered_df = df
    
    select_all = st.checkbox("✅ Select All Students", value=True)
    
    if select_all:
        selected_students = filtered_df
    else:
        student_names = filtered_df['student_name'].tolist()
        selected_names = st.multiselect(
            "Choose students:",
            options=student_names,
            default=student_names[:5]  # Default to first 5
        )
        selected_students = filtered_df[filtered_df['student_name'].isin(selected_names)]
    
    # Show selected students summary
    if not selected_students.empty:
        st.info(f"📊 {len(selected_students)} students selected for email reports")
        
        # Show sample of selected students
        with st.expander("👀 View Selected Students"):
            st.dataframe(selected_students[['student_name', 'student_id', 'email', 'parent_email']].head(10), use_container_width=True)
    
    if st.button("📧 Send Emails", type="primary"):
        if selected_students.empty:
            st.error("❌ Please select at least one student.")
        elif test_email:
            # Send test email
            with st.spinner("🔄 Sending test email..."):
                if not selected_students.empty:
                    test_student = selected_students.iloc[0]
                    success, message = st.session_state.email_service.send_student_report(
                        test_student.to_dict(), 
                        is_parent=False
                    )
                    
                    if success:
                        st.success(f"✅ Test email sent to {test_email}")
                    else:
                        st.error(f"❌ Failed to send test email: {message}")
        else:
            # Send actual emails
            with st.spinner("🔄 Sending emails..."):
                results = st.session_state.email_service.send_bulk_reports(
                    selected_students,
                    send_to_parents=send_to_parents,
                    send_to_students=send_to_students
                )
                
                if results:
                    # Show results
                    st.subheader("📊 Email Sending Results")
                    
                    success_count = sum(1 for r in results if r['success'])
                    total_count = len(results)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("✅ Successful", success_count)
                    
                    with col2:
                        st.metric("❌ Failed", total_count - success_count)
                    
                    with col3:
                        success_rate = (success_count / total_count * 100) if total_count > 0 else 0
                        st.metric("📈 Success Rate", f"{success_rate:.1f}%")
                    
                    # Show detailed results
                    if st.checkbox("📋 Show Detailed Results"):
                        results_df = pd.DataFrame(results)
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Email statistics
                        st.subheader("📈 Email Statistics")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            student_emails = results_df[results_df['recipient_type'] == 'Student']
                            parent_emails = results_df[results_df['recipient_type'] == 'Parent']
                            
                            st.write("**Student Emails:**")
                            student_success = len(student_emails[student_emails['success'] == True])
                            student_total = len(student_emails)
                            st.write(f"• Sent: {student_success}/{student_total}")
                            
                            st.write("**Parent Emails:**")
                            parent_success = len(parent_emails[parent_emails['success'] == True])
                            parent_total = len(parent_emails)
                            st.write(f"• Sent: {parent_success}/{parent_total}")
                        
                        with col2:
                            # Failed emails analysis
                            failed_emails = results_df[results_df['success'] == False]
                            if not failed_emails.empty:
                                st.write("**Failed Email Details:**")
                                for idx, row in failed_emails.iterrows():
                                    st.error(f"❌ {row['email']}: {row['message']}")
                            else:
                                st.success("🎉 All emails sent successfully!")
    
    # Email Templates Preview
    st.subheader("📋 Email Template Preview")
    
    if not selected_students.empty:
        sample_student = selected_students.iloc[0]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("👀 Preview Student Report"):
                email_html = st.session_state.email_service.create_html_report(sample_student.to_dict())
                st.components.v1.html(email_html, height=600, scrolling=True)
        
        with col2:
            if st.button("👀 Preview Parent Report"):
                parent_email_html = st.session_state.email_service.create_html_report(sample_student.to_dict())
                st.components.v1.html(parent_email_html, height=600, scrolling=True)
        
        with col3:
            st.write("**Report Contents:**")
            st.write("📊 Academic Performance Summary")
            st.write("📝 Assessment Breakdown")
            st.write("🎯 CO/PO Achievements")
            st.write("💡 Personalized Recommendations")
            st.write("🎯 Career Path Suggestions")
    
    # Email History (simplified - in production, this would come from database)
    st.subheader("📜 Recent Email Activity")
    
    # Show email statistics summary
    total_students = len(df)
    students_with_email = len(df[df['email'].notna()])
    parents_with_email = len(df[df['parent_email'].notna()])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("👥 Total Students", total_students)
    
    with col2:
        st.metric("📧 Student Emails Available", students_with_email)
    
    with col3:
        st.metric("👨‍👩‍👧 Parent Emails Available", parents_with_email)
    
    st.info("📋 Note: In a production environment, this section would show detailed email history, delivery status, and communication logs.")

def show_template_page():
    st.header("📋 Download Excel Template")
    
    st.markdown("""
    <div class="warning-message">
        <strong>📝 Template Instructions:</strong><br>
        • Download the Excel template for proper data format<br>
        • Fill in all required fields accurately<br>
        • Ensure email addresses are correct for report delivery<br>
        • Map COs properly for each assessment component
    </div>
    """, unsafe_allow_html=True)
    
    # Create and provide template
    if st.button("📥 Generate and Download Template"):
        try:
            from src.create_excel_template import create_student_template
            
            with st.spinner("🔄 Creating template..."):
                template_path = create_student_template()
                
                # Read template file
                with open(template_path, "rb") as template_file:
                    template_bytes = template_file.read()
                
                # Provide download button
                st.download_button(
                    label="📥 Download Student Data Template",
                    data=template_bytes,
                    file_name="student_data_template.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                
                st.success("✅ Template created successfully!")
                
                # Show template structure
                st.subheader("📊 Template Structure")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("""
                    <div class="metric-card">
                        <h4>📋 Student_Data Sheet</h4>
                        <p>• Student Information<br>
                           • Assessment Marks<br>
                           • CO Mappings</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="metric-card">
                        <h4>🎯 CO_PO_Mapping Sheet</h4>
                        <p>• CO Definitions<br>
                           • PO Mappings<br>
                           • Weightage Matrix</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown("""
                    <div class="metric-card">
                        <h4>🎓 PO_Definitions Sheet</h4>
                        <p>• PO Descriptions<br>
                           • Learning Outcomes<br>
                           • Assessment Criteria</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Show sample data format
                st.subheader("📝 Sample Data Format")
                
                sample_data = {
                    'student_id': ['STU001'],
                    'student_name': ['John Doe'],
                    'email': ['john@email.com'],
                    'parent_email': ['parent@email.com'],
                    'course_code': ['CSE101'],
                    'course_name': ['Introduction to Programming'],
                    'semester': ['Fall 2024'],
                    'credits': [3],
                    'mid_marks': [25],
                    'mid_co_mapping': ['CO1,CO2'],
                    'final_marks': [35],
                    'final_co_mapping': ['CO1,CO2,CO3'],
                    'ct_marks': [12],
                    'ct_co_mapping': ['CO1'],
                    'assignment_marks': [8],
                    'assignment_co_mapping': ['CO2,CO3'],
                    'attendance_marks': [4]
                }
                
                sample_df = pd.DataFrame(sample_data)
                st.dataframe(sample_df, use_container_width=True)
                
        except Exception as e:
            st.error(f"❌ Error creating template: {str(e)}")
    
    # Assessment weightage information
    st.subheader("⚖️ Assessment Weightage")
    
    weightage_data = {
        'Component': ['Mid Term', 'Final Exam', 'Class Test', 'Assignment', 'Attendance'],
        'Maximum Marks': [30, 40, 15, 10, 5],
        'Weightage (%)': [30, 40, 15, 10, 5]
    }
    
    weightage_df = pd.DataFrame(weightage_data)
    st.dataframe(weightage_df, use_container_width=True)
    
    # CO and PO definitions
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Course Outcomes (COs)")
        st.markdown("""
        **CO1:** Apply fundamental programming concepts  
        **CO2:** Design and implement algorithms  
        **CO3:** Analyze and debug code  
        **CO4:** Develop software solutions
        """)
    
    with col2:
        st.subheader("🎓 Program Outcomes (POs)")
        st.markdown("""
        **PO1:** Engineering Knowledge  
        **PO2:** Problem Analysis  
        **PO3:** Design/Development of Solutions  
        **PO4:** Conduct Investigations  
        ... and more (PO1-PO12)
        """)

def show_teacher_portal():
    st.header("👨‍🏫 Teacher Portal")
    
    # Check teacher authentication
    if not check_teacher_authentication():
        return
    
    # Teacher logout button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.teacher_authenticated = False
            st.session_state.current_teacher = None
            st.rerun()
    
    st.markdown(f"""
    <div class="success-message">
        <strong>👨‍🏫 Welcome Teacher: {st.session_state.current_teacher}</strong><br>
        Teacher Dashboard - Manage student data, view analytics, and send reports.
    </div>
    """, unsafe_allow_html=True)
    
    # Show teacher-specific features
    st.subheader("📊 Teacher Dashboard")
    
    if st.session_state.processed_data is not None:
        df = st.session_state.processed_data
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Students", len(df))
        
        with col2:
            avg_cgpa = df['grade_points'].mean()
            st.metric("📊 Average CGPA", f"{avg_cgpa:.2f}")
        
        with col3:
            pass_rate = len(df[df['grade_points'] >= 2.0]) / len(df) * 100
            st.metric("✅ Pass Rate", f"{pass_rate:.1f}%")
        
        with col4:
            excellent_rate = len(df[df['grade_points'] >= 3.3]) / len(df) * 100
            st.metric("🌟 Excellence Rate", f"{excellent_rate:.1f}%")
        
        # Quick Actions
        st.subheader("⚡ Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📤 Upload New Data", type="primary"):
                st.session_state.current_page = "Upload Data"
                st.rerun()
        
        with col2:
            if st.button("📧 Send Reports", type="primary"):
                st.session_state.current_page = "Email Reports"
                st.rerun()
        
        with col3:
            if st.button("📈 View Analysis"):
                st.session_state.current_page = "Analysis Results"
                st.rerun()
        
        with col4:
            if st.button("📋 Download Template"):
                st.session_state.current_page = "Download Template"
                st.rerun()
        
        # Recent Activity
        st.subheader("📈 Class Performance Overview")
        
        # Performance Distribution Chart
        col1, col2 = st.columns(2)
        
        with col1:
            # Grade Distribution
            grade_counts = df['grade'].value_counts()
            fig_grade = px.pie(
                values=grade_counts.values,
                names=grade_counts.index,
                title="Grade Distribution"
            )
            st.plotly_chart(fig_grade, use_container_width=True)
        
        with col2:
            # Performance Groups
            if 'performance_cluster' in df.columns:
                cluster_counts = df['performance_cluster'].value_counts().sort_index()
                cluster_names = ["High Performers", "Average Performers", "Needs Improvement"]
                cluster_labels = [cluster_names[i] for i in cluster_counts.index]
                
                fig_cluster = px.bar(
                    x=cluster_labels,
                    y=cluster_counts.values,
                    title="Performance Groups",
                    labels={'x': 'Performance Group', 'y': 'Number of Students'}
                )
                st.plotly_chart(fig_cluster, use_container_width=True)
        
        # Quick Student Search
        st.subheader("🔍 Quick Student Lookup")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            search_student = st.text_input("🔍 Search Student by Name or ID:", placeholder="Enter name or ID")
        
        with col2:
            st.write("")  # Spacer
            st.write("")  # Spacer
            view_details = st.button("👀 View Details")
        
        if search_student or view_details:
            if search_student:
                filtered_df = df[
                    df['student_name'].str.contains(search_student, case=False, na=False) |
                    df['student_id'].str.contains(search_student, case=False, na=False)
                ]
            else:
                filtered_df = df.head(10)  # Show first 10 students
            
            if not filtered_df.empty:
                st.dataframe(filtered_df[['student_name', 'student_id', 'email', 'grade', 'grade_points', 'total_marks']], use_container_width=True)
                
                # Quick actions for selected student
                selected_student_name = st.selectbox(
                    "Select student for actions:",
                    options=filtered_df['student_name'].tolist()
                )
                
                if selected_student_name:
                    student_data = filtered_df[filtered_df['student_name'] == selected_student_name].iloc[0]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"📧 Send Report to {selected_student_name}", type="primary"):
                            success, message = st.session_state.email_service.send_student_report(
                                student_data.to_dict(),
                                is_parent=False
                            )
                            if success:
                                st.success("✅ Report sent successfully!")
                            else:
                                st.error(f"❌ Failed to send report: {message}")
                    
                    with col2:
                        if pd.notna(student_data.get('parent_email')):
                            if st.button(f"👨‍👩‍👧 Send to Parent"):
                                success, message = st.session_state.email_service.send_student_report(
                                    student_data.to_dict(),
                                    is_parent=True
                                )
                                if success:
                                    st.success("✅ Parent report sent successfully!")
                                else:
                                    st.error(f"❌ Failed to send parent report: {message}")
                    
                    with col3:
                        if st.button(f"📊 View Full Analysis"):
                            # Store selected student for analysis page
                            st.session_state.selected_student = student_data
                            st.session_state.current_page = "Analysis Results"
                            st.rerun()
        
        # Class Statistics
        st.subheader("📊 Class Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Component-wise performance
            components = ['mid_marks', 'final_marks', 'ct_marks', 'assignment_marks', 'attendance_marks']
            component_stats = []
            
            for comp in components:
                if comp in df.columns:
                    stats = {
                        'Component': comp.replace('_marks', '').title(),
                        'Average': df[comp].mean(),
                        'Max': df[comp].max(),
                        'Min': df[comp].min()
                    }
                    component_stats.append(stats)
            
            if component_stats:
                comp_df = pd.DataFrame(component_stats)
                st.dataframe(comp_df, use_container_width=True)
        
        with col2:
            # Top and Bottom Performers
            st.write("**🏆 Top Performers:**")
            top_students = df.nlargest(3, 'grade_points')[['student_name', 'grade_points', 'grade']]
            for idx, (_, student) in enumerate(top_students.iterrows(), 1):
                st.write(f"{idx}. {student['student_name']} - CGPA: {student['grade_points']:.2f} ({student['grade']})")
            
            st.write("**📈 Students Needing Attention:**")
            bottom_students = df.nsmallest(3, 'grade_points')[['student_name', 'grade_points', 'grade']]
            for idx, (_, student) in enumerate(bottom_students.iterrows(), 1):
                st.write(f"{idx}. {student['student_name']} - CGPA: {student['grade_points']:.2f} ({student['grade']})")
    
    else:
        st.info("👈 Please upload student data first to view the teacher dashboard.")
        
        # Show quick access to upload
        col1, col2, col3 = st.columns(3)
        
        with col2:
            if st.button("📤 Upload Student Data Now", type="primary"):
                st.session_state.current_page = "Upload Data"
                st.rerun()

def show_student_portal():
    st.header("👨‍🎓 Student Portal")
    
    # Check student authentication
    if not check_student_authentication():
        return
    
    student = st.session_state.current_student
    
    # Student logout button
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("🚪 Logout", type="secondary"):
            st.session_state.student_authenticated = False
            st.session_state.current_student = None
            st.rerun()
    
    st.markdown(f"""
    <div class="success-message">
        <strong>👨‍🎓 Welcome Student: {student['student_name']}</strong><br>
        Student Portal - View your academic results, performance analytics, and request reports.
    </div>
    """, unsafe_allow_html=True)
    
    # Show student's results
    st.subheader("📊 Your Academic Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Total Marks", f"{student['total_marks']:.2f}%")
    
    with col2:
        st.metric("🎯 Grade", student['grade'])
    
    with col3:
        st.metric("📈 CGPA", f"{student['grade_points']:.2f}")
    
    # Detailed breakdown
    st.subheader("📝 Assessment Breakdown")
    
    breakdown_data = {
        'Component': ['Mid Term', 'Final Exam', 'Class Test', 'Assignment', 'Attendance'],
        'Marks Obtained': [
            student['mid_marks'],
            student['final_marks'],
            student['ct_marks'],
            student['assignment_marks'],
            student['attendance_marks']
        ],
        'Maximum Marks': [30, 40, 15, 10, 5],
        'Percentage': [
            (student['mid_marks']/30*100),
            (student['final_marks']/40*100),
            (student['ct_marks']/15*100),
            (student['assignment_marks']/10*100),
            (student['attendance_marks']/5*100)
        ]
    }
    
    breakdown_df = pd.DataFrame(breakdown_data)
    breakdown_df['Percentage'] = breakdown_df['Percentage'].round(1)
    st.dataframe(breakdown_df, use_container_width=True)
    
    # CO achievements
    co_achievements = []
    for key, value in student.items():
        if key.endswith('_achievement'):
            co_name = key.replace('_achievement', '')
            co_achievements.append({
                'CO': co_name,
                'Achievement (%)': f"{value:.1f}%"
            })
    
    if co_achievements:
        st.subheader("🎯 Course Outcomes Achievement")
        co_df = pd.DataFrame(co_achievements)
        st.dataframe(co_df, use_container_width=True)
    
    # Performance Analysis
    st.subheader("📈 Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📊 Performance Level:**")
        if student['grade_points'] >= 3.7:
            st.success("🌟 Outstanding Performance - Top 10%")
        elif student['grade_points'] >= 3.0:
            st.info("👍 Good Performance - Above Average")
        elif student['grade_points'] >= 2.0:
            st.warning("📊 Average Performance - Room for Improvement")
        else:
            st.error("📈 Needs Improvement - Focus on Fundamentals")
        
        st.write("**🎯 Strengths:**")
        if student['final_marks'] >= 35:
            st.write("✅ Strong final exam performance")
        if student['assignment_marks'] >= 8:
            st.write("✅ Excellent assignment work")
        if student['attendance_marks'] >= 4:
            st.write("✅ Good attendance record")
    
    with col2:
        st.write("**📚 Areas for Improvement:**")
        if student['mid_marks'] < 25:
            st.write("⚠️ Mid-term exam preparation")
        if student['ct_marks'] < 12:
            st.write("⚠️ Regular practice and quizzes")
        if student['attendance_marks'] < 4:
            st.write("⚠️ Class attendance")
        
        st.write("**💡 Recommendations:**")
        if student['grade_points'] < 3.0:
            st.write("• Meet with teachers for guidance")
            st.write("• Join study groups")
            st.write("• Regular practice sessions")
        else:
            st.write("• Take on challenging projects")
            st.write("• Help peers in study groups")
            st.write("• Explore advanced topics")
    
    # Request detailed report
    st.subheader("📧 Request Detailed Report")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📧 Send Detailed Report to My Email", type="primary"):
            success, message = st.session_state.email_service.send_student_report(
                student.to_dict(),
                is_parent=False
            )
            if success:
                st.success("✅ Detailed report sent to your email!")
            else:
                st.error(f"❌ Failed to send report: {message}")
    
    with col2:
        if st.button("📋 Preview Report"):
            email_html = st.session_state.email_service.create_html_report(student.to_dict())
            st.components.v1.html(email_html, height=600, scrolling=True)
    
    with col3:
        if pd.notna(student.get('parent_email')):
            st.write("👨‍👩‍👧 Parent email available for reports")
        else:
            st.write("📧 Parent email not on record")
    
    # Additional Resources
    st.subheader("📚 Additional Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🎯 Study Resources:**")
        st.write("• Course materials and lecture notes")
        st.write("• Practice problems and solutions")
        st.write("• Previous exam papers")
        st.write("• Online learning platforms")
    
    with col2:
        st.write("**🤝 Support Services:**")
        st.write("• Academic counseling")
        st.write("• Peer tutoring programs")
        st.write("• Teacher consultation hours")
        st.write("• Study group coordination")
    
    st.info("💡 **Tip:** Regular check your performance and seek help early when needed. Your teachers are here to support your learning journey!")

if __name__ == "__main__":
    main()
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
from datetime import datetime
import os

class EmailService:
    def __init__(self, sender_email, app_password):
        self.sender_email = sender_email
        self.app_password = app_password
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def create_html_report(self, student_data, co_po_data=None):
        """Create HTML email report for student"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                    border-radius: 10px 10px 0 0;
                }}
                .content {{
                    background: #f9f9f9;
                    padding: 30px;
                    border: 1px solid #ddd;
                    border-radius: 0 0 10px 10px;
                }}
                .grade-info {{
                    background: white;
                    padding: 20px;
                    margin: 20px 0;
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }}
                .achievement-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                    margin: 20px 0;
                }}
                .achievement-item {{
                    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                    color: white;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                }}
                .suggestions {{
                    background: #e8f5e8;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 5px solid #4caf50;
                }}
                .grade-excellent {{ color: #4caf50; font-weight: bold; }}
                .grade-good {{ color: #2196f3; font-weight: bold; }}
                .grade-average {{ color: #ff9800; font-weight: bold; }}
                .grade-poor {{ color: #f44336; font-weight: bold; }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #667eea;
                    color: white;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Academic Performance Report</h1>
                <h2>{student_data['student_name']}</h2>
                <p>Student ID: {student_data['student_id']}</p>
                <p>Course: {student_data['course_code']} - {student_data['course_name']}</p>
                <p>Semester: {student_data['semester']}</p>
            </div>
            
            <div class="content">
                <div class="grade-info">
                    <h3>🎯 Overall Performance</h3>
                    <table>
                        <tr>
                            <th>Metric</th>
                            <th>Score</th>
                            <th>Grade</th>
                            <th>Status</th>
                        </tr>
                        <tr>
                            <td>Total Marks</td>
                            <td>{student_data['total_marks']:.2f}%</td>
                            <td>{student_data['grade']}</td>
                            <td class="{self._get_grade_class(student_data['grade'])}">{self._get_performance_status(student_data['grade'])}</td>
                        </tr>
                        <tr>
                            <td>CGPA (4.0 Scale)</td>
                            <td colspan="3">{student_data['grade_points']:.2f}</td>
                        </tr>
                    </table>
                </div>
                
                <div class="grade-info">
                    <h3>📝 Assessment Breakdown</h3>
                    <table>
                        <tr>
                            <th>Component</th>
                            <th>Marks Obtained</th>
                            <th>Weightage</th>
                            <th>COs Mapped</th>
                        </tr>
                        <tr>
                            <td>Mid Term</td>
                            <td>{student_data['mid_marks']}/30</td>
                            <td>30%</td>
                            <td>{student_data.get('mid_co_mapping', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Final Exam</td>
                            <td>{student_data['final_marks']}/40</td>
                            <td>40%</td>
                            <td>{student_data.get('final_co_mapping', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Class Test</td>
                            <td>{student_data['ct_marks']}/15</td>
                            <td>15%</td>
                            <td>{student_data.get('ct_co_mapping', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Assignment</td>
                            <td>{student_data['assignment_marks']}/10</td>
                            <td>10%</td>
                            <td>{student_data.get('assignment_co_mapping', 'N/A')}</td>
                        </tr>
                        <tr>
                            <td>Attendance</td>
                            <td>{student_data['attendance_marks']}/5</td>
                            <td>5%</td>
                            <td>N/A</td>
                        </tr>
                    </table>
                </div>
        """
        
        # Add CO achievements if available
        co_achievements = []
        for key, value in student_data.items():
            if key.endswith('_achievement'):
                co_name = key.replace('_achievement', '')
                co_achievements.append(f"<div class='achievement-item'><strong>{co_name}</strong><br>{value:.1f}%</div>")
        
        if co_achievements:
            html_content += f"""
                <div class="grade-info">
                    <h3>🎯 Course Outcomes (COs) Achievement</h3>
                    <div class="achievement-grid">
                        {''.join(co_achievements)}
                    </div>
                </div>
            """
        
        # Add PO attainments if available
        po_attainments = []
        for key, value in student_data.items():
            if key.endswith('_attainment'):
                po_name = key.replace('_attainment', '')
                po_attainments.append(f"<div class='achievement-item'><strong>{po_name}</strong><br>{value:.1f}%</div>")
        
        if po_attainments:
            html_content += f"""
                <div class="grade-info">
                    <h3>🎓 Program Outcomes (POs) Attainment</h3>
                    <div class="achievement-grid">
                        {''.join(po_attainments[:6])}  # Show first 6 POs
                    </div>
                </div>
            """
        
        # Add suggestions
        suggestions = self._generate_suggestions(student_data)
        html_content += f"""
                <div class="suggestions">
                    <h3>💡 Academic Recommendations & Future Path Suggestions</h3>
                    <ul>
                        {''.join([f'<li>{suggestion}</li>' for suggestion in suggestions])}
                    </ul>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 30px; color: #666; font-size: 12px;">
                <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>This is an automated report from the Academic Performance Analysis System</p>
            </div>
        </body>
        </html>
        """
        
        return html_content
    
    def _get_grade_class(self, grade):
        """Get CSS class based on grade"""
        if grade in ['A+', 'A', 'A-']:
            return 'grade-excellent'
        elif grade in ['B+', 'B', 'B-']:
            return 'grade-good'
        elif grade in ['C+', 'C', 'C-']:
            return 'grade-average'
        else:
            return 'grade-poor'
    
    def _get_performance_status(self, grade):
        """Get performance status based on grade"""
        if grade in ['A+', 'A', 'A-']:
            return 'Excellent Performance 🌟'
        elif grade in ['B+', 'B', 'B-']:
            return 'Good Performance 👍'
        elif grade in ['C+', 'C', 'C-']:
            return 'Average Performance 📈'
        else:
            return 'Needs Improvement 📊'
    
    def _generate_suggestions(self, student_data):
        """Generate personalized suggestions based on performance"""
        suggestions = []
        grade_points = student_data.get('grade_points', 0)
        total_marks = student_data.get('total_marks', 0)
        
        if grade_points >= 3.7:
            suggestions.append("Excellent performance! Consider pursuing advanced courses or research opportunities.")
            suggestions.append("Your strong foundation makes you a candidate for academic scholarships.")
            suggestions.append("Explore leadership roles in academic projects and competitions.")
        elif grade_points >= 3.0:
            suggestions.append("Good performance! Focus on areas with lower scores to reach excellence.")
            suggestions.append("Consider joining study groups for collaborative learning.")
            suggestions.append("Explore internship opportunities to apply your knowledge.")
        elif grade_points >= 2.0:
            suggestions.append("Adequate performance. Identify weak areas and seek additional help.")
            suggestions.append("Regular attendance and consistent study habits will improve your grades.")
            suggestions.append("Consider academic support services and tutoring.")
        else:
            suggestions.append("Performance needs improvement. Meet with your academic advisor.")
            suggestions.append("Develop a structured study plan with daily goals.")
            suggestions.append("Focus on fundamentals and seek help early in the semester.")
        
        # Component-specific suggestions
        if student_data.get('attendance_marks', 0) < 4:
            suggestions.append("Improve your attendance - it's crucial for academic success.")
        
        if student_data.get('assignment_marks', 0) < 8:
            suggestions.append("Focus on completing assignments with quality and on time.")
        
        if student_data.get('ct_marks', 0) < 12:
            suggestions.append("Practice regularly with class tests and quizzes.")
        
        if student_data.get('mid_marks', 0) < 25:
            suggestions.append("Prepare better for mid-term exams with systematic study.")
        
        if student_data.get('final_marks', 0) < 35:
            suggestions.append("Develop comprehensive final exam preparation strategies.")
        
        # Career suggestions based on performance
        if grade_points >= 3.3:
            suggestions.append("Consider graduate studies or research-oriented careers.")
            suggestions.append("Your performance opens doors to competitive job opportunities.")
        elif grade_points >= 2.7:
            suggestions.append("Focus on building practical skills through projects and internships.")
            suggestions.append("Consider professional certifications to enhance your profile.")
        else:
            suggestions.append("Focus on building fundamental skills before exploring specializations.")
            suggestions.append("Consider skill development workshops and online courses.")
        
        return suggestions
    
    def send_email(self, recipient_email, subject, html_content, attachment_path=None):
        """Send email with optional attachment"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Add attachment if provided
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {os.path.basename(attachment_path)}'
                )
                msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.app_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, recipient_email, text)
            server.quit()
            
            return True, "Email sent successfully"
            
        except Exception as e:
            return False, f"Failed to send email: {str(e)}"
    
    def send_student_report(self, student_data, is_parent=False):
        """Send report to student or parent"""
        recipient_email = student_data.get('parent_email' if is_parent else 'email')
        
        if not recipient_email:
            return False, "No email address provided"
        
        recipient_type = "Parent" if is_parent else "Student"
        subject = f"Academic Performance Report - {recipient_type} of {student_data['student_name']}"
        
        html_content = self.create_html_report(student_data)
        
        return self.send_email(recipient_email, subject, html_content)
    
    def send_bulk_reports(self, students_df, send_to_parents=True, send_to_students=True):
        """Send reports to multiple students/parents"""
        results = []
        
        for idx, student in students_df.iterrows():
            student_dict = student.to_dict()
            
            # Send to parent
            if send_to_parents and pd.notna(student.get('parent_email')):
                success, message = self.send_student_report(student_dict, is_parent=True)
                results.append({
                    'student_id': student.get('student_id'),
                    'recipient_type': 'Parent',
                    'email': student.get('parent_email'),
                    'success': success,
                    'message': message
                })
            
            # Send to student
            if send_to_students and pd.notna(student.get('email')):
                success, message = self.send_student_report(student_dict, is_parent=False)
                results.append({
                    'student_id': student.get('student_id'),
                    'recipient_type': 'Student',
                    'email': student.get('email'),
                    'success': success,
                    'message': message
                })
        
        return results

# Test function
def test_email_service():
    """Test the email service"""
    # Configuration
    sender_email = "fahmidafaiza918@gmail.com"
    app_password = "faflqldwdmgyrxum"  # User provided app password
    
    email_service = EmailService(sender_email, app_password)
    
    # Sample student data
    student_data = {
        'student_id': 'STU001',
        'student_name': 'John Doe',
        'email': 'student@example.com',
        'parent_email': 'parent@example.com',
        'course_code': 'CSE101',
        'course_name': 'Introduction to Programming',
        'semester': 'Fall 2024',
        'total_marks': 85.5,
        'grade': 'A',
        'grade_points': 3.7,
        'mid_marks': 25,
        'mid_co_mapping': 'CO1,CO2',
        'final_marks': 35,
        'final_co_mapping': 'CO1,CO2,CO3',
        'ct_marks': 12,
        'ct_co_mapping': 'CO1',
        'assignment_marks': 8,
        'assignment_co_mapping': 'CO2,CO3',
        'attendance_marks': 4,
        'CO1_achievement': 88.5,
        'CO2_achievement': 82.3,
        'CO3_achievement': 79.8,
        'PO1_attainment': 85.2,
        'PO2_attainment': 81.6,
        'PO3_attainment': 83.4
    }
    
    return email_service, student_data

if __name__ == "__main__":
    email_service, student_data = test_email_service()
    print("Email service initialized successfully")
    print("Sample HTML report generated")
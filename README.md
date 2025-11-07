# 🎓 CGPA & CO/PO Analysis System

A comprehensive academic performance analysis system that calculates CGPA, analyzes Course Outcomes (COs) and Program Outcomes (POs), and provides intelligent insights using machine learning.

## 🌟 Features

### 📊 Core Functionality
- **CGPA Calculation**: Accurate 4.0 scale CGPA calculation with detailed grade analysis
- **CO/PO Analysis**: Comprehensive Course Outcomes and Program Outcomes attainment analysis
- **Assessment Tracking**: Multi-component assessment tracking (Mid, Final, CT, Assignment, Attendance)
- **Email Reports**: Automated email reports to students and parents

### 🤖 Machine Learning Features
- **Student Clustering**: ML-powered performance clustering for identifying student groups
- **Performance Prediction**: Predictive analytics for student performance trends
- **Intelligent Insights**: Data-driven recommendations and suggestions

### 🎯 Visualization & Analytics
- **Interactive Charts**: Dynamic CO/PO achievement charts
- **Performance Dashboards**: Comprehensive analytics dashboard
- **Trend Analysis**: Performance trends and statistical analysis

### 📧 Communication System
- **Automated Reports**: HTML-formatted email reports with detailed analysis
- **Parent Communication**: Separate reports for parents with academic suggestions
- **Student Feedback**: Personalized feedback and improvement recommendations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd cgpa_system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open in browser**
Navigate to `http://localhost:8501`

## 📋 System Architecture

### Assessment Components
| Component | Maximum Marks | Weightage |
|-----------|---------------|-----------|
| Mid Term  | 30            | 30%       |
| Final Exam| 40            | 40%       |
| Class Test| 15            | 15%       |
| Assignment| 10            | 10%       |
| Attendance| 5             | 5%        |

### Grading Scale (4.0 System)
| Percentage | Grade | Grade Points |
|------------|-------|--------------|
| 90-100     | A+    | 4.0          |
| 85-89      | A     | 3.7          |
| 80-84      | A-    | 3.3          |
| 75-79      | B+    | 3.0          |
| 70-74      | B     | 2.7          |
| 65-69      | B-    | 2.3          |
| 60-64      | C+    | 2.0          |
| 55-59      | C     | 1.7          |
| 50-54      | C-    | 1.3          |
| 45-49      | D+    | 1.0          |
| 40-44      | D     | 0.7          |
| <40        | F     | 0.0          |

## 📁 Excel Template Structure

The system requires Excel files with three specific sheets:

### 1. Student_Data Sheet
Contains student information and assessment marks:
- student_id, student_name, email, parent_email
- course_code, course_name, semester, credits
- Assessment marks and CO mappings

### 2. CO_PO_Mapping Sheet
Defines course outcomes and their mapping to program outcomes:
- Course_Outcome, Description
- PO1 through PO12 mapping (0 or 1)

### 3. PO_Definitions Sheet
Contains program outcome definitions:
- Program_Outcome, Description

## 🎯 Course Outcomes (COs)

- **CO1**: Apply fundamental programming concepts
- **CO2**: Design and implement algorithms
- **CO3**: Analyze and debug code
- **CO4**: Develop software solutions

## 🎓 Program Outcomes (POs)

- **PO1**: Engineering Knowledge
- **PO2**: Problem Analysis
- **PO3**: Design/Development of Solutions
- **PO4**: Conduct Investigations
- **PO5**: Modern Tool Usage
- **PO6**: Engineer and Society
- **PO7**: Environment and Sustainability
- **PO8**: Ethics
- **PO9**: Individual and Team Work
- **PO10**: Communication
- **PO11**: Project Management
- **PO12**: Life-long Learning

## 📧 Email Configuration

The system uses Gmail for email delivery. Configure the following in `src/email_service.py`:

```python
sender_email = "your-email@gmail.com"
app_password = "your-app-password"  # Gmail App Password
```

### Setting up Gmail App Password
1. Enable 2-factor authentication on Gmail
2. Go to Google Account settings
3. Select "Security" → "App passwords"
4. Generate a new app password
5. Use this password in the configuration

## 🖥️ User Interface

### Teacher Portal Features
- 📤 Upload student data files
- 📊 View comprehensive analytics
- 📧 Send bulk email reports
- 👥 View individual student results
- 📈 Track CO/PO attainment

### Student Portal Features
- 🔐 Secure login with student credentials
- 📊 View personal academic results
- 📧 Request detailed reports via email
- 📈 Track personal performance trends

### Dashboard Analytics
- 📊 Performance distribution charts
- 🎯 CO/PO achievement visualizations
- 🤖 ML-powered insights
- 📈 Statistical analysis
- 👥 Student clustering analysis

## 🤖 Machine Learning Features

### Student Clustering
- Automatically groups students into performance clusters
- Identifies high performers, average performers, and students needing improvement
- Provides insights into cluster characteristics

### Performance Prediction
- Uses Random Forest regression for performance prediction
- Identifies key factors affecting student performance
- Provides data-driven recommendations

### Anomaly Detection
- Identifies unusual performance patterns
- Flags students requiring attention
- Suggests intervention strategies

## 📊 Visualization Features

### Interactive Charts
- CO achievement bar charts
- PO attainment analysis
- Performance distribution histograms
- Student cluster scatter plots
- Correlation matrices

### Statistical Analysis
- Descriptive statistics
- Grade distribution analysis
- Component-wise performance analysis
- Trend analysis over time

## 🔄 Workflow

1. **Data Upload**: Teachers upload Excel files with student data
2. **Processing**: System processes data and calculates CGPA, CO/PO achievements
3. **Analysis**: ML models analyze performance patterns
4. **Visualization**: Generate interactive charts and reports
5. **Communication**: Send automated email reports to students and parents

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Email**: SMTPLib
- **File Processing**: OpenPyXL

## 📦 Deployment

### Local Deployment
```bash
streamlit run app.py
```

### Cloud Deployment
The system can be deployed on:
- Streamlit Cloud
- Heroku
- AWS
- Google Cloud Platform
- Any platform supporting Python applications

### Environment Variables
Set the following environment variables for production:
- `EMAIL_SENDER`: Gmail address for sending reports
- `EMAIL_PASSWORD`: Gmail app password

## 🔒 Security Considerations

- Email passwords should be stored as environment variables
- Student data should be encrypted at rest
- Regular backups of student data
- Access control for teacher and student portals

## 📞 Support

For technical support or questions:
- Check the troubleshooting guide
- Review the Excel template format
- Verify email configuration
- Contact system administrator

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📈 Future Enhancements

- [ ] Mobile app version
- [ ] Advanced ML models
- [ ] Real-time notifications
- [ ] Integration with learning management systems
- [ ] Multi-language support
- [ ] Advanced reporting features
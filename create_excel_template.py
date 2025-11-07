import pandas as pd
import os

def create_student_template():
    """Create a comprehensive Excel template for student data input"""
    
    # Define the structure
    template_data = {
        'student_id': ['STU001', 'STU002', 'STU003'],
        'student_name': ['John Doe', 'Jane Smith', 'Mike Johnson'],
        'email': ['john@email.com', 'jane@email.com', 'mike@email.com'],
        'parent_email': ['parent1@email.com', 'parent2@email.com', 'parent3@email.com'],
        'course_code': ['CSE101', 'CSE101', 'CSE101'],
        'course_name': ['Introduction to Programming', 'Introduction to Programming', 'Introduction to Programming'],
        'semester': ['Fall 2024', 'Fall 2024', 'Fall 2024'],
        'credits': [3, 3, 3],
        
        # Assessment components with their weights
        'mid_marks': [25, 28, 22],  # 30% weight
        'mid_co_mapping': ['CO1,CO2', 'CO1,CO2', 'CO1,CO2'],  # COs for mid questions
        
        'final_marks': [35, 38, 30],  # 40% weight
        'final_co_mapping': ['CO1,CO2,CO3', 'CO1,CO2,CO3', 'CO1,CO2,CO3'],  # COs for final questions
        
        'ct_marks': [12, 14, 10],  # 15% weight
        'ct_co_mapping': ['CO1', 'CO1', 'CO1'],  # COs for CT questions
        
        'assignment_marks': [8, 9, 7],  # 10% weight
        'assignment_co_mapping': ['CO2,CO3', 'CO2,CO3', 'CO2,CO3'],  # COs for assignment questions
        
        'attendance_marks': [4, 5, 3],  # 5% weight
    }
    
    df = pd.DataFrame(template_data)
    
    # Create CO-PO Mapping Sheet
    co_po_mapping = {
        'Course_Outcome': ['CO1', 'CO2', 'CO3', 'CO4'],
        'Description': [
            'Apply fundamental programming concepts',
            'Design and implement algorithms',
            'Analyze and debug code',
            'Develop software solutions'
        ],
        'PO1': [1, 1, 0, 1],  # Engineering Knowledge
        'PO2': [0, 1, 1, 1],  # Problem Analysis
        'PO3': [1, 1, 1, 1],  # Design/Development of Solutions
        'PO4': [0, 0, 0, 1],  # Conduct Investigations
        'PO5': [0, 0, 0, 0],  # Modern Tool Usage
        'PO6': [0, 0, 0, 0],  # Engineer and Society
        'PO7': [0, 0, 0, 0],  # Environment and Sustainability
        'PO8': [0, 0, 0, 0],  # Ethics
        'PO9': [0, 0, 0, 0],  # Individual and Team Work
        'PO10': [0, 0, 0, 0],  # Communication
        'PO11': [0, 0, 0, 0],  # Project Management
        'PO12': [0, 0, 0, 0]   # Life-long Learning
    }
    
    co_po_df = pd.DataFrame(co_po_mapping)
    
    # Create PO Definitions Sheet
    po_definitions = {
        'Program_Outcome': [f'PO{i}' for i in range(1, 13)],
        'Description': [
            'Engineering Knowledge: Apply knowledge of mathematics, science, engineering fundamentals',
            'Problem Analysis: Identify, formulate, research literature, and analyze engineering problems',
            'Design/Development: Design solutions for complex engineering problems and design system components',
            'Conduct Investigations: Use research-based knowledge and research methods for complex problems',
            'Modern Tool Usage: Create, select, and apply appropriate techniques, resources, and modern engineering tools',
            'Engineer and Society: Apply reasoning informed by contextual knowledge to assess societal issues',
            'Environment and Sustainability: Understand the impact of engineering solutions in societal context',
            'Ethics: Apply ethical principles and commit to professional ethics and responsibilities',
            'Individual and Team Work: Function effectively as an individual, and as a member or leader in teams',
            'Communication: Communicate effectively on complex engineering activities with the engineering community',
            'Project Management: Demonstrate knowledge and understanding of engineering and management principles',
            'Life-long Learning: Recognize the need for and have the preparation and ability to engage in independent learning'
        ]
    }
    
    po_df = pd.DataFrame(po_definitions)
    
    # Create Excel file with multiple sheets
    output_path = '/workspace/cgpa_system/data/student_template.xlsx'
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Student_Data', index=False)
        co_po_df.to_excel(writer, sheet_name='CO_PO_Mapping', index=False)
        po_df.to_excel(writer, sheet_name='PO_Definitions', index=False)
    
    print(f"Template created successfully: {output_path}")
    return output_path

if __name__ == "__main__":
    create_student_template()
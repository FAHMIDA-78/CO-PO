import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

class CGPACalculator:
    def __init__(self):
        self.grading_scale = {
            'A+': 4.0, 'A': 3.7, 'A-': 3.3,
            'B+': 3.0, 'B': 2.7, 'B-': 2.3,
            'C+': 2.0, 'C': 1.7, 'C-': 1.3,
            'D+': 1.0, 'D': 0.7, 'F': 0.0
        }
        
        self.weights = {
            'mid': 0.30,
            'final': 0.40,
            'ct': 0.15,
            'assignment': 0.10,
            'attendance': 0.05
        }
        
    def marks_to_grade(self, percentage):
        """Convert percentage to grade and grade points"""
        if percentage >= 90:
            return 'A+', 4.0
        elif percentage >= 85:
            return 'A', 3.7
        elif percentage >= 80:
            return 'A-', 3.3
        elif percentage >= 75:
            return 'B+', 3.0
        elif percentage >= 70:
            return 'B', 2.7
        elif percentage >= 65:
            return 'B-', 2.3
        elif percentage >= 60:
            return 'C+', 2.0
        elif percentage >= 55:
            return 'C', 1.7
        elif percentage >= 50:
            return 'C-', 1.3
        elif percentage >= 45:
            return 'D+', 1.0
        elif percentage >= 40:
            return 'D', 0.7
        else:
            return 'F', 0.0
    
    def calculate_total_marks(self, row):
        """Calculate total marks for a student"""
        total = (row['mid_marks'] * self.weights['mid'] +
                row['final_marks'] * self.weights['final'] +
                row['ct_marks'] * self.weights['ct'] +
                row['assignment_marks'] * self.weights['assignment'] +
                row['attendance_marks'] * self.weights['attendance'])
        return total
    
    def calculate_cgpa_for_student(self, row):
        """Calculate CGPA for a single student"""
        total_marks = self.calculate_total_marks(row)
        grade, grade_points = self.marks_to_grade(total_marks)
        return total_marks, grade, grade_points
    
    def process_student_data(self, df):
        """Process student data and calculate CGPA"""
        df['total_marks'] = df.apply(self.calculate_total_marks, axis=1)
        df['grade'] = ''
        df['grade_points'] = 0.0
        
        for idx, row in df.iterrows():
            total_marks, grade, grade_points = self.calculate_cgpa_for_student(row)
            df.at[idx, 'grade'] = grade
            df.at[idx, 'grade_points'] = grade_points
        
        return df
    
    def parse_co_mapping(self, co_string):
        """Parse CO mapping string to list"""
        if pd.isna(co_string) or co_string == '':
            return []
        return [co.strip() for co in co_string.split(',')]
    
    def calculate_co_achievement(self, row, co_name):
        """Calculate achievement for a specific CO"""
        co_weightage = {
            'mid': {'weight': self.weights['mid'], 'max_marks': 30},
            'final': {'weight': self.weights['final'], 'max_marks': 40},
            'ct': {'weight': self.weights['ct'], 'max_marks': 15},
            'assignment': {'weight': self.weights['assignment'], 'max_marks': 10},
            'attendance': {'weight': self.weights['attendance'], 'max_marks': 5}
        }
        
        total_co_score = 0
        total_weighted_score = 0
        
        for component in ['mid', 'final', 'ct', 'assignment', 'attendance']:
            marks_col = f'{component}_marks'
            co_col = f'{component}_co_mapping'
            
            if not pd.isna(row[marks_col]) and not pd.isna(row[co_col]):
                cos = self.parse_co_mapping(row[co_col])
                if co_name in cos:
                    # Distribute marks equally among COs
                    co_share = row[marks_col] / len(cos) if len(cos) > 0 else row[marks_col]
                    weighted_score = (co_share / co_weightage[component]['max_marks']) * co_weightage[component]['weight'] * 100
                    total_co_score += weighted_score
                    total_weighted_score += co_weightage[component]['weight'] * 100
        
        return (total_co_score / total_weighted_score * 100) if total_weighted_score > 0 else 0
    
    def calculate_all_co_achievements(self, df, co_list):
        """Calculate achievements for all COs"""
        for co in co_list:
            df[f'{co}_achievement'] = df.apply(lambda row: self.calculate_co_achievement(row, co), axis=1)
        return df
    
    def calculate_po_attainment(self, df, co_po_mapping, co_list):
        """Calculate PO attainment based on CO achievements"""
        po_list = [f'PO{i}' for i in range(1, 13)]
        
        for po in po_list:
            df[f'{po}_attainment'] = 0.0
            
            for idx, row in df.iterrows():
                po_score = 0
                total_co_weight = 0
                
                for co in co_list:
                    co_weight = co_po_mapping.loc[co_po_mapping['Course_Outcome'] == co, po].iloc[0]
                    if co_weight > 0:
                        co_achievement = row.get(f'{co}_achievement', 0)
                        po_score += co_achievement * co_weight
                        total_co_weight += co_weight
                
                if total_co_weight > 0:
                    df.at[idx, f'{po}_attainment'] = po_score / total_co_weight
        
        return df

class MLAnalyzer:
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.kmeans = KMeans(n_clusters=3, random_state=42)
        self.rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    
    def student_clustering(self, df, co_list, po_list):
        """Perform student clustering based on CO and PO achievements"""
        features = []
        feature_names = []
        
        # Add CO achievements
        for co in co_list:
            if f'{co}_achievement' in df.columns:
                features.append(df[f'{co}_achievement'].values)
                feature_names.append(f'{co}_achievement')
        
        # Add PO attainments
        for po in po_list:
            if f'{po}_attainment' in df.columns:
                features.append(df[f'{po}_attainment'].values)
                feature_names.append(f'{po}_attainment')
        
        if len(features) == 0:
            return df, {}
        
        feature_matrix = np.column_stack(features)
        feature_matrix_scaled = self.scaler.fit_transform(feature_matrix)
        
        # Perform clustering
        clusters = self.kmeans.fit_predict(feature_matrix_scaled)
        df['performance_cluster'] = clusters
        
        # Analyze clusters
        cluster_analysis = {}
        for cluster_id in range(3):
            cluster_data = df[df['performance_cluster'] == cluster_id]
            cluster_analysis[cluster_id] = {
                'size': len(cluster_data),
                'avg_cgpa': cluster_data['grade_points'].mean(),
                'characteristics': self._analyze_cluster_characteristics(cluster_data, feature_names)
            }
        
        return df, cluster_analysis
    
    def _analyze_cluster_characteristics(self, cluster_data, feature_names):
        """Analyze characteristics of a cluster"""
        characteristics = {}
        for feature in feature_names:
            if feature in cluster_data.columns:
                characteristics[feature] = cluster_data[feature].mean()
        return characteristics
    
    def predict_performance(self, df_train, df_predict, co_list):
        """Predict student performance using ML"""
        features = []
        
        for co in co_list:
            if f'{co}_achievement' in df_train.columns:
                features.append(f'{co}_achievement')
        
        if len(features) < 2:
            return df_predict
        
        X_train = df_train[features].fillna(0)
        y_train = df_train['grade_points']
        
        X_predict = df_predict[features].fillna(0)
        
        self.rf_model.fit(X_train, y_train)
        predictions = self.rf_model.predict(X_predict)
        
        df_predict['predicted_grade_points'] = predictions
        return df_predict

class VisualizationGenerator:
    def __init__(self):
        self.color_palette = px.colors.qualitative.Set3
    
    def create_co_po_charts(self, df, co_list, po_list):
        """Create interactive CO and PO achievement charts"""
        # CO Achievement Chart
        co_data = []
        for co in co_list:
            if f'{co}_achievement' in df.columns:
                co_data.append({
                    'CO': co,
                    'Average Achievement': df[f'{co}_achievement'].mean(),
                    'Max Achievement': df[f'{co}_achievement'].max(),
                    'Min Achievement': df[f'{co}_achievement'].min()
                })
        
        co_df = pd.DataFrame(co_data)
        
        # Create CO chart
        fig_co = go.Figure()
        fig_co.add_trace(go.Bar(
            x=co_df['CO'],
            y=co_df['Average Achievement'],
            name='Average Achievement',
            marker_color='lightblue'
        ))
        
        fig_co.add_trace(go.Scatter(
            x=co_df['CO'],
            y=co_df['Max Achievement'],
            mode='markers',
            name='Max Achievement',
            marker=dict(color='red', size=10)
        ))
        
        fig_co.add_trace(go.Scatter(
            x=co_df['CO'],
            y=co_df['Min Achievement'],
            mode='markers',
            name='Min Achievement',
            marker=dict(color='orange', size=10)
        ))
        
        fig_co.update_layout(
            title='Course Outcomes (COs) Achievement Analysis',
            xaxis_title='Course Outcomes',
            yaxis_title='Achievement (%)',
            height=500
        )
        
        # PO Attainment Chart
        po_data = []
        for po in po_list:
            if f'{po}_attainment' in df.columns:
                po_data.append({
                    'PO': po,
                    'Average Attainment': df[f'{po}_attainment'].mean()
                })
        
        po_df = pd.DataFrame(po_data)
        
        # Create PO chart
        fig_po = go.Figure()
        fig_po.add_trace(go.Bar(
            x=po_df['PO'],
            y=po_df['Average Attainment'],
            name='Average PO Attainment',
            marker=dict(color='lightgreen', line=dict(color='darkgreen', width=2))
        ))
        
        fig_po.update_layout(
            title='Program Outcomes (POs) Attainment Analysis',
            xaxis_title='Program Outcomes',
            yaxis_title='Attainment (%)',
            height=500
        )
        
        return fig_co, fig_po
    
    def create_performance_distribution(self, df):
        """Create performance distribution chart"""
        fig = px.histogram(
            df, 
            x='grade_points', 
            nbins=20,
            title='Student CGPA Distribution',
            labels={'grade_points': 'CGPA', 'count': 'Number of Students'}
        )
        
        fig.add_vline(
            x=df['grade_points'].mean(), 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"Mean: {df['grade_points'].mean():.2f}"
        )
        
        return fig
    
    def create_cluster_visualization(self, df):
        """Create student cluster visualization"""
        if 'performance_cluster' not in df.columns:
            return None
        
        fig = px.scatter(
            df,
            x='grade_points',
            y='total_marks',
            color='performance_cluster',
            title='Student Performance Clusters',
            labels={
                'grade_points': 'CGPA',
                'total_marks': 'Total Marks',
                'performance_cluster': 'Performance Cluster'
            }
        )
        
        return fig
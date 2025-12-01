import streamlit as st
import pandas as pd
import random
from collections import defaultdict

# Classroom capacities (excluding C002, C003, C004)
CLASSROOMS = {
    'C101': 48, 'C102': 48, 'C104': 48, 'C202': 48, 'C203': 48, 'C204': 48, 'C205': 48,
    'C302': 48, 'C303': 48, 'C304': 48, 'C305': 48, 'C402': 48, 'C403': 48, 'C404': 48,
    'C405': 48, 'C406': 48, 'C407': 48, 'C408': 48,
    'LAB106': 40, 'LAB107': 40, 'LAB206': 40, 'LAB207': 40, 'LAB208': 40,
    'LAB307': 40, 'LAB308': 40
}

# Main Electives (available to all branches in a year)
MAIN_ELECTIVES = {
    1: ['PH151', 'DS151', 'New_FSC', 'CS151'],
    2: ['EC251', 'EC252', 'New_IESI', 'New_ESE', 'CS152', 'CS251', 'New_ESD1', 'New_IRFIC', 'EC253', 'New_2DCG'],
    3: ['CS463', 'CS308', 'DS301', 'CS366', 'DS359', 'EC355', 'EC364', 'CS352', 'EC365'],
    4: ['EC456', 'DS401', 'EC462', 'EC465', 'PH454', 'CS457', 'DS458', 'CS468', 'CS473', 'New_SDN', 'CS470', 'MA452', 'EC463']
}

# HSS Basket Electives (specific branches)
HSS_ELECTIVES = {
    1: ['HS157', 'New_KKN', 'New_LITSG', 'New_BOD', 'HS156'],
    2: [],
    3: [],
    4: ['DS102']
}

# Core courses - ONLY fullsem + halfsem-2
CORE_COURSES = {
    1: {
        'CSEA': [
            {'code': 'MA162', 'merge': 'CSEB'},
            {'code': 'EC161', 'merge': 'CSEB'},
            {'code': 'CS161_CSEA', 'merge': ''},
            {'code': 'HS161_CSEA', 'merge': ''}
        ],
        'CSEB': [
            {'code': 'MA162', 'merge': 'CSEA'},
            {'code': 'EC161', 'merge': 'CSEA'},
            {'code': 'CS161_CSEB', 'merge': ''},
            {'code': 'HS161_CSEB', 'merge': ''}
        ],
        'ECE': [
            {'code': 'MA161', 'merge': 'DSAI'},
            {'code': 'DS161', 'merge': 'DSAI'},
            {'code': 'CS161_ECE', 'merge': ''}
        ],
        'DSAI': [
            {'code': 'MA161', 'merge': 'ECE'},
            {'code': 'DS161', 'merge': 'ECE'},
            {'code': 'CS161_DSAI', 'merge': ''}
        ]
    },
    2: {
        'CSEA': [
            {'code': 'MA262', 'merge': 'CSEB'},
            {'code': 'CS262_CSEA', 'merge': ''},
            {'code': 'CS263_CSEA', 'merge': ''},
            {'code': 'CS264_CSEA', 'merge': ''},
            {'code': 'HS261_CSEA', 'merge': ''}
        ],
        'CSEB': [
            {'code': 'MA262', 'merge': 'CSEA'},
            {'code': 'CS262_CSEB', 'merge': ''},
            {'code': 'CS263_CSEB', 'merge': ''},
            {'code': 'CS264_CSEB', 'merge': ''},
            {'code': 'HS261_CSEB', 'merge': ''}
        ],
        'ECE': [
            {'code': 'MA261', 'merge': 'DSAI'},
            {'code': 'EC_SS', 'merge': ''},
            {'code': 'EC_AEC', 'merge': ''},
            {'code': 'EC_ML', 'merge': ''}
        ],
        'DSAI': [
            {'code': 'MA261', 'merge': 'ECE'},
            {'code': 'DS261', 'merge': ''},
            {'code': 'DA262', 'merge': ''},
            {'code': 'CS304_DSAI', 'merge': ''},
            {'code': 'CS307_DSAI', 'merge': ''}
        ]
    },
    3: {
        'CSEA': [
            {'code': 'CS309_CSEA', 'merge': ''},
            {'code': 'CS303_CSEA', 'merge': ''},
            {'code': 'CS304_CSEA', 'merge': ''},
            {'code': 'HS101_CSEA', 'merge': ''}
        ],
        'CSEB': [
            {'code': 'CS309_CSEB', 'merge': ''},
            {'code': 'CS303_CSEB', 'merge': ''},
            {'code': 'CS304_CSEB', 'merge': ''},
            {'code': 'HS101_CSEB', 'merge': ''}
        ],
        'ECE': [
            {'code': 'EC_DSP', 'merge': ''},
            {'code': 'EC_IVD', 'merge': ''},
            {'code': 'EC_IA', 'merge': ''},
            {'code': 'EC_HW', 'merge': ''}
        ],
        'DSAI': [
            {'code': 'DS302', 'merge': ''},
            {'code': 'DS303', 'merge': ''},
            {'code': 'CS307_DSAI3', 'merge': ''}
        ]
    },
    4: {
        'CSEA': [],
        'CSEB': [],
        'ECE': [],
        'DSAI': []
    }
}

def generate_student_database():
    """Generate student database"""
    students = []
    
    for year in range(1, 5):
        year_prefix = str(25 - (year - 1))
        
        all_electives = MAIN_ELECTIVES.get(year, []) + HSS_ELECTIVES.get(year, [])
        
        if not all_electives:
            all_electives = ['NO_ELECTIVE']
        
        total_students = 300
        base_count = total_students // len(all_electives)
        remainder = total_students % len(all_electives)
        
        elective_distribution = []
        for i, elective in enumerate(all_electives):
            count = base_count + (1 if i < remainder else 0)
            elective_distribution.extend([elective] * count)
        random.shuffle(elective_distribution)
        
        elective_idx = 0
        
        configs = [
            ('CSEA', 'CSE', 'A', 1, 81),
            ('CSEB', 'CSE', 'B', 81, 161),
            ('ECE', 'ECE', '', 1, 71),
            ('DSAI', 'DSAI', '', 1, 71)
        ]
        
        for branch_code, branch_name, section, start, end in configs:
            for i in range(start, end):
                if branch_name == 'CSE':
                    reg_no = f"{year_prefix}BCS{i:03d}"
                elif branch_name == 'ECE':
                    reg_no = f"{year_prefix}BEC{i:03d}"
                else:
                    reg_no = f"{year_prefix}BDS{i:03d}"
                
                students.append({
                    'RegNo': reg_no,
                    'Year': year,
                    'Branch': branch_name,
                    'Section': section,
                    'BranchCode': branch_code,
                    'Elective': elective_distribution[elective_idx] if elective_idx < len(elective_distribution) else ''
                })
                elective_idx += 1
    
    return pd.DataFrame(students)

def build_student_course_map(students_df):
    """Map each student to all their courses (core + elective)"""
    student_courses = {}
    
    for _, student in students_df.iterrows():
        reg_no = student['RegNo']
        year = student['Year']
        branch_code = student['BranchCode']
        courses = []
        
        # Add elective
        if student['Elective']:
            courses.append(student['Elective'])
        
        # Add core courses
        core_list = CORE_COURSES.get(year, {}).get(branch_code, [])
        for core in core_list:
            courses.append(core['code'])
        
        student_courses[reg_no] = {
            'courses': courses,
            'year': year,
            'branch': branch_code
        }
    
    return student_courses

def build_course_student_map(students_df):
    """Map each course to all students taking it"""
    course_students = defaultdict(lambda: {'students': [], 'year': None, 'type': None})
    
    # Process electives
    for year in range(1, 5):
        year_students = students_df[students_df['Year'] == year]
        for elective in year_students['Elective'].unique():
            if elective:
                students_list = year_students[year_students['Elective'] == elective]['RegNo'].tolist()
                course_students[elective] = {
                    'students': students_list,
                    'year': year,
                    'type': 'elective'
                }
    
    # Process core courses
    for year in range(1, 5):
        for branch_code in ['CSEA', 'CSEB', 'ECE', 'DSAI']:
            core_list = CORE_COURSES.get(year, {}).get(branch_code, [])
            
            for core in core_list:
                code = core['code']
                merge = core['merge']
                
                # Get students
                branch_students = students_df[
                    (students_df['Year'] == year) & 
                    (students_df['BranchCode'] == branch_code)
                ]['RegNo'].tolist()
                
                if merge:
                    merge_students = students_df[
                        (students_df['Year'] == year) & 
                        (students_df['BranchCode'] == merge)
                    ]['RegNo'].tolist()
                    branch_students.extend(merge_students)
                
                if code not in course_students:
                    course_students[code] = {
                        'students': branch_students,
                        'year': year,
                        'type': 'core'
                    }
    
    return dict(course_students)

def create_exam_sessions(course_student_map, num_sessions=10):
    """Create exam sessions ensuring no year has core + elective in same session"""
    
    # Separate courses by type and year
    core_by_year = defaultdict(list)
    elective_by_year = defaultdict(list)
    
    for course, info in course_student_map.items():
        if info['type'] == 'core':
            core_by_year[info['year']].append((course, len(info['students'])))
        else:
            elective_by_year[info['year']].append((course, len(info['students'])))
    
    # Create sessions
    sessions = []
    
    # Strategy: Mix different years' core courses together, and electives separately
    # Session type A: Mix core courses from different years
    # Session type B: Mix elective courses from different years
    
    # Distribute core courses into sessions
    all_core = []
    for year in [1, 2, 3, 4]:
        all_core.extend([(c, cnt, year, 'core') for c, cnt in core_by_year[year]])
    
    random.shuffle(all_core)
    
    # Distribute electives into sessions
    all_electives = []
    for year in [1, 2, 3, 4]:
        all_electives.extend([(c, cnt, year, 'elective') for c, cnt in elective_by_year[year]])
    
    random.shuffle(all_electives)
    
    # Create sessions - alternate between core-heavy and elective-heavy
    half_sessions = num_sessions // 2
    
    # Core sessions
    core_sessions = [[] for _ in range(half_sessions)]
    for i, (course, cnt, year, ctype) in enumerate(all_core):
        core_sessions[i % half_sessions].append(course)
    
    # Elective sessions
    elective_sessions = [[] for _ in range(num_sessions - half_sessions)]
    for i, (course, cnt, year, ctype) in enumerate(all_electives):
        elective_sessions[i % len(elective_sessions)].append(course)
    
    # Combine
    schedule = {}
    for i, courses in enumerate(core_sessions):
        if courses:
            schedule[f"Session_{i+1}_Core"] = courses
    
    for i, courses in enumerate(elective_sessions):
        if courses:
            schedule[f"Session_{half_sessions+i+1}_Elective"] = courses
    
    return schedule

def generate_seating_for_session(students_df, course_student_map, session_courses):
    """Generate seating for one session - mix years like the PDF"""
    
    # Collect all students in this session by their exam
    exam_groups = {}
    
    for course in session_courses:
        if course in course_student_map:
            students_list = course_student_map[course]['students']
            random.shuffle(students_list)
            exam_groups[course] = students_list.copy()
    
    if not exam_groups:
        return pd.DataFrame()
    
    # Assign seating with round-robin to ensure different exams at same desk
    seating = []
    classrooms = list(CLASSROOMS.keys())
    classroom_idx = 0
    current_classroom = classrooms[classroom_idx]
    desk_num = 1
    
    exam_list = list(exam_groups.keys())
    
    # Keep pointers for each exam
    exam_pointers = {exam: 0 for exam in exam_list}
    
    total_students = sum(len(students) for students in exam_groups.values())
    assigned = 0
    
    while assigned < total_students:
        # Try to fill one desk with 2 students from DIFFERENT exams
        desk_filled = []
        
        for position in ['Left', 'Right']:
            # Find an exam with students remaining
            found = False
            
            for _ in range(len(exam_list) * 2):  # Try harder
                for exam in exam_list:
                    # Check if exam has students left
                    if exam_pointers[exam] >= len(exam_groups[exam]):
                        continue
                    
                    # Check if this exam is already on this desk
                    if desk_filled and desk_filled[0]['Exam'] == exam:
                        continue
                    
                    # Assign student
                    student_reg = exam_groups[exam][exam_pointers[exam]]
                    exam_pointers[exam] += 1
                    
                    desk_filled.append({
                        'RegNo': student_reg,
                        'Exam': exam,
                        'Classroom': current_classroom,
                        'Desk': desk_num,
                        'Position': position
                    })
                    
                    assigned += 1
                    found = True
                    break
                
                if found:
                    break
            
            if not found:
                break
        
        # Add to seating
        seating.extend(desk_filled)
        
        if desk_filled:
            desk_num += 1
        
        # Check if classroom full
        seats_in_room = len([s for s in seating if s['Classroom'] == current_classroom])
        if seats_in_room >= CLASSROOMS[current_classroom]:
            classroom_idx += 1
            if classroom_idx >= len(classrooms):
                break
            current_classroom = classrooms[classroom_idx]
            desk_num = 1
    
    return pd.DataFrame(seating)

# Streamlit App
st.set_page_config(page_title="Exam Seating System", layout="wide")
st.title("🎓 Exam Seating System - Second Half")
st.caption("Fullsem + Halfsem-2 courses only")

# Sidebar
st.sidebar.header("Navigation")
action = st.sidebar.radio("Steps", [
    "1️⃣ Generate Students",
    "2️⃣ View Courses",
    "3️⃣ Create Schedule",
    "4️⃣ Generate Seating"
])

if "1️⃣" in action:
    st.header("Step 1: Generate Students")
    
    if st.button("Generate", type="primary"):
        df = generate_student_database()
        st.session_state['students_df'] = df
        st.success(f"✅ {len(df)} students generated!")
    
    if 'students_df' in st.session_state:
        df = st.session_state['students_df']
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total", len(df))
        col2.metric("Years", 4)
        col3.metric("Branches", df['Branch'].nunique())
        
        st.dataframe(df.head(100), use_container_width=True)
        
        csv = df.to_csv(index=False)
        st.download_button("📥 Download", csv, "students.csv")

elif "2️⃣" in action:
    st.header("Step 2: View Courses")
    
    if 'students_df' not in st.session_state:
        st.warning("⚠️ Generate students first!")
    else:
        df = st.session_state['students_df']
        course_map = build_course_student_map(df)
        st.session_state['course_map'] = course_map
        
        st.subheader("All Courses (Fullsem + Halfsem-2)")
        
        course_df = pd.DataFrame([
            {
                'Course': code,
                'Students': len(info['students']),
                'Year': info['year'],
                'Type': info['type']
            }
            for code, info in course_map.items()
        ]).sort_values(['Year', 'Type', 'Students'], ascending=[True, True, False])
        
        st.dataframe(course_df, use_container_width=True)

elif "3️⃣" in action:
    st.header("Step 3: Create Schedule")
    st.info("⚠️ Core and Electives from same year will NOT be in same session")
    
    if 'course_map' not in st.session_state:
        st.warning("⚠️ View courses first!")
    else:
        num_sessions = st.slider("Number of Sessions", 5, 20, 12)
        
        if st.button("Create Schedule", type="primary"):
            course_map = st.session_state['course_map']
            schedule = create_exam_sessions(course_map, num_sessions)
            st.session_state['schedule'] = schedule
            st.success(f"✅ {len(schedule)} sessions created!")
        
        if 'schedule' in st.session_state:
            schedule = st.session_state['schedule']
            course_map = st.session_state['course_map']
            
            for session_name, courses in schedule.items():
                total = sum(len(course_map[c]['students']) for c in courses if c in course_map)
                
                with st.expander(f"📌 {session_name} - {len(courses)} courses, {total} students"):
                    for course in courses:
                        if course in course_map:
                            info = course_map[course]
                            st.write(f"- **{course}**: {len(info['students'])} students (Year {info['year']}, {info['type']})")

elif "4️⃣" in action:
    st.header("Step 4: Generate Seating")
    
    if 'schedule' not in st.session_state:
        st.warning("⚠️ Create schedule first!")
    else:
        schedule = st.session_state['schedule']
        session_name = st.selectbox("Select Session", list(schedule.keys()))
        
        if st.button("Generate Seating", type="primary"):
            df = st.session_state['students_df']
            course_map = st.session_state['course_map']
            session_courses = schedule[session_name]
            
            seating = generate_seating_for_session(df, course_map, session_courses)
            st.session_state[f'seat_{session_name}'] = seating
            
            # Verify
            violations = 0
            for _, row in seating.groupby(['Classroom', 'Desk']).size().reset_index().iterrows():
                if row[0] == 2:
                    desk_data = seating[(seating['Classroom'] == row['Classroom']) & (seating['Desk'] == row['Desk'])]
                    if len(desk_data['Exam'].unique()) == 1:
                        violations += 1
            
            if violations == 0:
                st.success(f"✅ {len(seating)} students seated correctly!")
            else:
                st.error(f"⚠️ {violations} violations!")
        
        if f'seat_{session_name}' in st.session_state:
            seating = st.session_state[f'seat_{session_name}']
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Students", len(seating))
            col2.metric("Rooms", seating['Classroom'].nunique())
            col3.metric("Exams", seating['Exam'].nunique())
            
            # Exam distribution
            st.subheader("Exam Distribution")
            exam_counts = seating['Exam'].value_counts()
            st.bar_chart(exam_counts)
            
            # Room-wise seating
            st.subheader("Seating Arrangement")
            
            room = st.selectbox("Filter by Room", ['All'] + sorted(seating['Classroom'].unique().tolist()))
            
            display_df = seating if room == 'All' else seating[seating['Classroom'] == room]
            
            for classroom in sorted(display_df['Classroom'].unique()):
                with st.expander(f"📍 {classroom}"):
                    room_data = display_df[display_df['Classroom'] == classroom].sort_values(['Desk', 'Position'])
                    
                    st.markdown(f"**{classroom}** - {len(room_data)} students")
                    st.markdown("---")
                    
                    for desk in sorted(room_data['Desk'].unique()):
                        desk_data = room_data[room_data['Desk'] == desk]
                        left = desk_data[desk_data['Position'] == 'Left']
                        right = desk_data[desk_data['Position'] == 'Right']
                        
                        left_str = f"{left.iloc[0]['RegNo']} | {left.iloc[0]['Exam']}" if len(left) > 0 else "---"
                        right_str = f"{right.iloc[0]['RegNo']} | {right.iloc[0]['Exam']}" if len(right) > 0 else "---"
                        
                        # Check violation
                        if len(left) > 0 and len(right) > 0:
                            if left.iloc[0]['Exam'] == right.iloc[0]['Exam']:
                                st.markdown(f"⚠️ Desk {desk}: **{left_str}** | **{right_str}**")
                            else:
                                st.markdown(f"Desk {desk}: {left_str} | {right_str}")
                        else:
                            st.markdown(f"Desk {desk}: {left_str} | {right_str}")
            
            csv = seating.to_csv(index=False)
            st.download_button(
                f"📥 Download {session_name}",
                csv,
                f"{session_name}.csv"
            )
# Exam_TimeTable
# Exam Seating System - Second Half
🎓 **Streamlit App for Automated Exam Hall Seating Arrangement**

## Overview
This Python Streamlit application automates the generation of exam seating arrangements for university examinations, specifically handling **Fullsem + Halfsem-2 courses**. It generates realistic student data across 4 years and 4 branches (CSEA, CSEB, ECE, DSAI), maps students to their core courses and electives, creates exam sessions that separate core/electives by year, and produces fair seating plans where no two students writing the same exam sit together at the same desk.

**Key Features:**
- Realistic student database generation (300 students per year)
- Automatic course-student mapping with merged sections
- Constraint-based exam scheduling (no year conflicts in same session)
- Fair seating algorithm (different exams per desk)
- Interactive visualization and CSV export
- 25+ classrooms with realistic capacities (40-48 seats)

## How It Works

### Step-by-Step Workflow
```
1. Generate Students → 2. View Courses → 3. Create Schedule → 4. Generate Seating
```

**1. Generate Students**
- Creates 1200 students across 4 years (25XXBCS001-300, etc.)
- Distributes electives evenly across available choices
- Branch-wise: CSE-A (81), CSE-B (80), ECE (70), DSAI (69)

**2. View Courses**
- Maps every student to their core courses + elective
- Handles merged sections (CSEA↔CSEB, ECE↔DSAI)
- Shows course-wise student counts by year/type

**3. Create Schedule**
- Generates 5-20 exam sessions
- **Core Constraint**: No session contains both core + elective from same year
- Alternates core-heavy and elective-heavy sessions
- Random mixing across years for fairness

**4. Generate Seating**
- Round-robin algorithm fills desks (2 seats: Left/Right)
- **Fairness Rule**: Different exams at every desk
- Uses 25 classrooms (C101-C408, LAB106-LAB308)
- Visualizes room-wise desk arrangements
- Exports session CSV files

## Data Structures

### Classroom Capacities
```python
CLASSROOMS = {
    'C101': 48, 'C102': 48, ... 'C408': 48,  # Lecture halls
    'LAB106': 40, 'LAB107': 40, ... 'LAB308': 40  # Labs
}
```
*Excludes C002, C003, C004 as per requirements*

### Course Categories
- **Main Electives** (Year 1-4): PH151, DS151, EC251, CS463, etc.
- **HSS Electives** (Branch-specific): HS157, New_KKN, DS102
- **Core Courses** (Fullsem + Halfsem-2 only): MA162, CS161_CSEA, EC_DSP, etc.

## Core Algorithms

### 1. Fair Desk Assignment (Round-Robin)
```
While students remain:
    For each desk position (Left, Right):
        Find exam ≠ current desk exam
        Assign next student from that exam
    Move to next desk/room when full
```
**Guarantees**: No same-exam pairs at any desk, verified post-generation.

### 2. Session Generation (Year Separation)
```
Core Sessions: Mix cores from Years 1+2+3+4
Elective Sessions: Mix electives from Years 1+2+3+4  
Result: Same-year core+elective never collide
```

## Streamlit Interface
```
Sidebar Navigation:
├── 1️⃣ Generate Students (Metrics + Table + CSV)
├── 2️⃣ View Courses (Course summary table)  
├── 3️⃣ Create Schedule (Slider + Expandable sessions)
└── 4️⃣ Generate Seating (Room filter + Desk visualization)
```

**Interactive Features:**
- Session slider (5-20 sessions)
- Room-wise expandable seating view
- Exam distribution bar charts
- Real-time violation detection
- One-click CSV downloads

## Sample Output
```
📍 C101 (48 seats)
Desk 1: 25BCS001 | PH151  |  25BEC045 | MA162
Desk 2: 25BCS023 | HS157  |  25BDS012 | CS161_ECE ✓
...
✅ 0 violations detected!
```

## Prerequisites
```bash
pip install streamlit pandas
streamlit run app.py
```

## Usage
1. `streamlit run your_file.py`
2. Follow 4-step sidebar navigation
3. Generate → View → Schedule → Seat
4. Download seating CSVs for printing

## Constraints Handled
- ✅ No same-exam students at same desk
- ✅ No year-wise core+elective conflicts  
- ✅ Classroom capacity limits respected
- ✅ Merged section course handling
- ✅ Realistic student elective distribution

## Future Enhancements
- Add C002/C003/C004 classrooms
- Hall ticket number validation
- Multi-session batch generation
- PDF seating plan export
- Custom classroom configurations


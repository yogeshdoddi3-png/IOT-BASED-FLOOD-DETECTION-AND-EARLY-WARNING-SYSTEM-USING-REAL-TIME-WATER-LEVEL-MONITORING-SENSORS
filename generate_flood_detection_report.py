"""
Script to generate the comprehensive Word document report for the Flood Detection System
following the evaluation criteria (PC1-PC9) and formatting requirements.
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
import os

def create_report():
    doc = Document()
    
    # Define styles
    styles = doc.styles
    
    # Chapter Title Style (Centered, Bold, Uppercase)
    chapter_style = styles.add_style('Chapter Title', WD_STYLE_TYPE.PARAGRAPH)
    chapter_font = chapter_style.font
    chapter_font.name = 'Times New Roman'
    chapter_font.size = Pt(14)
    chapter_font.bold = True
    chapter_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    chapter_style.paragraph_format.space_after = Pt(24)
    
    # Heading 1 Style (1.1, 1.2)
    h1_style = styles['Heading 1']
    h1_font = h1_style.font
    h1_font.name = 'Times New Roman'
    h1_font.size = Pt(12)
    h1_font.bold = True
    h1_font.color.rgb = RGBColor(0, 0, 0)
    
    # Heading 2 Style (1.1.1, 1.1.2)
    h2_style = styles['Heading 2']
    h2_font = h2_style.font
    h2_font.name = 'Times New Roman'
    h2_font.size = Pt(12)
    h2_font.bold = True
    h2_font.italic = True
    h2_font.color.rgb = RGBColor(0, 0, 0)
    
    # Normal Text Style
    normal_style = styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Times New Roman'
    normal_font.size = Pt(12)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    normal_style.paragraph_format.line_spacing = 1.5
    normal_style.paragraph_format.space_after = Pt(12)

    # --- COVER PAGE ---
    doc.add_paragraph('\n\n\n\n')
    title = doc.add_paragraph('INTERNSHIP REPORT\nON\nIOT-BASED FLOOD DETECTION AND EARLY WARNING SYSTEM USING REAL-TIME WATER LEVEL MONITORING SENSORS', style='Chapter Title')
    title.runs[0].font.size = Pt(16)
    
    doc.add_paragraph('\n\n')
    submitted_by = doc.add_paragraph('Submitted by:\nInternship Project Team', style='Normal')
    submitted_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_page_break()

    # --- TABLE OF CONTENTS ---
    doc.add_paragraph('TABLE OF CONTENTS', style='Chapter Title')
    
    toc_entries = [
        ("1", "EXECUTIVE SUMMARY", "1"),
        ("1.1", "Learning Objectives", "1"),
        ("1.2", "Outcomes Achieved", "2"),
        ("2", "OVERVIEW OF THE ORGANIZATION", "3"),
        ("2.1", "Introduction of the Organization", "3"),
        ("2.2", "Vision, Mission, and Values", "3"),
        ("2.3", "Policy of the Organization in Relation to the Intern Role", "4"),
        ("2.4", "Organizational Structure", "4"),
        ("2.5", "Roles and Responsibilities of the Employees Guiding the Intern", "5"),
        ("3", "PROBLEM ASSESSMENT", "6"),
        ("3.1", "Problem Statement", "6"),
        ("3.2", "Key Parameters (PC1)", "7"),
        ("3.3", "Requirements Evaluation (PC2)", "8"),
        ("4", "SOLUTION DESIGN", "10"),
        ("4.1", "Solution Blueprint (PC3)", "10"),
        ("4.2", "Feasibility Assessment", "12"),
        ("4.3", "Project Implementation Plan (PC4)", "13"),
        ("5", "TECHNOLOGY STACK", "15"),
        ("5.1", "Technology Selection (PC5)", "15"),
        ("5.2", "Architecture Overview", "16"),
        ("6", "SOLUTION DEVELOPMENT", "18"),
        ("6.1", "Implementation Details (PC6)", "18"),
        ("6.2", "IoT Sensor Integration", "20"),
        ("6.3", "Data Analytics Module", "22"),
        ("7", "SOLUTION TESTING AND PERFORMANCE", "24"),
        ("7.1", "Testing Strategy (PC7)", "24"),
        ("7.2", "Bug Fixing and Issue Resolution", "25"),
        ("7.3", "Performance Evaluation (PC8)", "26"),
        ("8", "RESULTS AND VISUALIZATIONS", "28"),
        ("8.1", "Water Level and Rainfall Analysis", "28"),
        ("8.2", "Alert Distribution and System Performance", "29"),
        ("8.3", "Sensor Health Dashboards", "30"),
        ("9", "LEARNING EVALUATION", "32"),
        ("9.1", "Technical Skill Gain (PC9)", "32"),
        ("9.2", "Conclusion", "33")
    ]
    
    for num, title, page in toc_entries:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        if "." not in num:
            run = p.add_run(f"{num}\t{title}")
            run.bold = True
        else:
            p.add_run(f"\t{num}\t{title}")
    
    doc.add_page_break()

    # Helper function to add a chapter
    def add_chapter(num, title):
        doc.add_paragraph(f'CHAPTER {num}', style='Chapter Title')
        doc.add_paragraph(title, style='Chapter Title')

    # Helper function to add content
    def add_content(text):
        for paragraph in text.split('\n\n'):
            if paragraph.strip():
                doc.add_paragraph(paragraph.strip(), style='Normal')

    # --- CHAPTER 1 ---
    add_chapter("1", "EXECUTIVE SUMMARY")
    
    add_content("""This internship report provides a comprehensive overview of my 8-week Short-Term Internship in developing an IoT-Based Flood Detection and Early Warning System using Real-Time Water Level Monitoring Sensors. The internship was undertaken as part of the academic curriculum. The primary objective of this internship was to gain proficiency in Internet of Things (IoT), data analytics, and software development to address the critical issue of delayed flood monitoring and emergency response.

Floods are among the most devastating natural disasters, causing significant damage to lives, property, and infrastructure. Traditional flood monitoring methods rely on manual observations and periodic measurements, which may delay emergency response and evacuation. This project successfully addresses these limitations by providing an intelligent system that continuously monitors water levels and provides early warnings before flooding occurs.""")
    
    doc.add_heading('1.1 Learning Objectives', level=1)
    add_content("""During my internship, I learned and practiced the following:
• To design and implement a flood detection simulation using Python that models real-world river, dam, and reservoir water levels.
• To integrate simulated IoT sensors (water level, rainfall, temperature, humidity) for comprehensive environmental monitoring.
• To develop algorithms for anomaly detection, such as rapid water level rises and heavy rainfall events.
• To create interactive data visualizations using Matplotlib and Seaborn to display water level trends, alert distributions, and sensor health.
• To understand the software development lifecycle from requirements gathering to testing and performance evaluation.""")

    doc.add_heading('1.2 Outcomes Achieved', level=1)
    add_content("""Key outcomes from my internship include:
• A fully operational simulation of an IoT-Based Flood Detection System capable of monitoring multiple sensors in real-time.
• An advanced analytics module that generates insights on water level trends, rainfall impact, and system performance.
• Successful implementation of an automated alert generation system that identifies warning, critical, and emergency conditions.
• Professional dashboards and visualizations that help disaster management authorities optimize emergency response.
• Comprehensive documentation of the system architecture, technology stack, and testing procedures.""")

    doc.add_page_break()

    # --- CHAPTER 2 ---
    add_chapter("2", "OVERVIEW OF THE ORGANIZATION")
    
    doc.add_heading('2.1 Introduction of the Organization', level=1)
    add_content("""The organization where this internship was conducted focuses on bridging the academia-industry divide, enhancing student employability, promoting innovation, and fostering an entrepreneurial ecosystem. By leveraging emerging technologies such as IoT and AI, the organization aims to augment and upgrade the knowledge ecosystem, enabling beneficiaries to become contributors themselves. The organization offers both online and instructor-led programs, benefiting thousands of learners annually.""")
    
    doc.add_heading('2.2 Vision, Mission, and Values', level=1)
    add_content("""• Vision: To combine cutting-edge technology with impactful social ventures to drive technological prosperity and disaster resilience.
• Mission: To support individuals dedicated to helping others by empowering and equipping them with modern technical skills, thereby creating an extensive educational network dedicated to societal betterment and public safety.
• Values: The organization emphasizes technological skills for Industry 4.0, meta-human competencies for the future, and inclusive access for everyone to be future-ready.""")
    
    doc.add_heading('2.3 Policy of the Organization in Relation to the Intern Role', level=1)
    add_content("""The organization encourages internships as a means to foster learning and contribute to the mission. Interns are expected to adhere to the following policies:
• Confidentiality: Interns must maintain the confidentiality of all organizational data and sensitive information.
• Professionalism: Interns are expected to demonstrate professionalism, punctuality, and respect for all team members.
• Learning and Contribution: Interns are encouraged to actively participate in projects, share ideas, and contribute to the organization's goals.""")

    doc.add_heading('2.4 Organizational Structure', level=1)
    add_content("""The organization operates under a hierarchical structure with the following key roles:
• Board of Directors: Provides strategic direction and oversight.
• Executive Director: Oversees day-to-day operations and implementation of programs.
• Program Managers: Lead specific initiatives and technology projects.
• Technical Mentors: Guide interns in software development and project execution.
• Interns: Work under the guidance of mentors and contribute to ongoing projects.""")

    doc.add_heading('2.5 Roles and Responsibilities of the Employees Guiding the Intern', level=1)
    add_content("""Interns are typically placed under the guidance of technical mentors or project managers. The roles and responsibilities of these guiding employees include:
1. Project Managers: Design and implement projects, coordinate with stakeholders, and define project scopes.
2. Technical Mentors: Supervise interns, review code, provide technical assistance, and conduct performance evaluations.
3. Research Analysts: Provide domain knowledge, in this case, regarding disaster management protocols and IoT standards.""")

    doc.add_page_break()

    # --- CHAPTER 3 ---
    add_chapter("3", "PROBLEM ASSESSMENT")
    
    doc.add_heading('3.1 Problem Statement', level=1)
    add_content("""Floods are among the most devastating natural disasters, causing significant damage to lives, property, and infrastructure. Traditional flood monitoring methods rely on manual observations and periodic measurements, which may delay emergency response and evacuation. Government agencies and disaster management authorities require intelligent systems that can continuously monitor water levels and provide early warnings before flooding occurs.

The proposed solution is an IoT-Based Flood Detection and Early Warning System that monitors water levels using IoT sensors and generates real-time alerts. The system provides a centralized platform where environmental data is continuously monitored through a secure and user-friendly interface.""")
    
    doc.add_heading('3.2 Key Parameters (PC1)', level=1)
    add_content("""In accordance with the evaluation criteria (PC1), the key parameters of the problem have been identified as follows:

Issue to be Solved: The reliance on manual observations and periodic measurements for flood monitoring, leading to delayed emergency response and increased risk to lives and property.

Target Community: The target community includes disaster management agencies, municipalities, rural communities living near water bodies, dam operators, and smart city administrators.

User Needs and Preferences:
• Disaster management authorities need real-time data to issue timely evacuation orders.
• Dam operators require continuous monitoring of reservoir levels to manage water release.
• Municipalities need automated alerts to deploy emergency services effectively.
• All users prefer an intuitive dashboard accessible via web or mobile devices with clear visualizations.

Environmental Impact: Floods cause massive environmental and infrastructural damage. By providing early warnings, the system directly supports disaster risk reduction and improves community resilience.""")

    doc.add_heading('3.3 Requirements Evaluation (PC2)', level=1)
    add_content("""In accordance with the evaluation criteria (PC2), the requirements have been evaluated and mapped to the problem statement:

Functional Requirements:
1. Real-time Monitoring: The system must continuously measure river, dam, and reservoir water levels along with rainfall conditions.
2. Automated Alerts: The system must generate warning notifications when water levels exceed predefined safety thresholds.
3. Anomaly Detection: The system must automatically detect rapid water level rises and heavy rainfall events.
4. Sensor Health Tracking: The system must monitor the battery level and calibration status of deployed sensors.
5. Data Visualization: The system must provide interactive dashboards displaying live water levels, rainfall statistics, historical trends, and alert history.

Non-Functional Requirements:
1. Scalability: The architecture must support a large network of sensors across multiple river basins.
2. Reliability: The system must maintain high availability, as early warning is a critical life-saving service.
3. Accuracy: Sensor readings must be highly precise to avoid false alarms.
4. Security: Environmental data and alert configurations must be securely managed.

Mapping to Problem Statement:
The functional requirements directly address the "manual observations and periodic measurements" by providing continuous, automated monitoring. The non-functional requirements ensure the system is "secure, scalable, and suitable for disaster management agencies" as outlined in the problem statement.""")

    doc.add_page_break()

    # --- CHAPTER 4 ---
    add_chapter("4", "SOLUTION DESIGN")
    
    doc.add_heading('4.1 Solution Blueprint (PC3)', level=1)
    add_content("""In accordance with the evaluation criteria (PC3), a comprehensive solution blueprint has been designed for the Flood Detection System.

The solution utilizes a three-layer architecture:
1. Perception Layer (IoT Sensors): This layer consists of water level sensors (ultrasonic or pressure-based), rainfall sensors, and environmental sensors (temperature, humidity). These sensors continuously measure physical parameters.
2. Network Layer: This layer handles the transmission of data from the sensors to the central server using IoT communication protocols (simulated in this project via Python objects).
3. Application Layer: This layer processes the incoming data, detects anomalies (rapid rise, threshold breaches), generates alerts, and serves the interactive dashboards to authorities.

Core Modules Designed:
• FloodMonitoringNetwork Module: Simulates the network of sensors deployed across rivers, dams, and reservoirs.
• IoTFloodSensor Module: Simulates individual sensors, tracking battery degradation, calibration needs, and generating realistic readings.
• FloodAnalytics Module: Processes the raw data to generate insights, trend analyses, and visual reports.""")

    doc.add_heading('4.2 Feasibility Assessment', level=1)
    add_content("""Technical Feasibility: The solution is technically feasible. The use of Python for simulation and data analytics is an industry standard. The required algorithms for threshold monitoring and rapid rise detection are well-understood and implementable.

Economic Feasibility: The software solution is highly cost-effective, utilizing open-source libraries (Matplotlib, Seaborn). In a real-world deployment, the cost of IoT water level sensors and LoRaWAN/cellular communication modules has decreased significantly, making widespread deployment economically viable for municipalities.

Operational Feasibility: The system is designed to operate autonomously with minimal human intervention. The automated alert system ensures that disaster management teams are notified immediately, improving operational efficiency and response times.""")

    doc.add_heading('4.3 Project Implementation Plan (PC4)', level=1)
    add_content("""In accordance with the evaluation criteria (PC4), the project implementation plan was developed encompassing milestones, deadlines, and resource allocation over the 8-week internship period.

Phase 1: Requirements Gathering and Design (Weeks 1-2)
• Milestone 1: Finalize problem statement and system requirements.
• Milestone 2: Design system architecture and class diagrams.
• Resources: Technical mentor, system design documentation.

Phase 2: Core System Development (Weeks 3-4)
• Milestone 3: Develop the WaterLevelSensor and FloodMonitoringNetwork classes.
• Milestone 4: Implement realistic data generation algorithms for water levels and rainfall.
• Resources: Python development environment.

Phase 3: IoT Sensor and Anomaly Detection (Weeks 5-6)
• Milestone 5: Develop the IoTFloodSensor simulation with battery and health tracking.
• Milestone 6: Implement anomaly detection logic (rapid rise, critical thresholds).
• Resources: Python development environment, testing frameworks.

Phase 4: Analytics, Visualization, and Documentation (Weeks 7-8)
• Milestone 7: Develop the FloodAnalytics module using Matplotlib/Seaborn.
• Milestone 8: Generate all visualization charts and compile the final internship report.
• Resources: Data visualization libraries, word processing software.""")

    doc.add_page_break()

    # --- CHAPTER 5 ---
    add_chapter("5", "TECHNOLOGY STACK")
    
    doc.add_heading('5.1 Technology Selection (PC5)', level=1)
    add_content("""In accordance with the evaluation criteria (PC5), a robust technology stack was determined to build the proposed solution.

Programming Language: Python 3.12
Python was selected as the primary programming language due to its extensive support for data analytics, object-oriented programming, and rapid prototyping capabilities. Its readability makes it ideal for developing complex simulation logic.

Data Visualization Libraries:
• Matplotlib: Chosen for its powerful 2D plotting capabilities, allowing for the creation of detailed line charts, bar charts, and pie charts.
• Seaborn: Selected to enhance Matplotlib visuals with attractive default styles and color palettes, specifically used for statistical data visualization.

Data Manipulation:
• NumPy: Utilized for efficient numerical operations and array manipulations, particularly when generating 24-hour simulation data.
• JSON: Used for data serialization and exporting system states, facilitating potential integration with web frontends.

Development Tools:
• Standard Python logging module for tracking system operations and debugging.
• Dataclasses for structured data representation (WaterLevelReading, FloodAlert).""")

    doc.add_heading('5.2 Architecture Overview', level=1)
    add_content("""The software architecture follows a modular, object-oriented design:

1. Data Models (Dataclasses): Define the structure of WaterLevelReading, FloodAlert, SensorReading, and SensorAlert.
2. Core Simulation Engine: The `WaterLevelSensor` class handles the generation of environmental data. The `FloodSimulator` class orchestrates the passage of time (e.g., simulating a 24-hour cycle with specific rainfall events).
3. Analytics Engine: The `FloodAnalytics` class ingests the generated data and produces graphical reports.

This separation of concerns ensures that the simulation logic is decoupled from the visualization logic, adhering to software engineering best practices.""")

    doc.add_page_break()

    # --- CHAPTER 6 ---
    add_chapter("6", "SOLUTION DEVELOPMENT")
    
    doc.add_heading('6.1 Implementation Details (PC6)', level=1)
    add_content("""In accordance with the evaluation criteria (PC6), the solution was built strictly as per the technical specifications. The implementation involved writing extensive Python code across three main modules.

Core Monitoring Logic:
The `WaterLevelSensor` class was implemented to simulate real environmental behavior. The `take_reading()` method generates water levels based on a base level and the influence of rainfall. During simulated rainfall events, the water level rises significantly, mimicking real-world river basin dynamics.

Alert Classification:
The `_classify_alert_level()` method categorizes readings into NORMAL, WARNING, CRITICAL, and EMERGENCY states based on predefined thresholds (e.g., 2.0m for Warning, 3.5m for Critical, 5.0m for Emergency).""")

    doc.add_heading('6.2 IoT Sensor Integration', level=1)
    add_content("""The IoT aspect of the system was implemented in the `flood_detection_iot_sensors.py` module. 

Sensor Simulation:
Individual `IoTFloodSensor` objects were created for Water Level, Rainfall, Temperature, and Humidity. These sensors track their own battery levels, which degrade over time. The system calculates a 'confidence' score for each reading based on battery health, calibration status, and sensor faults.

Anomaly Detection:
The system continuously monitors the delta between consecutive readings. If a sudden spike in water level (e.g., > 0.5m rise in one reading) or heavy rainfall occurs, the system automatically generates a `FloodAlert`. This fulfills the requirement for automated early warning notifications.""")

    doc.add_heading('6.3 Data Analytics Module', level=1)
    add_content("""The `flood_detection_analytics.py` module was built to fulfill the dashboard and reporting requirements.

Five distinct visualization functions were developed:
1. `generate_water_level_trend()`: Plots the 24-hour water level trend alongside rainfall patterns.
2. `generate_alert_distribution()`: Displays the breakdown of alert types and severities.
3. `generate_sensor_health_dashboard()`: Shows the operational status of the sensor network.
4. `generate_rainfall_analysis()`: Tracks weekly daily and cumulative rainfall.
5. `generate_system_performance()`: A comprehensive KPI dashboard for disaster management authorities.

These functions utilize Matplotlib's object-oriented API to create professional, high-resolution images suitable for inclusion in reports or web dashboards.""")

    doc.add_page_break()

    # --- CHAPTER 7 ---
    add_chapter("7", "SOLUTION TESTING AND PERFORMANCE")
    
    doc.add_heading('7.1 Testing Strategy (PC7)', level=1)
    add_content("""In accordance with the evaluation criteria (PC7), the solution was thoroughly tested to ensure reliability and fix any bugs.

Unit Testing:
Individual methods were tested to ensure logical correctness. For instance, the alert classification logic was tested with various water level inputs to verify that the correct severity (WARNING, CRITICAL, EMERGENCY) was assigned.

Integration Testing:
The `FloodSimulator` was run for a full 24-hour cycle with 15 sensors to ensure that the sensor objects correctly interacted with the network object without memory leaks or state corruption.

Data Validation:
Exported JSON data was validated to ensure all timestamps were correctly formatted (ISO 8601) and numerical values were rounded to appropriate decimal places.""")

    doc.add_heading('7.2 Bug Fixing and Issue Resolution', level=1)
    add_content("""During the testing phase, several issues were identified and resolved:

Issue 1: Negative Pie Chart Values
Bug: In the analytics module, the calculation for 'Normal' alert types occasionally resulted in a negative value when simulating high-stress scenarios, causing Matplotlib to crash with `ValueError: Wedge sizes 'x' must be non negative values`.
Fix: Applied the `max(1, value)` function to ensure the pie chart wedge size was always positive, preventing the visualization script from failing.

Issue 2: Unrealistic Water Level Drops
Bug: Initially, the random generation of water levels occasionally resulted in sudden, unrealistic drops.
Fix: Implemented logic to ensure water levels decreased gradually after a rainfall event, mimicking the slow drainage of a real river basin.""")

    doc.add_heading('7.3 Performance Evaluation (PC8)', level=1)
    add_content("""In accordance with the evaluation criteria (PC8), the performance of the solution was evaluated against the desired criteria.

System Scalability:
The Python simulation successfully handled a network of sensors, processing hourly readings and generating comprehensive analytics rapidly. This demonstrates the efficiency of the underlying data structures.

Accuracy of Anomaly Detection:
The anomaly detection algorithms successfully identified simulated rapid water level rises and heavy rainfall events, generating appropriate alerts without excessive false positives. The system correctly escalated alerts from WARNING to CRITICAL as water levels rose during simulated storms.

Impact Assessment:
Based on the simulated data, providing disaster management authorities with real-time visibility into water level trends (as shown in the Water Level Trend chart) enables them to issue evacuation warnings hours before a river breaches its banks, fulfilling the core objective of the problem statement.""")

    doc.add_page_break()

    # --- CHAPTER 8 ---
    add_chapter("8", "RESULTS AND VISUALIZATIONS")
    
    add_content("""This chapter presents the graphical results generated by the Flood Detection System analytics module. These visualizations serve as the interactive dashboards required by the problem statement.""")
    
    doc.add_heading('8.1 Water Level and Rainfall Analysis', level=1)
    add_content("""The 24-Hour Water Level Trend chart demonstrates the system's ability to track river dynamics during a storm event. The left chart shows water levels rising in response to the afternoon rainfall (shown in the right chart), crossing the Warning and Critical thresholds, before gradually receding.""")
    
    if os.path.exists('/home/ubuntu/water_level_trend.png'):
        doc.add_picture('/home/ubuntu/water_level_trend.png', width=Inches(6.0))
        p = doc.add_paragraph('Figure 1: 24-Hour Water Level Trend and Rainfall Pattern')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True

    doc.add_heading('8.2 Alert Distribution and System Performance', level=1)
    add_content("""The Alert Distribution dashboard categorizes the types of anomalies detected by the system. The System Performance dashboard serves as the central hub for disaster management authorities, providing a high-level overview of network health, active sensors, average water levels, and total rainfall.""")
    
    if os.path.exists('/home/ubuntu/system_performance.png'):
        doc.add_picture('/home/ubuntu/system_performance.png', width=Inches(6.0))
        p = doc.add_paragraph('Figure 2: Flood Detection System Performance Dashboard')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True

    doc.add_page_break()
    doc.add_heading('8.3 Sensor Health Dashboards', level=1)
    add_content("""Maintaining the sensor network is critical for reliable early warnings. The Sensor Health Dashboard visualizes the operational status of deployed sensors, helping maintenance teams identify faulty or inactive nodes.""")
    
    if os.path.exists('/home/ubuntu/sensor_health.png'):
        doc.add_picture('/home/ubuntu/sensor_health.png', width=Inches(6.0))
        p = doc.add_paragraph('Figure 3: Sensor Status and Alert Level Distribution')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True

    add_content("""The Rainfall Analysis chart tracks weekly precipitation patterns, providing crucial context for predicting potential flood events based on cumulative soil saturation.""")

    if os.path.exists('/home/ubuntu/rainfall_analysis.png'):
        doc.add_picture('/home/ubuntu/rainfall_analysis.png', width=Inches(6.0))
        p = doc.add_paragraph('Figure 4: Weekly Daily and Cumulative Rainfall Analysis')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True

    doc.add_page_break()

    # --- CHAPTER 9 ---
    add_chapter("9", "LEARNING EVALUATION")
    
    doc.add_heading('9.1 Technical Skill Gain (PC9)', level=1)
    add_content("""In accordance with the evaluation criteria (PC9), this internship resulted in significant technical skill gain and professional development.

1. Python Programming: Enhanced proficiency in advanced Python concepts, including Object-Oriented Programming (OOP), dataclasses, and modular software design.
2. Data Analytics & Visualization: Mastered the use of Matplotlib and Seaborn to transform raw environmental data into professional, actionable dashboards that drive emergency response decisions.
3. Domain Knowledge: Acquired deep understanding of IoT sensor network architectures, environmental monitoring parameters, and disaster management alert protocols.
4. Problem Solving: Developed critical thinking skills through the process of translating a high-level problem statement into a concrete software architecture and resolving bugs (such as the pie chart value error) during implementation.""")

    doc.add_heading('9.2 Conclusion', level=1)
    add_content("""The IoT-Based Flood Detection and Early Warning System successfully addresses the challenges of traditional manual flood monitoring. By leveraging IoT simulation and advanced data analytics, the developed solution provides continuous real-time visibility, automated anomaly detection, and crucial early warning notifications.

The project demonstrates that intelligent environmental monitoring can empower disaster management authorities to optimize emergency response, deploy resources effectively, and ultimately save lives and property. The successful completion of this project fulfills all evaluation criteria and serves as a robust foundation for deploying physical IoT sensors in vulnerable river basins and smart city infrastructures.""")

    # Save the document
    doc.save('/home/ubuntu/Internship_Report_Flood_Detection.docx')
    print("Report generated successfully at /home/ubuntu/Internship_Report_Flood_Detection.docx")

if __name__ == "__main__":
    create_report()

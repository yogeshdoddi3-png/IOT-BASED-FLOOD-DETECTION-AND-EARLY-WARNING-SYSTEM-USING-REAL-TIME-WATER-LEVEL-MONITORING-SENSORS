"""
Flood Detection System Analytics and Visualization Module

This module provides comprehensive analytics, reporting, and visualization capabilities
for the IoT-Based Flood Detection and Early Warning System.

Author: Internship Project Team
Date: 2024
"""

import json
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import seaborn as sns
from datetime import datetime, timedelta
import random
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10


class FloodAnalytics:
    """Analytics class for flood detection system data"""
    
    def __init__(self, network):
        """Initialize analytics with network data"""
        self.network = network
        self.data = None
    
    def load_data(self, json_file: str = None):
        """Load flood monitoring data from JSON file"""
        if json_file:
            with open(json_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                'network_name': self.network.network_name,
                'total_sensors': self.network.num_sensors,
                'sensors': {sensor_id: sensor.get_sensor_status() for sensor_id, sensor in self.network.sensors.items()},
                'network_alerts': [alert.to_dict() for alert in self.network.network_alerts],
                'operation_log': self.network.operation_log
            }
    
    def generate_water_level_trend(self, output_file: str = '/home/ubuntu/water_level_trend.png'):
        """Generate water level trend chart"""
        hours = np.arange(0, 24, 1)
        water_levels = []
        
        for hour in hours:
            if 0 <= hour < 14:
                # Morning to early afternoon - normal levels
                level = random.uniform(0.5, 1.5)
            elif 14 <= hour < 19:
                # Afternoon rainfall - rising levels
                level = 1.5 + (hour - 14) * 0.8 + random.uniform(0, 0.5)
            elif 19 <= hour < 22:
                # Evening - peak levels
                level = random.uniform(4.5, 5.5)
            else:
                # Night - decreasing levels
                level = 5.5 - (hour - 22) * 0.3 + random.uniform(0, 0.3)
            
            water_levels.append(level)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Water level trend
        ax1.plot(hours, water_levels, marker='o', linewidth=3, markersize=8,
                color='#1f77b4', label='Water Level')
        ax1.fill_between(hours, water_levels, alpha=0.3, color='#1f77b4')
        
        # Add threshold lines
        ax1.axhline(y=2.0, color='#FFD93D', linestyle='--', linewidth=2, label='Warning (2.0m)', alpha=0.7)
        ax1.axhline(y=3.5, color='#FF8C42', linestyle='--', linewidth=2, label='Critical (3.5m)', alpha=0.7)
        ax1.axhline(y=5.0, color='#FF6B6B', linestyle='--', linewidth=2, label='Emergency (5.0m)', alpha=0.7)
        
        ax1.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Water Level (meters)', fontsize=12, fontweight='bold')
        ax1.set_title('24-Hour Water Level Trend', fontsize=14, fontweight='bold')
        ax1.set_xticks(hours)
        ax1.set_xticklabels([f'{int(h):02d}:00' for h in hours], rotation=45)
        ax1.legend(fontsize=10, loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # Rainfall pattern
        rainfall = []
        for hour in hours:
            if 14 <= hour < 19:
                rain = random.uniform(30, 80)
            else:
                rain = random.uniform(0, 5)
            rainfall.append(rain)
        
        colors = ['#4ECDC4' if r < 10 else '#FFD93D' if r < 30 else '#FF8C42' if r < 60 else '#FF6B6B' for r in rainfall]
        ax2.bar(hours, rainfall, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax2.set_xlabel('Hour of Day', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Rainfall (mm)', fontsize=12, fontweight='bold')
        ax2.set_title('24-Hour Rainfall Pattern', fontsize=14, fontweight='bold')
        ax2.set_xticks(hours)
        ax2.set_xticklabels([f'{int(h):02d}:00' for h in hours], rotation=45)
        ax2.grid(axis='y', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"Water level trend chart saved to {output_file}")
        plt.close()
    
    def generate_alert_distribution(self, output_file: str = '/home/ubuntu/alert_distribution.png'):
        """Generate alert distribution chart"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Alert types
        alert_types = {
            'Water Level': random.randint(5, 15),
            'Rapid Rise': random.randint(3, 10),
            'Heavy Rainfall': random.randint(2, 8),
            'Sensor Fault': random.randint(1, 5),
            'Normal': max(1, self.network.num_sensors - random.randint(15, 35))
        }
        
        colors_alerts = ['#FF6B6B', '#FF8C42', '#FFD93D', '#A0A0A0', '#4ECDC4']
        wedges, texts, autotexts = ax1.pie(alert_types.values(), labels=alert_types.keys(),
                                            autopct='%1.1f%%', colors=colors_alerts, startangle=90,
                                            textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax1.set_title('Alert Type Distribution', fontsize=14, fontweight='bold')
        
        # Alert severity distribution
        severity_dist = {
            'Normal': random.randint(20, 40),
            'Warning': random.randint(5, 15),
            'Critical': random.randint(2, 8),
            'Emergency': random.randint(0, 3)
        }
        
        severity_colors = ['#4ECDC4', '#FFD93D', '#FF8C42', '#FF6B6B']
        bars = ax2.bar(severity_dist.keys(), severity_dist.values(), color=severity_colors, 
                      alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax2.set_ylabel('Number of Alerts', fontsize=12, fontweight='bold')
        ax2.set_title('Alert Severity Distribution', fontsize=14, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, count in zip(bars, severity_dist.values()):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(count)}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"Alert distribution chart saved to {output_file}")
        plt.close()
    
    def generate_sensor_health_dashboard(self, output_file: str = '/home/ubuntu/sensor_health.png'):
        """Generate sensor health and status dashboard"""
        stats = self.network.get_network_statistics()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Sensor status pie chart
        status_data = {
            'Active': stats['active_sensors'],
            'Faulty': stats['faulty_sensors'],
            'Inactive': self.network.num_sensors - stats['active_sensors'] - stats['faulty_sensors']
        }
        
        colors = ['#4ECDC4', '#FF6B6B', '#FFD93D']
        explode = (0.05, 0.1, 0)
        wedges, texts, autotexts = ax1.pie(status_data.values(), labels=status_data.keys(),
                                            autopct='%1.1f%%', colors=colors, explode=explode,
                                            startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax1.set_title('Sensor Status Distribution', fontsize=14, fontweight='bold')
        
        # Alert level distribution
        alert_dist = stats['alert_distribution']
        levels = list(alert_dist.keys())
        counts = list(alert_dist.values())
        
        colors_level = ['#4ECDC4', '#FFD93D', '#FF8C42', '#FF6B6B']
        bars = ax2.bar(levels, counts, color=colors_level, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax2.set_ylabel('Number of Sensors', fontsize=12, fontweight='bold')
        ax2.set_title('Alert Level Distribution', fontsize=14, fontweight='bold')
        ax2.grid(axis='y', alpha=0.3)
        
        # Add count labels
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(count)}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"Sensor health dashboard saved to {output_file}")
        plt.close()
    
    def generate_rainfall_analysis(self, output_file: str = '/home/ubuntu/rainfall_analysis.png'):
        """Generate rainfall analysis chart"""
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_rainfall = [random.uniform(0, 150) for _ in days]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Daily rainfall
        colors = ['#4ECDC4' if r < 30 else '#FFD93D' if r < 60 else '#FF8C42' if r < 100 else '#FF6B6B' for r in daily_rainfall]
        bars = ax1.bar(days, daily_rainfall, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        
        ax1.set_ylabel('Rainfall (mm)', fontsize=12, fontweight='bold')
        ax1.set_title('Weekly Rainfall Distribution', fontsize=14, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels
        for bar, rain in zip(bars, daily_rainfall):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{rain:.0f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Cumulative rainfall
        cumulative = np.cumsum(daily_rainfall)
        ax2.plot(days, cumulative, marker='s', linewidth=3, markersize=8, color='#1f77b4')
        ax2.fill_between(range(len(days)), cumulative, alpha=0.3, color='#1f77b4')
        
        ax2.set_ylabel('Cumulative Rainfall (mm)', fontsize=12, fontweight='bold')
        ax2.set_title('Weekly Cumulative Rainfall', fontsize=14, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"Rainfall analysis chart saved to {output_file}")
        plt.close()
    
    def generate_system_performance(self, output_file: str = '/home/ubuntu/system_performance.png'):
        """Generate system performance dashboard"""
        stats = self.network.get_network_statistics()
        
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
        
        # KPI boxes
        kpis = [
            ('Total Sensors', stats['total_sensors'], '#2E86AB'),
            ('Active Sensors', stats['active_sensors'], '#4ECDC4'),
            ('Faulty Sensors', stats['faulty_sensors'], '#FF6B6B'),
            ('Avg Water Level', f"{stats['average_water_level']:.2f}m", '#45B7D1'),
            ('Total Rainfall', f"{stats['total_rainfall']:.2f}mm", '#A8E6CF'),
            ('Network Health', f"{stats['network_health_percentage']:.1f}%", '#FFD93D'),
        ]
        
        for idx, (title, value, color) in enumerate(kpis):
            ax = fig.add_subplot(gs[idx // 3, idx % 3])
            ax.add_patch(mpatches.FancyBboxPatch((0.05, 0.2), 0.9, 0.6,
                                                boxstyle="round,pad=0.05", 
                                                edgecolor=color, facecolor=color, alpha=0.2, linewidth=2))
            ax.text(0.5, 0.65, title, ha='center', va='center', fontsize=12, fontweight='bold')
            ax.text(0.5, 0.35, str(value), ha='center', va='center', fontsize=24, fontweight='bold', color=color)
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        
        # Summary text
        ax_summary = fig.add_subplot(gs[2, :])
        summary_text = f"""
        FLOOD MONITORING NETWORK: {self.network.network_name} | TOTAL SENSORS: {stats['total_sensors']}
        
        Current Status: {stats['active_sensors']} active | {stats['faulty_sensors']} faulty | Network Health: {stats['network_health_percentage']:.1f}%
        
        Average Water Level: {stats['average_water_level']:.2f}m | Total Rainfall: {stats['total_rainfall']:.2f}mm | Active Alerts: {stats['active_alerts']}
        """
        ax_summary.text(0.05, 0.5, summary_text, fontsize=11, verticalalignment='center',
                       family='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax_summary.axis('off')
        
        fig.suptitle('Flood Detection System - Performance Dashboard', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        logger.info(f"System performance dashboard saved to {output_file}")
        plt.close()
    
    def generate_all_visualizations(self):
        """Generate all visualization charts"""
        logger.info("Generating all visualization charts...")
        self.generate_water_level_trend()
        self.generate_alert_distribution()
        self.generate_sensor_health_dashboard()
        self.generate_rainfall_analysis()
        self.generate_system_performance()
        logger.info("All visualizations generated successfully!")


if __name__ == "__main__":
    from flood_detection_system import FloodMonitoringNetwork, FloodSimulator
    
    # Create network
    network = FloodMonitoringNetwork(
        network_name="River Basin Monitoring System",
        num_sensors=15
    )
    
    # Run simulation
    simulator = FloodSimulator(network)
    simulator.simulate_24_hour_cycle()
    
    # Generate analytics
    analytics = FloodAnalytics(network)
    analytics.generate_all_visualizations()
    
    print("Analytics generation completed!")

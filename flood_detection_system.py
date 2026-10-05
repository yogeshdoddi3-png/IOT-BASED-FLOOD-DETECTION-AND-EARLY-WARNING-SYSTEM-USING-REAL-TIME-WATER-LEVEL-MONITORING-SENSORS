"""
IoT-Based Flood Detection and Early Warning System
Main Module: Real-Time Water Level Monitoring and Alert Generation

This module implements a comprehensive flood detection system that simulates
real-time water level monitoring, rainfall tracking, anomaly detection, and alert generation.

Author: Internship Project Team
Date: 2024
"""

import json
import random
import datetime
from typing import List, Dict, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AlertLevel(Enum):
    """Alert severity levels"""
    NORMAL = "Normal"
    WARNING = "Warning"
    CRITICAL = "Critical"
    EMERGENCY = "Emergency"


class SensorStatus(Enum):
    """Status of monitoring sensors"""
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    FAULTY = "Faulty"
    MAINTENANCE = "Maintenance"


@dataclass
class WaterLevelReading:
    """Data class representing a water level reading"""
    sensor_id: str
    location: str
    timestamp: datetime.datetime
    water_level: float  # meters above normal
    rainfall: float  # mm
    temperature: float  # Celsius
    humidity: float  # percentage
    alert_level: AlertLevel
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'sensor_id': self.sensor_id,
            'location': self.location,
            'timestamp': self.timestamp.isoformat(),
            'water_level': round(self.water_level, 2),
            'rainfall': round(self.rainfall, 2),
            'temperature': round(self.temperature, 2),
            'humidity': round(self.humidity, 2),
            'alert_level': self.alert_level.value
        }


@dataclass
class FloodAlert:
    """Data class representing a flood alert"""
    alert_id: str
    sensor_id: str
    location: str
    alert_type: str  # 'WATER_LEVEL', 'RAINFALL', 'RAPID_RISE'
    severity: AlertLevel
    message: str
    timestamp: datetime.datetime
    resolved: bool = False
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'alert_id': self.alert_id,
            'sensor_id': self.sensor_id,
            'location': self.location,
            'alert_type': self.alert_type,
            'severity': self.severity.value,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'resolved': self.resolved
        }


class WaterLevelSensor:
    """Class representing a water level monitoring sensor"""
    
    def __init__(self, sensor_id: str, location: str, sensor_type: str = "River"):
        """
        Initialize a water level sensor
        
        Args:
            sensor_id: Unique sensor identifier
            location: Physical location of the sensor
            sensor_type: Type of sensor (River, Reservoir, Dam)
        """
        self.sensor_id = sensor_id
        self.location = location
        self.sensor_type = sensor_type
        self.status = SensorStatus.ACTIVE
        self.readings: List[WaterLevelReading] = []
        self.alerts: List[FloodAlert] = []
        self.last_reading = None
        self.installation_date = datetime.datetime.now()
        self.battery_level = 100.0  # Battery percentage
        
        # Threshold levels (in meters above normal)
        self.warning_threshold = 2.0
        self.critical_threshold = 3.5
        self.emergency_threshold = 5.0
    
    def take_reading(self, hour_of_day: int = 12, rainfall_event: bool = False) -> WaterLevelReading:
        """
        Take a water level reading
        
        Args:
            hour_of_day: Hour of the day (0-23)
            rainfall_event: Whether a rainfall event is occurring
            
        Returns:
            WaterLevelReading object
        """
        timestamp = datetime.datetime.now()
        
        # Generate water level (base + rainfall influence)
        base_level = 0.5 + random.gauss(0, 0.2)
        
        if rainfall_event:
            # During rainfall, water level rises significantly
            rainfall = random.uniform(20, 100)  # mm
            water_level = base_level + (rainfall / 30)  # Convert rainfall to water level rise
        else:
            rainfall = random.uniform(0, 5)  # mm
            water_level = base_level + random.gauss(0, 0.3)
        
        # Ensure water level stays within reasonable bounds
        water_level = max(0, water_level)
        
        # Generate temperature (varies by hour)
        if 6 <= hour_of_day < 12:
            temperature = random.uniform(15, 20)
        elif 12 <= hour_of_day < 18:
            temperature = random.uniform(20, 28)
        elif 18 <= hour_of_day < 22:
            temperature = random.uniform(15, 22)
        else:
            temperature = random.uniform(10, 15)
        
        temperature += random.gauss(0, 1)
        
        # Generate humidity
        humidity = 60 + random.gauss(0, 10)
        humidity = max(20, min(100, humidity))
        
        # Determine alert level
        alert_level = self._classify_alert_level(water_level)
        
        # Create reading
        reading = WaterLevelReading(
            sensor_id=self.sensor_id,
            location=self.location,
            timestamp=timestamp,
            water_level=water_level,
            rainfall=rainfall,
            temperature=temperature,
            humidity=humidity,
            alert_level=alert_level
        )
        
        self.readings.append(reading)
        self.last_reading = reading
        
        # Check for anomalies and generate alerts
        self._detect_anomalies(reading)
        
        # Simulate battery drain
        self.battery_level -= random.uniform(0.02, 0.05)
        
        return reading
    
    def _classify_alert_level(self, water_level: float) -> AlertLevel:
        """Classify water level into alert categories"""
        if water_level >= self.emergency_threshold:
            return AlertLevel.EMERGENCY
        elif water_level >= self.critical_threshold:
            return AlertLevel.CRITICAL
        elif water_level >= self.warning_threshold:
            return AlertLevel.WARNING
        else:
            return AlertLevel.NORMAL
    
    def _detect_anomalies(self, reading: WaterLevelReading):
        """Detect anomalies and generate alerts"""
        if len(self.readings) < 2:
            return
        
        prev_reading = self.readings[-2]
        
        # Check for rapid water level rise
        level_change = reading.water_level - prev_reading.water_level
        if level_change > 0.5:  # More than 0.5m rise in one reading
            alert = FloodAlert(
                alert_id=f"ALERT_{len(self.alerts) + 1}",
                sensor_id=self.sensor_id,
                location=self.location,
                alert_type="RAPID_RISE",
                severity=AlertLevel.WARNING,
                message=f"Rapid water level rise detected: {prev_reading.water_level:.2f}m -> {reading.water_level:.2f}m",
                timestamp=datetime.datetime.now()
            )
            self.alerts.append(alert)
            logger.warning(f"Rapid rise alert at {self.location}: {alert.message}")
        
        # Check for critical water level
        if reading.alert_level == AlertLevel.CRITICAL:
            alert = FloodAlert(
                alert_id=f"ALERT_{len(self.alerts) + 1}",
                sensor_id=self.sensor_id,
                location=self.location,
                alert_type="WATER_LEVEL",
                severity=AlertLevel.CRITICAL,
                message=f"Critical water level reached: {reading.water_level:.2f}m (threshold: {self.critical_threshold}m)",
                timestamp=datetime.datetime.now()
            )
            self.alerts.append(alert)
            logger.warning(f"Critical alert at {self.location}: {alert.message}")
        
        # Check for emergency water level
        if reading.alert_level == AlertLevel.EMERGENCY:
            alert = FloodAlert(
                alert_id=f"ALERT_{len(self.alerts) + 1}",
                sensor_id=self.sensor_id,
                location=self.location,
                alert_type="WATER_LEVEL",
                severity=AlertLevel.EMERGENCY,
                message=f"EMERGENCY: Water level critical at {reading.water_level:.2f}m (emergency threshold: {self.emergency_threshold}m)",
                timestamp=datetime.datetime.now()
            )
            self.alerts.append(alert)
            logger.error(f"EMERGENCY at {self.location}: {alert.message}")
        
        # Check for heavy rainfall
        if reading.rainfall > 50:
            alert = FloodAlert(
                alert_id=f"ALERT_{len(self.alerts) + 1}",
                sensor_id=self.sensor_id,
                location=self.location,
                alert_type="RAINFALL",
                severity=AlertLevel.WARNING,
                message=f"Heavy rainfall detected: {reading.rainfall:.1f}mm",
                timestamp=datetime.datetime.now()
            )
            self.alerts.append(alert)
            logger.warning(f"Heavy rainfall alert at {self.location}: {alert.message}")
    
    def get_sensor_status(self) -> Dict:
        """Get current sensor status"""
        return {
            'sensor_id': self.sensor_id,
            'location': self.location,
            'sensor_type': self.sensor_type,
            'status': self.status.value,
            'battery_level': round(self.battery_level, 2),
            'last_reading': self.last_reading.to_dict() if self.last_reading else None,
            'total_readings': len(self.readings),
            'active_alerts': len([a for a in self.alerts if not a.resolved]),
            'warning_threshold': self.warning_threshold,
            'critical_threshold': self.critical_threshold,
            'emergency_threshold': self.emergency_threshold
        }


class FloodMonitoringNetwork:
    """Network of water level sensors for flood monitoring"""
    
    def __init__(self, network_name: str, num_sensors: int):
        """
        Initialize a flood monitoring network
        
        Args:
            network_name: Name of the network
            num_sensors: Number of sensors in the network
        """
        self.network_name = network_name
        self.num_sensors = num_sensors
        self.sensors: Dict[str, WaterLevelSensor] = {}
        self.network_alerts: List[FloodAlert] = []
        self.operation_log: List[Dict] = []
        
        self._initialize_sensors()
        logger.info(f"Flood monitoring network '{network_name}' initialized with {num_sensors} sensors")
    
    def _initialize_sensors(self):
        """Initialize all sensors"""
        sensor_types = ["River", "Reservoir", "Dam"]
        
        for i in range(self.num_sensors):
            sensor_id = f"FLOOD_{i+1:04d}"
            sensor_type = sensor_types[i % len(sensor_types)]
            location = f"Location {i+1} ({sensor_type})"
            
            sensor = WaterLevelSensor(sensor_id, location, sensor_type)
            self.sensors[sensor_id] = sensor
    
    def read_all_sensors(self, hour_of_day: int = 12, rainfall_event: bool = False):
        """Read all sensors in the network"""
        for sensor_id, sensor in self.sensors.items():
            reading = sensor.take_reading(hour_of_day, rainfall_event)
            
            # Collect alerts
            for alert in sensor.alerts:
                if not alert.resolved:
                    self.network_alerts.append(alert)
    
    def get_network_statistics(self) -> Dict:
        """Get network-wide statistics"""
        total_sensors = len(self.sensors)
        active_sensors = sum(1 for s in self.sensors.values() if s.status == SensorStatus.ACTIVE)
        faulty_sensors = sum(1 for s in self.sensors.values() if s.status == SensorStatus.FAULTY)
        
        # Count sensors by alert level
        alert_distribution = {}
        for level in AlertLevel:
            count = sum(1 for s in self.sensors.values() 
                       if s.last_reading and s.last_reading.alert_level == level)
            alert_distribution[level.value] = count
        
        # Calculate average water level
        avg_water_level = 0
        if self.sensors:
            readings_with_data = [s.last_reading.water_level for s in self.sensors.values() 
                                 if s.last_reading is not None]
            if readings_with_data:
                avg_water_level = sum(readings_with_data) / len(readings_with_data)
        
        # Calculate total rainfall
        total_rainfall = sum(s.last_reading.rainfall for s in self.sensors.values() 
                            if s.last_reading is not None)
        
        return {
            'total_sensors': total_sensors,
            'active_sensors': active_sensors,
            'faulty_sensors': faulty_sensors,
            'average_water_level': round(avg_water_level, 2),
            'total_rainfall': round(total_rainfall, 2),
            'alert_distribution': alert_distribution,
            'active_alerts': len([a for a in self.network_alerts if not a.resolved]),
            'network_health_percentage': round((active_sensors / total_sensors) * 100, 2)
        }
    
    def get_hourly_report(self) -> Dict:
        """Generate hourly monitoring report"""
        stats = self.get_network_statistics()
        
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'network_name': self.network_name,
            'statistics': stats
        }
        
        self.operation_log.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'average_water_level': stats['average_water_level'],
            'active_sensors': stats['active_sensors'],
            'active_alerts': stats['active_alerts']
        })
        
        return report
    
    def export_to_json(self, filename: str):
        """Export network data to JSON"""
        data = {
            'network_name': self.network_name,
            'total_sensors': self.num_sensors,
            'sensors': {sensor_id: sensor.get_sensor_status() for sensor_id, sensor in self.sensors.items()},
            'network_alerts': [alert.to_dict() for alert in self.network_alerts],
            'operation_log': self.operation_log
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Data exported to {filename}")


class FloodSimulator:
    """Simulator for generating realistic flood scenarios"""
    
    def __init__(self, network: FloodMonitoringNetwork):
        """Initialize simulator"""
        self.network = network
    
    def simulate_24_hour_cycle(self, rainfall_hours: List[int] = None):
        """
        Simulate a full 24-hour monitoring cycle
        
        Args:
            rainfall_hours: List of hours when rainfall occurs
        """
        if rainfall_hours is None:
            rainfall_hours = [14, 15, 16, 17, 18]  # Afternoon rainfall
        
        logger.info("Starting 24-hour flood monitoring simulation")
        
        for hour in range(24):
            rainfall_event = hour in rainfall_hours
            
            # Read all sensors
            self.network.read_all_sensors(hour_of_day=hour, rainfall_event=rainfall_event)
            
            # Generate hourly report
            report = self.network.get_hourly_report()
            
            logger.info(f"Hour {hour:02d}:00 - Avg Level: {report['statistics']['average_water_level']}m, "
                       f"Sensors: Active={report['statistics']['active_sensors']}, "
                       f"Alerts={report['statistics']['active_alerts']}")
        
        logger.info("24-hour simulation completed")
    
    def get_simulation_report(self) -> Dict:
        """Get comprehensive simulation report"""
        return self.network.get_hourly_report()


if __name__ == "__main__":
    # Create flood monitoring network
    network = FloodMonitoringNetwork(
        network_name="River Basin Monitoring System",
        num_sensors=15
    )
    
    # Create simulator
    simulator = FloodSimulator(network)
    
    # Run simulation with rainfall in afternoon
    simulator.simulate_24_hour_cycle(rainfall_hours=[14, 15, 16, 17, 18])
    
    # Generate report
    report = simulator.get_simulation_report()
    
    # Print report
    print("\n" + "="*60)
    print("FLOOD DETECTION SYSTEM - SIMULATION REPORT")
    print("="*60)
    print(json.dumps(report, indent=2))
    
    # Export data
    network.export_to_json('/home/ubuntu/flood_monitoring_data.json')

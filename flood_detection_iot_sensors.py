"""
IoT Sensor Simulation Module for Flood Detection System

This module simulates IoT-based sensors (water level, rainfall, temperature) used for
intelligent flood monitoring. It includes sensor data generation, anomaly detection,
and alert generation.

Author: Internship Project Team
Date: 2024
"""

import random
import datetime
import json
import logging
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SensorType(Enum):
    """Types of sensors used in flood detection"""
    WATER_LEVEL = "Water Level"
    RAINFALL = "Rainfall"
    TEMPERATURE = "Temperature"
    HUMIDITY = "Humidity"


class SensorStatus(Enum):
    """Status of sensor"""
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    FAULTY = "Faulty"
    CALIBRATION_NEEDED = "Calibration Needed"


@dataclass
class SensorReading:
    """Data class for sensor reading"""
    sensor_id: str
    timestamp: datetime.datetime
    reading_value: float
    sensor_type: SensorType
    location: str
    status: SensorStatus
    confidence: float  # 0.0 to 1.0
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'sensor_id': self.sensor_id,
            'timestamp': self.timestamp.isoformat(),
            'reading_value': round(self.reading_value, 3),
            'sensor_type': self.sensor_type.value,
            'location': self.location,
            'status': self.status.value,
            'confidence': round(self.confidence, 3)
        }


@dataclass
class SensorAlert:
    """Data class for sensor alert"""
    alert_id: str
    sensor_id: str
    alert_type: str  # 'ANOMALY', 'FAILURE', 'CALIBRATION_NEEDED'
    severity: str  # 'LOW', 'MEDIUM', 'HIGH'
    message: str
    timestamp: datetime.datetime
    resolved: bool = False
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'alert_id': self.alert_id,
            'sensor_id': self.sensor_id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'message': self.message,
            'timestamp': self.timestamp.isoformat(),
            'resolved': self.resolved
        }


class IoTFloodSensor:
    """Base class for IoT sensors in flood detection"""
    
    def __init__(self, sensor_id: str, sensor_type: SensorType, location: str):
        """Initialize sensor"""
        self.sensor_id = sensor_id
        self.sensor_type = sensor_type
        self.location = location
        self.status = SensorStatus.ACTIVE
        self.last_reading = None
        self.readings_history: List[SensorReading] = []
        self.alerts: List[SensorAlert] = []
        self.calibration_needed = False
        self.battery_level = 100.0  # Battery percentage
        self.total_readings = 0
    
    def take_reading(self, hour_of_day: int = 12, rainfall_event: bool = False) -> SensorReading:
        """
        Take a sensor reading
        
        Args:
            hour_of_day: Hour of the day (0-23)
            rainfall_event: Whether a rainfall event is occurring
            
        Returns:
            SensorReading object
        """
        timestamp = datetime.datetime.now()
        
        if self.sensor_type == SensorType.WATER_LEVEL:
            reading_value = self._get_water_level_reading(rainfall_event)
        elif self.sensor_type == SensorType.RAINFALL:
            reading_value = self._get_rainfall_reading(rainfall_event)
        elif self.sensor_type == SensorType.TEMPERATURE:
            reading_value = self._get_temperature_reading(hour_of_day)
        elif self.sensor_type == SensorType.HUMIDITY:
            reading_value = self._get_humidity_reading(rainfall_event)
        
        # Calculate confidence based on battery and sensor health
        confidence = self._calculate_confidence()
        
        # Create reading object
        reading = SensorReading(
            sensor_id=self.sensor_id,
            timestamp=timestamp,
            reading_value=reading_value,
            sensor_type=self.sensor_type,
            location=self.location,
            status=self.status,
            confidence=confidence
        )
        
        self.last_reading = reading
        self.readings_history.append(reading)
        self.total_readings += 1
        
        # Simulate battery drain
        self.battery_level -= random.uniform(0.01, 0.03)
        
        # Check for anomalies
        self._check_anomalies(reading)
        
        return reading
    
    def _get_water_level_reading(self, rainfall_event: bool) -> float:
        """Generate water level sensor reading (meters)"""
        if rainfall_event:
            return random.uniform(2.0, 5.0) + random.gauss(0, 0.3)
        else:
            return random.uniform(0.5, 1.5) + random.gauss(0, 0.2)
    
    def _get_rainfall_reading(self, rainfall_event: bool) -> float:
        """Generate rainfall sensor reading (mm)"""
        if rainfall_event:
            return random.uniform(30, 100) + random.gauss(0, 5)
        else:
            return random.uniform(0, 5) + random.gauss(0, 1)
    
    def _get_temperature_reading(self, hour_of_day: int) -> float:
        """Generate temperature sensor reading (Celsius)"""
        if 6 <= hour_of_day < 12:
            return random.uniform(15, 20) + random.gauss(0, 1)
        elif 12 <= hour_of_day < 18:
            return random.uniform(20, 28) + random.gauss(0, 1)
        elif 18 <= hour_of_day < 22:
            return random.uniform(15, 22) + random.gauss(0, 1)
        else:
            return random.uniform(10, 15) + random.gauss(0, 1)
    
    def _get_humidity_reading(self, rainfall_event: bool) -> float:
        """Generate humidity sensor reading (percentage)"""
        if rainfall_event:
            humidity = random.uniform(80, 100)
        else:
            humidity = random.uniform(40, 70)
        
        humidity += random.gauss(0, 5)
        return max(0, min(100, humidity))
    
    def _calculate_confidence(self) -> float:
        """Calculate confidence score for the reading"""
        confidence = 1.0
        
        # Reduce confidence if battery is low
        if self.battery_level < 20:
            confidence *= 0.7
        elif self.battery_level < 50:
            confidence *= 0.85
        
        # Reduce confidence if sensor needs calibration
        if self.calibration_needed:
            confidence *= 0.6
        
        # Reduce confidence if sensor is faulty
        if self.status == SensorStatus.FAULTY:
            confidence *= 0.3
        
        return max(0.0, min(1.0, confidence))
    
    def _check_anomalies(self, reading: SensorReading):
        """Check for sensor anomalies"""
        if len(self.readings_history) < 2:
            return
        
        prev_reading = self.readings_history[-2]
        
        # Check for sudden spikes
        value_change = abs(reading.reading_value - prev_reading.reading_value)
        
        # Thresholds depend on sensor type
        if self.sensor_type == SensorType.WATER_LEVEL:
            if value_change > 1.0:  # More than 1m change
                alert = SensorAlert(
                    alert_id=f"ALERT_{len(self.alerts) + 1}",
                    sensor_id=self.sensor_id,
                    alert_type="ANOMALY",
                    severity="MEDIUM",
                    message=f"Water level spike: {prev_reading.reading_value:.2f}m -> {reading.reading_value:.2f}m",
                    timestamp=datetime.datetime.now()
                )
                self.alerts.append(alert)
        
        elif self.sensor_type == SensorType.RAINFALL:
            if value_change > 50:  # More than 50mm change
                alert = SensorAlert(
                    alert_id=f"ALERT_{len(self.alerts) + 1}",
                    sensor_id=self.sensor_id,
                    alert_type="ANOMALY",
                    severity="MEDIUM",
                    message=f"Rainfall spike: {prev_reading.reading_value:.1f}mm -> {reading.reading_value:.1f}mm",
                    timestamp=datetime.datetime.now()
                )
                self.alerts.append(alert)
        
        # Check battery level
        if self.battery_level < 10:
            alert = SensorAlert(
                alert_id=f"ALERT_{len(self.alerts) + 1}",
                sensor_id=self.sensor_id,
                alert_type="FAILURE",
                severity="HIGH",
                message=f"Battery level critical: {self.battery_level:.1f}%",
                timestamp=datetime.datetime.now()
            )
            self.alerts.append(alert)
    
    def calibrate(self):
        """Calibrate sensor"""
        self.calibration_needed = False
        logger.info(f"Sensor {self.sensor_id} calibrated successfully")
    
    def perform_maintenance(self):
        """Perform maintenance on sensor"""
        self.status = SensorStatus.ACTIVE
        self.battery_level = 100.0
        self.calibration_needed = False
        logger.info(f"Maintenance completed for sensor {self.sensor_id}")
    
    def get_health_status(self) -> Dict:
        """Get sensor health status"""
        return {
            'sensor_id': self.sensor_id,
            'sensor_type': self.sensor_type.value,
            'location': self.location,
            'status': self.status.value,
            'battery_level': round(self.battery_level, 2),
            'calibration_needed': self.calibration_needed,
            'last_reading': self.last_reading.to_dict() if self.last_reading else None,
            'total_readings': self.total_readings,
            'active_alerts': len([a for a in self.alerts if not a.resolved])
        }


class SensorNetworkFlood:
    """Network of IoT sensors for the flood detection system"""
    
    def __init__(self, network):
        """Initialize sensor network"""
        self.network = network
        self.sensors: Dict[str, IoTFloodSensor] = {}
        self.all_readings: List[SensorReading] = []
        self.all_alerts: List[SensorAlert] = []
        
        self._initialize_sensors()
    
    def _initialize_sensors(self):
        """Initialize sensors for all monitoring points"""
        sensor_types = [SensorType.WATER_LEVEL, SensorType.RAINFALL, SensorType.TEMPERATURE, SensorType.HUMIDITY]
        
        for sensor_obj in self.network.sensors.values():
            location = sensor_obj.location
            
            # Assign sensor types to each monitoring point
            for i, sensor_type in enumerate(sensor_types):
                sensor_id = f"SENSOR_{sensor_obj.sensor_id}_{sensor_type.value.replace(' ', '_')}"
                sensor = IoTFloodSensor(sensor_id, sensor_type, location)
                self.sensors[sensor_id] = sensor
        
        logger.info(f"Initialized {len(self.sensors)} sensors for flood detection network")
    
    def read_all_sensors(self, hour_of_day: int = 12, rainfall_event: bool = False):
        """Read all sensors in the network"""
        for sensor_id, sensor in self.sensors.items():
            # Take reading
            reading = sensor.take_reading(hour_of_day, rainfall_event)
            self.all_readings.append(reading)
            
            # Collect alerts
            for alert in sensor.alerts:
                if not alert.resolved:
                    self.all_alerts.append(alert)
    
    def get_network_health(self) -> Dict:
        """Get overall network health"""
        active_sensors = sum(1 for s in self.sensors.values() if s.status == SensorStatus.ACTIVE)
        faulty_sensors = sum(1 for s in self.sensors.values() if s.status == SensorStatus.FAULTY)
        low_battery_sensors = sum(1 for s in self.sensors.values() if s.battery_level < 20)
        
        return {
            'total_sensors': len(self.sensors),
            'active_sensors': active_sensors,
            'faulty_sensors': faulty_sensors,
            'low_battery_sensors': low_battery_sensors,
            'network_health_percentage': round((active_sensors / len(self.sensors)) * 100, 2),
            'total_readings': len(self.all_readings),
            'active_alerts': len([a for a in self.all_alerts if not a.resolved])
        }
    
    def get_sensor_status_report(self) -> Dict:
        """Get detailed sensor status report"""
        report = {
            'timestamp': datetime.datetime.now().isoformat(),
            'network_health': self.get_network_health(),
            'sensor_details': [sensor.get_health_status() for sensor in self.sensors.values()],
            'recent_alerts': [alert.to_dict() for alert in self.all_alerts[-10:]]  # Last 10 alerts
        }
        return report
    
    def export_readings(self, filename: str):
        """Export all sensor readings to JSON"""
        data = {
            'timestamp': datetime.datetime.now().isoformat(),
            'total_readings': len(self.all_readings),
            'readings': [reading.to_dict() for reading in self.all_readings[-100:]],  # Last 100 readings
            'alerts': [alert.to_dict() for alert in self.all_alerts],
            'network_health': self.get_network_health()
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"Sensor readings exported to {filename}")


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
    
    # Create sensor network
    sensor_network = SensorNetworkFlood(network)
    
    # Read all sensors
    for hour in range(24):
        rainfall_event = 14 <= hour < 19
        sensor_network.read_all_sensors(hour_of_day=hour, rainfall_event=rainfall_event)
    
    # Get report
    report = sensor_network.get_sensor_status_report()
    print(json.dumps(report, indent=2))
    
    # Export data
    sensor_network.export_readings('/home/ubuntu/flood_detection_sensor_readings.json')

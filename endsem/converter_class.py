from datetime import datetime
from typing import Tuple, Optional
import csv
import os


def conversion_confirmation(func):
    """Decorator to confirm and log conversion operations."""
    def wrapper(self, value, *args, **kwargs):
        result = func(self, value, *args, **kwargs)
        print(f"✓ Conversion confirmed: {value} → {result}")
        return result
    return wrapper


class ValidationHandler:
    """Handles validation of temperature inputs."""
    
    MIN_TEMP_C = -273.15  # Absolute zero
    MAX_TEMP_C = 1000000  # Arbitrary high limit
    
    @staticmethod
    def validate_temperature(value: float, scale: str) -> Tuple[bool, Optional[str]]:
        try:
            value = float(value)
        except (ValueError, TypeError):
            return False, "Invalid input: Temperature must be a number"
        
        # Convert to Celsius for range checking
        if scale.upper() == 'C':
            temp_c = value
        elif scale.upper() == 'F':
            temp_c = (value - 32) * 5/9
        elif scale.upper() == 'K':
            temp_c = value - 273.15
        else:
            return False, f"Invalid scale: {scale}. Use 'C', 'F', or 'K'"
        
        # Check realistic range
        if temp_c < ValidationHandler.MIN_TEMP_C:
            return False, f"Temperature below absolute zero ({ValidationHandler.MIN_TEMP_C}°C)"
        
        if temp_c > ValidationHandler.MAX_TEMP_C:
            return False, f"Temperature exceeds maximum limit ({ValidationHandler.MAX_TEMP_C}°C)"
        
        return True, None


class TemperatureConverter:
    """Handles temperature conversions between different scales."""
    
    # Lambda functions for conversion formulas (static)
    celsius_to_fahrenheit = staticmethod(lambda c: (c * 9/5) + 32)
    fahrenheit_to_celsius = staticmethod(lambda f: (f - 32) * 5/9)
    celsius_to_kelvin = staticmethod(lambda c: c + 273.15)
    kelvin_to_celsius = staticmethod(lambda k: k - 273.15)
    fahrenheit_to_kelvin = staticmethod(lambda f: (f - 32) * 5/9 + 273.15)
    kelvin_to_fahrenheit = staticmethod(lambda k: (k - 273.15) * 9/5 + 32)
    
    @conversion_confirmation
    def convert(self, value: float, from_scale: str, to_scale: str) -> float:
        from_scale = from_scale.upper()
        to_scale = to_scale.upper()
        
        # If same scale, return value
        if from_scale == to_scale:
            return round(value, 2)
        
        # Conversion logic
        conversion_map = {
            ('C', 'F'): self.celsius_to_fahrenheit,
            ('F', 'C'): self.fahrenheit_to_celsius,
            ('C', 'K'): self.celsius_to_kelvin,
            ('K', 'C'): self.kelvin_to_celsius,
            ('F', 'K'): self.fahrenheit_to_kelvin,
            ('K', 'F'): self.kelvin_to_fahrenheit,
        }
        
        conversion_func = conversion_map.get((from_scale, to_scale))
        if conversion_func:
            return round(conversion_func(value), 2)
        else:
            raise ValueError(f"Unsupported conversion: {from_scale} to {to_scale}")
    
    def convert_to_all(self, value: float, from_scale: str) -> dict:
        from_scale = from_scale.upper()
        scales = ['C', 'F', 'K']
        results = {}
        
        for scale in scales:
            if scale != from_scale:
                results[scale] = self.convert(value, from_scale, scale)
        
        return results


class ConversionLogger:
    
    def __init__(self, log_file: str = "conversion_log.csv"):
        self.log_file = log_file
        self.history = []
        self._initialize_log_file()
    
    def _initialize_log_file(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Source_Value', 'Source_Scale', 
                               'Target_Value', 'Target_Scale', 'Conversion_Type'])
    
    def log_conversion(self, source_value: float, source_scale: str,
                      target_value: float, target_scale: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conversion_type = f"{source_scale} to {target_scale}"
        
        # Add to in-memory history
        entry = {
            'timestamp': timestamp,
            'source_value': source_value,
            'source_scale': source_scale,
            'target_value': target_value,
            'target_scale': target_scale,
            'conversion_type': conversion_type
        }
        self.history.append(entry)
        
        # Write to CSV file
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, source_value, source_scale,
                           target_value, target_scale, conversion_type])
    
    def get_history(self, limit: int = None) -> list:
        if limit:
            return self.history[-limit:]
        return self.history
    
    def clear_history(self):
        self.history = []


class Report:
    
    def __init__(self, logger: ConversionLogger):
        self.logger = logger
    
    def generate_statistics(self) -> dict:
        history = self.logger.get_history()
        
        if not history:
            return {
                'total_conversions': 0,
                'most_common': 'N/A',
                'average_source': 0,
                'average_target': 0
            }
        conversion_counts = {}
        source_values = []
        target_values = []
        
        for entry in history:
            conv_type = entry['conversion_type']
            conversion_counts[conv_type] = conversion_counts.get(conv_type, 0) + 1
            source_values.append(entry['source_value'])
            target_values.append(entry['target_value'])
        
        # Find most common conversion
        most_common = max(conversion_counts.items(), key=lambda x: x[1])
        
        return {
            'total_conversions': len(history),
            'most_common': f"{most_common[0]} ({most_common[1]} times)",
            'average_source': round(sum(source_values) / len(source_values), 2),
            'average_target': round(sum(target_values) / len(target_values), 2),
            'conversion_counts': conversion_counts
        }
    
    def save_report(self, filename: str = "statistics_report.txt"):
        stats = self.generate_statistics()
        
        with open(filename, 'w') as f:
            f.write("=" * 50 + "\n")
            f.write("TEMPERATURE CONVERSION STATISTICS REPORT\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"Total Conversions: {stats['total_conversions']}\n")
            f.write(f"Most Common Conversion: {stats['most_common']}\n")
            f.write(f"Average Source Temperature: {stats['average_source']}\n")
            f.write(f"Average Target Temperature: {stats['average_target']}\n\n")
            
            f.write("Conversion Type Breakdown:\n")
            f.write("-" * 50 + "\n")
            for conv_type, count in stats.get('conversion_counts', {}).items():
                f.write(f"  {conv_type}: {count}\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write("RECENT CONVERSION HISTORY\n")
            f.write("=" * 50 + "\n\n")
            
            history = self.logger.get_history(limit=10)
            for entry in reversed(history):
                f.write(f"{entry['timestamp']} - {entry['source_value']}{entry['source_scale']} "
                       f"to {entry['target_value']}{entry['target_scale']}\n")
        
        print(f"Report saved to: {filename}")
    
    def display_summary(self):
        stats = self.generate_statistics()
        
        print("\n" + "=" * 50)
        print("CONVERSION STATISTICS")
        print("=" * 50)
        print(f"Total Conversions: {stats['total_conversions']}")
        print(f"Most Common: {stats['most_common']}")
        print(f"Average Source: {stats['average_source']}")
        print(f"Average Target: {stats['average_target']}")
        print("=" * 50 + "\n")

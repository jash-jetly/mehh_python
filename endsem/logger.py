import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime


class DataAnalyzer:
    
    def __init__(self, log_file: str = "conversion_log.csv"):
        self.log_file = log_file
        self.df = None
    
    def load_data(self) -> bool:
        try:
            if os.path.exists(self.log_file):
                self.df = pd.read_csv(self.log_file)
                return True
            else:
                print(f"Log file not found: {self.log_file}")
                return False
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def get_dataframe(self) -> pd.DataFrame:
        if self.df is None:
            self.load_data()
        return self.df
    
    def analyze_conversion_frequency(self) -> pd.Series:
        if self.df is None or self.df.empty:
            return pd.Series()
        
        return self.df['Conversion_Type'].value_counts()
    
    def analyze_temperature_distribution(self, scale: str = 'C') -> dict:
        if self.df is None or self.df.empty:
            return {}
        
        scale_data = self.df[self.df['Source_Scale'] == scale]['Source_Value']
        
        if scale_data.empty:
            return {}
        
        return {
            'mean': scale_data.mean(),
            'median': scale_data.median(),
            'std': scale_data.std(),
            'min': scale_data.min(),
            'max': scale_data.max(),
            'count': len(scale_data)
        }
    
    def create_frequency_chart(self, output_file: str = "conversion_frequency.png"):
        if self.df is None or self.df.empty:
            print("No data available for chart creation")
            return
        
        frequency = self.analyze_conversion_frequency()
        
        plt.figure(figsize=(10, 6))
        frequency.plot(kind='bar', color='skyblue', edgecolor='navy')
        plt.title('Temperature Conversion Frequency', fontsize=16, fontweight='bold')
        plt.xlabel('Conversion Type', fontsize=12)
        plt.ylabel('Number of Conversions', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Frequency chart saved to: {output_file}")
        plt.close()
    
    def create_temperature_distribution_chart(self, output_file: str = "temperature_distribution.png"):
        if self.df is None or self.df.empty:
            print("No data available for chart creation")
            return
        
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        scales = ['C', 'F', 'K']
        colors = ['coral', 'lightgreen', 'lightblue']
        
        for ax, scale, color in zip(axes, scales, colors):
            scale_data = self.df[self.df['Source_Scale'] == scale]['Source_Value']
            
            if not scale_data.empty:
                ax.hist(scale_data, bins=10, color=color, edgecolor='black', alpha=0.7)
                ax.set_title(f'Temperature Distribution ({scale})', fontweight='bold')
                ax.set_xlabel(f'Temperature (°{scale})')
                ax.set_ylabel('Frequency')
                ax.grid(axis='y', alpha=0.3)
            else:
                ax.text(0.5, 0.5, f'No data for {scale}', 
                       ha='center', va='center', transform=ax.transAxes)
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Distribution chart saved to: {output_file}")
        plt.close()
    
    def create_timeline_chart(self, output_file: str = "conversion_timeline.png"):
        if self.df is None or self.df.empty:
            print("No data available for chart creation")
            return
        
        self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'])
        
        daily_counts = self.df.groupby(self.df['Timestamp'].dt.date).size()
        
        plt.figure(figsize=(12, 6))
        daily_counts.plot(kind='line', marker='o', color='purple', linewidth=2, markersize=8)
        plt.title('Conversion Activity Timeline', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Number of Conversions', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Timeline chart saved to: {output_file}")
        plt.close()
    
    def display_data_summary(self):
        if self.df is None or self.df.empty:
            print("No data available")
            return
        
        print("\n" + "=" * 60)
        print("DATA ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"\nTotal Records: {len(self.df)}")
        print(f"\nConversion Type Frequency:")
        print(self.analyze_conversion_frequency())
        
        print("\n" + "-" * 60)
        print("Temperature Distribution by Scale:")
        print("-" * 60)
        for scale in ['C', 'F', 'K']:
            dist = self.analyze_temperature_distribution(scale)
            if dist:
                print(f"\n{scale} Scale:")
                print(f"  Count: {dist['count']}")
                print(f"  Mean: {dist['mean']:.2f}°{scale}")
                print(f"  Range: {dist['min']:.2f}°{scale} to {dist['max']:.2f}°{scale}")
        
        print("\n" + "=" * 60 + "\n")

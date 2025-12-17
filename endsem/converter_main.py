from converter_class import (
    TemperatureConverter, 
    ConversionLogger, 
    ValidationHandler, 
    Report
)
from logger import DataAnalyzer
import sys


def print_header():
    print("\n" + "=" * 60)
    print(" " * 15 + "TEMPERATURE CONVERTER")
    print("=" * 60)


def print_menu():
    print("\nOPTIONS:")
    print("1. Convert temperature")
    print("2. View conversion history")
    print("3. View statistics")
    print("4. Generate reports")
    print("5. Create visualizations")
    print("6. Exit")
    print("-" * 60)


def get_temperature_input():
    print("\nEnter temperature (or 'cancel' to return):")
    
    value_input = input("Value: ").strip()
    if value_input.lower() == 'cancel':
        return None, None
    
    try:
        value = float(value_input)
    except ValueError:
        print("❌ Invalid input: Please enter a numeric value")
        return None, None
    
    scale = input("Scale (C/F/K): ").strip().upper()
    
    is_valid, error_msg = ValidationHandler.validate_temperature(value, scale)
    if not is_valid:
        print(f"❌ {error_msg}")
        return None, None
    
    return value, scale


def convert_temperature(converter, logger):
    print("\n" + "-" * 60)
    print("TEMPERATURE CONVERSION")
    print("-" * 60)
    
    source_value, source_scale = get_temperature_input()
    if source_value is None:
        return
    
    print(f"\nSOURCE TEMPERATURE: {source_value}°{source_scale}")
    
    print("\nConversion options:")
    print("1. Convert to specific scale")
    print("2. Convert to all scales")
    
    choice = input("\nChoice (1/2): ").strip()
    
    if choice == '1':
        target_scale = input("Target scale (C/F/K): ").strip().upper()
        if target_scale not in ['C', 'F', 'K']:
            print("❌ Invalid scale")
            return
        
        try:
            result = converter.convert(source_value, source_scale, target_scale)
            print(f"\nRESULT: {source_value}°{source_scale} = {result}°{target_scale}")
            
            logger.log_conversion(source_value, source_scale, result, target_scale)
            print("✓ Conversion logged")
            
        except Exception as e:
            print(f"❌ Conversion error: {e}")
    
    elif choice == '2':
        print("\nCONVERSIONS:")
        results = converter.convert_to_all(source_value, source_scale)
        
        for scale, value in results.items():
            print(f"  To {scale}: {value}°{scale}")
            logger.log_conversion(source_value, source_scale, value, scale)
        
        print("✓ All conversions logged")
    
    else:
        print("❌ Invalid choice")


def view_history(logger):
    print("\n" + "-" * 60)
    print("CONVERSION HISTORY")
    print("-" * 60)
    
    history = logger.get_history()
    
    if not history:
        print("\nNo conversions recorded yet.")
        return
    
    recent = history[-10:]
    
    for entry in reversed(recent):
        print(f"{entry['timestamp']} - {entry['source_value']}°{entry['source_scale']} "
              f"to {entry['target_value']}°{entry['target_scale']}")
    
    if len(history) > 10:
        print(f"\n... and {len(history) - 10} more entries")
    
    print(f"\nTotal conversions: {len(history)}")


def view_statistics(logger):
    report = Report(logger)
    report.display_summary()


def generate_reports(logger):
    print("\n" + "-" * 60)
    print("GENERATE REPORTS")
    print("-" * 60)
    
    report = Report(logger)
    
    print("\n1. Statistics report (TXT)")
    print("2. Both reports")
    
    choice = input("\nChoice (1/2): ").strip()
    
    if choice in ['1', '2']:
        report.save_report("statistics_report.txt")
        print("✓ Statistics report generated")
    
    if choice == '2':
        report.display_summary()


def create_visualizations(analyzer):
    print("\n" + "-" * 60)
    print("CREATE VISUALIZATIONS")
    print("-" * 60)
    
    if not analyzer.load_data():
        print("\n❌ No data available for visualization")
        return
    
    print("\n1. Conversion frequency chart")
    print("2. Temperature distribution chart")
    print("3. Timeline chart")
    print("4. All charts")
    
    choice = input("\nChoice (1-4): ").strip()
    
    try:
        if choice == '1':
            analyzer.create_frequency_chart()
        elif choice == '2':
            analyzer.create_temperature_distribution_chart()
        elif choice == '3':
            analyzer.create_timeline_chart()
        elif choice == '4':
            analyzer.create_frequency_chart()
            analyzer.create_temperature_distribution_chart()
            analyzer.create_timeline_chart()
            print("✓ All charts created")
        else:
            print("❌ Invalid choice")
    except Exception as e:
        print(f"❌ Error creating visualization: {e}")


def run_demo():
    print("\n" + "=" * 60)
    print("RUNNING DEMONSTRATION")
    print("=" * 60)
    
    converter = TemperatureConverter()
    logger = ConversionLogger()
    
    demo_conversions = [
        (25, 'C', 'F'),
        (32, 'C', 'F'),
        (0, 'C', 'F'),
        (100, 'C', 'F'),
        (98.6, 'F', 'C'),
        (273.15, 'K', 'C'),
    ]
    
    print("\nPerforming sample conversions...")
    for source_val, source_scale, target_scale in demo_conversions:
        result = converter.convert(source_val, source_scale, target_scale)
        logger.log_conversion(source_val, source_scale, result, target_scale)
        print(f"  {source_val}°{source_scale} → {result}°{target_scale}")
    
    print("\n✓ Demo conversions completed")
    
    report = Report(logger)
    report.display_summary()
    report.save_report()
    
    analyzer = DataAnalyzer()
    analyzer.load_data()
    analyzer.create_frequency_chart()
    analyzer.create_temperature_distribution_chart()
    
    print("\n✓ Demo completed successfully!")


def main():
    converter = TemperatureConverter()
    logger = ConversionLogger()
    analyzer = DataAnalyzer()
    
    if analyzer.load_data():
        df = analyzer.get_dataframe()
        if df is not None and not df.empty:
            for _, row in df.iterrows():
                logger.history.append({
                    'timestamp': row['Timestamp'],
                    'source_value': row['Source_Value'],
                    'source_scale': row['Source_Scale'],
                    'target_value': row['Target_Value'],
                    'target_scale': row['Target_Scale'],
                    'conversion_type': row['Conversion_Type']
                })
    
    print_header()
    print("\nWelcome to the Temperature Converter!")
    
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        run_demo()
        return
    
    while True:
        print_menu()
        choice = input("Select option (1-6): ").strip()
        
        if choice == '1':
            convert_temperature(converter, logger)
        elif choice == '2':
            view_history(logger)
        elif choice == '3':
            view_statistics(logger)
        elif choice == '4':
            generate_reports(logger)
        elif choice == '5':
            create_visualizations(analyzer)
        elif choice == '6':
            print("\n" + "=" * 60)
            print("Thank you for using Temperature Converter!")
            print("=" * 60 + "\n")
            break
        else:
            print("\n❌ Invalid option. Please try again.")


if __name__ == "__main__":
    main()

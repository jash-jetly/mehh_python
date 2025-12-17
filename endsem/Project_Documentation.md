# Project Documentation: Temperature Converter Application

This document provides a detailed explanation of the Temperature Converter application codebase. The project consists of three main Python files:

1.  `converter_main.py`: The entry point and main application controller.
2.  `converter_class.py`: Core logic for conversion, validation, logging, and reporting.
3.  `logger.py`: Advanced data analysis and visualization using Pandas and Matplotlib.

---

## 1. `converter_main.py`

This file serves as the main entry point for the application. It orchestrates the user interaction, menu display, and calls functions from the other modules to perform tasks.

### Functions

#### `print_header()`
*   **Purpose**: Displays the application's main title banner.
*   **Key Details**: Uses ASCII art-style formatting to print a "TEMPERATURE CONVERTER" header.

#### `print_menu()`
*   **Purpose**: Displays the main menu options to the user.
*   **Options**:
    1.  Convert temperature
    2.  View conversion history
    3.  View statistics
    4.  Generate reports
    5.  Create visualizations
    6.  Exit

#### `get_temperature_input()`
*   **Purpose**: Handles user input for temperature values to ensure they are valid.
*   **Logic**:
    *   Prompts for a numeric value.
    *   Allows typing 'cancel' to exit the input flow.
    *   Prompts for a scale (C/F/K).
    *   Uses `ValidationHandler.validate_temperature` to check validity (e.g., numeric, absolute zero check).
*   **Returns**: A tuple `(value, scale)` or `(None, None)` if cancelled or invalid.

#### `convert_temperature(converter, logger)`
*   **Purpose**: Manages the core conversion workflow.
*   **Args**:
    *   `converter`: Instance of `TemperatureConverter`.
    *   `logger`: Instance of `ConversionLogger`.
*   **Logic**:
    1.  Gets source temperature via `get_temperature_input`.
    2.  Offers two choices:
        *   **Convert to specific scale**: Asks for target scale, performs conversion, and logs it.
        *   **Convert to all scales**: Converts the source value to Celsius, Fahrenheit, and Kelvin, displaying and logging all results.
    3.  Handles errors like invalid scales or calculation exceptions.

#### `view_history(logger)`
*   **Purpose**: Displays a list of past conversions.
*   **Args**: `logger` instance.
*   **Logic**:
    *   Retrieves history from the logger.
    *   Shows the last 10 entries in reverse order (newest first).
    *   Indicates if there are more entries hidden.

#### `view_statistics(logger)`
*   **Purpose**: Shows a statistical summary of the session/history.
*   **Args**: `logger` instance.
*   **Logic**: Uses the `Report` class to display a summary (total conversions, averages, etc.).

#### `generate_reports(logger)`
*   **Purpose**: Creates persistent report files.
*   **Args**: `logger` instance.
*   **Logic**:
    *   Prompts user to generate a text report ("statistics_report.txt").
    *   Can also display the summary on screen.

#### `create_visualizations(analyzer)`
*   **Purpose**: Interfaces with the `DataAnalyzer` to generate charts.
*   **Args**: `analyzer` instance (from `logger.py`).
*   **Options**:
    1.  Conversion frequency chart
    2.  Temperature distribution chart
    3.  Timeline chart
    4.  All charts

#### `run_demo()`
*   **Purpose**: Runs an automated demonstration of the app's capabilities.
*   **Logic**:
    *   Performs a predefined list of conversions.
    *   Generates stats and saves a report.
    *   Creates all available visualization charts.
    *   Useful for testing or showcasing features quickly.

#### `main()`
*   **Purpose**: The main application loop.
*   **Logic**:
    1.  Initializes `TemperatureConverter`, `ConversionLogger`, and `DataAnalyzer`.
    2.  Loads existing history from the CSV file into the logger (to persist state across runs).
    3.  Checks for a `--demo` command-line argument to run `run_demo()`.
    4.  Enters a `while True` loop to display the menu and process user choices until "Exit" is selected.

---

## 2. `converter_class.py`

This file contains the business logic for conversions, input validation, and managing the history log.

### Decorator

#### `conversion_confirmation(func)`
*   **Purpose**: A decorator that wraps conversion methods.
*   **Effect**: Prints a confirmation message (e.g., "✓ Conversion confirmed...") after a successful conversion.

### Classes

#### `ValidationHandler`
*   **Purpose**: Static utility class for validating temperature inputs.
*   **Constants**:
    *   `MIN_TEMP_C`: -273.15 (Absolute Zero)
    *   `MAX_TEMP_C`: 1,000,000 (Arbitrary upper safety limit)
*   **Method**:
    *   `validate_temperature(value, scale)`: Checks if the value is a number, if the scale is valid (C/F/K), and if the temperature is within the realistic range (converting to Celsius internally for the check).

#### `TemperatureConverter`
*   **Purpose**: Performs the actual mathematical conversions.
*   **Lambdas**: Defines static lambda functions for all pair conversions (e.g., `celsius_to_fahrenheit`, `kelvin_to_celsius`).
*   **Methods**:
    *   `convert(value, from_scale, to_scale)`:
        *   Decorated with `@conversion_confirmation`.
        *   Uses a dictionary `conversion_map` to look up the correct lambda function.
        *   Returns the converted value rounded to 2 decimal places.
    *   `convert_to_all(value, from_scale)`:
        *   Iterates through all supported scales and converts the source value to every other scale.
        *   Returns a dictionary of results.

#### `ConversionLogger`
*   **Purpose**: Manages the storage and retrieval of conversion history.
*   **Attributes**:
    *   `log_file`: Path to the CSV file (default: "conversion_log.csv").
    *   `history`: In-memory list of conversion records.
*   **Methods**:
    *   `__init__`: Initializes the list and ensures the CSV file header exists.
    *   `_initialize_log_file`: Creates the CSV file with headers if it doesn't exist.
    *   `log_conversion(...)`: Adds a new record to `self.history` and appends it to the CSV file. The record includes timestamp, values, scales, and conversion type.
    *   `get_history(limit)`: Returns the history list, optionally sliced by a limit.
    *   `clear_history()`: Clears the in-memory history.

#### `Report`
*   **Purpose**: Generates statistical summaries from the logger data.
*   **Methods**:
    *   `generate_statistics()`: Calculates total conversions, most common conversion type, and average source/target temperatures. Returns a dictionary.
    *   `save_report(filename)`: Writes a formatted text report to a file, including the statistics and a list of recent conversions.
    *   `display_summary()`: Prints the statistics to the console.

---

## 3. `logger.py`

This file handles advanced data analysis and visualization using `pandas` and `matplotlib`.

### Class

#### `DataAnalyzer`
*   **Purpose**: Analyze the CSV log file and create charts.
*   **Attributes**:`df` (Pandas DataFrame) to hold the loaded data.
*   **Methods**:
    *   `load_data()`: Reads "conversion_log.csv" into a Pandas DataFrame.
    *   `get_dataframe()`: Returns the dataframe, loading it if necessary.
    *   `analyze_conversion_frequency()`: Returns a count of each unique `Conversion_Type`.
    *   `analyze_temperature_distribution(scale)`: Calculates statistics (mean, median, std, min, max) for a specific temperature scale.
    *   `create_frequency_chart(output_file)`: Generates a bar chart of conversion frequencies and saves it as a PNG image.
    *   `create_temperature_distribution_chart(output_file)`: Generates a set of 3 histograms (one for each scale) to show the distribution of input temperatures.
    *   `create_timeline_chart(output_file)`: Plots the number of conversions over time (a line chart).
    *   `display_data_summary()`: Prints a comprehensive textual summary of the dataset to the console, including frequency counts and distribution stats for each scale.

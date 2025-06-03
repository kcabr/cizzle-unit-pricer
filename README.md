# Unit Cost Calculator

A desktop application for comparing unit costs of products across different stores to help you find the best deals when shopping.

## What It Does

The Unit Cost Calculator helps you make informed shopping decisions by:

- **Comparing unit prices** across different package sizes and stores
- **Supporting both dry and liquid measurements** with automatic unit conversions
- **Highlighting the best deals** in an easy-to-read comparison table
- **Saving and loading sessions** so you can revisit comparisons later
- **Auto-saving changes** to prevent data loss

### Supported Units

**Dry Products (weight-based):**

- Grams (g), Ounces (oz), Pounds (lb), Kilograms (kg)
- Results shown as cost per gram and cost per ounce

**Liquid Products (volume-based):**

- Milliliters (ml), Fluid Ounces (fl oz), Liters (L), Cups, Pints, Quarts, Gallons
- Results shown as cost per ml, cost per fl oz, and cost per liter

## Features

- ✅ **Multi-store comparison** - Compare prices from Aldi, Amazon, Target, Walmart, and other stores
- ✅ **Unit conversion** - Automatically converts between different measurement units
- ✅ **Session management** - Save/load comparison sessions as XML files
- ✅ **Auto-save** - Automatically saves changes to prevent data loss
- ✅ **Best value highlighting** - The best deal is highlighted in green
- ✅ **Product URLs** - Store product URLs for easy reference
- ✅ **Keyboard shortcuts** - Ctrl+N (new), Ctrl+O (open), Ctrl+S (save)

## Setup Instructions

### Requirements

- Python 3.9 or higher
- tkinter (usually included with Python)

### Installation

1. **Clone or download this repository**

   ```bash
   git clone <repository-url>
   cd unit-cost-calculator
   ```

2. **Ensure Python is installed**

   ```bash
   python --version
   ```

   If Python is not installed, download it from [python.org](https://python.org)

3. **Run the application**
   ```bash
   python main.py
   ```

### Usage

1. **Start a new session** and select product type (Dry or Liquid)
2. **Add products** by clicking "+ Add Product"
3. **Enter product details:**
   - Product name
   - Store
   - Price
   - Quantity and unit
   - Optional: Product URL for reference
4. **Click "Calculate & Compare"** to see results
5. **Save your session** using File → Save Session for later reference

### Session Files

- Sessions are saved as XML files that can be shared or backed up
- The application automatically loads your last session when started
- Auto-save keeps your work safe as you make changes

## Example Use Case

Compare breakfast cereal prices:

- Store A: $4.99 for 18 oz box
- Store B: $3.79 for 12 oz box
- Store C: $6.49 for 24 oz box

The calculator will show you the cost per ounce for each, helping you identify that Store C actually offers the best value despite the higher upfront cost.

## File Structure

- `main.py` - Main application file
- `README.md` - This file
- Session files (`.xml`) - Saved comparison sessions

## Contributing

Feel free to submit issues or pull requests to improve the application.

## License

This project is open source. See the license file for details.

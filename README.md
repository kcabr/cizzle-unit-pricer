# 🧮 Unit Cost Calculator 💰

```
    ╔═══════════════════════════════════════╗
    ║        💸 FIND THE BEST DEALS! 💸     ║
    ║                                       ║
    ║  🏪 Store A: $4.99 / 18oz = $0.277   ║
    ║  🏪 Store B: $3.79 / 12oz = $0.316   ║
    ║  🏪 Store C: $6.49 / 24oz = $0.270 ⭐ ║
    ║                                       ║
    ║        ✨ Store C is the winner! ✨   ║
    ╚═══════════════════════════════════════╝
```

A desktop application for comparing unit costs of products across different stores to help you find the best deals when shopping.

## 🎯 What It Does

The Unit Cost Calculator helps you make informed shopping decisions by:

- 🔍 **Comparing unit prices** across different package sizes and stores
- ⚖️ **Supporting both dry and liquid measurements** with automatic unit conversions
- 🌟 **Highlighting the best deals** in an easy-to-read comparison table
- 💾 **Saving and loading sessions** so you can revisit comparisons later
- 🔄 **Auto-saving changes** to prevent data loss
- 📋 **Live calculations** - results update as you type!

### 📏 Supported Units

**🥫 Dry Products (weight-based):**

```
g ←→ oz ←→ lb ←→ kg
📦 Results: cost per gram & cost per ounce
```

**🥤 Liquid Products (volume-based):**

```
ml ←→ fl oz ←→ L ←→ cups ←→ pints ←→ quarts ←→ gallons
🧴 Results: cost per ml, fl oz, & liter
```

## ✨ Features

- 🏬 **Multi-store comparison** - Compare prices from Aldi, Amazon, Target, Walmart, and other stores
- 🔄 **Unit conversion** - Automatically converts between different measurement units
- 💾 **Session management** - Save/load comparison sessions as XML files
- 💿 **Auto-save** - Automatically saves changes to prevent data loss
- 🥇 **Best value highlighting** - The best deal is highlighted in green
- 🔗 **Product URLs** - Store product URLs for easy reference
- ⌨️ **Keyboard shortcuts** - Ctrl+N (new), Ctrl+O (open), Ctrl+S (save)
- 📋 **Click-to-copy** - Click any price to copy it to clipboard
- ⚡ **Live updates** - Results calculate automatically as you type

## 🚀 Setup Instructions

### 📋 Requirements

- 🐍 Python 3.9 or higher
- 🖼️ tkinter (usually included with Python)
- 📄 PyYAML (optional, for better config file format - will fallback to JSON if not available)

### 🛠️ Installation

1. **📥 Clone or download this repository**

   ```bash
   git clone <repository-url>
   cd unit-cost-calculator
   ```

2. **🔍 Ensure Python is installed**

   ```bash
   python --version
   ```

   If Python is not installed, download it from [python.org](https://python.org)

3. **📦 Install PyYAML (optional, for better config files)**

   ```bash
   pip install PyYAML
   ```

   If not installed, the app will use JSON format for config files instead.

4. **🎮 Run the application**
   ```bash
   python main.py
   ```

### 🎯 Usage

```
Step 1: 🆕 Start → Select product type (Dry/Liquid)
   ↓
Step 2: ➕ Add products → Enter details
   ↓
Step 3: ⚡ Watch → Results update live!
   ↓
Step 4: 💾 Save → Keep your comparison
```

1. **🆕 Start a new session** and select product type (Dry or Liquid)
2. **➕ Add products** by clicking "+ Add Product"
3. **📝 Enter product details:**
   - 🏷️ Product name
   - 🏪 Store
   - 💰 Price
   - 📦 Quantity and unit
   - 🔗 Optional: Product URL for reference
4. **👀 Watch results update live** as you type!
5. **💾 Save your session** using File → Save Session for later reference

### 💾 Session Files

- 📄 Sessions are saved as XML files that can be shared or backed up
- 🔄 The application automatically loads your last session when started
- 💿 Auto-save keeps your work safe as you make changes

## 🥣 Example Use Case

**🌾 Compare breakfast cereal prices:**

```
┌─────────────────────────────────────────────────────┐
│  🏪 STORE COMPARISON - Breakfast Cereal             │
├─────────────────────────────────────────────────────┤
│  🅰️  Store A: $4.99 for 18 oz → $0.277/oz         │
│  🅱️  Store B: $3.79 for 12 oz → $0.316/oz         │
│  🅲  Store C: $6.49 for 24 oz → $0.270/oz ⭐ BEST  │
└─────────────────────────────────────────────────────┘
```

The calculator reveals that **Store C** offers the best value at **$0.270 per ounce**, even though it has the highest upfront cost!

💡 **Pro tip:** Sometimes buying the bigger, more expensive package saves you money per unit!

## 📁 File Structure

```
unit-cost-calculator/
├── 🐍 main.py                    # Main application file
├── 📖 README.md                  # This file
├── 🏠 ~/.unit_cost_calculator_config.yaml  # Config file
└── 📁 Sessions/
    ├── 🥣 cereal_comparison.xml
    ├── 🧴 shampoo_deals.xml
    └── 🍎 grocery_list.xml
```

## 🤝 Contributing

Feel free to submit issues or pull requests to improve the application!

```
     🐛 Found a bug?     →  📝 Open an issue
     💡 Have an idea?    →  🚀 Submit a PR
     ❤️ Love the app?    →  ⭐ Star the repo
```

## 📜 License

This project is open source. See the license file for details.

---

```
Made with ❤️ for smart shoppers everywhere! 🛒✨
```

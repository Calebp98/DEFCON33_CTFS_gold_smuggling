# DEFCON33 CTF - Gold Smuggling Network Analysis

This project contains analysis tools for investigating the "Jack Colton" emerald smuggling case from DEFCON33 CTF.

## Files

- **`index.html`** - Interactive web-based network visualization tool
- **`smuggling_analysis.py`** - Python script for network analysis and static visualization  
- **`smuggling_network.png`** - Generated network diagram

## Key Findings

### Smuggling Path Discovered
1. **AXAD**: Emerald added at Customs Outpost (2.5oz → 2.6oz weight discrepancy)
2. **AFAF**: Emerald transferred to hollow pendant at Transit Hub
3. **XFGA**: Final delivery from Port to Zolo's Camp hidden in coffee beans

### Critical Evidence
- **Weight Discrepancy**: AXAD shipment shows 2.6oz actual vs 2.5oz documented (+0.1oz emerald)
- **Transfer Container**: AFAF hollow pendant (0.5oz) - perfect for concealing small emerald
- **Single Port Route**: Only 1 shipment FROM Port (coffee to Zolo's Camp)

## Usage

### Interactive Visualization
```bash
open index.html
```
Features:
- Network graph with weighted edges
- Highlight suspicious routes and items
- Filter by weight categories
- Detailed tooltips with shipment info

### Python Analysis
```bash
python smuggling_analysis.py
```
Generates:
- Network statistics
- Route analysis (from/to Port)
- Suspicious item identification
- Weight pattern analysis

## Investigation Summary

**Jack Colton** orchestrated a sophisticated emerald smuggling operation using the shipping network. The emerald was:
1. Planted in a carved box at Customs Outpost
2. Transferred to a hollow pendant at Transit Hub  
3. Delivered to Port for Jack Colton to retrieve
4. Hidden in coffee beans for final transport to Zolo's Camp

The weight discrepancy in shipment AXAD and the hollow pendant AFAF provide concrete evidence of the smuggling method.
# Multi LoRA Stack for ComfyUI

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![ComfyUI](https://img.shields.io/badge/ComfyUI-Compatible-green.svg)](https://github.com/comfyanonymous/ComfyUI)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)

> **Powerful standalone ComfyUI custom nodes for managing multiple LoRAs in a single, dynamic interface**

A complete replacement for rgthree's Power Lora Loader with **zero dependencies** and **two specialized versions** to fit any workflow.

## ✨ Features

🎛️ **Dynamic Interface** - Add unlimited LoRA slots with a single click  
🔄 **Easy Management** - Toggle, reorder, and remove LoRAs with intuitive controls  
💪 **Dual Versions** - Choose between full functionality or model-only optimization  
📊 **Visual Feedback** - Clean, wide interface with clear status indicators  
⚡ **Performance** - Efficient loading and processing of multiple LoRAs  
🔧 **No Dependencies** - Standalone implementation, works with any ComfyUI installation  

## 🚀 Quick Start

### Installation

1. **Clone or download** this repository to your ComfyUI custom nodes directory:
   ```bash
   cd ComfyUI/custom_nodes/
   git clone https://github.com/ShmuelRonen/multi-lora-stack.git
   ```

2. **Restart ComfyUI**

3. **Find the nodes** in the `loaders` category:
   - **Multi LoRA Stack** - Full version with MODEL + CLIP
   - **Multi LoRA Stack (Model Only)** - Streamlined model-only version

### Basic Usage

1. Add either node to your workflow
2. Connect your base MODEL (and CLIP for full version)
3. Click **"➕ Add LoRA"** to add LoRA slots
4. Select LoRAs from the dropdown menus
5. Adjust strength values as needed
6. Toggle individual LoRAs on/off or use **"Toggle All"**

## 📊 Node Versions

| Feature | **Multi LoRA Stack** | **Multi LoRA Stack (Model Only)** |
|---------|---------------------|----------------------------------|
| **Inputs** | MODEL + CLIP | MODEL only |
| **Outputs** | MODEL + CLIP | MODEL only |
| **Best For** | Style LoRAs, Character LoRAs, Complex workflows | Flux LoRAs, Performance-focused workflows |
| **Interface** | 4 connection points | 2 connection points |
| **Performance** | Standard | Optimized |

### When to Use Which?

**Choose Multi LoRA Stack (Full):**
- Working with style or character LoRAs
- Need CLIP text encoding modifications
- Maximum compatibility with existing workflows
- Professional/production work

**Choose Multi LoRA Stack (Model Only):**
- Using modern LoRAs (especially Flux)
- Performance-critical workflows
- Prefer cleaner, simpler interface
- Experimental/testing workflows


## 🎛️ Controls

### Main Controls
- **➕ Add LoRA** - Adds a new LoRA slot
- **Toggle All LoRAs** - Enables/disables all LoRAs at once

### Per-LoRA Controls
- **Enable Toggle** - Turn individual LoRAs on/off
- **LoRA Dropdown** - Select from available LoRAs
- **Strength Slider** - Adjust influence (-2.0 to +2.0)
- **Remove Button** - Delete the LoRA slot

## 📝 Technical Details

### File Structure
```
multi-lora-stack/
├── __init__.py                          # Node registration
├── multi_lora_stack.py                  # Full version backend
├── multi_lora_stack_model_only.py       # Model-only backend
└── web/
    ├── multi_lora_stack.js              # Full version UI
    └── multi_lora_stack_model_only.js   # Model-only UI
```

### Data Format
LoRA configurations are stored as JSON:
```json
[
  {
    "on": true,
    "lora": "flux/style_lora.safetensors",
    "strength": 1.0
  },
  {
    "on": false,
    "lora": "character_lora.safetensors", 
    "strength": 0.8
  }
]
```

### Backend Processing
- **Full Version**: Uses ComfyUI's `LoraLoader()` for MODEL + CLIP processing
- **Model Only**: Uses ComfyUI's `LoraLoaderModelOnly()` for optimized model-only processing

## 🔧 Installation Details

### Method 1: Git Clone (Recommended)
```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/yourusername/multi-lora-stack.git
```

### Method 2: Manual Download
1. Download the repository as ZIP
2. Extract to `ComfyUI/custom_nodes/multi-lora-stack/`
3. Ensure the file structure matches the layout above

### Method 3: Individual Files
Create the directory structure and copy files:
```bash
mkdir -p ComfyUI/custom_nodes/multi-lora-stack/web/
# Copy each file to its respective location
```

## 🐛 Troubleshooting

### Nodes Don't Appear
- ✅ Verify file structure matches exactly
- ✅ Check ComfyUI console for error messages  
- ✅ Restart ComfyUI completely
- ✅ Ensure all Python files are in the root directory

### LoRA Dropdown Empty
- ✅ Verify LoRAs exist in `models/loras/` directory
- ✅ Test with ComfyUI's standard LoRA Loader first
- ✅ Check file permissions

### JavaScript Errors
- ✅ Ensure JS files are in the `web/` subdirectory
- ✅ Check browser console (F12) for specific errors
- ✅ Clear browser cache and reload

### LoRAs Not Loading
- ✅ Check ComfyUI console for debug output
- ✅ Verify LoRA names match exactly with files
- ✅ Ensure LoRAs are enabled (toggle on)
- ✅ Test strength values (non-zero)

## 🆚 Comparison with rgthree Power Lora Loader

| Feature | **Multi LoRA Stack** | **rgthree Power Lora Loader** |
|---------|---------------------|-------------------------------|
| **Dependencies** | ✅ None (standalone) | ❌ Requires rgthree framework |
| **Installation** | ✅ Simple (drop-in) | ❌ Complex (dependencies) |
| **Versions** | ✅ Two optimized versions | ⚪ Single version |
| **Compatibility** | ✅ Any ComfyUI installation | ❌ Requires rgthree ecosystem |
| **Updates** | ✅ Independent updates | ❌ Dependent on rgthree updates |
| **Interface** | ✅ Wide, clean design | ⚪ Compact design |

## 🤝 Contributing

Contributions are welcome! Please:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup
```bash
# Clone the repo
git clone https://github.com/ShmuelRonen/multi-lora-stack.git
cd multi-lora-stack

# Make changes and test in ComfyUI
# Follow the installation instructions above for testing
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by rgthree's Power Lora Loader
- Built for the ComfyUI community
- Thanks to all contributors and testers

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/multi-lora-stack/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/multi-lora-stack/discussions)
- **ComfyUI**: [ComfyUI Repository](https://github.com/comfyanonymous/ComfyUI)

---

**⭐ If this project helps your workflow, please give it a star!**

Made with ❤️ for the ComfyUI community

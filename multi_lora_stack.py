from nodes import LoraLoader

class MultiLoRAStack:
    """A powerful node to load multiple LoRAs with individual controls."""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "clip": ("CLIP",),
                "lora_stack": ("STRING", {
                    "multiline": True, 
                    "default": "[]",
                    "forceInput": False
                }),
            },
            "optional": {},
        }

    RETURN_TYPES = ("MODEL", "CLIP")
    RETURN_NAMES = ("MODEL", "CLIP") 
    FUNCTION = "load_loras"
    CATEGORY = "loaders"

    def load_loras(self, model, clip, lora_stack="[]", **kwargs):
        """Loads multiple LoRAs based on the configuration."""
        import json
        
        # Debug output
        print(f"\n=== MultiLoRAStack Debug ===")
        print(f"Received lora_stack: {lora_stack}")
        print(f"Received kwargs: {list(kwargs.keys())}")
        
        # Parse lora_stack if it's a string
        lora_configs = []
        if isinstance(lora_stack, str):
            try:
                lora_configs = json.loads(lora_stack)
                print(f"✅ Parsed {len(lora_configs)} LoRA configs from JSON")
                for i, config in enumerate(lora_configs):
                    print(f"  Config {i}: {config}")
            except Exception as e:
                print(f"❌ Failed to parse JSON: {e}")
                lora_configs = []
        else:
            lora_configs = lora_stack if isinstance(lora_stack, list) else []
        
        # Also check kwargs for lora configurations (for backward compatibility)
        for key, value in kwargs.items():
            if key.upper().startswith('LORA_') and isinstance(value, dict):
                if 'on' in value and 'lora' in value and 'strength' in value:
                    lora_configs.append(value)
                    print(f"➕ Added LoRA config from kwargs: {key}")
        
        applied_count = 0
        
        # Process each LoRA configuration
        for i, config in enumerate(lora_configs):
            print(f"\n--- Processing LoRA {i+1} ---")
            
            if not isinstance(config, dict):
                print(f"❌ Skipping invalid config at index {i}: {config}")
                continue
                
            # Check if this LoRA should be applied
            if not config.get('on', False):
                print(f"⏸️ Skipping disabled LoRA: {config.get('lora', 'Unknown')}")
                continue
                
            lora_name = config.get('lora')
            if not lora_name or lora_name == "None":
                print(f"❌ Skipping empty/None LoRA")
                continue
                
            strength_model = float(config.get('strength', 1.0))
            strength_clip = float(config.get('strengthTwo', strength_model))
            
            # Skip if both strengths are 0
            if strength_model == 0 and strength_clip == 0:
                print(f"⏸️ Skipping zero-strength LoRA: {lora_name}")
                continue
            
            print(f"🔄 Attempting to load LoRA:")
            print(f"   Name: {lora_name}")
            print(f"   Model Strength: {strength_model}")
            print(f"   Clip Strength: {strength_clip}")
            
            # Apply the LoRA using ComfyUI's standard loader
            try:
                # Create a new LoraLoader instance
                lora_loader = LoraLoader()
                
                # Apply the LoRA
                model, clip = lora_loader.load_lora(model, clip, lora_name, strength_model, strength_clip)
                applied_count += 1
                print(f"✅ Successfully applied LoRA: {lora_name}")
                
            except Exception as e:
                print(f"❌ Failed to load LoRA '{lora_name}': {str(e)}")
                print(f"   Error type: {type(e).__name__}")
                import traceback
                print(f"   Full traceback: {traceback.format_exc()}")
        
        print(f"\n=== Summary ===")
        print(f"Applied {applied_count} out of {len(lora_configs)} LoRAs")
        print(f"===================\n")
        
        return (model, clip)

# Register the node
NODE_CLASS_MAPPINGS = {
    "MultiLoRAStack": MultiLoRAStack
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiLoRAStack": "Multi LoRA Stack"
}
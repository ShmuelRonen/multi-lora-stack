from nodes import LoraLoader, LoraLoaderModelOnly

class MultiLoRAStack:
    """A powerful node to load multiple LoRAs with individual controls."""
    
    def __init__(self):
        # Use a single instance for caching benefits
        self.lora_loader = LoraLoader()
    
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
                return (model, clip)
        else:
            lora_configs = lora_stack if isinstance(lora_stack, list) else []
        
        applied_count = 0
        current_model = model
        current_clip = clip
        
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
                # Apply the LoRA to current model and clip
                current_model, current_clip = self.lora_loader.load_lora(
                    current_model, current_clip, lora_name, strength_model, strength_clip
                )
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
        
        return (current_model, current_clip)


class MultiLoRAStackModelOnly:
    """A powerful node to load multiple LoRAs with individual controls (Model Only)."""
    
    def __init__(self):
        # Use a single instance for caching benefits
        self.lora_loader = LoraLoaderModelOnly()
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "lora_stack": ("STRING", {
                    "multiline": True, 
                    "default": "[]",
                    "forceInput": False
                }),
            },
            "optional": {},
        }

    RETURN_TYPES = ("MODEL",)
    RETURN_NAMES = ("MODEL",) 
    FUNCTION = "load_loras"
    CATEGORY = "loaders"

    def load_loras(self, model, lora_stack="[]", **kwargs):
        """Loads multiple LoRAs based on the configuration (Model Only)."""
        import json
        
        # Debug output
        print(f"\n=== MultiLoRAStackModelOnly Debug ===")
        print(f"Received lora_stack: {lora_stack}")
        
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
                return (model,)
        else:
            lora_configs = lora_stack if isinstance(lora_stack, list) else []
        
        applied_count = 0
        current_model = model
        
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
            
            # Skip if strength is 0
            if strength_model == 0:
                print(f"⏸️ Skipping zero-strength LoRA: {lora_name}")
                continue
            
            print(f"🔄 Attempting to load LoRA (Model Only):")
            print(f"   Name: {lora_name}")
            print(f"   Model Strength: {strength_model}")
            
            # Apply the LoRA using ComfyUI's model-only loader
            try:
                # FIXED: Use the correct method name
                current_model, = self.lora_loader.load_lora_model_only(
                    current_model, lora_name, strength_model
                )
                applied_count += 1
                print(f"✅ Successfully applied LoRA (Model Only): {lora_name}")
                
            except Exception as e:
                print(f"❌ Failed to load LoRA '{lora_name}': {str(e)}")
                print(f"   Error type: {type(e).__name__}")
                import traceback
                print(f"   Full traceback: {traceback.format_exc()}")
        
        print(f"\n=== Summary ===")
        print(f"Applied {applied_count} out of {len(lora_configs)} LoRAs (Model Only)")
        print(f"===================\n")
        
        return (current_model,)


# Register the nodes
NODE_CLASS_MAPPINGS = {
    "MultiLoRAStack": MultiLoRAStack,
    "MultiLoRAStackModelOnly": MultiLoRAStackModelOnly
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MultiLoRAStack": "Multi LoRA Stack",
    "MultiLoRAStackModelOnly": "Multi LoRA Stack (Model Only)"
}
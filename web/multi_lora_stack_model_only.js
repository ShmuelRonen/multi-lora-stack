import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

// Get available LoRAs from the API
async function getAvailableLoras() {
    try {
        const response = await api.fetchApi("/object_info");
        const objectInfo = await response.json();
        
        // Look for LoRA inputs in any loader node
        for (const [nodeName, nodeInfo] of Object.entries(objectInfo)) {
            if (nodeInfo.input?.required?.lora_name) {
                return nodeInfo.input.required.lora_name[0] || ["None"];
            }
        }
        return ["None"];
    } catch (error) {
        console.error("Error fetching LoRAs:", error);
        return ["None"];
    }
}

app.registerExtension({
    name: "MultiLoRAStackModelOnly",
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "MultiLoRAStackModelOnly") {
            console.log("Registering MultiLoRAStackModelOnly node");
            
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = async function () {
                console.log("MultiLoRAStackModelOnly node created");
                
                const result = onNodeCreated?.apply(this, arguments);
                
                // Set wider default size
                this.size = [450, 300];
                
                // Initialize node data
                this.loraData = [];
                this.availableLoras = await getAvailableLoras();
                
                // Add control buttons
                this.addWidget("button", "➕ Add LoRA", null, () => {
                    this.addLoRA();
                });
                
                this.addWidget("button", "Toggle All LoRAs", null, () => {
                    this.toggleAllLoRAs();
                });
                
                // Add initial LoRA
                this.addLoRA();
                
                return result;
            };
            
            // Add methods to the node prototype
            nodeType.prototype.addLoRA = function() {
                const index = this.loraData.length;
                console.log(`Adding LoRA ${index + 1} (Model Only)`);
                
                // Add LoRA data
                this.loraData.push({
                    on: true,
                    lora: "None",
                    strength: 1.0
                });
                
                // Create widgets for this LoRA
                const enableWidget = this.addWidget("toggle", `Enable LoRA ${index + 1}`, true, (value) => {
                    this.loraData[index].on = value;
                    this.updateLoraStack();
                });
                
                const loraWidget = this.addWidget("combo", `LoRA ${index + 1}`, "None", (value) => {
                    this.loraData[index].lora = value;
                    this.updateLoraStack();
                }, {
                    values: this.availableLoras
                });
                
                const strengthWidget = this.addWidget("number", `Strength ${index + 1}`, 1.0, (value) => {
                    this.loraData[index].strength = value;
                    this.updateLoraStack();
                }, {
                    min: -2.0,
                    max: 2.0,
                    step: 0.1
                });
                
                const removeWidget = this.addWidget("button", `Remove LoRA ${index + 1}`, null, () => {
                    this.removeLoRA(index);
                });
                
                // Store widget references
                this.loraData[index]._widgets = {
                    enable: enableWidget,
                    lora: loraWidget,
                    strength: strengthWidget,
                    remove: removeWidget
                };
                
                this.updateLoraStack();
                this.setSize([this.size[0], this.computeSize()[1]]);
            };
            
            nodeType.prototype.removeLoRA = function(index) {
                console.log(`Removing LoRA ${index + 1} (Model Only)`);
                
                // Get widgets to remove
                const loraItem = this.loraData[index];
                if (loraItem && loraItem._widgets) {
                    // Remove widgets from the node
                    Object.values(loraItem._widgets).forEach(widget => {
                        const widgetIndex = this.widgets.indexOf(widget);
                        if (widgetIndex !== -1) {
                            this.widgets.splice(widgetIndex, 1);
                        }
                    });
                }
                
                // Remove from data array
                this.loraData.splice(index, 1);
                
                // Update remaining widget names and indices
                this.updateWidgetNames();
                this.updateLoraStack();
                this.setSize([this.size[0], this.computeSize()[1]]);
            };
            
            nodeType.prototype.updateWidgetNames = function() {
                // Update widget names after removal
                this.loraData.forEach((loraItem, index) => {
                    if (loraItem._widgets) {
                        loraItem._widgets.enable.name = `Enable LoRA ${index + 1}`;
                        loraItem._widgets.lora.name = `LoRA ${index + 1}`;
                        loraItem._widgets.strength.name = `Strength ${index + 1}`;
                        loraItem._widgets.remove.name = `Remove LoRA ${index + 1}`;
                    }
                });
            };
            
            nodeType.prototype.toggleAllLoRAs = function() {
                const allEnabled = this.loraData.every(lora => lora.on);
                const newState = !allEnabled;
                
                console.log(`Toggling all LoRAs to: ${newState} (Model Only)`);
                
                this.loraData.forEach((loraItem, index) => {
                    loraItem.on = newState;
                    if (loraItem._widgets && loraItem._widgets.enable) {
                        loraItem._widgets.enable.value = newState;
                    }
                });
                
                this.updateLoraStack();
            };
            
            nodeType.prototype.updateLoraStack = function() {
                // Find the lora_stack widget
                const stackWidget = this.widgets.find(w => w.name === "lora_stack");
                if (stackWidget) {
                    const jsonData = JSON.stringify(this.loraData.map(item => ({
                        on: item.on,
                        lora: item.lora,
                        strength: item.strength
                    })));
                    stackWidget.value = jsonData;
                    console.log("Updated lora_stack (Model Only):", jsonData);
                } else {
                    console.warn("lora_stack widget not found (Model Only)");
                }
            };

            // Override computeSize to ensure minimum width
            const originalComputeSize = nodeType.prototype.computeSize;
            nodeType.prototype.computeSize = function(out) {
                const size = originalComputeSize ? originalComputeSize.call(this, out) : [300, 200];
                // Ensure minimum width of 450px
                size[0] = Math.max(size[0], 450);
                return size;
            };
        }
    }
});
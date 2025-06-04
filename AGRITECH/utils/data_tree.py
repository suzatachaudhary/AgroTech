class TreeNode:
    def __init__(self, name, data=None):
        self.name = name
        self.data = data  # Optional data (e.g., crop details)
        self.children = {}  # Child nodes

    def add_child(self, name, data=None):
        self.children[name] = TreeNode(name, data)

    def get_child(self, name):
        return self.children.get(name)


# Initialize tree
root = TreeNode("India")

# Add regions
for region in ["North", "South", "East", "West"]:
    root.add_child(region)

# Add states to each region
region_states = {
    "North": ["Punjab", "Haryana", "Himachal Pradesh"],
    "South": ["Karnataka", "Tamil Nadu", "Kerala"],
    "East": ["West Bengal", "Odisha", "Bihar"],
    "West": ["Rajasthan", "Gujarat", "Maharashtra"],
}

for region, states in region_states.items():
    region_node = root.get_child(region)
    for state in states:
        region_node.add_child(state)

# Add crop types and crops for each state
state_crops = {
    "Punjab": {
        "Vegetable": ["Tomato", "Onion", "Cauliflower"],
        "Fruit": ["Guava", "Mango", "Kinnow"],
        "Grain": ["Wheat", "Rice", "Maize"],
    },
    "Haryana": {
        "Vegetable": ["Potato", "Tomato", "Spinach"],
        "Fruit": ["Banana", "Papaya", "Mango"],
        "Grain": ["Wheat", "Bajra", "Rice"],
    },
    "Himachal Pradesh": {
        "Vegetable": ["Carrot", "Cabbage", "Radish"],
        "Fruit": ["Apple", "Plum", "Cherry"],
        "Grain": ["Barley", "Maize", "Wheat"],
    },
    "Karnataka": {
        "Vegetable": ["Brinjal", "Okra", "Pumpkin"],
        "Fruit": ["Pineapple", "Banana", "Guava"],
        "Grain": ["Ragi", "Rice", "Maize"],
    },
    "Tamil Nadu": {
        "Vegetable": ["Onion", "Drumstick", "Tomato"],
        "Fruit": ["Jackfruit", "Banana", "Papaya"],
        "Grain": ["Rice", "Millet", "Maize"],
    },
    "Kerala": {
        "Vegetable": ["Cucumber", "Pumpkin", "Amaranthus"],
        "Fruit": ["Banana", "Pineapple", "Jackfruit"],
        "Grain": ["Rice", "Tapioca", "Maize"],
    },
    "West Bengal": {
        "Vegetable": ["Cabbage", "Cauliflower", "Potato"],
        "Fruit": ["Mango", "Guava", "Litchi"],
        "Grain": ["Rice", "Jute", "Maize"],
    },
    "Odisha": {
        "Vegetable": ["Pumpkin", "Brinjal", "Tomato"],
        "Fruit": ["Coconut", "Mango", "Papaya"],
        "Grain": ["Rice", "Maize", "Millet"],
    },
    "Bihar": {
        "Vegetable": ["Cauliflower", "Cabbage", "Tomato"],
        "Fruit": ["Mango", "Litchi", "Banana"],
        "Grain": ["Rice", "Wheat", "Maize"],
    },
    "Rajasthan": {
        "Vegetable": ["Onion", "Garlic", "Cucumber"],
        "Fruit": ["Ber", "Pomegranate", "Guava"],
        "Grain": ["Wheat", "Bajra", "Barley"],
    },
    "Gujarat": {
        "Vegetable": ["Potato", "Tomato", "Brinjal"],
        "Fruit": ["Mango", "Chiku", "Pomegranate"],
        "Grain": ["Rice", "Wheat", "Jowar"],
    },
    "Maharashtra": {
        "Vegetable": ["Onion", "Chilli", "Tomato"],
        "Fruit": ["Banana", "Grapes", "Mango"],
        "Grain": ["Jowar", "Rice", "Bajra"],
    }

}


for state, crop_data in state_crops.items():
    for region_node in root.children.values():
        state_node = region_node.get_child(state)
        if state_node:
            for crop_type, crops in crop_data.items():
                crop_type_node = TreeNode(crop_type, data=crops)
                state_node.children[crop_type] = crop_type_node


# Utility functions
def get_states_by_region(region):
    region_node = root.get_child(region)
    return list(region_node.children.keys()) if region_node else []


def get_crop_types_by_state(state):
    for region_node in root.children.values():
        state_node = region_node.get_child(state)
        if state_node:
            return list(state_node.children.keys())
    return []


def get_crops_by_type(state, crop_type):
    for region_node in root.children.values():
        state_node = region_node.get_child(state)
        if state_node:
            crop_type_node = state_node.get_child(crop_type)
            return crop_type_node.data if crop_type_node else []
    return []

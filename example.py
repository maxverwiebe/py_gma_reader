from py_gma_reader import AddonReader

file = "C:/Users/summe/OneDrive/Desktop/104607228.gma"

with open(file, "rb") as file:
    reader = AddonReader(file)
    addon = reader.parse_addon()
        
    addon.extract_files("C:/Users/summe/OneDrive/Desktop/myaddon")
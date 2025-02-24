import pickle
import os

def save_best_genome(genome, filename="best_genome.pkl"):
    """Saves the best genome safely."""
    try:
        with open(filename, "wb") as f:
            pickle.dump(genome, f, protocol=pickle.HIGHEST_PROTOCOL)
        print("Best genome saved successfully!")
    except Exception as e:
        print(f"Error saving the best genome: {e}")

def load_best_genome(filename="best_genome.pkl"):
    """Loads the best saved genome, if available."""
    if not os.path.exists(filename):
        print("No saved genome found.")
        return None
    
    try:
        with open(filename, "rb") as f:
            genome = pickle.load(f)
        print("Best genome loaded successfully!")
        return genome
    except Exception as e:
        print(f"Error loading the best genome: {e}")
        return None

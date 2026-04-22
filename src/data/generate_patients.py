import os
import subprocess
import shutil

SYNTHEA_JAR = "tools/synthea.jar"
OUTPUT_DIR = "data/raw/patients"
SYNTHEA_OUTPUT = "output/fhir"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_patients(count=100, state="Massachusetts"):
    print(f"Generating {count} synthetic patients...")
    cmd = ["java", "-jar", SYNTHEA_JAR, "-p", str(count), state]
    subprocess.run(cmd, check=True)

    if os.path.exists(SYNTHEA_OUTPUT):
        files = os.listdir(SYNTHEA_OUTPUT)
        for f in files:
            shutil.move(os.path.join(SYNTHEA_OUTPUT, f), os.path.join(OUTPUT_DIR, f))
        print(f"Moved {len(files)} files to {OUTPUT_DIR}")
    else:
        print("Synthea output not found.")

if __name__ == "__main__":
    generate_patients(count=100)
import sys

sys.path.insert(0, "src")

try:
    print("SUCCESS: PatientCreate imported")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback

    traceback.print_exc()

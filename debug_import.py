import sys

sys.path.insert(0, "src")

try:
    print("SUCCESS: PatientCreate imported")
except ImportError as e:
    print(f"ERROR: {e}")
    import traceback

    traceback.print_exc()

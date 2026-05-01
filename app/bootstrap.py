# app/bootstrap.py
import os
from pathlib import Path
import shutil

def ensure_baseline_bootstrap():
    """
    Ensures the app has an ACTIVE model and metrics on a cold deploy.
    Uses train_from_export.bootstrap_from_specific_csv() if needed.
    """

    # Import here to avoid circular imports
    import train_from_export

    # These paths are already Railway-safe in train_from_export.py
    models_dir = train_from_export.MODELS_DIR
    base_model = train_from_export.BASE_MODEL_PATH
    active_model = train_from_export.ACTIVE_MODEL_PATH
    credit_model = train_from_export.CREDIT_MODEL_PATH
    metrics_path = train_from_export.METRICS_PATH

    # If we already have an active model, nothing to do
    if active_model.exists() and metrics_path.exists():
        print("✅ Bootstrap not needed: active model + metrics already exist.")
        return

    # If credit_model exists, promote it to base/active
    if credit_model.exists():
        if not base_model.exists():
            shutil.copy2(credit_model, base_model)
        if not active_model.exists():
            shutil.copy2(credit_model, active_model)

        print("✅ Bootstrap: promoted credit_model.pkl → base_model.pkl + active_model.pkl")
        return

    # Otherwise train a baseline bundle from the bootstrap CSV
    csv_path = os.getenv("BOOTSTRAP_CSV", str(train_from_export.DATA_DIR / "data_for_training.csv"))
    print(f"⚠️ Bootstrap training required. Using CSV: {csv_path}")

    train_from_export.bootstrap_from_specific_csv(csv_path)
    print("✅ Bootstrap training completed.")

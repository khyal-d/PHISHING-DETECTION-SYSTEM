from .packages import *
from .config import *


def predict_url_features(feature_dict_or_series, artifacts_path="phish_artifacts.pkl"):
    bundle = joblib.load(artifacts_path)
    selected_cols = bundle["selected_cols"]
    scaler       = bundle["scaler"]
    best_model   = bundle["best_model"]
    best_scaled  = bundle["best_scaled"]
    name         = bundle["best_model_name"]
 
    X_new = pd.DataFrame([dict(feature_dict_or_series)])

    X_new = X_new.reindex(columns=selected_cols, fill_value=0)

    if best_scaled:
        X_new_arr = scaler.transform(X_new)
    else:
        X_new_arr = X_new.values

    y_pred = best_model.predict(X_new_arr)[0]

    try:
        y_proba = best_model.predict_proba(X_new_arr)[:, 1][0]
    except Exception:
        y_proba = (best_model.decision_function(X_new_arr)[0]
                   if hasattr(best_model, "decision_function") else np.nan)

    return {
        "model": name,
        "label": y_pred,
        "phishing_probability": float(y_proba) if np.isscalar(y_proba) else np.nan
    }
 
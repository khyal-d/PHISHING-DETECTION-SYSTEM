from utils.packages import *
from utils.config import *
from utils.feature_extractor import *
from utils.predictor import *

# ===============================================================
# CELL 7: Testing the Extractor
# ===============================================================

def get_phishing_results(test_urls):
    results = {}
    if type(test_urls)==str:
        test_urls = [test_urls]
    
    for u in test_urls:
        # print("\nURL:", u)
        features = extract_all_url_structure_features(u)
        features_dict = dict(features)  # convert OrderedDict → normal dict
        # print(f"Extracted {len(features_dict)} features.\n")
        results[u] = features_dict  
    feature_input = results[test_urls[0]]  # features for the first test URL

    new_features = feature_input  # Use the features extracted earlier
    result = predict_url_features(new_features)

    required_result = {
        'label': result['label'],
        'phishing_probability': round(result['phishing_probability'], 2)
    }
    return required_result

if __name__=="__main__":
    test_urls = [
    "http://rgipt.ac.in"
    ]
    res = get_phishing_results(test_urls)
    print(res)
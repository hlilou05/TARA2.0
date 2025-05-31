from flask import Flask, request, jsonify
from your_module import AssetRiskProfile  # or import from M1.py
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend to call API from different port

@app.route("/generate_asset", methods=["POST"])
def generate_asset():
    data = request.get_json()
    
    asset = AssetRiskProfile(
        data["component"],
        data["func"],
        data["assetID"],
        data["assetList"],
        data["assetDesc"]
    )
    
    return jsonify(asset.to_list())

if __name__ == "__main__":
    app.run(port=5000, debug=True)

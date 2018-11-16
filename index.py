from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/getInterpretation", methods=['POST','GET'])
def get_bee():
	result = request.form
	final_rfc_base_file = "adaboost.pickle"
	final_rfc_base_iteration_file = "adaboost.pickle"
	final_rfc_base = pickle.load(open(final_rfc_base_file, "rb"))
	final_rfc_base_iteration = pickle.load(open(final_rfc_base_iteration_file, "rb"))
	instance = np.array([[zip_code_lst.index(int(result['zip'])), subspecies_lst.index(result['subspecies']), result['pollen']]])
	prediction = [ada.predict(instance)[0], rfc.predict(instance)[0], svm.predict(instance)[0]]
	return render_template("result.html", prediction=prediction)
	
if __name__ == '__main__':	
	app.run(debug=True)
	
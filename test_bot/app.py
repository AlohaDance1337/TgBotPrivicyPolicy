from flask import Flask, jsonify,make_response,render_template,send_file,request

import logging
import codecs
import uuid


logging.basicConfig(level=logging.INFO,filename="logsFlask",filemode='w')

app = Flask(__name__, template_folder= 'core/templates/')

@app.route("/create_document/<doc_type>", methods = ['GET','POST'])
def create_document(doc_type):
    document_type = doc_type
    app_name = request.args.get('app_name')
    dev_username = request.args.get('dev_username')
    email = request.args.get('email')

    if document_type == "privacy_policy":
        content = render_template('Privacy_policy_page.html', app = app_name, mail = email, dev_username = dev_username)
    if document_type == "terms_of_use":
        content = render_template('Term_of_Use.html', app = app_name, mail = email, dev_username = dev_username)
    if document_type == None:
        return make_response(jsonify({"error": "Invalid document type"}), 400)
    
    unique_id = uuid.uuid4().hex[:10]
    file_name = f"{unique_id}_{app_name}.html"

    with codecs.open(f"html-files/{file_name}", "w+", "utf-8") as f:
        if  document_type == "privacy_policy":
            f.write(content)
        if document_type == "terms_of_use":
            f.write(content)

    response = jsonify({"url": f"/{file_name.replace(' ', '-')}"})
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/<html_file>',  methods = ['GET','POST'])
def sendFiled(html_file):
    return send_file(path_or_file=f'html-files/{html_file}')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, threaded = True, debug = False)
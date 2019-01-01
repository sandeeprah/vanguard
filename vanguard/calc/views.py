import os
import json
import tempfile
import pdfkit
from collections import OrderedDict
from pathlib import Path
from flask import request, render_template, jsonify, abort, current_app, make_response
from vanguard import app
from techlib.schemautils import sDocPrj
from techlib.genutils import load_class, load_function, change_date_format

@app.route('/calculations/')
def calc_index():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    calc_index_html_path = os.path.join('root', 'index.html')
    return render_template(calc_index_html_path)


@app.route('/calculations/<path:calc_index_path>/')
def calc_category_index(calc_index_path):
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    calc_index_path = os.path.sep.join(calc_index_path.strip('/').split('/'))
    calc_index_html_path = os.path.join('root', calc_index_path, 'index.html')
    try:
        return render_template(calc_index_html_path)
    except Exception as e:
        return "Invalid Path"

@app.route('/htm/calculate/<path:calc_path>', methods=['GET', 'POST'])
def htm_calculate(calc_path):
    try:
        if (request.method=='GET'):
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            calc_path = os.path.sep.join(calc_path.strip('/').split('/'))
            doc_json_path = os.path.join(curr_dir, 'root', calc_path, 'doc.json')
            doc = json.load(open(doc_json_path), object_pairs_hook=OrderedDict)
            doc_string = json.dumps(doc, indent=4)
            doc_html_path = os.path.join('root', calc_path, 'doc.html')
        else:
            doc_file = request.files['doc']
            docRaw = json.loads(doc_file.read().decode('utf-8'))
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            calc_path = os.path.sep.join(calc_path.strip('/').split('/'))
            schema_path = os.path.join(curr_dir, 'root', calc_path, 'schema.py')
            macro_path = os.path.join(curr_dir, 'root', calc_path, 'macro.py')
            docSchema = load_class(schema_path, 'docSchema')
            docParsed = docSchema.load(docRaw)
            if (len(docParsed.errors) > 0):
                response = {}
                response['message'] = "Document Contains Errors"
                response["schemaErrors"] = docParsed.errors
                return json_response(response), 400

            calculate = load_function(macro_path, 'calculate')
            doc = docParsed.data
            calculate(doc)
            doc_string = json.dumps(doc, indent=4)
            doc_html_path = os.path.join('root', calc_path, 'doc.html')
        return render_template(doc_html_path, doc=doc_string)
    except Exception as e:
        print(str(e))
        return "Failure in loading the calculation from path"



@app.route('/api/calculate/<path:calc_path>', methods=['GET','POST'])
def api_calculate(calc_path):
    try:
        if (request.method=='GET'):
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            doc_json_path = os.path.join(curr_dir, 'root', calc_path, 'doc.json')
            doc = json.load(open(doc_json_path), object_pairs_hook=OrderedDict)
            response = doc
        else:
            req = request.get_json()
            docRaw = req['doc']
            curr_dir = os.path.dirname(os.path.abspath(__file__))
            calc_path = os.path.sep.join(calc_path.strip('/').split('/'))
            schema_path = os.path.join(curr_dir, 'root', calc_path, 'schema.py')
            macro_path = os.path.join(curr_dir, 'root', calc_path, 'macro.py')
            docSchema = load_class(schema_path, 'docSchema')
            docParsed = docSchema.load(docRaw)
            if (len(docParsed.errors) > 0):
                response = {}
                response['message'] = "Document Contains Errors"
                response["schemaErrors"] = docParsed.errors
                return json_response(response), 400

            calculate = load_function(macro_path, 'calculate')
            doc = docParsed.data
            calculate(doc)
            response= doc
        return json_response(response)
    except Exception as e:
        print(str(e))
        response = {}
        response["message"] = "Error occcured"
        response["error_text"] = str(e)
        return json_response(response), 400


def json_response(input):
    str_response = json.dumps(input, indent=4)
    return current_app.response_class(str_response, mimetype='application/json')



@app.route('/pdf/calculate/<path:calc_path>', methods=['POST'])
def convert_pdf(calc_path):
    response = {}
    options = {}
    options['header-html'] ='dummy'
    try:
        req = request.get_json()
        if ('doc' not in req):
            errors['message'] = "'resource' missing in request"
            return json_response(errors), 400
        print ("received document for pdf conversion")
        docRaw = req['doc']
        basicSchema = sDocPrj()
        docParsed = basicSchema.load(docRaw)
        if (len(docParsed.errors) > 0):
            response["message"] = "The Document Meta Information has errors"
            response["schemaErrors"] = docParsed.errors
            return json_response(errors), 400

        doc = docParsed.data
        doc_string = json.dumps(doc, indent=4)
        project_no= doc['meta']['project_no']
        project_title= doc['meta']['project_title']
        docClass_code = doc['meta']['docClass_code']
        title = doc["meta"]["docInstance_title"]
        doc_no = doc['meta']['doc_no']
        rev = doc['meta']['rev']
        date = doc['meta']['date']

        curr_dir = os.path.dirname(os.path.abspath(__file__))
        calc_path = os.path.sep.join(calc_path.strip('/').split('/'))
        doc_html_path = os.path.join('root', calc_path, 'doc.html')
        main_content = render_template(doc_html_path, doc=doc_string)

        options = {
            'page-size' : 'A4',
            'margin-top':'25mm',
            'margin-bottom':'19mm',
            'margin-left':'19mm',
            'margin-right':'19mm',
            'encoding':'UTF-8',
            'print-media-type' : None,
    #            'header-left' : 'My Static Header',
            'header-line' : None,
            'header-font-size' : '8',
            'header-font-name' : 'Calibri',
            'header-spacing' : '5',
            'footer-left' : "www.codecalculation.com",
            'footer-line' : None,
            'footer-font-size' : '8',
            'footer-font-name' : 'Calibri',
            'footer-spacing' : '5',
            'disable-smart-shrinking' : None,
            'no-stop-slow-scripts' : None,
            'javascript-delay': 300,
            'enable-javascript': None,
            'debug-javascript': None,
            '--encoding': "utf-8",
            'header-html':''
        }

        user_home_dir = str(Path.home())
        wkhtmltopdf_path = os.path.join(user_home_dir, 'wkhtmltox/bin/wkhtmltopdf')
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        this_folderpath = os.path.dirname(os.path.abspath(__file__))
        css_path = os.path.join(this_folderpath, 'print.css')

        context_header = {}
        context_header['title'] = title
        context_header['rev'] = rev
        context_header['doc_no'] = doc_no
        context_header['date'] = change_date_format(date)
        add_pdf_header(options, context_header=context_header)
        pdf = pdfkit.from_string(main_content, False, configuration=config, options=options, css=css_path)
        response = pdf_response(pdf)
    except Exception as e:
        print(str(e))
        response['message'] = str(e)
        return json_response(response), 400
    finally:
        if (os. path. isfile(options['header-html'])):
            os.remove(options['header-html'])

    return response


def add_pdf_header(options, context_header):
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as header:
        options['header-html'] = header.name
        header.write(
            render_template('header.html', context_header=context_header).encode('utf-8')
        )
    return

def add_pdf_footer(options):
    # same behaviour as add_pdf_header but without passing any variable
    return

def pdf_response(pdf):
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    filename = 'pdf-from-html.pdf'
    response.headers['Content-Disposition'] = ('attachment; filename=' + filename)
    return response

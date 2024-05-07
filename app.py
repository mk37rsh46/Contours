from flask import Flask, render_template, request, jsonify
import gen_graph
import io

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'pwdkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    graph_type = request.form['graphType']
    interpolation_type = request.form['interpolationType']
    try:
        csv_data = io.StringIO(file.stream.read().decode('UTF8'), newline=None)
        graph_file = ""
        if graph_type != "3d":
            graph_file = gen_graph.create_contour_graph(csv_data, interpolation_type=interpolation_type, graph_type=graph_type)
        else:
            graph_file =  gen_graph.create_3d_graph(csv_data)
        return jsonify( status="Graph Created!", graph=graph_file)

    except Exception as e:
         return jsonify( status="Problem Creating", graph="")



if __name__ == '__main__':
    app.run(debug=True)

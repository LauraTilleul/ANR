# -*- coding:utf-8 -*-
from scripts_python import script_basic_stats, script_bubble_cooc, script_gender, script_partners, script_best_programs
from flask import Flask, request, render_template
import jinja2
import json

app = Flask(__name__)
app.jinja_loader=jinja2.FileSystemLoader('./view/templates')

@app.route('/', methods=['GET'])
def index():
        return render_template("index.html")

@app.route('/scatterplot', methods=['GET'])
def scatterplot():
        return render_template("scatter_plot.html")

@app.route('/basic_stats', methods=['GET'])
def basic_stats():
        #script_basic_stats.getDataBasicStats()
        return render_template("basic_stats.html")

@app.route('/gender',methods=['GET'])
def gender():
        #script_gender.formatDataToJson()
        return render_template("gender.html")

@app.route('/bubbleChart',methods=['GET'])
def bubbleChart():
    #script_bubble_cooc.getDataBubble(50)
    return render_template("bubble_chart.html")

    
@app.route('/graphePartner',methods=['GET'])
def graphePartner():
    #script_partners.getDataPartners()
    return render_template("graphe_partenaires.html")
           
@app.route('/cooccurence', methods=['GET'])
def cooccurence():
    #script_bubble_cooc.getDataCooccurences()
    return render_template("cooccurences.html")

@app.route('/programmes', methods=['GET','POST'])
def programmes():
    sex=request.args['sexe']
    sex=sex.capitalize()
    var=sex
    if sex != "Femme" and sex != "Homme" : 
        sex='All'
        var='projet'

    #script_best_programs.getDataPrograms(sex)
    return render_template("programs.html", sexe=sex, var=var)

if __name__ == '__main__':
        app.run(debug=True)

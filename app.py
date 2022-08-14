import requests
from flask import Flask,render_template,jsonify,request
from neo2flask import traveledge
app = Flask(__name__)
storage={}

@app.route('/')
def hello_world():  # put application's code here
    return render_template('page1.html')

@app.route('/kgmap')
def show():
    return render_template('page2.html')



@app.route('/getindex',methods=['GET','POST'])
def get():

    id=request.args.get('id')
    idlist = []
    idlist.append(str(id))
    nodedata = []
    relationdata = []
    for re in storage['relation']:
        if (str(re['source']) == str(id) and str(re['name']=='hasEvent') and str(re['target']) not in idlist):
            idlist.append(str(re['target']))
    for node in storage['node']:
        if (str(node['id']) in idlist):
            nodedata.append(node)
    for relation in storage['relation']:
        if (str(relation['source']) in idlist) or (str(relation['target']) in idlist):
            relationdata.append(relation)
    return jsonify({'node': nodedata, 'relation': relationdata})

@app.route('/travalEdge',methods=['GET','POST'])
def getdata():

    type=request.args.get('type')

    datadict = {'美食': 'ACT-Eat', '娱乐': 'ACT-Entertain', '购物': 'ACT-Buy', '旅游': 'ACT-Visit', '住宿': 'ACT-live',
                '拍照': 'ACT-Shoot'}
    travel = datadict[type]
    cypher = "match (n:`" + str(
        travel) + "`)<-[r1]-(n1:Travel)-[r2:hasEvent]->(n3)-[r3:nextEvent]->(n4) return n1, n3,n4 limit 40"
    trvelkg = traveledge(cypher)
    nodelist, relationlist = trvelkg.getData()
    node2index = trvelkg.node2index(nodelist)
    relation=[]
    for n in nodelist:
        n = n.update({'id': node2index[n['name']]})

    for re in relationlist:
        relation.append({'source': node2index[re[0]['name']], 'target': node2index[re[1]['name']], 'name': 'hasEvent'})
        relation.append({'source': node2index[re[0]['name']], 'target': node2index[re[2]['name']], 'name': 'hasEvent'})
        relation.append({'source': node2index[re[1]['name']], 'target': node2index[re[2]['name']], 'name': 'nextEvent'})
    storage.update({'node':nodelist})
    storage.update({'relation':relation})
    return jsonify({'node':nodelist,'relation':relation})

if __name__ == '__main__':
    app.run()

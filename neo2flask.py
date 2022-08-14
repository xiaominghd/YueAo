
# coding=utf-8
from py2neo import Graph
import pandas as pd
class traveledge():

    def __init__(self,cypher):

        self.cypher=cypher
        self.grah=Graph("bolt://10.112.184.124:7687",auth=('neo4j','123456'))

    """""""""
    initCypher 从neo4j数据库中获取数据
    返回的是一个结构化的数据，在这里暂时只支持对于节点的查询
    返回数据的顺序与Cypher语句中的顺序一致
    """""""""
    def initCypher(self):

        data=self.grah.run(self.cypher).data()

        return data
    """""""""
    在这里定义你图的节点，因为返回的数据是结构化的数据，而且有的部分其实并不需要做展示，所以需要进行转化
    输入：
    图node
    输出：
    自己定义的结构数据，注意coategory属性是必须的，这个数据将会标明当前的节点属于哪一类，有利于进行展示
    """""""""
    def graphnode(self , x):

        if ('ACT-Eat' in x.keys()):
            des = ''
            if 'time' in x.keys():
                des += x['time']
            if 'name' in x.keys():
                des += x['name']
            if 'menu' in x.keys():
                des += x['menu']
            return {'name':des,'category':0}

        if('ACT-Buy' in x.keys()):
            des = ''
            if 'time' in x.keys():
                des += x['time']
            if 'name' in x.keys():
                des += x['name']
            if 'role' in x.keys():
                des += x['role']
            return {'name':des,'category':1}

        if ('ACT-Entertain' in x.keys()):
            des = ''
            if 'time' in x.keys():
                des += x['time']
            des += x['name']
            return {'name':des,'category':2}

        if ('ACT-live' in x.keys()):
            des = ''
            if 'time' in x.keys():
                des += x['time']
            des += x['name']
            return {'name': des, 'category': 3}

        if ('ACT-Visit' in x.keys()):
            des = ''
            if 'time' in x.keys():
                des += x['time']
            des += x['name']
            return {'name':des,'category':4}

        if ('ACT-Go' in x.keys()):
            des = ''
            if 'time' in x.keys():
                des += x['time']
            des += x['name']
            return {'name': des, 'category': 5}

        if ('ACT-Shoot' in x.keys()):
            des = ''
            if 'time' in x.keys():
                des += x['time']
            des += x['name']
            if 'role' in x.keys():
                des += x['role']
            return {'name': des, 'category': 6}

        elif ('user_id' in x.keys()):
            node={}
            des = ''

            if ('date' in x.keys()):
                des += x['date']
                node.update({'date':x['date']})

            des += x['companion']
            node.update({'companion': x['companion']})
            des += '花费'
            des += x['cost']
            node.update({'cost': x['cost']})

            if ('days' in x.keys()):
                des=des+'游玩了'+x['days']
                node.update({'day':x['days']})

            node.update({'name':des})
            node.update({'category':7})
            return node

    """""""""
    这里是最主要的，直接调用该函数可以获取node 和relation
    但是并不能够直接用，因为在前端echarts中是以index来识别每一个node
    """""""""
    def getData(self):

        nodelist=[]
        relation=[]
        data=self.initCypher()
        for d in data:
            mid=[]
            for k in dict(d).keys():
                x=self.graphnode(dict(d)[k])
                if(x not in nodelist):
                    nodelist.append(x)
                mid.append(x)
            relation.append(mid)

        return nodelist,relation

    def node2index(self,nodelist):

        name2index={}
        index=0

        for node in nodelist:

            if(node['name'] not in name2index):
                name2index.update({node['name']:index})
                index+=1

        return name2index



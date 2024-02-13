from elasticsearch import Elasticsearch
from flask import current_app

def create_index(name):
    es:Elasticsearch = current_app.es
    es.indices.create(index=name)

def add_post(index_name,post_name,body,post_id):
    es:Elasticsearch = current_app.es
    doc_post = {
                'post_name':post_name,
                'body':body
                }
    es.index(index=index_name,id=post_id,document=doc_post)

def get_posts(index_name,data):
    es:Elasticsearch = current_app.es
    result = es.search(index=index_name,query={'multi_match':{'query':data,'fields':['post_name','body']}})
    return result['hits']['hits']


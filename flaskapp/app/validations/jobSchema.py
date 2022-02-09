jobSchema = {
   'type': 'object',
   'properties': {
        'order': {'type': 'integer'},
        'url':{'type':'string'},
        'action':{
            'type':'string'
        },
        'actionValue':{'type':'string'},
        'serviceId':{'type':'integer'},
        'description':{'type':'string'}
    },
    'required': ['order','url','action','actionValue','serviceId','description']
}
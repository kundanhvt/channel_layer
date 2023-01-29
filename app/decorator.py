import json
def is_authenticated(func):
    def wrapper(self,*args, **kwargs):
        breakpoint()
        if not self.scope['user'].is_authenticated:
            self.send({
                'type':'websocket.sned',
                'text':json.dumps({"msg":"Login Required"})
            })
            return
        return func(*args,**kwargs)
    return wrapper

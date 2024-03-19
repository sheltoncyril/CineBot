class ServiceRegistry:
    def __init__(self, service_map):
        self.service_map = service_map
        self.initalized_service_map = dict()
        for svc_name in service_map.keys():
            self._init_service(svc_name)

    def _init_service(self, svc_name, args=None, kwargs=None):
        svc = self.service_map.get(svc_name)
        svc = svc()
        svc.init(*args, **kwargs)
        self.initalized_service_map[svc_name] = svc

    def get_service(self, svc_name):
        svc = self.initialized_service_map.get(svc_name)
        if svc:
            return svc
        raise NotImplementedError

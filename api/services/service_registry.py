from .similarity_recommender_service import SimilarityRecommenderService
from .tfidf_recomender_service import TFIDFRecommenderService

service_map = dict(similarity_recommender_service=SimilarityRecommenderService, tfidf_recommender_service=TFIDFRecommenderService)


class ServiceRegistry:
    def __init__(self):
        self.service_map = service_map
        self.initialized_service_map = dict()

    def init(self):
        for svc_name in service_map.keys():
            self._init_service(svc_name)

    def _init_service(self, svc_name, args=None, kwargs=None):
        svc = self.service_map.get(svc_name)
        svc = svc()
        svc.init()
        self.initialized_service_map[svc_name] = svc

    def get_service(self, svc_name):
        svc = self.initialized_service_map.get(svc_name)
        if svc:
            return svc
        raise NotImplementedError(f"service {svc_name} is not implemented.")

    def cleanup(self):
        pass
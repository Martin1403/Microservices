import logging

from deepspeech import Model

logging.basicConfig(level=logging.DEBUG)


class DeepSpeech(Model):
    def __init__(self, model_path, scorer_path=None):
        super().__init__(model_path=model_path)
        logging.debug(f"Model loaded: {model_path}")
        if scorer_path:
            self.enableExternalScorer(scorer_path=scorer_path)
            logging.debug(f"Scorer loaded: {scorer_path}")

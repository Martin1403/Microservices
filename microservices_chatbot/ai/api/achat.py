import os
import asyncio
import click
import pickle

from functools import wraps
from typing import List, Optional

import tensorflow as tf

from ai.api.model import Seq2SeqModel


def load_model():
    path = os.path.abspath(os.path.join(os.path.dirname(__name__), "ai"))
    tf.reset_default_graph()
    word2id = pickle.load(open(f"{path}/model/word2id.pkl", "rb"))
    id2word = pickle.load(open(f"{path}/model/id2word.pkl", "rb"))
    args = pickle.load(open(f"{path}/model/args.pkl", "rb"))

    model = Seq2SeqModel(14, word2id, id2word, args.maxlen)
    model.declare_placeholders()
    model.create_embeddings(args.emb)
    model.build_encoder(args.hidden)
    model.memory_network(args.hidden)
    model.build_decoder(args.hidden, len(word2id.keys()), word2id['^'], word2id['$'])

    session = tf.compat.v1.Session()
    session.run(tf.compat.v1.global_variables_initializer())
    saver = tf.compat.v1.train.Saver()
    saver.restore(session, f"{path}/model/model.ckpt")
    print('Model')
    return model, session


model, session = load_model()


class ChatBot(object):

    def __init__(self, text):
        self.output = None
        self.text = text

    async def __aenter__(self):
        global model, session
        self.output = model.predict_sentence(self.text, session)
        return self

    async def __aexit__(self, *args):
        pass

    def __await__(self):
        return self.__aenter__().__await__()


def async_run(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper


@click.command("test-async-chat")
@async_run
async def test_async_chat():
    async with ChatBot(text="hello") as sess:
        sess = await sess

    click.echo(sess.output)

    async with ChatBot(text="what can i do for you?") as sess:
        sess = await sess

    click.echo(sess.output)

    click.echo("Async ok...")


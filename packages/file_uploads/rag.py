import os
import time
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from file_uploads import process
import uuid

INDEX_NAME = "energy-bill-extraction"
BLOCK_SIZE = 20
MODEL = "text-embedding-3-small"

client = OpenAI()

# Setup Pinecone

pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY")
)

def get_index(index=INDEX_NAME):
    if index not in pc.list_indexes().names():
        pc.create_index(
            name=index,
            dimension=1536,
            metric='dotproduct',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-west-2'
            )
        )
        while not pc.describe_index(index).status['ready']:
            time.sleep(1)
        return pc.Index(index)
    else:
        return pc.Index(index)
    

def save_to_index(path_to_file, index=INDEX_NAME):
    content = process(path_to_file)
    lines = content.split('\n')
    blocks = [lines[i:i+BLOCK_SIZE] for i in range(0, len(lines), BLOCK_SIZE)]
    # print(blocks)

    for block in blocks:
        line = ' '.join(block)

        # Pinecone needs an ID, the Embedding data and the text as metadata
        ids = [str(uuid.uuid4())]
        res = client.embeddings.create(input=line, model=MODEL)
        embeds = [record.embedding for record in res.data]
        meta = [{"text": line}]
        # The actual inset statement
        to_upsert = zip(ids, embeds, meta)
        index.upsert(vectors=list(to_upsert))


def query_index(query, index=INDEX_NAME, num_results=4):
    xq = client.embeddings.create(input=query, model=MODEL).data[0].embedding
    res = index.query(vector=[xq], top_k=num_results, include_metadata=True)
    _output = """{'matches': [{'id': '932',
              'metadata': {'text': 'Why did the world enter a global '
                                   'depression in 1929 ?'},
              'score': 0.751888752,
              'values': []},
             {'id': '787',
              'metadata': {'text': "When was `` the Great Depression '' ?"},
              'score': 0.597448647,
              'values': []},
             {'id': '400',
              'metadata': {'text': 'What crop failure caused the Irish Famine '
                                   '?'},
              'score': 0.367482603,
              'values': []},
             {'id': '835',
              'metadata': {'text': 'What were popular songs and types of songs '
                                   'in the 1920s ?'},
              'score': 0.324545294,
              'values': []},
             {'id': '262',
              'metadata': {'text': 'When did World War I start ?'},
              'score': 0.320995867,
              'values': []}],
            'namespace': '',
            'usage': {'read_units': 6}}"""
    for match in res['matches']:
        print(f"{match['score']:.2f}: {match['metadata']['text']}")
    return res



    
# print(index.describe_index_stats())
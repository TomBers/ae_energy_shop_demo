import os
import time
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec
from file_uploads import process
import uuid

index_name = "energy-bill-extraction"

client = OpenAI()

# Setup Pinecone

pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY")
)

# Create an Index (another word for table) if it doesn't exist
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='dotproduct',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-west-2'
        )
    )
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

# Connect to Vector Store
index = pc.Index(index_name)
BLOCK_SIZE = 20

MODEL = "text-embedding-3-small"
# Process the file and create embeddings
# content = process("tst.pdf")
# lines = content.split('\n')
# blocks = [lines[i:i+BLOCK_SIZE] for i in range(0, len(lines), BLOCK_SIZE)]
# print(blocks)

# for block in blocks:
#     line = ' '.join(block)

#     Pinecone needs an ID, the Embedding data and the text as metadata
#     ids = [str(uuid.uuid4())]
#     res = client.embeddings.create(input=line, model=MODEL)
#     embeds = [record.embedding for record in res.data]
#     meta = [{"text": line}]
#     The actual inset statement
#     to_upsert = zip(ids, embeds, meta)
#     index.upsert(vectors=list(to_upsert))


query = "What is my estimated annual cost?"
# Create an embedding for the query
xq = client.embeddings.create(input=query, model=MODEL).data[0].embedding
res = index.query(vector=[xq], top_k=15, include_metadata=True)
print(res)
    
# print(index.describe_index_stats())
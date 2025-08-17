#pip install simhash datasketch
from simhash import Simhash
from datasketch import MinHash

chunk_size = 40
comparison_threshold = 70
chunks = list()
chunk_to_group = dict()
strings = list()

strings.append("The quick brown fox jumped over the lazy dog.")
strings.append('The quick brown dog jumped over the lazy fox.')
strings.append('What will this do? Lazy dogs are lazy foxes.')

#break each string into chunks
for i in range(len(strings)):
    curr_string = strings[i]
    for j in range(0, len(curr_string), chunk_size):
        chunk = curr_string[j:j + chunk_size]
        chunks.append(chunk)
print(chunks)

#group chunks with a similarity rate
curr_gr = 1
for i in range(len(chunks)):
    for j in range(i + 1, len(chunks)):
        #check if curr_str is already in a group
        gr = 0
        for group in chunk_to_group.keys():
            if chunks[i] in chunk_to_group[group]:
                gr = group
                break

        if gr == 0:
            chunk_to_group[curr_gr] = set()
            chunk_to_group[curr_gr].add(chunks[i])
            gr = curr_gr
            curr_gr += 1

        #get similarity rate first, comparison val is always curr_str
        ####### SIMHASH EXAMPLE #######
        # hash_1 = Simhash(chunks[i])
        # hash_2 = Simhash(chunks[j])
        # distance = hash_1.distance(hash_2)

        # similarity_percentage = ((64 - distance) / 64) * 100

        # print("DEBUG: ", chunks[i], chunks[j], similarity_percentage)

        # if similarity_percentage >= comparison_threshold:
        #     chunk_to_group[gr].add(chunks[j])


        ####### MINHASH EXAMPLE #######
        
        m1 = MinHash(num_perm=128)
        m2 = MinHash(num_perm=128)

        shingles1 = chunks[i].split()
        shingles2 = chunks[j].split()

        for s in shingles1:
            m1.update(s.encode('utf8'))
        for s in shingles2:
            m2.update(s.encode('utf8'))

        print("DEBUG: S1: ", chunks[i], "S2: ", chunks[j], m1.jaccard(m2))

        if m1.jaccard(m2) * 100 >= comparison_threshold:
            chunk_to_group[gr].add(chunks[j])

#anything that didn't get grouped
for i in range(len(chunks)):
    if i not in chunk_to_group:
        chunk_to_group[gr] = set()
        chunk_to_group[gr].add(chunks[i])
        gr += 1

print(chunk_to_group)

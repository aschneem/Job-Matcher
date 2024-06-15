"""functions to assist with the creation of vectors and basic vector calculations"""
import math

CHARACTERS_TO_STRIP = "-•*◦\u2220\u2640"
translate_table = str.maketrans('', '', CHARACTERS_TO_STRIP)

def normalize(string):
    """normalizes the string for the purposes of building a vector"""
    return string.lower().translate(translate_table)

def keyword_vector_to_named_vector(keyword_vector):
    """Converts a keyword vector to a vector with the keyword as the dimension 
    and keyword score as the magnitude for that component"""
    named_vector = {}
    for keyword in keyword_vector:
        norm_keyword = keyword['keyword'].lower().translate(translate_table)
        named_vector[norm_keyword] = keyword['score']
    return named_vector

def pos_list_to_named_vector(string_list):
    """Converts a part of speach list to a vector with the word as the dimension 
    and the frequency as the magnitude for that component"""
    vector = {}
    for token in string_list:
        norm_token = token.get('lemma', '').lower().translate(translate_table)
        vector[norm_token] = vector.get(norm_token, 0) + 1
    return vector

def entity_vector_to_named_vector(entity_vector):
    """Converts a entity list to a vector with the entity as the dimension 
    and the frequency as the magnitude for that component"""
    named_vector = {}
    for entity in entity_vector:
        name = entity['text'] + '_' + entity['label']
        named_vector[name] = named_vector.get(name, 0) + 1
    return named_vector

def magnitude_named_vector(vector):
    """computes the magnitude fo the vector"""
    mag = 0
    for dim in vector.keys():
        mag = mag + (vector[dim] * vector[dim])
    return math.sqrt(mag)

def dot_product_named_vector(vector_a, vector_b):
    """computes the dot product between two named vectors"""
    result = 0
    for dim in vector_a.keys():
        result = result + (vector_a[dim] * vector_b.get(dim, 0))
    return result

def cosine_sim_named_vector(vector_a, vector_b):
    """calculates the cosine similarity between two vectors"""
    mag = magnitude_named_vector(vector_a) * magnitude_named_vector(vector_b)
    if mag == 0:
        return 0
    return dot_product_named_vector(vector_a, vector_b) / (mag)

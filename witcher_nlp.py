import pandas as pd
import numpy as np
import spacy
import os

def main():
    # Load spacy module
    nlp = spacy.load("en_core_web_sm")

    # Scan directory and load books
    books_load = [book for book in os.scandir("data") if ".txt" in book.name]

    #! Read the books and load into nlp
    texts = []
    for book in books_load:
        text = open(book).read()
        texts.append(text)
              
    docs = list(nlp.pipe(texts, n_process=4))

    # Load character names
    characters_df = pd.read_csv("characters.csv")
    
    # ! Create function to list of list of named entities
    sentence_entities_list = [lambda x: sentence_entities(characters_df, docs[x])]

    #! Create dataframe of relationships between characters
    relationships = []
    for x in range(sentence_entities_list):
        relationships.append({'book': book[x].name, 'relations_df': character_relations(sentence_entities_list[x])})
    


# Function to create list of entities in each sentence
def sentence_entities(characters_df, doc):
    # Create lists of named entities for each sentence
    sentence_entity_df = []

    # Loop through sentences to store named entities
    for sentence in doc.sents:
        entity_list = [ent.text for ent in sentence.ents]
        sentence_entity_df.append({'sentence': sentence, 'entities': entity_list})

    # Convert list to dataframe and display
    sentence_entity_df = pd.DataFrame(sentence_entity_df)

    # Apply above function to  clean entity dataframe of non-character entities
    sentence_entity_df['character_entities'] = sentence_entity_df['entities'].apply(lambda x: filter_entity(x, characters_df))

    # Remove empty entity lists
    sentence_entity_df = sentence_entity_df[sentence_entity_df['character_entities'].map(len) > 0]

    # Convert character entities to only being the first name of the characters
    sentence_entity_df['character_entities'] = sentence_entity_df['character_entities'].apply(lambda x: [item.split()[0]
                                                                                                        for item in x])
    
    return sentence_entity_df

# Function to filter out the non-character entities from the dataframe
def filter_entity(ent_list, characters_df):
    return [ent for ent in ent_list
            if ent in list(characters_df.character)
            or ent in list(characters_df.first_name)]

# Create dataframe of relationships between characters
def character_relations(sentence_entity_df):
    # Window size for sentences in which we will accept for a relationship to form
    window_size = 5

    # Create relationships list
    relationships = []

    # Loop through windows
    for i in range(sentence_entity_df.index[-1]):
        end_i = min(i+5, sentence_entity_df.index[-1])
        character_list = sum((sentence_entity_df.loc[i: end_i].character_entities), [])
            
        # Remove any duplicates
        unique_characters = [character_list[i] for i in range(len(character_list))
                            if (i==0) or character_list[i] != character_list[i-1]]
            
        # When more than 1 character in window append to relationships list
        if len(unique_characters) > 1:
            for idx, x in enumerate(unique_characters[:-1]):
                y = unique_characters[idx + 1]
                relationships.append({'source': x, 'target': y})

    # Convert list to dataframe
    relationships_df = pd.DataFrame(relationships)

    # Sort the relationships
    relationships_df = pd.DataFrame(np.sort(relationships_df.values, axis=1), columns = relationships_df.columns)

    # Create column for weighting relationships
    relationships_df['weight'] = 1
    # Aggregate relationships and weight them
    relationships_df = relationships_df.groupby(['source','target'], sort=False, as_index=False).sum()

if __name__ == "__main__":
    main()
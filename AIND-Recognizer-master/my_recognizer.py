import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer
    test_sequences = list(test_set.get_all_Xlengths().values())

    for test_X, test_Xlength in test_sequences:
        log_likelihood_words_dict = dict()
        for word, hmm_model in models.items():
            try:
                log_likelihood_words_dict[word] = hmm_model.score(test_X,test_Xlength)
            except:
                #Can't get hmm_model, so just assign a negative score
                log_likelihood_words_dict[word] = -10000
                continue
        probabilities.append(log_likelihood_words_dict)

    for prob in probabilities:
        guesses.append(max(prob,key=prob.get))
    return probabilities, guesses


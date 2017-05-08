import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class   (ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Baysian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on BIC scores
        score_and_n = []
        for n in range(self.min_n_components, self.max_n_components):
            try:
                hmm_model = GaussianHMM(n_components=n, covariance_type="diag", n_iter=1000,
                                        random_state=self.random_state, verbose=self.verbose).fit(self.X,
                                                                                                  self.lengths)
                logl = hmm_model.score(self.X, self.lengths)
                #https://rdrr.io/cran/HMMpa/man/AIC_HMM.html
                # p = m ^ 2 + km - 1
                # m = n: number of states in the Markov chain of the model
                # k = : single numeric value representing the number of parameters of the underlying distribution of the observation process (e.g. k=2 for the normal distribution (mean and standard deviation)).
                num_of_parameter = n * n + n * self.X.shape[1] - 1
                bic = -2 * logl + num_of_parameter * np.log(len(self.X))
                score_and_n.append([bic, n])

            except:
                # just ignore the error case
                pass

        if len(score_and_n) > 0:
            _, highest_n =  min(score_and_n)
            hmm_model = GaussianHMM(n_components=highest_n, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=self.verbose).fit(self.X, self.lengths)
            return hmm_model
        else:
            return self.base_model(self.n_constant)


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # TODO implement model selection based on DIC scores
        score_and_n = []
        for n in range(self.min_n_components, self.max_n_components):
            try:
                hmm_model = GaussianHMM(n_components=n, covariance_type="diag", n_iter=1000,
                                        random_state=self.random_state, verbose=self.verbose).fit(self.X,
                                                                                                  self.lengths)
                logl_i = hmm_model.score(self.X, self.lengths)
                log_rest_list = []
                for word in self.hwords:
                    if word != self.this_word:
                        X, lengths = self.hwords[word]
                        log_rest_list.append(hmm_model.score(X, lengths))
                logl_rest = np.average(log_rest_list)
                dic = logl_i - logl_rest
                score_and_n.append([dic, n])

            except:
                # just ignore the error case
                pass

        if len(score_and_n) > 0:
            _, highest_n = max(score_and_n)
            hmm_model = GaussianHMM(n_components=highest_n, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=self.verbose).fit(self.X, self.lengths)
            return hmm_model
        else:
            return self.base_model(self.n_constant)


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # if length of sequences is less than 2, we just return the base_model, because KFold requires splits to be at least 2.
        if len(self.sequences) < 2:
            return self.base_model(self.n_constant)

        score_and_n = []
        for n in range(self.min_n_components, self.max_n_components):
            scores_array = []
            split_method = KFold(n_splits=min(3,len(self.sequences)))
            for cv_train_idx, cv_test_idx in split_method.split(self.sequences):
                trainX, trainlengths = combine_sequences(cv_train_idx, self.sequences)
                try:
                    hmm_model = GaussianHMM(n_components=n, covariance_type="diag", n_iter=1000,
                                            random_state=self.random_state, verbose=self.verbose).fit(trainX, trainlengths)
                    testX, testlengths = combine_sequences(cv_test_idx, self.sequences)
                    scores_array.append(hmm_model.score(testX, testlengths))
                except:
                    #just ignore the error case
                    pass
            if len(scores_array) > 0:
                score_and_n.append([np.average(scores_array), n])
        if len(score_and_n) > 0:
            _, highest_n = max(score_and_n)
            hmm_model = GaussianHMM(n_components=highest_n, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=self.verbose).fit(self.X, self.lengths)
            return hmm_model
        else:
            return self.base_model(self.n_constant)

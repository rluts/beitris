import {
  QUIZ_ANSWER,
  QUIZ_LOADED,
  CATEGORIES_LOADED,
  QUESTION_SKIPPED, SET_TITLE, LOADING
} from './constants';
import axios from 'axios';

const apiUrl = '/api';

export const ask = (category) => {
  return (dispatch) => {

    dispatch(loading());
    return axios.post(`${apiUrl}/ask/`, {category})
      .then(response => {
        dispatch(quizLoaded(response.data))
      })
      .catch(error => {
        console.warn('Backend return error');
        console.warn(error.response);
        dispatch(ask(category))
      });
  };
};

export const quizLoaded =  (data) => {
  return {
    type: QUIZ_LOADED,
    question: data.question,
    imageUrl: data.url,
    questionId: data.question_id
  }
};

export const check = (answer, question) => {
  return (dispatch) => {
    return axios.post(`${apiUrl}/answer/`, {answer, question})
      .then(response => {
        dispatch(answerChecked(response.data))
      })
      .catch(error => {
        throw(error);
      });
  };
};

export const loading = () => {
  return {
    type: LOADING
  }
};

export const skip = (question) => {
  return (dispatch) => {
    return axios.post(`${apiUrl}/answer/get_answer/`, {question})
      .then(response => {
        dispatch(skipped(response.data))
      })
      .catch(error => {
        throw(error);
      });
  };
};

export const loadCategoriesAjax = () => {
  return (dispatch) => {
    return axios.get(`${apiUrl}/categories/`)
      .then(response => {
        dispatch(categoriesLoaded(response.data))
      })
      .catch(error => {
        throw(error);
      });
  };
};

export const categoriesLoaded = (data) => {
  return{
    type: CATEGORIES_LOADED,
    categories: data
  }
};

export const answerChecked = (data) => {

  return {
    type: QUIZ_ANSWER,
    right: data.result === "OK",
  }
};

export const skipped = (data) => {
  return {
    type: QUESTION_SKIPPED,
    rightAnswer: data.result[0]
  }
};

export const setTitle = (text) => {
  return {
    type: SET_TITLE,
    titleText: text
  }
};

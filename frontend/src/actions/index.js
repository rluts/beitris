import {
  QUIZ_ANSWER,
  QUIZ_LOADED,
  CATEGORIES_LOADED,
  QUESTION_SKIPPED,
  SET_TITLE,
  LOADING,
  STATUS_LOADED,
  CLEAR_STATUS,
  AUTHENTICATION_SUCCESS,
  LOGOUT_SUCCESS
} from './constants';
import axios from 'axios';
import {BACKEND_URL} from "../constants";
import cookie from "react-cookies";


const API_URL = BACKEND_URL + '/api'


const getCsrfTokenHeader = () => {
  return {'X-CSRFToken': cookie.load('csrftoken')}
}


export const getBackendStatus = () => {
  return (dispatch) => {
    return axios.get(`${API_URL}/status/`)
        .then(response => {
          dispatch(statusLoaded(response.data))
        })
  }
}

export const authenticateRequest = (email, password, rememberMe) => {
  return (dispatch) => {
    return axios.post(`${API_URL}/auth/login/`,
        {email, password, rememberMe}, {headers: getCsrfTokenHeader()})
        .then(response => {
          dispatch(authenticationLoaded(response.data))
        })
        .catch(error => {
          throw error
        })
  }
}

export const logoutRequest = () => {
  return (dispatch) => {
    return axios.post(`${API_URL}/auth/logout/`, {},{headers: getCsrfTokenHeader()})
        .then(() => {
          dispatch(logoutSuccess())
        })
  }
}

export const logoutSuccess = () => {
  delete localStorage.websocketKey;
  return {
    type: LOGOUT_SUCCESS
  }
}

export const authenticationLoaded = (data) => {
  localStorage.setItem('websocketKey', data.key);
  return {
    type: AUTHENTICATION_SUCCESS,
    data: data.user
  }
}

export const statusLoaded = (data) => {
  return {
    type: STATUS_LOADED,
    data
  }
};

export const clearStatus = () => {
  return {
    type: CLEAR_STATUS
  }
};


export const ask = (category) => {
  return (dispatch) => {

    dispatch(loading());
    return axios.post(`${API_URL}/ask/`, {category},
        {headers: getCsrfTokenHeader()})
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
    imageUrl: BACKEND_URL + data.url,
    questionId: data.question_id
  }
};

export const check = (answer, question, category) => {
  return (dispatch) => {
    return axios.post(`${API_URL}/answer/`, {answer, question},
        {headers: getCsrfTokenHeader()})
      .then(response => {
        dispatch(answerCheckedHandler(response.data, category))
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

export const skip = (question, category) => {
  return (dispatch) => {
    return axios.post(`${API_URL}/answer/get_answer/`, {question},
        {headers: getCsrfTokenHeader()})
      .then(response => {
        dispatch(skippedHandler(response.data, category))
      })
      .catch(error => {
        throw(error);
      });
  };
};

export const loadCategoriesAjax = () => {
  return (dispatch) => {
    return axios.get(`${API_URL}/categories/`)
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

export const answerCheckedHandler = (data, category) => {
  const result = data.result === "OK";
  return (dispatch) => {
    if (result) {
        dispatch(ask(category));
    }
    dispatch(answerChecked(result))
  }
};

export const answerChecked = (result) => {
  return {
      type: QUIZ_ANSWER,
      right: result,
  }
};

export const skippedHandler = (data, category) => {
  return (dispatch) => {
    dispatch(skipped(data));
    dispatch(ask(category))
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

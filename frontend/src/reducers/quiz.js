import {
  QUIZ_ANSWER,
  QUIZ_LOADED,
  CATEGORIES_LOADED,
  QUESTION_SKIPPED,
  SET_TITLE,
  LOADING,
  STATUS_LOADED,
  CLEAR_STATUS,
  AUTHENTICATION_SUCCESS, LOGOUT_SUCCESS
} from "../actions/constants";

const initialState = {
  loading: false,
  question: null,
  statusLoaded: false
};

const quiz = (state = initialState, action) => {
  switch (action.type) {
    case AUTHENTICATION_SUCCESS:
      return {
        ...state,
        authorized: true,
        user: action.data
      };
    case LOGOUT_SUCCESS:
      return {
        authorized: false,
        user: null
      };
    case  STATUS_LOADED:
      return {
        ...state,
        statusLoaded: true,
        ...action.data
      };
    case CLEAR_STATUS:
      return {
        ...state,
        statusLoaded: false
      }
    case QUIZ_LOADED:
      return {
        ...state,
        loading: false,
        titleText: action.question,
        imageUrl: action.imageUrl,
        questionId: action.questionId,
        answered: false
      };
    case QUIZ_ANSWER:
      return {
        ...state,
        right: action.right,
        answered: true
      };
    case CATEGORIES_LOADED:
      return {
        ...state,
        categories: action.categories
      };
    case QUESTION_SKIPPED:
      return {
        ...state,
        titleText: `This is ${action.rightAnswer}`
      };
    case SET_TITLE:
      return {
        ...state,
        titleText: action.titleText
      };
    case LOADING:
      return {
        ...state,
        loading: true
      };
    default:
      return state
  }
};
export default quiz

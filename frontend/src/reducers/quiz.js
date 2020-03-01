import {
  QUIZ_ANSWER,
  QUIZ_LOADED,
  CATEGORIES_LOADED,
  QUESTION_SKIPPED, SET_TITLE, LOADING
} from "../actions/constants";

const initialState = {
  loading: false,
  question: null
};

const quiz = (state = initialState, action) => {
  switch (action.type) {
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
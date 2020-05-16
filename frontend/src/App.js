import React, {Component} from 'react';
import './css/styles.scss'
import Quiz from "./components/quiz/Quiz";
import {BrowserRouter as Router, Route, Switch} from "react-router-dom";
import SignIn from "./components/auth/SignIn";
import SignUp from "./components/auth/SignUp";
import BeitrisLayout from "./layouts";
import {connect} from "react-redux";
import {
    ask,
    authenticateRequest,
    check,
    clearStatus,
    getBackendStatus,
    loadCategoriesAjax, logoutRequest,
    setTitle,
    skip
} from "./actions";
import Loading from "./components/auth/Loading";
import PrivateRoute from "./components/auth/PrivateRoute";


function mapStateToProps(state) {
    return state.quiz;
}

const mapDispatchToProps = dispatch => {
  return {
      loadStatus: () => {
          dispatch(getBackendStatus());
      },
      loadQuiz: (category) => {
          dispatch(ask(category));
      },
      loadCategories: () => {
          dispatch(loadCategoriesAjax())
      },
      checkAnswer: (answer, questionId, category) => {
          dispatch(check(answer, questionId, category))
      },
      setTitle: (text) => {
          dispatch(setTitle(text))
      },
      skipQuestion: (question, category) => {
          dispatch(skip(question, category))
      },
      clearStatus: () => {
          dispatch(clearStatus())
      },
      authenticate: (email, password, rememberMe) => {
          dispatch(authenticateRequest(email, password, rememberMe))
      },
      logout: () => {
          dispatch(logoutRequest())
      }
    };
};


class App extends Component {
    componentDidMount() {
        this.props.loadStatus()
    }

    render() {
        return (
                <Router>
                    <BeitrisLayout user={this.props.user} logout={this.props.logout}>
                        <Switch>
                            <PrivateRoute path="/quiz" authenticated={this.props.authorized}>
                                <Quiz {...this.props} />
                            </PrivateRoute>,
                            <Route path="/login">
                                <SignIn
                                    authenticate={this.props.authenticate}
                                    authorized={this.props.authorized}
                                />
                            </Route>
                            <Route path="/register">
                                <SignUp/>
                            </Route>
                            <Route path="/">
                                <Loading
                                    authorized={this.props.authorized}
                                    statusLoaded={this.props.statusLoaded}
                                    clearStatus={this.props.clearStatus}
                                    loadStatus={this.props.loadStatus}
                                />
                            </Route>
                        </Switch>
                    </BeitrisLayout>
                </Router>
        );
    }
}


export default connect(
    mapStateToProps, mapDispatchToProps
)(App);

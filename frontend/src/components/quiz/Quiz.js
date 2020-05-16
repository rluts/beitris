import React, {Component} from 'react';
import '../../css/styles.scss'
import CircularProgress from "@material-ui/core/CircularProgress";
import Grid from '@material-ui/core/Grid';
import Answer from "./Answer";
import Categories from "./Categories";
import Snackbar from "../snackbar/Snackbar";


class Quiz extends Component {

    state = {
        answer: '',
        category: '',
    };

    componentDidMount() {
        this.props.loadCategories();
        this.props.setTitle('Please choose category')
    }

    checkAnswer = (event) => {
        event.preventDefault();
        if (this.state.answer.trim()) {
            this.props.checkAnswer(this.state.answer, this.props.questionId, this.state.category);
            this.setState({answer: ''})
        }
    };

    handleChangeAnswer = (event) => {
        this.setState({answer: event.target.value});
    };
    handleChangeCategory = (event) => {
        this.setState({category: event.target.value});
        this.props.loadQuiz(event.target.value)
    };
    handleSkip = (event) => {
        event.preventDefault();
        this.props.skipQuestion(this.props.questionId, this.state.category);
    };

    render() {
        return (
            <Grid
              container
              spacing={0}
              direction="column"
              alignItems="center"
              justify="center"
              style={{ minHeight: '100vh', paddingTop: 64 }}
            >
                <Grid item lg={5} md={8} sm={10}>
                    <div className="BeitrisBlock">
                        <h2>{this.props.titleText}</h2>
                        <div>
                            <Categories disabled={!!this.state.loading} category={this.state.category}
                                        categories={this.props.categories}
                                        handleChangeCategory={this.handleChangeCategory}
                            />
                        </div>
                        <div>
                            {this.props.imageUrl && !this.props.loading ?
                            <img  className="QuizImage" src={this.props.imageUrl} alt={this.props.questionId} />
                            : this.props.loading ? <CircularProgress /> : null
                            }
                        </div>
                        <Answer disabled={!!this.state.loading} answer={this.state.answer} handleChangeAnswer={this.handleChangeAnswer} handleSkip={this.handleSkip} checkAnswer={this.checkAnswer}/>
                        <Snackbar open={this.props.answered} success={this.props.right} />
                    </div>
                </Grid>
            </Grid>
        );
    }
}

export default Quiz;
